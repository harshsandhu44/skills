import type { Command } from "commander";
import { getSkills, type Skill } from "../lib/manifest.js";
import { installSkill } from "../lib/installer.js";

export function registerAdd(program: Command): void {
  program
    .command("add [names...]")
    .description("Install one or more skills into .claude/skills/")
    .option("-a, --all", "Install all available skills")
    .option("-c, --category <category>", "Install all skills in a category")
    .action(async (names: string[], opts: { all?: boolean; category?: string }) => {
      const skills = await getSkills();
      let toInstall: Skill[];

      if (opts.all) {
        toInstall = skills;
        console.log(`Installing all ${skills.length} skills...`);
      } else if (opts.category) {
        toInstall = skills.filter((s) => s.category === opts.category);
        if (toInstall.length === 0) {
          console.error(`No skills found in category "${opts.category}".`);
          console.error(`Available categories: ${[...new Set(skills.map((s) => s.category))].sort().join(", ")}`);
          process.exit(1);
        }
        console.log(`Installing ${toInstall.length} skills from "${opts.category}"...`);
      } else if (names.length > 0) {
        toInstall = [];
        for (const name of names) {
          const skill = skills.find((s) => s.name === name);
          if (!skill) {
            console.warn(`  ⚠ Unknown skill "${name}" — skipping`);
          } else {
            toInstall.push(skill);
          }
        }
        if (toInstall.length === 0) {
          process.exit(1);
        }
      } else {
        console.error("Specify skill names, --all, or --category <category>.");
        console.error("Example: claude-skills add debug-issue");
        process.exit(1);
      }

      let failed = 0;
      for (const skill of toInstall) {
        try {
          await installSkill(skill);
        } catch (err) {
          console.error(`  ✗ ${(err as Error).message}`);
          failed++;
        }
      }

      const installed = toInstall.length - failed;
      console.log(`\nInstalled ${installed} skill${installed === 1 ? "" : "s"} to .claude/skills/`);
      if (failed > 0) process.exit(1);
    });
}
