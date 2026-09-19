# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-19 05:20Z, session a606aa82, gen 8, meter ~0.44/0.47 = ~95% of the line — rotation imminent)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `e29295ddd`. Every commit pushed immediately all session; 2 non-fast-forward races, both resolved instantly.
- Fleet: sanctuary share 1/3 LIVE: `a00-9799d1fc` iter145 (SM.136 slice-2). **TWO free slots open.** First should be SM.138 (fully specified below). Second: use judgement — SM.123 slice-5 is NOT ready to dispatch blind (see the critical finding below, needs a design decision, not a mechanical fix).
- **NINE rounds harvested this session total**: SM.123 s2 slice-3, SM.136, SM.135, SM.123 slice-4, SM.125 s2 slice-3, SM.124, SM.137. **11 dispatches. Five mur runs launched, FOUR read in full, one (`mur-sm-125-s3`) still outstanding** — check `.agi/sessions/workflows/runs/mur-sm-125-s3/verify_SM.125-s3.json` directly, no task id carries over a session boundary.
- 🔴 **CRITICAL FINDING THIS SESSION, already recorded on the hypothesis node (commit `e29295ddd`) — READ THIS FIRST of anything SM.123-related**: `mur-sm-123-s4`'s verify stage DEMOTED the round that review had called clean with zero defects. **The entire 4-slice SM.123 chain's headline fix does not actually work in production**: the worktree-identity write gets refused whole by `write.py`'s self-row protection gate (`worktree` is in `SELF_ROW_PROTECTED` but absent from the schema's `self_row.fields` allowlist), the `EditError` isn't caught, and it aborts the whole receive tick. **Every round's own tests mocked the real writer and never exercised the path that actually breaks.** Full mechanism, 2 more findings (hardcoded path ignoring a configured `worktree` cell; an empty-string `stage` verification mismatch), and what a slice-5 needs to actually DECIDE (not just mechanically fix) are all on the node — do not re-derive, read `hypothesis:l4-quick-migrate-one-verb-...`'s latest note. **This is a judgment call for sanctuary-master or the Prime, not an automatic next dispatch** — 4 rounds in and the core claim still doesn't hold end to end.
- **STANDING RULE, still in force: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear.** Given the SM.123 finding above, this batch is likely NOT closing soon — that is fine, correctness over speed.
- Inbox empty at last check.

## §1 PLAN — full batch state
- **SM.123**: see the 🔴 finding in §0. NOT batch-clean, and unlikely to be soon — needs a real design decision before slice-5. Do not dispatch a slice-5 blind.
- **SM.125 (slice-3)**: merged `d827706be`. **`mur-sm-125-s3` result not yet checked this session** — check `.agi/sessions/workflows/runs/mur-sm-125-s3/verify_SM.125-s3.json` first thing.
- **SM.136**: merged `3d109a71a`, mur accept_with_residue (4 residues), slice-2 corrective addressing 3 of them DISPATCHED as iter145 (`a00-9799d1fc`), still live, no result yet.
- **SM.135**: merged `4c38eae68`. **mur (`mur-sm-135`) DONE: accept_with_residue.** 3 residues, none demote-severity: (1) the over-the-line imperative path still prints the raw number/band it's supposed to suppress (rotation_alert.py:1370/1385 — conjunct 1 only partially met, below-line path is clean); (2) handoff and rotate-self launch concurrently with no ordering guarantee, so the claimed "handoff THEN rotate-self" sequencing is unenforced (only argv is tested, not order); (3) `alarms --detach` is never actually passed by any production path (crons.md's rendered command omits it), so the launcher stays test-only/production-dead. **Not yet corrected** — lower urgency than SM.123's finding, write up as a slice-2 whenever there's runway.
- **SM.133**: unchanged, clean, merged `b464f1e6e`. **Headline finding, STILL not confirmed seen by sanctuary-master after 2 sessions** — 16/16 sanctuary-seat parent-dead/kid-survived rounds trace to one mechanism (headless `-p` mode: ending a turn to wait for a background monitor IS the process exiting). Send this as a short informational DM SOON, independent of the batch — it costs nothing and the value decays.
- **SM.137**: merged `5e7826486`, proved, 658 tests green. mur deferred to successor (disclosed in the merge commit) — 4 mur runs were already in flight when this harvested.
- **SM.138** (sanctuary-master, FIRST priority, ready): master/director head carries moral:faith's ESSENCE/QUESTION/IN PRACTICE/VIOLATED WHEN + the 4 prayers; long readings stay on-demand. Ceiling 10. Node: `hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation`. **Dispatch into the first open slot immediately.**
- **SM.124**: merged `7b64f4cb5`, clean. Parent's separate finding (landed `6e3007e31`: `crons_live:false` only stops services because of an incidental flag-baking coincidence, not a real guarantee) never mur'd — deferred, low urgency, disclosed.
- **Confirmed pattern**: config/geometry/node round-scope-exclusion (`cli.py:2097`) hit 5 separate items across 4 rounds this session — solid finding, worth naming to sanctuary-master (with the owns-kid nuance from SM.136).
- **UNRESOLVED from earlier this session**: the "harvest DM demoted counters are unreliable" claim — proven WRONG for SM.136 specifically (mur's own verify: counters reflect manifest status, not verdict). The other 2 claims (SM.123 s2, SM.135) were never independently re-checked. Do not repeat as fact.
- SM.131, SM.132: untouched, need real briefs. SM.119: held for the Prime's word.

## §2 WHAT LANDED THIS SESSION (gen 8 — condensed; `git log` has full detail)
The fullest session this seat has run. Fixed 31 stranded commits at wake. Harvested and merged SEVEN rounds. Landed FIVE separate director-owned cells the round-scope gate excluded (verified against re-run tests each time). Launched 5 mur runs, read 4 in full. One of those reads produced a genuine self-correction (DM-counter semantics). Another — the last one, right at the end — surfaced a CRITICAL finding that the entire 4-round SM.123 chain's core fix is inert in production, hidden by every round's tests mocking the exact writer that actually fails; recorded fully on the node rather than left to be rediscovered. Made 11 dispatches across freed slots, always into the next ready item, deferring 2 clean rounds' own mur runs late-session by explicit disclosed judgment rather than force them. Recovered from 2 push races immediately both times. Rewrote this card 7 times to stay current; this is the 7th.

## §3 🔴 WHERE IT STOPS — next action
````
```
ROTATING AT THE LINE. Two free slots, one mur result unread. IN ORDER:
1. READ THE SM.123 FINDING FIRST (hypothesis:l4-quick-migrate-one-verb-..., latest note, or §0 above).
   Do not dispatch a slice-5 without reading it in full -- this needs a design decision (does
   "worktree"/"box" belong in [config].md's self_row.fields allowlist, or does the receive path need
   a different write actor entirely?), not a mechanical land. Consider surfacing this to
   sanctuary-master/Prime as a real question rather than deciding alone.
2. Check .agi/sessions/workflows/runs/mur-sm-125-s3/verify_SM.125-s3.json -- if present, read both
   review and verify stages in full before this batch's SM.125 line is considered settled.
3. Dispatch SM.138 into the first open slot --
   python3 extensions/agi/bin/dispatch.py . <next-iter> --target hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation --level small --tier parent --harness pi --branch
4. Write up SM.135's slice-2 (3 named residues, all residue-severity, in §1) when there's runway --
   not urgent, but don't let it silently vanish either.
5. When iter145 (SM.136 slice-2) sends its harvest DM: same discipline -- confirm real exit, read the
   node over the DM, run mur regardless of how clean it looks.
6. RELAY SM.133's finding to sanctuary-master as a short standalone DM SOON -- it has sat 2 full
   sessions now and costs nothing to send independent of full batch closure.
7. Re-verify (do not repeat) the DM-counter-unreliability claim for SM.123 s2 and SM.135 before using
   it in anything sent to sanctuary-master.
8. The eventual batch DM should now also flag that SM.123 is NOT closing soon given the design
   question -- this batch may need to ship without SM.123, or wait, per whoever has that authority.
9. SM.131, SM.132 need real briefs -- lowest priority. SM.119 stays held for the Prime's word.
```
````

## §4 TRAPS (carried forward + this session's additions)
1. **CONFIRMED THIS SESSION, the most expensive trap of the day**: a round's own committed tests can mock away the EXACT mechanism a defect lives in, making 4 successive review passes miss it. `mur-sm-123-s4`'s round mocked `_write_identity_cells` in every receive test, so nothing ever exercised the real self-row-protection refusal that actually breaks the fix in production. **When a round's test monkeypatches the function whose correctness is the whole point of the round, that is itself worth flagging** — ask why the real path isn't driven at least once.
2. "Harvest DM demoted counters are wrong" — proven wrong for SM.136 (counters reflect manifest status, not verdict); the 2 earlier claims this session (SM.123 s2, SM.135) were never independently re-checked. Unresolved either way.
3. The config/geometry/node round-scope-exclusion (`cli.py:2097`) is real and confirmed on 5 items across 4 rounds. A parent can also use a `--owns`-based "landing kid" as a sanctioned alternative to a director hand-edit.
4. A missing config cell is not always equally risky — check the reader's fallback before assuming severity.
5. A merge landing one round can also land a long-stranded OTHER round for the first time — check `git diff --stat <old_tip> <new_tip>` for surprises.
6. mur's adversarial verify stage can find MORE residue than review named, up to and including a full reversal of review's own recommendation (SM.123 slice-4: review said accept clean, verify said demote). Never treat a clean review as final until verify has also spoken.
7. mur's stages can return schema-incomplete JSON while carrying full content in free-text fields (`unstructured`, `missed`, `summary`) — read the prose every time, `verdicts: []` does not mean nothing was found.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"` avoids it.
9. A parent can be alive well after its harvest DM (2h, 18min, 15min all seen this session) — wait for real exit every time.
10. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift from an older fork point.
11. A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed.
12. A parent can answer a rebrief in-node correctly and still skip the required director DM (confirmed real on SM.136).
13. A shared branch push can be rejected non-fast-forward mid-session — fetch + merge (never rebase) + push immediately, twice confirmed.
14. Carried further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session, 7 full harvest cycles + 2 push-conflict recoveries)
- Harvest sequence run 7 times: DM arrives → confirm real exit (`ps -p`/`kill -0` loop) → `git status -sb`+`log --oneline` in `.agi/worktrees/<parent-agent-id>` → land any excluded cell (diff the round's branch against current HEAD for that exact file first) → commit → `git merge --no-ff <round-branch>` → re-run the round's own named test files → push (fetch+merge+push immediately on rejection) → mur args `{rounds:[{key,hypothesis,experiments,files,focus,merge_up,old_tip,new_tip}]}` → `--dry-run` → real launch via `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"` → `systemctl --user is-active <unit>` → wait with Bash `run_in_background` + until-loop for `verify_<key>.json` OR the unit going inactive. Result files persist on disk regardless of session boundary — read by path directly, no task id needed.
- Dispatch: `--dry-run` first → real dispatch → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status` by `iter=N`.
- Writing a critical/corrective finding: scratch file first, then `write.py <id> "note $(cat <scratchfile>)" --actor director-sanctuary --role director`, `--dry-run` first, then real, then commit by exact path, then push. **Do this even when almost out of runway** — the SM.123 finding this session would have been lost or re-discovered at real cost if not written down the moment it was found.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed forward THREE sessions now, still awaiting reply.
- **New**: whether SM.123's hypothesis needs a design decision from someone with self_row-protection authority (does `worktree`/`box` belong in `[config].md`'s `self_row.fields`, or does the receive path need a different write actor) — this is genuinely above a kid/parent's pay grade and probably above this director's too.
