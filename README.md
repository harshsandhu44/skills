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
/plugin install dev-workflow@harshsandhu
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
invoked as `claude-meta:grill-me`.

## Plugins

| Plugin | Contents | Description |
| ------ | -------- | ----------- |
| `dev-workflow` | `commit`, `review`, `branch-tests`, `tdd` | The everyday coding loop: commit, review, branch tests, and TDD. |
| `claude-meta` | `write-a-skill`, `grill-me`, `hand-off`, `caveman` | Skills for steering Claude itself: authoring, planning, handoffs, terse mode. |
| `web-perf` | `web-perf`, `bundle-diet`, `nextjs-perf-review`, `seo-a11y-audit`, `landing-page-roast` | Analyze and improve web performance, bundles, Next.js rendering, SEO/a11y, and conversion. |
| `product-ops` | 7 skills + 4 agents | Turn fuzzy product ideas into shippable plans: specs, slices, API/DB design, debugging, scope cuts, AI metrics. |
| `release-ops` | 5 skills + 3 commands | Ship with confidence: PR write-ups, checklists, changelogs, dependency upgrades, postmortems. |
| `security-ops` | 5 skills + 3 agents + hooks | Lightweight security review: threat models, authz/rate-limit checks, secret sweeps, dependency risk. |
| `research-lab` | 3 skills + 4 agents | Research before building: distill papers, tear down competitors, kill weak ideas, find/check evidence, size markets. |
| `field-notes` | 3 skills | Personal debriefs: F1 races, football matches, and night-sky observation sessions. |
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
