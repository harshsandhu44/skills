<div align="center">
<pre>
writing skills
Claude prompts for technical writing and communication
</pre>
</div>

<pre>
Skills:

  commit
    review current git changes, validate them, and create
    a clean conventional commit

  pr
    create a pull request from the current branch with a
    strong title and description

  write-status-update
    turn raw notes, tickets, commits, or progress bullets
    into a clear stakeholder-ready status update
</pre>

<pre>
Add a skill to your project:

  npm install -g @harshsandhu44/skills-cli
  claude-skills add commit

  or manually:

  mkdir -p .claude/skills/commit
  curl -o .claude/skills/commit/SKILL.md \
    https://raw.githubusercontent.com/harshsandhu44/skills/main/skills/writing/commit/SKILL.md

  Replace commit with any skill name above.
</pre>

<p align="center"><code>../README.md for full library index</code></p>
