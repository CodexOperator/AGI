---
id: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
mint_id: 812b7aa1f51f4fb881bc9a69df812b74
type: hypothesis
parents:
  - goal:g7.32.6
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 6fcee7280f2effca
season: 2
tags:
  - engine
  - send
  - boxes
testable_claim: "(1) seating writes the row box cell from AGI_BOX (2) this_box refuses an unset AGI_BOX and an empty or unknown row box is never local (3) the foreign-row refusal prints once per row+cause, names the box, and sends no keys (assigned: director-engine)"
title: "every live row carries its own box from AGI_BOX; an unset or unknown box is refused on every box, once per row+cause (send-is-hub-only, belam 00:35Z; assigned: director-engine)"
town: core
---
# hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused

## OWNER, verbatim (on the parent goal)
21:0xZ 09-26: "Can we not have the local box name be a global env variable that gets set as part of the ini routine somehow? Like the box label in the network or something. Then just check that."
belam 00:35Z 09-27 on the owner's go: done = (1) every live row carries its own box, written at seating from AGI_BOX (2) empty/unknown box refused on EVERY box, once per row+cause, naming the box (3) no send-keys into such a row's window.

## Measured
- extensions/agi/bin/boxes.py:153 `this_box` = AGI_BOX from the env, else the .env file, else the posts node's `default_box` (= core-town on this graph): an unset AGI_BOX silently becomes core-town.
- boxes.py:168 `row_is_local`: a row with NO box cell takes `default_box` (core-town), so on local-town every such row is FOREIGN; send.py:2198 refuses it as a nudge target, printing 'box (default)', on every sweep (belam 00:35Z: 6 rows).
- No seating path is known to write the row's `box` cell from AGI_BOX (the kid measures the seat-row writer and names it file:line before any code).

## CLAIM
(1) seating writes the row's own `box` cell from AGI_BOX (the one seat-row writer), so a newly seated live row always carries it (2) `this_box` REFUSES when AGI_BOX is unset (no silent default) and `row_is_local` treats an empty or unknown row box as NOT local on every box -- '(default)' is never a match (3) send.py's foreign-row refusal is printed ONCE per row+cause (not every sweep), names the box, and sends no keys into that row's window.

## Dispatch line
config-max: the box label is env AGI_BOX (set by the box init, never a config literal); default_box stays only as the posts node's documentation, never a locality fallback. template-max: none. code: the seat-row writer, boxes.py's two readers, the refusal's once-only memo.

## FALSIFIERS
- a temp graph with AGI_BOX unset: `this_box` returns any value instead of refusing.
- a row with box '' or an unknown label is local on some box.
- two sweeps over one foreign row print the refusal twice, or any send-keys reaches its window.
- a fresh seat on a temp graph leaves the row without `box`.

## TESTS
extensions/agi/tests/test_box_identity.py (new; temp graphs, monkeypatched env, a fake tmux runner -- never the live pane). Neighbourhood (send): test_send.py test_seatsig.py test_heal.py test_bin_help_smoke.py test_write_self_row.py. Every pytest under `timeout 600`, --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/bin/boxes.py · the ONE seat-row writer (named by the kid, file:line) · extensions/agi/bin/send.py (the foreign refusal at ~2198 only) · extensions/agi/tests/test_box_identity.py.

## CEILING
2 kids · <= 50 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude; never the live .env.

## CORRECTIVE DH.525 -- closes mur-director-engine-17 DH.498-k1 + k2 (verify: accept_with_residue, NOT_MET conjuncts (2b) and (3))
BASE      CUT FROM season2/loops/hypothesis-every-live-row-carrie-a00-efb7f2a8 tip 69958a4a9 (worktree a00-efb7f2a8). No merge. Never rebase.
OUT OF SCOPE  the backfill of the 18 boxless config:posts rows -> the director's [red] to its master (other posts' rows), NOT this round.
1. test_box_guard.py:46-64 still pins the removed default_box fallback (this_box == default_box, a boxless row is local) and is RED at the base -> re-pin both tests to the new contract (an unset box is refused by name), never delete them.
2. crons.py:795-810 -- _this_box catches boxes.this_box's refusal and returns '', and _on_this_box treats '' as no gate, so a box with no AGI_BOX runs EVERY cron job -> fail CLOSED: an unset box runs no box-gated job and prints the refusal once; one test.
3. boxes.py:186 row_is_local returns `not own` when this_box raises (fail-open, pinned by test_box_identity.py:124), contradicting conjunct (2b) 'an empty or unknown row box is never local on any box' -> make it never-local and re-pin :124, OR record on the kid node, with the measured reason, why (2b) must keep this one exception; pick one.
4. send.py:2176 _FOREIGN_REFUSALS is process-local; the nudge_sweep cron is a new process every tick (crons.py:955) -> conjunct (3) 'once per row+cause' needs a durable memo (a small state file under .agi/sessions, keyed row+cause) OR the node narrows (3) to the long-lived reaper (heal.py:1898 _repair_stranded_wakes) with that census line added; pick one, test it.
5. rotate.py:9657 -- no committed test drives _successor_row_write to the _stamp_row_box call -> one test through _successor_row_write.
6. experiment:a00-fb8c4f95-cd7594 says '12 tests, 12 passed'; test_box_identity.py has 17 -> RE-RUN, paste, fix (write.py).
ANON      no user name, home or repo path value, host or IP, no box hardware names (class prefixes only); patterns write <user>
TESTS     test_box_guard.py test_box_identity.py test_crons*.py test_send.py test_rotate*.py -k box test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/crons.py (_this_box/_on_this_box) · extensions/agi/bin/boxes.py (row_is_local) · extensions/agi/bin/send.py (the foreign-refusal memo) · extensions/agi/tests/test_box_guard.py · extensions/agi/tests/test_box_identity.py · experiment:a00-fb8c4f95-cd7594 (write.py) · the kid's own node. NEVER .agi/nodes/.geometry/posts.md.
CEILING   HARD CAP: 2 kids (1: items 1-3, 2: items 4-6) · net <= 25 production lines · <= 90 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.577 -- closes mur-director-engine-25 DH.525-k1 demote + DH.525-k2 demote
BASE      CUT FROM season2/loops/hypothesis-every-live-row-carrie-a00-3a9014b2 tip 557a90602 (branch de-base-577; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. HARD CAP BREACH 3.4x
2. 2. FALSE BYTE CLAIM IN A THOUGHT (.agi/config.json:235) + production_lines: 67
3. 3. VERDICT CONTRADICTION in a00-35013368-3c4237.md
4. 4. config_max — hardcoded twin of the intended cell
5. 5. P9d SEAM OPEN — per-worktree memo
6. 9. SCOPE DEVIATION — third test file, 165 lines
7. 10. IO + LOST-UPDATE WINDOW (send.py:2286, read at 2237-2245)
8. 11. ORDER NOT MERGED
9. 12. HAND-LANDED KID BYTES
10. STALE DOCSTRING THAT NOW ASSERTS THE OPPOSITE OF THE CODE — extensions/agi/bin/crons.py:806-809, _this_box's docstring still reads 'Unresolved (no AGI_BOX, no default_box cell) is the empty string, which gates nothing in `_on_this_box` and substitutes to nothing.' That is precisely the behaviour crons.py:801-802 removed in this same diff (`if not own: return False`). A future reader who trusts the docstring concludes the fail-closed gate does not exist and can 'fix' _on_this_box back. The first reviewer cited crons.py:981-989 as the fail-closed evidence and did not notice the sibling docstring 175 lines above it contradicting it.
11. THE FIRST REVIEWER'S OWN DEFECT 7 RESTS ON A FALSE PREMISE THAT IS ALSO REPEATED IN A NODE BODY — a00-35013368-3c4237.md:56 ('What this does NOT do: the long-lived reaper (heal.py _repair_stranded_wakes) is a separate in-process memo and was NOT narrowed') and the order's own item 4 both describe a memo that does not exist: heal.py:1999-2013 holds none, and the only set is send.py:2176, reached by the reaper through send.wake -> _nudge_target (send.py:2245/2279). So the node records a non-existent residue as a caveat. Under this round's rules ('a claim about a reader that was never read is wording') that caveat is false prose, and it should be corrected in place rather than carried forward as a live open item.
12. I CHECKED AND CLEARED one concern neither reviewer raised: the durable memo lands at <repo>/.agi/sessions/foreign_refusals.tsv, and .gitignore:104 (`.agi/sessions/*`) already ignores that directory, so the memo can never be committed into the graph and cannot pollute git status or the grid. `git check-ignore -v .agi/sessions/foo.tsv` confirms. No defect; recorded so the next reader does not re-open it.
13. Sharpening of the first reviewer's defect 10, which the node's own caveat understates: the memo read at send.py:2234 is on the RESOLUTION path, not the sweep path — _nudge_target is called from four sites (send.py:2371, 2798, 2948, 2997), so an interactive `send dm` pays it too. The order's cost note and the node's :149 caveat both describe it as per-row-per-sweep.
14. 1. Frontmatter verdict contradicts the node's own demotion (a00-35013368-3c4237.md:21)
15. 2. The cited config cell is not in the tree; the path runs from a hardcoded twin (send.py:2184)
16. 3. Durable memo resolves per-worktree, not per-box (send.py:2194)
17. 4. _this_box docstring states the behaviour this round inverted (crons.py:806/809)
18. 5. Dead branch, guarded forget is unreachable (send.py:2288)
19. 7. a00-fb8c4f95 still asserts a red tree that is green (a00-fb8c4f95-cd7594.md:110)
20. 8. HARD CAP breached 3.3x/2.3x with no re-brief (send.py:65)
21. A green test pins a live crontab-stripping behaviour whose blast radius was never measured. test_box_guard.py:166-195 (`test_crons_box_gate_fails_closed_on_an_unset_box`) asserts that with AGI_BOX unset, `render_managed_lines` emits NO runnable line for a box-gated job — and it is green. But the live cron:crons node gates FOUR enabled jobs with `box: local-town`: mail_poll (crons.md:15-19), maint_gc (:29-34), prime_merge (:35-40) and memory_alarm (:41-46), while grid_sync (:8-11), branch_push (:12-14) and nudge_sweep (:26-28) are UNGATED and therefore survive. So on any box whose ini never set AGI_BOX, the still-running ungated grid_sync re-applies every 5 minutes and strips exactly those four from that box's crontab — including memory_alarm, installed 09-26 against the 03:20Z memory livelock (crons.md:45), and prime_merge, the Prime's merge routine. That is the identical harm the sibling node refused at a00-fb8c4f95-cd7594.md:119-125 ('would make `heal` and `mail_poll` stop working on any dev graph and on any box whose ini never ran'), yet the round carried no such caveat into the cron path; the banner at crons.py:981-989 makes the refusal visible but does not prevent the outage.
22. The config-reading branch of the memo path is exercised by no real project, only by the new test's own hand-written fixture. send.py:2189-2191 reads `paths.core.foreign_refusal_memo` through `locations.load_config`, but because that cell is absent from `.agi/config.json` at this commit (defect 2), the branch resolves to None for every real invocation and falls through to the literal at send.py:2184. The only fixture in the tree that supplies the cell is test_foreign_refusal_durability.py's own `_graph`, which writes it by hand to match the code. So the 'config-max' design is verified only against a fixture authored to agree with the implementation, and the fallback at send.py:2194 — the path every production call actually takes — has no test asserting the resolved location.
23. Defect 1's machine-visible half, which the first reviewer did not name: the demotion exists ONLY in THOUGHT prose. The loop's own commit subjects record the opposite state — `git log` shows 'a00-35013368 done: experiment:a00-35013368-3c4237 verdict=proved' and 'a00-3a9014b2 done: experiment:a00-114ee609-176796 verdict=proved'. So the evidence gate, the viewport and any parent reading frontmatter all see `proved` for a round whose own review paragraph concludes 'a lean at 70, not `proved`' (:144). The round is not merely internally inconsistent; the value the graph scores is the one the review refused.
24. The memo rewrite is non-atomic and unguarded against concurrent sweeps, a window the round's own probes never test. send.py:2239 uses `path.write_text(...)`, which truncates then writes, while `_foreign_refusal_said` at send.py:2203 reads the same file. nudge_sweep runs every 2 minutes (crons.md:26-28) and `wake --all-local` fans out across rows, so a reader landing between truncate and write sees an empty or partial file and re-names a refusal that was already named — the exact defect the round exists to remove. a00-35013368-3c4237.md:146 caveat (3) names the per-row IO shape but not the torn-read window, and probe P6 (:141) exercises only SEQUENTIAL processes, never two concurrent sweeps, so no committed test would catch it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_box_guard.py test_foreign_refusal_durability.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/crons.py · extensions/agi/bin/send.py · extensions/agi/tests/test_box_guard.py · extensions/agi/tests/test_foreign_refusal_durability.py · .agi/config.json · .agi/nodes/experiment/a00-114ee609-176796.md · .agi/nodes/experiment/a00-35013368-3c4237.md · .agi/nodes/experiment/a00-fb8c4f95-cd7594.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = the code + config items, k2 = the node-text items) · <= 15 production lines net over 557a90602 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.577: mur-director-engine-25 DH.525-k1 + DH.525-k2 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
