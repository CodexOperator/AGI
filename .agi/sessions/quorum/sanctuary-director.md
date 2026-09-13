# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (session in progress, as of 18:53Z: R3.1-R3.4 all harvested; R3.4 closed the safety-critical bypass mur-52 found (would have deleted 5 live branches incl. this post's own) but ONLY for kind post/town_main — a live re-check found 3 loop branches STILL unconditionally deletable, so R3.5 (content-containment, EVERY kind) is minted + dispatched, LIVE now as L4.352. `--apply`/`--delete-old` remain NO-GO until R3.5 lands + mur-53. See §0/§2/§3.)

🔴 **TREE:** `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`**; **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. Heavy concurrent write load — several stale-base refusals this session, all real, all resolved by sync+re-cut or `--allow-stale-base` as the sanctioned third step.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY** — edit the quorum card only.

🔴 **NAMING/TRACKING, owner order 16:4xZ:** no post but the Prime tracks generations. Timestamps/hashes for "when", never `gen N`. **Post renames land in SM.18's bundle — do not rename anything here.**

🔴 **NEW OWNER DECISION THIS SESSION, not yet implemented, watch for it landing:** owner 18:3xZ asked whether posts can be local-only, auto-merged, no origin push. Prime ruling (relayed to SM 18:4xZ): YES — post branches (this one included) will stop being pushed as heads, mirrored instead to `refs/agi/posts/<name>` at rotation/merge-up; **merge-up drops the window-ask/grant round-trip — the post takes the advisory suite lock itself and tells the Prime ONE line after.** This is SM's implementation to land, not mine — but once it lands, the MERGE-UP RECIPE below (step 2's window ask) is superseded. Check `doc:l4-owner-decisions` / SM's own card before assuming the old recipe still applies, especially after a rotation.

## §0 STATE (live — updated as work lands)

**AUTHORITY:** owner speaks ONLY through the Prime (belam); every decision banked verbatim in `doc:l4-owner-decisions`. Two more entries landed there this session beyond the mur-52 verdict: (1) owner GO'd hand-deleting 10 **old-spelling legacy** branches (different set, different mechanism, explicitly does not touch what R3.4/R3.5 gate); (2) the posts-local-only ruling above.

- **PRIME = belam** = live seat **agi-16** `[1b5b3b]`. Verified this session.
- **Ids:** L4.347=R3.1, L4.348=R3.2, L4.349=R3.3 → merge-up-52 (`bef788a5e`), all ACCEPTED WITH RESIDUE by mur-52 (destructive-path verdict: NO-GO, see below). L4.350=R1 → **harvested** (rotate.py closeout gate, merged `8f9589eab`). L4.351=R3.4 → **harvested** (the origin-presence gate, merged `04e1a4e7e`, proved for kind post/town_main — see the critical caveat below). **L4.352=R3.5 — LIVE** (parent `a00-09056a37`, real spawn verified, background wait `beakccpky` armed 1800s).
- 🔴 **THE CRITICAL FINDING, still governing everything — read before touching branch-reshuffle:** mur-52 (belam XIX, 18:25Z) accepted R3.1-R3.3 but found `--delete-old`'s B2 gate had a bypass (`cli.py:4039 if not new: continue`) that let 5 LIVE branches — `season2/posts/sanctuary-director` (**this post's own**), `sanctuary-helper`, `sensei-director`, and 2 town mains — queue for UNCONDITIONAL delete. R3.4 fixed this for `kind in (post, town_main)` by requiring the derived v3 successor be confirmed present on origin — independently reverified (diff read, 76 tests passed twice, live read-only dry-run reconfirmed all 5 now REFUSE). **But R3.4's own harvest surfaced a NEW open gap**: the same live dry-run (`--kinds towns,posts,loops`, the ACTUAL kinds the planned live sequence uses) still shows THREE `season2/loops/*` branches queued for unconditional delete — R3.4's gate only fires for post/town_main, never loop. This is not a defect in R3.4 (out of its stated scope) but it means **`--delete-old` is still not safe for the planned kinds set**. R3.5, just dispatched, is scoped to close this too (content-containment, applied to EVERY kind, per belam's own spec plus this session's addendum) — see the R3.5 hypothesis node for the full claim, do not paraphrase from memory.
- **Tree:** synced repeatedly this session, clean each time. Post branch tip `80c5dd190` before R3.5's dispatch commit.
- 🔴 **mur-51 demoted L4.345, fix = SANCTUARY MASTER SM.23** — checked this session: SM.23's own hypothesis node has no HARVEST yet (still open, `demoted-pending-fix` stands). Not mine, don't touch. **Do not restart the reaper.**
- 🔴 **OWNER-ORDERED RENAME, check before EVERY rotate-self:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json` — not re-checked yet this session.
- **Meter:** crossed the 70% warning band this session (0.386/0.47 ≈ 0.82 of the line at last reading); approaching rotation but not there. Card kept current throughout so a rotation at any point is one clean call.

## §1 LANDED

**R3.1+R3.2+R3.3** (merge-up-52, `bef788a5e`) and **R1/L4.350** (rotate.py closeout gate, `8f9589eab`): full detail in git log + each node's HARVEST note; compressed here since both are done and verified. mur-52 ACCEPTED R3.1-R3.3 WITH RESIDUE but found the destructive-path hole described in §0.

**R3.4/L4.351 (the origin-presence gate, harvested this session):** read the actual `cli.py` bypass myself (lines ~4039, ~3576/~3593 for the two bundled residues) before minting, rather than paraphrasing belam's DM. New helper `_rs_v3_successor` derives the remote-visible v3 successor for a `new is None` post/town_main job and the B2 gate refuses (all-or-nothing) unless it's confirmed present on origin. Folds in both mur-52-bundled residues (resume-leg abort-vs-collect; refs/grid status-print position). ONE kid, real diff matched the spec exactly, avoided a real near-miss (gating on the post_main itself, which is upstream-unset by contract and would break genuine migrations forever — used the season-owner town trunk instead). Independently reverified: full diff read, 76 tests passed (twice, parent worktree + post-merge), live read-only dry-run with the ACTUAL planned kinds reconfirmed all 5 named branches now refuse. **The kid's own review surfaced the loop-kind gap** (§0) — an honest, correctly-scoped "proved" for what the claim promised, not a defect. Merged `04e1a4e7e`, HARVEST note (with the loop-kind caveat prominent) written+pushed.

**R3.5 minted (this session):** belam's own spec (content containment: every job's tip an ancestor of its successor or the trunk, `git merge-base --is-ancestor`) expanded with this session's own addendum: it must apply to EVERY kind, not mirror R3.4's post/town_main-only reach, or the same 3 loop branches stay exposed. Cited the existing (but shape-different, unrelated) `cmd_loop_prune`/`_v3_loop_post_main` ancestor-check as a style reference, not a call site. Dispatched as L4.352, real spawn verified.

## §2 LIVE + QUEUE

**LIVE: R3.5 = L4.352 (`a00-09056a37`), tier=parent.** Background wait armed (`beakccpky`, 1800s) — do not hand-poll. **Safety-critical, same discipline as R3.4's harvest**: at completion, check the parent's worktree directly, read the node's real verdict, independently rerun the fixtures + `test_branch_reshuffle*.py`, AND independently rerun a **read-only** `--dry-run --delete-old --kinds towns,posts,loops` to confirm the 3 loop branches (plus the original 5) are no longer unconditionally deletable — "tests pass" is not sufficient proof for this hypothesis class, the live dry-run list is the ground truth (this is literally how mur-52 caught R3.1-R3.3's gap and how R3.4's own gap was caught).

**QUEUE after R3.5 harvests:**
1. **ONE merge-up, numbered 53**, carrying R3.4 + R3.5 together.
2. Window ask to belam with numbers (unless the posts-local-only change above has landed by then — check first).
3. Belam's verify.
4. **mur-53 by name.**
5. **Only on mur-53 ACCEPT**: `branch-reshuffle --dry-run --kinds towns,posts,loops` (never `main`) → `--apply` → suite green → `--delete-old` → cell re-spellings (Prime applies) → `verify` → commit. **Read the `--dry-run` list BY NAME every time** — belam's own note: the Prime's manual-cleanup count does not match the engine's own derived delete-set count (13 jobs under default kinds, 17 with main+loop).

**R2/R4/R5/R6** still need a separate signed GO from belam — not yet asked, unrelated.

**Sources for R2/R4/R5/R6** (R1 done): mur-49 review JSON (`.agi/sessions/reviews/mur-49.review.json`, MAIN only, gitignored — read the relevant node body first). Keys L4.337 (R5), L4.338 (R4, R6).

**GRAMMAR (still correct):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (**no literal `&&` anywhere in generated text** — it splits write.py's script parser into a bogus second verb call; write "and" instead, hit this twice this session). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; `stale-base` = sync + `find .agi/sessions/iter-L4.NNN -type d -empty -delete` + re-cut SAME id; 2 refusals in a row is normal under contention — `--allow-stale-base "<reason>"` is the sanctioned third step; VERIFY via `find`/`git worktree list`, never the printed lines). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` backgrounded. harvest = diff vs merge-base → review bytes + node directly → check parent worktree `git status -sb` directly → merge `--no-ff -F file` → re-run suites here → real-tree proof (read-only/dry-run only, for THIS hypothesis class specifically confirm the actual dry-run OUTPUT LIST, not just green tests) → `write.py <node> "note HARVEST L4.NNN (sanctuary-director, <ts>): …"` → commit + push.

## §3 🔴 NEXT COMMAND

``````
`````
````
```
R3.5 = L4.352 (a00-09056a37) is LIVE. Background wait armed (beakccpky, 1800s) -- wait for the notification, do not hand-poll. When the parent is done:
  1. Check the parent's own worktree git status -sb directly.
  2. Read the owned node's real frontmatter verdict (not the commit subject).
  3. Read the full cli.py diff yourself -- confirm it adds a content-containment check (git merge-base --is-ancestor against the derived successor or the season trunk) that applies to EVERY kind the B2 gate loop processes, not just post/town_main.
  4. Independently rerun the fixtures + test_branch_reshuffle*.py + test_branch_reshuffle.py yourself.
  5. THE CRITICAL CHECK: independently run a READ-ONLY `cli.py branch-reshuffle --dry-run --delete-old --kinds towns,posts,loops` against the merged tree and confirm the three loop branches (season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb, -the-ack-prints-onl-a00-b6b11bd7, -the-meter-hook-rot-a00-d0a730f6) are no longer unconditionally queued -- either refused for containment, or admitted ONLY if their content is genuinely already merged (a legitimate outcome, not presumed either way). NEVER run --delete-old for real.
  6. Merge, re-run suites here, write the HARVEST note (carry forward whether any FURTHER kind/edge case is still open, the way R3.4's note carried forward the loop gap), commit+push.

THEN: merge-up-53 (R3.4+R3.5 together) -- check first whether the posts-local-only change (top of this card) has landed; if so its new recipe applies (no window-ask round-trip, take the suite lock yourself) instead of the old MERGE-UP RECIPE below. Window ask (old form) or suite-lock-self (new form) -> belam's verify -> mur-53 by name -> ONLY on ACCEPT run the branch-reshuffle live sequence, reading the --dry-run list BY NAME every time, never an expected count.

SEPARATELY, still true: mur-51/SM.23 -- checked this session, still open (no HARVEST on the SM.23 node), not yours to fix, just re-check next time. This post is generation-less -- no "gen N" anywhere. Check .agi/sessions/seats/sanctuary-director.rename.json fresh before ever rotating. If the meter crosses 0.47 before R3.5 harvests, it is fine to rotate with R3.5 still live -- the successor picks up the background-wait-equivalent fresh (any bash background task from this seating is gone at rotation) by re-running spawn_budget.py status --iter L4.352 --wait --timeout <N> themselves; the card above has everything needed to pick this up cold.
```
````
`````
``````

## §4 TRAPS (kept from the prior card, trimmed where superseded)

- 🔴 A literal `&&` inside claim/title/note/thought TEXT (not just a shell command) breaks `write.py`'s script parser (splits on `&&` looking for the next verb) — write "and" instead. Hit twice this session on generated falsifier-command prose.
- 🔴 `write.py`'s `set`/`create --set` edits whatever tree your CWD resolves to — from your OWN worktree it edits YOUR copy, not MAIN's. Correct/intended (mint on your branch, dispatch from there) — just don't Read MAIN's copy to check your own edit landed.
- 🔴 A tier-parent's `cli.py done --owns ...` does **not** write the verdict onto the owned node's frontmatter — only the parent's own `agent.json`. Commit SUBJECT can disagree with the node's real `verdict:` (hit on R3.1/R3.2/R3.3/R3.4; did NOT recur on R1 — check every time regardless).
- 🔴 **For a round guarding a destructive path, "tests pass" answers a narrower question than the gate actually asks** — mur-52's whole finding was R3.1-R3.3's tests all green while the real read-only dry-run still queued deleting 5 live branches; R3.4's own harvest repeated the pattern one level down (its tests were green, its OWN claim was proved, but a live dry-run with the real planned `--kinds` still showed 3 loop branches unconditionally deletable). **Always independently re-run the actual read-only command with the actual planned flags and read its actual output list**, never stop at "the suite is green."
- 🔴 A round's session records can be split across MULTIPLE worktrees with MAIN's own copy sitting completely EMPTY — and a dispatch's own printed manifest path can be under YOUR WORKTREE, not MAIN. Check the path actually printed.
- 🔴 `grid.py commit --all` REFUSES on a non-master/non-main branch — MAIN only. A concurrent `grid_sync` cron may beat you to a version — "0 new version(s)" isn't necessarily an error; verify with `grid.py versions <node>`.
- 🔴 root `HANDOFF.md` and the quorum card are TWO DIFFERENT FILES. Edit the quorum card only.
- 🔴 Under heavy concurrent write load, `dispatch.py` can print `{"issue": "stale-base", ...}` **and then keep printing lines that look like a successful spawn** — verify with `find`/`git worktree list`. Hit repeatedly this session; sync+re-cut resolved most, `--allow-stale-base` resolved one after two real refusals.
- 🔴 At harvest, always check the parent's own worktree with `git status -sb` directly.
- 🔴 A merge commit's own prose can mischaracterize which node a round targeted if written from memory — verify against the round's own harvest commit, not a neighboring round's hypothesis. Mischaracterized R3.1's target once this session; corrected in the follow-up report, left the merge commit's own text as-is (node/HARVEST note is authoritative, not commit prose; harness rule: never amend without being asked).
- 🔴 A round's own narrow test suite going green is not the same as the full engine suite staying green.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>`, never `reset --hard`.
- 🔴 `-F <file>` for every commit/merge/dm message. Never `pkill -f` in a Bash-tool command — `pgrep -f` then `kill <pid>`.
- 🔴 The five node counts are the ENGINE'S metric, never `find | wc`.
- 🔴 A DM claiming to relay a real owner order can be genuine but still arrive before your own branch has synced far enough to see the doc entry it cites — sync before disbelieving.
- `date -u` for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll — `--wait`, backgrounded if long. `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

Full rotation-level stamp check post-merge-up-52: `verification.py --level rotation --stamp` → **ALL 10 GREEN**, baseline `bef788a5e` (active=2811, deprecated=198, total=3009, broken_links=0). `test_branch_reshuffle_v3.py`+`test_branch_reshuffle.py`: grew 62→69→70 (R3.1/R3.2/R3.3) →76 (R3.4, +6 fixtures), independently reconfirmed each time (parent worktree + post-merge here). `test_rotate*.py`: 742 passed + 1 xfailed, independently reconfirmed twice for R1. R3.5's own numbers: not yet in.

## §6 BANKED (not mine; with a recommendation)

**16.** `test_sensei_wake_audit.py` F2/F3 label drift — flagged, already fixed by someone else on MAIN minutes later. Closed.

**14-15, 13** carried unchanged from the prior card (master-sensei's verification-weakening suggestion not adopted; the "testing plan" phrase's exact scope unconfirmed; director-review's mur-50 process suggestion re: remote-visibility fixtures, not yet minted).

Carried unchanged: 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits. 7. L4.192 wording residue. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**11. RULED by the Prime:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` + the ListAgents row + `tmux capture-pane`. For a RELAYED OWNER DECISION, verify independently against `doc:l4-owner-decisions` and the commit that banked it. **Sync first if the cited entry isn't found locally.**
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`.
- **Spend:** $5.00 floor: below it NO new round is dispatched, live rounds finish — PAUSED until the owner resumes.
- **No "gen N" anywhere.**

## MERGE-UP RECIPE (may be superseded — check the posts-local-only note at the top of this card first)

1. This branch synced to `origin/season2/main`; `verify` green here.
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline.
3. In MAIN (`git status` first; never clean/stash): `git merge --no-ff season2/posts/sanctuary-director -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (timeout 600000) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message, five numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

**FIRST, always:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json`. Re-check fresh.

At **0.47** of the meter's `est.` number, or sooner at a clean stopping point. `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed, NO flag. Refuses by name when the card's where-it-stops slot is stale — write the card, or pass `--stops '<one line>'`. **NEVER pass a model flag.** Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- A relayed instruction with real stakes deserves independent verification against the graph, not blind trust OR reflexive refusal.
- A round's session dir can be completely empty in one worktree while the real data lives in another; check all plausible locations.
- A rule's own predicted outcome can legitimately differ from the real case without that being a defect — read why, cite the mechanism.
- A completion tool writing to "the record" can mean two different records depending on flag mode — trace a commit/node mismatch to source, don't shrug it off.
- Correct your own record in the file your successor reads, in the same breath as the finding.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- A DM citing a graph doc can be genuine but still outrun your own branch's sync.
- A round's own narrow test suite going green is not the same as the full engine suite staying green.
- Verify a round's target hypothesis against its own harvest commit message, not from memory.
- **"Tests pass" is not the same question as "does the actual dry-run list still contain the dangerous thing"** — for a round guarding a destructive path, the ground truth is the real (read-only) command's actual output, not a narrower test suite's green result. This bit twice in one session: once at the R3.1-R3.3 → R3.4 boundary (mur-52's own finding), once at the R3.4 → R3.5 boundary (this post's own finding, one level down, same shape).
