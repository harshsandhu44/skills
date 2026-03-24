import type { Command } from "commander";
import { getSkills } from "../lib/manifest.js";

export function registerList(program: Command): void {
  program
    .command("list")
    .description("List available skills")
    .option("-c, --category <category>", "Filter by category")
    .action(async (opts: { category?: string }) => {
      const skills = await getSkills();
      const filtered = opts.category
        ? skills.filter((s) => s.category === opts.category)
        : skills;

      if (filtered.length === 0) {
        console.log(opts.category ? `No skills found in category "${opts.category}".` : "No skills found.");
        return;
      }

      const byCategory: Record<string, typeof filtered> = {};
      for (const skill of filtered) {
        (byCategory[skill.category] ??= []).push(skill);
      }

      for (const [category, categorySkills] of Object.entries(byCategory)) {
        console.log(`\n${category}`);
        const maxLen = Math.max(...categorySkills.map((s) => s.name.length));
        for (const skill of categorySkills) {
          console.log(`  ${skill.name.padEnd(maxLen + 2)}${skill.description}`);
        }
      }
      console.log();
    });
}
