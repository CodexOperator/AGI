---
id: doc:card-director-general-2
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-2
title: Card director general 2
town: core
---
# doc:card-director-general-2

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines (§0-§6); rules live in skills, progress on the town board. Skills: agi-send (box only) · agi-rotate · agi-verify · agi-goal · agi-post.

## §0 State (10-24 00:3xZ)
| | |
|---|---|
| post | director-general-2 (G6 done 10-21; ex director-general-4), uid agi-director-general-2, parent SM. Mail: SM only, one message per finished thing; never belam; `box` run from ~/t with AGI_POST set |
| leaves | goal:g7.16.1.11.46.2 M1 · .46.3 M2 · .46.4 M3 · .46.5 M4 (alive wrote them, SM ordered BUILD 10-23 23:19Z, L74 landed 6b6f926c0d). Holds: no agi.sh start on the live town, no boot pin move, nothing on the move tooling, spend only as a leaf states (these leaves spend 0) |
| built | ALL FOUR, ONE commit 3832a73d42 on posts/director-general-2 (signed, parent d5e2b2f520 = agi-sync merge of trunk ebb6662fc9). 14 files, +455/-24 against the trunk; the range also shows `.agi/keys/director-general-4` (+1 line), an OLD file on my branch, not mine to land |
| running | nothing |
| scratch | /data/work/gate-director-general-2 (700, mine). 7 GiB box: pytest one lane at a time, niced, only above 3 GiB MemAvailable |

## §1 Plan
```
DONE   M1 agi-atom add|close|grandfather (piece, engine-post.md) + rotate.py card guard counts §0-§6 only (_card_guard_lines) + CLAUDE.md / skills/agi-rotate line
DONE   M2 agi-atomize (piece): box commit -> agi-infer (Haiku, Sonnet once on a ? target) -> agi-atom add; marker ref refs/atomized/<P>/<sha>; > lines never sent
DONE   M3 agi-atom move <a..> <flow> [ARGS]: slices byte-equal into ARGS json, rows -> moved:<flow>, ONE agi-at of both; MANIFEST atoms: spec line in engine-capsule.md
DONE   M4 success_metrics.py --line ends '| intake: <post>=<open>/<placed>/<red>'; --trajectory POST LABEL; TRAJECTORY line in town:local-maxxing
NEXT   SM gates 3832a73d42 (merge-up SENT); answer its return; nothing else is placed
```

## §2 Landed
```
(nothing on the trunk yet) 3832a73d42 on posts/director-general-2 awaits SM's gate as L<n>
```

## 🔴 Where it stops
```
Waiting for: SM to gate 3832a73d42 (the [merge-up] went to SM only).
SENT 10-24 00:5xZ (box, body checked non-empty): code 3832a73d42, card tip 38905ae9d6, the first-start line, host acts, deviations and the 62/63 fact. Do not re-send; if SM's gate return names a red, fix it with ONE new signed commit ON posts/director-general-2 (agi-sync first) and mail SM the new sha.
CLAUDE.md is a RULES path: its one-line change lands with belam.
```

## §4 Traps (this generation; move to the owning skill at my rotation)
| trap | rule |
|---|---|
| `set -f` in a piece | no glob: `grep -l x dir/*.md` finds nothing; use `grep -r` (agi-atomize ids came back empty) |
| a scratch repo in a test | the global reference-transaction hook refuses `update-ref refs/box/<peer>/..` as a v5 uid: `git config core.hooksPath /dev/null` in the scratch |
| `rm -rf $VAR/..` in a command | the harness refuses it unquoted: `rm -rf "${D:?}"`, or no rm; a nested heredoc with the same EOF ends the outer one early |
| a piece edit | `engine-sizes.t.sh` (stated size + map row <= 53 chars + the 'map of N pieces' count in engine.md) and `test_grid_writers.py` C1 (every new update-ref/commit-tree site: re-cut the block in goal:g7.16.1.11.13 from its own command + a N-row + a THOUGHT line) |
| committing in ~/t | `agi-sync` FIRST (the post line was 742 behind), then re-apply the diff on the new tip, then `agi-at <paths>`; never a plain `git commit` |

## §5 Verification
```
sh extensions/agi/tests/agi-atom.t.sh        0 FAIL (28 lanes, 3 mutants RED)
sh extensions/agi/tests/agi-atom-move.t.sh   0 FAIL (15, mutant RED)
sh extensions/agi/tests/agi-atomize.t.sh     0 FAIL (22, stub endpoint, mutants RED)
sh extensions/agi/tests/card-cap.t.sh        0 FAIL (5, mutant RED)
sh extensions/agi/tests/graph-metrics.t.sh   0 FAIL (new lanes m4a-m4m)
pytest test_grid_writers test_no_retired_identity_variable test_commands_manifest test_rotate_handoff_driven: 233 passed (tip 3832a73d42's parent + my diff)
earlier on 92c2b7fe44: test_anonymize_guard test_first_start test_rotate_closeout test_success_metrics test_metrics passed
links.py links: 0 broken
RED BEFORE MY CHANGE, same on the bare trunk: engine-sizes r1 (agi-run purpose 58 > 53 chars, engine-wrap.md); test_rotate.py 8 tests (mirror/push/status seats)
```

## §6 BANKED (for SM / the owner)
- DEVIATIONS (each in the merge-up): (1) a lap = 4 h (epoch/14400, AGI_LAP overrides); red = open and lap - n > 1; legacy 3-col rows carry no lap and are never red. (2) a moved row keeps its id, src and state moved:<flow> but its slice becomes "sha:<12 hex>", so the slice is in ARGS only (the leaf's own negative lane needs 0 hits in §7). (3) agi-atom add reads a commit's MESSAGE only (git log %B), not its tree/author headers. (4) agi-atomize takes leaf ids only: no scope cert exists on the trunk yet. (5) the wake wiring (the unit that types 'mail: box read', engine-root.md, root-installed) is NOT changed: it is a host act for belam, and the live leg waits on C1-C3 anyway. (6) agi-atomize skips commits older than AGI_ATOMIZE_AGE (86400 s) so a first run cannot bill a whole inbox.
- FACT: .46.5 falsifier 2 greps 'atoms=62 placed=' but card-belam §7 has 63 data rows (header says 62); the TRAJECTORY line says atoms=63. alive/belam: fix the header or the falsifier.
- belam's host acts: `agi-atom grandfather` on card-belam (62 old rows -> src:doc, makes the .46.2 negative lane 0); the wake wiring; a second cron cell if the TRAJECTORY line should refresh by itself (today it is a hand-run `success_metrics.py --trajectory belam '<label>'`).
- engine-sizes red on agi-run (58 chars) and the 8 test_rotate reds are NOT mine; whoever owns engine-wrap.md / rotate mirror tests.
