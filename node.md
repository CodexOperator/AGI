---
id: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
mint_id: 9c32ff237c4141e8be07f1db4682ff0a
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: e8c436a2bfd74454
season: 2
tags:
  - engine
  - cli
  - gate
testable_claim: "(1) when testable_claim carries a numbered item, cli._claim_conjunct_numbers returns the field numbers only (2) the body is read only for a node with no numbered field (3) the probe gate is unchanged on every other shape (assigned: director-engine)"
title: "the probe gate counts claim conjuncts from testable_claim only -- body prose never inflates the set (mur-10 DH.465; assigned: director-engine)"
town: core
---
# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

## Measured
- `cli._claim_conjunct_numbers` (extensions/agi/bin/cli.py:1169) unions every `_CLAIM_ITEM_RE` `(n)` match in the `testable_claim` field WITH every match in the node BODY (:1178, :1181), so review prose that numbers its own orders inflates the conjunct set: mur-director-engine-10 DH.465 measured [1,2,3,4] for a 3-conjunct claim; DH.477 had to reword another seat's authored review prose to de-number it.
- A candidate fix exists UNREVIEWED on branch season2/loops/hypothesis-heal-worktree-refusal-a00-c3688e41 (DH.476, off-orders there): the field wins outright when it carries a numbered item; the body is read only when the field has none.

## CLAIM
(1) when `testable_claim` carries at least one numbered item, `_claim_conjunct_numbers` returns the field's numbers ONLY; (2) the body is read only for a node with no numbered field; (3) the parent probe gate's behaviour on every other shape is unchanged.

## Dispatch line
config-max: none. template-max: none. code: the claim-surface rule in cli.py (the schema already names testable_claim as the claim field).

## FALSIFIERS
- a node whose field says (1)(2)(3) and whose body quotes (4) returns [1,2,3,4].
- a node with no numbered field and a numbered body CLAIM returns [].
- test_cli.py or its neighbourhood goes red.

## TESTS
extensions/agi/tests/test_cli_claim_conjunct_scope.py (new or taken from DH.476's branch after review). Neighbourhood: test_cli.py test_heal_watch.py test_dispatch.py.

## FILE SCOPE
extensions/agi/bin/cli.py (`_claim_conjunct_numbers` only) · extensions/agi/tests/test_cli_claim_conjunct_scope.py

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD.

## CORRECTIVE DH.523 -- closes mur-director-engine-17 DH.492-k1 (verify: accept_with_residue)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-cfed6d3f tip cd17ab80c (worktree a00-cfed6d3f). No merge. Never rebase.
1. No committed test reaches cli._parent_probe_gate (test_cli_claim_conjunct_scope.py:37,46,56,69 call only _claim_conjunct_numbers) -> ONE test through _parent_probe_gate for a field-only claim and one for the unchanged shape (claim 3).
2. experiment:a00-a041cdef-3b79fa carries its five probes only as body prose (:82-86) -> set its probes field with write.py (the [experiment] schema declares it).
3. Corpus effect unquantified: RE-COUNT the live hypothesis nodes whose numbered testable_claim differs from the body's (n) set (the reviewer measured 43), paste the command + number on the kid node, and name two whose demanded set shrinks.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_cli.py -k probe + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · experiment:a00-a041cdef-3b79fa (write.py) · the kid's own node. 0 production lines.
CEILING   HARD CAP: 1 kid · 0 production lines · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.541 -- closes mur-director-engine-20 DH.523-k1 (verify: accept_with_residue; every unrefuted defect + missed item below)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-966d7899 tip 06e6912da (branch de-base-541). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Corpus-count replay command names a non-existent scratch script — .agi/nodes/experiment/a00-ea0222b3-4ed78e.md:64 — the pasted count_conjuncts.py under .agi/sessions/iter-DH.523/ is absent, so the command is not rerunnable verbatim (an adapted equivalent reproduces 43/43)
2. a00-ea0222b3-4ed78e.md carries NO frontmatter `probes:` field; its six parent-run probes live as THOUGHT/body prose at committed lines 133-139 ('probes: [gate] ... HOLD'). This is exactly the prose-not-field class the round's JOB 2 fixed on experiment:a00-a041cdef-3b79fa (frontmatter lines 14-18, verified: 5 dicts, all six keys, classes gate/gate/gate/gate/wire). The corrective did not apply its own rule to its own node. Note severity.
3. Node-frontmatter probes are written but reader-less: cli.py:2028 sets set_fm['probes'] in _append_verdict_to_node, yet the only reader of `probes` in the shipped tree is cli.py:1216 (`_parse_probes(getattr(args,'probes',None)) or rec.get('probes')`), i.e. the gate reads --probes or the agent record, never the node frontmatter. So JOB 2's 'now machine-readable' claim (a00-ea0222b3-4ed78e.md:57-59) overstates consumption: the field is written, nothing shipped reads it. Wording/note, not mechanism.
4. Line-count inaccuracy: a00-ea0222b3-4ed78e.md:43 says '18-line helper' and :131/:146 say '+22 test lines'; `git diff --numstat cd17ab80c 06e6912 -- extensions/agi/tests/test_cli_claim_conjunct_scope.py` is +33 (27 non-blank). Still under the 40-line ceiling, so no ceiling breach — a number wrong by 11, note only.
5. UNVERIFIED (no committed test, probe not run per the no-probe rule): no committed test drives cmd_done end-to-end with a FIELD_NODE whose body review cites (1)..(4). The committed coverage composes two disjoint facts — the new tests drive _parent_probe_gate with FIELD_NODE (test_cli_claim_conjunct_scope.py:84/:91/:98, I ran it: 6 passed) and test_cli.py:887/:904 drive cmd_done with a plain 4-conjunct node. The combined end-to-end behaviour is attested only by the parent's scratch probe (a00-ea0222b3-4ed78e.md:138). Probe I would run but did not: temp graph whose hypothesis has testable_claim (1)(2)(3) + body review (1)..(4); cli.cmd_done --parent hypothesis:target with probes 1..3 -> rc 0, with probes 1..2 -> rc 2 naming conjunct 3.
6. The node's own CAVEAT (a00-ea0222b3-4ed78e.md:129) is false: it asserts 'Only my wire probe ... covers the call site, and it lives in a parent scratch dir, not in a committed test.' The cli.py:1554 call site IS covered by committed tests test_cli.py:887/:904 (green: test_cli.py -k probe -> 7 passed). The parent's self-criticism understates its own evidence and is the same mistaken premise as first-reviewer defect 2; a note, not a round defect.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat or worktree
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · .agi/nodes/experiment/a00-a041cdef-3b79fa.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over the ROUND BASE (git diff --numstat <tip above>) · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.560 -- closes mur-director-engine-24 DH.541-k1 demote
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-1362856d tip 98b2b99e5 (branch de-base-560; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
SETTLED   the verify demote driver (DH.492's cli.py body e12a57722 absent from the trunk) is MERGE ORDER, not a defect: e12a57722 is an ancestor of 98b2b99e5 and lands with this chain (director, git merge-base --is-ancestor). Do NOT touch cli.py for it.
1. 1. Line-count correction partial: '+22 test lines' survives at two sites (:182, :209) though :50 was corrected to +33/+27
2. 2. Duplicated truncated paragraph: the '**43 of 1268 ...** -- the reviewer's 43' line is emitted twice, first copy ending mid-clause (:120-122)
3. 6. Correction label points down at an original that is above it: the false CAVEAT remains verbatim at :194
4. MISSED -- the correction is MISFILED, not merely mislabelled: a00-ea0222b3:196-208 sits after '<!-- THOUGHT:END -->' (:195), so DH.541's delta about the false CAVEAT is body/state while the false CAVEAT is still the THOUGHT (:194). The first reviewer reported only the 'points down' wording and missed the G2.11 region error -- a regenerating scan or a thought-reader keeps the retracted claim as this version's reasoning.
5. MISSED -- a00-0f446ede:147 asserts 'The node's text is corrected to those numbers' for ITEM 4. That is false on the bytes: '+22 test lines' survives at a00-ea0222b3:182 and :209. This is the citing site of the first reviewer's defect 1, and neither the round nor its parent review names it.
6. MISSED -- doubled H1 in the round's new node: a00-0f446ede-c1a870.md:38 and :39 are both '# experiment:a00-0f446ede-c1a870' (derived heading + the authored body repeating it). Sibling nodes carry one (a00-ea0222b3:30, a00-a041cdef:29). Measured frequency 5/200 experiment nodes -- a minority artifact, cosmetic, residue only. (BODY:BEGIN with no BODY:END is NOT a defect: 315 of the first 400 experiment nodes have that shape.)
7. UNVERIFIED -- TMM.268's 'bytes == last write-log sha' precondition for 98b2b99e5. The write-log lives in the kid worktree, pruned. Probe I WOULD run: sha1 of `git show 98b2b99e5:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md` against the last write-log sha recorded for agent a00-0f446ede in `.agi/sessions/iter-DH.541/*/write-log*`. NOT RUN (the log is gone). The commit asserts the equality; I cannot confirm it.
8. UNVERIFIED -- probe c3_new_test_is_not_vacuous_mutation (a00-0f446ede:25, 'rc=2 refusal_4=True'). I did not re-run the monkeypatch. Read-verified only: cli.py:1209-1235 plus FIELD_NODE (test file :22-29, field (1)(2)(3), body citing (1)..(4)) implies the pre-fix union demands {1,2,3,4}, so 3 probes leave conjunct 4 missing -- the claim is mechanically sound. Probe I WOULD run: monkeypatch cli._claim_conjunct_numbers back to the field|body union and re-run the round's rc-0 assertion, expecting rc 2 naming conjunct 4. (cmd_done is not on the forbidden list; I chose not to author it.)
9. UNVERIFIED -- the 62 whole-frontmatter variant (a00-0f446ede:99-102). Not re-run; the two named nodes' whole-frontmatter deltas are [5,20,192] and [], consistent with the class, but the 62/62 total is unmeasured by me.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · .agi/nodes/experiment/a00-0f446ede-c1a870.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 98b2b99e5 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.589 -- closes mur-director-engine-30 DH.560-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-da08fcf5 tip 4e82ecf3f (branch de-base-589; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Stale numstat "40 0" still uncorrected on the node the round edited (a00-0f446ede-c1a870.md:78 body, :180 evidence), where the tip measures 40/3
2. 2. Parent probe 1's observed line number is a first-match artifact (a00-9f9aaacd-303434.md:15 'end=194')
3. 3. Pasted reproduction command no longer prints the reported number (a00-ea0222b3-4ed78e.md:51)
4. 4. Negative control does not discriminate under mutation (extensions/agi/tests/test_cli_claim_conjunct_scope.py:98)
5. THIRD recurrence of the uncommitted foreign-node edit, hand-landed by the director post inside the range under review: commits cfac66b6c (kid done) and c412999be (parent done) touch ONLY .agi/nodes/experiment/a00-9f9aaacd-303434.md, and the two nodes the round edited land only in 4e82ecf3f ('director-engine: land DH.560's logged node edits left uncommitted in the parent worktree', author belam@local-town). That violates the order's explicit PARENT clause - 83201e836: 'COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)' - while the round's own review asserts 'NO DEVIATION from the review rules' (a00-9f9aaacd-303434.md:196) and 'The only residue that stands is item 7 UNVERIFIED' (:198). The identical defect was already charged twice on these bytes: a00-0f446ede-c1a870.md:192 ('recurring, not one-off', cf. 06e6912da for the DH.523 case) and :199. Chargeable, and the fix belongs in `cli done` committing the whole FILE SCOPE, not in a director post - the round's own item-10 fact (c) at :133-135 ('`cli.py done` is the only commit') is falsified by its own round.
6. The two number defects are ONE latent mechanism the round did not touch: node text pastes base-relative numstat WITHOUT pinning the base (a00-0f446ede-c1a870.md:78 and :141-144, a00-ea0222b3-4ed78e.md:51-55) - the base `cd17ab80c` predates the very edit being counted, and the unbased `git diff --numstat` at :78 counts a different delta again. Nothing in DH.560 prevents the third instance. The rule belongs in the order TEMPLATE the round itself names at :154-155, next to the file:line format, so every corrective's number-pastes carry a base that contains the round's own bytes.
7. Checked and CLEAR (recorded so the next reviewer does not re-raise it): the absence of extensions/agi/tests/test_cli_claim_conjunct_scope.py at this worktree's HEAD (7d7aa870c) is branch divergence, not a deletion - 4e82ecf3f lives only on season2/loops/hypothesis-probe-gate-counts-cla-a00-da08fcf5, HEAD's cli.py:1169 still carries the pre-fix field|body union, and no .agi/nodes file is deleted anywhere in the diff (3 files, +225/-15). No test in the diff touches a real tmux pane, systemd unit, crontab or process: the only run recorded is pytest with --basetemp under /tmp (a00-9f9aaacd:165-168).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · .agi/nodes/experiment/a00-0f446ede-c1a870.md · .agi/nodes/experiment/a00-9f9aaacd-303434.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 4e82ecf3f · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.626 -- closes mur-director-engine-35 DH.589-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-f364d7a3 tip 15bc46e00 (branch de-base-626; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. ITEM 4 section duplicated verbatim in the landed node (the class this round exists to kill) -- .agi/nodes/experiment/a00-ea0222b3-4ed78e.md:111 -- Lines 79-110 and 111-143 are the same 32 lines plus one blank (diff of the two ranges is empty apart from that blank): '## ITEM 4 (DH.589 a00-bc9448e3) -- the negative control now DISCRIMINATES under mutation' appears twice, ending in the same '150 passed, 6 skipped' paste. The parent (a00-f364d7a3, a00-bc9448e3-61e351.md:209 charge (b)) saw it and correctly refused to hand-fix a kid's bytes; director commit 15bc46e00 landed it as-is. One write.py body edit on this node removes 33 duplicated lines.
2. Stale line-number paste: the corrected THOUGHT:END measurement is a pre-merge instant -- .agi/nodes/experiment/a00-9f9aaacd-303434.md:194 -- a00-9f9aaacd-303434.md:15 and :181-196 (and the same paste at a00-bc9448e3-61e351.md:54-66) assert 'FULL SET {194, 213} ... the real closing marker at this tip is :213'. At 15bc46e00 the same grep returns 281 (prose mention) and 300 (marker), BEGIN :261, CAVEAT :279 -- shifted by the duplicate block that landed with this round. The order claim still holds (retraction is inside the THOUGHT, after the corrected CAVEAT), so this is a stale measurement, not a wrong conclusion; it is the round's own subject matter, a number pasted as a line number.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · .agi/nodes/experiment/a00-0f446ede-c1a870.md · .agi/nodes/experiment/a00-9f9aaacd-303434.md · .agi/nodes/experiment/a00-bc9448e3-61e351.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 15bc46e00 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.666 ran (parent a00-384c3b60, harvested 04:33Z 09-28 at 8005cdd06); mur-eg-12 accept_with_residue; its pure-text residues fixed by the director (skill agi-corrective §3a) at c2ddbb9fc on season2/loops/hypothesis-probe-gate-counts-cla-a00-384c3b60 -> batched re-mur.
ROUNDS    this post's rounds on this node: DH.626 DH.641 DH.666; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

## CORRECTIVE DH.641 -- closes mur-director-engine-37 DH.626-k1 demote
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-87eecd53 tip 82a23fe26 (branch de-base-641; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Three of four probe records deleted from a00-9f9aaacd without disclosure, verdict left at proved — .agi/nodes/experiment/a00-9f9aaacd-303434.md:15
2. 3. The flagship base-pinned paste is not what the named command prints at the named base — .agi/nodes/experiment/a00-7b5520ac-96a290.md:78
3. 4. The false marker claim survives ahead of its own correction on both corrected nodes — .agi/nodes/experiment/a00-9f9aaacd-303434.md:191
4. Attribution of defect 3 is a MISS in the first review's framing: the false paste was introduced by the parent a00-87eecd53's own two write.py updates at 20:53:45 and 20:54:00 (worktree a00-87eecd53/.agi/sessions/write-log.jsonl, shas 5a4f9065 -> a3a4abb8), after the kid's committed 573a4e62f version carried the correct 279/281 lines. A reviewer edited the evidence it was reviewing.
5. The DH.626 parent review exists nowhere else in the tree: `git grep -l 'PARENT REVIEW DH.626' 82a23fe26` returns only .agi/nodes/experiment/a00-7b5520ac-96a290.md, and `git ls-tree -r 82a23fe26 | grep 87eecd53` is empty — no node file for a00-87eecd53. The round's only review record is the mis-pasted block, so the parent review is simultaneously the sole copy and the false one.
6. G2.11 residue the reviewer did not name: two of the three edited nodes change their body in this version with NO THOUGHT delta. a00-bc9448e3-61e351.md:232-242 (THOUGHT) is byte-identical to base although base :209 (the DH.589 record) was removed and :210-227 added; a00-ea0222b3-4ed78e.md:229-268 (THOUGHT) is byte-identical to base although 32 lines were deleted above it. A thought-reader of either version sees no reason for the change. (a00-9f9aaacd has no authored THOUGHT block at all — its THOUGHT:BEGIN/END mentions are all prose pastes at :55-:68, :180-:187, :226-:241.)
7. New duplicate ITEM numbers inside one node, the same heading-collision class the DH.560 review charged at a00-9f9aaacd-303434.md:216 ('its "## ITEM 10" heading TWICE'): a00-9f9aaacd-303434.md:219 adds '## ITEM 1 (DH.626 a00-7b5520ac)' while :33 is already '## ITEM 1 — FIXED.', and a00-bc9448e3-61e351.md:210 adds '## ITEM 3 (DH.626 a00-7b5520ac)' while :75 is already '## ITEM 3 — the pasted command still RUNS…'. The suffix disambiguates, but the round cross-references sections by bare number ('ITEM 2 above').
8. UNVERIFIED (not run): the round's '79 passed, 6 skipped' (a00-7b5520ac-96a290.md:135-141 and probe p3) cannot be reproduced in this checkout — extensions/agi/tests/test_cli_claim_conjunct_scope.py exists at BOTH merge tips (git ls-tree at 15bc46e00 and 82a23fe26) but is absent at this worktree's HEAD 6a536148a, and it was never deleted in history on this branch, so `pytest extensions/agi/tests/test_cli_claim_conjunct_scope.py extensions/agi/tests/test_bin_help_smoke.py -q` here errors 'file or directory not found'. The probe I WOULD run, read-only: `cd <worktree at 82a23fe26> && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli_claim_conjunct_scope.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider`. I ran no probe touching rotate/heal/send/dispatch.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-7b5520ac-96a290.md · .agi/nodes/experiment/a00-9f9aaacd-303434.md · .agi/nodes/experiment/a00-bc9448e3-61e351.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 82a23fe26 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.666 -- closes mur-director-engine-41 DH.641-k1 demote
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-9c666748 tip 8698b348e (branch de-base-666; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Re-created mis-paste on the round's own evidence node -- .agi/nodes/experiment/a00-df914bba-114582.md:72
2. No authored THOUGHT block of its own -- a00-df914bba-114582.md:74
3. The merging parent wrote into the evidence it reviewed, and did not charge it: commit bf784385b ('a00-9c666748 done', 22:08:03) is inside the review range and edits .agi/nodes/experiment/a00-df914bba-114582.md -- flipping `edited_by:` at :9 from a00-df914bba to a00-9c666748, appending its harvest to Agent Notes, and (via the thought splice) replacing the two real grep output lines. That is the same act the round itself charged as ITEM 4 on the DH.626 parent ('A reviewer edited the evidence it was reviewing'), raised against its own side and left uncharged. The first reviewer's defect 1 saw the paste but not its writer, its commit, or that it was a write.py thought verb rather than a hand edit.
4. The parent's own P6(b) self-verification (pasted at :85) checks only that a00-7b5520ac now prints 261/279/281/300; it never re-reads the node the harvest was writing into, so the six 'all HOLD' probes cover a file the same `done` call was mutating. A verification that excludes the file under the writer's own hand is the near miss this round was chartered to catch.
5. UNVERIFIED by me (probe I would run, not run): the DH.641 parent's P3 wire probe ('real cli.py done DH.641 --verdict proved --dry-run --parent hypothesis:target' in a tmp graph, record status still running). The only deliverable figure I could reproduce is ITEM 8's suite count: extracted 82a23fe26's extensions/ to /tmp and ran the two named files -> '79 passed, 6 skipped, 1 warning', matching :104-107. The P3/P4 subprocess and monkeypatch claims are parent scratch, not committed tests, and are not decidable from the diff.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-7b5520ac-96a290.md · .agi/nodes/experiment/a00-9f9aaacd-303434.md · .agi/nodes/experiment/a00-bc9448e3-61e351.md · .agi/nodes/experiment/a00-df914bba-114582.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 8698b348e · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.666: mur-director-engine-41 DH.641-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
