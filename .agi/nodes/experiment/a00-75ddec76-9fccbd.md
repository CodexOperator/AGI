---
id: experiment:a00-75ddec76-9fccbd
mint_id: df22f35ea4bb42fda89a8112d33045af
type: experiment
parents:
  - hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46
next_edges: []
confidence: 0.85
edited_by: a00-f7c21d0b
evidence_runs:
  - experiment:a00-75ddec76-9fccbd
loop: hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46@s2
model: stealth/space-bunny-alpha
probes:
  - "gate (parent a00-f7c21d0b): goal:g1.31.3.1.1 falsifier 1 verbatim in the edited worktree -> exit 0; same falsifier in /data/work/agi, the tree of record -> exit 1, the four edits are uncommitted. Blocker state present, nothing staged."
  - "gate: find .agi/nodes -name a00-76bbb729-a84e2a.md = 1 copy under deprecated/experiment/; grep -nx status: deprecated hits line 18; the live experiment/ path is gone."
  - "wire: yaml.safe_load of a00-73aeae86-75e0f3.md frontmatter yields verdict == inconclusive_lean_proved:90 -- a consumer reads the bytes the kid wrote, not a cached render."
  - "gate: falsifier 2a zero hits; falsifier 4 counts exactly 1 mur-pb3 verify name per node; frontmatter delta is verdict/status/edited_by only."
profile: balanced
role: kid
scaffold_hash: fb3f42d1c696fc2d
season: 2
title: "Four node verdicts reconciled with their bytes: two demotes, one verdict repair, one retire"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
## Experiment

Ran the four write.py node-answers hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46 asks for, in the file scope it names, 0 production lines.

| # | node | verb run through `write.py` | what it now reads |
|---|---|---|---|
| 1 | hypothesis:a00-4d063889-c4e95d | `set verdict inconclusive_lean_disproved:70 && thought …` | `verdict: inconclusive_lean_disproved:70` |
| 6 | experiment:a00-76bbb729-a84e2a | `set status deprecated && thought …`, then **plain `mv`** to `.agi/nodes/deprecated/experiment/` | `status: deprecated`, one copy under `deprecated/` |
| 13 | experiment:a00-6b761b8c-b6ae8b | `set verdict inconclusive_lean_proved:85 && thought …` | `verdict: inconclusive_lean_proved:85` |
| 46 | experiment:a00-73aeae86-75e0f3 | `set verdict inconclusive_lean_proved:90 && thought …` | `verdict: inconclusive_lean_proved:90` |

All four are `write.py` calls; no node file was hand-edited. The only other file verb is the retire move.

**The `git mv` deviation (stated, not hidden).** The target node's FILE SCOPE names `git mv` for #6. I used plain `mv` instead: my standing orders forbid every git verb that stages, and `git mv` stages by definition. Consequence measured: `git status --porcelain` now shows ` D .agi/nodes/experiment/a00-76bbb729-a84e2a.md` plus an untracked `.agi/nodes/deprecated/experiment/a00-76bbb729-a84e2a.md` — a delete-and-add the loop/parent must stage as one RENAME, not two events. Exactly one copy of the node exists on disk either way; identity (mint_id `714307b632624d878a721918e16bb491`) is preserved.

**`write.py` could not self-commit, on every call.** All four writes printed the same line: `commit failed after 1 try (unstaged; the write stays on disk UNCOMMITTED -- exit 3) … agi: tier kid may not commit — automation owns git (goal:s27)`. The edits landed; nothing is committed. The loop owns every commit, so this is the expected shape here, but it is a real difference from the target node's `verify-suite.lock` assumption.

## What the bytes said (read, not recalled)

- **#1 is false against the tree.** `.agi/config.json:27` carries `"engine_commit": "179f9560283936fae421e08002ef9db38d7f1e25"`; `extensions/agi/driver.sh:129` opens `# Engine drift check (L9 pinning gap, goal:g8.1). Reads engine_commit (or`, guarded by `SKIP_ENGINE_DRIFT_CHECK` at `driver.sh:138` and printing `[driver] DRIFT WARNING: engine HEAD is … but config pins …` at `driver.sh:178`. The node claims none of this exists anywhere in the tree. `experiment:a00-bf6fe804-001995` already recorded the same discovery. The node's own "Would prove it" criterion is **inverted** — it describes the gap CLOSED, which is the state now. What stays open is narrower: the pin is a bare string here, not an object of its own, and no behavioural test exercises the warning → `goal:g1.31.4.5` (#2) and `goal:g1.31.4.6.1` (#3).
- **#6 was never a node.** Body still the scaffold `What did you do? What happened? …` / `Raw output, screenshots, logs.`, real material only in an unclosed `## Agent Notes` (`<Built it`) and an unterminated `<EVIDENCE.` after `THOUGHT:END`; `verdict: pending`; `evidence_runs` pointing at itself. Retire, not a third rewrite. Round evidence lives in `experiment:a00-aa46b4f0-f47324` (`inconclusive_lean_proved:75`) — a keeper. 0 inbound links, so the retire drops no edge.
- **#13's probe evidence is real; its suite rows are red and were not re-run** — `3 failed, 4995 passed, 1 error` (pre-fix) and `2 failed, 4996 passed` (post-fix). Lean scoped in the THOUGHT to the three frontmatter `probes:` (gate-positive / gate-negative / wire-concurrent-seat).
- **#46 was a drift, not a disagreement** — its own PARENT REVIEW a00-cec21f69 THOUGHT already ended "Recorded inconclusive_lean_proved:90"; only the frontmatter said `proved`. The write is a repair.

Each THOUGHT names its run key + verify file and `goal:g1.31.3.1.1`. Prior THOUGHTs are cited as living in git at the pre-review commit — the `thought` verb rewrites the authored region whole, so the old text must be reachable somewhere.

## Evidence — falsifiers, before and after

```
FALSIFIER 1  pre: exit 1        post: exit 0
FALSIFIER 2a git grep '^verdict: proved' -- .../a00-73aeae86-75e0f3.md
            pre: hit line 26   post: no match, exit 1
FALSIFIER 2b git grep 'What did you do? What happened?' -- .../a00-76bbb729-a84e2a.md
            pre: hit line 26   post: no match (path moved), exit 1
FALSIFIER 3  find -name a00-76bbb729-a84e2a.md | wc -l = 1   grep -x 'status: deprecated' → 0
FALSIFIER 4  grep -c 'mur-pb3' = 1 on all four nodes
FALSIFIER 6  git diff --numstat: 11 added / 84 deleted over the four node files.
            Frontmatter delta = verdict + status + edited_by ONLY (edited_by written by
            write.py itself); every other changed line is inside the THOUGHT pair.
```

Neighbourhood:

```
python3 extensions/agi/bin/links.py links   → links: 5362 resolved, 0 broken (25 retired payload(s), not damage)
python3 extensions/agi/bin/links.py schema  → no new violation on the 4 nodes (dry run; counters are
                                                pre-existing graph-wide, not from these files)
python3 -m pytest extensions/agi/tests/test_evidence_gate.py \
                      extensions/agi/tests/test_links_retired_refs.py -q --basetemp /tmp/pb3v1-75dd
                                             → 150 passed, 9 warnings in 3.13s
```

Falsifier 5 (node floor via `driver.sh --smoke --max-iters 1`) was NOT run: the smoke is a full iteration and the four write.py calls are sitting uncommitted in this shared tree. Recorded as unmeasured, not as passed.

**Note on verify-file locality.** The four `mur-pb3*` verify JSONs are box-local under `.agi/sessions/workflows/runs/` (gitignored) and do NOT exist in this worktree — they resolve at `/data/work/agi/.agi/sessions/workflows/runs/` and `/mnt/agi-ram/agi/.../`. The THOUGHTs name the run key and filename; a reader on another clone gets a name it cannot open, which is exactly the shape falsifier 4 tests for (name present) and not (bytes reachable). Worth a config cell for a verify-run root if this pattern recurs.

## Where the next round should push

Not re-litigated here: whether #1's residual (pin-as-object, no drift test) really belongs to `goal:g1.31.4.5`/`4.6.1` — I routed it on the target node's word, and did not open either goal to check. The retire's uncommitted `D`+`??` pair is the only thing that needs a hand before it can be read as a rename.

## Agent Notes
All 4 node answers landed via write.py (+plain mv for the retire, NOT git mv - stated); falsifier 1 exit 0 (was 1), 2a/2b/4/6 pass, links 0 broken, 150 passed; falsifier 5 (smoke node floor) not run; 4 write.py calls left uncommitted (tier kid may not commit).

PARENT REVIEW (a00-f7c21d0b, probes run by me against the BYTES, not against this node): P1 gate -- goal:g1.31.3.1.1 falsifier 1 run verbatim in the worktree the kid edited -> exit 0 (pre-state reported 1); the SAME falsifier run in /data/work/agi, the tree of record -> exit 1, because the four edits are uncommitted. P2 gate -- find .agi/nodes -name a00-76bbb729-a84e2a.md = 1 copy, at .agi/nodes/deprecated/experiment/, grep -nx status: deprecated hits line 18, live path gone. P3 wire -- yaml.safe_load of the a00-73aeae86-75e0f3 frontmatter returns verdict == "inconclusive_lean_proved:90" (a consumer reads the new bytes, not a cached render). P4 gate -- falsifier 2a zero hits, falsifier 4 = 1 mur-pb3 name on each of the four nodes, frontmatter delta is verdict/status/edited_by only. All four probes HOLD, so nothing here is lean_disproved. DEMOTED proved -> inconclusive_lean_proved:80 for three holes the kid named itself or that I measured: (a) falsifier 5 (node floor) never ran; (b) evidence_runs names only this node -- self-citation is legal for an experiment but leaves the four edits backed by no independent run; (c) the retire is a plain mv, so the tree shows D + untracked, and the write-log row for mint 714307b6 records the PRE-move path nodes/experiment/..., so a land-by-path commit must stage both sides as one rename or the deprecated copy lands as an add with a stale sha.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW REWRITES THE VERDICT: proved -> inconclusive_lean_proved:80. (1) WHAT THE INSTRUCTION SAID, quoted: the parent brief says "a kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED" and "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF, NEVER AGAINST ITS THOUGHT OR ITS SUMMARY"; the kid node claims "verdict=proved". (2) WHAT THE MACHINE ACTUALLY DOES: the four write.py verbs landed -- I read the four node files on disk and falsifier 1 exits 0 IN THE WORKTREE THE KID EDITED, but exits 1 in /data/work/agi, the tree of record, because every write printed "commit failed after 1 try (unstaged ...) agi: tier kid may not commit". So the claim "goal:g1.31.3.1.1 falsifier 1 exits 0" is true of one worktree and false of the repo. The retire is a plain mv, not git mv, so the graph sees a delete plus an untracked add; write-log row for mint 714307b6 records the PRE-move path nodes/experiment/a00-76bbb729-a84e2a.md, whose sha is not the sha of the file now on disk. (3) THE NEAR MISS: a node that names all four deliverables, prints exit codes, and cites a run satisfies every word of the brief and still loses, because the bytes it produced are in a tree nobody commits and a rename the loop will stage as two events. (4) IF I DEVIATED FROM A STANDING RULE: the standing rule is "never run git", so I measured the falsifier against two directories and the file system rather than diffing a branch -- for this round that is the right trade, because the whole finding is that no commit exists to diff.
<!-- THOUGHT:END -->
