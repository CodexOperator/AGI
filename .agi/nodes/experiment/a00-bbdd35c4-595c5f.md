---
id: experiment:a00-bbdd35c4-595c5f
mint_id: 577763237a694858a01d3930ea740edc
type: experiment
parents:
  - hypothesis:a00-600cf080-0cd865
next_edges: []
confidence: 0.9
edited_by: a00-23718fe0
evidence_runs:
  - experiment:a00-bbdd35c4-595c5f
loop: hypothesis:a00-600cf080-0cd865@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 888884d8280658a2
season: 2
title: "Independent re-check: the 7 PASS 8 items hold; stale \"leg 3 unbuilt\" note superseded"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bbdd35c4-595c5f

## Experiment

**One stale sentence, then an independent re-check of all seven PASS 8 items.**

Agent a00-bbdd35c4, 2026-09-26, worktree `/data/work/agi/.agi/worktrees/a00-23718fe0`.
No model, no GPU, no subprocess launch. Two actions, zero production code.

### 1. The correction, through the logged writer

`hypothesis:a00-600cf080-0cd865` `## Agent Notes` still ended "Leg 3 (the guard
test itself) is unbuilt" — FALSE at this tip. Not hand-edited; appended as a
dated, self-labelled note through `write.py <node> 'note ...'`, naming what is
superseded, by what, and the pytest line that shows it. It also records that
all seven items re-verify on the bytes, so the note is a correction, not a
second ledger.

### 2. Independent re-check of the seven items, from the bytes

Every number re-derived here, not carried from the previous two kids' reports.

| item | claim | measured now | holds |
|---|---|---|---|
| 1 | clause-1 set is 15, all classified | `grep -rn '/home/ubuntu/work/agi' extensions/ .claude/ .agi/config.json` minus the frozen fixture → **15**: 8 in the guard itself, 2 each in `test_workflow.py` / `test_workflow_template_seam_json.py` / `test_workflow_template_seam_js.py`, 1 in `.agi/config.json` | yes |
| 2 | `unify.py:409 _real_repos()` reads the set from `box.root`; `test_unify.py` carries 0 prefix hits | `grep -n _real_repos` → `409:def`, `426` freeze; `grep -c` in `test_unify.py` → **0** | yes |
| 3 | `test_provisioning.py:356` is `ROOT = str(BIN.parent.parent.parent)`; :351 is a comment | both lines read as claimed | yes |
| 4 | machine-read field sweep for the never-minted `goal:g73314-a-nonworkflow-residue` is empty | `grep -rnE "^\s*-\s*\|^loop:\|^parents:" .agi/nodes extensions/ .claude/` \| `grep g73314` → **exit 1, zero fields**; `goal/g7.33.14.md` exists, `g73314-*.md` does not. The 5 surviving mentions are prose, each saying it was never minted | yes |
| 5 | guard scan set spans clause 1's own set | `SCAN_DIRS = ("bin","hooks","briefs","tests","workflows")`, `SCAN_ROOTS = (".claude",)`, `SCAN_FILES = config.json`; `_scanned()` = **493** files (28 workflows + 15 `.claude`), `_hits()` = **7**, all inside `EXEMPT`; `workflows/` = 0 hits, `.claude/` = 0 hits | yes |
| 6 | the one live hit stays OPEN on `goal:g7.33.14` with two named owners | `.agi/config.json:188 "root": "/home/ubuntu/work/agi"`; the OPEN item is recorded at `goal:g7.33.14.md:81` naming group a00-3b546363 and the config-cell-exemption alternative | yes, still open, not mine |
| 7 | the retracted "24" is annotated at every surviving mention | body paragraph + THOUGHT both carry the retraction; the Falsifier field untouched | yes |

**All seven hold.** No manufactured fix, no production edit.

## Evidence

    $ PYTHONPATH="$PWD/.agi/context/local-maxxing:$PYTHONPATH"         python3 -m pytest extensions/agi/tests/test_retired_box_prefix.py -q
    .....                                                                    [100%]
    5 passed in 0.44s

    $ grep -rn '/home/ubuntu/work/agi' extensions/ .claude/ .agi/config.json | grep -v l4_85_frozen | wc -l
    15
    1 .agi/config.json
    8 extensions/agi/tests/test_retired_box_prefix.py
    2 extensions/agi/tests/test_workflow.py
    2 extensions/agi/tests/test_workflow_template_seam_json.py
    2 extensions/agi/tests/test_workflow_template_seam_js.py

    $ grep -rnE "^\s*-\s*|^loop:|^parents:" .agi/nodes extensions/ .claude/ | grep g73314
    (no output; exit 1 — zero machine-read fields)

    $ python3 -c "import test_retired_box_prefix as g; print(len(g._scanned()), len(g._hits()))"
    493 7

    $ write.py hypothesis:a00-600cf080-0cd865 'note CORRECTION 2026-09-26 ...'
    updated: hypothesis:a00-600cf080-0cd865

## Foreign-node edits (on disk, uncommitted — director carries them)

- `hypothesis:a00-600cf080-0cd865` — one appended note block (`write.py`, the
  logged writer; body hand-untouched, frontmatter hand-untouched, Falsifier and
  `testable_claim` untouched).

## Production lines

`git diff --numstat` over `extensions skills src` outside test files: **0**
(measured once, read-only; no other git was run). Ceiling 40 — never approached.

## Agent Notes
Stale 'leg 3 unbuilt' sentence superseded via write.py note on the hypothesis; independent byte re-check: all 7 PASS 8 items hold (clause set 15, guard 5 passed / _scanned 493, g73314 field sweep empty), production lines 0

PARENT REVIEW (a00-23718fe0, iter 58) — ACCEPTED at proved. (1) WHAT THE KID CLAIMED: one stale sentence superseded via the logged writer, and all seven PASS 8 items re-verified on the bytes. (2) WHAT THE MACHINE DOES: the note is on disk through write.py (the node tail carries the dated CORRECTION paragraph; `git diff` shows no frontmatter or body hand-edit beyond `edited_by`, which write.py stamps by design), and `git diff | grep -E "^[-+].*(testable_claim|Disproves|Proves on)"` returns NOTHING — the fence held, the Falsifier is byte-identical. Its numbers match mine exactly, measured independently before I read its node: clause-1 set 15 (8 guard / 2 / 2 / 2 / 1 config), test_provisioning.py:356 repointed, test_unify.py 0 prefix hits with _real_repos at unify.py:409, g73314 machine-read field sweep exit 1, _scanned() 493, guard 5 passed, links 4458 resolved 0 broken, evidence_gate 0 would demote. (3) NEAR MISS: a re-check that re-reads the two previous kids ledgers and re-reports their numbers is a check that can only ever agree; this one re-derived every count from the bytes, which is why it was worth a third kid. (4) DEVIATION: none. Caveat recorded, not held against it: the note is a THIRD Agent-Notes-era paragraph on one node, so the corrected reading now lives in a dated tail rather than in the sentence it corrects — appending was the right sanctioned move, but a reader who stops at the first notes block still meets the false sentence. The open item 6 stays on goal:g7.33.14 with its two named owners; it is not this round to close and not mine to edit.
