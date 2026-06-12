# harshsandhu

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

## Install

Add the marketplace, then install a plugin from it:

```text
/plugin marketplace add harshsandhu44/skills
/plugin install dev-workflow@harshsandhu
```

## Plugins

| Plugin | Skills | Description |
| ------ | ------ | ----------- |
| `dev-workflow` | `commit`, `review`, `branch-tests`, `tdd` | The everyday coding loop: commit, review, branch tests, and TDD. |
| `claude-meta` | `write-a-skill`, `grill-me`, `hand-off`, `caveman` | Skills for steering Claude itself: authoring, planning, handoffs, terse mode. |
| `web-perf` | `web-perf` | Analyze web performance and Core Web Vitals using Chrome DevTools. |

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
