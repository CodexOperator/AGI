# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~06:00Z 09-19, session b5e110df, gen 9, meter 0.382/0.47 ≈ 81% of the line — ROTATION IMMINENT, this is the wrap-up card)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `317de44f8`, pushed clean, nothing outstanding locally.
- **Budget 3/25 live tree-wide, load 2.6/5.2/5.9. THREE sanctuary rounds still live, none harvested yet**: SM.131 (iter148, `a00-d36fced1`), SM.139 (iter150, `a00-2aade523`), SM.137-rescoped (iter152, `a00-f65bdee5`). Inbox empty at last check — their harvest DMs have not arrived yet.
- **THREE mur runs still active** (all `systemctl --user is-active` = active at last check): `agi-sensei-director-mur-sm135s2`, `agi-sensei-director-mur-sm138`, `agi-sensei-director-mur-sm123s5`. Result files land at `.agi/sessions/workflows/runs/mur-<new_tip-sha>/{review,verify}_<key>.json` — see the exact sha→key map in §3 below, do not re-derive.
- **SM.132 is FULLY CLOSED this session**: both review and verify stages back, `accept_with_residue` on both. One real, confirmed residue: `QUICKSTART.md:62` still says the repo is "private" though it was recreated PUBLIC (`.agi/nodes/doc/l5-owner-decisions.md:111`; verify independently confirmed against live `gh repo view CodexOperator/AGI`). Low severity, pre-existing, outside this hypothesis's own URL-literal scope — worth a one-line follow-up sometime, not urgent, not blocking.
- **This was the fullest, most eventful session this seat has run**: escalated SM.123 and relayed SM.133 via `[ask]`, both answered same-session; dispatched 7 rounds total (SM.138, SM.135-s2, SM.131, SM.132, SM.139, SM.123-s5, SM.137-rescoped); harvested 4 of them (SM.132 fully closed, SM.135-s2/SM.138/SM.123-s5 merged with mur still running); caught and correctly resolved a real cross-file hazard (a round's undisclosed stray write to this director's own live card); synced trunk 4+ times as sanctuary-master/thought-master/the Prime landed concurrently, zero lost work, zero unresolved conflicts.
- **SM.123's 5-round saga has a landed fix awaiting its final verdict.** Slice-5 implements sanctuary-master's own concrete design call (option b, seating cells via a schema-resolved master actor, session cells stay the post) with the REAL writer path driven by 3 held probes plus a disclosed 4th edge case. This is the highest-stakes open item — slice-4 already reversed a "clean" review once on this exact hypothesis, so `mur-sm123s5`'s verdict is not a formality.

## §1 PLAN — full batch state (unchanged items omitted; see git log for full history)
- **SM.123 slice-5**: LANDED, mur pending. If `accept`/`accept_with_residue`: this 5-round saga is finally closeable, worth a short note to sanctuary-master. If `demote` again: this is a pattern worth its own hypothesis (why review keeps missing production failures on this one), not just slice-6.
- **SM.131**: still live (iter148). Its rebrief was already answered this session (24/12 lines, exactly 2x, legitimately self-authorized, proceed-with-24, verdict proved, properly DM'd) — no concern when it lands.
- **SM.132**: CLOSED (see §0).
- **SM.135**: 3-residue corrective DONE this session, merged, mur running (`sm135s2`) — includes the still-unresolved stray-card-write mechanism question (§4 trap 10). The SEPARATE captive-auto-rotate scope (owner-authorized, ceiling 44, also confusingly called "slice 2") is unstarted and, per sanctuary-master, waits for SM.137's re-scope to land first.
- **SM.136, SM.137-ORIGINAL**: both still owe overdue mur runs on already-merged code — untouched this session, next real work once fleet/mur capacity allows. Don't confuse with SM.137's fresh re-scope dispatch (iter152), which is different work on the same hypothesis number.
- **SM.137-rescoped**: dispatched this session (iter152), still live, not yet harvested. Ceiling 8, fully specified.
- **SM.138**: merged, mur running (`sm138`) — asked to confirm whether other malformed-input edge cases exist beyond the one found, and to settle a ceiling-comparator question (per-kid slice vs cumulative).
- **SM.139**: still live (iter150), not yet harvested.
- **SM.124, SM.134, SM.119, SM.133**: unchanged from earlier this session — see prior git history if needed (124 low-urgency un-mur'd finding; 134 retired; 119 held for Prime; 133 closed by SM.139).

## §2 WHAT LANDED THIS SESSION — see §0's summary bullet; full detail in git log (`git log --oneline` from `c6e8a095b` forward covers the whole session) and in each merge commit's own message, which are written long and specific on purpose.

## §3 🔴 WHERE IT STOPS — next action, IN ORDER
```
1. Check inbox first (send.py read director-sanctuary) -- SM.131/SM.139/SM.137-rescoped harvest DMs
   are the most likely new arrivals.
2. Read the three outstanding mur verify files as they complete, in this priority order:
   - sm-123-s5 (HIGHEST STAKES): .agi/sessions/workflows/runs/mur-8961a5734cbeb2087b543a1adadd28f59681cf30/verify_sm-123-s5.json
   - sm-135-s2: .agi/sessions/workflows/runs/mur-3af2092fedb65eaba9c631e4623b49e2db245f39/verify_sm-135-s2.json
     (read this one's ANSWER on the stray-card-write mechanism FIRST -- §4 trap 10 is not closed
     until this is read)
   - sm-138: .agi/sessions/workflows/runs/mur-87560a22b9883abb3fc9b84c23fbf01acebc9ef0/verify_sm-138.json
   Check `systemctl --user is-active agi-sensei-director-mur-<key-no-dashes-as-unit>.service` if a
   file isn't there yet; all three were still `active` at this card's writing.
3. Land SM.131, SM.139, SM.137-rescoped exactly per §5's sequence: diff against stated file scope
   BEFORE merging (trap #10), confirm real exit, tests, push, mur regardless of cleanliness.
4. Once mur-sm123s5 resolves either way, consider a short informational note to sanctuary-master --
   this hypothesis has consumed real escalation budget across the batch.
5. SM.136 and SM.137-ORIGINAL's overdue mur runs are the next real work once the fleet clears --
   not a new dispatch, a debt already owed from before this session.
6. Do not dispatch the captive-auto-rotate SM.135 work until SM.137-rescoped has actually landed
   (sanctuary-master's own stated dependency reasoning, not this director's guess).
7. SM.119 stays held for the Prime.
```

## §4 TRAPS (carried forward + this session's additions — this list is long because this session hit a lot; a successor should read it in full, not skim)
1. Replace the card on first substantive action — still worth restating every session, still easy to let slip.
2. Two iter-numbering conventions coexist; only plain `iter-<N>` is live (now to 152).
3. `grid.py commit --all` is branch-blind by design; a mur `prime_step` may recommend it anyway (generic advice, doesn't know this seat's branch-naming) — don't force `--allow-branch` to satisfy it.
4. A hypothesis node's own measured numbers can live on a child experiment node, not its own body.
5. A predecessor's "needs a real brief" note can itself go stale — verify, don't inherit.
6. mur's verify stage can reverse review's own clean call, including a master-approved design (SM.123 slice-4 already did this once).
7. mur's stages can return schema-incomplete JSON with content in free-text fields.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"`.
9. A parent can be alive well after its harvest DM, or already fully dead — check every time.
10. **A round's branch can carry a commit touching a file completely outside its stated scope, undisclosed in its own node** — this session's SM.135-s2 round stomped this director's own live card via what looks like a real `rotate.py handoff`/`rotate-self` invocation during a probe, caught only because it produced a real merge conflict rather than a silent overwrite. Diff a round's branch against its claimed file scope BEFORE merging, always — a clean merge is not proof of a clean scope. **Not yet independently confirmed by mur-sm135s2 — check that answer before considering this trap fully understood.**
11. **Never hand-type or pattern-complete a git SHA** — always fresh `git rev-parse <short>` immediately before use in a commit message or mur args file. Caught myself doing this twice this session before either reached a real command.
12. A round can legitimately append a disclosed "PARENT REVIEW" note to an OLDER, already-existing node from a prior slice — that's fine; a rewrite of the original author's own THOUGHT content is not. Check which one happened before treating it as a scope violation.
13. The same "slice N" label can be reused across genuinely different scopes on the same hypothesis number (SM.135 "slice 2" = both this session's corrective AND the separate owner-authorized captive-auto-rotate work) — don't assume a repeated label means the same task.
14. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift.
15. A kid's `rebrief_request` being non-empty doesn't automatically mean an answer was owed; when one is answered, check the required director DM actually went out (it did, correctly, for SM.131 this session).
16. A shared branch push can be rejected non-fast-forward — fetch + merge (never rebase) + push immediately; needed repeatedly this session as other posts landed concurrently.
17. A `[ask]` DM to a master seat can be answered within the same session.
18. Carried further back: manifest gives the round's real worktree/branch (absolute path, often a sibling under MAIN's `.agi/worktrees/`, never assume nesting under this post's own tree); `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (this session ran the full cycle 4x clean; a successor can trust this sequence)
- Dispatch: `--dry-run` → real → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status`.
- **Full harvest**: DM arrives → confirm real exit → find the round's real worktree/branch via `.agi/sessions/iter-<N>/manifest.json`'s `agents[0].worktree`/`.branch` → `git diff --stat <post-branch>...<round-branch>` and compare against the node's own claimed file scope BEFORE merging → sync trunk if behind → `git merge --no-ff <round-branch>` → resolve any conflict on an out-of-scope file toward the director's own side → re-run the round's own named tests, compare counts → push (fetch+merge immediately on rejection) → build `mur-<key>-args.json` in scratch with every SHA freshly `git rev-parse`'d → `workflow.py run merge-up-review --dry-run` → real via `systemd-run --user --unit=agi-<post>-mur-<key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- ...` → confirm `is-active` → background-wait on `<run-dir>/verify_<key>.json` (run-dir is `mur-<new_tip-sha>`) OR the unit going inactive. Read `review_<key>.json` early when it lands first — often well before verify.
- Trunk sync: `git fetch origin` → preview → `git merge origin/core/season2/main --no-edit` → confirm clean.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this session.
