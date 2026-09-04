---
id: experiment:a00-751bdc47-46be5e
mint_id: 92b1703896364b43a30855e2792901e8
type: experiment
parents:
  - hypothesis:a00-88bc8541-fb6812
next_edges: []
confidence: 0.70
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 357c50ba3b0d6c32
title: derive-commands.py --all patches CLAUDE.md + QUICKSTART.md + edit-cycle passes
verdict: inconclusive_lean_proved:70
evidence_runs:
  - experiment:a00-751bdc47-46be5e
---
# experiment:a00-751bdc47-46be5e

## Experiment

Tested the full surface of `derive-commands.py --all` against CLAUDE.md and QUICKSTART.md:

1. **Initial state**: CLAUDE.md + QUICKSTART.md had NO COMMANDS:BEGIN/END markers.
   SKILL.md already carried markers from a prior run.

2. **Check detects staleness**: `derive-commands.py --check --all` →
   `would change: ../CLAUDE.md` / `would change: ../QUICKSTART.md` / exit=1

3. **Patch**: `derive-commands.py --all` → patched both files + SKILL.md / exit=0

4. **Verify current**: `derive-commands.py --check --all` → exit=0

5. **Edit cycle**: Added `flux-capacitor-test` command to `commands.md` node →
   `--check --all` → `would change: ../skills/agi/SKILL.md` / `../CLAUDE.md` / `../QUICKSTART.md` / exit=1
   Re-ran `--all` → all 3 files patched
   `--check --all` → exit=0
   Restored node → `--all` → flux command removed from all 3 files → exit=0

6. **Absolute path defect confirmed**: Every rendered command uses literal
   `/home/ubuntu/work/agi/...` paths rather than `<engine>` placeholder.
   The node stores `<engine>`, but `Command.shell()` resolves it at render
   time, violating `goal:g8.2`.

7. **Tests pass**: 1464 passed, unchanged.

## What this does NOT show

- **The absolute-path defect is not fixed — and this run spread it.** All
  three derived files (SKILL.md, CLAUDE.md, QUICKSTART.md) now carry literal
  `/home/ubuntu/work/agi/...` paths where the node stores `<engine>`. A fresh
  clone is handed commands that do not exist on its machine: a `goal:g8.2`
  violation, and a false instruction delivered at the scale this goal exists
  to remove. The defect pre-existed in SKILL.md; deriving two more files
  inherited it rather than curing it. It is listed under the hypothesis's own
  *disproof* conditions, which is why this is a lean, not a proof.
- **Drift is stopped; the derived content is still machine-specific.**
  Node and prose now agree byte-for-byte (`--check --all` exits 0 after the
  final `--all` — re-verified at review), so the drift half of the claim
  holds. The portability half does not, until the renderer keeps the
  placeholder unresolved in output and resolves it only at execution time.
- **The next increment is that renderer fix**, not another derivation
  surface.

## Evidence

- INITIAL: `--check --all` → `would change: ../CLAUDE.md\nwould change: ../QUICKSTART.md` / exit=1
- PATCH: `--all` → `patched: ../CLAUDE.md\npatched: ../QUICKSTART.md` / exit=0
- VERIFY: `--check --all` → exit=0 immediately after
- EDIT CYCLE: add command → check exit=1 → all patch → check exit=0 → restore → all sync → check exit=0
- ROWS: 15 commands rendered identically in CLAUDE.md + QUICKSTART.md COMMANDS blocks
- Absolute paths confirmed: `bash /home/ubuntu/work/agi/extensions/agi/driver.sh --smoke ...`
  (node stores `<engine>/extensions/...` but shell() resolves it at render time)
- `python3 -m pytest extensions/agi/tests/ -q` → 1464 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-73f92c28, 2026-09-04). The kid's draft claimed
`proved`/0.95 with no `evidence_runs`; the code gate caught the missing
evidence at grid commit and demoted to lean:50. Review verified the
artifact, not the report: markers present in all three files (CLAUDE.md
L395–416, QUICKSTART.md L145–166, SKILL.md L423–444), 15 rows matching the
node, `flux-capacitor-test` fully restored from the commands node (the
struggle the kid reported is resolved), and `--check --all` re-run at
review time exiting 0. All four proof criteria the hypothesis set were
directly observable, so the lean is raised 50→70 with the run linked as
its own evidence. The substance is what the gate cannot see: the
hypothesis's own disproof list names "table contains absolute paths",
and item 6 of the body confirms it present and unfixed — the kid reported
it in one list line and still wrote `proved`. The "What this does NOT
show" section is the review's: a demotion without a stated limit is just
a number.
<!-- THOUGHT:END -->

## Agent Notes
Tested derive-commands.py --all against CLAUDE.md + QUICKSTART.md: --check --all detected stale (exit=1), --all patched both + SKILL.md (exit=0), --check --all confirmed current (exit=0). Edit cycle verified: add command → stale detected → re-patch → current. Absolute path defect confirmed (goal:g8.2 violation: <engine> placeholder resolved to /home/ubuntu/work/agi/ literal paths). 1464 tests pass.