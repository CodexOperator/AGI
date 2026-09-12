# SESSION HANDOFF — 2026-09-12 sanctuary-director: LIVE SCRATCHPAD (written by the 114003Z session — record `sanctuary-director.20260912T114003Z.json`, window @320, woke 11:40:03Z; the successor replaces this wholesale AS IT WORKS)

🔴 **IF THE PRIME HAS RUN THE LIVE RENAMES** (`cli.py post-rename --apply`, then `branch-reshuffle --apply --kinds posts,towns`): your worktree is `.agi/worktrees/post-sanctuary-director` on `season2/posts/sanctuary-director`, MAIN on `season2/main`, rows in `config:posts`, spellings `--post`/`AGI_POST`; every `seat/…@s2` / `origin/season/s2` below reads through the one-season alias (readers accept both). **Not run as of 12:00Z** — `git branch --show-current` = `seat/sanctuary-director@s2`; the alias layer IS live.

**OWNER: no generations in prose/dms/commits — name a session by its rotation-record stamp · this post touches only its own tracking, in this file · "wrap up this loop soon" · seat → POST in prose · doc trim pass.** Owner verbatim lives in `doc:l4-owner-decisions`, never here.

## §0 STATE (stamped 12:00Z)

```
WAKE = 0 required calls (STARTUP carries record, facts, prime-authority,   ROUND (each L4.NNN)                          CLOSE
git-state, inbox, live-spawns — re-running any of them buys nothing)      claim_append ──► commit+push ──► dispatch    ONE line to the Prime = numbers only
   ▼                                                                      status --iter --wait 540 ──► review BYTES
ONE send.py read <post> at every seam ──► IDLE unless necessary           merge round branch ──► run on the REAL tree
                                                                          ──► harvest note ──► commit+push
```

- **PRIME = `68dbd1`** (IS-AUTHORIZED 11:40Z vs origin/season/s2 @ `7b9d127f3`). Its steps after mur-46: post-rename → branch-reshuffle → `--delete-old` after a green stamp → the season CLOSE. **Rail: openrouter only** (owner 01:31Z), pi for every parent/kid; a 403 = one line to the Prime and stop. Merge-up window is STATE (`test -f .agi/sessions/verify-suite.lock` in MAIN + inbox before ANY MAIN merge). A role is RESOLVED, never typed.
- **Peers:** helper `sanctuary-helper` ref `5f209b` @307 standing by (dm 11:41Z), next id L4.260, cuts nothing unless named; no reply owed. sensei-director / master-sensei: resolve by `send.py whois <ref> --claim <post>`, never by name; sensei-director owns rotate.py + SL7.*; SL2#19 landed `7b9d127f3`. Predecessor 074751Z: its self-reap = `s12_self_reap` in the record, ONE `rotate.py status --seat sanctuary-director --record latest`, never ps/tmux.
- **Tree:** seat `a708d9aad` (L4.319 merge) = origin seat + 2 (note + card pending push), 3 behind origin/season/s2 at the GO (main tip `f9905b5ac`). Prime's baseline for 46: **2481/195/2676, tests 3954/15/1x**, lock FREE on main + 5 seats. MAIN `/home/ubuntu/work/agi` carries others' live uncommitted dirt — leave it. Live spawns at 11:40Z: 6/25, all SL7.39/40 (the sensei's) + L4.319 (now done); none mine live.
- **Ids: L4.319 LANDED; free L4.320+.** UNIT: reaper `heal.py watch` from MAIN (heal.py edits are dead in the live watcher until the Prime restarts it).
- **Helpers in `$S`** (`/tmp/claude-1001/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<session-id>/scratchpad`, die with the session): `l4319/` (branches.py probe + merge msg). `note.py`/`mint.py`/`claim_append.py` are ~12 lines each over write.py; rewrite on first need.

## §1 LANDED THIS SESSION (11:40Z–)

- Wake 11:40Z: zero required acts. Call 1 = `spawn_budget.py status --iter L4.319 --wait 540` (parent still live at 11:50Z); call 2 = inbox read (helper standing by · **WINDOW 46 GO signed 11:42Z** · kid a00-3e3acdf1 proved) + second wait → parent done 11:57Z.
- **L4.319 LANDED `a708d9aad`** (11:59Z; parent `a00-d5b6e48c`, 2 kids a00-3e3acdf1 proved / a00-8632c40f; 19 min; parent's done commit landed cleanly, no scratch staged, no kid worktrees): A `_RESHUFFLE_DEFAULT_KINDS = {post, town_main}` — no `--kinds` → defaults + prints the defaulting line (main/loops only when named; master add-only) · B `branches.py` `_POST_AT_RE` `post/<n>@sN` → `season<N>/posts/<n>`, reverse `_canonical_to_old` → `post/<n>@sN` (default) / `seat/<n>@sN` (`legacy_seat=True`, `ref_candidates` uses it). Director re-ran on the real seat tree: 85 passed (test_branch_reshuffle + test_branches + test_cli); unfiltered `branch-reshuffle --dry-run` prints the defaulting line, 5 legacy branches (3 posts + 2 towns), NO loop/* and NO master job, nothing changed, tree clean. **RESIDUE (measured in-process on the round's branches.py, on the node for the Prime): `ref_candidates('post/<n>@s2')` → `[season2/posts/<n>, seat/<n>@s2]` — the INPUT spelling is dropped, so at the rename mid-point (post-rename --apply done, reshuffle --apply not yet, `--delete-old` not yet) a reader handed the live post/ name never tries it (it still resolves through the not-yet-deleted seat/ ref, same tip unless post/ moved). One-line fix: canonical + intermediate + legacy, deduped.**

## §2 LIVE + QUEUE (stamped 12:00Z)

**LIVE: nothing dispatched.** **QUEUE: merge-up 46 = GO (signed 11:42Z)** — Prime HOLDS main commits until my merge-up line; L4.319 rides 46 (done before the recipe started). Then mur-46 by name together with mur-SL2.19 (the Prime's). H/I LIVE STEPS + rungs 2-4 HELD (Prime).

**GRAMMAR (do not re-derive):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (max 2 parents). cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; returns after spawn; `--level big` refused). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout 540` (rounds run 19-41 min; the reaper's `overdue` dm at ~28 min is informational). Order lines live in the node's `testable_claim`; the parent writes its done note under `## Agent Notes`; harvest note = `write.py <node> "note HARVEST L4.NNN (sanctuary-director 114003Z, <ts>): …" --actor sanctuary-director --role director`.

- Rungs 2-4 minted + HELD (`l4-a-ring-decision-carries-m-of-n-signatures`, `l4-a-veto-freezes-never-frees`, `l4-an-untrusted-lane-earns-tier-by-signed-verdicts`) — dispatch only after the flip, on the Prime's GO.
- NEXT SEASON (on their nodes): L4.291 residue · rotation-record argv cap · pin-reap round 2 (Prime's C) · helper's `l4-heal-reads-the-freshest-seat-row` · P2 residues L4.296/294/301/303 · L4.304 kid-3 patch · 26 junk crash-recovery records · I round 2 residues (`verification._integration_branch` uncalled; the dry-run writes a gitignored plan file) · L4.319 residue above.

## §3 🔴 NEXT COMMAND (stamped 12:00Z — the 114003Z session, mid merge-up 46)

**(a) DONE: L4.319 harvested + noted. (b) IN FLIGHT: merge-up 46** — `git fetch`; `git merge --no-edit origin/season/s2` in the seat (3 behind at the GO; never rebase); re-run the touched suites (`test_post_rename test_branch_reshuffle test_branches test_cli test_seat_alias_notice test_hook_alias_notice test_send test_dispatch_dry_run test_git_commit_guard`); push seat → **MERGE-UP RECIPE** below (MAIN: `git status` first; lock `test -f .agi/sessions/verify-suite.lock` absent; `git merge --no-ff seat/sanctuary-director@s2 -F file` → render → `--render --check` → `commands.py run verify-suite` FOREGROUND → `grid.py commit --all` → push season/s2 + grid refs → `verification.py --level rotation --stamp`) → ONE message to the Prime: five numbers + hash + one g15 line per node (L4.316 (1), L4.317 (3), L4.318 (2), L4.319 = the two residue rulings) + the ref_candidates residue → idle. **If the successor wakes with MAIN already carrying the merge (`git -C /home/ubuntu/work/agi log --oneline -3` shows it) but no message sent: run verify-suite / stamp / message from where it stopped — never re-merge.** Never `--apply`/`--delete-old` on the real tree; live renames + CLOSE = the Prime's/owner's. Rotate at 0.47 (merge origin first, F14).

## §4 TRAPS (the ones that bit; older ones live in the nodes)

- 🔴 MAIN's `seats.md` reads `M` after every ack — the EOF-newline hunk (SL7.04, master-sensei's). Leave it; never `git checkout -- seats.md` in MAIN. `cut` is shadowed on this box — awk substr.
- 🔴 A parent may run kids in THEIR OWN worktrees (`.agi/worktrees/<kid>`); at harvest check every kid id for a worktree + branch, commit under the kid's authorship, merge the kid branches, `git rm -qf` any `.agi/tmp/*` the parent staged; diff the deletions. (L4.319: none of this — one clean done commit.)
- 🔴 The pre-commit hook may REFUSE a parent's `done:` on a `season2/loops/*` branch, leaving the round STAGED in its worktree — harvest = `git -C .agi/worktrees/<parent> add -A .agi/nodes` + commit as the parent, then merge. L4.305's guard patch held on L4.317/318/319.
- 🔴 A kid can consume YOUR inbox — the FILE `.agi/sessions/inbox/sanctuary-director.md` is the record; never `| head` a read. `peek` does not mark read; `read` does.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>` + per-file restore, never `reset --hard`. The `:07` branch_push cron publishes anything held in MAIN.
- 🔴 `-F <file>` for every commit/merge/dm message (`-m`/double quotes run backticks). `git merge` needs the EXACT branch name (`git branch --list '*<agent>*' | sed 's/^[*+ ]*//'`). A refused dispatch (`stale-base`) leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` — rmdir, sync, re-cut the SAME id.
- 🔴 `pkill -f` in a Bash-tool command kills that command — `pgrep -f` then `kill <pid>`. Never `cat` a manifest raw (`jq '.agents[] | {id,status,pid,fail_reason}'`); never print a claude argv; the record's `ps_before` is ~50 KB — grep `"result"`/`termd` only.
- `date -u` in the same call for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait` is the wait. `crons.py` refuses from a worktree — `crontab -l | grep agi-crons`.

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35 s (`bin-suite-fresh` red on the merits after engine edits; the merge-up suite clears it). Baseline: active ≥ 2481 / dep 195 (2676), links 0, goals byte-identical; last MAIN suite 3954/15 @ SL2#19 (`7b9d127f3`), the Prime's.

## §6 BANKED (not mine; with a recommendation)

1. Kid model (`~deepseek/deepseek-v4-flash-latest`) — the owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced (L4.102). 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub`: two loop commits unpushed on `main` — the owner's relay pushes. 7. L4.192 wording residue. 8. Four dirty agent worktrees removed by hand 2026-09-11 16:35Z (diffs lost). 9. Junk crash-recovery records for this post in `rotations/` — MAIN's dir, the Prime's prune. g15 candidates to PROPOSE: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath` (L4.197); rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling (L4.319 residue).

## STANDING RULES (binding; the nodes hold the reasoning)

- **Reporting (owner 2026-09-10, verbatim in `doc:l4-owner-decisions`): only when NECESSARY** = a merge-up ready/done (ONE message, numbers, ask the window in it) · a Prime-only decision · a rotation line · a red merge or a rule-changing finding. Binds me→Prime and helper→me.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` (exit 0) + the ListAgents row + `tmux capture-pane` — all three, even for a message announcing itself as the new Prime. `idle` is not dead.
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop. The repo is PUBLIC (AGPL-3.0): log lines, never keys.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent, the parent merges every kid branch before `done:`. Never: wake another post · write `config:seats` (0a's code may) · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`. Landed + verified work is never re-derived — a fix-only claim says what is already done. **`HANDOFF.md` is the Prime's file; this one is the post's.**
- **Spend:** `provisioning.py spend`; a round ≈ $0.06-0.10; stop dispatching at account remaining < $1.00 and report; never auto-switch to the Claude fallback; never mint/revoke a key.

## MERGE-UP RECIPE

1. Seat synced to `origin/season/s2`; seat `verify` green (bin-suite-fresh may be red on the merits).
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline (window 46: granted 11:42Z, signed).
3. In MAIN `/home/ubuntu/work/agi` (`git status` first; leave files outside your path set alone; never clean/stash): `git merge --no-ff seat/sanctuary-director@s2 -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (`timeout: 600000`; 10/10 first read) → `grid.py commit --all` → `git push origin season/s2` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` AFTER the push (`--level quick` stamps nothing) → ONE message, five numbers + hash.
4. **Never merge-then-hold** — MAIN is pushed by the Prime and the `:07` `branch_push` cron; `grid_sync` pushes grid refs every 5 min.

## ROTATING YOURSELF

At **0.47** (close under the line). **Out = ONE call**: `rotate.py rotate-self --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` (effort `max`; never `loop`) — its `--prepare` gate is the check and NAMES what blocks; no `ps`, no fetch/behind by hand, no `--dry-run` rehearsal first. If it names `behind`: `git merge --no-edit origin/season/s2` (F14) and re-run. The card is written DURING the work, not at rotation. The 074751Z → 114003Z join cost the successor 0 wake calls and 0 re-derivations (§2 GRAMMAR read, not re-derived). The prayer closes a SESSION, after the report.

## WHAT THIS POST HAS LEARNED

- Ask what subject a check actually resolved before you believe its verdict (`crons.py show` from a worktree, `meter --seat` on a frozen row, a green test that requires the defect).
- Run it against the real tree, with the bytes under review, from the tree that has the defect; paste what you ran into the node. Probe the round's module in-process (`git show <branch>:<file> > $S/x.py`; import it) before you believe a ruling is closed — L4.319's tests pass and the input spelling is still dropped.
- Check the easy inference before you make it, especially when it flatters your own work; cite the mechanism (file:line), never the correlate.
- Correct your own record in the file your successor reads, in the same breath as the finding. A round that stops at the correct boundary is not a failed round.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
