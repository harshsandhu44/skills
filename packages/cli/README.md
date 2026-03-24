<div align="center">
<pre>
@skills/cli
install Claude Code skills from the community library
</pre>
</div>

<pre>
A CLI for adding skills to any repo. Skills are markdown files that tell
Claude how to behave for a specific task — drop them in, invoke by name.
</pre>

<pre>
Install:

  npm install -g @skills/cli
</pre>

<pre>
Usage:

  claude-skills list                       list all available skills
  claude-skills list --category coding     list skills in a category
  claude-skills search <query>             search by name or description
  claude-skills add <name>                 install a skill
  claude-skills add <name> <name> ...      install multiple skills
  claude-skills add --category <category>  install all skills in a category
  claude-skills add --all                  install all 15 skills
</pre>

<pre>
Skills are installed to .claude/skills/<name>/SKILL.md in your current directory.
Invoke any installed skill in Claude Code with /<name>.

  claude-skills add debug-issue
  -> .claude/skills/debug-issue/SKILL.md

  /debug-issue   (in Claude Code)
</pre>

<pre>
Categories:

  coding     debug, implement, review, test, simplify
  product    user stories, acceptance criteria
  qa         test plans, edge case analysis
  repo       branch review, PR descriptions, issue writing
  writing    commits, PRs, status updates
</pre>

<p align="center"><code>github.com/harshsandhu44/skills for the full skill library</code></p>
