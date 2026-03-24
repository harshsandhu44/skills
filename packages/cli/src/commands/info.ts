import { existsSync } from "fs";
import { join } from "path";
import type { Command } from "commander";
import { getSkills } from "../lib/manifest.js";
import { resolveSkill, suggestSkills } from "../lib/fuzzy.js";

export function registerInfo(program: Command): void {
  program
    .command("info <name>")
    .description("Show details for a skill")
    .option("-t, --target-dir <dir>", "Directory to check for local install (default: cwd or $CLAUDE_SKILLS_DIR)")
    .action(async (name: string, opts: { targetDir?: string }) => {
      const skills = await getSkills();
      const skill = resolveSkill(name, skills);

      if (!skill) {
        const suggestions = suggestSkills(name, skills);
        if (suggestions.length > 0) {
          console.error(`Skill "${name}" not found — did you mean: ${suggestions.join(", ")}?`);
        } else {
          console.error(`Skill "${name}" not found.`);
        }
        process.exit(1);
      }

      const targetDir = opts.targetDir ?? process.env.CLAUDE_SKILLS_DIR ?? process.cwd();
      const installPath = join(targetDir, ".claude", "skills", skill.name, "SKILL.md");
      const isInstalled = existsSync(installPath);

      console.log();
      console.log(`  name        ${skill.name}`);
      console.log(`  category    ${skill.category}`);
      console.log(`  description ${skill.description}`);
      console.log(`  source      ${skill.rawUrl}`);
      console.log(`  installed   ${isInstalled ? `yes (${installPath})` : "no"}`);
      console.log();
    });
}
