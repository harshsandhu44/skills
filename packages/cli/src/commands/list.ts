import type { Command } from "commander";
import { getSkills } from "../lib/manifest.js";

const BOLD = process.stdout.isTTY ? "\x1b[1m" : "";
const RESET = process.stdout.isTTY ? "\x1b[0m" : "";

export function registerList(program: Command): void {
  program
    .command("list")
    .description("List available skills")
    .option("-c, --category <category>", "Filter by category")
    .option("-j, --json", "Output as JSON")
    .action(async (opts: { category?: string; json?: boolean }) => {
      const skills = await getSkills();
      const filtered = opts.category
        ? skills.filter((s) => s.category === opts.category)
        : skills;

      if (filtered.length === 0) {
        console.log(opts.category ? `No skills found in category "${opts.category}".` : "No skills found.");
        return;
      }

      if (opts.json) {
        console.log(JSON.stringify(filtered, null, 2));
        return;
      }

      const byCategory: Record<string, typeof filtered> = {};
      for (const skill of filtered) {
        (byCategory[skill.category] ??= []).push(skill);
      }

      for (const [category, categorySkills] of Object.entries(byCategory).sort(([a], [b]) =>
        a.localeCompare(b)
      )) {
        console.log(`\n${BOLD}${category}${RESET}`);
        const maxLen = Math.max(...categorySkills.map((s) => s.name.length));
        for (const skill of categorySkills.sort((a, b) => a.name.localeCompare(b.name))) {
          console.log(`  ${skill.name.padEnd(maxLen + 2)}${skill.description}`);
        }
      }
      console.log();
    });
}
