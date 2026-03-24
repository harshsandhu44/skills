import type { Command } from "commander";
import { getSkills } from "../lib/manifest.js";

export function registerSearch(program: Command): void {
  program
    .command("search <query>")
    .description("Search skills by name or description")
    .action(async (query: string) => {
      const skills = await getSkills();
      const q = query.toLowerCase();
      const results = skills.filter(
        (s) => s.name.toLowerCase().includes(q) || s.description.toLowerCase().includes(q)
      );

      if (results.length === 0) {
        console.log(`No skills matched "${query}".`);
        return;
      }

      const maxLen = Math.max(...results.map((s) => s.name.length));
      console.log();
      for (const skill of results) {
        console.log(`  ${skill.name.padEnd(maxLen + 2)}[${skill.category}] ${skill.description}`);
      }
      console.log();
    });
}
