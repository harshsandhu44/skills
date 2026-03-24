const MANIFEST_URL =
  "https://raw.githubusercontent.com/harshsandhu44/skills/main/skills-manifest.json";

export interface Skill {
  name: string;
  category: string;
  description: string;
  rawUrl: string;
}

interface Manifest {
  version: number;
  generatedAt: string;
  skills: Skill[];
}

let cached: Skill[] | null = null;

export async function getSkills(): Promise<Skill[]> {
  if (cached) return cached;

  let res: Response;
  try {
    res = await fetch(MANIFEST_URL);
  } catch {
    throw new Error("Could not reach skills registry. Check your internet connection.");
  }

  if (!res.ok) {
    throw new Error(`Failed to fetch skills manifest: ${res.status} ${res.statusText}`);
  }

  const manifest: Manifest = await res.json();
  cached = manifest.skills;
  return cached;
}

export async function getCategories(): Promise<string[]> {
  const skills = await getSkills();
  return [...new Set(skills.map((s) => s.category))].sort();
}
