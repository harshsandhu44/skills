#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write): scan the just-written file for likely secrets and
warn. Non-blocking by design — the write already happened in PostToolUse, so the
honest model is to surface a warning, not pretend to prevent it. Always exits 0.

Hook contract: receives the tool call as JSON on stdin. We read the file at
`tool_input.file_path` (falling back to the inline content the tool reported).
Stdlib only.
"""
import json
import os
import re
import sys


# (label, pattern). High-signal, low-false-positive secret shapes.
PATTERNS = [
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("OpenAI/Stripe-style secret key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Hardcoded credential", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*"
        r"['\"][^'\"\s]{16,}['\"]"
    )),
]


def get_text(data):
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path")
    if path and os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                return path, fh.read()
        except OSError:
            pass
    # Fall back to whatever content the tool reported inline.
    text = ti.get("content") or ti.get("new_string") or ""
    return path, text


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    path, text = get_text(data)
    if not text:
        sys.exit(0)

    hits = []
    for label, pat in PATTERNS:
        if pat.search(text):
            hits.append(label)

    if hits:
        where = path or "the edited file"
        sys.stderr.write(
            "security-ops: possible secret(s) detected in "
            f"{where}: {', '.join(sorted(set(hits)))}.\n"
            "If real, remove it, rotate the key, and move it to a secret store / env var.\n"
        )
    sys.exit(0)  # never block — the write already happened


if __name__ == "__main__":
    main()
