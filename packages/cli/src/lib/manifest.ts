import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";

const MANIFEST_URL =
  "https://raw.githubusercontent.com/harshsandhu44/skills/main/skills-manifest.json";

const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

function getCachePath(): string {
  return join(homedir(), ".cache", "skills-cli", "manifest.json");
}

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

interface DiskCache {
  cachedAt: string;
  manifest: Manifest;
}

export function validateManifest(data: unknown): Manifest {
  if (typeof data !== "object" || data === null) {
    throw new Error("Invalid manifest: expected an object.");
  }
  const obj = data as Record<string, unknown>;
  if (!Array.isArray(obj.skills)) {
    throw new Error("Invalid manifest: missing skills array.");
  }
  for (const skill of obj.skills) {
    if (typeof skill !== "object" || skill === null) {
      throw new Error("Invalid manifest: skill entry is not an object.");
    }
    const s = skill as Record<string, unknown>;
    for (const field of ["name", "category", "description", "rawUrl"]) {
      if (typeof s[field] !== "string") {
        throw new Error(`Invalid manifest: skill missing string field "${field}".`);
      }
    }
  }
  return data as Manifest;
}

function readDiskCache(): DiskCache | null {
  const cachePath = getCachePath();
  if (!existsSync(cachePath)) return null;
  try {
    const raw = readFileSync(cachePath, "utf-8");
    return JSON.parse(raw) as DiskCache;
  } catch {
    return null;
  }
}

function writeDiskCache(manifest: Manifest): void {
  const cachePath = getCachePath();
  const cacheDir = join(homedir(), ".cache", "skills-cli");
  mkdirSync(cacheDir, { recursive: true });
  const cache: DiskCache = { cachedAt: new Date().toISOString(), manifest };
  writeFileSync(cachePath, JSON.stringify(cache, null, 2));
}

let cached: Skill[] | null = null;

export async function getSkills(): Promise<Skill[]> {
  if (cached) return cached;

  // Check disk cache (fresh within TTL)
  const diskCache = readDiskCache();
  if (diskCache) {
    const age = Date.now() - new Date(diskCache.cachedAt).getTime();
    if (age < CACHE_TTL_MS) {
      cached = diskCache.manifest.skills;
      return cached;
    }
  }

  let res: Response;
  try {
    res = await fetch(MANIFEST_URL);
  } catch {
    // Network failure — fall back to stale disk cache if available
    if (diskCache) {
      console.error("⚠ Using cached manifest (offline or network error).");
      cached = diskCache.manifest.skills;
      return cached;
    }
    throw new Error("Could not reach skills registry. Check your internet connection.");
  }

  if (!res.ok) {
    if (diskCache) {
      console.error(`⚠ Registry returned ${res.status} — using cached manifest.`);
      cached = diskCache.manifest.skills;
      return cached;
    }
    throw new Error(`Failed to fetch skills manifest: ${res.status} ${res.statusText}`);
  }

  const data: unknown = await res.json();
  const manifest = validateManifest(data);
  writeDiskCache(manifest);
  cached = manifest.skills;
  return cached;
}

export async function getCategories(): Promise<string[]> {
  const skills = await getSkills();
  return [...new Set(skills.map((s) => s.category))].sort();
}
