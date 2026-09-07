---
id: hypothesis:a00-001de563-9bd20a
mint_id: 7960e8366fbb4cc4aee5ca4ed76ac8af
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: e818aadef94821ef
season: 1
thought_session: season
title: A00 001de563 9bd20a
verdict: pending
---
# hypothesis:a00-001de563-9bd20a

## Hypothesis

**Claim:** The three distribution shapes `goal:g8.1` compares (drop-in clone,
skill package, real install) are not mutually exclusive — the engine's
architecture naturally splits into two layers that fit different shapes:

1. **Engine code** (Python scripts under `extensions/`, `skills/`, `src/`,
   `lib/`, `bin/`) stays as a drop-in git clone. This preserves forkability
   (engine out of project history, no vendoring risk) and avoids fitting ~15
   entry points + a test suite + a `src/` tree into a skill package format
   that was designed for small agent integrations, not multi-tool engines.

2. **Pi integration layer** (the `~/.claude/skills/agi` symlink, the
   SessionStart hook in `hooks/cc-session-start.sh`, the skill definition
   under `skills/agi/`) ships as a separate installable skill package via
   `pip`/`uv`. This gives the integration the pinning and dependency story
   a package format provides, without burdening the engine code with a
   packaging surface it does not need.

**The claim:** this hybrid is the right answer to g8.1's question because it
resolves the tensions the goal body flags — forkability preserved by the
clone, clean pinning provided by the package layer, no skill format stretch
for the engine code — without requiring a winner-take-all shape decision.

**What would prove it:** a working decomposition where:

- The engine exists as a standalone git repo, cloneable into any project's
  `.agi/` (as it is today). **Verifier:** `python3 -m pytest
  extensions/agi/tests/ -q` passes from the clone with no project-level
  install step.
- The pi integration layer (`skills/agi/SKILL.md` + symlink + session-start
  hook) is extracted into a separate package (e.g. `pi-skill-agi` on PyPI)
  that depends on the engine clone at runtime and declares its expected
  engine version. **Verifier:** `uv tool install pi-skill-agi` pulls the
  integration package, and `driver.sh --smoke` from inside any project that
  has the engine cloned produces the same output as before the split.
- The engine version pin (the L9 gap) is declared in the package metadata
  rather than in `.agi/config.json`, so `uv tool list --outdated` reports
  drift without the engine needing a custom drift checker.

**What would disprove it:**

- The split introduces a circular dependency — the integration package
  imports engine code, and the engine includes integration config (
  `config.json` declares which skill to load). A bootstrap loop that makes
  one unusable without the other would disprove the claim that these are
  independent layers.
- The integration package ends up duplicating the engine clone's entry-point
  discovery (`level3.py` reads `git ls-files` off the clone, which a pip
  package cannot do against a gitignored directory). If more than one entry
  point needs to discover the clone's layout, the split leaks.
- Testing requires two repos, two CI pipelines, and a release gate, which
  is worse for maintainability than one clone or one package alone — the
  shape decision that intended to *reduce* configuration surface.

**Why this is distinct from the sibling hypotheses under g8.1:** Siblings
a00-23fc51e6, a00-4d063889, and a01-0c63908f all address the L9 pinning gap
within shape 1 (drop-in clone), adding an `engine_commit` field to
`config.json` plus a drift check. This hypothesis instead questions the
mutual-exclusivity assumption — claiming the three shapes are *dimensions*
that each cover a different part of the engine's surface, not alternatives
to choose among.

<!-- THOUGHT:BEGIN -->
Parent (a00-2fd44d74) reviewed on iteration 1047, after the kid's first pass.
Two things changed and why the node now says what it says:

1. The kid's body is kept as written. The claim — the three g8.1 distribution
   shapes are dimensions covering different layers of the engine, not
   winner-take-all alternatives, so a hybrid split (engine code = clone,
   pi integration = installable package) answers the goal — is a genuine
   testable hypothesis that no sibling has made (the siblings only touch the
   L9 pinning gap inside shape 1). Its self-identified disproof path (a pip
   package cannot `git ls-files` a gitignored clone, so entry-point
   discovery leaks across the split) is a real tension, not filler. I
   accepted the kid's `pending` verdict as honest: no experiment has run,
   so there is nothing to prove or disprove yet, and `pending` is the only
   defensible state. Nothing to demote.

2. This version removes a duplicated `## Agent Notes` heading. The kid
   called `cli.py done` twice with two different `--notes` strings, and the
   second write left both notes stacked in the body. The surviving note
   matches the one recorded in the session's agent.json. The duplicate was
   noise, not content.
<!-- THOUGHT:END -->

## Agent Notes
Hybrid shape hypothesis under g8.1: engine code stays as drop-in clone (preserves forkability, avoids skill format stretch), pi integration layer ships as installable package (pinning/dependency story). Distinct from siblings covering L9 pinning gap only.