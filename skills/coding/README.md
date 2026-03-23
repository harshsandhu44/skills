<div align="center">
<pre>
coding skills
Claude prompts for software engineering tasks
</pre>
</div>

<pre>
Skills:

  debug-issue
    debug a bug with reproduction steps, code path tracing,
    and the smallest safe fix

  implement-from-ticket
    implement a feature or fix from ticket text (Jira, Linear, GitHub issue)
    keeping scope tight and matching local conventions

  reduce-complexity
    simplify overly complex code while preserving behavior —
    functions, components, modules, or flows

  review-changed-files
    review only files modified in the current branch for bugs,
    regressions, edge cases, and missing validation

  write-tests
    write or update tests for branch-modified files using the
    repo's existing testing library and conventions
</pre>

<pre>
Add a skill to your project:

  mkdir -p .claude/skills/debug-issue
  curl -o .claude/skills/debug-issue/SKILL.md \
    https://raw.githubusercontent.com/harshsandhu44/claude-skills/main/skills/coding/debug-issue/SKILL.md

  Replace debug-issue with any skill name above.
</pre>

<p align="center"><code>../README.md for full library index</code></p>
