<div align="center">
<pre>
claude-skills
a personal library of reusable Claude skill prompts
</pre>
</div>

<pre>
Skills are markdown files that define how Claude should behave for a specific task.
Drop one into a Claude conversation to get consistent, focused output every time.
</pre>

<pre>
Structure:
  skills/
    coding/       -> debugging, refactoring, code review
    product/      -> PRDs, specs, strategy
    writing/      -> technical docs, copy, editing

  Filenames: lowercase-kebab-case.md
</pre>

<pre>
Adding a skill:
  1. pick a category under skills/
  2. create a .md file with a clear name
  3. define: purpose, when to use, instructions, output style
</pre>

<pre>
Fetching a skill via raw URL:
  https://raw.githubusercontent.com/harshsandhu44/claude-skills/main/skills/{category}/{skill-name}.md

  Example:
  https://raw.githubusercontent.com/harshsandhu44/claude-skills/main/skills/coding/react-debugging.md
</pre>

<p align="center"><code>organized prompts, consistent results</code></p>
