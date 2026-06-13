---
name: dependency-risk
description: Review a dependency change for supply-chain and vulnerability risk — new packages, install scripts, maintainer/ownership signals, and audit output — before adding or upgrading. Use when a PR adds or bumps dependencies, or when triaging the output of an audit/advisory tool.
---

# Dependency Risk

Every dependency is code you didn't write running with your privileges. A malicious or
abandoned package is a breach waiting to happen, and supply-chain attacks increasingly
target exactly this moment — the moment you add a package. This skill vets the change.

This is the security lens; the `dependency-upgrade` skill (in `release-ops`) covers the
mechanics of upgrading safely once you've decided to.

## Process

### 1. See exactly what changed

```bash
git diff <base>...HEAD -- <lockfile> <manifest>
```

The lockfile diff is the truth — it shows **transitive** additions, not just the direct
package you added. A one-line manifest change can pull in dozens of new packages. Review
the whole set the lockfile reveals.

### 2. Vet each new / upgraded package

For a newly-added package especially, check the signals:

- **Popularity & maintenance** — downloads, age, last release, open-vs-closed issues. A
  brand-new, low-download package added as a direct dependency deserves scrutiny.
- **Maintainer & ownership** — recent ownership transfer, a single maintainer, a name
  that's a near-miss of a popular package (typosquatting).
- **Install scripts** — does it run `postinstall`/`preinstall`/`prepare` scripts? Those
  execute arbitrary code on `install`, in CI and on dev machines. Read what they do.
- **Footprint** — does a utility need network or filesystem access it shouldn't?

### 3. Run the audit, then triage it

```bash
npm audit / pnpm audit / pip-audit / cargo audit / govulncheck   # per ecosystem
```

Don't just read the scary number. For each advisory:

- Is the vulnerable code path **actually reachable** from your usage, or is it a dev-only
  / transitive dependency you never invoke?
- Is there a fixed version, and does upgrading break anything?
- Severity **and** exploitability in *your* context — a critical in an unused code path
  may rank below a medium in a request handler.

### 4. Decide and record

Per package/advisory: **accept** (with reason), **upgrade/patch**, **replace** (find a
safer package), or **remove** (do you even need it?). For accepted risks, write down why
and when to revisit. The cheapest dependency is the one you don't add — challenge whether
a small utility is worth a new supply-chain entry at all.

## Output shape

```text
## Change          (direct + transitive additions from the lockfile diff)
## Package risk     (per new package: popularity / maintainer / install-scripts / footprint)
## Advisories       (audit findings · reachable? · fix available · severity-in-context)
## Decisions        (accept / upgrade / replace / remove + reason)
```

Flag two things loudest: a new dependency with an install script you didn't read, and a
reachable high-severity advisory with no fix. Those are where supply-chain incidents
come from.
