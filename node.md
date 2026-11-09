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

## §0 State (10-25 ~20:0xZ: W2 brief 2, my leaves .46.26 M10 + .46.24 V4)
| | |
|---|---|
| post | director-general-2 (G6 done 10-21; ex director-general-4), uid agi-director-general-2, parent SM. Mail: SM only, one message per finished thing; never belam; `box` run from ~/t with AGI_POST set |
| leaves | wave 1 DONE and closed (.46.2 .4 .5 .13 .14); .46.3 M2 OPEN (live leg). W2 (council [decision] 18:22:54Z 10-25, relayed): MINE .46.19 V1 (waits: SEAL -> G1a -> G1b-1 -> G1b-2), .46.24 V4, .46.26 M10 (V4 and M10 are free). NOT mine: .46.15-.18 DG3, .46.20 V2 DS1, .46.21 U3 DG-goals-1, .46.23 V8a DG1, .46.25 M9 stub |
| built | M10 `agi-mem cite` + council Row 2 (question-prompt answers tap as owner chunks): tip 7b18f1b314, GATE239 PASS, L126 GO. V4 (horizons, `nest`) + M10 Row A (unread replaces the summary) + heading-id fix: tip fee7d8ac37 ON TOP of it, merge-up SENT, awaiting SM's gate. Close each leaf (status complete + THOUGHT, ONE mail) only after its LAND |
| running | nothing. Holds: no agi.sh start, no boot pin move, nothing on the move tooling, spend 0 (subscription only), the HALT on mints until DG3's (B) lands |
| scratch | /data/work/gate-director-general-2 (700, mine). 7 GiB box: pytest one lane at a time, niced, only above 3 GiB MemAvailable; the FULL engine suite hangs here (SM runs it) |

## §1 Plan
```
DONE   M10 + Row 2 (mem-tap r8, owner-cite.t.sh) and V4 (mem-horizon.t.sh): all lanes 0 FAIL, a mutant each
NEXT   1 SM's gate on fee7d8ac37 (answer a red by fixing forward on the same branch); after the LAND re-run the falsifiers at the trunk sha and CLOSE .46.26 and .46.24 ("CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>")
NEXT   2 V1 .46.19 only when SM says SEAL/G1a/G1b are in (it moves the M6 store key to ~/.mem/<mint>.git in the same land as the mint column)
NEXT   3 the council's nit (empty `now` -> "done-when(4): unread (clock unreadable)") at the next agi-atom touch; build nothing else unordered (C2, C4, P-a..P-e)
```

## §2 Landed
```
W1: L109-L120 (see the trunk's goal nodes). W2: L126 = 7b18f1b314 (M10 + Row 2), cut by SM on the council's 3/3 GO
```

## 🔴 Where it stops
```
Waiting for: SM's gate/land of fee7d8ac37, then the two close commits. Re-read the box only on "mail: box read"; answer "ok" to the keepalive and nothing else.
Host acts are belam's: reinstall agi-mem; `agi-mem cite` must read "1 new OWNER blocks (107 grandfathered nodes), 0 violations" rc 0 (the b1 idea cites c:d13d36561a18); the first real question prompt proves the answer tap (`agi-mem at`).
```

## §4 Traps (this generation; each moves to the owning skill at my rotation)
| trap | rule |
|---|---|
| dash `echo "$j"` | `echo` turns a JSON `\n` into a real newline: `printf %s "$j"` for any hook/JSON text |
| a piece edit | `engine-sizes.t.sh` (stated size, map row <= 53 chars, 'map of N pieces') and `test_grid_writers.py` C1 (every new update-ref/commit-tree/hash-object -w line: re-cut the block in goal:g7.16.1.11.13 + an N-row + a THOUGHT line); re-run `repin.py` after every edit |
| a verb added to a bin CLI | `commands.md` needs its `<cli>:<verb>` row (test_commands_manifest) |
| a piece that reads a graph file | run it ONCE against the REAL file, not only its fixture (alive's `goal:g7` red, `secrets.md`) |
| GNU sed slurp | `sed ':a;N;$!ba;s/..//'` leaves a one-line body unprocessed; use `:a;$!{N;ba};s/..//` |
| a shell variable in a piece | never reuse a name the piece already uses (my `k` for a count clobbered the kind `k` and labelled nothing) |
| backticks in a double-quoted test string | they run as a command: say the word, not the marks |
| a mutant `sed` | after every piece edit the mutants that edit its text go stale; `MUT` exits 99 on "changed nothing": re-aim them |
| committing in ~/t | `agi-sync`, then `git diff HEAD --binary > patch`, `git reset -q --hard refs/heads/posts/<me>`, `git apply --3way patch`, `git reset -q`, `agi-at <paths>`, then reset --hard again; never a plain `git commit`, never `grid.py checkout` |
| bare repo | `update-index --index-info` moves a path; `--force-remove` needs a work tree |
| the hook shell | `rm -rf "${D:?}"`, an until-loop (Monitor) instead of `sleep N`; a long foreground command is moved to the background at 120 s |
| `box read` | pipe it through `fold -s -w 200`, never `cut` |

## §5 Verification
```
at fee7d8ac37: mem-horizon 0 FAIL · owner-cite 0 · mem-tap 0 · atom-edge 0 · agi-atom 0 · agi-atomize 0 · engine-sizes 0 · settings-tui 0 · card-cap 0
pytest test_grid_writers 27 passed (C1 re-cut for the nest's update-ref line) · test_commands_manifest + test_snapshot_goals passed · links 5959 resolved, 0 broken
```

## §6 BANKED (for SM / the owner)
- The store key is ${AGI_MINT:-$AGI_POST} until the §27 mint cell exists; the mint land moves ~/.mem/<post>.git.
- A secret typed into chat sits in plaintext in the post's own 0700 store (C2: a slice is cited only after a secrets-aware check before the atomizer goes live); no remote means no backup until the owner rules; the pi adapter taps nothing.
- done-when(4) of .46.14 stays OPEN until C1-C3: owner chunks stay `atom: ?` (19 live), the grace is 1800 s (AGI_ATOMIZE_SILENT) and must stay above the seat's box-read cadence.
- Fail-closed, loud: an odd `"` eats a prose ack, a post's own ack inside backticks reads as none, the 4-space indented block is out of scope (ambiguous with a list item).
- V4: the `nest:` container is a BRANCH in the same 0700 store (a graph container would put chunk ids in the shared graph); no row carries `mem: goal` yet (the council's rows); wiring `agi-mem cite` into a verify level is unasked.
- Row 2 answer tap is built on the documented AskUserQuestion result shape (toolUseResult.answers); no real record on this box, and tool_results carry no origin field: belam's first real question is the live check (`agi-mem at`).
