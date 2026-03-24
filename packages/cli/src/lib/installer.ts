import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import type { Skill } from "./manifest.js";

export async function installSkill(skill: Skill, targetDir: string = process.cwd()): Promise<void> {
  let content: string;
  try {
    const res = await fetch(skill.rawUrl);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status} ${res.statusText}`);
    }
    content = await res.text();
  } catch (err) {
    throw new Error(`Failed to download ${skill.name}: ${(err as Error).message}`);
  }

  const skillDir = join(targetDir, ".claude", "skills", skill.name);
  mkdirSync(skillDir, { recursive: true });
  writeFileSync(join(skillDir, "SKILL.md"), content);
  console.log(`  ✓ ${skill.name} (${skill.category})`);
}
