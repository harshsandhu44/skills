#!/usr/bin/env python3
"""PreToolUse hook (Bash): hard-block a narrow, high-confidence set of
destructive commands. Exit 2 blocks the command and shows the reason to Claude;
exit 0 lets it through. Deliberately conservative — only patterns that are almost
never a legitimate intent are blocked, to keep false positives near zero.

Hook contract: receives the tool call as JSON on stdin (`tool_input.command`).
Stdlib only.
"""
import json
import re
import sys


# Targets that make `rm -rf` catastrophic.
RM_DANGER_TARGET = re.compile(
    r"\brm\s+(?:-\S+\s+)*(?:/|~|/\*|\$HOME|\${HOME})(?:\s|$)", re.I
)
RM_NO_PRESERVE = re.compile(r"\brm\b.*--no-preserve-root", re.I)

FORK_BOMB = re.compile(r":\s*\(\s*\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:")

PIPE_TO_SHELL = re.compile(
    r"\b(?:curl|wget)\b[^|]*\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b", re.I
)

DD_TO_DISK = re.compile(r"\bdd\b[^\n]*\bof=/dev/(?:sd|disk|nvme|hd|vd)", re.I)

FORCE_PUSH_MAIN = re.compile(
    r"\bgit\s+push\b[^\n]*\s(?:--force\b|-f\b)[^\n]*\b(?:main|master)\b"
    r"|\bgit\s+push\b[^\n]*\b(?:main|master)\b[^\n]*\s(?:--force\b|-f\b)",
    re.I,
)


def reason_for(cmd: str):
    if RM_NO_PRESERVE.search(cmd) or RM_DANGER_TARGET.search(cmd):
        return "recursive force-remove of a root/home path (rm -rf on / ~ or $HOME)"
    if FORK_BOMB.search(cmd):
        return "fork bomb"
    if PIPE_TO_SHELL.search(cmd):
        return "piping a downloaded script straight into a shell (curl|sh / wget|sh)"
    if DD_TO_DISK.search(cmd):
        return "dd writing directly to a disk device"
    if FORCE_PUSH_MAIN.search(cmd):
        return "force-push to main/master"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # can't parse — don't get in the way

    cmd = (data.get("tool_input") or {}).get("command", "")
    if not isinstance(cmd, str) or not cmd.strip():
        sys.exit(0)

    normalized = re.sub(r"\s+", " ", cmd)
    reason = reason_for(normalized)
    if reason:
        sys.stderr.write(
            f"Blocked by security-ops: {reason}.\n"
            f"Command: {cmd.strip()}\n"
            "If this is intentional, run it yourself outside the agent.\n"
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
