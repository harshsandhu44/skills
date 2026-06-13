# harshsandhu

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

## Install

Add the marketplace, then install a plugin from it:

```text
/plugin marketplace add harshsandhu44/skills
/plugin install dev-workflow@harshsandhu
```

## Updating

Installed plugins are cached snapshots, not live links to this repo. After a
change is pushed here, pull it into an installation with:

```text
/plugin update dev-workflow@harshsandhu
```

Skills are namespaced by their plugin once installed — e.g. `grill-me` is
invoked as `claude-meta:grill-me`.

## Plugins

| Plugin | Contents | Description |
| ------ | -------- | ----------- |
| `dev-workflow` | `commit`, `review`, `branch-tests`, `tdd` | The everyday coding loop: commit, review, branch tests, and TDD. |
| `claude-meta` | `write-a-skill`, `grill-me`, `hand-off`, `caveman` | Skills for steering Claude itself: authoring, planning, handoffs, terse mode. |
| `web-perf` | `web-perf` | Analyze web performance and Core Web Vitals using Chrome DevTools. |
| `product-ops` | 6 skills + 4 agents | Turn fuzzy product ideas into shippable plans: specs, slices, API/DB design, debugging, scope cuts. |
| `release-ops` | 5 skills + 3 commands | Ship with confidence: PR write-ups, checklists, changelogs, dependency upgrades, postmortems. |
| `security-ops` | 5 skills + 3 agents + hooks | Lightweight security review: threat models, authz/rate-limit checks, secret sweeps, dependency risk. |

## Repository layout

```text
.claude-plugin/marketplace.json   # marketplace manifest
plugins/<plugin>/                  # one directory per plugin
  .claude-plugin/plugin.json       # plugin manifest
  skills/                          # SKILL.md-based skills
  commands/                        # slash commands (optional)
  agents/                          # subagents (optional)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), and [docs/authoring-skills.md](docs/authoring-skills.md)
for skill/command/agent conventions and templates.

## License

[MIT](LICENSE)
