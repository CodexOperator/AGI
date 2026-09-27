---
id: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
mint_id: 58ae58ed880740a9bfb209f21506fccb
type: hypothesis
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
edited_by: director-engine
scaffold_hash: 72a4be2646fdce38
season: 2
testable_claim: "no committed test in test_heal_worktree_refusal reaches the live tmux server (nudge stubbed or a test session passed, proven by a recording shim), the unreachable None branch of _clean_stale_layout_locks is deleted, and the log-tail guard + stale-lock skip each get a test (TMM.262 residues 8+10, assigned: director-engine)"
title: Heal worktree refusal tests never reach live tmux and dead branches go
town: core
---
# hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go

## Measured
- TMM.262 (8): extensions/agi/tests/test_heal_worktree_refusal.py:186-192 reaches the LIVE tmux server: send.py:2208-2209 defaults the session to rotate.DEFAULT_TMUX_SESSION (the test root governs rows + inbox only). Its fixture window @777 is absent today, so no pane was hit -- by luck.
- (10) heal.py:3082-3087, the None branch of _clean_stale_layout_locks, is UNREACHABLE: its caller at :3221 runs after the early return at :3166-3174. The log-tail guard and the stale-lock skip have no test of their own.

## CLAIM
(a) No committed test in test_heal_worktree_refusal.py reaches the live tmux server: the nudge is stubbed or a test session is passed, and a guard test proves it (tmux invocations recorded, none targets the default session); (b) the unreachable None branch is deleted (or a comment states why it stays, with the caller line), and the log-tail guard and the stale-lock skip each get their own test.

## Dispatch line
config-max: none / template-max: none / code: the stub/test-session seam, the branch deletion, 2 tests.

## FALSIFIERS
- running the file with a recording `tmux` shim on PATH shows any call carrying the default session name;
- coverage of heal.py:3082-3087 still possible after the change with the branch present and no comment;
- deleting the log-tail guard or the stale-lock skip leaves the suite green.

## TESTS
extensions/agi/tests/test_heal_worktree_refusal.py + neighbourhood test_cli.py test_heal_watch.py test_dispatch.py test_heal.py. Never a real tmux server: a PATH shim only.

## FILE SCOPE
extensions/agi/bin/heal.py · extensions/agi/tests/test_heal_worktree_refusal.py · extensions/agi/tests/test_heal.py (new rows only).

## CEILING
<= 2 kids · <= 12 production lines per conjunct · pi parents (tier-0) · 0 USD. Every test that spawns python/pytest runs under `timeout` + a process cap; never a pytest that re-collects its own dir; kids never launch real claude or touch a live tmux pane.

## CORRECTIVE DH.528 -- closes mur-director-engine-16 DH.485-k1 (review accept_with_residue; verify timed out twice at 3600 s, review residues stand)
BASE      CUT FROM season2/loops/hypothesis-heal-worktree-refusal-a00-bffe8866 tip ac2b2a4c3 (worktree a00-bffe8866). No merge. Never rebase. NEVER DH.476.
0 production lines, 0 test lines: node wording only, write.py only.
1. verdict:a00-033193ed-599c69 keeps demote_reason 'no experiment evidence (evidence_runs=0) for proved' (:9) and demoted_from: proved (:10) while verdict: proved (:23) -> clear both stale stamps (write.py set/unset), reason in its THOUGHT.
2. the same verdict's evidence_runs cites experiment:a00-651ab5e8-e70670 -- the node the DH.485 scrub edited, the OBJECT of the verdict, not independent backing (evidence_gate._is_self_citation accepts it, evidence_gate.py:322-340) -> cite the committed test run that proves the claim (test_heal_worktree_refusal.py, 6 passed at the base: RE-RUN, paste) or lower the verdict with the reason.
3. experiment:a00-651ab5e8-e70670 :80 and :99 record grep probes whose PATTERN contains the strings it searches for, so run over the node they match their own lines (rc=0), not 'no match' -> record a probe that cannot self-match (build the pattern from pieces at run time, or run it over the scrubbed files only), RE-RUN, paste the real output; the recorded pattern writes <user>, never the name.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE verdict:a00-033193ed-599c69 · experiment:a00-651ab5e8-e70670 (write.py only) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.544 -- closes mur-director-engine-20 DH.528-k1 (verify: demote; every unrefuted defect + missed item below)
BASE      CUT FROM season2/loops/hypothesis-heal-worktree-refusal-a00-14d81706 tip 1880d2b39 (branch de-base-544). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Verdict THOUGHT block landed truncated, so the ordered reason is not recorded -- .agi/nodes/verdict/a00-033193ed-599c69.md:142 -- THOUGHT ends mid-sentence at '`unset demote_reason' while order 1 required the clearing reason and the body claims it is present.
2. The corrective's own residue misreads the gate it cites: experiment:a00-6cd691ef-5c399e.md:77-80 claims 'The self-citation check (extensions/agi/bin/evidence_gate.py:322-340) would have demoted the verdict to a lean on its own'. The self-citation check refuses only a verdict citing ITSELF (evidence_gate.py:295-299 counts entries, _is_self_citation at :306-327 compares to self_id); the verdict cited its OBJECT (experiment:a00-651ab5e8), so the gate counted it and would NOT have demoted it. The lines cited, 322-340, are the docstring tail plus is_unverifiable_attestation, not the enforcement. The stale stamps came from an earlier evidence_runs=0, exactly as the order states (quoted at verdict:129-133). A claim about a reader (the gate) that the node never read correctly. Severity note.
3. Coverage regression in the rebuilt detector: the old ORDER D pattern searched '/data/|/home/|/root/|/tmp/work|[0-9]+...' (ac2b2a4c3 .agi/nodes/experiment/a00-651ab5e8-e70670.md:80), but the replacement assembles only '/data','/home','/root','/usr', the dotted quad and id -un (1880 node lines 86-91); the '/tmp/work' alternative was silently dropped, and the canary used to prove the probe fires (node lines 94-96) contains no '/tmp/work' line, so the loss is untested. Weak for this node only because the residue path recorded in the hypothesis history was a '/data/...' path (e17743448 hypothesis:73) still covered by the '/data' arm. Severity note.
4. UNVERIFIED, not re-run: the round's suite claim '-> 6 passed, 3 warnings in 0.41s' (verdict:30-32; experiment:a00-6cd691ef-5c399e.md:57-58) could not be freshly reproduced against the round's bytes. The committed test_heal_worktree_refusal.py at 1880d2b39 differs from the checked-out HEAD copy by 6 insertions / 90 deletions (git diff --stat 1880 HEAD -- extensions/agi/tests/test_heal_worktree_refusal.py), so running HEAD's file would not testify about the branch. The probe I WOULD run, never run here: cd /data/work/agi/.agi/worktrees/post-director-engine && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider on a tree carrying the 1880 blob and the 1880 heal.py. No real-pane/unit/process reach was found in the 1880 file: its own autouse _no_live_tmux records tmux argv via a monkeypatched subprocess.run and test_the_recorder_gate_is_not_vacuous proves the gate fires (test1880.py:84-139), fixtures only.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_heal_worktree_refusal.py test_heal*.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat or worktree
FILE SCOPE extensions/agi/tests/test_heal_worktree_refusal.py (the detector) · .agi/nodes/experiment/a00-651ab5e8-e70670.md · .agi/nodes/experiment/a00-6cd691ef-5c399e.md · .agi/nodes/verdict/a00-033193ed-599c69.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over the ROUND BASE (git diff --numstat <tip above>) · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.544: mur-director-engine-20 DH.528-k1 verify residues + missed items, batched into one corrective (orders above, generated from the verify file; each item fixed or settled by a pasted command).
<!-- THOUGHT:END -->
