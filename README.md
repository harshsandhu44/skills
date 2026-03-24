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
    coding/       -> debug, implement, review, test, simplify
    product/      -> user stories, acceptance criteria
    qa/           -> test plans, edge case analysis
    repo/         -> branch review, PR descriptions, issue writing
    writing/      -> commits, PRs, status updates

  Filenames: lowercase-kebab-case/SKILL.md
</pre>

<pre>
Skills:

  coding/
    debug-issue              debug a bug with reproduction steps and a minimal fix
    implement-from-ticket    implement a feature from ticket text (Jira, Linear, GitHub)
    reduce-complexity        simplify complex code while preserving behavior
    review-changed-files     review only branch-modified files for bugs and risks
    write-tests              write or update tests for branch-modified files

  product/
    create-acceptance-criteria   create testable acceptance criteria from requirements
    write-user-stories           turn a feature idea into structured user stories

  qa/
    edge-case-hunter         identify edge cases and failure modes before release
    test-plan                create a practical test plan for a feature or release

  repo/
    branch-review            holistic review of a branch before merge
    issue-writer             turn rough problems into clear GitHub/Linear issues
    pr-description           write a clear PR description from branch changes

  writing/
    commit                   review changes and create a clean commit
    pr                       create a pull request with a strong title and description
    write-status-update      turn raw notes into a stakeholder-ready status update
</pre>

<pre>
Install with the CLI (recommended):

  npm install -g @harshsandhu44/skills-cli

  claude-skills list
  claude-skills add debug-issue
  claude-skills add --category coding
  claude-skills add --all
</pre>

<pre>
Install manually:
  Skills live in .claude/skills/ inside any repo. To add one:

  mkdir -p .claude/skills/debug-issue
  curl -o .claude/skills/debug-issue/SKILL.md \
    https://raw.githubusercontent.com/harshsandhu44/skills/main/skills/coding/debug-issue/SKILL.md

  Then invoke it in Claude Code with:
    /debug-issue
</pre>

<pre>
Adding a new skill to this library:
  1. pick a category under skills/
  2. create a directory with a clear name
  3. add a SKILL.md with frontmatter: name, description
  4. define: purpose, when to use, instructions, output style
</pre>

<p align="center"><code>organized prompts, consistent results</code></p>
