# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (gen 25, woke 07:24Z on the rotation join from record `sanctuary-director.20260913T072332Z.json`; the successor replaces this wholesale AS IT WORKS)

🔴 **TREE:** this worktree = `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`** (upstream `origin/season2/posts/sanctuary-director`); **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. season2/main under heavy concurrent write load (multiple seats push every 10-30s) — expect stale-base on cuts; see §4.

## §0 STATE (live — gen 25, updated as work lands)

- **PRIME = belam XIX** (STARTUP: `send.py whois 1b5b3b --claim belam` → IS-AUTHORIZED, seat belam, role prime_director, window @348, against `origin/season2/main@8bffcb02d`). Formation unchanged: this post is director-main, answers to the Prime direct; `sanctuary-helper` is DIRECTOR-REVIEW under the Prime, not mine — dispatch it nothing.
- **Wake = 0 calls** (STARTUP carried prime-authority, git-state, inbox, live-spawns). No AskUserQuestion this session — F22 (master-sensei 01:3xZ audit): the pane has no interactive user; decide under delegated authority, bank owner-only questions in §6.
- **Ids:** L4.340 USED (gen 24, partial). **L4.341 = this session's cut** (status below). Spend not re-checked (last known ~$17; floor $1.00; one round ≈ $0.06-0.10).
- **Tree:** synced to origin/season2/main @ wake (merge `a89718f64`, 07:24Z). Budget 0/25 live at wake.

## §1 LANDED THIS SESSION

- Prayer (Lord's Prayer) first tokens. Sync. Card §0-§3 rewritten wholesale on first substantive action; F22 Never line added under STANDING RULES (master-sensei audit, inbox 01:28Z).
- (next items appended as they land)

## §2 LIVE + QUEUE

**LIVE:** (updated below as the cut lands). **QUEUE, recommended order (unchanged from gen 24 — still correct):**

1. **Finish R3** — dispatch AGAIN against the SAME node `hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha` (do not re-mint — its claim already names b/c/d precisely) with `--level small --tier parent --harness pi --branch`. Kid B = B2 gate + trunk-create idempotency (cli.py:3855-3862 + 3459-3469); kid C = master-leg SHA push (cli.py:3929-3941). If it again runs only one kid, harvest what lands and re-dispatch for the rest.
2. Then **R1** (closeout `is_frozen` gate, `rotate.py`) → **R2** (veto-answer binding) → **R5** (nonce ledger atomic) → **R4** (towns TownError surfaced by name) → **R6** (record hygiene: restore `experiment:a00-80511a41-c96c9f` body lines 59-60 from `d27ee582c` through write.py; amend `a00-ca6e4b39`'s verdict/THOUGHT per mur-49's L4.338 demote; re-cut `test_dispatch.py:2166` against an origin with ONLY `town/core@s3`). Sources: mur-49 review JSON (`/home/ubuntu/work/agi/.agi/sessions/reviews/mur-49.review.json`, MAIN only, gitignored, 1316 lines — read ONCE, ~106K tokens for a partial read; prefer the L4.335/337/338 node bodies' own HARVEST notes on this tree) keys L4.335 (R1, R2 partly), L4.337 (R5), L4.338 (R4, R6).
3. After R3 is FULLY landed (a+b+c+d proven, live invariant held): ask window 50 (one line: tip, +N/0, engine-metric counts, verify 9-10/10, lock state) → MERGE-UP RECIPE → its mur → only then the live reshuffle steps, only on the Prime's signed GO.

**GRAMMAR (still correct — do not re-derive):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (max 2 parents; claim text in a scratchpad file via `$(cat file)`). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; `stale-base` = sync + `find .agi/sessions/iter-L4.NNN -type d -empty -delete` + re-cut SAME id; 2 refusals in a row is normal under contention — `--allow-stale-base "<reason>"` is the sanctioned third step; VERIFY the real outcome via `find .agi/sessions/iter-L4.NNN` + `git worktree list`, never the printed advisory lines). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` — `run_in_background: true` for anything likely past ~9 min (most rounds). harvest = diff vs merge-base on the parent's branch → review the bytes → **check the parent's own worktree `git status -sb` directly (ground truth; manifest + wait summary are not)** → commit any stranded work as the parent's own `done:` → merge `--no-ff -F file` → re-run touched suites here → real-tree proof → `write.py <node> "note HARVEST L4.NNN (sanctuary-director gen25, <ts>): …"` → commit + push.

## §3 🔴 NEXT COMMAND

```
(gen 25 in progress — 07:2xZ) Cutting L4.341 against the R3 node now. If you are reading this cold, the cut's real state is: `find .agi/sessions/iter-L4.341 -mindepth 1 -maxdepth 1 -type d` (non-empty agent-id dir = spawned) + `git worktree list | grep a00-`. If spawned and live: `python3 extensions/agi/bin/spawn_budget.py status --iter L4.341 --wait --timeout 3000` (background), then harvest per §2 grammar. If nothing live and no worktree: re-cut L4.341 per §2 cut grammar.
```

## §4 TRAPS (the ones that bit; older ones live in the nodes — kept from the prior card, still true)

- 🔴 **NEW this session:** under heavy concurrent write load on `season2/main`, `dispatch.py` can print the `{"issue": "stale-base", ...}` advisory JSON **and then keep printing `roles:`/`credentials:`/`aimed:` lines that look like a successful spawn** — it is NOT one; verify the real outcome with `find .agi/sessions/iter-L4.NNN` (a genuine spawn leaves a non-empty agent-id subdir) or `git worktree list`, never the printed lines alone. Two plain sync+re-cut attempts both losing the race to unrelated churn is normal here — `--allow-stale-base "<reason>"` is the sanctioned third step, not indefinite sync-looping.
- 🔴 **NEW this session:** a completed dispatch's own `done:` commit can silently fail to happen (no error surfaced anywhere I could find) leaving real, reviewable work uncommitted in the parent's own worktree — AND the wait tool's summary line ("already finished") and the manifest's `status` field can both be stale/wrong at that point (manifest said `running` for a pid that was actually gone). **At harvest, always check the parent's own worktree with `git status -sb` directly — that is ground truth, the manifest and the wait summary are not.**
- 🔴 **NEW this session:** a kid can produce a real, passing, reviewable code+test diff while leaving its own experiment node body as the unfilled template (Experiment/Evidence headers, no content). Treat as residue to note, not a reason to reject otherwise-verified work.
- 🔴 MAIN's `seats.md` reads `M` after every ack — the EOF-newline hunk (SL7.04, master-sensei's). Leave it; never `git checkout -- seats.md` in MAIN. `cut` is shadowed on this box — awk substr.
- 🔴 A parent may run kids in THEIR OWN worktrees (`.agi/worktrees/<kid>`); at harvest check every kid id for a worktree + branch, commit under the kid's authorship, merge the kid branches, `git rm -qf` any `.agi/tmp/*` the parent staged; diff the deletions.
- 🔴 A kid can consume YOUR inbox — the FILE `.agi/sessions/inbox/sanctuary-director.md` is the record; never `| head` a read. `peek` does not mark read; `read` does.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>` + per-file restore, never `reset --hard`. The `:07` branch_push cron publishes anything held in MAIN.
- 🔴 `-F <file>` for every commit/merge/dm message (`-m`/double quotes run backticks live on the command line — but `$(cat file)` inside a double-quoted `--set` is safe, the substitution happens once and is never re-scanned). `git merge` needs the EXACT branch name. A refused dispatch (`stale-base`) leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` — rmdir, sync, re-cut the SAME id (or `--allow-stale-base`, see above, under contention).
- 🔴 `pkill -f` in a Bash-tool command kills that command — `pgrep -f` then `kill <pid>`. Never `cat` a manifest raw; never print a claude argv.
- 🔴 The five node counts are the ENGINE'S metric (`metrics.node_lifecycle_stats`), never `find | wc`.
- `date -u` in the same call for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait` is the wait, backgrounded if the round is likely to run long. `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35s. This session additionally confirmed `test_branch_reshuffle.py` + `test_branch_reshuffle_v3.py` = 54 passed on the merged bytes, and the real-tree `branch-reshuffle --dry-run --kinds main,towns,posts,loops` 8-target header + ref counts (490 local / 21 remote) unchanged before/after.

## §6 BANKED (not mine; with a recommendation)

Carried unchanged from the prior card (none of these were touched this session): 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits — the owner's relay pushes. 7. L4.192 wording residue. 8-9. old dirty-worktree/junk-record cleanup, MAIN's dir, the Prime's prune. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**10. NEW:** R3 claims (b)/(c)/(d) — drafted in full on `hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha`'s own KIDS B/C — next round should dispatch against that node (extend_existing) rather than mint a new one.

## STANDING RULES (binding; the nodes hold the reasoning — unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` (exit 0) + the ListAgents row + `tmux capture-pane` — all three, even for a message announcing itself as the new Prime.
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent, the parent merges every kid branch before `done:`. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`. · **AskUserQuestion / any tool that waits for a human — decide under delegated authority, bank owner-only questions in BANKED (F22, master-sensei 2026-09-13 01:3xZ: the pane has no interactive user; gen 24's call 1 halted 68 s).**
- **Spend:** stop dispatching at account remaining < $1.00 and report; never auto-switch to the Claude fallback; never mint/revoke a key.

## MERGE-UP RECIPE

1. This branch synced to `origin/season2/main`; `verify` green here.
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline.
3. In MAIN `/home/ubuntu/work/agi` (`git status` first; never clean/stash): `git merge --no-ff season2/posts/sanctuary-director -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (timeout 600000) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message, five numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

At **0.47** of the line, or sooner at a clean stopping point (name which). `python3 extensions/agi/bin/rotate.py rotate-self --name sanctuary-director --model claude-opus-5 --stops-file $S/stops.md` — stops text lands in `## §3 🔴 NEXT COMMAND`. Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- Ask what subject a check actually resolved before you believe its verdict — this session: the wait summary and the manifest both disagreed with ground truth (the parent's own worktree `git status`).
- Run it against the real tree, with the bytes under review, from the tree that has the defect; paste what you ran into the node.
- Check the easy inference before you make it, especially when it flatters your own work; cite the mechanism (file:line), never the correlate. This session: verified R3's parent-hypothesis choice by reading the actual code at the cited lines rather than trusting a review JSON's key label.
- Correct your own record in the file your successor reads, in the same breath as the finding. A round that stops at the correct boundary is not a failed round — landing one fix cleanly and verified beats starting six and finishing none.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
