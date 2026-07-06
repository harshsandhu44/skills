#!/usr/bin/env python3
"""Compare developer vs Claude-assisted commits over a time range and write an HTML report.

A commit is "Claude-assisted" when its message has a `Co-Authored-By:` trailer
naming Claude. Everything else is "developer".

Usage:
    report.py --since "30 days ago" [--until now]
              [--repo . | --repo owner/name | --repos a,b,c --org acme | --org acme]
              [--author me@x.com | --author all | --authors u1,u2,...]
              [--out-dir DIR] [--open]

Repo scope: local repo (default), a remote `owner/repo`, a curated `--repos`
list, or a whole GitHub org (needs the gh CLI). Remote repos are shallow-cloned
once and reused across every author. With `--authors`, writes one HTML report
per user. Prints one `author<TAB>path` line per report written.
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

US = "\x1f"  # unit separator
RS = "\x1e"  # record separator


def git(repo, args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, check=True,
    ).stdout


def sh(args):
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def org_repos(org):
    """List `owner/repo` slugs for a GitHub org/user via the gh CLI."""
    if not shutil.which("gh"):
        sys.exit("--org needs the GitHub CLI (`gh`) installed and authenticated.")
    out = sh(["gh", "repo", "list", org, "--no-archived", "--limit", "500",
              "--json", "nameWithOwner", "--jq", ".[].nameWithOwner"])
    slugs = [s for s in out.splitlines() if s.strip()]
    if not slugs:
        sys.exit(f"No repositories found for org/user '{org}'.")
    return slugs


def login_emails(slugs, login):
    """Resolve a GitHub login to the git author email(s) it commits under, via gh.

    GitHub maps commits to a login by email, so a login rarely appears in the git
    author string itself — we ask the API which emails belong to it.
    """
    emails = set()
    for slug in slugs:
        try:
            out = sh(["gh", "api", f"/repos/{slug}/commits?author={login}&per_page=100",
                      "--jq", ".[].commit.author.email"])
        except subprocess.CalledProcessError:
            continue
        emails.update(e for e in out.splitlines() if e.strip())
    return emails


def resolve_author(login, slugs):
    """Turn a user token into git --author pattern(s). '' = all; email/name used as-is."""
    if not login:
        return []            # everyone
    if "@" in login or not slugs:
        return [login]       # already an email, or no GitHub API scope → substring match
    emails = login_emails(slugs, login)
    return sorted(emails) if emails else [login]


def clone_temp(slug, since):
    """Shallow-clone a `owner/repo` (or URL) since a date into a temp dir; return its path."""
    url = slug if "://" in slug or slug.endswith(".git") else f"https://github.com/{slug}.git"
    dest = tempfile.mkdtemp(prefix="cvd-clone-")
    sh(["git", "clone", "--quiet", f"--shallow-since={since}", url, dest])
    return dest


def analyze(repo, since, until, author):
    """Return (commit_total, stats, authors) for one local repo."""
    is_claude = classify(repo, since, until, author)
    stats = collect(repo, since, until, author, is_claude)
    authors = author_split(repo, since, until, author, is_claude)
    total = stats["claude"]["commits"] + stats["dev"]["commits"]
    return total, stats, authors


def aggregate(repo_paths, since, until, author):
    """Sum analyze() across several local repos. Returns (total, stats, authors)."""
    stats = {"claude": {"commits": 0, "added": 0, "removed": 0, "files": 0},
             "dev": {"commits": 0, "added": 0, "removed": 0, "files": 0}}
    authors = defaultdict(lambda: {"claude": 0, "dev": 0})
    total = 0
    for path in repo_paths:
        t, st, au = analyze(path, since, until, author)
        total += t
        for b in ("claude", "dev"):
            for k in stats[b]:
                stats[b][k] += st[b][k]
        for name, v in au.items():
            authors[name]["claude"] += v["claude"]
            authors[name]["dev"] += v["dev"]
    return total, stats, authors


def open_in_browser(path):
    opener = ("open" if sys.platform == "darwin"
              else "start" if sys.platform.startswith("win")
              else "xdg-open")
    if shutil.which(opener) or opener == "start":
        subprocess.run([opener, path], check=False, shell=(opener == "start"))


def slug(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-") or "all"


def filters(since, until, author):
    """author may be a string, a list of patterns (OR-matched by git), or falsy (all)."""
    f = [f"--since={since}"]
    if until:
        f.append(f"--until={until}")
    if author:
        pats = author if isinstance(author, (list, tuple, set)) else [author]
        f += [f"--author={p}" for p in pats]
    return f


def classify(repo, since, until, author):
    """Return {hash: is_claude} using the Co-Authored-By trailer."""
    out = git(repo, [
        "log", *filters(since, until, author),
        f"--pretty=format:%H{US}%(trailers:key=Co-authored-by,valueonly)",
    ])
    result = {}
    for line in out.splitlines():
        if US not in line:
            continue
        h, coauthors = line.split(US, 1)
        result[h] = "claude" in coauthors.lower()
    return result


def collect(repo, since, until, author, is_claude):
    """Aggregate commit count and line churn per bucket."""
    out = git(repo, ["log", *filters(since, until, author),
                     f"--pretty=format:{RS}%H", "--numstat"])

    stats = {
        "claude": {"commits": 0, "added": 0, "removed": 0, "files": 0},
        "dev": {"commits": 0, "added": 0, "removed": 0, "files": 0},
    }
    authors = defaultdict(lambda: {"claude": 0, "dev": 0})
    bucket = None
    for line in out.split("\n"):
        if line.startswith(RS):
            h = line[1:].strip()
            bucket = "claude" if is_claude.get(h) else "dev"
            stats[bucket]["commits"] += 1
        elif line.strip() and bucket:
            parts = line.split("\t")
            if len(parts) == 3:
                added, removed, _ = parts
                stats[bucket]["files"] += 1
                stats[bucket]["added"] += int(added) if added.isdigit() else 0
                stats[bucket]["removed"] += int(removed) if removed.isdigit() else 0
    return stats


def author_split(repo, since, until, author, is_claude):
    """Per-author commit counts split by bucket."""
    out = git(repo, ["log", *filters(since, until, author),
                     f"--pretty=format:%H{US}%an"])
    authors = defaultdict(lambda: {"claude": 0, "dev": 0})
    for line in out.splitlines():
        if US not in line:
            continue
        h, name = line.split(US, 1)
        authors[name]["claude" if is_claude.get(h) else "dev"] += 1
    return authors


def bar(claude, dev):
    total = claude + dev
    pct = round(100 * claude / total) if total else 0
    return pct


def render(repo, since, until, author, stats, authors):
    c, d = stats["claude"], stats["dev"]
    tc = c["commits"] + d["commits"]
    ta = c["added"] + d["added"]
    esc = html.escape

    def row(label, cv, dv):
        tot = cv + dv
        pct = round(100 * cv / tot) if tot else 0
        return (f"<tr><td>{esc(label)}</td>"
                f"<td class=n>{dv:,}</td>"
                f"<td class=n>{cv:,}</td>"
                f"<td class=n>{tot:,}</td>"
                f"<td class=bar><span style='width:{pct}%'></span><em>{pct}%</em></td></tr>")

    author_rows = "".join(
        f"<tr><td>{esc(name)}</td><td class=n>{v['dev']:,}</td>"
        f"<td class=n>{v['claude']:,}</td>"
        f"<td class=n>{v['dev'] + v['claude']:,}</td></tr>"
        for name, v in sorted(authors.items(),
                              key=lambda kv: -(kv[1]['dev'] + kv[1]['claude']))
    )

    who = f" &middot; author: {esc(author)}" if author else " &middot; all authors"
    window = f"{esc(since)} → {esc(until or 'now')}"
    return f"""<!doctype html><meta charset=utf-8>
<title>Claude vs Developer commits</title>
<style>
:root{{color-scheme:light dark}}
body{{font:15px/1.5 -apple-system,system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem}}
h1{{font-size:1.4rem;margin-bottom:.2rem}}
.sub{{color:#888;margin-top:0}}
table{{border-collapse:collapse;width:100%;margin:1.2rem 0}}
th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid #8884}}
th{{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#888}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
td.bar{{position:relative;width:160px}}
td.bar span{{display:inline-block;height:14px;background:#7c5cff;border-radius:3px;vertical-align:middle}}
td.bar em{{margin-left:.4rem;font-style:normal;font-size:.8rem;color:#888}}
.cards{{display:flex;gap:1rem;flex-wrap:wrap}}
.card{{flex:1;min-width:160px;border:1px solid #8884;border-radius:8px;padding:1rem}}
.card b{{font-size:1.8rem;display:block}}
.card small{{color:#888}}
</style>
<h1>Claude-assisted vs Developer commits</h1>
<p class=sub>{esc(repo)} &middot; {window}{who}</p>
<div class=cards>
  <div class=card><b>{tc:,}</b><small>total commits</small></div>
  <div class=card><b>{c['commits']:,}</b><small>Claude-assisted ({round(100*c['commits']/tc) if tc else 0}%)</small></div>
  <div class=card><b>{d['commits']:,}</b><small>developer-only</small></div>
</div>
<table>
<tr><th>Metric</th><th>Developer</th><th>Claude-assisted</th><th>Total</th><th>Claude share</th></tr>
{row("Commits", c['commits'], d['commits'])}
{row("Files changed", c['files'], d['files'])}
{row("Lines added", c['added'], d['added'])}
{row("Lines removed", c['removed'], d['removed'])}
</table>
<h2 style="font-size:1rem">By author</h2>
<table>
<tr><th>Author</th><th>Dev commits</th><th>Claude-assisted</th><th>Total</th></tr>
{author_rows}
</table>
<p class=sub>Claude-assisted = commit message carries a <code>Co-Authored-By: Claude</code> trailer.</p>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="git date, e.g. '30 days ago' or 2026-01-01")
    ap.add_argument("--until", default="", help="git date; default now")
    ap.add_argument("--repo", default=".",
                    help="local repo path (default), or a remote 'owner/repo' to shallow-clone")
    ap.add_argument("--repos", default="",
                    help="comma-separated repo list; bare names are prefixed with --org")
    ap.add_argument("--org", default="",
                    help="GitHub org/user; with no --repos, analyze ALL its repos (needs gh)")
    ap.add_argument("--out-dir", default="",
                    help="directory for the HTML reports (default: a temp dir)")
    ap.add_argument("--author", default="",
                    help="single author (git name, email, or GitHub username); "
                         "default is the current git user. Pass 'all' for everyone.")
    ap.add_argument("--authors", default="",
                    help="comma-separated authors; writes one HTML report per author")
    ap.add_argument("--open", action="store_true", help="open each report in the default browser")
    args = ap.parse_args()

    # Resolve the list of authors to report on (one HTML each). "" means all authors.
    if args.authors:
        author_list = [a.strip() for a in args.authors.split(",") if a.strip()]
    elif args.author == "all":
        author_list = [""]
    elif args.author:
        author_list = [args.author]
    else:
        try:
            me = git(".", ["config", "user.email"]).strip()
        except subprocess.CalledProcessError:
            me = ""
        if not me:
            sys.exit("No --author/--authors given and git user.email is unset.")
        author_list = [me]

    out_dir = args.out_dir or tempfile.mkdtemp(prefix="claude-vs-dev-")
    os.makedirs(out_dir, exist_ok=True)

    cleanup = []
    try:
        # Resolve the scope into local repo paths (cloning remotes once) + GitHub slugs.
        slugs = None
        if args.repos:
            names = [r.strip() for r in args.repos.split(",") if r.strip()]
            slugs = [n if "/" in n else f"{args.org}/{n}" for n in names]
            if any("/" not in s for s in slugs):
                sys.exit("--repos entries need an owner: pass owner/name or add --org.")
            scope = f"{args.org or 'repos'}: {', '.join(n.split('/')[-1] for n in slugs)}"
            repos = [clone_temp(s, args.since) for s in slugs]
            cleanup += repos
        elif args.org:
            slugs = org_repos(args.org)
            print(f"Analyzing {len(slugs)} repos in {args.org}…", file=sys.stderr)
            scope = f"org: {args.org} ({len(slugs)} repos)"
            repos = [clone_temp(s, args.since) for s in slugs]
            cleanup += repos
        elif "/" in args.repo and not any(
                args.repo.startswith(p) for p in ("./", "../", "/", "~")):
            scope = args.repo
            slugs = [args.repo]
            repos = [clone_temp(args.repo, args.since)]
            cleanup += repos
        else:
            scope = args.repo
            repos = [args.repo]

        # One report per author, reusing the already-cloned repos. For GitHub logins,
        # resolve the login to its commit email(s) so real-name identities still match.
        results = []
        for login in author_list:
            patterns = resolve_author(login, slugs)
            total, stats, authors = aggregate(repos, args.since, args.until, patterns)
            label = login or "all"
            if total == 0:
                print(f"[{label}] no matching commits in that range.", file=sys.stderr)
                continue
            out = os.path.join(out_dir, f"claude-vs-dev-{slug(label)}.html")
            with open(out, "w") as f:
                f.write(render(scope, args.since, args.until, label if login else "",
                               stats, authors))
            results.append((label, out))
    except subprocess.CalledProcessError as e:
        sys.exit(e.stderr or str(e))
    finally:
        for d in cleanup:
            shutil.rmtree(d, ignore_errors=True)

    if not results:
        sys.exit(2)
    for label, out in results:
        if args.open:
            open_in_browser(out)
        print(f"{label}\t{out}")


if __name__ == "__main__":
    main()
