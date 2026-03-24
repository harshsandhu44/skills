import { describe, it, expect, beforeEach, afterEach, mock } from "bun:test";
import { mkdirSync, writeFileSync, rmSync, existsSync, readFileSync } from "fs";
import { join } from "path";
import { tmpdir } from "os";
import { installSkill } from "../lib/installer.js";
import type { Skill } from "../lib/manifest.js";

const FAKE_SKILL: Skill = {
  name: "test-skill",
  category: "testing",
  description: "A test skill",
  rawUrl: "https://example.com/SKILL.md",
};

const SKILL_CONTENT = "---\nname: test-skill\ndescription: A test skill\n---\n# Test\n";

function makeTmpDir(): string {
  const dir = join(tmpdir(), `skills-test-${Date.now()}`);
  mkdirSync(dir, { recursive: true });
  return dir;
}

function skillFilePath(targetDir: string, name: string): string {
  return join(targetDir, ".claude", "skills", name, "SKILL.md");
}

describe("installSkill", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = makeTmpDir();
    globalThis.fetch = mock(async () => ({
      ok: true,
      status: 200,
      text: async () => SKILL_CONTENT,
    })) as unknown as typeof fetch;
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("installs skill to target directory", async () => {
    await installSkill(FAKE_SKILL, tmpDir);
    const filePath = skillFilePath(tmpDir, FAKE_SKILL.name);
    expect(existsSync(filePath)).toBe(true);
    expect(readFileSync(filePath, "utf-8")).toBe(SKILL_CONTENT);
  });

  it("skips already-installed skill without --force", async () => {
    const filePath = skillFilePath(tmpDir, FAKE_SKILL.name);
    mkdirSync(join(tmpDir, ".claude", "skills", FAKE_SKILL.name), { recursive: true });
    writeFileSync(filePath, "existing content");

    await installSkill(FAKE_SKILL, tmpDir);

    // File should not be overwritten
    expect(readFileSync(filePath, "utf-8")).toBe("existing content");
  });

  it("overwrites existing skill with --force", async () => {
    const filePath = skillFilePath(tmpDir, FAKE_SKILL.name);
    mkdirSync(join(tmpDir, ".claude", "skills", FAKE_SKILL.name), { recursive: true });
    writeFileSync(filePath, "existing content");

    await installSkill(FAKE_SKILL, tmpDir, { force: true });

    expect(readFileSync(filePath, "utf-8")).toBe(SKILL_CONTENT);
  });

  it("does not write files in dry-run mode", async () => {
    await installSkill(FAKE_SKILL, tmpDir, { dryRun: true });
    expect(existsSync(skillFilePath(tmpDir, FAKE_SKILL.name))).toBe(false);
  });

  it("throws on download failure", async () => {
    globalThis.fetch = mock(async () => ({
      ok: false,
      status: 404,
      statusText: "Not Found",
      text: async () => "",
    })) as unknown as typeof fetch;

    expect(installSkill(FAKE_SKILL, tmpDir)).rejects.toThrow("Failed to download test-skill");
  });
});
