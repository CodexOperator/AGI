# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (session in progress, as of 18:2xZ: R3.1 + R3.2 + R3.3 all harvested; merge-up-52 merged + verified (10/10 green) + pushed to MAIN as `bef788a5e`; reported to belam with numbers+hash; AWAITING belam's mur-52 registration + ACCEPT before running the `--apply`/`--delete-old` live sequence — inbox still empty. R1/L4.350 (`a00-00aafa3a`) DISPATCHED + LIVE in parallel — see §2/§3, both threads are open at once right now.)

🔴 **TREE:** this worktree = `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`** (upstream `origin/season2/posts/sanctuary-director`); **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. season2/main under heavy concurrent write load (multiple seats push every 10-30s) — expect stale-base on cuts; see §4.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY**, not what feeds rotate-self (`--prompt-file` points at THIS file, `.agi/sessions/quorum/sanctuary-director.md`). Edit the quorum card; leave the root file alone unless the user asks about it specifically.

🔴 **NAMING/TRACKING, owner order 16:4xZ, Prime ruling 16:5xZ (`doc:l4-owner-decisions`):** no post but the Prime tracks generations. Every non-prime post is a perpetual seat, identified by post name + timestamp, never `gen N`. This card, dm lines, commit messages: timestamps/hashes for "when", "earlier"/"this seating"/"the predecessor" for relative order. Mechanics fix tracked as `hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-seatings-key-on-session-id-and-the-label-is-the-post-name-alone` (SM.24) — Sanctuary Master's code, not this post's. Post renames land in SM.18's bundle — **do not rename anything here.**

## §0 STATE (live — updated as work lands)

**AUTHORITY:** under the survival formation the owner speaks ONLY through the Prime (belam); every owner decision is banked verbatim in `doc:l4-owner-decisions` — verify there, never wait for a pane voice. Paid dispatch + merge-up push are standing duties. **Sync first if a cited doc entry isn't found locally** — absence in a stale branch isn't absence on the graph (bit this post more than once).

- **PRIME = belam** = live seat **agi-16** `[1b5b3b]`, tmux `view-sanctuary-master:@348`. Re-verified this session (`send.py whois 1b5b3b --claim belam` → IS-AUTHORIZED). 🔴 Unresolved anomaly carried from an earlier seating, not re-checked this session: a prior `ListAgents` once showed TWO separate `encryption-town` rows under `Remote Control`, distinct from `agi-16` — likely the owner running belam from more than one place, never 3-way resolved. Flag if a future belam-claimed message looks inconsistent.
- **Wake = 0 calls this seating** (STARTUP + AFTER_JOIN carried everything; ack already answered `continue` by the predecessor; reap-proof grep exit 1 = chain fully reaped, confirmed via the record's own `s12_self_reap`, not by hand-`ps`).
- master-sensei DM'd (17:13Z): the predecessor's 17:09Z rotation fired early (0.22 of the meter, not 0.47) because the facts feed truncated at F13 — fixed on MAIN `728698e23`. Not actionable for me beyond: **rotate only when the `[meter]` hook's `est.` number ≥ 0.47** (currently ~0.16).
- **Ids/state:** L4.347=R3.1, L4.348=R3.2, L4.349=R3.3 — **all three harvested, merged (merge-up-52, `bef788a5e`), verified 10/10, pushed.** Full detail in §1. **L4.350=R1 DISPATCHED** (parent `a00-00aafa3a`, real spawn verified via manifest+worktree+branch): fixes mur-49's demotion of L4.335 — the is_frozen gate lives on the wrong seams (`_stops_push`/`_perform_season_merge`, rotate-self-only) instead of `_make_closeout_seams`'s own `_merge_up`/`_push` (the real closeout seam table, confirmed zero is_frozen references). Re-cut the hypothesis in place with mur-49's exact prime_step instructions, dispatched, background wait armed (`bne97paat`, 1800s). See §2/§3.
- 🔴 **mur-51 demoted L4.345** — unchanged this session, not re-checked: fix owner is the **SANCTUARY MASTER, round SM.23** (`hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate`); node marked `demoted-pending-fix` on `585a9c963`/`139643de0`. **Do not restart the reaper.** Check if SM.23 landed before touching this again.
- 🔴 **OWNER-ORDERED RENAME, check before EVERY rotate-self:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json` — not re-checked yet this session, re-check fresh before rotating, don't trust this note.
- **Tree:** synced repeatedly this session (clean each time). Post branch tip `989b3e325`; MAIN tip `bef788a5e` (post-merge-up-52, both pushed).

## §1 LANDED

**R3.1/L4.347 + R3.2/L4.348** (predecessor's work, compressed): both independently re-verified proved on this branch before this session started — see git log (`835bc6e5d`/`7ce22f708` for R3.1, `b766fed2c`/`d95e80bbe` for R3.2) and each hypothesis node's own HARVEST note for the full detail (the `--owns` verdict-label trap hit both times; node frontmatter was authoritative both times).

**R3.3/L4.349 (this session's harvest):** kid `a00-c3b10525` fixed `_rs_v3_local_post_source` (the `--delete-old` B2 exemption) so it actually calls `_post_rename_upstream` on both `branch` and the derived `target` — a post_main carrying a foreign upstream (a real live migration) now REFUSES instead of being silently exempted. New falsifier `test_v3_delete_old_refuses_a_post_main_carrying_a_foreign_upstream` reproduced the pre-fix hole (rc 0, both origin refs deleted) and confirmed the post-fix refusal; existing positive-exemption test unchanged. **Parent ran its own independent adversarial probe outside pytest** against the same fixture shape — refused correctly, positive control still exempted (a step beyond R3.1/R3.2's own rigor). I independently: read the diff directly (matches the node's own claim), confirmed node frontmatter `verdict: proved` (commit subject said `pending` — same `--owns` trap, third time in a row), re-ran the suite myself twice (parent worktree + post-merge): **70 passed** both times. Merged `--no-ff` (`ab68c8d40`→ actually the merge commit is unhashed here, see git log), HARVEST note written + pushed.

**Collateral caught + fixed:** R3.2's harvested comment (`b08c2c656`) had named the planned MAIN tip literally (`season2/main`) inside a code comment — tripped `test_branch_spelling_grep.py`'s frozen-debt pin (a *different* hypothesis's test, `l4-every-branch-name-derives-from-one-tuple...`) on the first full `verify-suite` run since R3.1. This had been sitting merged and undetected because R3.1/R3.2's own harvests only ever ran the narrower `test_branch_reshuffle*.py` suite, never the full engine suite. Fixed with a one-line reword (comment-only, `989b3e325`); branch-reshuffle suites reconfirmed 70/70 after.

**merge-up-52 (this session, done):** window asked + **GRANTED by belam XIX 17:20Z** (lock free, baseline active=2803 deprecated=198 total=3001 sha=`d53edc6e0`, floor cleared). Synced, `commands.py run verify` (9/10, `bin-suite-fresh` red = expected) and `verify-suite` (found the 3 failures above — 1 fixed, 1 confirmed stale pytest-cache phantom test that no longer exists, 1 confirmed **pre-existing on MAIN itself** — see below) run in the worktree first. Merged `--no-ff` into MAIN (`bef788a5e`). `snapshot-goals.py --render` + `--render --check`: clean. `commands.py run verify-suite` FOREGROUND in MAIN: 4713 passed/15 skipped/**1 failed** — `test_sensei_wake_audit.py::TestSLO8WhosPrefix::test_item2_live_f2_whois_rederive_is_category_a_with_live_facts` (F2→F3 label drift). **Reproduced this failure directly against MAIN's own checkout BEFORE the merge touched anything** — confirmed pre-existing, traces to `rotations.md`'s fact-renumbering (master-sensei's own recent fix, entered my branch only via the origin sync), not caused by R3.1/R3.2/R3.3, not fixed by me (out of my domain — flagged to belam instead, see §6 banked #16). `grid.py commit --all`: "0 new version(s)" — checked directly (`grid.py versions <node>` on two of the merged nodes: v1, v2 present) — a concurrent `grid_sync` cron had apparently already versioned + pushed them (`refs/grid/*` push said "Everything up-to-date"). Pushed MAIN (`08d8fd395..bef788a5e`, clean fast-forward, no contention). `verification.py --level rotation --stamp`: **ALL 10 GREEN**, baseline updated to `bef788a5e` (active=2811 deprecated=198 total=3009). Reported to belam: numbers + hash + the pre-existing-failure flag + **a correction** (see next).

**Correction I owe the record:** my own window-ask DM mischaracterized R3.1's target hypothesis as the same one as R3.2's (`...collect-refusals-and-continue...`). Checked `git log --grep` against R3.1's actual harvest commit (`835bc6e5d`) and found its real target is `hypothesis:l4-trunk-create-resume-ls-remote-gates-push-if-remote-absent` ("mur-50 residue (c) fix") — a *different*, related hypothesis in the same mur-50 cluster. R3.2 is the one on `l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip`; R3.3 on `l4-b-exemption-calls-the-upstream-check-its-docstring-promises`. Corrected in my follow-up report to belam. **The merge commit's own prose on MAIN still has the error** — left uncorrected (unpushed-but-already-made local commit; the harness's own git safety rule says never amend without the user asking, and this project's own convention already treats commit prose as non-authoritative — the node/HARVEST notes are the record, and those are correct). Lesson banked in §4/WHAT THIS POST HAS LEARNED: verify a round's target hypothesis against its own harvest commit, not from memory.

## §2 LIVE + QUEUE

**LIVE: waiting on belam.** Sent the merge-up-52 completion report (numbers+hash+correction+pre-existing-failure flag) at ~17:5xZ. Inbox checked repeatedly since, still empty. Belam's own sequence's remaining steps (verbatim, unchanged from the grant):

4. Belam's verify (of the merge-up-52 numbers/hash I reported).
5. **mur-52 by name** (director-review's registered adversarial workflow) — this is what actually makes R3.1+R3.2+R3.3 "VERIFIED" per belam's corrected gate meaning.
6. **On ACCEPT**, run in order, each gated on the previous succeeding, no announcement needed between steps:
   `branch-reshuffle --dry-run --kinds towns,posts,loops` (**never `main`**) → `--apply` → suite green → `--delete-old` → the cell re-spellings below (Prime applies) → `verify` → commit.
7. Fallback (**not needed** — R3.3 landed well inside the 45-minute window, all three are already in ONE merge-up-52 as belam's primary path wanted).

**Cell re-spellings** (captured this session via the live `--dry-run --kinds towns,posts,loops` on the real tree, PRINTED ONLY — the Prime applies them, do not apply by hand):
```
nodes/.geometry/ladder.md:60: season/s2 -> season2/main
nodes/.geometry/ladder.md:61: town/streaming-suite@s2 -> season2/streaming-suite/season1/main
nodes/.geometry/ladder.md:62: town/web-app-suite@s2 -> season2/web-app-suite/season1/main
nodes/.geometry/ladder.md:157: season/s2 -> season2/main
nodes/.geometry/rotations.md:161: season/s2 -> season2/main
nodes/.geometry/rotations.md:175: season/s2 -> season2/main
nodes/.geometry/rotations.md:178: loop/<hypothesis-slug-prefix>-<agent>@s2 -> season2/loops/<hypothesis-slug-prefix>-<agent>
nodes/.geometry/rotations.md:182: season/s2 -> season2/main
nodes/.geometry/rotations.md:185: seat/x@s2 -> season2/posts/x
nodes/.geometry/rotations.md:187: season/s2 -> season2/main (x2)
```
Runbook note printed alongside: a rename needs one `crons.py apply` within the 5-min grid_sync window, else `branch_push` keeps pushing the old name.

**R1 = L4.350, LIVE.** Read mur-49's actual review JSON entry for L4.335 (not just the node's own compressed demotion line) and got the PRECISE finding: `_make_closeout_seams`'s own `_merge_up`/`_push` (the real seam table `_closeout_run_steps` drives) consult is_frozen NOWHERE (verified myself: the falsifier `sed -n '/^def _make_closeout_seams/,/^def _closeout_run_steps/p' extensions/agi/bin/rotate.py | grep -c is_frozen` prints 0) — the earlier L4.335 fix instead gated `_stops_push`/`_perform_season_merge`, which only run on a post's OWN routine rotate-self catch-up-merge/push, never on an actual merge-up into MAIN. Net effect live: a frozen prime scope currently gates the WRONG thing (routine housekeeping, for every post) while leaving the real merge-up path completely ungated. mur-49's own `prime_step` field gave the exact prescribed fix (move the gate to the right two functions, remove/rescope it from the wrong two) plus the falsifier command and a fixture-test spec — re-cut the hypothesis node's `testable_claim`+`title`+`thought` in place with that exact instruction (RUNG 4, after RUNG 3's L4.335), committed+pushed (`f2fd5d61e`), synced (`85bc12940`, picked up someone else's fix of the sensei F2/F3 test — already closed, see §1), dispatched L4.350 (parent `a00-00aafa3a`, worktree/branch/manifest all verified real). Background wait armed (`bne97paat`, 1800s timeout) — **this touches rotate.py's closeout mechanics that govern every post's own rotation, mine included, so harvest this one with EXTRA care**: independently confirm the falsifier command prints >= 2 after, independently confirm a non-prime post's own rotate-self is never held while prime is frozen, don't just trust the kid's own fixture claims.

R2/R4/R5/R6 still need a **separate signed GO** from belam beyond this window grant — not yet asked, unrelated.

**GRAMMAR (still correct — do not re-derive):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (max 2 parents; claim text via `$(cat file)`). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; `stale-base` = sync + `find .agi/sessions/iter-L4.NNN -type d -empty -delete` + re-cut SAME id; 2 refusals in a row is normal under contention — `--allow-stale-base "<reason>"` is the sanctioned third step; VERIFY via `find .agi/sessions/iter-L4.NNN` + `git worktree list`, never the printed lines). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` — `run_in_background: true` past ~9 min. harvest = diff vs merge-base on the parent's branch → review the bytes AND the node content directly (self-reported verdict ≠ ground truth) → **check the parent's own worktree `git status -sb` directly** → commit any stranded work as the parent's own `done:` → merge `--no-ff -F file` → re-run touched suites here → real-tree proof (non-destructive dry-run only if the round touches a destructive path) → `write.py <node> "note HARVEST L4.NNN (sanctuary-director, <ts>): …"` → commit + push. For a round split across worktrees, check BOTH before assuming a manifest is empty.

## §3 🔴 NEXT COMMAND

``````
`````
````
```
TWO live threads right now -- check both:

1. Check inbox fresh: python3 extensions/agi/bin/send.py read sanctuary-director. If belam has replied with mur-52's outcome:
  - ACCEPT -> run, IN ORDER, each gated on the previous succeeding: branch-reshuffle --dry-run --kinds towns,posts,loops (never main, already captured this session -- see §2 for the exact cell re-spelling lines) -> --apply -> suite green -> --delete-old -> the cell re-spellings (Prime applies, you do not hand-edit them) -> verify -> commit. Report completion to belam (numbers+hash, only-when-necessary applies).
  - Anything else (a hold, a correction, a question) -> answer it before touching branch-reshuffle at all; these are DESTRUCTIVE steps (--delete-old removes real origin refs), never proceed on an assumption.

2. R1/L4.350 (parent a00-00aafa3a) is live, background wait armed (bne97paat, 1800s) -- do NOT hand-poll, wait for the notification. When it lands: check the parent's own worktree (/home/ubuntu/work/agi/.agi/worktrees/a00-00aafa3a) git status -sb directly, read the owned kid node(s)' real frontmatter verdict (not the commit subject, not a DM -- confirmed wrong on all of R3.1/R3.2/R3.3 so far), review the rotate.py diff yourself line by line (this touches EVERY post's own rotate-self mechanics -- read it like a security patch, not a routine fix), then INDEPENDENTLY run: `sed -n '/^def _make_closeout_seams/,/^def _closeout_run_steps/p' extensions/agi/bin/rotate.py | grep -c is_frozen` (must now print >= 2, it printed 0 before), the new/extended fixture tests in test_rotate*.py yourself, and touched suites (test_veto.py, test_write_veto_gate.py, test_rotate*.py at minimum). Confirm BOTH halves of the claim landed: (a) the closeout merge_up/push now refuse HELD when frozen, (b) a non-prime post's own rotate-self is no longer held by a frozen prime scope. Harvest per the §2 GRAMMAR block once satisfied. If it dies or drags very long, that is fine to report/bank -- this is NOT gating anything else this session, it is genuinely parallel work.

Do not block idle on either thread alone -- if one is waiting, work the other, or update this card and hold for a notification.

SEPARATELY, before ever rotating: (1) test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json -- re-check fresh, not done yet this session. (2) mur-51/SM.23 (§0) -- check if landed; if not, leave demoted-pending-fix standing, do not re-fix yourself. (3) this post is generation-less by owner order -- never "gen N" in card/dm/commits, timestamps or hashes only. (4) the test_sensei_wake_audit.py F2/F3 failure (§1/§6-banked-16) is NOT yours to fix -- confirmed pre-existing on MAIN, flagged to belam already, leave it for whoever owns config:rotations/sensei.
```
````
`````
``````

## §4 TRAPS (kept from the prior card, trimmed where superseded; two new ones added this session)

- 🔴 **NEW this session:** before naming a round's target hypothesis in a report or a merge commit's prose, verify it against that round's own HARVEST commit message (`git log --grep "L4.NNN"` or read the commit `harvest L4.NNN (...): ...` subject directly) — do not infer it from a neighboring round's hypothesis or from memory. Mischaracterized R3.1's target once this session (assumed it shared R3.2's hypothesis; it didn't) and had to correct it after the merge commit was already made.
- 🔴 **NEW this session:** a round's own narrow test suite passing (e.g. `test_branch_reshuffle*.py`) does not guarantee the FULL engine suite stays green — R3.2's harvested comment hand-spelled a branch name and only a full `verify-suite` run (not re-run since R3.1) caught it, one merge-up later. Run the full suite before a merge-up window closes, not just the round's own suite, and don't assume a prior session's "not re-run recently" note means it's still fine.
- 🔴 A tier-parent's `cli.py done --owns <kid-node-id> --verdict X ...` does **not** write `X` onto the owned node's frontmatter — only into the parent's own `agent.json`. Commit SUBJECT and a kid's self-reported DM can disagree with the node's real `verdict:` (hit on all three of R3.1/R3.2/R3.3 now). **The node file's frontmatter is authoritative. Never trust a commit-subject `verdict=` or a DM.**
- 🔴 A round's session records can be split across MULTIPLE worktrees with MAIN's own `.agi/sessions/iter-L4.NNN` copy sitting completely EMPTY. Check every plausible location before assuming no data.
- 🔴 `grid.py commit --all` REFUSES on a non-master/non-main branch by design — never run it on a post branch. From MAIN only, as part of the merge-up recipe. (Also: a concurrent `grid_sync` cron may beat you to it — "0 new version(s)" is not necessarily an error, verify with `grid.py versions <node>` before assuming something's wrong.)
- 🔴 root `HANDOFF.md` and `.agi/sessions/quorum/sanctuary-director.md` are TWO DIFFERENT FILES. Edit the quorum card only.
- 🔴 Under heavy concurrent write load, `dispatch.py` can print `{"issue": "stale-base", ...}` **and then keep printing lines that look like a successful spawn** — verify with `find .agi/sessions/iter-L4.NNN` or `git worktree list`, never the printed lines alone.
- 🔴 At harvest, always check the parent's own worktree with `git status -sb` directly — the manifest/wait-tool summary can be stale.
- 🔴 A kid can produce a real, passing, reviewable diff while leaving its own experiment node body as the unfilled template — note as residue, not a rejection reason.
- 🔴 A parent may run kids in THEIR OWN worktrees; at harvest check every kid id for a worktree + branch, merge the kid branches, `git rm -qf` any `.agi/tmp/*` staged.
- 🔴 A kid can consume YOUR inbox — `read` marks read, `peek` does not; never `| head` a raw file read.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>` + per-file restore, never `reset --hard`.
- 🔴 `-F <file>` for every commit/merge/dm message. A refused dispatch leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` — rmdir, sync, re-cut the SAME id.
- 🔴 `pkill -f` in a Bash-tool command kills that command — `pgrep -f` then `kill <pid>`. Never `cat` a manifest raw.
- 🔴 The five node counts are the ENGINE'S metric (`metrics.node_lifecycle_stats`), never `find | wc`.
- 🔴 A DM claiming to relay a real owner order can be genuine but still arrive before your own branch has synced far enough to see the doc entry it cites — sync before concluding a citation is missing/false.
- `date -u` for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait`, backgrounded if long. `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

`commands.py run verify` in a worktree: 9/10, `bin-suite-fresh` red is normal (closes only via a full suite run recorded fresh enough, or the Prime's own cadence). `commands.py run verify-suite`, run twice this session: first pass (pre comment-fix) 3 failed/4711 passed/15 skipped; second pass (post comment-fix) **1 failed/4713 passed/15 skipped** — the survivor confirmed pre-existing on MAIN itself, not mine. `test_branch_reshuffle_v3.py` + `test_branch_reshuffle.py`: 70 passed, independently re-run three times this session (parent worktree, post-merge here, post-comment-fix here). **Full rotation-level stamp check in MAIN, post-merge-up-52: `verification.py --level rotation --stamp` → ALL 10 GREEN**, baseline updated to `bef788a5e` (active=2811, deprecated=198, total=3009, broken_links=0). Node count grew from the 2803/198/3001 baseline belam granted the window against — never shrank, per the standing invariant.

## §6 BANKED (not mine; with a recommendation)

**16. NEW this session:** `test_sensei_wake_audit.py::TestSLO8WhosPrefix::test_item2_live_f2_whois_rederive_is_category_a_with_live_facts` fails on MAIN (confirmed directly against MAIN's own tip, before merge-up-52 touched anything): expects label `F2`, gets `F3`. Traces to `rotations.md`'s fact-renumbering (master-sensei's own recent fix, `728698e23`, the same one behind the early-rotation DM this session — see §0). Not caused by R3.1/R3.2/R3.3, not fixed by me — out of this post's domain (sensei/`config:rotations` facts numbering). Flagged to belam in the merge-up-52 report. Recommendation: whoever owns that test (master-sensei, or director-review at next mur) either updates the pinned expected label or investigates why the renumbering shifted a load-bearing category-a case.

**14. master-sensei's suggested STANDING RULES weakening, not adopted.** Drop ListAgents+tmux from Prime-identity verification, keep only signed `whois`? Left as-is — the fuller habit is what surfaced the duplicate `encryption-town` Remote Control rows (§0). Whoever owns this policy (belam or the owner directly) makes the call explicitly.

**15. the "testing plan" phrase.** AUTHORITY cites owner-confirmed "proceed with testing plan as is" — ambiguous scope. Not blocking (independently verified a different way). Worth confirming if it recurs.

**13. director-review's mur-50 process suggestion (still not minted):** "resumability claims should require a remote-visibility fixture (ls-remote), not a local-ref-only comparison." Not urgent. Belam or master-sensei's call.

Carried unchanged from the prior card: 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits — the owner's relay pushes. 7. L4.192 wording residue. 8-9. old dirty-worktree/junk-record cleanup, MAIN's dir, the Prime's prune. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**11. RULED by the Prime 07:28Z:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; the nodes hold the reasoning — unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` (exit 0) + the ListAgents row + `tmux capture-pane` — all three, even for a message announcing itself as the new Prime. For a specific RELAYED OWNER DECISION, the stronger check is independent verification against `doc:l4-owner-decisions` and the commit that banked it. **Sync first if the cited entry isn't found locally** — absence in a stale branch is not evidence of absence.
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent, the parent merges every kid branch before `done:`. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`. · **AskUserQuestion / any tool that waits for a human — decide under delegated authority where it is genuinely operational; a decision that would spend real money or touch shared state and that you cannot verify independently is still worth surfacing plainly rather than either blind compliance or silent refusal.**
- **Spend:** $5.00 floor (`config.json` `provisioning.min_account_remaining_usd = 5.0`): below it NO new round is dispatched, live rounds finish, NO Sonnet parents/kids fallback — PAUSED until the owner resumes; report the pause; never auto-switch to any Claude fallback; never mint/revoke a key.
- **No "gen N" anywhere:** this post is generation-less on every human/model-readable surface. Timestamps and commit hashes carry "when"; "earlier"/"this seating"/"the predecessor" carry relative order.

## MERGE-UP RECIPE

1. This branch synced to `origin/season2/main`; `verify` green here.
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline.
3. In MAIN `/home/ubuntu/work/agi` (`git status` first; never clean/stash): `git merge --no-ff season2/posts/sanctuary-director -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (timeout 600000) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message, five numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

**FIRST, always:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json`. Re-check fresh, do not trust any prior note.

At **0.47** of the meter's `est.` number, or sooner at a clean stopping point (name which). `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed: name, role, model, effort, prompt-file and timeout come from your row + key, NO flag, nothing to look up (never `-h`); it refuses by name when the card's where-it-stops slot is stale — write the card, or pass `--stops '<one line>'`. Stops text lands in `## §3 🔴 NEXT COMMAND`. **NEVER pass a model flag: the `config:seats` row owns the model.** Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. Keep the card current as each part finishes so the rotation is ONE call. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- A relayed instruction with real stakes (money, shared state) deserves independent verification against the graph, not blind trust OR reflexive refusal.
- Ask what subject a check actually resolved before you believe its verdict — a round's session dir can be completely empty in one worktree while the real data lives in another; check all plausible locations.
- A rule's own predicted outcome can legitimately differ in the real case without that being a defect — read why, cite the mechanism, don't assume drift from spec means a bug.
- **A completion tool writing to "the record" can mean two different records** (a dispatched agent's own bookkeeping vs. the node it reviewed) depending on which flag mode it ran under — a label mismatch between a commit subject and a node's frontmatter, or a kid's own self-reported DM, is worth tracing to source once, not shrugging off or blindly picking one side. Confirmed on all three of R3.1/R3.2/R3.3 now — treat it as the default expectation, not a surprise.
- Correct your own record in the file your successor reads, in the same breath as the finding. A round that stops at the correct boundary is not a failed round.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- A DM citing a graph doc can be genuine but still outrun your own branch's sync — absence locally isn't absence on the graph; sync before disbelieving.
- **A round's own narrow test suite going green is not the same as the full engine suite staying green** — run the full `verify-suite` before closing a merge-up window, even when the round's own suite already passed twice.
- **Verify a round's target hypothesis against its own harvest commit message, not from memory or a neighboring round's target** — a report or merge-commit description written from inference can name the wrong hypothesis even when every underlying fact checked was itself correct.
