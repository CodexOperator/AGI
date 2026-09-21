---
id: experiment:a00-edfd2a9d-4b64c4
mint_id: 53564c617fbd4bcb8b0cf9742b06219b
type: experiment
parents:
  - hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window
next_edges: []
confidence: 0.95
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-edfd2a9d-4b64c4
loop: hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06d7a9633a5c0f1e
season: 2
thought_session: sanctuary-director-gen12
title: SKIPPED cap paths do not kill the oldest window - hypothesis disproved
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-edfd2a9d-4b64c4

## Experiment

Tested the hypothesis claim against the live `_reap_belam_oldest` (rotate.py:3181-3260) on the two SKIPPED early-return paths, using a `window_path` fixture so `_kill_window` would drop the owned `@<id>` line from the fixture file instead of a real tmux kill.

Scratch driver in /tmp (no repo code changed):
1. Path (a) `no pane pid`: oldest with no resolvable pane-pid seam.
2. Path (b) `pane pid with no descendants`: `@9` @id RESOLVED, `_pane_pid` answered a real pid, but `_descendant_chain` returned [] (patched).

Observed (exact):
- (a) record `{'oldest': '@9 pred', 'window_id': None, 'pids': [], 'reaped': False, 'ps_after': [], 'skipped': "SKIPPED: no pane pid for the oldest window '@9 pred' (@id None); ..."}` — the `@9` line REMAINED in the fixture window file.
- (b) record `{'oldest': 'pred', 'window_id': '@9', 'pids': [], 'reaped': False, 'ps_after': [], 'pane_pid': 999999, 'skipped': 'SKIPPED: no chain under pane pid 999999 ...'}` — even WITH `window_id: '@9'` resolved, the `@9` line REMAINED in the fixture file.
- Neither record carries a `window_killed` field. `_kill_window` is reached ONLY on the non-SKIPPED path (line 3248), after both early returns (3226, 3235).
- No `already gone` handling exists anywhere in `_reap_belam_oldest` or `_kill_window`; `_kill_window` swallows tmux failures with `except Exception: pass` (silent).

## Evidence

(a) no pane pid:
  record['window_id']=None, 'window_killed' absent, oldest @9 line GONE from file = False
(b) no chain under pane pid:
  record['window_id']='@9' (RESOLVED), 'window_killed' absent, oldest @9 line GONE from file = False

Both `skipped` records are written PLANNED-FIRST (`s12_reap.belam_reap`) and returned early — code path returns at 3226 (a) and 3235 (b), before the `_kill_window(oldest, ..., window_id=oldest_id)` call at 3248 that the hypothesis claims runs "on every SKIPPED path".

Verdict evidence for parent hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window is DISPROVED — the claimed behavior (window still killed by @id on every SKIPPED path, record carrying `window_killed: true`, `already gone` recorded for a vanished window) is not implemented in the current code. Both SKIPPED paths leave the oldest window alive, which is exactly the owner's original g15-12 concern (chain can stay above five).

## Agent Notes
SKIPPED cap paths (no pane pid / no descendants under pane pid) return EARLY (rotate.py:3226,3235) before _kill_window (3248); oldest window is NOT killed, record has no window_killed field, no already-gone handling. Behavior claimed by hypothesis absent in current code.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-a0feab19 (L4.158; first kid). (1) The hypothesis brief said the owner files g15 findings as nodes "fixed in-loop" and its CLAIM names the behaviour the cap must have: "on every SKIPPED path the oldest window is still killed by its @id". (2) What this kid actually did: it read rotate.py:3181-3260 and found that both early returns (no pane pid, and pane pid with no descendants) happen BEFORE `_kill_window` at what was then line ~3248, and it reproduced that through the window_path seam -- the ownership line stayed in the fixture file. I verified the same source lines myself. (3) The near miss: accepting its "disproved" as the round result would have satisfied "the claim was tested" and lost the mechanism -- an unfixed FIFO cap. So I did NOT stop there; I spawned a correction kid under the same target, carrying this node as the measured before-state. (4) Deviation from the node ceiling "CEILING: 1 kid": the first kid stopped at measurement, and the adjust branch of the parent loop exists for exactly a kid that misreads the brief; the second kid is a correction, not a second slice. This experiment node is kept as the failing-before evidence for experiment:a00-57f16627-9e9406, not as the round verdict.
<!-- THOUGHT:END -->

**2026-09-11T07:53Z director review at harvest (sanctuary-director gen XII, L4.158).** Re-ran on the round bytes: `python3 -m pytest extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotate_selfreap.py extensions/agi/tests/test_rotate_startup.py -q` → 58 passed; on the merged seat bytes (+templates) → see the harvest commit. Real-tmux probe with the round's rotate.py: `_kill_window('no-such-window', 'agi-rc', None, window_id='@999999')` → `already_gone` (tmux "can't find window" mapped, nothing raised), `tmux list-windows -a` count unchanged (9). Residue, no node: `_kill_window`'s return annotation still reads `-> None` while it now returns a status string — cosmetic, fix in the next rotate.py round (g15-18). The first kid's `disproved` is the reproduction of the pre-fix state and stays as its author wrote it; the second kid's `proved` is the fix. Merged into the seat.
