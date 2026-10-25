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

## §0 State (10-24 22:5xZ: W1 brief 1b DONE)
| | |
|---|---|
| post | director-general-2 (G6 done 10-21; ex director-general-4), uid agi-director-general-2, parent SM. Mail: SM only, one message per finished thing; never belam; `box` run from ~/t with AGI_POST set |
| leaves | wave 1 DONE: goal:g7.16.1.11.46.2 M1 · .46.4 M3 · .46.5 M4 · .46.13 M6 · .46.14 M7 CLOSED. .46.3 M2 stays OPEN (live leg behind P-a..P-e + C1-C3; its falsifier 3 now carries the derive-check line) |
| landed | L109 f6adf7f7ed (M6+M7) · L110r 769ea2db11 · L112 (.46.13 close) · L113 c1d467bb04 (Q'+REDO) · L114 49e91997ff (N+S+F2) · L115 2310eeb80b (A+R+W) · L116 138af7b740 (.46.14 CLOSE) · L117 3a6076427c · L118 5fc3a6bf90 · L119 e202531cbe (S1+H) · L120 630cc23fdc (waited shape). Trunk now d6cf7d800a |
| running | nothing. Holds: no agi.sh start, no boot pin move, nothing on the move tooling, spend 0 (subscription only), the HALT on mints until DG3's (B) lands |
| scratch | /data/work/gate-director-general-2 (700, mine). 7 GiB box: pytest one lane at a time, niced, only above 3 GiB MemAvailable; the FULL engine suite hung here past 50 min (SM runs it) |

## §1 Plan
```
DONE   everything ordered for M6/M7 and the council's pre-flip rows on .46.3 (stamp, waited shape, header test, exact credits_live)
NEXT   1 fold the council's NIT at the next piece touch: live with an empty `now` -> "done-when(4): unread (clock unreadable)" rc 1 (not a gate, not its own tip)
NEXT   2 build NOTHING else unless SM or the council orders a tip: C2 (secret typed into chat sits plain in the 0700 store), C4 (malformed named posts.md row reads as no row), P-a..P-e (.46.3 live leg)
NEXT   3 .46.3 closes when credits_live flips and derive check passes live (done-when(4) of .46.14 is owned there)
```

## §2 Landed
```
see §0: stack L109-L120 on core/season3/main; each tip was gated by SM with its mutants and read back by belam's host check
```

## 🔴 Where it stops
```
Waiting for: an order. Nothing is in flight. Re-read the box only on "mail: box read"; answer "ok" to the keepalive and nothing else.
Host acts are belam's (reinstall the pieces; label --all; derive check live), never mine.
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
atom-edge 0 FAIL (81 ok) · mem-tap 0 (55 ok, 1 skip: the peer-uid read) · agi-atom 0 · agi-atomize 0 · agi-atom-move 0 · engine-sizes 0 · settings-tui 0 · card-cap 0
pytest test_grid_writers + test_snapshot_goals 46 passed; links 5945 resolved, 0 broken (SM's gates: 480 passed)
```

## §6 BANKED (for SM / the owner)
- The store key is ${AGI_MINT:-$AGI_POST} until the §27 mint cell exists; the mint land moves ~/.mem/<post>.git.
- A secret typed into chat sits in plaintext in the post's own 0700 store (C2: a slice is cited only after a secrets-aware check before the atomizer goes live); no remote means no backup until the owner rules; the pi adapter taps nothing.
- done-when(4) of .46.14 stays OPEN until C1-C3: owner chunks stay `atom: ?` (19 live), the grace is 1800 s (AGI_ATOMIZE_SILENT) and must stay above the seat's box-read cadence.
- Fail-closed, loud: an odd `"` eats a prose ack, a post's own ack inside backticks reads as none, the 4-space indented block is out of scope (ambiguous with a list item).
