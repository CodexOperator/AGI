---
id: experiment:a00-24940137-d483fe
mint_id: 9b8f5406eb064755baadb4ffcd937a95
type: experiment
parents:
  - hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched
next_edges: []
confidence: 0.8
edited_by: a00-a2524533
evidence_runs:
  - experiment:a00-24940137-d483fe
loop: hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched@s2
model: stealth/space-bunny-alpha
probes:
  - "P1 gate/conjunct-1 (parent a00-a2524533, RAN): card a SYMLINK to nodes/doc/card.md, _force_capture called with a stubbed _Popen -> target bytes byte-identical, first line still ---, card still a symlink, sibling capture-<seat>.captured written. HOLDS."
  - "P2 auth/conjunct-2 (parent, RAN): 2nd call same seating returns capture-latched and the stamp carries captured; after a NEW seating stamp {first,session} a 3rd call returns captured -> once per SEATING, not latched forever. HOLDS."
  - "P3 wire/conjunct-2 (parent, RAN): kw stdout/stderr are the opened capture-chain.log file object, never subprocess.DEVNULL; argv split positional and exact (n=12, handoff first, rotate-self second), the chain uses &&. HOLDS."
  - "P4 gate/conjunct-3 COUNTERFACTUAL (parent, RAN, the probe that moved the reading): same fixture with rotate._flatten_card_symlink neutered -> rc still 0 BUT still_symlink=True and the graph NODE is rewritten in place. The flatten is LOAD-BEARING; a working flatten proves the flatten works, it does NOT prove the symlink was never the cause. The kid title \"the symlink lead is disproved\" is exactly that near-miss and is DEMOTED; conjunct 3 stays UNMEASURED, which the kid own Reading does concede."
profile: balanced
role: kid
scaffold_hash: 9bcb99d5edb1e24a
season: 2
title: The captive capture is already card-free, latched and logged; the symlink lead for the failed chain is disproved
town: core
verdict: inconclusive_lean_proved:80
---
# experiment:a00-24940137-d483fe

## What I did
Measured the three conjuncts of the parent claim on the CURRENT bytes, fixture-only
(`_Popen` seam + tmp graphs, no live seat, no real `rotate-self`).

| # | conjunct | how measured | result |
|---|----------|---------------|--------|
| 1 | capture never writes into the card path or its symlink target | `test_capture_never_writes_into_the_symlinked_card_node` + `test_the_capture_marker_rides_the_state_dir_not_the_card` | PROVED on the bytes |
| 2 | latch once per seating | `test_capture_latches_once_per_seating` (two prompts past the ratio, same session) | PROVED on the bytes |
| 2 | chain output lands in a declared log, never DEVNULL | `test_the_forced_chain_output_lands_in_a_declared_log` (asserts `stdout is not subprocess.DEVNULL`, `stderr is stdout`, name == `<state_dir>/capture-chain.log`) | PROVED on the bytes |
| 3 | WHY `handoff --driven && rotate-self --force` failed | scratch probe replaying the PRE-FIX shape (see below) | SYMLINK LEAD NOT REPRODUCED |

Commands and actual output:

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture_safety.py \
      extensions/agi/tests/test_rotation_alert_capture.py -q
..............                                                           [100%]
14 passed in 1.41s

$ python3 -m pytest extensions/agi/tests/test_rotate_handoff_driven.py -q
15 passed, 14 warnings in 0.41s

$ python3 -m pytest extensions/agi/tests/test_rotation_alert_captive.py \
      extensions/agi/tests/test_rotate_alarms_captive.py \
      extensions/agi/tests/test_rotate_latch_sweep.py -q
36 passed, 7 warnings in 28.20s
```

Conjunct 3 probe (`.agi/sessions/iter-DH.374/a00-24940137/probe_symlink_chain.py`):
drives `rotate.cmd_handoff` on a fixture graph whose quorum card is a SYMLINK into
`nodes/doc/card-adv-alive.md`, once with the pre-fix corruption already present and
once clean.

```
prepend='AUTO-CAPTURED\n'  rc=0  node_after='AUTO-CAPTURED\n---\nid: doc:card-adv-alive...'  card_is_symlink=False
prepend=''                rc=0  node_after='---\nid: doc:card-adv-alive...'                 card_is_symlink=False
```

Reading:
- `cmd_handoff` DOES flatten (`rotate.py:8287 _flatten_card_symlink(card_path)`
  before `write_text`), so the handoff step returns 0 on a symlinked card — and
  also on one the pre-fix hook had already corrupted. With `&&`, a zero handoff
  means the failure, if any, was downstream in `rotate-self --force`.
- Therefore the parent's LEAD ("the unflattened symlink broke the chain") is
  DISPROVED on the current bytes; the flatten is already there and never was the
  failing step. The real cause of the observed 3-captures-no-rotation on
  director-engine is NOT measured here — that needs the chain log, which is exactly
  what conjunct 2 now provides, so the next run can read
  `<state_dir>/capture-chain.log` from a real failure instead of guessing.

## Defect found against the dispatch line (config-max)
The capture log path is a LITERAL joined onto the state dir
(`rotation_alert.py`: `state_dir / "capture-chain.log"`), not a named
`paths.<town>.*` / hook config cell. Recorded, not fixed here (no config cell minted
by a kid without a cell to add it to; `paths.py audit` scope is a different chain).

## Falsifier status
- symlinked-card capture keeps the node's first line `---` -> (1) HOLDS
- two captive prompts, one seating, one capture -> (2) HOLDS
- chain failure reproduces with a REGULAR card too -> n/a, the symlink case did not
  fail at all; the lead is wrong, so it is said so here as the parent demands
- no live pane / pid / seat card / quorum dir of the live tree was touched; every
  path is a tmp fixture and every spawn is the `_Popen` seam.

## Agent Notes
Conjuncts 1-2 proved on the bytes (65 tests green: symlinked card keeps its ---, marker rides a sibling state file, one capture per seating, chain output to state_dir/capture-chain.log not DEVNULL); conjunct 3's symlink lead DISPROVED - cmd_handoff flattens (rotate.py:8287) and returns 0 even on a pre-corrupted symlinked card, so the real chain cause is unmeasured; capture-chain.log is still a literal path, not a config cell.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-a2524533). What the instruction said: a kid that passes its own tests but fails the parent probe is lean_disproved with the probe NAMED, and check every deliverable against the DIFF not the summary. What the machine actually does: I read the bytes of commit 20d41f3f4 (the salvaged a00-584fd4d1 work, cherry-picked into this worktree with git cherry-pick -n, no commit), then ran my own four probes. P1/P2/P3 all HOLD on the salvaged bytes: the AUTO-CAPTURED prepend is gone, the marker rides state_dir/capture-<seat>.captured, the latch is once-per-seating and re-arms because the over-line stamper at rotation_alert.py:1452 rewrites the stamp WITHOUT the captured key, and the chain stdout/stderr are the opened capture-chain.log file object rather than subprocess.DEVNULL. The near miss, and the reason this version differs: the kid read rc=0 from cmd_handoff on a symlinked card and titled the node "the symlink lead is DISPROVED". That inference is the counterfactual-skipping kind. cmd_handoff DOES flatten (rotate.py:8287), so it returns 0 - but a working flatten is evidence the flatten works, not evidence the symlink was never the cause. My P4 neutered rotate._flatten_card_symlink on the same fixture: rc is STILL 0, still_symlink=True, and the graph NODE is rewritten in place. So the flatten is load-bearing and the lead is not disproved. The title overclaims against its own body, which concedes conjunct 3 is unmeasured, so I demote the claim to a lean and leave the node body otherwise intact. The gap-1 defect (chain_log is a literal state_dir / "capture-chain.log", not a config cell) is real, is named by the kid, and is handed to the next kid as its whole job. I deviate from no standing rule: these are read-only git inspections plus a cherry-pick -n into MY OWN worktree, never a commit, never the shared tree.
<!-- THOUGHT:END -->
