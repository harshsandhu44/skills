#!/usr/bin/env python3
"""Render a deliverables markdown report to a styled, standalone HTML file.

Handles the narrow markdown subset this skill emits: h1/h2/h3, a pipe table,
blockquote, unordered list, paragraphs, and inline `code`, **bold**, [links](url).
No dependencies — the plugin ships its own renderer rather than requiring pandoc.

Usage:  md2html.py report.md [report.html]   # default: same path with .html
Prints the HTML path written.
"""
import html
import re
import sys

INLINE = [
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
]


def inline(text):
    text = html.escape(text)
    for pat, repl in INLINE:
        text = pat.sub(repl, text)
    return text


def is_table_sep(line):
    return bool(re.match(r"^\|[\s:|-]+\|$", line.strip()))


def render(md):
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
        elif s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>"); i += 1
        elif s.startswith("## "):
            out.append(f"<h2>{inline(s[3:])}</h2>"); i += 1
        elif s.startswith("# "):
            out.append(f"<h1>{inline(s[2:])}</h1>"); i += 1
        elif s.startswith(">"):
            out.append(f"<blockquote>{inline(s.lstrip('> ').rstrip())}</blockquote>"); i += 1
        elif s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(f"<li>{inline(lines[i].strip()[2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif s.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(s)
            i += 2  # skip header + separator
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            thead = "".join(f"<th>{inline(c)}</th>" for c in head)
            rows = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body
            )
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{rows}</tbody></table>")
        else:
            out.append(f"<p>{inline(s)}</p>"); i += 1
    return "\n".join(out)


TEMPLATE = """<!doctype html><meta charset=utf-8>
<title>{title}</title>
<style>
:root{{color-scheme:light dark}}
body{{font:15px/1.55 -apple-system,system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem}}
h1{{font-size:1.5rem;margin-bottom:.3rem}}
h2{{font-size:1.15rem;margin-top:2rem}}
h3{{font-size:1rem;color:#888;margin-top:1.5rem}}
table{{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.92rem}}
th,td{{text-align:left;padding:.45rem .6rem;border-bottom:1px solid #8884;vertical-align:top}}
th{{font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:#888}}
td:last-child,th:last-child{{text-align:right;font-variant-numeric:tabular-nums}}
code{{background:#8882;padding:.1em .35em;border-radius:4px;font-size:.85em}}
a{{color:#4c7cff}}
blockquote{{border-left:3px solid #8884;margin:1rem 0;padding:.2rem 0 .2rem 1rem;color:#888}}
ul{{padding-left:1.2rem}}
</style>
{body}
"""


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: md2html.py report.md [report.html]")
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else re.sub(r"\.md$", "", src) + ".html"
    md = open(src).read()
    m = re.search(r"^#\s+(.+)$", md, re.M)
    title = m.group(1).strip() if m else "Deliverables"
    with open(dst, "w") as f:
        f.write(TEMPLATE.format(title=html.escape(title), body=render(md)))
    print(dst)


if __name__ == "__main__":
    main()
