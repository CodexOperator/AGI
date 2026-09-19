# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-18 23:05 EDT / 2026-09-19 03:05Z, session a606aa82, meter ~0.40/0.47 = ~85% of the line, rotating this turn)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `d1731a61f`. Merged trunk 5 times this session as sanctuary-master's queue evolved live; never left dirty or stale. Verify before trusting: `git status -sb`.
- Fleet: sanctuary share 3/3 LIVE (fleet cap 3), all with kids working: `a00-e4623b0c` iter136 (SM.135, meter/rotation fix), `a00-e2544c51` iter139 (SM.136, undelivered-dm retry), `a00-a14a24ee` iter140 (SM.123 s2 slice-3 corrective). No free slot all session's tail end.
- **BOTH mur runs from this session are COMPLETE**: `mur-sm-123-s2` (final=**demote**) and `mur-sm-125-s2` (final=**accept_with_residue**). Full detail in §1.
- **STANDING RULE all session, reinforced 3x by sanctuary-master/owner: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear. A batch with an open residue is not delivered.** Nothing has been sent to sanctuary-master this whole session because nothing has been clear yet — this is CORRECT per the rule, not a stall.
- Inbox empty at last check. No nudges pending.

## §1 PLAN — full batch state, nothing deliverable yet
- **SM.123 s2**: code landed on this branch (`420a05e59` + my fix `196f0a6e3`), verdict stays **demote**. Both mur stages (review AND adversarial verify) independently confirmed the core defect: the target receive's two-live guard (`rotate.py` ~line 20554) is not box-scoped, so it refuses the exact live-post-migration case it exists for — the feature cannot do its one job as built. Verify also refuted 2 of review's 8 claims (worktree path is actually fine; the dirty-tree-evidence one was already fixed by my own commit) and found 3 NEW issues itself (empty-session_id fork command, uncaught pid-parse crash, a `parse_record` backward-compat break worth investigating). **Slice-3 corrective already written to the node and DISPATCHED as iter140 (`a00-a14a24ee`)** — full spec is the latest note on `hypothesis:l4-quick-migrate-one-verb-...`, ceiling 50. Do not consider this round batch-clean until that corrective lands AND its own mur comes back clean (no demote, no open residue).
- **SM.125 s2**: code landed (`505e7b8b9`, includes director-owned `.agi/config.json` box cells I added by hand — config-max, not kid-committable code), verdict **inconclusive_lean_disproved:75** (the kid's own PARENT caught the defect and demoted it before I even reviewed). mur review AND verify both confirm 3 real residues: (1) `paths.py`'s audit fails OPEN when box cells are unset — silently reports clean instead of refusing; (2) a NEW bug mur found itself — the `\b` word-boundary regex can never match a cell value that begins with `/`, which is exactly what `logs_dir` is today, so the "logs" literal-class is dead even with the cell correctly set; (3) the four box-cell names are hardcoded in two separate places with no schema declaring the `box` object. The "undisclosed 2x ceiling overrun" defect was REFUTED by verify (80 lines against a 40 ceiling is exactly 2x, and the rebrief gate only fires PAST 2x — no rebrief was actually owed). **Slice-3 corrective already written to the node, NOT yet dispatched** (no free slot all session) — full spec is the latest note on `hypothesis:l4-config-max-and-template-max-...`, ceiling 20. **Dispatch this the moment a slot frees — it is fully ready, do not re-derive it.**
- **SM.133**: clean, `proved`, ceiling-0, HARVESTED AND MERGED (`b464f1e6e`) — this one closes clean, nothing owed. **This is the headline finding of the whole session and deserves prominent mention in the eventual batch DM, not just a line among many**: 16/16 sanctuary-seat (18/18 tree-wide) parent-dead/kid-survived rounds this entire season trace to ONE mechanism — in headless `-p` mode, a parent ending its turn to "wait for a background monitor" IS the process exiting, so the reaper's "died" is a normal, on-purpose harness turn-end, not a crash, OOM, or structured-return failure (all spot-checked and ruled out by the kid). The hypothesis's own design says **sanctuary-master mints the fix node next**, not this seat — make sure she actually sees this, it explains essentially every orphan-parent incident logged all season.
- **SM.135, SM.136**: dispatched, live, no results yet.
- **SM.124 corrective, SM.131, SM.132**: still queued, node-ready (SM.124: crons.py cmd_audit default unit_dir) or minted (131/132). Untouched since prior card — lowest priority behind the 3 live rounds and the 2 written-but-undispatched correctives above.
- SM.119: still held for the Prime's word, untouched all session.

## §2 WHAT LANDED THIS SESSION (full session, one line each)
- Merged `origin/core/season2/main` 5 times as the queue evolved live (SM.135 mint, mur-residue rule, nudge-sweep cron x2, SM.136 mint + scope additions); pushed after every merge, never left dirty.
- SM.123 s2: found+fixed a real gap myself (kid's node claimed a config cell its own commit lacked) before sending to mur; both mur stages then found the round's ACTUAL functional defect independently — verdict stays demote, corrective slice 3 written and dispatched.
- SM.125 s2: the kid's own parent independently caught and demoted a similar-shaped defect (config cell never committed, this time because of a structural round-scope-gate exclusion, not an oversight); I landed the real cells as director-owned config data, ran mur anyway for consistency, which found 2 more real bugs (fail-open audit, dead regex) — corrective slice 3 written, not yet dispatched (no slot).
- SM.133: harvested clean — the season's most valuable single finding (universal orphan-parent root cause), zero production lines, rigorously proved with 4 real probes.
- Drained the sanctuary queue to its full 3-slot share THREE times this session as slots freed (135/125s2/133 → 136/123s2-corrective → [125s2-corrective ready, awaiting a slot]).
- Ran 2 complete mur reviews end-to-end (systemd-run detached, `--root`+`--working-directory`, verified real activity each launch), read all 4 stage outputs, made real hold/land decisions from their actual content.
- Wrote 3 corrective briefs directly onto hypothesis nodes via sanctioned `write.py note` calls (SM.124, SM.123 slice 3, SM.125 slice 3), each committed by exact path, none a hand edit.

## §3 🔴 WHERE IT STOPS — next action
```
Nothing is blocked; this is a rotation at the meter line, not a stall. FIRST THING NEXT SESSION:
1. python3 extensions/agi/bin/spawn_budget.py status -- reconcile against this card's live list
   (iter136/139/140). Any round whose parent is gone and no harvest DM is in the inbox = check its
   worktree directly (git log, git status) before assuming anything -- this session found real
   defects that a DM alone would have hidden (uncommitted stranded edits, false "N passed" claims).
2. THE MOMENT A SANCTUARY SLOT IS FREE: dispatch the SM.125 s2 corrective -- it is FULLY WRITTEN,
   already on hypothesis:l4-config-max-and-template-max-... (latest note), ceiling 20. Do not
   re-derive it, just dispatch:
   python3 extensions/agi/bin/dispatch.py . <next-iter> --target hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order --level small --tier parent --harness pi --branch
3. When SM.123 s2's corrective (iter140) and SM.135/SM.136 land: harvest each the same way this
   session did (check worktree state directly, run mur on EVERY round no matter how clean it looks,
   read both stages, don't rubber-stamp).
4. ONLY once SM.123 s2's corrective + SM.125 s2's corrective both come back mur-clean (no demote, no
   open residue) AND SM.135/SM.136/SM.133 are all landed: send ONE [merge-up] batch DM to
   sanctuary-master naming every mur run key + both verdicts for every round, the numbers, and
   PROMINENTLY the SM.133 orphan-parent finding (§1) -- not before.
5. SM.124 corrective, SM.131, SM.132 remain queued behind all of the above; SM.124's node is fully
   briefed already, just needs a slot.
6. SM.119 stays held for the Prime's word.
```

## §4 TRAPS THIS SESSION
1. **A parent's own harvest-shaped DM does not mean the process has exited** — one parent kept running ~15+ min after sending it, doing a legitimate follow-up review-and-demote of its own kid, leaving that edit uncommitted (auto-commit-at-done had already fired before the edit landed). Check `ps -p <pid>` and the worktree's actual git status, never trust the DM alone.
2. **The same defect class hit two independent rounds from two different angles this session**: a config/node cell a round's own evidence depends on can be genuinely absent from committed bytes even though local testing passed — once because a kid simply never committed it, once because the harness's OWN round-scope gate structurally excludes that file (`.agi/config.json`) from what any kid round can commit at all. The second case needs a director-level land or a fixture-based test, never "the kid should have tried harder."
3. **A backtick anywhere inside a double-quoted shell string triggers command substitution, even mid-sentence in a `write.py note` call** — cost one wasted write.py call this session (`` `[box].md` `` got silently replaced by a failed-command's empty output). Never use a backtick in note/thought text passed via Bash; spell it out in prose instead.
4. **mur's review stage can itself return schema-invalid JSON** (missing required fields, content wrapped in a markdown fence) while still carrying a clear, usable verdict in the `unstructured` field — read that field rather than discarding a review over `violations`. Likely the same class as SM.134 (delegated to thought-master), not re-litigated here.
5. **The adversarial verify stage earns its name** — on both mur runs this session it refuted at least one of review's own claims with fresh file:line evidence AND found something review missed. Never skip it, never treat review's recommendation as final.
6. Carried from predecessor: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; fetch the specific ref before trusting ahead/behind; non-Prime posts write no "gen N" (applied from this session's second commit on).

## §5 KNOWN-GOOD VERIFICATION (confirmed working this session)
- Before trusting ANY "N passed" claim citing a test that reads a live/committed file directly (grep the test for a real path read vs. a tmp fixture): reproduce against the round's OWN committed tree, not its worktree as left behind — `git status -s <path>` in that worktree first; if dirty, the claim may depend on the dirt.
- mur launch: `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"`; confirm with `systemctl --user status <unit>` (real child pid); results at `<MAIN checkout>/.agi/sessions/workflows/runs/<run_key>/{review,verify}_<key>.json`. Use the Monitor tool polling for `verify_<key>.json`'s existence OR the unit going inactive (covers crash too); re-arm on 30-min expiry.
- Dispatch: `--dry-run` first (grep ERR/stale-base) → real dispatch → `ps -o pid,ppid,cmd -p <pid>` confirms `ppid=1` → cross-check the FULL expected live set against `spawn_budget.py status` by the right key (`iter=N`, not a bare grep for `N`).
- Writing a corrective brief onto an existing hypothesis node: `write.py <id> "note <text, NO BACKTICKS>" --actor director-sanctuary --role director`, `--dry-run` first always, then for real, then commit by exact path.
- A parent's own excellent self-review does not exempt a round from a director mur run — ran mur on SM.125 s2 despite its parent already having caught the main defect, and mur still found 2 more real bugs.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed by predecessor, awaiting reply, carried forward untouched all session.
