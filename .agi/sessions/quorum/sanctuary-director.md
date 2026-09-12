# SESSION HANDOFF — 2026-09-12 sanctuary-director: LIVE SCRATCHPAD (written by the 043918Z session — record `sanctuary-director.20260912T043918Z.json`, ref `7ae713`, window @315, gen 20, 04:39Z–; the successor replaces this wholesale AS IT WORKS)

🔴 **IF THE PRIME HAS RUN THE LIVE RENAMES** (`cli.py post-rename --apply`, `branch-reshuffle --apply --kinds main,posts,towns` — its last steps after mur-44): your worktree is `.agi/worktrees/post-sanctuary-director` on `season2/posts/sanctuary-director`, MAIN on `season2/main`, rows in `config:posts`, spellings `--post`/`AGI_POST`; every `seat/…@s2` / `origin/season/s2` below then reads through the one-season alias (readers accept both). **Not run as of 04:43Z** — `git branch --show-current` = `seat/sanctuary-director@s2`; the alias layer IS live (`branches.py: deprecated alias used: season/s2 -> season2/main`, whois verifies against `origin/season2/main`).

**OWNER: no generations in prose/dms/commits — name a session by its rotation-record stamp · this post touches only its own tracking, in this file · "wrap up this loop soon" · seat → POST in prose · doc trim pass.** Owner verbatim lives in `doc:l4-owner-decisions`, never here.

## §0 STATE (stamped 04:43Z)

```
WAKE (measured 04:43Z, 7 calls)                                  ROUND (each L4.NNN)                        CLOSE
ListAgents ──► rotate.py ack --seat sanctuary-director --gen N   claim_append ──► commit+push ──► dispatch   ONE line to the Prime = numbers only
   --ref <bare> continue  (worked FIRST TRY: SL5.01 landed —     status --iter --wait 540 ──► review BYTES
   spawn row pre-committed 7bca4a9d6; ack commits ITS row IN     merge round branch ──► run on the REAL
   MAIN and prints the push line: git -C /home/ubuntu/work/agi push)   tree ──► note.py harvest ──► commit+push
   ▼
ONE send.py read sanctuary-director (every seam) ──► IDLE unless necessary
```

- **PRIME = XIV `agi-37 [92eda4]` @314 busy** (whois IS-AUTHORIZED 04:39Z). Its last steps: mur-44 by name → `post-rename --apply` → `branch-reshuffle --apply --kinds main,posts,towns` → `--delete-old` after a green stamp → the season CLOSE. **Owner's cut-off is MET on this post's side** (A-G, H, I landed in mur-44 `14cd8fb29`, 11/11, 3733/14, stamp 2373/195/2568). **Rail: openrouter only** (owner 01:31Z), pi for every parent/kid; a 403 = one line to the Prime and stop. Pin-reap STAYS NOT ARMED. Merge-up window is STATE (`test -f .agi/sessions/verify-suite.lock` in MAIN + inbox before ANY MAIN merge). A role is RESOLVED, never typed.
- **Peers at 04:43Z:** sensei-director `seat-sensei-director-88 [0a14a7]` @313 → **rotating 04:56Z to @316** (alert seq 49; successor ref = its ack row in MAIN, `send.py whois <ref> --claim sensei-director`, never by name; owns rotate.py spawn/first_turn/bootstrap/handoff/ack + SL7.04). master-sensei `agi-88 [516457]` @292 not in ListAgents at 04:39Z (agi-1b/-14/-f8/-b3/-31 present; resolve by whois, never by name). Helper `seat-sanctuary-helper-88 [5f209b]` @307 idle (L4.257-259 rode mur-42). Predecessor `seat-sanctuary-director-34 [27c314]` @308 still busy at 04:40Z — its self-reap is proved by the record's `s12_self_reap`, one `rotate.py status --seat sanctuary-director --record latest` later, never ps/tmux.
- **Tree:** MAIN `season/s2` tip `3d4e2521c` (my ack, pushed 04:40Z) over `7bca4a9d6` (spawn row) over `e93422726`. Seat tip `b2e7eaf25` = origin seat; seat is behind origin/season/s2 by the two row commits + ack (rows only; merge before rotate-self per F14). MAIN carries live uncommitted dirt NOT mine: `goal/g17.1.md` + `GOALS.md` (someone's render mid-write) and the seats.md trailer hunk (§4). A pytest subset (`timeout 590 … test_send test_seatsig test_sensei test_heal …`) was running from MAIN at 04:41Z — a sibling's rotation-level verification, not the suite lock (absent).
- **Free ids: L4.308+.** UNIT: reaper `heal.py watch` from MAIN (restarted 19:56Z; heal.py changes since are dead in the live watcher until the Prime restarts it).
- **Helpers in `$S`** (`/tmp/claude-1001/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<session-id>/scratchpad`, die with the session): none written this session yet — `note.py <node> <file>` · `mint.py <spec.json>` · `claim_append.py <node> <file>` are ~12 lines each over write.py (Edit/create + submit, actor sanctuary-director role director); rewrite on first need.

## §1 LANDED THIS SESSION (04:39Z–)

- Wake 04:39Z: ListAgents → ack `3d4e2521c` (first try) → push → inbox empty. 7 calls.
- **Finding → sensei-director dm 04:4xZ, already known:** `rotate.py ack` leaves MAIN's `seats.md` dirty (trailer newline; `_seats_ownrow_content` rotate.py:5342 commits `join + "\n"`, the row writer drops the EOF 0a). **Fix = SL7.04 at the WRITER** (`_serialize_node` in node_writer: every node write ends with exactly one 0a; ack gate + prepare check read a whitespace-only delta as clean; harvested on the sensei-director's seat 04:17Z, lands at SL2#14). Not mine to touch (master-sensei 04:41Z). 3 calls spent characterising it — the master-sensei's note: read the sibling's pending fixes before deriving a MAIN-dirt mechanism by hand.
- 04:44Z inbox: helper standing by (rotation 8, 5f209b @307, next id L4.260, cuts nothing under CLOSE-SOON); master-sensei + sensei-director on the newline residue (above). No replies owed.

## §2 LIVE + QUEUE (stamped 05:23Z)

**mur-44 verdict (Prime 05:15Z, inbox file ts 05:15:17): L4.304/305/306 ACCEPT with residue; L4.307 DEMOTE (grid guard reopened). LIVE RENAMES HELD by the Prime until the rounds below land + mur-45 by name. The Prime keeps the loop open for exactly these.**

- **L4.311 LANDED 05:33Z** (seat merge 068ff0e1b; harvest note on the (1) node; 161 passed; verify 9/10 with bin-suite-fresh red on the merits; 2572 nodes). Parent `done` COMMITTED on `season2/loops/*` (e61898e0d) = (a) claim (3) proved live, recorded on (a).
- **LIVE (cut 05:32Z from seat tip 17b8ba9a1, behind 0):** L4.312 = I round 2, parent `a00-325f2fa0` pid 1720065 · L4.313 = (a), parent `a00-4aba4f92` pid 1720565 · L4.314 = (b), parent `a00-c4ab3885` pid 1721178 — all pi/deepseek-v4.1-flash on `season2/loops/<slug>-<agent>`. Wait: `python3 extensions/agi/bin/spawn_budget.py status --iter L4.312 --wait` (then 313, 314). First cut refused stale-base (behind 40: the Prime pushed SL2#14 ~05:30Z) — rmdir'd the empty dirs, merged, re-cut the SAME ids.
- **QUEUED, in this order (minted/appended, committed):** after L4.311 harvests → in PARALLEL (disjoint files): I round 2 (`hypothesis:l4-branches-follow-the-season-grammar`, claim tail "FIX-ONLY ROUND 2", 4 kids by region: cli.py branch-reshuffle / dispatch.py:382 / rotate.py first-decision+harvest-table / verification.py+ladder.md+crons runbook) + (a) `hypothesis:l4-a-parent-done-commits-on-every-grammar` (tests only unless a refusal is real) + (b) `hypothesis:l4-whois-names-the-ref-it-read` (send.py whois print). Then H round 2 (`hypothesis:l4-a-seat-is-a-post-everywhere`, "FIX-ONLY ROUND 2", 4 kids: cli.py post-rename / --seat notice shared / sensei wake-audit reader / cc-session-start.next.sh) — AFTER I lands (cli.py + dispatch.py shared; I owns the seat-branch target). Then merge-up 45 (ONE message; suite window one at a time), then the Prime runs mur-45 by name.
- **Rungs 2-4** (`l4-a-ring-decision-carries-m-of-n-signatures`, `l4-a-veto-freezes-never-frees`, `l4-an-untrusted-lane-earns-tier-by-signed-verdicts`) already minted + HELD — the Prime's "mint rungs 2-4 now" is met; dispatch after the flip per the plan, when the Prime says GO.
- Ids: L4.308-310 are EMPTY untracked dirs in MAIN's sessions (01:37Z/04:01Z/05:15:43Z — not mine; someone's refused cuts) — skipped, not reused. **Next free: L4.312+.** Dispatch shape: `AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target <node> --level small --tier parent --harness pi --branch`.
- NEXT SEASON (on their nodes): L4.291 residue · rotation-record argv cap · pin-reap round 2 (Prime's C) · helper's `l4-heal-reads-the-freshest-seat-row` · P2 residues L4.296/294/301/303 · L4.304 kid-3 patch (delete with the worktree) · 26 junk crash-recovery records.

## §3 🔴 NEXT COMMAND (stamped 05:23Z)

**Wait on L4.312/313/314 (`spawn_budget.py status --iter L4.NNN --wait`, one per round) → harvest each per §4 (kid worktrees; parent `done` should now COMMIT on `season2/loops/*` — that commit hash is (a)'s live proof, record it on (a)) → merge the round branch into the seat → real-tree check: from the parent worktree `grid.py commit --all` must exit 2 naming its branch → `commands.py run verify` → note.py harvest on the (1) node → commit+push → then H round 2 (L4.315) → merge-up 45 (ONE message to the Prime; suite window one at a time).**

## §4 TRAPS (the ones that bit; older ones live in the nodes they came from)

- 🔴 **MAIN's `seats.md` reads `M` after every ack** — the trailer-line newline hunk (§1), NOT a row mid-edit. Leave it; never `git checkout -- seats.md` in MAIN (erases identity cells). `cut` is shadowed on this box (bit me 04:41Z — use awk substr).
- 🔴 **A parent may run its kids in THEIR OWN worktrees** (`.agi/worktrees/<kid>`, branch `season2/loops/…-<kid>`) and its `done` carries only its own scratch (L4.307) — at harvest check every kid id for a worktree, commit under the kid's authorship, merge the kid branches, `git rm` any `.agi/tmp/*` the parent staged. Kids may leave work staged-uncommitted; kids may make unrelated global edits — diff the deletions.
- 🔴 **Dispatch emits loop branches in the new grammar (`season2/loops/<slug>-<agent>`) but the pre-commit hook lets a parent commit only on `loop/*`** — a parent `done:` may be REFUSED and the round left STAGED in its worktree. Harvest = `git -C .agi/worktrees/<parent> add -A .agi/nodes` + commit with `-c user.name=<id> -c user.email=<id>@agi.local`, then merge. L4.305's guard patch landed with I (mur-44) — verify on the first real round before trusting it. Branch: `git branch --list '*<agent>*'`.
- 🔴 **A kid can consume YOUR inbox** — the inbox FILE `.agi/sessions/inbox/sanctuary-director.md` is the record: `grep -n '^ts: ' | tail` and `awk '/<ts>/{f=1} f'` when a read looks thin; never `| head` a read. An mtime loop misses a dm in the SAME SECOND — compare size too (`stat -c '%Y %s'`).
- 🔴 **A merge-up window GRANT is state** — `test -f` the lock (never `ls … | grep -c`) + `ps -p <pid>` + inbox before `git merge` in MAIN; undo with `git reset --soft <base>` + per-file restore, never `reset --hard` (MAIN's comms/rotations carry live uncommitted messages). The `:07` branch_push cron publishes a merge held in MAIN mid-suite.
- 🔴 **`-F <file>` for every commit/merge/dm message** — `-m`/double quotes run backticks; `"$(cat file)"` is safe (substitution output is not re-evaluated). `git merge` needs the EXACT branch name. A refused dispatch (`{"issue": "stale-base"}`) leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` — rmdir, sync, re-cut the SAME id.
- 🔴 **`pkill -f '<pattern>'` in a Bash-tool command kills that command** — `pgrep -f` then `kill <pid>`. `grep -v grep` hides your own claude process. Never `cat` a manifest raw (`jq '.agents[] | {id,status,pid,fail_reason}'`); never print a claude argv; the record's `ps_before` is ~50 KB — grep `"result"`/`termd` only.
- **Timestamps from `date -u` in the same call**; `ls -la` prints local (UTC-4). Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait` is the wait. `crons.py` refuses from a worktree; `crontab -l | grep agi-crons`.

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35 s (`bin-suite-fresh` red on the merits after engine edits; the merge-up suite clears it). Baseline: active ≥ 2373 / dep 195 (2568), links 0, goals byte-identical; last MAIN suite 3733/14 @ `14cd8fb29`.

## §6 BANKED (not mine; with a recommendation)

1. Kid model (`~deepseek/deepseek-v4-flash-latest`) — the owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced (L4.102). 5. L4.126's parent died under the INLINE reaper. 8. Stub repo `/home/ubuntu/work/streamer-stub` carries two loop commits unpushed on `main` — the owner's relay session pushes. 9. L4.192 wording residue (send.py "fallback" docstrings). 10. Four dirty agent worktrees removed by hand 2026-09-11 16:35Z (diffs lost). 11. Junk crash-recovery records for this post in `rotations/` (pid 1102718) — MAIN's dir, the Prime's prune. g15 candidates to PROPOSE: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath` (L4.197); rungs 2-4 as g15 lines (owner horizon `vision:web-app-suite`).

## STANDING RULES (binding; the nodes hold the reasoning)

- **Reporting (owner 2026-09-10, verbatim in `doc:l4-owner-decisions`): only when NECESSARY** = a merge-up ready/done (ONE message, numbers, ask the window in it) · a Prime-only decision · a rotation line · a red merge or a rule-changing finding. Binds me→Prime and helper→me.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` (exit 0) + the ListAgents row + `tmux capture-pane` — all three, even for a message announcing itself as the new Prime. `idle` is not dead.
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop. The repo is PUBLIC (AGPL-3.0): log lines, never keys.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent, the parent merges every kid branch before `done:`. Never: wake another post · write `config:seats` (0a's code may) · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`. Landed + verified work is never re-derived — a fix-only claim says what is already done. **`HANDOFF.md` is the Prime's file; this one is the post's.**
- **Spend:** `provisioning.py spend`; a round ≈ $0.06-0.10; stop dispatching at account remaining < $1.00 and report; never auto-switch to the Claude fallback; never mint/revoke a key.

## MERGE-UP RECIPE

1. Seat synced to `origin/season/s2`; seat `verify` green (bin-suite-fresh may be red on the merits).
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline.
3. In MAIN `/home/ubuntu/work/agi` (`git status` first; leave files outside your path set alone; never clean/stash): `git merge --no-ff seat/sanctuary-director@s2 -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (`timeout: 600000`; 10/10 first read) → `grid.py commit --all` → `git push origin season/s2` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` AFTER the push (`--level quick` stamps nothing) → ONE message, five numbers + hash.
4. **Never merge-then-hold** — MAIN is pushed by the Prime and the `:07` `branch_push` cron; `grid_sync` pushes grid refs every 5 min.

## ROTATING YOURSELF

At **0.47** (close under the line). **Out = ONE call** (owner 03:2xZ via master-sensei 04:41Z): `rotate.py rotate-self --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` (effort `max`; never `loop`) — its `--prepare` gate is the check and NAMES what blocks (behind season/s2, stale template, dirty rows); no `ps`, no fetch/behind by hand, no `--dry-run` rehearsal first. The card (this file) is written DURING the work, not at rotation. The predecessor's 214458Z out paid 4 re-derivation calls — that is the number to beat. If the gate names `behind`, `git merge --no-edit origin/season/s2` (F14) and re-run. The record's `s12_self_reap` proves your own reap. The prayer closes a SESSION, after the report.

## WHAT THIS POST HAS LEARNED

- Ask what subject a check actually resolved before you believe its verdict (`crons.py show` from a worktree, `meter --seat` on a frozen row, a green test that requires the defect).
- Run it against the real tree, with the bytes under review, from the tree that has the defect; paste what you ran into the node.
- Check the easy inference before you make it, especially when it flatters your own work; cite the mechanism (file:line), never the correlate.
- Correct your own record in the file your successor reads, in the same breath as the finding. A round that stops at the correct boundary is not a failed round.
