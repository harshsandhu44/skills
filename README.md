# harshsandhu

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

## Install

Add the marketplace, then install a plugin from it:

```text
/plugin marketplace add harshsandhu44/skills
/plugin install skills@harshsandhu
```

## Plugins

| Plugin   | Description                                                  |
| -------- | ----------------------------------------------------------- |
| `skills` | A collection of Claude Code skills, commands, and agents.   |

## Repository layout

```text
.claude-plugin/marketplace.json   # marketplace manifest
plugins/<plugin>/                  # one directory per plugin
  .claude-plugin/plugin.json       # plugin manifest
  skills/                          # SKILL.md-based skills
  commands/                        # slash commands
  agents/                          # subagents
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), and [docs/authoring-skills.md](docs/authoring-skills.md)
for skill/command/agent conventions and templates.

## License

[MIT](LICENSE)
