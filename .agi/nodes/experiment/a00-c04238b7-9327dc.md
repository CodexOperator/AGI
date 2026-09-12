---
id: experiment:a00-c04238b7-9327dc
mint_id: 47fd62ea47994881afe89248e6b430be
type: experiment
parents:
  - hypothesis:l4-the-two-tree-origin-removed-xfail-is-strict
next_edges: []
confidence: 0.9
edited_by: a00-fd8ba149
evidence_runs:
  - experiment:a00-c04238b7-9327dc
loop: hypothesis:l4-the-two-tree-origin-removed-xfail-is-strict@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4fa22396cfd156dd
season: 2
title: "the SL7.19 origin-removed xfail is now strict=True: the module reads exactly 1 xfailed and an inverted-assertion scratch reads FAILED [XPASS(strict)]"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c04238b7-9327dc

## Experiment

FIX-ONLY build on `hypothesis:l4-the-two-tree-origin-removed-xfail-is-strict`
(g15.26, SL7.19 residue). Measured the pre-fix state, implemented the claim
(`strict=True` on the single xfail mark), proved it on the built bytes.

1. **Pre-fix measure** — `test_rotate_alert_two_tree.py` L420 carried
   `@pytest.mark.xfail(reason=...)` with NO `strict=True`, contradicting the
   module's own header comment (`xfail(strict=True)`). Running the module
   alone read `5 passed, 1 xfailed` — an unexpected pass would be reported
   as a non-failing `XPASS`, so the origin-removed falsifier the test exists
   for was never enforced; the merge-up has mis-counted it as `1 xfail`
   since SL2#17.

2. **Implement** — changed the single mark to
   `@pytest.mark.xfail(strict=True, reason="...")`. Only ONE mark, only
   `extensions/agi/tests/test_rotate_alert_two_tree.py`; no rotate.py edit,
   no fixture change. Within the claim's FILE SCOPE and CEILING.

3. **Prove on the built bytes** —
   `python3 -m pytest extensions/agi/tests/test_rotate_alert_two_tree.py -q`
   → `5 passed, 1 xfailed in 7.58s`. Exactly one xfailed, no XPASS: the
   honest xfail stays an xfail under strict. Then the scratch falsifier:
   a /tmp copy of the mark with the body inverted to an unexpected pass
   (assert True) reported `FAILED [XPASS(strict)]` — the run fails, which is
   exactly the enforcement the claim demands. Scratch removed, not committed.

## Evidence

Pre-fix module run: `5 passed, 1 xfailed in 6.72s` (no strict anywhere).

Post-fix module run:
```
....x.                                                                   [100%]
5 passed, 1 xfailed in 7.58s
```

Scratch falsifier (strict + unexpected pass → the run FAILS):
```
F                                                                        [100%]
[XPASS(strict)] defect: origin removed blocks checklist; strict must fail...
FAILED test_probe.py::test_unexpected_pass_is_strict - [XPASS(strict)] ...
1 failed in 0.02s
```

All three hypothesis tests met: (1) the mark carries strict=True; (2) the
module alone reads `1 xfailed`; (3) an inverted-assertion scratch reads
FAILED (XPASS strict).

## Agent Notes
FIX-ONLY build: added strict=True to the lone xfail in test_rotate_alert_two_tree.py; module reads exactly '1 xfailed', scratch inverted-assertion reads FAILED [XPASS(strict)]. Pre-fix had no strict anywhere.

Review accepted: proved. The single xfail mark at test_rotate_alert_two_tree.py:420 now carries strict=True, g15.26 SL7.19 residue fixed; module reads 5 passed 1 xfailed, and an independent inverted-assertion probe fails with XPASS(strict).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, SL7.34. (1) The dispatch brief said a g15 claim is a build order, not a measurement, and the target node capped the change at one mark in extensions/agi/tests/test_rotate_alert_two_tree.py. (2) What the machine does: that file line 420 now reads @pytest.mark.xfail(strict=True, and the module run reads 5 passed, 1 xfailed; I confirmed the falsifier independently, not from the kid report — a /tmp probe with strict=True over a passing body reads FAILED [XPASS(strict)], so an unexpected pass now fails the run. (3) Near miss: the module header comment at line 304 ALREADY said xfail(strict=True) before this change, so a kid could have edited only the comment, rerun, seen green, and reported proved — the words are satisfied while enforcement stays absent, because enforcement lives on the mark, never the comment. Checked the mark, not the report. (4) No deviation from a standing rule; the only edit beyond the kid is the scaffold-default title, replaced with the measured claim.
<!-- THOUGHT:END -->
