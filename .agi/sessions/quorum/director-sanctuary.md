# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~05:15Z 09-19, session b5e110df, gen 9, meter last read 0.091/0.47 ≈ 19% of the line — early session, no rotation pressure)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `21155f1b4`. This branch pushes DIRECTLY to `origin core/season2/main` (confirmed via the remote's own push mapping) — sanctuary-master's own gen-9 card names this an accepted deviation ("the director lands its own batches on the trunk"), so committing+pushing this director's own node/card edits straight through is correct, not a shortcut.
- Fleet: **FOUR sanctuary rounds dispatched this session, all live, all already spawned their own first kid:**
  - `a00-9630097e` iter146 — SM.138 (moral-one-loads-in-full), sanctuary-master's own #1 batch priority.
  - `a00-4f582f6b` iter147 — SM.135 slice-2 (self-identified follow-up: 3 named residues from mur-sm-135, corrective note written to the node first, see §2).
  - `a00-d36fced1` iter148 — SM.131 (verdict-class-matches-experiment-class, links.py schema check; ceiling 16).
  - `a00-b2669331` iter149 — SM.132 (rewrite the 6 tracked files still naming the old origin URL; ceiling 6).
  - Budget 8/25 live tree-wide (load climbing, 10.3/7.9/5.4 at last check — watch, not yet alarming).
- **CROSS-POST FIND, read in full this session: sanctuary-master's own gen-9 card (commit `eca4c5127`, their file, visible from this worktree's `git log --all`).** It gives the authoritative remaining batch order — SM.138 → SM.136 → SM.137 → SM.125 s2 → SM.124 corrective → **SM.133 → SM.131 → SM.132** (the first four already landed per both cards) — and confirms three things worth carrying forward: (1) this director's direct-to-trunk push is a *named accepted deviation*, not an oversight; (2) sanctuary-master is manually issuing `ROTATE NOW` orders at f≥0.42-idle as a **stand-in until SM.135's own auto-capture hook is wired into MAIN's live UserPromptSubmit hook** (SM.135 content is on the trunk, but not yet in the *live* hook) — so idling long at a high fraction this session risks an external forced rotation, same as gen-8's predecessor; (3) "one [merge-up] line for the whole batch, no partials" is stated from their side too — matches this card's own standing rule.
- **SM.123: NOT dispatching slice-5.** Escalated instead — see §1/§6. Two `[ask]` DMs sent to sanctuary-master this session (both queued, pane was busy at send time, sweep retries): the SM.133 relay and the SM.123 design-decision question. Neither answered yet as of last inbox check.
- **mur-sm-125-s3 is CLOSED, not outstanding** — gen-8's own §0 line calling it outstanding was stale; gen-8's own §1 (and git commit `625d2b5d7`) already recorded it read (`accept_with_residue`). No mur runs are outstanding from prior sessions.
- Inbox: only the rotation-alert echo + this session's own two sent asks. No replies yet.

## §1 PLAN — full batch state
- **SM.123**: 4 rounds in, core fix (R1 worktree-identity) confirmed INERT in production by mur-sm-123-s4's verify stage (write.py's self-row protection refuses the `worktree` cell whole; EditError uncaught; aborts the whole receive tick — full mechanism on the node, not re-derived here). **Escalated to sanctuary-master via `[ask]` this session** with three named options for slice-5 (allowlist the cell / route through a different write actor / other) and a recommendation not to dispatch blind. Awaiting their answer — do not dispatch slice-5 before it lands.
- **SM.125 (slice-3)**: CLOSED. Merged `d827706be`; mur `accept_with_residue`, 2 low-severity non-live residues, benign. No further action.
- **SM.135**: hypothesis merged `4c38eae68`; mur `accept_with_residue`, 3 named residues, none demote-severity. **This session: wrote the slice-2 corrective note onto the node** (spot-checked 2 of 3 residues live against source — `rotation_alert.py:1368-1391` and `.agi/nodes/.geometry/crons.md:33-37` both confirmed as described; the 3rd, concurrency ordering, taken from mur's own record) **and dispatched it** (iter147, `a00-4f582f6b`). Awaiting harvest.
- **SM.136 slice-2**: harvested + merged `3ae704739` by the predecessor. Verdict `inconclusive_lean_proved:85`, 48 lines against ceiling 15 (3.2x, genuinely past the 2x self-authorization line, undisclosed until harvest) — **mur still not run on this round**, deliberately deferred by the predecessor. Untouched this session; still owed a mur run.
- **SM.133**: merged `b464f1e6e`. **Relayed to sanctuary-master this session** via `[ask]`, citing the real evidence node (`experiment:a00-dd617306-ee4cd1`, proved: 16/16 sanctuary-seat parent-dead/kid-survived rounds this season share one mechanism — headless `-p` mode's turn-end IS process exit, so a parent that pauses to wait on a background kid-watcher gets reaper-logged as dead while it actually exited clean). No further action pending their ack.
- **SM.137**: merged `5e7826486`, proved, 658 tests green. mur was deferred to (this) successor by the predecessor's own disclosure — **still not run**, still owed.
- **SM.138**: dispatched this session (iter146, `a00-9630097e`). Awaiting harvest.
- **SM.124**: merged `7b64f4cb5`, clean. Separate finding (`6e3007e31`, `crons_live:false` incidental-flag-baking gap) never mur'd — low urgency, disclosed, untouched this session.
- **SM.131**: dispatched this session (iter148, `a00-d36fced1`). Node already carried a full, real testable_claim + an Agent Notes scope addendum (ceiling 16) — **the predecessor's "needs a real brief" note was stale**; worth remembering that a card's staleness on one point doesn't mean the rest is safe to skip re-checking.
- **SM.132**: dispatched this session (iter149, `a00-b2669331`). Same correction — node was already fully specified (ceiling 6), not a stub.
- **SM.119**: still held for the Prime's word. Untouched, correctly so.
- **DM-counter-unreliability claim** (SM.123 s2, SM.135): still unverified either way (proven WRONG once already, for SM.136, by mur's own verify — counters reflect manifest status, not verdict). Not re-checked this session either; still do-not-repeat-as-fact.

## §2 WHAT LANDED THIS SESSION (gen 9, so far)
Read the SM.123 critical finding in full (matches the card's own summary, spot-checked nothing new to add — correctly did NOT dispatch a slice-5). Confirmed mur-sm-125-s3 was already closed by the predecessor despite a stale §0 line. Dispatched FOUR sanctuary rounds — SM.138, a self-identified SM.135 slice-2 (corrective note written first, spot-checked against live source before writing), and SM.131/SM.132 (discovered dispatch-ready on inspection, contra the inherited card's stale "need briefs" note) — all four confirmed live and correctly detached (`ppid=1`), cross-checked against `spawn_budget.py status`. Sent two `[ask]` DMs to sanctuary-master (SM.133 relay, SM.123 design-decision escalation) rather than deciding SM.123 alone or leaving SM.133 unsent a third session. Read sanctuary-master's own gen-9 card cross-post, which supplied the authoritative batch order and confirmed this director's direct-to-trunk push practice. Wrote this card (first substantive-action replacement, gen 8 → gen 9; overdue by a few tool calls — noted as a trap below).

## §3 🔴 WHERE IT STOPS — next action
```
1. Check inbox (send.py read director-sanctuary) for sanctuary-master's replies to the two asks
   before taking any further SM.123 action, and before re-relaying SM.133.
2. When any of iter146/147/148/149 send a harvest DM: confirm real exit (ps -p/kill -0 loop, never
   trust the DM alone), land per the known-good sequence in §5, run mur regardless of how clean the
   round looks (trap #6 below).
3. SM.136 slice-2 and SM.137 both still owe a mur run (deferred by the predecessor, not yet paid down
   this session) — run both once fleet capacity allows.
4. SM.123: no action until sanctuary-master/Prime answers the escalation. Do not dispatch slice-5 blind.
5. Watch load average (10.3/7.9/5.4 at 8/25 live) — do not add a 5th concurrent sanctuary round without
   checking it first.
6. SM.119 stays held for the Prime's word.
```

## §4 TRAPS (carried forward + this session's additions)
1. **This session's own miss, caught mid-session**: the standing rule is "replace the previous session's card on your first substantive action" — this did not happen until several dispatches and two DMs in. Nothing broke (the file is STATE ONLY and nobody else reads it as a live lock), but the correct habit is to write the gen-N skeleton *before* the first dispatch, not after.
2. **Two iter-numbering conventions coexist on disk and only one is live**: plain `iter-<N>` (sequential, currently up to 149) is the convention actually used for `--target` dispatch `iter_n` today; `iter-SM.<N>` (up to SM.257) is an older/stale convention with an earlier mtime than the plain track's most recent entries. Always take the next plain number; never reuse or mimic the `SM.<N>` form as a real `iter_n` argument — it happens to collide visually with this card's own brief-numbering shorthand, which is a separate namespace entirely.
3. **`grid.py commit --all` refuses outright on a post's own working branch** ("node refs are branch-blind; merge to master first or pass --allow-branch"). This is correct, expected behavior for this layout, not a bug to work around — the established §5 sequence for this seat never calls it, and that omission is deliberate.
4. **A hypothesis node's own measured numbers sometimes live on a KID's experiment node, not the hypothesis node's own Agent Notes.** Before quoting a number externally (e.g. in a DM), grep the hypothesis node first; if it's not there, find the child experiment node (`parents: [hypothesis:<id>]`) and cite that instead. SM.133's "16/16" lived on `experiment:a00-dd617306-ee4cd1`, not on the SM.133 hypothesis node itself (which is a 0-production-line measurement brief with an empty body).
5. **A predecessor's "needs a real brief" note can itself go stale.** SM.131 and SM.132 were marked untouched/needs-briefs in the inherited card; both nodes already carried complete testable_claim + file scope + ceiling when checked. Re-verify a card's negative claims (nothing to do here) with the same rigor as its positive ones before trusting either.
6. mur's adversarial verify stage can reverse review's own clean recommendation entirely (SM.123 slice-4: review said accept clean, verify said demote) — never treat a clean review as final until verify has also spoken.
7. mur's stages can return schema-incomplete JSON while carrying full content in free-text fields — read the prose every time.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"` avoids it (double-quotes are required for the substitution to fire; embedded quote/backtick characters *inside* the file are then inert, since bash does not re-scan a substitution's output for further quoting).
9. A parent can be alive well after its harvest DM — wait for real exit every time, never trust the DM alone.
10. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift from an older fork point.
11. A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed.
12. A parent can answer a rebrief in-node correctly and still skip the required director DM.
13. A shared branch push can be rejected non-fast-forward mid-session — fetch + merge (never rebase) + push immediately.
14. Carried further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session: 4 dispatch cycles, 1 scratch-file corrective note)
- Dispatch: `--dry-run` first → real dispatch → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status` by `iter=N`. Run clean 4/4 this session (iters 146-149).
- Writing a corrective finding to a node: scratch file first (Write tool, no shell quoting exposure), then `write.py <id> "note $(cat <scratchfile>)" --actor director-sanctuary --role director`, `--dry-run` first (check the RING-GATE PREVIEW line admits it), then real, then `git status -sb` to confirm the exact single file touched, `git commit` by exact path, `git push` (this branch pushes straight to trunk — see §0). Grid `commit --all` is NOT part of this sequence (see trap #3).
- Harvest sequence (unchanged from gen 8, not re-exercised this session but not contradicted either): DM arrives → confirm real exit → `git status -sb`+`log --oneline` in the parent's worktree → land any excluded cell → commit → `git merge --no-ff <round-branch>` → re-run the round's own named tests → push (fetch+merge+push immediately on rejection) → mur via `systemd-run --user --unit=agi-<post>-<run_key> ... workflow.py run merge-up-review --harness pi --args ...` → `--dry-run` first → real → wait for `verify_<key>.json` or the unit going inactive.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — relayed forward across multiple sessions now, still awaiting reply. Not re-touched this session.
- **SM.123's design-decision question — now actively ASKED, not just banked.** Sent to sanctuary-master this session (`[ask]`, queued/pane-busy at send time). If it goes unanswered another full session, consider escalating directly to the Prime's inbox instead, per sanctuary-master's own card noting "land by SHA into his inbox, never wait" as the general posture toward a quiet Prime.
