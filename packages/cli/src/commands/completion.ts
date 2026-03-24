import type { Command } from "commander";
import { getSkills } from "../lib/manifest.js";

const BASH_COMPLETION = (skills: string[]) => `
# bash completion for claude-skills
_claude_skills() {
  local cur prev words
  COMPREPLY=()
  cur="\${COMP_WORDS[COMP_CWORD]}"
  prev="\${COMP_WORDS[COMP_CWORD-1]}"
  local commands="list add search info completion"
  local skills="${skills.join(" ")}"

  case "\${prev}" in
    add|info)
      COMPREPLY=( $(compgen -W "\${skills}" -- "\${cur}") )
      return 0 ;;
    search)
      return 0 ;;
    claude-skills)
      COMPREPLY=( $(compgen -W "\${commands}" -- "\${cur}") )
      return 0 ;;
  esac
}
complete -F _claude_skills claude-skills
`;

const ZSH_COMPLETION = (skills: string[]) => `
# zsh completion for claude-skills
#compdef claude-skills

_claude_skills() {
  local -a commands skills
  commands=(
    'list:List available skills'
    'add:Install one or more skills'
    'search:Search skills by name or description'
    'info:Show details for a skill'
    'completion:Print shell completion script'
  )
  skills=(${skills.map((s) => `'${s}'`).join(" ")})

  case "\$words[2]" in
    add|info)
      _describe 'skills' skills ;;
    *)
      _describe 'commands' commands ;;
  esac
}

_claude_skills
`;

export function registerCompletion(program: Command): void {
  program
    .command("completion <shell>")
    .description("Print shell completion script (bash or zsh)")
    .action(async (shell: string) => {
      const skills = await getSkills();
      const names = skills.map((s) => s.name);

      if (shell === "bash") {
        process.stdout.write(BASH_COMPLETION(names));
      } else if (shell === "zsh") {
        process.stdout.write(ZSH_COMPLETION(names));
      } else {
        console.error(`Unknown shell "${shell}". Supported: bash, zsh`);
        console.error('Usage: eval "$(claude-skills completion bash)"');
        process.exit(1);
      }
    });
}
