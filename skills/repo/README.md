<div align="center">
<pre>
repo skills
Claude prompts for Git and repository workflow tasks
</pre>
</div>

<pre>
Skills:

  branch-review
    holistic review of the current branch — intent, changed areas,
    risk level, test coverage, and merge readiness

  issue-writer
    turn a rough problem statement, bug, or idea into a clear issue
    with context, scope, and expected outcome

  pr-description
    write a clear pull request description from branch changes,
    commit history, ticket text, or notes
</pre>

<pre>
Add a skill to your project:

  npm install -g @skills/cli
  claude-skills add pr-description

  or manually:

  mkdir -p .claude/skills/pr-description
  curl -o .claude/skills/pr-description/SKILL.md \
    https://raw.githubusercontent.com/harshsandhu44/skills/main/skills/repo/pr-description/SKILL.md

  Replace pr-description with any skill name above.
</pre>

<p align="center"><code>../README.md for full library index</code></p>
