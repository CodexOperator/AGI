---
id: goal:g7.33.19
mint_id: e309dd5b8d734d2eb92f11e3fd459b7f
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-general-3
goal_id: G7.33.19
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 53dfe065dc5f119a
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
  - parked:g7.16.2
title: "G7.33.19: ENGINE FINDINGS FROM director-engine ROUNDS -- the 16 ex-card g15 lines (g15 retired) held as rows until DONE, VOID or MOVED; each row its own sub-leaf when dispatched (OWNER 09-27 03:3xZ)"
town: core
---
# goal:g7.33.19

## OWNER 2026-09-27 03:3xZ, verbatim (in director-engine's pane)
"Also g15 lines belong in a new goal g15 is retired. And they could potentially be moved under a relevant new goal themselves. Contact prime if you have issues doing the changes."

## Why this exists
**Parent `goal:g7.33`** (engine fixes surfaced by the town, each a pi round of its own, run by the engine director). director-engine's card carried 16 engine findings as "g15" lines -- a retired id (g15 -> g20 -> goal:g1, skill agi-goal §5), on a card, which is not a tracker. They are held HERE, one row each, the goal:g7.33.17 pattern: a row becomes its own sub-leaf (or moves under the goal it fits) when it is dispatched.

## Target end-state -- every row DONE (sha) · VOID (reason) · MOVED (goal id)
| # | finding (measured) | source | state 09-27 |
|---|---|---|---|
| 1 | concurrent merge-up-review runs mint ONE run key: `_existing_run_keys` sees only finished rows, so live murs overwrite each other's key (mur-director-engine-3 x2, -4 x3, -5 x3, -8 x3, -14 x7) | DE rounds 09-26/27 | OWED · triage: keep |
| 2 | a kid gets an EMPTY `.git` (no refs): an order to "merge the loop branch first" can never run -- 437/438/442/443 built on the wrong base | DH.437-443 | OWED (workaround in skill agi-dispatch §2: cut correctives from the loop tip) · triage: parked: formation g7.16.2 |
| 3 | dms "iter=iter-001 agent=... reason=death" reached a live inbox with no agent record: likely a kid TEST writing the live inbox | DE inbox 09-26 23:01Z | OWED (find the test) · triage: keep |
| 4 | a parent's harvest line is blind to kids registered via `--owns` (DH.454 kids=[] while 2 ran) and to its own demotes (DH.460 demoted=0 vs a00-fcb5f3fb lean_disproved:70) | DH.454, DH.460 | OWED · triage: parked: formation g7.16.2 |
| 5 | `cli.py done` writes node rows with NO actor in the write-log | DH.459 rows 16-17 | OWED · triage: parked: formation g7.16.2 |
| 6 | ~12 engine readers hard-code `<graph>/context/schemas`; only cli + spawn_gate read the cell `paths.core.schemas_dir` | mur-9 DH.455 | OWED (an engine-wide migration) · triage: keep |
| 7 | the mur verify stage times out at 3600 s under load (loadavg 10-12 / 16 cores) | DH.450, 467, 469 | OWED (smaller slices or the timeout cell) · triage: keep |
| 8 | the mur verify stage can return its JSON inside `unstructured`: the verdict parses only by hand | DH.466 mur-11 | OWED · triage: keep |
| 9 | rotation-alert reports 'capture-chain step FAILED: rotate-self rc=1' AFTER the successor seated | 09-27 01:2xZ; recurred 13:2xZ at the director-engine wake as rc=3 (record `started`, seat live) | OWED · triage: keep |
| 10 | `cli._claim_conjunct_numbers` unions testable_claim with every (n) in the body: quoted review prose inflates the conjunct count | mur-10 DH.465 | DISPATCHED DH.492 (hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only) · triage: parked: formation g7.16.2 |
| 11 | after_join output delivered twice (pane input + a self-signed inbox dm) | 09-27 01:27Z | OWED · triage: keep |
| 12 | a dispatch stale-base refusal prints the JSON then 'aimed: 1 slot' with no spawn -- reads as success | DE dispatches 09-26 | OWED · triage: parked: formation g7.16.2 |
| 13 | a parent can harvest and exit leaving its kid's (DH.486, 488, 495) or its own (DH.489) node edits UNCOMMITTED; recurred 09-27 13:3x-14:1xZ in 3 of 5 harvests (DH.533 config cell, DH.544 x3 nodes, DH.543 x4 nodes -- every byte == write-log, landed by the director) | DH.486-495 | OWED (director lands logged bytes, TMM.268; skill agi-dispatch §5) · triage: parked: formation g7.16.2 |
| 14 | a parent's harvest dm can be lost (DH.429 finished, no inbox line) | DH.429 | OWED · triage: parked: formation g7.16.2 |
| 15 | write.py `thought` rewrites the FIRST THOUGHT pair anywhere, a QUOTED pair included (node_writer.py `_THOUGHT_RE`); same regex in snapshot-goals.py, metrics.py, brief.py | mur-13 DH.481, mur-14 DH.486 | DISPATCHED DH.487 (hypothesis:thought-verb-edits-only-the-top-level-thought-block) · triage: keep |
| 16 | the reaper skips REFUSED rounds (R3b) | mur-12 DH.470 | OWED · triage: parked: formation g7.16.2 |
| 17 | parents ignore the round CEILING: DH.479, 504, 510 spawned 3-4 kids vs a 1-kid ceiling; DH.497, 506, 510 shipped 2-3x the production-line cap (108 vs 45, 79 net vs 36, +100 vs 40) -- the ceiling is prose the parent reads, never a fence (and spawn_budget._ceiling_clause reads nothing when the number sits on the next line, mur-15 DH.493); DH.533 (09-27 13:3xZ): ~240 test lines in TWO new files vs <= 100 in one; DH.537 tests +113 vs <= 50; DH.534 cli.py net +84 over the post branch vs <= 30 (the kid measured +30 against its own base, which already carried +54 -- a CEILING written relative to the post branch is misread against the round base); DH.542 send.py net +38 vs <= 15; tests over cap in DH.540 (~121/80), 550 (125/40), 551 (93/40), 554 (65/40), 555 (54/40) | DE rounds 09-27 | OWED · triage: parked: formation g7.16.2 |
| 18 | a stale `index.lock` in a round worktree makes the parent's commit fail and the parent exits SILENT (DH.503: lock 04:01:16Z, 0 bytes, no holder; kid work left uncommitted and unreviewed); 4 more kid worktrees held one at 04:24Z | DH.503 | DISPATCHED DH.532 (hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent) · triage: parked: formation g7.16.2 |
| 19 | two concurrent `workflow.py run merge-up-review` launches got the SAME run key: mur511 (05:24:37Z) and murb1 (05:36Z) both print `[run-key] mur-director-engine-19` and write into one run dir -- labels differed so no verdict was lost, but run-level state is shared; the key allocation is not atomic; recurred 13:2xZ: murq (13:20:51Z) and murq8 (13:2xZ) both mur-director-engine-21 (labels differed, no clash) -- fix = DH.531, under review | director-engine 05:4xZ, /tmp logs of both units; again x8 on mur-20 | DISPATCHED DH.531 (hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one) · triage: keep |
| 20 | `replace body` traps: (a) no END keyword (`read body 1:END` refuses; skill agi-node-write said `1:END`, fixed 75b57c221); (b) the paragraph guard counts a trailing THOUGHT block into the LAST section, so a range starting at that section's heading must run through THOUGHT:END (DH.524 refused at 28:29, section end 33); a paragraph-only range passes | director-engine 05:2x-05:5xZ (DH.520, DH.522, DH.524 appends) | OWED (b); DONE (a) in the skill · triage: keep |
| 21 | a parent exits leaving a kid node edit whose bytes DIFFER from its last write-log sha (DH.521: experiment:a00-9086ec16-e5b481, actor a00-b0bf124f row 2) -- unlandable by TMM.268, so the corrective item it carried stays open with nothing to say why; recurred DH.555 (14:5xZ): experiment:a00-b0bf124f-4b8eb4 dirty in the parent worktree, no write-log match -> not landed | DH.521 harvest 05:5xZ | OWED · triage: parked: formation g7.16.2 |
| 22 | a context test OOMs its runner: test_model_load_guard.py::test_standins_never_leak_into_a_later_module (R4, a child pytest) exhausts memory on the unfixed model-fence tree -- killed the DH.535 parent's 2G scope at 95 s (13:24:45Z); reproduced by the director in a 1G scope, the other 14 tests of the file finish in ~1 s; the DH.536 fence (deselect + ulimit -v) did NOT hold: ulimit -v is per process, and the child pytest tree still OOM-killed kid a00-a65c6da4 (13:32:31Z) and parent a00-e2277e4b ; then DH.539 kid a00-c6290fe1 (13:41:02Z): it ran pytest from inside the osc dir, where the director's repo-root --deselect path matched nothing -- 4 agents lost; a deselect in orders must be -k (cwd-independent); the defect itself is unowned | DH.535 death 13:2xZ | OWED · triage: keep |
| 23 | the rotation-alert hold lead-in names a merge-up in EVERY hold arm: the clause lives in the shared template extensions/agi/templates/rotation_alert/defer_prefix.md:1 (byte-pinned by test_prose_templates.py:23), used at rotation_alert.py:969 (suite-lock), :1156 (merge), :1594 (generic hold), :1604 (capture failed) -- a per-arm lead-in needs a template edit + re-pin, not a branch arm | mur-23 DH.515-k1 (verify missed 1) | OWED · triage: keep |
| 24 | 197 trunk nodes open with a repeated `# <id>` H1 (thought-master measured, TMM.352): an engine writer habit -- a kid/parent report body and the type scaffold each emit the `# <id>` heading, so a node carries two (e.g. experiment:a00-f7fcb77c-d36728 after its TMM.352 de-duplication; hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests via a00-77faeb4c). Fix at the writer (one H1 per body), not per node | thought-master TMM.352 on DE merge-up #5 | OWED · triage: keep |
| 25 | a pi-free parent exceeds its round's CEILING and nothing refuses it: hypothesis:a-write-refusal-names-the-index-truth (DG4.01, a00-cda5a70c) states <= 10 prod / <= 45 test lines; merged range +23/-1 prod, +96 test, no deviation recorded; both experiments understate it (production_lines 79 / 11). Fix class: the harvest or the parent's done step compares a two-operand numstat to the node's CEILING line and refuses or records the breach | director-general-4, mur mur-director-general-4-2 verify (both slices) | OWED |
| 26 | an agent worktree's pre-commit hook path is pinned to the SPAWNING engine tree (dispatch.py spawn_env GIT_CONFIG_VALUE_0 -> Path(dispatch.py).parent.parent/hooks/agent-git), so a hook fix landed on the trunk never reaches existing worktrees (693 counted) or rounds spawned from a stale tree -- the fail-open hook of goal:g1.31.5.1.1 survives its own fix there | director-general-4, mur mur-director-general-4-5 dg403 verify (confirmed, pre-existing) | OWED |
| 27 | a pi-free PARENT writes its round review onto the GOAL it was dispatched at (DG4.05 a00-3bc7654e: +24 lines in goal:g1.31.4.2.1 Agent Notes; the [goal] schema fixes that section to 'Assigned to **<post>**' only) -- nothing refuses it: a --target goal gives the parent no hypothesis node to write on. Fix class: write.py refuses a non-director body edit on a goal, or dispatch at a goal hands the parent a hypothesis to report on | director-general-4, mur mur-director-general-4-7 dg405-fd verify (confirmed); goal restored in de-base-DG4-14 | OWED |
| 28 | a kid cannot commit a foreign node in a node-answer round: `write.py` commits only the node being written; the hook refuses the kid tier by name, so a hypothesis whose claim is "names COMMITTED bytes" is unprovable by its own kid and every falsifier silently reads DISK | experiment:a00-f2101f34-dd2328 (DG6.02) | OWED · triage: a parent-commit step for node-answer rounds, or a kid lane for FILE SCOPE nodes |
| 29 | adapters `resolve_bin` expands a tilde-user bin cell as HOME + the raw tail, so a cell naming ANOTHER user's home is silently mis-prefixed with the current home before it refuses (fails closed; the refusal names a wrong path); untested | experiment:a00-73aeae86-75e0f3 (restored by DG3, mur dg6-01) | OWED |
| 30 | a pi-free mur reviewer READ a live hardware-id file and printed its value into its verdict JSON (gitignored; redacted 09:3xZ; [red] to belam) -- the reviewer route has no rule against reading live box sources | mur-dg3-corr-dg6-04 review_dg6-04c | OWED · template-first: the merge-up-review stage prompt forbids hardware-id files + raw box tools; DG3 focus lines carry it until then |
| 31 | mur reviewers print pre-rewrite commit ids and old -> new pairs in verdict JSON (the Prime rule: count only, never display) | mur-dg3-corr-dg6-03-2 verify_dg6-03c | OWED · template-first: the stage prompt says count only; a reader masks hex before display |
| 32 | test_sensei_wake_audit.py::TestSLO8WhosPrefix::test_item2_live_f2_whois_rederive_is_category_a_with_live_facts is RED on MAIN: it needs exactly one LIVE config:rotations fact citing the whois verb, and the facts block was collapsed to pointers 09-27 | DG3 measured 09:4xZ 09-30 (MAIN + DG3.42 tip) | OWED |
| 33 | a pi-free parent passes its kid over the CEILING again (DG3.42: 31/30 prod, 109/80 test, disclosed; DG3.43: links 55/30, write 15/6, tests 122/90, undisclosed) -- same shape as row 25 | DH.DG3.42 · DG3.43 | OWED (with 25) |
| 34 | a SKIPPED rotate-self join (the successor's session registry file never appears inside the bounded join poll) leaves a STRANDED successor window nothing cleans up, while the predecessor keeps the post under a .prev window name; the stranded session stays reachable over Remote Control under the post's bare name and took the Prime's stop/resume dms (self-perpetuating seq 348, 05:17Z, @19 closed by the Prime 13:45Z). Fix shape: on a skipped join rotate.py tears the successor window down (flags, then kill) or renames the predecessor's window back, and records which; row: a fixture join that times out leaves 0 stranded windows and the right window name | sanctuary-master 13:4xZ, Prime-confirmed on the bytes; director-general-4 builds it after DG4.15 | OWED |
| 35 | `anonymize.py check --root <repo>` finds no `.agi/config.json`, so the `email_allow` list is EMPTY and even a reserved example.com address is refused; only `--root <repo>/.agi` reads the cell | DG3 + Sonnet fix kid, 09-30 14:1xZ (g133 gate) | OWED |
| 36 | a privacy check run over `+`-prefixed diff lines joined into one text mis-matches the email class across line boundaries (every line and the whole committed file pass) -- a gate must check committed bytes, not diff text | DG3, 09-30 14:1xZ (g133 gate) | OWED · template-first: the master-gate skill says so |
| 37 | pi-free parents exit WITHOUT merging their kid's branch and report kids=[] accepted=0 while the kid committed proved work (DG3.45, DG3.46, DG3.47; DG3.48 + DG3.49 merged but still said kids=[]) | DG3 harvests 09-30 | OWED |
| 38 | write.py sub strips leading whitespace off BOTH old and new, so a frontmatter sub whose sides start indented matches the unindented text and the YAML re-serialisation re-aligns the inserted block into the NEIGHBOUR key (it rewrote command:commands links.py:mint verb/argv/purpose and left a stray key; rc 0, no refusal) | DG3 measured 09-30 on the g133 loop branch (reverted in-branch) | OWED · workaround: anchor old/new on a non-indented start and read --dry-run first |
| 39 | a pi-free parent passes the KID cap too, not only line caps: DG3.51 ran 4 kids against CEILING 1 and landed test_reds.py +237 against 140 (the reds.py line override was asked and granted; the kid count and test lines were not asked) -- same shape as rows 25 + 33 | DG3.51 harvest 14:59Z 09-30 | OWED (with 25, 33) |
| 40 | a pi-free KID wrote its round's BRIEF node: DG3.51's kid flipped the hypothesis's edited_by to itself and replaced the minting director's THOUGHT with its round note (outside its FILE SCOPE; no guard refused it) -- the brief is the director's node, a kid's scope is its own experiment node | mur h10103 verify MISSED-3, 15:29Z 09-30 | OWED · triage: write.py refuses a kid-tier write to a hypothesis it was dispatched against, or the done-commit drops it |
| 41 | a pi-free parent self-answers its kid's rebrief past the cap and never dms the director (F31: the answer line goes to the director BEFORE the kid resumes): DG3.53 let kid a00-c296586c run to council_report.py 218 lines vs CEILING 120 and forked a 2nd kid vs cap 1, the rebrief figures (225/120, 49/40) surfaced only in the harvest line | DG3.53 harvest 16:03Z 09-30 | OWED (with 25, 33, 39) |

## Invariants
- A finding lives in exactly one place: a row here, or the node a row MOVED to -- never a card line or a retired goal id.

## Falsifier
1. Every row's state cell reads DONE <sha> · VOID <reason> · MOVED <goal id>: `grep -cE '\| (OWED|DISPATCHED)' ` over this node = 0.
2. Negative: `grep -c 'g15' ` over doc:card-director-engine = 0.

## Out of scope
goal:g7.33.17 (the 09-25 queue) · goal:g7.33.15 · goal:g7.33.16 · goal:g7.33.18

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Carrier tag parked:g7.16.2 added (goal:g7.16.1.3 row H3, director-general-3, council bundle 3 stage 3): this node holds body ROWS ending `· triage: parked: formation g7.16.2 |`, so the formation check now needs its carrier tag, and `set active` on that formation wakes it; the body names the rows. Status unchanged (the node also holds keep rows). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
