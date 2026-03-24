import { describe, it, expect, afterEach, mock } from "bun:test";
import { rmSync, existsSync, mkdirSync, writeFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { validateManifest } from "../lib/manifest.js";

const CACHE_PATH = join(homedir(), ".cache", "skills-cli", "manifest.json");

const VALID_MANIFEST = {
  version: 1,
  generatedAt: new Date().toISOString(),
  skills: [
    { name: "debug-issue", category: "coding", description: "Debug a bug", rawUrl: "https://example.com/skill.md" },
  ],
};

describe("validateManifest", () => {
  it("accepts a valid manifest", () => {
    const result = validateManifest(VALID_MANIFEST);
    expect(result.skills).toHaveLength(1);
    expect(result.skills[0].name).toBe("debug-issue");
  });

  it("rejects null", () => {
    expect(() => validateManifest(null)).toThrow("expected an object");
  });

  it("rejects manifest without skills array", () => {
    expect(() => validateManifest({ version: 1, generatedAt: "now" })).toThrow("missing skills array");
  });

  it("rejects manifest with non-array skills", () => {
    expect(() => validateManifest({ skills: "nope" })).toThrow("missing skills array");
  });

  it("rejects skill entry missing category", () => {
    expect(() =>
      validateManifest({ skills: [{ name: "x", description: "d", rawUrl: "u" }] })
    ).toThrow('missing string field "category"');
  });

  it("rejects skill entry missing rawUrl", () => {
    expect(() =>
      validateManifest({ skills: [{ name: "x", category: "c", description: "d" }] })
    ).toThrow('missing string field "rawUrl"');
  });

  it("rejects skill entry that is not an object", () => {
    expect(() => validateManifest({ skills: [42] })).toThrow("not an object");
  });
});

describe("disk cache fallback", () => {
  afterEach(() => {
    if (existsSync(CACHE_PATH)) rmSync(CACHE_PATH);
  });

  it("reads a valid cache file", () => {
    const cacheDir = join(homedir(), ".cache", "skills-cli");
    mkdirSync(cacheDir, { recursive: true });
    const cache = { cachedAt: new Date().toISOString(), manifest: VALID_MANIFEST };
    writeFileSync(CACHE_PATH, JSON.stringify(cache));
    expect(existsSync(CACHE_PATH)).toBe(true);
    const raw = JSON.parse(require("fs").readFileSync(CACHE_PATH, "utf-8"));
    expect(raw.manifest.skills).toHaveLength(1);
  });
});
