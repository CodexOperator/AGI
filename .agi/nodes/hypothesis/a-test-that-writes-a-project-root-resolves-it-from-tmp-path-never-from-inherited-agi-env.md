---
id: hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env
mint_id: ee9eda3c8dd94667a88a273904c1259b
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: f8a5b9667b432cfa
season: 2
testable_claim: The test that rewrote a post worktree's config.json and made a nodes/nodes self-loop at 05:03Z 09-28 is named by a scratch-tree repro under a dummy AGI_* env, and after the fix it leaves that scratch tree byte-identical.
title: A test that writes a project root resolves it from tmp_path, never from inherited AGI_* env (TMM.322 leak)
town: core
---
# hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env

# hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env

## Measured
- 05:03Z 09-28, director-engine post worktree: a pytest run from a shell carrying the seat's AGI_POST / AGI_SEAT left (a) `.agi/config.json` rewritten -- workflows.review / drafting / deep-search `provider: pi-free` -> PAID `pi`, a `drafting.model` deepseek slug added, a `mint.storage_categories` block added -- and (b) a `.agi/nodes/nodes` self-loop. thought-master verified it contained, 0 spend (TMM.322).
- The leaked bytes are NOT a fixture literal: `git grep storage_categories -- extensions/` is empty at 230bf04de, so a test wrote an OLDER / FOREIGN config version over the live tree instead of into its tmp_path.
- Detached systemd units carry no AGI_* (`systemctl --user show-environment` has none); a seat's interactive shell does -- the leak needs the inherited env.

## CLAIM
The test that wrote it is NAMED (file::test, reproduced in a scratch tmpfs worktree with a dummy AGI_* env, the transcript pasted), and fixed so that a test which writes a project root (config.json, nodes/) resolves that root from tmp_path -- never from inherited AGI_* env, cwd, or a git ref of the live tree. Re-running the named test under the same dummy env leaves the scratch tree byte-identical (git status empty).

## Dispatch line
config-max: none (no cell carries a test's root) · template-max: the TESTS line of every brief already scrubs AGI_POST/AGI_SEAT (TMM.322) -- keep, cite · code: the named test's (or its fixture's) root resolution -- the only code.

## FALSIFIERS
- no test reproduces the write under a dummy AGI_* env in a scratch worktree (then say so with the transcript, and name the next suspect: a non-test writer);
- after the fix, the named test under the dummy env still changes any byte of the scratch tree;
- the fix changes a production resolver's behaviour for a real seat.

## TESTS
The named test file + its neighbourhood + test_bin_help_smoke.py, run ONLY in a scratch worktree under /dev/shm (git worktree add --detach), TMPDIR + --basetemp under /dev/shm, with a DUMMY AGI_POST/AGI_SEAT (never a live post name); never in a post worktree or MAIN.

## FILE SCOPE
The named test file and, only if the root resolution lives there, its conftest/fixture · the kid's own node. No production file without naming it OUTSIDE first.

## CEILING
1 kid · 0 production lines · <= 30 test lines net · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. QUEUED behind the EG.9 chain (TMM.322 (1)).

## CORRECTIVE DH.EG.94 -- closes mur-eg-24 EG.60 demote
BASE      CUT FROM season2/loops/hypothesis-a-test-that-writes-a--a00-34668655 tip bfc310107 (branch de-base-EG.94; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Config half of the guard cannot see the incident shape (test:108, abs(mtime_before-mtime_after) > 0.6 is a window; parent PROBE A returned ['nodes'] only)
2. 2. Non-vacuity test manufactures the state it claims to witness (test:193, time.sleep(0.7) before the write)
3. 3. verdict cell contradicts the node's own THOUGHT (a00-64e1ebef-356f47.md:25 'verdict: proved' vs :116 'DEMOTED proved -> inconclusive_lean_proved:60')
4. 5. New-entry detector is blind to a stranded artefact (test:110, nodes_a - nodes_b cannot see a self-loop left by a killed run)
5. 11. 0.6 literal duplicated (test:108 and test:125, no named constant)
6. MISSED, demote-grade: the malformed-entry filter reds the suite on a LEGITIMATE graph action. test:111-113 flags any new entry with len(parts) != 2, but a retired node is moved to .agi/nodes/deprecated/<type>/<slug>.md - three path parts - and that tree holds 222 such files today. AGENTS.md's standing convention is 'Retire, never delete: status deprecated + move to .agi/nodes/deprecated/<type>/'. So any node deprecated while the suite runs is reported as 'the suite wrote a fixture artefact into the LIVE tree'. The docstring at test:97-104 believes the noise handled is 'new well-formed <type>/<slug>.md' and never names the deprecated/ shape, so the new guard introduces a false positive on a routine, frequent action - a misattributed red in the Prime's rotation verify. One-line fix: accept the 3-part deprecated/<type>/<slug>.md form (or any part count >= 2 ending in .md).
7. MISSED, residue: the failure message misattributes cause. The widened check's findings are concatenated into the pre-existing assertion at test:173-177, whose text says 'the suite wrote a fixture artefact into the LIVE tree'. _graph_leaks returns a live config.json path or a malformed entry name (test:108-113), neither of which is a fixture artefact and neither of which is written by this file - so a benign concurrent config edit or a legitimate deprecated/ move surfaces as a claim about the fixture suite, sending the next reader after the wrong code. Same fix site as the item above.
8. MISSED, residue: the nodes/ half is silently vacuous on a tree without nodes/. test:92 is 'if base.is_dir() else set()', so on any checkout where .agi/nodes is absent _graph_snapshot returns an empty set, _graph_leaks can only ever report the config half, and the guard reports clean while watching nothing. A one-line assert _LIVE_NODES.is_dir() in the non-vacuity test would close it.
9. MISSED, note: a00-77564413-0707e5.md lands an UNFILLED scaffold as its body - the H1 is duplicated at :19-20 and the template placeholders are still there ('## Experiment / What did you do? What happened? Include command/inputs and actual outputs.' :21-23, '## Evidence / Raw output, screenshots, logs.' :25-27). The only authored content is Agent Notes at :30, which is where the parent's account of the dead kid lives. A reader opening the dead-no-work record reads the unanswered template first.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_no_live_root_writes.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_no_live_root_writes.py · .agi/nodes/experiment/a00-64e1ebef-356f47.md · .agi/nodes/experiment/a00-77564413-0707e5.md · .agi/nodes/experiment/a00-b8517494-599b4f.md · .agi/nodes/hypothesis/a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines net over bfc310107 · test lines net <= 0 over bfc310107 (the round is already +63 vs its 30 cap: every fix is paid for by cutting; one named constant replaces the duplicated 0.6) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat bfc310107 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.128 -- closes mur-eg-34 EG.94-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-test-that-writes-a--a00-3c9b4a51 tip 0e4e636a1 (branch de-base-EG.128; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1) not-a-gate -- the live graph witness spans one test function, so a leak from any other test in the run is invisible (cited file:142)
2. 5) duplicated write_text of retired.md (cited file:190)
3. 6) '## Evidence' still carries the 'Raw output, screenshots, logs.' scaffold on all three nodes (cited a00-0a1da446-239cfa.md:116)
4. MISSED (mechanism, the substantive one): the rotate call site is structurally inert. test_no_live_root_writes.py:156-160 calls rot.run_after_join_for_seat(graph, 'wt', ...) with only send_dm/type_input overridden, but the `graph` fixture (:128-135) creates just config.json + sessions/ -- no rotations/ record -- so rotate.py:15418 _latest_rotate_record globs <rotations>/wt.*.json, finds nothing (and its applied_rename fallback at :15345-15362 iterates the same empty list), and :15419-15420 returns None before any root resolution, write, commit or dm. The call therefore witnesses none of the 'rotations/*.seating.json leak' its own comment at :156 names. It is PRE-EXISTING (unchanged context in the diff; identical at bfc310107) and this round's docstring rewrite did drop the old suite-wide 'drives the primary heal/send/rotate/cli producer code paths' sentence (old :9) -- but neither the node nor the test discloses that one of the guard's drive sites executes nothing. Not demote: nothing regressed, and the other three sites (heal._dm_crash_recovery -> send.send at :148-154, send.send at :155-157, cli._alarm_dispatcher_on_done at :162-169) are real writes, and the guard's own scope is the conftest pin.
5. MISSED (mechanism, introduced by this diff): the new `assert _LIVE_NODES.is_dir(), f'vacuous guard: no nodes/ at {_LIVE_NODES}'` at :143 is a + line and hard-FAILS the live test instead of skipping it, so in any checkout with no .agi/nodes (fresh clone, a worktree created before the graph) the guard is red for a condition in which no leak is possible. tests/conftest.py carries no skipif convention for a missing project root, so nothing softens it; in this repo .agi/nodes always exists, so it never fires here. A skipif on `not _LIVE_NODES.is_dir()` would close it.
6. THE LIVE LEAK THIS GUARD EXISTS FOR, measured by the director 13:1xZ 09-28: a stray project root at <tmpdir>/.agi (config.json + context/ + sessions/.spawn-budget/a00-abc123-r1.lease, created 09:41Z) sat above every --basetemp /tmp fixture; the nearest-enclosing resolver sent fixture graphs to it and test_sensei_wake_audit.py read 18 failed with a /tmp basetemp vs 1 failed with a /dev/shm one (the director moved it aside; now 1 failed both ways). The lease id matches test_dispatch.py's _reap_one tests (the `iter_dir / "a00-abc123-r1"` fixtures): spawn_budget.budget_dir(tmp_path) on a tmp_path with no .agi marker resolves UPWARD. Make the guard a SUITE-WIDE GATE for this class: a session-scoped check that fails the run naming the test when a test leaves a .agi at tempfile.gettempdir() or adds a lease/record under the live root's sessions -- and PASTE, on your node, where budget_dir(tmp_path) resolves today for a tmp_path with no marker (one python -c command, its output). Fixing test_dispatch.py itself is OUTSIDE: name it.
KIDBRIEF  (mur-eg-31 EG.97 parent finding: the corrective reached the parent only, so the kid wrote code over a 0 cap) -- PARENT: dispatch your kid with --orders pointing at a file holding THIS WHOLE SECTION, and paste its FILE SCOPE + CEILING into the kid prompt; verify the kid's context carries the word CORRECTIVE before it starts.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_no_live_root_writes.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/conftest.py (the session-scoped gate only) · extensions/agi/tests/test_no_live_root_writes.py · .agi/nodes/experiment/a00-0a1da446-239cfa.md · .agi/nodes/experiment/a00-64e1ebef-356f47.md · .agi/nodes/experiment/a00-77564413-0707e5.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 0e4e636a1 · <= 40 test lines net over 0e4e636a1 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 0e4e636a1 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.128: mur-eg-34 EG.94-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
