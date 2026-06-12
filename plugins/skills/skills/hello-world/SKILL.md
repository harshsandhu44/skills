---
name: hello-world
description: Reference example skill demonstrating correct SKILL.md structure. Use when you want a template for authoring a new skill, or to verify the plugin loads.
---

# Hello World

This is a reference skill. It exists to demonstrate the structure every skill in
this plugin follows and to confirm the plugin is discovered after install.

## What a skill is

A skill is a directory containing a `SKILL.md` file with YAML frontmatter. Claude
loads the `name` and `description` of every skill up front, then reads the full
body **only when the description matches the task** — this is progressive
disclosure, and it keeps context lean.

## Frontmatter rules

- `name` — kebab-case, matches the directory name.
- `description` — one or two sentences. Lead with *what it does*, then *when to
  use it*. This is the only text Claude sees before deciding to load the skill,
  so make the trigger conditions explicit.

## Bundling extra files

A skill can ship reference docs or scripts alongside `SKILL.md`. Reference them
by relative path from the body so Claude reads them on demand rather than loading
everything at once:

```text
skills/
└── hello-world/
    ├── SKILL.md
    └── reference.md   # read when the body points to it
```

## Authoring a new skill

See [`docs/authoring-skills.md`](../../../../docs/authoring-skills.md) at the repo
root for conventions and copy-paste templates for commands, agents, hooks, and
MCP servers.
