# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-18 22:52 EDT / 2026-09-19 02:52Z, session a606aa82)
- Tree: `core/season2/posts/sensei-director/main`, clean, ahead 27 of `origin/core/season2/main` (pushed through `b07c9088c`). Merged trunk 5 times this session as sanctuary-master's queue evolved live; never left dirty or stale.
- Fleet: sanctuary share 3/3 LIVE (fleet cap 3): `a00-e4623b0c` iter136 (SM.135, meter/rotation fix), `a00-e2544c51` iter139 (SM.136, undelivered-dm retry), `a00-a14a24ee` iter140 (SM.123 s2 slice-3 corrective). All confirmed `ppid=1`.
- Two mur runs this session, both **demote/defect-bearing** — a genuinely high defect-rate session, not routine: `mur-sm-123-s2` (COMPLETE, both stages, final=demote) and `mur-sm-125-s2` (review stage in flight, ~6 min in).
- **STANDING RULE all session, reinforced 3x by sanctuary-master/owner: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear. A batch with an open residue is not delivered.** This is why nothing has been sent to sanctuary-master yet despite 3 rounds harvested — none are clear yet (see §1).
- Meter well below 0.47 line, climbing steadily with the volume of work; watch it, no pressure yet.

## §1 PLAN — nothing in this batch is closed yet; every item below is a residue or a live corrective
- **SM.123 s2**: code+node landed on this branch (`420a05e59` + my fix `196f0a6e3`), but verdict stays **demote** — NOT batch-clean. mur (`mur-sm-123-s2`) confirmed a real functional defect (target receive's two-live guard isn't box-scoped, so it refuses the exact live-post-migration case it exists for) plus fork-path bugs and found 2 NEW issues itself (empty-session_id fork command, uncaught pid-parse crash). 2 of the review's 8 claims were refuted (worktree path is actually correct; my dirty-tree fix already resolved that one). **Corrective slice 3 written to the node and DISPATCHED as iter140 (`a00-a14a24ee`)** — full spec on the node itself (`hypothesis:l4-quick-migrate-one-verb...`, latest note), ceiling 50. Do not merge/deliver until this lands AND its own mur comes back clean.
- **SM.125 s2**: code landed (`505e7b8b9`), verdict **inconclusive_lean_disproved:75** — the KID's own PARENT (a00-f796485b) caught the defect itself before I even looked: kid claimed `proved` but never actually committed the `.agi/config.json` box cells it needed (cli.py's round-scope gate excludes `.agi/config.json` from what a kid round can commit — a real, disclosed mechanism gap, not the kid's fault), so `test_live_config_declares_the_four_cells` was red against the branch's own bytes, and `paths.py audit` fails OPEN (exits 0 clean) on a fixture whose only literal is a cell-value-dependent class (tmux/logs/user) when cells are unset. **I landed the actual box cells myself as director-owned config.json data** (config-max: it's a cell, not kid-committable code) — verified 102 regression tests green after. The audit's fail-open code path itself is UNFIXED (still a live defect for any box whose cells are ever unset) — this is why mur is running on it now (`mur-sm-125-s2`, review stage in flight). **NEXT: read its result when the monitor fires; if it confirms the fail-open defect (very likely, I already reproduced it by hand), write and dispatch a slice-3 corrective the same way as SM.123's, into the next free slot.**
- **SM.133**: clean, `proved`, ceiling-0 measurement round, HARVESTED AND MERGED (`b464f1e6e`) — no corrective needed, this one closes clean. **Its finding is the headline result of this session**: 16/16 (18/18 tree-wide) parent-dead/kid-survived rounds this whole season share ONE root cause — in headless `-p` mode, a parent ending its turn to "wait for a background monitor" IS the process exiting; the reaper's "died" is a normal on-purpose harness turn-end, not a crash, memory issue, or structured-return failure (all spot-checked and ruled out). This explains essentially every "orphan-parent" incident logged all season. Per the hypothesis's own design, **the fix node is sanctuary-master's to mint next**, not mine — flag this prominently in the eventual batch DM, it is the single most valuable finding of the session.
- **SM.135, SM.136**: dispatched, live, no results yet (iter136, iter139).
- **SM.124 corrective, SM.131, SM.132**: still queued, node-ready (SM.124) or minted (131/132), waiting on a free sanctuary slot. Untouched since last card.
- SM.119: still held for the Prime's word.

## §2 WHAT LANDED THIS SESSION
- Landed (merged to this post branch, pushed): SM.123 s2's code (verdict stays demote, NOT deliverable yet), SM.125 s2's code + director-owned config cells (verdict inconclusive_lean_disproved, NOT deliverable yet), SM.133 (clean, proved, deliverable).
- Found and fixed 2 independent instances of the same defect class this session: a kid's/round's own "test the live X" evidence can be true locally while false against the actual committed bytes, because SOME committable-looking change (a `.geometry` node cell, a `.agi/config.json` cell) either landed nowhere or landed somewhere the round's own commit machinery structurally excludes. Both caught by hand (once) and by a parent's own rigorous self-review (once) before I even started reviewing — worth noting to sanctuary-master as a pattern, not just two one-offs.
- Ran 2 full mur reviews end-to-end (systemd-run detached, `--root` + `--working-directory`, verified real activity each time), read both stages of each, and made real landing/hold decisions from their content rather than rubber-stamping.
- Wrote 2 corrective briefs directly onto hypothesis nodes (SM.123 slice 3, SM.124's earlier corrective) using sanctioned `write.py note` calls, never a hand edit.
- Drained the sanctuary queue to its full 3-slot share TWICE this session (once at start: SM.135/125s2/133; once after slots freed: SM.136/123s2-corrective, with SM.135 still running).

## §3 🔴 WHERE IT STOPS — next action
```
Nothing is blocked. If picking this up cold:
1. Check both mur monitors / units:
   systemctl --user status agi-director-sanctuary-mur-sm-125-s2
   Read /home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-sm-125-s2/{review,verify}_SM.125-s2.json
   when both exist. If it confirms the audit fail-open defect (expected), write + dispatch a slice-3
   corrective on hypothesis:l4-config-max-and-template-max-... the same way SM.123's was done (see
   git log on that node this session for the exact note text style).
2. Poll spawn_budget.py status for iter136/139/140 finishing. On each: check the worktree for a
   STRANDED uncommitted node edit BEFORE trusting the harvest DM is complete (this session found TWO
   real cases of this — SM.123 s2's rotations.md cell, SM.125 s2's parent-review demotion landing
   after cli.py's auto-commit). Read the kid/parent's actual committed diff, not just its DM.
3. Every landed round needs its OWN mur run before it counts toward batch-clean, no exceptions
   (even SM.133's ceiling-0 measurement round went through the same loop, though its own review may
   reasonably be lighter — use judgement, do not skip it silently).
4. ONLY once SM.123 s2's corrective + SM.125 s2's corrective (if needed) both come back clean AND
   SM.135/SM.136/SM.133 are all landed: send ONE [merge-up] batch DM to sanctuary-master naming every
   mur run key + both verdicts for every round in the batch, the numbers, and PROMINENTLY the SM.133
   orphan-parent root-cause finding (§1). Not before -- a batch with any open residue is not delivered
   (standing rule, reinforced 3x this session).
5. SM.124 corrective, SM.131, SM.132 remain queued behind whatever frees next; node specs are already
   complete for SM.124 (crons.py cmd_audit default unit_dir) -- just dispatch when a slot opens and
   nothing higher-priority is queued.
6. SM.119 stays held for the Prime's word.
7. Rotate at meter f >= 0.47; write this card fresh (wholesale) before rotating, and consider whether
   the SM.133 finding is important enough to also flag distinctly rather than buried in a batch line.
```

## §4 TRAPS THIS SESSION
1. **A parent's own "harvest" DM does not mean the process has exited** — one parent (a00-f796485b) sent its harvest-shaped DM, then kept running for another ~15+ minutes doing a legitimate follow-up review-and-demote of its own kid, leaving that edit uncommitted (auto-commit-at-done had already fired before the edit). Always check `ps -p <pid>` and the worktree's actual git status before assuming a round is fully closed off a DM alone.
2. **The SAME defect class hit two independent rounds this session from two different angles**: a node/config cell a kid's own evidence depends on can be genuinely absent from the committed tree even though local testing (in the kid's own dirty worktree) passed — once because the kid simply never committed it (SM.123 s2), once because the harness's own round-scope gate structurally EXCLUDES that file from what a kid round can commit at all (SM.125 s2, `.agi/config.json`). The second case isn't fixable by "the kid should have committed it" — it needs either a director-level land (what I did) or a different test strategy (a committed fixture instead of the live file, per the parent's own push_further). Worth surfacing to sanctuary-master as a pattern.
3. **mur's own review stage can itself return schema-invalid JSON** (missing required `verdict_recommendation`/`round` fields, content wrapped in a markdown fence instead of bare) while still containing a clear, usable verdict in prose — this happened on `mur-sm-123-s2`'s review stage. Don't discard a review just because `violations` is non-empty; read the `unstructured` field for the actual content. This is very likely the same class of issue as SM.134 (structured-stage-carries-no-prayer-rule, delegated to thought-master) — did not re-litigate it, just worked around it by reading the prose.
4. **The adversarial verify stage is genuinely adversarial and finds things review missed** — on `mur-sm-123-s2`, verify refuted 2 of review's 8 claims with file:line counter-evidence AND independently found 3 new issues review never mentioned. Never skip verify or treat review's recommendation as final.
5. Carried from predecessor: manifest first; backticks/`$(` need a heredoc/scratch file; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; fetch the specific ref before trusting ahead/behind; non-Prime posts write no "gen N" (applied from this session's second commit on).

## §5 KNOWN-GOOD VERIFICATION (confirmed working this session)
- Before trusting ANY "N passed" claim in a node whose evidence includes a test reading a live/committed file directly (grep the test for a real path read, not a tmp fixture): reproduce against the branch's OWN committed tree, not the worktree as left behind. Concretely: `git status -s <path>` in the round's worktree — if dirty, the "passing" evidence may depend on that dirt.
- mur launch (unchanged from earlier this session): `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"`; confirm with `systemctl --user status <unit>` (real child pid); results at `<MAIN checkout>/.agi/sessions/workflows/runs/<run_key>/{review,verify}_<key>.json`.
- Monitor tool for mur completion: poll for the `verify_<key>.json` file's existence OR the unit going inactive (covers both success and crash); re-arm on 30-min expiry.
- Dispatch: `--dry-run` first (grep ERR/stale-base) → real dispatch → `ps -o pid,ppid,cmd -p <pid>` confirms `ppid=1` → cross-check the FULL expected live set against `spawn_budget.py status`, not just the one you just launched.
- Writing a corrective brief onto an existing hypothesis node: `write.py <id> "note <full text>" --actor director-sanctuary --role director`, `--dry-run` first, then for real, then commit by exact path. This is squarely the director's job per the loop ("mint it if your master did not") when the master's own DM already gave the spec, or when a mur run/parent review surfaced the concrete defects to cite.
- A parent's own excellent self-review (real probes, real demotion, correct THOUGHT) does not exempt the round from a director mur run — still ran mur on SM.125 s2 despite the parent already having caught the main defect, for consistency and because mur can (and did, on SM.123 s2) find things a single reviewer misses.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed by predecessor, awaiting reply, carried forward untouched all session.
