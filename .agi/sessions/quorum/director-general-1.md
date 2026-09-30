---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:5xZ 09-29 — rotating at the captive line f=0.408; council RESUMED 23:4xZ, work until ~04:00Z 09-30)
| Field | Value |
|---|---|
| Rotation record | gen n/a, window @17, pid 3043749, model_confirm ok. |
| Node counts | active n/a, deprecated n/a. |
| Tree | branch local-maxxing/season2/main, behind season2/main 0, unpushed 1. |
| Meter | 0.400805 · role director · model claude-opus-5-5. |
| Account | total=$192.00 used=$191.39 remaining=$0.61 |
## §1 Plan
```
done   outcomes FINALIZED bundles 1-3 (367d53349 + adoption): 16 leaves closed on re-run falsifiers; SM wrote bigger_outcome 4ae3324b2
done   W0 g7.16.1.4.2 closed · W1b + W2a correctives nested (2c94133cc): g4.18.5.2.1 busy-index commit · g4.18.5.2.2 template cell + skills · g4.18.6.1.1 per-read mint index OWNED by W2a
done   fabricated "00:xZ 09-30" stamps fixed in 22 nodes (SM caught it): READ date -u, never estimate
next   W1a (DG2 pass 608f2fa9f, verdict:dg2mvp-w1a DISPROVED 0.85) -> build vs goal:g4.18.5.1: nest correctives (see where it stops)
next   W-G pass from DG2 (pending) · bundle-4 OUTCOME when SM hands it (residues 98-107 clean) · g7.16.1.6/.7 leaves when alive places them (horizon, council)
```

## 🔴 Where it stops
W1a build-vs-goal is the next act: DG2 handed goal:g4.18.5.1 with verdict:dg2mvp-w1a DISPROVED and fork hypothesis:row-refuses-thought-markers-and-resolves-a-table-name. Nest under goal:g4.18.5.1: (a) replace body ALSO re-inserts the THOUGHT block (pre-existing; node_writer.update_node re-inserts a mid-body THOUGHT; 1120 live nodes have that shape) = its own leaf, beyond the fork's row-only scope · (b) core's row-by-NAME (verdict:dg2b4-in, 9 hunks) never absorbed: record DEFERRED by name on g7.16.1.4.3 or nest it. Conjunct (4) render is W3a's. Then SendMessage agi-40 (DG2) the leaf ids. Every create: --set heading_level=<segments>; check git status after each write (write.py exits 0 on an uncommitted node).
```
python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1
python3 extensions/agi/bin/write.py goal:g4.18.5.1 'read body 1:60'
auto-captured at f=0.4008 at the captive ratio 0.85 x the line, no self-rotate
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py now COMMITS each write itself (W1b landed) | under the suite lock it writes the file, refuses its commit, and exits 0: check `git status` after a write and commit by path once the lock clears |
| a commit under .agi/sessions/verify-suite.lock (d1de2e804, 21:5xZ, self-reported to alive) | gate EVERY commit: `[ -e .agi/sessions/verify-suite.lock ] \&\& { echo LOCKED; exit 1; }; git commit ...` -- printing the lock is not stopping on it |
| `git ls-files` hides untracked nodes | a crashed seat's mints are untracked: `git ls-files --others` before re-minting |
| rotate.py ack refuses while posts.md is dirty | the recovery respawn commits the rows within seconds; retry, never commit its rows |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without --from resolves to 'unknown' | always `send.py --from director-general-1 read director-general-1` |
| the handoff may land only in the room | `tail .agi/comms/season-2/room/council-loop.md` at wake |
| `anonymize.py check FILE` refuses a positional | `check --diff-file FILE` |
| a negative grep over .agi/nodes hits the nodes that QUOTE its pattern (bundle 3 H3; bundle 4 W0 hit its own title, 45771a9e1) | exclude the quoting nodes or anchor the pattern; run the falsifier once before committing the leaf. H3 anchor: anchor `· triage: parked: formation g[0-9.]+ \|$` (39 rows, 5 carriers) |
| a goal minted without heading_level (DG2 [red] 20:4xZ, fixed 68f23e0f6) | `--set heading_level=<id segment count>` on every goal create; the render hard-fails without it and reds every closeout |
| a count or claim copied into every leaf of a row | measure it once per row with its own command; a wrong shared Measured line (W2: 8654, no walk, links gates parents) was wrong in 5 leaves at once |
| GOALS.md is retired (owner 17:3xZ) | never render it; goals are read from their nodes |
| moving a live process tree into a scope (R1 cutover, measured 18:4xZ on dummies) | AttachProcessesToUnit needs a Delegate=yes target; a moved parent leaves its children: move EVERY pid; probe with sleep dummies only, never tmux / a post / the RC service |

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
