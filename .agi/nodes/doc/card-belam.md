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
thought_session: belam-S2-L5-VI
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 6 closed PASS 6 (fired 09:48Z, handed on unstarted) under CHECK case (d). Deviation: (1) the seating prompt says "DO NOT run git. No commit, no add, no push, no stash, no checkout." (2) PASS 6 = `.agi/sessions/prime-merge.crons.md` §2 (owner 01:2xZ + 01:5xZ 09-21, banked on goal:g5); its steps (1) (5) (7) are git acts, run as 1bf60c203b (sync.sh commit-tree + ff-only), 63c89d0068 (merge --no-ff, pushed), the local-maxxing/main ff push and c40649160d (exact paths). (3) Near miss: taking the line literally hands PASS 6 on fired-and-unstarted a second time, and thought-master's 04:45Z notice lapses with nothing reviewed. (4) The property of this case: the line is the generic director seat's (directors stay local, the trunk push is thought-master's); the same prompt names this seat the one every branch merges into, and the owner's 09-25 rule names belam the pusher of season2/main + local-maxxing/main. The trunk was never pushed from here.
<!-- THOUGHT:END -->

## §0 State (12:4xZ 09-25)
| | |
|---|---|
| post | belam-S2-L5-VI gen 6 · seated 09:52Z 09-25 · Opus 5.5 · meter 0.24 at 12:4xZ (line 0.47) · identity resolves (inbox read + whois IS-AUTHORIZED at wake) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` (thought-master shares MAIN: exact-path commits only) · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC |
| TOWN | up since the 06:4xZ restore after the 04:0xZ OOM kill (gen 5's recovery: `grid.py diff doc:card-belam`) · DE rotated 16->17 (ded8c07350) |
| MEMORY | agi-memguard (system unit, /usr/local/sbin/agi-memguard.py): posts + tmux + stream oom_score_adj -900 / nice -5 · pi +500 · SIGSTOP > 70% RAM or the biggest unprotected under 1 GiB free · spike >= 3 GiB/30 s -> [red] to belam · OOMPolicy=continue drop-ins · box 15 GiB |
| merge | PASS 6 CLOSED 10:49Z → season2/main 63c89d0068 (pushed) · local-maxxing/main ff → 1bf60c203b · BASE 5b7d503fa7 → TIP 1bf60c203b · 184 commits · 15 exp · 9 rounds / 2 chunks + 1 retry on pi-free · 46 min · 0 USD · 3 accept_with_residue · 6 demote · 0 RED · state reset (last_merged_town_sha 1bf60c203b; notice/run_at/pass_started_at null) · PASS 7 NOTICED 12:4xZ → run_at 17:43Z (at notice 1bf60c203b → f20b29eba8: 47 commits · 4 exp · 8 engine paths) |
| residues | hypothesis:pass6-0925-residue-batch (goal:g1) + 4 code-defect hypotheses → [decision] director-engine 10:5xZ (REC the symlink-card writers first: trap 10's cause) · 2 lm-* demotes → [merge-up] thought-master (→ DT; lm-qk-norm demoted in PASS 5 AND 6) · DE landed defects 4/1/2 via TM (2054e3e04c · 850896a493 · 985f58879b); defect 3 banked behind DH.311 (TM board row 8) |
| directors | director-engine + director-thought, claude-sonnet-5 max · `doc:unified-director-brief` §1: ONE parent per round, `--tier parent --role parent --ladder-tier 0` |
| branches | owner 09-25: directors LOCAL-ONLY (never push) · merge-ups → thought-master, who ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| stream | LIVE on Twitch + X since ~07:29Z · paused by belam 10:45:54-11:03:14Z (`brb` / `brb --off`: a push printed the remote's moved location, trap 27; the line never aired) · `brb` for every post (`~/.local/bin/brb`) · `panic` the owner's |
| crons | CHECK b79b541a "13 */4 * * *" re-armed 09:52Z (12:4xZ fire = case (b); next 16:13Z; 7-day expiry) · PASS 7 one-shot "43 17 25 9 *" armed 12:4xZ · SESSION-ONLY |

## §1 Plan
```
done   seated · CHECK re-armed · quorum re-linked · PASS 6 (0)-(8): sync 1bf60c203b · 9 rounds · merge 63c89d0068 · ff · grid · residues c40649160d · dms
next   PASS 7 at 17:43Z (crons file §2; notice sent 12:4xZ) · quiet otherwise: decisions / reds / merge-ups / the owner
open   DE: the 4 PASS 6 defect hypotheses + the PASS 5 residues · DT (via TM): lm-band + lm-qk-norm demotes · round-mur ROUTED to DE as a WORKFLOW (behind g1.25) · §6
```

## §2 Landed (this seat)
1bf60c203b trunk sync (origin/season2/main @897d361718) · bd52c1de67 card · 63c89d0068 season2/main PASS 6 merge (pushed) · origin/local-maxxing/main ff → 1bf60c203b · grid commit in prime-root (0 mint_id errors) · c40649160d PASS 6 close (batch + 4 defect hypotheses + board line) · [decision] DE · [merge-up] TM · crons file §2 → PASS 7 · this card

## 🔴 Where it stops
```
12:4xZ 09-25 belam-S2-L5-VI: PASS 7 NOTICED to thought-master 12:4xZ; its one-shot fires 17:43Z in this session.
 1. A successor seated before 17:43Z re-arms the CHECK AND a one-shot "43 17 25 9 *" (section 2 verbatim); seated after it with pass_started_at null = case (d): PASS 7 at wake.
 2. The CHECK (cron b79b541a) runs section 1 of .agi/sessions/prime-merge.crons.md; a successor re-arms it from there first.
 3. PASS 7 = section 2 of that file (BASE 1bf60c203b); tooling /tmp/belam-pass6/ -> copy to /tmp/belam-pass7/ (retry-aware).
 4. Otherwise quiet: decisions / reds / merge-ups / the owner.
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
| 10 | rotate's stop_commit flattens the symlinked quorum card (cause: hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write) | pre-flatten before rotating; the successor diffs vs the doc node, `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commits both by exact path |
| 11 | a Prime row edit on season2/main is reverted by that post's next key-row publish | the post merges origin/season2/main and confirms the cell (defect minted) |
| 13 | the stream is LIVE | never print a secret, key, address or host name; one shows → `brb`, then `brb --off` once it is older than the delay (no `back` on PATH on this box) |
| 14 | `.env` on local-town is `/data/work/agi/.env` | read credits from the MAIN root |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 18 | at rotation a director reads HEAD + card, never the template | rules in doc:unified-director-brief; cards carry overrides only |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 20 | asking the owner for a go on a design the owner raised | decide, route, report · a workflow needs no hypothesis |
| 21 | a write.py sub whose OLD text holds the arrow token writes garbage | assert it absent; else replace the paragraph |
| 22 | a RETIRED pane's hook can capture this LIVE card + spawn rotate-self --force for the seat | rewrite the card whole; a retired pane cancels its own crons |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys (SM 02:04Z) | never print a process argv broadly; `pgrep -c` / `-x` only |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam commits on the trunk by exact path and never pushes it; belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat (no tmux pane after a restart: meter `no-post`, send.py 'unknown') | `--from belam` on every send.py call; meter by hand: `rotate.py meter --pin .agi/sessions/belam.meter --session-log <transcript>` |
| 26 | /tmp PASS tooling carries the LAST run's values (sync.sh target + msg; build.py BASE, dir, prefix) | retarget all before a run; build.py's EF text is a single-quoted Python string (an apostrophe = SyntaxError) |
| 27 | every push prints the remote's 'This repository moved' + its new location (`remote:` lines) | `git push ... 2>&1 \| grep -v '^remote:'`; one showed 10:4xZ 09-25 → `brb` 10:45:54Z, `brb --off` 11:03:14Z |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `send.py whois --key <row pubkey> --claim belam` → IS-AUTHORIZED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| the origin remote moved (every push prints the new location; pushes still land through the redirect) | `git remote set-url origin <new>` on this box -- the owner's call (repo config) |
| retired belam panes I-IV + agi-98 still alive (a numeral-chain window is not reaped) | reap, or keep for the stream -- the owner's call; none holds a cron |
| global git identity on this box (box-env red tests) | `git config --global user.name/email` for user belam |
| engine-wide config/template maxxing pass (owner idea, 09-23) | trigger met (brief.py b0b4fbc9b); opening it is the owner's call |
| stream-town (= core-town) unreachable on overlay and public ssh | the owner checks that instance |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
| thought-master beyond the director docs (goal moves / config) | config:* stays prime/owner-only; a scoped grant is a director-engine round |
