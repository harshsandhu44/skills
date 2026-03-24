import type { Skill } from "./manifest.js";

function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0))
  );
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] =
        a[i - 1] === b[j - 1]
          ? dp[i - 1][j - 1]
          : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

/**
 * Resolves a skill by name:
 * 1. Exact match
 * 2. Case-insensitive substring match (picks shortest)
 */
export function resolveSkill(query: string, skills: Skill[]): Skill | undefined {
  const exact = skills.find((s) => s.name === query);
  if (exact) return exact;

  const q = query.toLowerCase();
  const partial = skills.filter((s) => s.name.toLowerCase().includes(q));
  if (partial.length > 0) {
    return partial.sort((a, b) => a.name.length - b.name.length)[0];
  }

  return undefined;
}

/**
 * Returns up to 3 closest skill names for "did you mean?" suggestions,
 * using Levenshtein distance, filtered to a reasonable threshold.
 */
export function suggestSkills(query: string, skills: Skill[]): string[] {
  const q = query.toLowerCase();
  const threshold = Math.max(3, Math.floor(query.length / 2));

  return skills
    .map((s) => ({ name: s.name, dist: levenshtein(q, s.name.toLowerCase()) }))
    .filter(({ dist }) => dist <= threshold)
    .sort((a, b) => a.dist - b.dist)
    .slice(0, 3)
    .map(({ name }) => name);
}
