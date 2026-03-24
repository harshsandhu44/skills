import { readFileSync, readdirSync, writeFileSync } from "fs";
import { join } from "path";

const REPO_OWNER = "harshsandhu44";
const REPO_NAME = "skills";
const BRANCH = "main";
const BASE_RAW_URL = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}`;

interface Skill {
  name: string;
  category: string;
  description: string;
  rawUrl: string;
}

function parseFrontmatter(content: string): Record<string, string> {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const result: Record<string, string> = {};
  for (const line of match[1].split("\n")) {
    const colon = line.indexOf(":");
    if (colon === -1) continue;
    const key = line.slice(0, colon).trim();
    const value = line.slice(colon + 1).trim();
    result[key] = value;
  }
  return result;
}

const root = join(import.meta.dir, "..");
const skillsDir = join(root, "skills");
const skills: Skill[] = [];

for (const category of readdirSync(skillsDir)) {
  if (category.endsWith(".md") || category.endsWith(".json")) continue;
  const categoryPath = join(skillsDir, category);

  for (const skillDir of readdirSync(categoryPath)) {
    const skillPath = join(categoryPath, skillDir);
    const skillFile = join(skillPath, "SKILL.md");

    let content: string;
    try {
      content = readFileSync(skillFile, "utf-8");
    } catch {
      continue;
    }

    const meta = parseFrontmatter(content);
    const name = meta.name || skillDir;
    const description = meta.description || "";
    const rawUrl = `${BASE_RAW_URL}/skills/${category}/${skillDir}/SKILL.md`;

    skills.push({ name, category, description, rawUrl });
  }
}

// Sort by category then name for stable output
skills.sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name));

const manifest = {
  version: 1,
  generatedAt: new Date().toISOString(),
  skills,
};

const outPath = join(root, "skills-manifest.json");
writeFileSync(outPath, JSON.stringify(manifest, null, 2) + "\n");
console.log(`Generated ${skills.length} skills → skills-manifest.json`);
