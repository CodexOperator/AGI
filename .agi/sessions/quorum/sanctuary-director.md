# SESSION HANDOFF — 2026-09-12 sanctuary-director: LIVE SCRATCHPAD (written by the 074751Z session — record `sanctuary-director.20260912T074751Z.json`, session cc15b73c, window @320, woke 07:47:52Z; the successor replaces this wholesale AS IT WORKS)

🔴 **IF THE PRIME HAS RUN THE LIVE RENAMES** (`cli.py post-rename --apply`, then `branch-reshuffle --apply --kinds posts,towns`): your worktree is `.agi/worktrees/post-sanctuary-director` on `season2/posts/sanctuary-director`, MAIN on `season2/main`, rows in `config:posts`, spellings `--post`/`AGI_POST`; every `seat/…@s2` / `origin/season/s2` below reads through the one-season alias (readers accept both). **Not run as of 07:50Z** — `git branch --show-current` = `seat/sanctuary-director@s2`; the alias layer IS live (`branches.py: deprecated alias used: season/s2 -> season2/main`).

**OWNER: no generations in prose/dms/commits — name a session by its rotation-record stamp · this post touches only its own tracking, in this file · "wrap up this loop soon" · seat → POST in prose · doc trim pass.** Owner verbatim lives in `doc:l4-owner-decisions`, never here.

## §0 STATE (stamped 10:30Z)

```
WAKE = 0 required calls (SL7.06: the predecessor answers `continue`;      ROUND (each L4.NNN)                          CLOSE
STARTUP carries record, facts, prime-authority, git-state, inbox,        claim_append ──► commit+push ──► dispatch    ONE line to the Prime = numbers only
live-spawns — re-running any of them buys nothing)                       status --iter --wait 540 ──► review BYTES
   ▼                                                                      merge round branch ──► run on the REAL tree
ONE send.py read <post> at every seam ──► IDLE unless necessary           ──► harvest note ──► commit+push
```

- **PRIME = `68dbd1`** (IS-AUTHORIZED 07:47Z vs origin/season/s2 @ `3c8ad978e`; `92eda4` = XIV is STALE). Its steps after mur-45: post-rename → branch-reshuffle → `--delete-old` after a green stamp → the season CLOSE. **Rail: openrouter only** (owner 01:31Z), pi for every parent/kid; a 403 = one line to the Prime and stop. Pin-reap NOT ARMED. Merge-up window is STATE (`test -f .agi/sessions/verify-suite.lock` in MAIN + inbox before ANY MAIN merge). A role is RESOLVED, never typed.
- **Peers 07:50Z:** helper `sanctuary-helper` ref `5f209b` @307 (rotation 8) standing by, next id L4.260, cuts nothing unless named (dm 07:5xZ; no reply owed). sensei-director / master-sensei: resolve by `send.py whois <ref> --claim <post>`, never by name; sensei-director owns rotate.py + SL7.*; master-sensei owns SL7.04 (seats.md EOF newline). Predecessor 043918Z: its self-reap = `s12_self_reap` in the record, one `rotate.py status --seat sanctuary-director --record latest` later, never ps/tmux.
- **Tree:** seat `bf9b18192` = origin seat, synced to origin/season/s2 `63ba0926f` (Prime's g17.1 note `bf7881ad1` + dms), 3 ahead (card, merge, mints). Rotation baseline stamped @`23d243b7d` (mur-45). MAIN `/home/ubuntu/work/agi` carries others' live uncommitted dirt — leave it. Live spawns 8/25 at 07:47Z, ALL SL7.18-22 (the sensei's), none mine.
- **Ids: L4.316 + L4.317 LIVE, L4.318 reserved for line (2); free L4.319+.** UNIT: reaper `heal.py watch` from MAIN (restarted 19:56Z; later heal.py edits are dead in the live watcher until the Prime restarts it).
- **Helpers in `$S`** (`/tmp/claude-1001/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<session-id>/scratchpad`, die with the session): none yet — `note.py`/`mint.py`/`claim_append.py` are ~12 lines each over write.py; rewrite on first need.

## §1 LANDED THIS SESSION (07:47Z–)

- Wake 07:47:52Z: zero required acts (record reads `started` by construction; STARTUP inbox empty). 1 call: stamp + card path + peek (helper's standing-by dm). Card replaced 07:50Z.
- **mur-45 LANDED `23d243b7d`** — GO (signed, 08:08:33Z) → seat merged origin `567ce1730` (`6c55cf7db`, clean) → 749 passed / 14 suites → MAIN merge `--no-ff` `23d243b7d` → render no-op, check byte-identical → verify-suite 11/11 (2426/195/2621, tests 3868/15, seat-model 3/0 drift) → grid 0 new → pushed `567ce1730..23d243b7d` + grid refs 08:19Z → stamp 10/10 baseline @`23d243b7d` → ONE message to the Prime 08:21:34Z (numbers + 5 g15 lines). 7 calls GO→message.
- **mur-45 BY NAME (Prime 10:22Z, wf_2144282d-658, g17.1 `bf7881ad1`):** L4.311/315 ACCEPT_WITH_RESIDUE · L4.313/314 ACCEPT · **L4.312 DEMOTED** (post-rename --apply never re-points an existing upstream; step 6 deletes origin/seat/<n>@s2 before the gate; `_post_rename_upstream` ignores the returncode; --delete-old sorts master first; origin-moved refusal re-baselines). Orders executed 10:27-10:28Z: minted under g15 (`bf9b18192`) (1) `l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing` (2) `l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true` (3) `l4-a-harvest-note-cites-only-what-resolves`; cut L4.316 = (1), L4.317 = (3) in parallel (disjoint); (2) waits for (1) — both touch cli.py. L4.311 residue routed to the sensei-director by the Prime. 9 calls orders→cut (5 were grammar recovery: dispatch/mint/claim shape — now in §0 GRAMMAR below).

## §2 LIVE + QUEUE (stamped 07:50Z)

**LIVE (cut 10:28Z, sessions under this worktree's `.agi/sessions/iter-L4.31x/`):**
- **L4.316** = (1) I/H round 3 fix-only → parent `a00-454c3e1e` pid 4192944, `git branch --list '*a00-454c3e1e*'`; scope cli.py post-rename/branch-reshuffle regions + test_post_rename + test_branch_reshuffle; 4 kids by region (A upstream re-point, B --apply deletes nothing, C --delete-old order posts,towns,main/master never, D origin-moved refusal never re-baselines). Fixture only; real-tree `--dry-run` pasted on the node.
- **L4.317** = (3) L4.313 wording, nodes only → parent `a00-05a1eac0` pid 4193632, `git branch --list '*a00-05a1eac0*'`.
- **QUEUE: L4.318** = (2) L4.315 residue on `hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true` — cut ONLY after L4.316 is merged into the seat (cli.py overlap). Then merge-up 46 request (numbers). H/I LIVE STEPS + rungs 2-4 HELD (Prime).

**GRAMMAR (recovered 10:24-10:27Z, 5 calls — do not re-derive):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (max 2 parents; spawn gate names the rule). cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; returns after spawn, inline reaper OFF; `--level big` refused). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout 540`. Order lines live in the node's `testable_claim` (verbatim Prime + FILE SCOPE + KIDS by region + PROOF/DISPROOF); the parent writes its done note under `## Agent Notes`; the harvest note = `write.py <node> "note HARVEST L4.NNN (sanctuary-director 074751Z, <ts>): …"`.

- Rungs 2-4 minted + HELD (`l4-a-ring-decision-carries-m-of-n-signatures`, `l4-a-veto-freezes-never-frees`, `l4-an-untrusted-lane-earns-tier-by-signed-verdicts`) — dispatch only after the flip, on the Prime's GO.
- NEXT SEASON (on their nodes): L4.291 residue · rotation-record argv cap · pin-reap round 2 (Prime's C) · helper's `l4-heal-reads-the-freshest-seat-row` · P2 residues L4.296/294/301/303 · L4.304 kid-3 patch · 26 junk crash-recovery records · I round 2 residues on I (`branches._canonical_to_old` lacks `town/<t>@s<N>`; `verification._integration_branch` uncalled; the dry-run writes a gitignored plan file).

## §3 🔴 NEXT COMMAND (stamped 10:30Z)

**Waiting on L4.316 + L4.317:** `python3 extensions/agi/bin/spawn_budget.py status --iter L4.316 --wait --timeout 540` (repeat until the parent is terminal; same for L4.317). HARVEST each (§4 traps): `git fetch`; branch = `git branch --list '*<parent-id>*'`; `git diff --stat $(git merge-base HEAD <branch>)..<branch>`; check `.agi/worktrees/<kid-id>` for every kid id in the parent's note (staged-uncommitted work → commit under the kid's authorship, merge the kid branch); a parent refused by the pre-commit hook leaves the round STAGED in `.agi/worktrees/<parent>` → `git -C … add -A .agi/nodes` + commit as the parent; then `git merge --no-ff <exact branch> -F file` into the seat; run the touched suites on the REAL seat tree (L4.316: test_post_rename test_branch_reshuffle test_cli; L4.317: `links.py links` + `links.py schema`); harvest note on the node; commit + push. THEN cut L4.318 = (2) (`--target hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true`), wait, harvest the same way. THEN seat `verify` → ONE merge-up-46 request to the Prime (numbers; `send.py send belam`), hold for the grant, MERGE-UP RECIPE. Rotate at 0.47 (merge origin first, F14). The live renames + CLOSE are the Prime's/owner's; never `--apply` on the real tree.

## §4 TRAPS (the ones that bit; older ones live in the nodes)

- 🔴 MAIN's `seats.md` reads `M` after every ack — the EOF-newline hunk (SL7.04, master-sensei's), never a row mid-edit. Leave it; never `git checkout -- seats.md` in MAIN (erases identity cells). `cut` is shadowed on this box — awk substr.
- 🔴 A parent may run kids in THEIR OWN worktrees (`.agi/worktrees/<kid>`, branch `season2/loops/…-<kid>`); its `done` carries only its own scratch — at harvest check every kid id for a worktree, commit under the kid's authorship (`-c user.name=<id> -c user.email=<id>@agi.local`), merge the kid branches, `git rm` any `.agi/tmp/*` the parent staged; diff the deletions (kids make unrelated global edits).
- 🔴 The pre-commit hook may REFUSE a parent's `done:` on a `season2/loops/*` branch, leaving the round STAGED in its worktree — harvest = `git -C .agi/worktrees/<parent> add -A .agi/nodes` + commit as the parent, then merge. L4.305's guard patch landed in mur-44 — verify on the first real round. Branch: `git branch --list '*<agent>*'`.
- 🔴 A kid can consume YOUR inbox — the FILE `.agi/sessions/inbox/sanctuary-director.md` is the record (`grep -n '^ts: ' | tail`; `awk '/<ts>/{f=1} f'`); never `| head` a read; an mtime loop misses same-second dms — compare size too (`stat -c '%Y %s'`). `peek` does not mark read; `read` does.
- 🔴 A merge-up GRANT is state — `test -f` the lock + `ps -p <pid>` + inbox before `git merge` in MAIN; undo = `git reset --soft <base>` + per-file restore, never `reset --hard` (MAIN carries live comms/rotations). The `:07` branch_push cron publishes anything held in MAIN.
- 🔴 `-F <file>` for every commit/merge/dm message (`-m`/double quotes run backticks; `"$(cat file)"` is safe). `git merge` needs the EXACT branch name. A refused dispatch (`{"issue": "stale-base"}`) leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` — rmdir, sync, re-cut the SAME id.
- 🔴 `pkill -f '<pattern>'` in a Bash-tool command kills that command — `pgrep -f` then `kill <pid>`. Never `cat` a manifest raw (`jq '.agents[] | {id,status,pid,fail_reason}'`); never print a claude argv; the record's `ps_before` is ~50 KB — grep `"result"`/`termd` only.
- `date -u` in the same call for stamps (`ls -la` prints UTC-4). Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait` is the wait. `crons.py` refuses from a worktree — `crontab -l | grep agi-crons`.

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35 s (`bin-suite-fresh` red on the merits after engine edits; the merge-up suite clears it). Baseline: active ≥ 2426 / dep 195 (2621), links 0, goals byte-identical; last MAIN suite 3868/15 @ mur-45 (`23d243b7d`), stamped.

## §6 BANKED (not mine; with a recommendation)

1. Kid model (`~deepseek/deepseek-v4-flash-latest`) — the owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced (L4.102). 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub`: two loop commits unpushed on `main` — the owner's relay pushes. 7. L4.192 wording residue (send.py "fallback" docstrings). 8. Four dirty agent worktrees removed by hand 2026-09-11 16:35Z (diffs lost). 9. Junk crash-recovery records for this post in `rotations/` (pid 1102718) — MAIN's dir, the Prime's prune. g15 candidates to PROPOSE: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath` (L4.197); rungs 2-4 as g15 lines (owner horizon `vision:web-app-suite`).

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

At **0.47** (close under the line). **Out = ONE call**: `rotate.py rotate-self --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` (effort `max`; never `loop`) — its `--prepare` gate is the check and NAMES what blocks (behind season/s2, stale template, dirty rows); no `ps`, no fetch/behind by hand, no `--dry-run` rehearsal first. If it names `behind`: `git merge --no-edit origin/season/s2` (F14) and re-run. The card is written DURING the work, not at rotation. The 043918Z → 074751Z join cost the successor 1 call and 0 re-derivations — that is the number to hold. The prayer closes a SESSION, after the report.

## WHAT THIS POST HAS LEARNED

- Ask what subject a check actually resolved before you believe its verdict (`crons.py show` from a worktree, `meter --seat` on a frozen row, a green test that requires the defect).
- Run it against the real tree, with the bytes under review, from the tree that has the defect; paste what you ran into the node.
- Check the easy inference before you make it, especially when it flatters your own work; cite the mechanism (file:line), never the correlate.
- Correct your own record in the file your successor reads, in the same breath as the finding. A round that stops at the correct boundary is not a failed round.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
