import { describe, it, expect } from "bun:test";
import { resolveSkill, suggestSkills } from "../lib/fuzzy.js";
import type { Skill } from "../lib/manifest.js";

function makeSkills(names: string[]): Skill[] {
  return names.map((name) => ({
    name,
    category: "test",
    description: "",
    rawUrl: "",
  }));
}

const skills = makeSkills(["debug-issue", "write-tests", "review-changed-files", "branch-review", "commit"]);

describe("resolveSkill", () => {
  it("resolves exact match", () => {
    expect(resolveSkill("commit", skills)?.name).toBe("commit");
  });

  it("resolves case-insensitive substring match", () => {
    expect(resolveSkill("Debug", skills)?.name).toBe("debug-issue");
  });

  it("picks shortest substring match", () => {
    // "review" matches both "review-changed-files" and "branch-review"; picks shorter
    const result = resolveSkill("review", skills);
    expect(result?.name).toBe("branch-review");
  });

  it("returns undefined for no match", () => {
    expect(resolveSkill("nonexistent-xyz", skills)).toBeUndefined();
  });
});

describe("suggestSkills", () => {
  it("suggests close matches for typos", () => {
    const suggestions = suggestSkills("comit", skills);
    expect(suggestions).toContain("commit");
  });

  it("returns empty array for completely unrelated query", () => {
    const suggestions = suggestSkills("zzzzzzzzzzzzz", skills);
    expect(suggestions).toHaveLength(0);
  });
});
