# Contributing

Thanks for contributing! This repo is a Claude Code plugin marketplace. Most
contributions add a **skill**, **command**, or **agent** to the `skills` plugin.

## Add a skill

1. Create `plugins/skills/skills/<your-skill>/SKILL.md`.
2. Use kebab-case for the directory and the frontmatter `name` (they must match).
3. Write a `description` that says *what it does* and *when to use it* — this is
   all Claude sees before loading the skill.
4. See [docs/authoring-skills.md](docs/authoring-skills.md) for the full
   conventions and templates (including commands, agents, hooks, and MCP).

## Validate locally

Before opening a PR, validate the manifests the same way CI does:

```bash
claude plugin validate . --strict
claude plugin validate plugins/skills --strict
```

Lint the markdown:

```bash
npx markdownlint-cli2 "**/*.md"
```

## Commits & PRs

- Use clear, imperative commit messages (e.g. `add foo skill`).
- One logical change per PR.
- Bump `version` in `plugins/skills/.claude-plugin/plugin.json` and add a
  [CHANGELOG.md](CHANGELOG.md) entry when releasing.
