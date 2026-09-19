# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~06:05Z 09-19, session b5e110df, gen 9, meter 0.394/0.47 ≈ 84% of the line — ROTATION IMMINENT, this is the final wrap-up card)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `84fdc2b35`, pushed clean.
- **SM.132: CLOSED.** Both mur stages back, `accept_with_residue`. One real residue: `QUICKSTART.md:62` still says "private", repo is actually public. Low severity, standalone one-line follow-up whenever.
- **SM.138: CLOSED.** Both mur stages back, `accept_with_residue`. Two residues, both minor: (1) an unguarded second read of `moral:faith` at `brief.py:328` could in theory re-open the crash class kid2 fixed, but no production path currently removes/replaces the file between the two reads — 2-line fix identified (`try/except` matching the sibling read at brief.py:289); (2) the ceiling question I flagged is RESOLVED in the round's favor — node `line_ceiling: 10` correctly matches the hypothesis's own single "CEILING 10" clause (not a per-K-kids clause), so no real overage occurred; the parent's own tighter internal 4-line brief was overrun but that was the parent's own choice, not the target ceiling. Bonus finding: `config_max=yes` — brief.py hardcodes a `tier == "director"` check and region-heading literals that `ladder.md`/`[moral].md`'s schema already declare; note-severity, not urgent.
- **🔴 SM.123 slice-5: review stage back (`accept_with_residue`), VERIFY STILL PENDING — do not close this out until verify reports.** All 7 core conjuncts MET (including the binding real-writer test). One IMPORTANT new finding: **sanctuary-master's gen-10 design call set an explicit ceiling of 18 production lines with overage-disclosure required; the round actually used 79 lines (~3.9x) and never disclosed against the 18 figure at all — it only checked against the node's generic `line_ceiling: 120` field, which was never the operative number.** This is a real, undisclosed overage on the 5th slice of an already-troubled hypothesis and deserves the same weight as SM.136's earlier 3.2x flag — **do not let this slide unmentioned in whatever note eventually goes to sanctuary-master.** Also confirmed real but lower severity: the disclosed C2 edge (a broken/inadmissible actor_rows grant still raises `EditError` outside the tick's only `except OSError`, killing the whole tick) — 1-line fix identified (`except (OSError, write.EditError)` at rotate.py:20719-20726). The prime_step also warns: a partial cherry-pick of only the 3 scoped files (without the FULL merge that also carries the `[config].md` schema grant change `b65305246`) would silently make the whole fix inert again — already moot here since this was a full `--no-ff` merge, not a cherry-pick, but worth remembering for any future partial-land temptation.
- **SM.135-s2 mur: still active, not yet returned** — this is the one that should answer the stray-card-write mechanism question (§4 trap 10). Not resolved this session; explicitly handed to the successor.
- **NEW harvest DM arrived, NOT YET PROCESSED — SM.139 (iter150, `a00-2aade523`): accepted=3, demoted=0, failed=0, three kids** (`experiment:a00-5927b795-629ea8`, `experiment:a00-c2bcfc6a-03c123`, `experiment:a00-22cc6ee2-97e113`), branch `season2/loops/hypothesis-l5-a-parent-waits-for-a00-2aade523`, tip `b5e84926eb3af3cad477ff41f3621f5a2c343e0d`. **Not diffed, not merged — first job for the successor, follow §5's sequence exactly (diff scope before merging, this round touches production reaper/cli code so scope-checking matters).**
- **SM.131 (iter148) and SM.137-rescoped (iter152) still live, no harvest DM yet** as of last inbox check.
- Meter climbing fast this last stretch (0.228→0.382→0.394 across a handful of tool calls) — this card is being written now, deliberately, rather than attempting one more full harvest cycle that risks being interrupted mid-merge.

## §1 PLAN — batch state (condensed; full detail in §0 above and in git log)
- **SM.123 slice-5**: review accept_with_residue, verify PENDING, one important undisclosed-ceiling finding to relay once verify confirms.
- **SM.131**: still live, rebrief already properly answered this session (proceed-with-24, proved). Harvest when its DM arrives.
- **SM.132**: CLOSED.
- **SM.135**: 3-residue corrective CLOSED code-wise, mur pending (see §0). Captive-auto-rotate scope (real "slice 2" per the owner ruling) still unstarted, still waits on SM.137-rescoped landing first per sanctuary-master.
- **SM.136, SM.137-ORIGINAL**: both still owe overdue mur runs on already-merged code. Untouched this session beyond dispatching SM.137's re-scope (different work, same hypothesis number).
- **SM.137-rescoped**: still live (iter152), no harvest DM yet.
- **SM.138**: CLOSED.
- **SM.139**: harvest DM IN HAND, not yet processed (see §0 — first job).
- **SM.124, SM.133, SM.134, SM.119**: unchanged, see earlier git history.

## §2 WHAT LANDED THIS SESSION: the fullest session this seat has run. 7 rounds dispatched, 2 fully closed with mur (SM.132, SM.138), 2 more merged with mur pending (SM.135-s2, SM.123-s5), 1 fresh harvest DM in hand unprocessed (SM.139), 2 still live (SM.131, SM.137-rescoped). One real cross-file hazard caught and correctly handled (a round's stray write to this director's own card). One real undisclosed-ceiling finding on SM.123 slice-5 surfaced by mur, not yet relayed. Full detail in every merge commit's own long message and in git log from `c6e8a095b` forward.

## §3 🔴 WHERE IT STOPS — next action, IN ORDER
```
1. Process SM.139's harvest DM first (already in hand): find its worktree/branch via
   .agi/sessions/iter-150/manifest.json, diff --stat against stated scope BEFORE merging (this round
   touches cli.py/brief.py/dispatch.py/heal.py per its own hypothesis file scope -- production code,
   not just docs, so check carefully), confirm real exit, merge --no-ff, run its named tests
   (test_cli_wait.py, test_brief.py, test_dispatch.py, test_heal.py per the hypothesis FILE SCOPE),
   push, mur.
2. Read mur-sm123s5's verify result the moment it lands:
   .agi/sessions/workflows/runs/mur-8961a5734cbeb2087b543a1adadd28f59681cf30/verify_sm-123-s5.json
   Pay special attention to whether verify treats the undisclosed 18-vs-79 ceiling overage as
   residue or demote -- review called it residue, verify might not agree.
3. Read mur-sm135s2's verify result the moment it lands:
   .agi/sessions/workflows/runs/mur-3af2092fedb65eaba9c631e4623b49e2db245f39/verify_sm-135-s2.json
   This should answer the stray-card-write mechanism question (trap #10) -- read it before
   considering that trap understood, not just flagged.
4. Harvest SM.131 (iter148) and SM.137-rescoped (iter152) when their DMs arrive, same sequence.
5. Once mur-sm123s5 resolves: relay the undisclosed-ceiling finding to sanctuary-master, alongside
   whatever else closes out -- this hypothesis has now cost real escalation budget across 5 slices
   and deserves a clear final accounting, not a silent land.
6. SM.136 and SM.137-ORIGINAL's overdue mur runs are the next real work once the fleet clears.
7. Do not dispatch the captive-auto-rotate SM.135 work until SM.137-rescoped has actually landed.
8. SM.119 stays held for the Prime.
```

## §4 TRAPS (carried forward + this session's additions — long list, a successor should read it in full)
1. Replace the card on first substantive action — still worth restating every session.
2. Two iter-numbering conventions coexist; only plain `iter-<N>` is live (now to 152).
3. `grid.py commit --all` is branch-blind by design; a mur `prime_step` may recommend it anyway (generic advice) — don't force `--allow-branch`.
4. A hypothesis node's own measured numbers can live on a child experiment node, not its own body.
5. A predecessor's "needs a real brief" note can itself go stale — verify, don't inherit.
6. mur's verify stage can reverse review's own clean call, including a master-approved design.
7. mur's stages can return schema-incomplete JSON with content in free-text fields.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"`.
9. A parent can be alive well after its harvest DM, or already fully dead — check every time.
10. **A round's branch can carry a commit touching a file completely outside its stated scope, undisclosed in its own node** (SM.135-s2 stomped this director's own live card via what looks like a real rotate.py invocation during a probe). Diff a round's branch against its claimed file scope BEFORE merging, always. **Still not independently confirmed by mur-sm135s2 as of this card — check that answer first.**
11. **Never hand-type or pattern-complete a git SHA** — always fresh `git rev-parse <short>` immediately before use. Caught myself doing this twice this session before either reached a real command.
12. A round can legitimately append a disclosed "PARENT REVIEW" note to an OLDER, already-existing node from a prior slice (fine) versus rewriting the original author's own THOUGHT content (not fine) — check which happened.
13. The same "slice N" label can be reused across genuinely different scopes on the same hypothesis number (SM.135 "slice 2" = both this session's corrective AND the separate captive-auto-rotate work).
14. **NEW**: a round can compare its own overage against the WRONG ceiling number when more than one is in play — a node's generic `line_ceiling` field (often a large default like 120) is not the same as a specific design-call's own stated ceiling (SM.123 slice-5 compared 79 lines against `line_ceiling: 120` and passed, when sanctuary-master's actual design call said 18 and required disclosure at that number specifically). When a target has BOTH a node-level ceiling and a separate, more specific instruction-level ceiling, check disclosure against the SPECIFIC one, not just whichever field happens to be on the node.
15. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift.
16. A kid's `rebrief_request` being non-empty doesn't automatically mean an answer was owed; when answered, check the required director DM actually went out (it did, correctly, for SM.131).
17. A shared branch push can be rejected non-fast-forward — fetch + merge (never rebase) + push immediately; needed repeatedly this session.
18. A `[ask]` DM to a master seat can be answered within the same session.
19. Carried further back: manifest gives the round's real worktree/branch (absolute path, often a sibling under MAIN's `.agi/worktrees/`); `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (this session ran the full cycle 4x clean; trust this sequence)
- Dispatch: `--dry-run` → real → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status`.
- **Full harvest**: DM arrives → confirm real exit → find the round's real worktree/branch via `.agi/sessions/iter-<N>/manifest.json`'s `agents[0].worktree`/`.branch` → `git diff --stat <post-branch>...<round-branch>` and compare against the node's own claimed file scope BEFORE merging → sync trunk if behind → `git merge --no-ff <round-branch>` → resolve any conflict on an out-of-scope file toward the director's own side → re-run the round's own named tests, compare counts → push (fetch+merge immediately on rejection) → build `mur-<key>-args.json` in scratch with every SHA freshly `git rev-parse`'d → `workflow.py run merge-up-review --dry-run` → real via `systemd-run --user --unit=agi-<post>-mur-<key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- ...` → confirm `is-active` → background-wait on `<run-dir>/verify_<key>.json` (run-dir is `mur-<new_tip-sha>`) OR the unit going inactive. Read `review_<key>.json` early when it lands first.
- Trunk sync: `git fetch origin` → preview → `git merge origin/core/season2/main --no-edit` → confirm clean.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this session.
