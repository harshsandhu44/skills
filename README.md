# harshsandhu

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace —
a collection of **skills, slash commands, and subagents** that teach Claude how to
do specific jobs well: ship code, review for security, plan features, audit web
performance, and more.

Each plugin is a small, focused bundle. Install only the ones you want; they layer
onto Claude Code without changing how you already work. Browse the [Plugins](#plugins)
table to see what's on offer.

**Who this is for:** anyone using Claude Code who wants sharper, repeatable help on
a recurring task — and contributors who want to add their own.

**Requirements:** [Claude Code](https://docs.claude.com/en/docs/claude-code)
installed and authenticated. That's it.

## Install

In Claude Code, add this marketplace once, then install any plugin from it:

```text
/plugin marketplace add harshsandhu44/skills
/plugin install code@harshsandhu
```

Installed skills become available automatically — Claude loads the right one when
your request matches its description, or you can invoke it directly (see
[namespacing](#updating)).

## Updating

Installed plugins are cached snapshots, not live links to this repo. After a
change is pushed here, refresh the marketplace and reload to pull it in:

```text
/plugin marketplace update harshsandhu
/reload-plugins
```

Refreshing the marketplace updates its installed plugins to their latest
version. To do this automatically at startup, enable auto-update for the
marketplace from the **Marketplaces** tab in `/plugin` (it's off by default for
third-party marketplaces).

Skills are namespaced by their plugin once installed — e.g. `grill-me` is
invoked as `notes:grill-me`.

## Plugins

| Plugin | Contents | Description |
| ------ | -------- | ----------- |
| `code` | 26 skills + 7 agents + 3 commands + hooks | The full code lifecycle: commit/review/test/TDD, PR write-ups and release checklists, product specs and API/DB design, web performance, and security review with guardrail hooks. |
| `notes` | 10 skills + 4 agents | Steer Claude and think before you build: skill authoring, planning, handoffs, terse mode; research and validation; plus personal debriefs for F1, football, and the night sky. |
| `magic` | `claude-vs-dev`, `deliverables` | Org tooling over the GitHub + Atlassian (Jira) MCP servers: split human vs Claude-assisted commits, and map a contributor's commits to the Jira tickets they delivered. |

## Repository layout

```text
.claude-plugin/marketplace.json   # marketplace manifest
plugins/<plugin>/                  # one directory per plugin
  .claude-plugin/plugin.json       # plugin manifest
  skills/                          # SKILL.md-based skills
  commands/                        # slash commands (optional)
  agents/                          # subagents (optional)
  hooks/hooks.json                 # event hooks (optional)
```

## Contributing

Contributions are welcome — a useful skill can be a single Markdown file. The
fastest path: fork, add a `SKILL.md` under the relevant `plugins/<plugin>/skills/`,
and open a PR.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the step-by-step (and how to validate
locally), and [docs/authoring-skills.md](docs/authoring-skills.md) for the full
skill/command/agent conventions and templates.

## License

[MIT](LICENSE)
