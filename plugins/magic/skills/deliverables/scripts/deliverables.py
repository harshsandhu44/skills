#!/usr/bin/env python3
"""Collect a user's git commits over a time range, grouped by referenced Jira key.

Scans one or more repos for commits by one or more authors, pulls the Jira key(s)
(pattern `ABC-123`) out of each commit message, and groups commits by ticket.
Commits with no Jira key land in a `no_ticket` bucket so nothing a user worked on
is dropped. Emits JSON on stdout; Jira enrichment + the markdown report are done
by the caller (Claude) via the Atlassian MCP.

Usage:
    deliverables.py --since "30 days ago" [--until now]
                    [--repo . | --repo owner/name | --repos a,b,c --org acme | --org acme]
                    [--author me@x.com | --author all | --authors u1,u2,...]

Repo scope and author resolution mirror the claude-vs-dev skill: local repo
(default), a remote `owner/repo`, a curated `--repos` list, or a whole GitHub org
(needs the gh CLI). Remotes are shallow-cloned once and reused across every author.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

US = "\x1f"  # unit separator (between fields)
RS = "\x1e"  # record separator (before each commit)
JIRA_KEY = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


def git(repo, args):
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True, check=True).stdout


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
    """Resolve a GitHub login to the git author email(s) it commits under, via gh."""
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
        return []
    if "@" in login or not slugs:
        return [login]
    emails = login_emails(slugs, login)
    return sorted(emails) if emails else [login]


def clone_temp(slug, since):
    """Shallow-clone a `owner/repo` (or URL) since a date into a temp dir; return its path."""
    url = slug if "://" in slug or slug.endswith(".git") else f"https://github.com/{slug}.git"
    dest = tempfile.mkdtemp(prefix="deliv-clone-")
    sh(["git", "clone", "--quiet", f"--shallow-since={since}", url, dest])
    return dest


def filters(since, until, author):
    f = [f"--since={since}"]
    if until:
        f.append(f"--until={until}")
    if author:
        pats = author if isinstance(author, (list, tuple, set)) else [author]
        f += [f"--author={p}" for p in pats]
    return f


def collect(repo, repo_label, since, until, author, tickets, no_ticket):
    """Read commits for one repo/author and file each under its Jira key(s)."""
    out = git(repo, ["log", *filters(since, until, author),
                     "--date=short", f"--pretty=format:{RS}%H{US}%ad{US}%B"])
    for record in out.split(RS):
        record = record.strip("\n")
        if not record or US not in record:
            continue
        sha, date, message = record.split(US, 2)
        subject = message.splitlines()[0] if message else ""
        entry = {"sha": sha[:12], "date": date, "subject": subject, "repo": repo_label}
        keys = sorted(set(JIRA_KEY.findall(message)))
        if keys:
            for k in keys:
                tickets[k].append(entry)
        else:
            no_ticket.append(entry)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="git date, e.g. '30 days ago' or 2026-01-01")
    ap.add_argument("--until", default="", help="git date; default now")
    ap.add_argument("--repo", default=".", help="local repo path, or remote 'owner/repo'")
    ap.add_argument("--repos", default="", help="comma-separated repos; bare names get --org prefix")
    ap.add_argument("--org", default="", help="GitHub org/user; with no --repos, ALL its repos (needs gh)")
    ap.add_argument("--author", default="", help="single author; default current git user. 'all' = everyone.")
    ap.add_argument("--authors", default="", help="comma-separated authors; one bucket per author")
    args = ap.parse_args()

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

    cleanup = []
    try:
        # Resolve scope into local repo paths (cloning remotes once) + GitHub slugs + labels.
        slugs = None
        if args.repos:
            names = [r.strip() for r in args.repos.split(",") if r.strip()]
            slugs = [n if "/" in n else f"{args.org}/{n}" for n in names]
            if any("/" not in s for s in slugs):
                sys.exit("--repos entries need an owner: pass owner/name or add --org.")
            repos = [(clone_temp(s, args.since), s) for s in slugs]
            cleanup += [p for p, _ in repos]
        elif args.org:
            slugs = org_repos(args.org)
            print(f"Scanning {len(slugs)} repos in {args.org}…", file=sys.stderr)
            repos = [(clone_temp(s, args.since), s) for s in slugs]
            cleanup += [p for p, _ in repos]
        elif "/" in args.repo and not any(
                args.repo.startswith(p) for p in ("./", "../", "/", "~")):
            slugs = [args.repo]
            repos = [(clone_temp(args.repo, args.since), args.repo)]
            cleanup += [p for p, _ in repos]
        else:
            repos = [(args.repo, args.repo)]

        result = {"since": args.since, "until": args.until or "now",
                  "repos": [label for _, label in repos], "authors": []}
        for login in author_list:
            patterns = resolve_author(login, slugs)
            tickets = defaultdict(list)
            no_ticket = []
            for path, label in repos:
                collect(path, label, args.since, args.until, patterns, tickets, no_ticket)
            total = sum(len(v) for v in tickets.values()) + len(no_ticket)
            result["authors"].append({
                "label": login or "all",
                "commit_total": total,
                "ticket_keys": sorted(tickets.keys()),
                "tickets": dict(tickets),
                "no_ticket": no_ticket,
            })
    except subprocess.CalledProcessError as e:
        sys.exit(e.stderr or str(e))
    finally:
        for d in cleanup:
            shutil.rmtree(d, ignore_errors=True)

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
