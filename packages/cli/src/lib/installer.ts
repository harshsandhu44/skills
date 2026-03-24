import { existsSync, mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import type { Skill } from "./manifest.js";

export interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
}

export async function installSkill(
  skill: Skill,
  targetDir: string = process.cwd(),
  options: InstallOptions = {}
): Promise<void> {
  const { force = false, dryRun = false } = options;
  const skillDir = join(targetDir, ".claude", "skills", skill.name);
  const skillFile = join(skillDir, "SKILL.md");

  if (!force && existsSync(skillFile)) {
    console.log(`  ⚠ ${skill.name} already installed (use --force to overwrite)`);
    return;
  }

  if (dryRun) {
    console.log(`  ~ ${skill.name} (${skill.category}) [dry run]`);
    return;
  }

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

  mkdirSync(skillDir, { recursive: true });
  writeFileSync(skillFile, content);
  console.log(`  ✓ ${skill.name} (${skill.category})`);
}
