---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-V
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

## §0 State (02:4xZ 09-25)
| | |
|---|---|
| post | belam-S2-L5-V gen 5 · seated 00:44Z 09-25 · Opus 5.5 · meter ~0.25 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC |
| merge | PASS 5 CLOSED 02:37Z → season2/main 8daa626e89 (pushed; grid commit there: 6 versions, 1 pre-existing error §6) · BASE 3b0c4e8e8f → TIP 5b7d503fa7 · 449 commits · 39 exp · 18 rounds / 4 chunks on pi-free · 27 min · 0 USD · 9 accept_with_residue · 9 demote · 0 RED · state reset (last_merged_town_sha 5b7d503fa7; notice/run_at/pass_started_at null) · crons file §2 = the PASS 6 template (goal:g1, board note) |
| residues | hypothesis:pass5-0925-residue-batch (goal:g1) · 3 code-defect hypotheses + veto hypothesis REOPENED → [decision] director-engine · 6 lm-* demotes → [merge-up] thought-master (→ director-thought) |
| directors | director-engine + director-thought, claude-sonnet-5 max · `doc:unified-director-brief` §1: ONE parent per round, `--tier parent --role parent --ladder-tier 0` |
| branches | owner 09-25: directors LOCAL-ONLY (never push) · merge-ups → thought-master, who ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` (ff'd d3f0403134 → 5b7d503fa7, 02:5xZ) + `season2/main` · brief §2 row replaced · [rule] dm x4 · no pre-push guard yet (offered to DE) |
| stream | LIVE on Twitch + X · PAUSED by stream-master's `brb` ~02:04Z (its `pgrep -a` printed relay keys into its own tool output; never the capture) · `back` = the owner's · `brb` for every post (`~/.local/bin/brb`) · `panic` the owner's (`/usr/local/bin/panic`) |
| owner asks | Jev: ANSWERED in chat -- the existing-tools survey ran 09-24 (troves/2026-09-24-jev-survey, experiment a00-ac62bcbe inconclusive-lean-proved 0.78, PASS 5 accept_with_residue); no trove survey ran 09-25 |
| crons | CHECK 4f4c68c7 "13 */4 * * *" (next 04:13Z) · SESSION-ONLY · retired belam panes hold no crons |

## §1 Plan
```
done   seated · crons · quorum · owner stream line (dm x4, ~/.local/bin/brb, doc:unified-head E) · PASS 5 (0)-(9)
       · the owner's Jev ask answered · owner branch rule: brief §2 row, [rule] dm x4, local-maxxing/main ff'd, grid no-ID fix → DE · keys: the owner's
next   04:13Z CHECK (§1 verbatim): live leases tier=parent only · otherwise quiet: decisions / reds / merge-ups / owner
open   round-mur ROUTED to director-engine as a WORKFLOW (behind g1.25) · PASS 5 residues (DE + TM) · §6
```

## §2 Landed (this seat)
f6dd6dad92 card at seating · 5b7d503fa7 trunk sync (season2/main key row) · da01751a85 HEAD stream line + card · 8daa626e89 season2/main PASS 5 merge (pushed) · bca1ec38d0 PASS 5 residue batch + 3 defect hypotheses + veto reopen + board line · 69fefbe2e2 card · origin/local-maxxing/main ff → 5b7d503fa7 · director brief §2 branches row + this card

## 🔴 Where it stops
```
02:4xZ 09-25 belam-S2-L5-V: PASS 5 closed at season2/main 8daa626e89 (18 rounds, 0 RED); quiet until the 04:13Z CHECK; stream held for the owner's back.
 1. CHECK fires 04:13Z: run section 1 of .agi/sessions/prime-merge.crons.md as written, plus spawn_budget.py status = tier=parent leases only.
 2. Otherwise quiet: answer only decisions / reds / merge-ups and the owner. The stream stays held until the owner runs back.
 3. A new pending delta -> the CHECK's case (b): 5 h notice, then a PASS 6 one-shot from section 2 (the template: goal:g1, board note, /tmp/belam-pass5 tooling).
 4. A successor at wake: RE-ARM the CHECK (CronCreate "13 */4 * * *", section 1 verbatim), re-link the quorum symlink (trap 10), write this card whole.
```
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the logs too when a post says it wrote |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text (defect minted) |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 4 | write.py body numbering can differ from file lines | `sub <old> => <new>` (literal); never ` && ` inside a unit |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py via sync.sh: temp index + ff-only, never a conflicted MAIN |
| 7 | two `note` units in one submit keep one; a body writer cannot share a submit with `thought` | one body writer per submit, `thought` alone |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi / pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | diff vs the doc node, `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit both by exact path |
| 11 | a Prime row edit on season2/main is reverted by that post's next key-row publish | the post merges origin/season2/main and confirms the cell (defect minted) |
| 12 | `cd` moves the session's working directory | absolute paths, `git -C`, subshells |
| 13 | the stream is LIVE | never print a secret, key, address or host name; one shows → `brb` |
| 14 | `.env` on local-town is `/data/work/agi/.env` | read credits from the MAIN root |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 16 | background writes of many nodes outlast the 120 s Bash timeout | pass a timeout |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 18 | at rotation a director reads HEAD + card, never the template | rules in doc:unified-director-brief; cards carry overrides only |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 20 | asking the owner for a go on a design the owner raised | decide, route, report · a workflow needs no hypothesis |
| 21 | a write.py sub whose OLD text holds the arrow token writes garbage | assert it absent; else replace the paragraph |
| 22 | a RETIRED pane's hook captured this LIVE card + spawned rotate-self --force for the seat (gen 4 01:59Z, its own f=0.4794; refused: behind 1) | rewrite the card whole; a retired pane cancels its own crons (gen 4 did) |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys (SM 02:04Z) | never print a process argv broadly; `pgrep -c` / `-x` only |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam commits on the trunk by exact path and never pushes it; belam pushes only `season2/main` + `local-maxxing/main` |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| experiment:a00-2a4dfb57-triage (09-18) has no mint_id -- every grid commit logs 1 error | `backfill-mint-ids.py --write` by its town (local-maxxing) or a director-engine round |
| stream `back` after stream-master's brb (02:04Z) | the owner's; keys never reached the capture per SM |
| director-thought's stray origin head `refs/heads/local-maxxing/season2/posts/director-thought/main` (owner: pushed by accident) | delete it (one `git push origin --delete`) -- a remote deletion, so the owner's go or thought-master's |
| retired belam panes I-IV + agi-98 still alive (a numeral-chain window is not reaped) | reap, or keep for the stream -- the owner's call; none holds a cron |
| global git identity on this box (box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | trigger met (brief.py b0b4fbc9b); opening it is the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
| thought-master beyond the director docs (goal moves / config) | config:* stays prime/owner-only; a scoped grant is a director-engine round |
