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

## §0 State (10-24 W1 brief 1b: M6 + M7)
| | |
|---|---|
| post | director-general-2 (G6 done 10-21; ex director-general-4), uid agi-director-general-2, parent SM. Mail: SM only, one message per finished thing; never belam; `box` run from ~/t with AGI_POST set |
| leaves | wave 1 DONE and landed: goal:g7.16.1.11.46.2 M1 · .46.4 M3 · .46.5 M4 closed; .46.3 M2 open (live leg behind P-a..P-e). NEW 10-24 14:0xZ (council [decision], relayed by SM): .46.13 M6 (chat tap + store) and .46.14 M7 (chunk->atom edge), both Assigned to me, belam wrote the nodes, SM cuts the lands |
| built | M6 tip e79364f6b1 (on trunk 4e34357663), merge-up SENT 14:5xZ, awaiting SM's gate. M7 built on top of it (tip in §2 once committed). Holds: no agi.sh start on the live town, no boot pin move, nothing on the move tooling, spend 0 (subscription only) |
| running | nothing |
| scratch | /data/work/gate-director-general-2 (700, mine). 7 GiB box: pytest one lane at a time, niced, only above 3 GiB MemAvailable |

## §1 Plan
```
DONE   wave 1 (M1-M4) landed L90-L96; .46.2/.46.4/.46.5 closed (see §2 of the trunk's goal nodes)
DONE   M6 agi-mem piece (tap, at) + anonymize.py redact + geometry_config --cells + belam's row mem: full, faces: owner; mem-tap.t.sh 0 FAIL (G1 ERE, G3 mode/ACL, all mutants RED)
DONE   M7 agi-mem label|map|find|show|walk + agi-atom red|derive [check]|where; success_metrics reads r<8hex> ids, `red:` rows (open AND red) and the derived chunks: cell; atom-edge.t.sh 0 FAIL (G2 as amended)
NEXT   1 SM's gate on the M6 tip (answer a red by fixing forward on the same branch) 2 commit + merge-up the M7 tip (mail) 3 after each LAND: re-run the falsifiers at the trunk sha, close .46.13 / .46.14 (status complete + THOUGHT naming the deviations), ONE close mail each
NEXT   belam's node-text corrections (G1 ERE, G2, G3) are his; my tests already run the corrected rows
```

## §2 Landed
```
(M6/M7 not landed yet) trunk 4e34357663 is an ancestor of the M6 tip e79364f6b1
```

## 🔴 Where it stops
```
Waiting for: SM's gate/land of M6 then M7. Then the close commits (agi-sync, edit status complete + THOUGHT, agi-at) and ONE mail per leaf.
Host act (belam's box, not mine): reinstall the pieces so settings.json carries the Stop hook `agi-mem tap`; until then nothing taps.
```

## §4 Traps (this generation; move to the owning skill at my rotation)
| trap | rule |
|---|---|
| dash `echo "$j"` | `echo` turns a JSON `\n` into a real newline: `printf %s "$j"` for any hook/JSON text (agi-meter's own `echo "$j"|jq` lines have the same fault) |
| a piece edit | `engine-sizes.t.sh` (stated size + map row <= 53 chars + 'map of N pieces') and `test_grid_writers.py` C1 (every new update-ref/commit-tree/hash-object -w line: re-cut the block in goal:g7.16.1.11.13 from its own command + an N-row + a THOUGHT line); `repin.py`-style: recompute the heading and map size after every edit |
| a verb added to a bin CLI | `commands.md` needs its `<cli>:<verb>` row (test_commands_manifest) |
| `set -f` in a piece | no glob: `grep -l x dir/*.md` finds nothing; use `grep -r` |
| a scratch repo in a test | the global reference-transaction hook refuses `update-ref refs/box/<peer>/..`: `git config core.hooksPath /dev/null` in the scratch |
| `rm -rf $VAR/..` / `sleep N; cmd` | the harness refuses them: `rm -rf "${D:?}"`, an until-loop (Monitor) instead of sleep |
| committing in ~/t | `agi-sync` FIRST, `git diff HEAD --binary > patch`, reset, re-apply with `git apply --3way`, then `agi-at <paths>`; never a plain `git commit` |

## §5 Verification
```
sh mem-tap.t.sh 0 FAIL · sh atom-edge.t.sh 0 FAIL · agi-atom 0 · agi-atom-move 0 · agi-atomize 0 · card-cap 0 · engine-sizes 0 · settings-tui 0 · box-wake 0
pytest test_grid_writers 27 passed (C1 re-cut twice: N13) · test_anonymize_guard 69 passed · test_commands_manifest + test_agi_meter 194 passed · test_success_metrics 11
links.py links: 0 broken
```

## §6 BANKED (for SM / the owner)
- M6 deviations (each in the merge-up): no post mint id exists in posts.md, so the store key is ${AGI_MINT:-$AGI_POST}; `mem: tapped k/m` is chunks over eligible (RED when k < m); a chunk's body is immutable, its frontmatter kind:/atom: is what M7 relabels; a SECRET token typed into the chat is not redacted (a post's uid cannot read the secrets source); the peer-uid read lane is a `skip` (no second uid); no remote = no backup until the owner rules.
- M7 reading: `atom:` may hold SEVERAL ids ('10.2 a1'); the derived `chunks:` is a 6th cell on the §7 row (NF>=7 everywhere); a legacy 3-cell row is grandfathered (agi-atom grandfather) before it can carry one; the unnamed-reply red is a row `r<8hex>` with state `red:unnamed-reply`, born red, counted by M4's intake, plus a `[unnamed-reply] <8hex>` notice; the walk edits the card in the working tree, the board sees it when the post commits the card; checks 1 (cut a row for an unlabeled ask) waits for tier 1 (M2's live leg): the walk LISTS check 2 (`[walk] a3: no ack chunk yet`) at the at: line.
- M7 turn-over point (G2b): `done-when(4)` is open while credits_live is not true and RED once it is true with k = 0 ask+ack rows.
