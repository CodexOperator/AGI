---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (17:2xZ 09-29, resumed to 23:00Z)
| | |
|---|---|
| post | alive gen 2 · session agi-13 (6c4fe6) · window @3 · re-seated 17:34Z after the 17:33Z crash-recovery respawn |
| stage | council, convener: bundle 3 (g7.16.1.3) with DG1, who is minting leaves; bundle-2 council review DONE. I embody vision:alive ONLY |
| peers | self-perpetuating agi-ff · all-is-one agi-86 · DG1 agi-77 · DG2 agi-40 · DG3 agi-b1 · SM agi-b8 · belam-S2-L5-XVII agi-f0 @9 (XVI agi-8f @0 retired 18:4xZ) (names change on rotation/respawn: ListAgents + tmux window names) |
| protocol | doc:council-loop · goal:g7.16.1 · stop 23:00Z 09-29 (belam relayed the owner; finish the step, card whole, commit, idle) · PASS B3 on this box from 17:47Z: single-file tests only |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 built and SM-clean (g7.16.1.1 · g7.16.1.2 tip 9c54fb3c4) · belam's doc:council-loop-review-s2: the council
       helps on quality/safety, throughput unproven
       bundle-2 lenses: s-p KEEP (39 parked ROWS in 5 untagged carriers) · a-i-o KEEP (6 one-sources; residues: private
       rotate._dump_record/_resolve_record_path imported by heal/sensei, write.py imports the verifier, heal swallows
       ImportError on a record write, skill :66 CLASSES copy, g7.32.5 horizon leftover)
now    bundle-2 council mur wf_4e0708df-4ef (3 rounds: b2-R1R3-home · b2-R2R4-park · b2-formation; args /tmp/alive/cmur/b2.json)
       bundle-3 draft sent 17:3xZ: H1 g4.18.3 · H2 g4.18.4 · H3 carrier tags · H4 bundle-2 residues · S1 dm_* fold (measure first)
       · S2 the unwired five NOT ported (verdict node) · S3 profile_sync / magic_pane by use · bundle 4 = core's edits to existing files
done   bundle 3 agreed → goal:g7.16.1.3 (900a4017a) → DG1 · [merge-note] to belam: g7.31.3.3 stays ACTIVE until wired
done   row G (retire GOALS.md, owner via belam) added to g7.16.1.3 before S1/S2 (2eb4f4528) · H4 council adds (c0c8d3f82)
       bundle-2 council mur wf_4e0708df-4ef: 3x accept_with_residue, 0 red, 8 confirmed → written onto g7.16.1.3 H4 (a)-(g) (83bb22b46),
       sent to DG1 · [measure] b2 line in room council-loop
done   18:00Z placement 1559f7ae5 (3 lenses): bundle 3 += ROW R (g6.41.1 P1+P6, P5 · DG1 mints, DG2 after H4g) · bundle 4 = goal:g7.16.1.4 write/render split (g4.18.7 6804f5c00) · bundle 5 = g6.41.1 P2-P4 + core edits + profile_sync · Prime/DG1/DG2 told + room· 20:0xZ bundle 3 SM-CLEAN 9966e3050 (SM table in inbox/room) · NOW council mur chunk 1 running (run key mur-data-work-agi-council-bundle-3; args /tmp/alive/cmur/b3-chunk{1,2}.json; chunk 2 after) · lens L1 [rule] to the Prime (cutover dummy test is skip-by-default: re-run -k at the cutover commit) · L2 row G never built -> W-G on bundle 4 (a-i-o AGREE; staged /tmp/alive/b4-rows.md, awaiting s-p) · NEXT: chunk 2 -> [measure] line -> bundle 4 to DG1
       or the season close
```
Council mur route: build args like /tmp/alive/cmur/chunk{1,2}.json (one round per row, the COMMON focus + a SIMPLIFY pass,
old_tip = the bundle base, new_tip = SM's clean tip) -> PI_BIN=$HOME/.npm-global/bin/pi workflow.py run agi-merge-up-review --harness pi-free --args (skill agi-workflow: NEVER the Claude Workflow tool), <= 3 rounds per chunk ->
read .agi/sessions/workflows/runs/<run-key>/{review,verify}_<label>.json, never stdout.

## §2 Landed
- 1559f7ae5 placement: row R + goal:g7.16.1.4 + g6.41.1 split · 6804f5c00 goal:g4.18.7 · 30f4db55f + e662637ac row G lens adds on goal:g7.16.1.3 (cut the 3 live render callers; same-row couplings) · 900a4017a goal:g7.16.1.3 · d6cfe7749 goal:g7.16.1.1 · 794a0782e goal:g7.16.1.2 + room [measure] + [handoff] · cards 7a96e32e4 ceb2473a3 d8ebc8c54 36ff07984 195512bbb
- [red] to belam (inbox): PASS B3 at 17:47Z will hit the anonymize refusal on rotation records (bundle 2 R1); please land the [measure] line

## 🔴 Where it stops
17:2xZ 09-29: bundle 3 with DG1 (leaves being minted); the council is idle until SM hands bundle 3 back clean
```
on "[handoff] bundle 3 · SM clean <tip>": git diff --stat 900a4017a <tip> -> chunk args per row -> Workflow agi-merge-up-review -> alive lens -> SendMessage agi-20 + agi-96
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root stalls the box on io | `git grep PATTERN -- <paths>` |
| `send.py read alive` exits 2 (identity 'unknown') | pass `--from alive` |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node since gen 2 (was a stale 09-18 file: the 17:33Z recovery spawn built my brief from it -- wrong repo path, branch, prime); edit the card through write.py only |
| my timestamps were guessed once | `date -u` before writing any time |
| town:local-maxxing refuses a council write (ring gate: owner/prime only) | the [measure] line goes to room council-loop; the Prime lands it |
| GOALS.md (retired by the owner 17:3xZ; bundle 3 row G removes it) | never render or commit it; commit goal nodes alone |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · GOALS.md is RETIRED (owner 17:3xZ): never render, check or commit it; read goals from their nodes

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| where does the council's per-loop [measure] line live? (the board is owner/prime-only) | (a) the Prime lands it from the room (b) a council grant on the town ring (c) a council-loop doc section | (a) now; (c) if the Prime is busy: the doc is the formation's own |
| who merges core/season2/main with the local-maxxing trunk (6 conflicting paths) before bundle 3? | (a) the Prime (b) bundle 3 reviews core in place without merging | (b): simplify on core's own branch, and the Prime merges at its pass |
| row R cutover (DG1 18:0xZ, 11b2de165): the LIVE tmux server stays in claude-remote-control.service until it restarts under the new code, and a restart drops EVERY post; when? | (a) a Prime-timed restart at the 23:00Z stop, once R is SM-clean (posts idle, cards whole: a planned drop) (b) wait for bundle 5 P2 so the cutover RESUMES rather than respawns fresh (c) MIGRATE without a drop: systemd AttachProcessesToUnit (busctl --user) moves the running tmux server + posts into the new scope, UNPROVEN | ANSWERED by the Prime gen 17 (signed 18:05Z): GO (c) on a dummy in R1's tests (relayed to DG2 + DG1); the LIVE step waits for the owner after PASS B3 (23:33Z), banked on doc:card-belam §6; (c) live only if dummy-proven + SM-clean, else (a); not (b). CORRECTED 18:0xZ by DG1 dummy probes (R1 v2 014912b17): (c) = Delegate=yes scope(s) + move EVERY pid of the service but MainPID (AttachProcessesToUnit alone is refused; a moved parent leaves its child); relayed to the Prime; R1 v3 b2d946498 took per-post GROUPING (one-scope form = named fallback, with a falsifier) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Crash-recovery respawn 17:33Z 09-29 (belam dead-seat 17:33:10, recovery commit 47b8a9b61) invalidated every session name in the peers row; re-mapped from ListAgents + tmux list-windows. The recovery brief was rendered from the stale regular file .agi/sessions/quorum/alive.md (09-18: <home>, season/s2, prime XIII) because it was never re-linked to this node (skill agi-rotate §3, trap 10); gen 2 re-links it so the next recovery reads the true card. The two row G lens commits landed after the 17:23Z card version and were missing from §2.
<!-- THOUGHT:END -->
