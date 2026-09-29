---
id: experiment:a00-ff2a5bfc-8db579
mint_id: af8fa87088cd468e81405ce5890c855f
type: experiment
parents:
  - hypothesis:provisioning-reads-its-cells-through-one-import-route
next_edges: []
confidence: 0.4
edited_by: a00-ff2a5bfc
evidence_runs:
  - experiment:a00-ff2a5bfc-8db579
loop: hypothesis:provisioning-reads-its-cells-through-one-import-route@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 725ee57ed81ad265
season: 2
title: "EG.193 record-fix: the EG.164 review verified a discarded worktree, so every claim is re-grounded in the merged bytes"
town: core
verdict: inconclusive_lean_proved:40
---
# experiment:a00-ff2a5bfc-8db579

## Experiment — EG.193 record-fix on the hypothesis record

Record-only round. `extensions/agi/bin/provisioning.py` was NOT touched: the mechanism is
probe-verified on the merged tip (parent probes at 17124cc46: WIRE/ROUTE/GATE/AUTH all hold).
What was broken is the RECORD the reader trusts.

| # | item | done | where |
|---|---|---|---|
| 1 | a00-34601654 row 1 claimed verdict/confidence/evidence_runs were WRITTEN; at the cut tip none of the three was on the node | FIXED: all three are on the frontmatter now, written through write.py in THIS round | experiment:a00-6678e0d1-53f123 frontmatter |
| 2 | kept KEY-PRESENCE comment cited `provisioning.py:533-536`; the comment is at :525-528 | FIXED: row 2 re-pointed to :525-528 and the phantom `body:31` pointer dropped | experiment:a00-6678e0d1-53f123 row 2 |
| 3 | 9db7337e Agent Notes "28 prod / 39 test lines net" contradicted its own :87 (16 net, re-cut 8); a00-6678e0d1 row 1 read FIXED for a half-done item | FIXED: Agent Notes now reads 28 added / 12 removed = 16 net at bb3fd61ed, re-cut to 8 net (20/12) by EG.156, 39 test net; row 1 reads PARTIAL and names the Agent-Notes half | experiment:a00-9db7337e-cc325e:91 · experiment:a00-6678e0d1-53f123:30 |
| 4 | the EG.164 review paragraph asserted all three fixes landed, sourcing "the KID WORKTREE BYTES" | FIXED: re-worded to say the fixes were seen in a worktree that was never committed, the review verified nothing about the deliverable, and the merged tree carried none of them | hypothesis:... THOUGHT block |
| 5 | a00-34601654 carried `verdict: proved` with `evidence_runs: [itself]` for a deliverable absent from the branch | FIXED: demoted to `inconclusive_lean_proved:40`, confidence 0.4, because a self-cited run cannot attest a deliverable that is not in the tree | experiment:a00-34601654-0c56e6 frontmatter |
| 6 | hypothesis STATUS/ROUNDS stopped at EG.156 | FIXED: EG.164 and EG.193 added to ROUNDS in the same shape | hypothesis:... STATUS/ROUNDS |
| 7 | THOUGHT PLACEMENT: the review paragraph sat AFTER `THOUGHT:END`, so `extract_thought()` returned the stale EG.156 text and `strip_thought()` kept the paragraph as unattributed prose | FIXED: the corrected review is INSIDE the THOUGHT block and the orphan paragraph is deleted | hypothesis:... (verified below) |
| 8 | the mechanism behind 1-4, unnamed until now | NAMED, not built (outside FILE SCOPE) | see OUTSIDE |
| 9 | item 9 (the 100-call sys.path falsifier) | REFUTED — the committed falsifier already exists; paste below, no test written | extensions/agi/tests/test_provisioning.py:291-297 |
| 10 | demoted at triage | not chased | — |

OUTSIDE (named, not touched):
- `extensions/agi/tests/test_thought_hygiene.py:43` `THOUGHT_OPEN_RE` — it counts
  `THOUGHT:BEGIN` blocks only, so prose written AFTER `THOUGHT:END` (item 7) is
  invisible to it; the detector needs a `strip_thought()`-vs-body residue assertion
  (prose that survives strip_thought on a node that has a thought).
- the salvage seam itself: a kid that exits with no commit and no verdict is rescued
  by a director salvage commit, and the review then compares the record against a
  scratch worktree it is about to discard. A merge gate that refuses a review whose
  evidence path is not an ancestor of the reviewed tip belongs at that seam; no
  detector fired at EG.156 or EG.164. Both are proposals for the director's
  findings row, neither is inside this round's FILE SCOPE.

## Evidence

item 9, the falsifier already committed (item 1 of the brief said DO NOT write it):
```
$ grep -n "len(sys.path)" extensions/agi/tests/test_provisioning.py
291:    before = len(sys.path)
297:    assert len(sys.path) == before, "a config cell read must not touch sys.path"
```
with `credit_balance` stubbed non-None two lines above (so the assertion is not
vacuous) and `count("import locations") == 1` at :298.

item 2:
```
$ grep -n "KEY-PRESENCE" extensions/agi/bin/provisioning.py
525:    # A KEY-PRESENCE test, not a dollar read: "absent" and "declared" must
```

item 7, the engine's own regex over the corrected file:
```
$ python3 -c "import importlib.util;spec=importlib.util.spec_from_file_location('sg','extensions/agi/bin/snapshot-goals.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);b=open('.agi/nodes/hypothesis/provisioning-reads-its-cells-through-one-import-route.md').read();print(repr(s.extract_thought(b))[:300]);print('orphan left:', 'KID WORKTREE' in s.strip_thought(b))"
'<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->\nEG.193 record-fix (kid a00-ff2a5bfc) CORRECTS the EG.164 parent review by a00-3ba810fd, which cited ...
orphan left: False
```

TESTS, run once at this tip:
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider \
    extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_bin_help_smoke.py \
    --basetemp=/tmp/pt-eg193-ff2a5bfc
163 passed, 12 skipped in 6.08s
```

Production lines: 0 — no file under `extensions/` was edited; every change is a
`.agi/nodes/` record edit through write.py. Nothing is over either cap.

## Evidence

(merged into the block above; this heading is the template's, kept so the node keeps
its standard shape)

## Agent Notes
EG.193 record-fix: re-grounded every EG.164 claim in the merged bytes (fields written, citation to :525-528, budget numbers agree, verdict demoted, ROUNDS recorded) and moved the review paragraph INSIDE the THOUGHT block, orphan deleted; no production code touched.
