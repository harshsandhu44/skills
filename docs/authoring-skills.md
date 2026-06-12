# Authoring skills, commands, agents, hooks & MCP

This plugin auto-discovers components by directory. Drop a file in the right
place and it loads — no manifest edits needed.

## Skills — `plugins/skills/skills/<name>/SKILL.md`

```markdown
---
name: my-skill
description: What it does, and when Claude should use it. Be explicit about triggers.
---

# My Skill

Body is loaded only when the description matches the task (progressive
disclosure). Keep the description sharp; keep the body focused.
```

- Directory name == frontmatter `name`, kebab-case.
- Bundle reference docs/scripts in the same folder and link them by relative
  path so they're read on demand.

## Commands — `plugins/skills/commands/<name>.md`

User-invoked slash commands. The body is the prompt; frontmatter is optional.

```markdown
---
description: One line shown in the /command picker.
---

Do the thing the user asked, using $ARGUMENTS.
```

## Agents — `plugins/skills/agents/<name>.md`

Subagents Claude can delegate to.

```markdown
---
name: my-agent
description: When to delegate to this agent.
tools: Read, Grep, Glob
---

System prompt for the agent.
```

## Hooks — `plugins/skills/hooks/hooks.json`

Add this file only when you have a real hook (an empty one trips `--strict`).

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "echo edited" }]
      }
    ]
  }
}
```

## MCP servers — `plugins/skills/.mcp.json`

Add only when bundling a real MCP server.

```json
{
  "mcpServers": {
    "my-server": { "command": "npx", "args": ["-y", "@scope/server"] }
  }
}
```

## Validate

```bash
claude plugin validate plugins/skills --strict
```
