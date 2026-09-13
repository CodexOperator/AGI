# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (session in progress, as of 18:32Z: mur-52 VERDICT IN — R3.1/R3.2/R3.3 all ACCEPTED WITH RESIDUE but `--apply`/`--delete-old` are **NO-GO**: a pre-existing bypass would delete 5 LIVE branches today, THIS post's own included. R1/L4.350 harvested. R3.4/L4.351 (the safety fix) DISPATCHED + LIVE. R3.5 next after that. See §0/§2/§3.)

🔴 **TREE:** this worktree = `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`** (upstream `origin/season2/posts/sanctuary-director`); **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. season2/main under heavy concurrent write load (multiple seats push every 10-30s) — **two stale-base refusals in a row hit this session dispatching R3.4**, both real (verified empty dirs), resolved with `--allow-stale-base` as the sanctioned third step; see §4.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY**, not what feeds rotate-self (`--prompt-file` points at THIS file). Edit the quorum card; leave the root file alone unless the user asks about it specifically.

🔴 **NAMING/TRACKING, owner order 16:4xZ, Prime ruling 16:5xZ (`doc:l4-owner-decisions`):** no post but the Prime tracks generations. Every non-prime post is a perpetual seat, identified by post name + timestamp. This card, dm lines, commit messages: timestamps/hashes for "when". Post renames land in SM.18's bundle — **do not rename anything here.**

## §0 STATE (live — updated as work lands)

**AUTHORITY:** owner speaks ONLY through the Prime (belam); every owner decision banked verbatim in `doc:l4-owner-decisions`. **New entry this session, highly relevant:** OWNER 18:2xZ GO'd the Prime to HAND-DELETE 10 **old-spelling legacy** origin branches (`seat/*` x4, `post/*` x3, `town/*` x2, `season/s2`) — each individually proved 0-ahead of season2/main first, done 18:30Z, origin heads 24->14. The doc entry is explicit: **"The engine `--delete-old` stays gated (R3.4/R3.5) for the v3 reshuffle itself."** Different branch set (old pre-v3 legacy names, fully merged already), different (manual, hand-verified) mechanism — does NOT change anything below; if anything it confirms this session's read is correct.

- **PRIME = belam** = live seat **agi-16** `[1b5b3b]`. Verified this session (`whois` IS-AUTHORIZED). 🔴 Unresolved anomaly carried from an earlier seating, not re-checked: a prior `ListAgents` once showed TWO `encryption-town` Remote Control rows distinct from `agi-16` — likely the owner running belam from more than one place.
- **Ids:** L4.347=R3.1, L4.348=R3.2, L4.349=R3.3 — merge-up-52 (`bef788a5e`), all ACCEPTED WITH RESIDUE by mur-52. L4.350=R1 — **harvested** (RUNG 4 closeout-gate fix, merged `8f9589eab`, inconclusive_lean_proved:90). **L4.351=R3.4 — LIVE** (parent `a00-c87d831d`, dispatched after two stale-base refusals + `--allow-stale-base`; real spawn verified). R3.5 not yet minted — next after R3.4 harvests, see §2.
- 🔴 **THE CRITICAL FINDING (belam XIX mur-52, 18:25Z) — read this before touching branch-reshuffle at all:** mur-52 (director-review) ACCEPTED R3.1/R3.2/R3.3 (each hole they claimed to close, independently reproduced) but ran the actual destructive-path check READ-ONLY against REAL origin (`cli.py branch-reshuffle --dry-run --delete-old --kinds post,town_main`) and found it queues UNCONDITIONAL deletes of 5 LIVE branches: `season2/posts/sanctuary-director` (**this post's own branch**), `season2/posts/sanctuary-helper`, `season2/posts/sensei-director`, and two town mains. Mechanism: `cli.py:4039 if not new: continue` (a job with no derivable rename target) skips the B2 upstream-check gate ENTIRELY — R3.1-R3.3 never reach this path, by construction, pre-existing since `20c460468`. **`--apply` and `--delete-old` are NO-GO until R3.4 (this bypass) and R3.5 (a new content/ancestry check, separately scoped) land and pass mur-53.** Full verbatim in git log / the R3.4 hypothesis node; do not paraphrase this from memory, re-read it if in doubt.
- **Tree:** synced repeatedly this session (clean each time, several incoming merges: someone else's sensei-F2/F3 fix `e2b354832`, the owner-decisions entry above, a spawn-budget doc tweak). Post branch tip `5e43b86ca` before R3.4's dispatch commit.
- 🔴 **mur-51 demoted L4.345** — unchanged this session, not re-checked: fix owner **SANCTUARY MASTER, round SM.23**. `demoted-pending-fix` on `585a9c963`. **Do not restart the reaper.**
- 🔴 **OWNER-ORDERED RENAME, check before EVERY rotate-self:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json` — not re-checked yet this session.

## §1 LANDED

**R3.1/L4.347 + R3.2/L4.348 + R3.3/L4.349** (full detail in the prior card / git log / each node's HARVEST note): all three harvested and merged this session as **merge-up-52** (`bef788a5e`), verified 10/10 green, pushed, reported to belam. mur-52 (18:25Z) reviewed all three: **ACCEPTED WITH RESIDUE** — each is a real, correctly-scoped fix for what it claimed, no demote-worthy defect — but see §0 for why that doesn't clear `--apply`/`--delete-old`.

**R1/L4.350 (RUNG 4 closeout gate, harvested this session):** mur-49 had found L4.335's earlier fix gated the WRONG functions (`_stops_push`/`_perform_season_merge`, a post's own rotate-self-only catch-up path) instead of `_make_closeout_seams`'s own `_merge_up`/`_push` (the real seam table driving MAIN merge-ups, confirmed zero `is_frozen` references). Re-cut the hypothesis in place with mur-49's own `prime_step` instructions (read the actual review JSON, not just the compressed node line). Dispatched, ONE kid did both halves (add the gate to the closeout seams, remove it from the rotate-self-only ones) plus a bonus third probe on a body residue; the PARENT itself ran independent probes against a REAL frozen `vetoes.md` (not monkeypatched) for all three conjuncts — genuinely strong single-kid rigor. Independently reverified: full diff read (exact match to spec, minimal), falsifier command run myself (now 3, was 0), `test_rotate*.py` run myself twice (742 passed, 1 xfailed both times), live `is_frozen` invariant reconfirmed False. Merged `8f9589eab`, HARVEST note written+pushed. **This touches every post's own rotate-self mechanics, mine included — worth its own mur before reaching MAIN, same discipline as the branch-reshuffle work, not lower-stakes just because it's a different file.**

**mur-52's critical finding + R3.4 minted (this session):** see §0. Read the actual mechanism in `cli.py` myself (lines ~3990-4057 for the B2 gate loop, ~3555-3594 for the R3.1 residue site) before minting, rather than paraphrasing belam's DM — confirmed the exact line numbers, confirmed `_stops_push`/`_perform_season_merge` residues belam named. Minted `hypothesis:l4-delete-old-new-is-none-arm-bypasses-b2-and-would-delete-five-live-branches` (parents `goal:g15` + R3.3's hypothesis), folding in BOTH bundled residues (R3.1's abort-vs-collect, R3.2's refs/grid status-print position) per belam's exact instruction. Dispatched as L4.351 after two real stale-base refusals (verified empty, cleaned, re-synced each time) using `--allow-stale-base` as the sanctioned third step.

## §2 LIVE + QUEUE

**LIVE: R3.4 = L4.351 (`a00-c87d831d`), tier=parent.** Just dispatched. Background wait armed (`bi19zdk5r`, 1800s). **This is safety-critical — read the node's own claim in full at harvest, do not skim.** The live invariant is non-negotiable: `--delete-old` must NEVER be run for real against live origin during this round, only `--dry-run` / disposable `tmp_path` fixtures. At harvest: check the parent's worktree `git status -sb` directly, read the node's real frontmatter verdict, independently re-run the falsifier / new fixtures / `test_branch_reshuffle*.py`, AND independently re-run a **read-only** `--dry-run --delete-old --kinds post,town_main` against the merged tree to confirm the 5 named branches (or their fixture equivalents) are no longer queued for unconditional deletion — this is the one round this session where "the tests pass" is not enough; the actual dry-run list is the ground truth belam used to catch the hole in the first place.

**QUEUE after R3.4 harvests:**
1. Mint **R3.5** — belam's spec (verbatim, from the mur-52 DM): "`--delete-old` requires CONTENT containment: every job's tip must be an ancestor of its successor or of the trunk (`git merge-base --is-ancestor`), refused by name otherwise (new mechanism — scope it as its own claim)." Parent from `goal:g15` + R3.4's hypothesis (extends the now-unified gate R3.4 builds). **Do NOT dispatch R3.5 in parallel with R3.4** — same file region, serialize (harvest R3.4 first, mint+dispatch R3.5 against the post-R3.4 tree).
2. **ONE merge-up, numbered 53**, carrying R3.4 + R3.5 together (mirrors the merge-up-52 pattern for R3.1-3.3).
3. Window ask to belam with numbers.
4. Belam's verify.
5. **mur-53 by name.**
6. **Only on mur-53 ACCEPT** does the branch-reshuffle live sequence become live-eligible: `--dry-run --kinds towns,posts,loops` (never `main`) -> `--apply` -> suite green -> `--delete-old` -> cell re-spellings (Prime applies) -> `verify` -> commit. **Read the `--dry-run` list BY NAME before any real run** (belam's own note: the Prime's "10 old branches" count from the manual cleanup does NOT match the engine's own derived delete-set count — 13 jobs under default kinds, 17 with main+loop — never trust an expected count over the actual printed list).

**R2/R4/R5/R6** still need a **separate signed GO** from belam beyond the original window grant — not yet asked, unrelated to R3.4/R3.5.

**Sources for R1/R2/R4/R5/R6** (R1 done; unchanged for the rest): mur-49 review JSON (`/home/ubuntu/work/agi/.agi/sessions/reviews/mur-49.review.json`, MAIN only, gitignored — read the relevant node body first). Keys L4.335 (R1, done), L4.337 (R5), L4.338 (R4, R6).

**GRAMMAR (still correct — do not re-derive):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (max 2 parents; **no literal `&&` anywhere in claim/title/note/thought text** — it splits the write.py script into a bogus second verb call, hit this exact trap once this session on a falsifier command containing `cd x && sed ...`; write "and" or restructure instead). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; `stale-base` = sync + `find .agi/sessions/iter-L4.NNN -type d -empty -delete` + re-cut SAME id; 2 refusals in a row is normal under contention — `--allow-stale-base "<reason>"` is the sanctioned third step; VERIFY via `find .agi/sessions/iter-L4.NNN` + `git worktree list`, never the printed lines). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` backgrounded. harvest = diff vs merge-base → review the bytes AND the node content directly → check the parent's worktree `git status -sb` directly → merge `--no-ff -F file` → re-run touched suites here → real-tree proof (read-only/dry-run only for a destructive-path round) → `write.py <node> "note HARVEST L4.NNN (sanctuary-director, <ts>): …"` → commit + push.

## §3 🔴 NEXT COMMAND

``````
`````
````
```
R3.4 = L4.351 (a00-c87d831d) is LIVE, dispatched after two real stale-base refusals resolved with --allow-stale-base. Background wait armed (bi19zdk5r, 1800s) -- wait for the notification, do not hand-poll. When the parent is done:
  1. Check the parent's own worktree git status -sb directly (never the manifest/a DM alone).
  2. Read the owned node's real frontmatter verdict (not the commit subject -- this trap has hit on R3.1, R3.2, and R3.3 so far; check again here).
  3. Read the full rotate.py-equivalent diff yourself (this one is cli.py's --delete-old B2 gate + the two residue sites) -- confirm it matches hypothesis:l4-delete-old-new-is-none-arm-bypasses-b2-and-would-delete-five-live-branches's claim: the new-is-None arm now gates on origin-presence of the derived v3 successor; _stops_push/_perform_season_merge's abort-vs-collect residue fixed; the refs/grid status-print position residue fixed.
  4. Independently rerun the new fixtures + test_branch_reshuffle*.py + test_branch_reshuffle_v3.py yourself.
  5. THE CRITICAL CHECK, do not skip it: independently run a READ-ONLY `cli.py branch-reshuffle --dry-run --delete-old --kinds post,town_main` against the merged tree and confirm season2/posts/sanctuary-director (and the other 4 named branches) are NO LONGER queued for unconditional deletion, while a genuinely-migrated branch's dry-run line is unchanged. NEVER run --delete-old for real.
  6. Merge, re-run suites here, write the HARVEST note, commit+push, per the §2 GRAMMAR block.

THEN: mint R3.5 (belam's exact spec is in §2 QUEUE item 1 -- ancestor/merge-base content-containment check, its own claim, parented off R3.4's hypothesis + goal:g15). Dispatch it the same way (sync, cut, verify real spawn, background wait). Do NOT dispatch R3.5 in parallel with anything else touching cli.py's branch-reshuffle region.

THEN merge-up-53 (R3.4+R3.5 together) -> window ask to belam with numbers -> belam's verify -> mur-53 by name -> ONLY on ACCEPT run the branch-reshuffle live sequence from §2 QUEUE item 6, reading the --dry-run list BY NAME every time, never an expected count.

SEPARATELY, still true, unchanged: mur-51/SM.23 (§0) is not yours to fix, just check if landed. This post is generation-less -- no "gen N" anywhere. Check .agi/sessions/seats/sanctuary-director.rename.json fresh before ever rotating. The meter crossed the 55% warning band this session (0.31 of the window vs 0.47 threshold, i.e. ~0.66 of the line) -- not yet at the rotation threshold, but getting closer; keep this card current as R3.4 lands so a rotation, if it comes before R3.5 is minted, is one clean call.
```
````
`````
``````

## §4 TRAPS (kept from the prior card, trimmed where superseded; two new ones added this session)

- 🔴 **NEW this session:** a literal `&&` inside claim/title/note/thought TEXT (not just in a shell command you're constructing) breaks `write.py`'s script parser — it splits on `&&` to find the NEXT verb call, so a falsifier command like `cd x && sed -n ...` embedded in prose becomes `no verb 'sed'`. Write "and", or restructure the command to avoid the literal token, before ever passing long generated text to `write.py`.
- 🔴 **NEW this session:** `write.py`'s `set`/`create --set` operates on whatever tree your CWD resolves to as the project root — running it from your OWN worktree edits YOUR tree's node copy, not MAIN's. Obvious in hindsight, cost one confused Read of the wrong file before checking `git status -sb` in the right place. This is actually correct/intended (mint on your own branch, then dispatch from there) — just don't Read MAIN's copy to check your own edit landed.
- 🔴 A tier-parent's `cli.py done --owns <kid-node-id> --verdict X ...` does **not** write `X` onto the owned node's frontmatter — only into the parent's own `agent.json`. Commit SUBJECT and a kid's self-reported DM can disagree with the node's real `verdict:` (hit on R3.1/R3.2/R3.3; did NOT recur on R1 — the commit subject matched the node that time, so don't assume it's guaranteed to mismatch, just always check). **The node file's frontmatter is authoritative.**
- 🔴 A round's session records can be split across MULTIPLE worktrees with MAIN's own `.agi/sessions/iter-L4.NNN` copy sitting completely EMPTY — and a dispatch's OWN printed manifest path can be under YOUR WORKTREE, not MAIN, even though the command was run "from" a path that looks like it should resolve to MAIN. Check the path dispatch.py itself prints, not an assumed location.
- 🔴 `grid.py commit --all` REFUSES on a non-master/non-main branch — MAIN only. A concurrent `grid_sync` cron may beat you to a version — "0 new version(s)" is not necessarily an error; verify with `grid.py versions <node>` before assuming something's wrong.
- 🔴 root `HANDOFF.md` and `.agi/sessions/quorum/sanctuary-director.md` are TWO DIFFERENT FILES. Edit the quorum card only.
- 🔴 Under heavy concurrent write load, `dispatch.py` can print `{"issue": "stale-base", ...}` **and then keep printing lines that look like a successful spawn** — verify with `find .agi/sessions/iter-L4.NNN` or `git worktree list`, never the printed lines alone. Hit this TWICE in a row this session dispatching R3.4; both were real, both resolved by sync+re-cut, third attempt used `--allow-stale-base`.
- 🔴 At harvest, always check the parent's own worktree with `git status -sb` directly — the manifest/wait-tool summary can be stale.
- 🔴 A merge commit's own prose can mischaracterize which node a round actually targeted if written from memory/inference — verify against the round's own harvest commit (`git log --grep`), not a neighboring round's hypothesis. Mischaracterized R3.1's target once this session, corrected in the follow-up report; the merge commit's own text was left wrong (harness rule: never amend without being asked; this project's convention: the node/HARVEST note is authoritative, not commit prose).
- 🔴 A round's own narrow test suite going green is not the same as the full engine suite staying green — run the full `verify-suite` before closing a merge-up window.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>` + per-file restore, never `reset --hard`.
- 🔴 `-F <file>` for every commit/merge/dm message. Never `pkill -f` in a Bash-tool command (kills that command) — `pgrep -f` then `kill <pid>`.
- 🔴 The five node counts are the ENGINE'S metric (`metrics.node_lifecycle_stats`), never `find | wc`.
- 🔴 A DM claiming to relay a real owner order can be genuine but still arrive before your own branch has synced far enough to see the doc entry it cites — sync before concluding a citation is missing/false.
- `date -u` for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo (mints a REAL key). Never hand-poll `spawn_budget.py status` — `--wait`, backgrounded if long. `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

`commands.py run verify-suite`, run twice this session pre-merge-up-52: first pass 3 failed/4711 passed/15 skipped; second pass (after a comment-fix) 1 failed/4713 passed/15 skipped (the survivor confirmed pre-existing on MAIN, since fixed by someone else). Full rotation-level stamp check post-merge-up-52: `verification.py --level rotation --stamp` -> **ALL 10 GREEN**, baseline `bef788a5e` (active=2811, deprecated=198, total=3009, broken_links=0). `test_branch_reshuffle_v3.py`+`test_branch_reshuffle.py`: 70 passed (grew from 62->69->70 across R3.1/R3.2/R3.3), independently reconfirmed by mur-52 too (40+30+3=73 across three files including the spelling-grep test). `test_rotate*.py`: 742 passed + 1 xfailed, independently reconfirmed twice for R1 (parent worktree + post-merge here). R3.4's own numbers: not yet in, see §2/§3.

## §6 BANKED (not mine; with a recommendation)

**16.** `test_sensei_wake_audit.py` F2/F3 label drift — flagged to belam mid-session, **already fixed by someone else on MAIN** (`e2b354832`) minutes later. Confirms flagging-not-fixing was the right call for an out-of-domain finding. No longer open.

**14. master-sensei's suggested STANDING RULES weakening, not adopted.** Drop ListAgents+tmux from Prime-identity verification, keep only signed `whois`? Left as-is. Whoever owns this policy (belam or the owner directly) makes the call explicitly.

**15. the "testing plan" phrase.** AUTHORITY cites owner-confirmed "proceed with testing plan as is" — ambiguous scope. Not blocking. Worth confirming if it recurs.

**13. director-review's mur-50 process suggestion (still not minted):** "resumability claims should require a remote-visibility fixture (ls-remote), not a local-ref-only comparison." Not urgent. Belam or master-sensei's call.

Carried unchanged from the prior card: 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators — never `--fix` blind. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits. 7. L4.192 wording residue. 8-9. old dirty-worktree/junk-record cleanup. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**11. RULED by the Prime 07:28Z:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; the nodes hold the reasoning — unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` (exit 0) + the ListAgents row + `tmux capture-pane` — all three, even for a message announcing itself as the new Prime. For a specific RELAYED OWNER DECISION, the stronger check is independent verification against `doc:l4-owner-decisions` and the commit that banked it. **Sync first if the cited entry isn't found locally.**
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent, the parent merges every kid branch before `done:`. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`. · **AskUserQuestion / any tool that waits for a human — decide under delegated authority where it is genuinely operational; a decision that would spend real money or touch shared state and that you cannot verify independently is still worth surfacing plainly rather than either blind compliance or silent refusal.**
- **Spend:** $5.00 floor (`config.json` `provisioning.min_account_remaining_usd = 5.0`): below it NO new round is dispatched, live rounds finish, NO Sonnet parents/kids fallback — PAUSED until the owner resumes; report the pause; never auto-switch to any Claude fallback; never mint/revoke a key.
- **No "gen N" anywhere:** this post is generation-less on every human/model-readable surface. Timestamps and commit hashes carry "when".

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
- **A completion tool writing to "the record" can mean two different records** depending on which flag mode it ran under — a label mismatch between a commit subject and a node's frontmatter is worth tracing to source once, not shrugging off. (Confirmed on R3.1/R3.2/R3.3; did NOT recur on R1 — check every time regardless, but don't assume it's inevitable either.)
- Correct your own record in the file your successor reads, in the same breath as the finding.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- A DM citing a graph doc can be genuine but still outrun your own branch's sync — sync before disbelieving.
- **A round's own narrow test suite going green is not the same as the full engine suite staying green** — run the full `verify-suite` before closing a merge-up window.
- **Verify a round's target hypothesis against its own harvest commit message, not from memory or a neighboring round's target.**
- **"Tests pass" is not the same question as "does the actual dry-run list still contain the dangerous thing"** — mur-52's whole finding was that R3.1-R3.3's tests all passed while the real destructive-path check, run read-only against real origin, still queued deleting five live branches. For any round guarding a destructive path, the ground-truth check is running the real (read-only) command and reading its actual output list, not trusting green tests for a narrower claim than the gate question actually asks.
