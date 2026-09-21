---
id: hypothesis:prime-merge-routine-is-one-cron-script
mint_id: 33ee0c710b864e1ca9a545ba570ea060
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: belam
scaffold_hash: 6f3986e6d4fbfc17
season: 2
testable_claim: "A single cron-driven script (prime_merge.py tick) reproduces the Prime's hand merge routine end-to-end on local-town: given a town trunk ahead of season2/main with landed experiments it sends the 5 h notice once, runs the merge-up-review in <=6-round chunks at run_at, merges --no-ff by SHA into season2/main only on all-GO, verifies, pushes, and never merges on a red -- proved by its own tests on a temp repo and one live tick."
title: "prime_merge.py: the Prime's town->season2/main merge routine is one cron script (assigned: director-engine)"
town: core
---
<!-- BODY:BEGIN -->
# prime_merge.py — the Prime's town→season2/main merge routine as ONE cron script

Owner 01:2xZ 09-21 (verbatim on goal:g14): check the town trunk periodically, one large mur, a 5 h resource notice to thought-master, quiet push-only. Owner 01:4xZ 09-21: crons persist in crons.py, config-maxxed; engine follow-ups (residues) are assigned to director-engine and documented. DONE by the Prime: cadence `prime_merge` on cron:crons (`13 */6 * * *`, box local-town, applied 01:5xZ) — INERT until this file exists (`test -f … && python3 … prime_merge.py tick --root {root}`); the interim runs are the Prime's own (first 06:39Z 09-21).

## Contract — `prime_merge.py tick --root <.agi>` (idempotent, state-driven, cron every 6 h)
State `.agi/sessions/prime-merge.state.json` {root, town, last_merged_town_sha, notice_sent_at, run_at, run_key, claim} — untracked, box-local.
1. fetch; TIP = town tip; BASE = last_merged_town_sha or origin/season2/main; BASE must be an ancestor of TIP (else exit 3, one [red] to the Prime).
2. delta = commits, experiment/hypothesis nodes, engine/config paths in BASE...TIP. No landed experiment → exit 0, silent.
3. No notice pending → ONE `[owner]` 5 h notice to thought-master (send.py; body from a file; claim ~3 GB RAM / 2 cores / no GPU; delta numbers; run_at = now + 5 h, off-minute) → state → exit 0.
4. Notice pending, now < run_at → exit 0, silent.
5. RUN: freeze TIP; rounds = one per hypothesis with ≥1 landed experiment (key, hypothesis, experiments, files = payload paths, focus, merge_up, old_tip, new_tip) + ONE `engine-delta` round (every engine/config path; focus: tests present, no secrets, no node deletions, no protocol regressions). `workflow.py run agi-merge-up-review --harness pi` in chunks of ≤6 rounds, sequential (a 15-item round timed out at 1800 s, SM 19:23Z 09-16); when director-engine's chained workflow (parent drain → mur → residues batched → batch mur) exists, call it instead — one config cell names it. Concurrency capped so peak RSS stays under the claim; peak measured and logged. Refuse (exit 3) while the suite lock is held or credits < floor 1.6 + the expected run cost.
6. All GO → root worktree `.agi/worktrees/prime-root` on `season2/main` (create from origin/season2/main if absent, else pull --ff-only) → `merge --no-ff TIP -m "merge <town> @<sha> into season2/main (prime_merge <run_key>: N rounds GO)"` → verify THERE: links 0 broken · goals byte-identical · smoke active ≥ previous (never drops) · commands.py run verify · no `.agi/nodes` deletion in the merge diff → push season2/main → `grid.py commit --all` there (the one branch the grid accepts) → state.last_merged_town_sha = TIP, notice cleared → ONE numbers-only note on goal:g14 + GOALS re-render, committed by exact path on the town trunk, pushed. Any red → exit 2, NO merge, ONE `[red]` line to thought-master and the Prime. Residues (findings that are not reds) → g15 hypothesis nodes with note `assigned: director-engine`, one dm listing them.
7. Never: dm anyone else; write in a post worktree; merge on a red; delete a node; force-push; rebase.
Tests: temp repo with root + town branches; fake runner via env `PRIME_MERGE_WORKFLOW_CMD`; transitions no-delta / notice / wait / run-GO / run-red; never-merge-on-red; ancestry refusal; chunking 13 → 6+6+1.

## Limitations measured by the Prime on local-town (candidate follow-up rounds, assigned to director-engine)
- L1 `workflow.py:1381` `_pi_harness_cfg` is config-over-env: `workflow.py run --harness pi` launches the config's `/home/ubuntu/.npm-global/bin/pi` even with PI_BIN set (pi_adapter.resolve_bin is env-over-config; heal.py:3113 env-first). Works here only because that path was made to exist by hand. Fix = env-over-config + one test.
- L2 crons.py: the optional `log:` cell is not placeholder-rendered — `{logs}` reached the crontab literally (01:5xZ 09-21); the cell was dropped. Fix = render `log` like `cmd`, or refuse an unrendered brace.
- L3 `.agi/config.json` `box.*` and `harnesses.*.bin` are core-town literals (/home/ubuntu…) in a tracked, merge-shared file; per-box values need the box overlay or `{user}`/`$PATH` resolution.
- L4 integration-branch names (`season2/main`, `season/s2`) omit the town trunk: `commands.py run verify` never stamps node-count on local-maxxing/season2/main; `verification.py window` reads season2/main's tip. The routine verifies in the season2/main worktree; the town trunk stays unstamped.
- L5 `bin-suite-fresh` fails on local-town: no suite timestamp was ever recorded here (5804/18/26 at 701ac93bc ran by hand). The routine does not run the suite (one runner per tree).
- L6 rotate-self `--force` into the prime slot wrote the successor as a spawn row at gen 1 (record gen_before 3 / gen_after 1; 0899a142e): the gen counter reset.
- L7 Bash-tool shells do not re-source the profile inside a running session: PI_BIN reaches only sessions seated after 05:22Z 09-20; the cron line sets it explicitly.
- L8 the Prime's interim session crons (Claude CronCreate) die at rotation and expire in 7 days — superseded by the cron:crons cadence once this script lands.
- L9 encryption-town: node + a checkout at ~/work/agi, no pi — not a mur host without an install pass.
- L10 `send.py send` takes the body from argv only (no --file); the owner's 00:2xZ 09-17 ruling (bodies are files, never argv strings) is still open (SM.78 struck).

## Agent Notes
assigned: director-engine (owner 01:4xZ 09-21: engine follow-up rounds and residues go to director-engine, documented and sent). Priority 1 = the script (it activates the applied cron:crons cadence prime_merge); L1 and L2 as its residues or their own rounds, the director's call. Merge-up = numbers-only dm to belam.

owner 01:56Z 09-21 (goal:g14): after a completed pass (all chunks + merge + verify + push) the tick sends ONE diagram-maxed report dm to thought-master (flow: delta -> mur[chunks] -> GO/red counts -> merge sha -> verify -> push; residues -> g15 nodes assigned director-engine); never per chunk. The 5 h notice is the only other dm. Reports and notes are diagram-maxed (one compact flow or table; negations, conditions, attributions, supersessions explicit).
