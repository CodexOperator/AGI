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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.94: mur-eg-24 EG.60 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
