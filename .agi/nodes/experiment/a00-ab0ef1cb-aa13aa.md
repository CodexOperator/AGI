---
id: experiment:a00-ab0ef1cb-aa13aa
mint_id: f969ea657b154b26add3f0f98b001f28
type: experiment
parents:
  - hypothesis:l4-replace-api-drops-source
next_edges: []
confidence: 0.95
edited_by: a00-fc960ef7
evidence_runs:
  - experiment:a00-ab0ef1cb-aa13aa
loop: hypothesis:l4-replace-api-drops-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3f36a2a4c0d16250
season: 2
title: "\"API path of write.py replace silently deletes the target range; CLI path works\""
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ab0ef1cb-aa13aa

## Experiment

Driving `write.py`'s PYTHON API the way a director is told to for long prose —
`write.Edit` + `write.verb_replace` + `write.submit`, with NO manual
`edit.replace_text` assignment — against a FIXTURE payload in a temp graph.
Never a real repo node or payload (house rule in the hypothesis).

**The API path reports success while deleting.**

```
status       : updated
payload_changed: True
before lines : 6 after lines: 5
line3 still present: False
```

`verb_replace(edit, "payload", "3:3", "-")` then `submit(...)` returned
`status='updated' payload_changed=True` while line 3 vanished from the file
and nothing took its place. In a throwaway git repo the numstat reads exactly
what the hypothesis predicts:

```
numstat (adds deletes): 0	1	lib/mod.txt
```

ZERO insertions, ONE deletion — the range is dropped, not replaced.

**The CLI path, same verb, same range, works** (`1 1`), which is why this
shipped:

```
cli rc: 0 | out: updated: build:b1 / payload .../mod.txt replaced
cli numstat (adds deletes): 1	1	lib/mod.txt | line3: True
```

## Evidence

- `verb_replace` (`write.py:329-355`) records `edit.replace_from = source` and
  NOTHING ELSE. `submit` (`:616-625`) splices `edit.replace_text`, which for an
  API caller is still `""`; `_splice_range` (`:700-727`) faithfully splices the
  empty string, so the range is dropped. The only reader that turns
  `replace_from` into `replace_text` is `main()` at `write.py:1184-1191`, the
  CLI path — confirmed by reading the source.
- Root cause of no catch: the existing tests
  (`test_write.py:936-1009`) ALL set `edit.replace_text = ...` by hand after
  `verb_replace` — doing `main()`'s job for it. No test drives the API path
  naked, exactly as the hypothesis states.
- Fix is NOT implemented here. This node is the experiment (reproduction),
  standing as the evidence for a verdict; requirements (1)-(4) of the
  hypothesis (one shared resolver, empty-source refusal, stdin contract,
  explicit-deletion stance) remain open for a build/verdict step.
- Ran the targeted reproduction only (temp fixtures + `python3 -m pytest
  extensions/agi/tests/test_write.py -q` baseline). Did NOT run the full
  suite; did not touch `.agi/nodes/.geometry/*`.

## Verdict

**The hypothesis's central, measurable claim is PROVED**: driven through the
Python API, `write.py replace` silently deletes the target range and reports
`status='updated' payload_changed=True` while doing it (`0 1`). CLI works
(`1 1`); the two paths disagree because only the CLI resolves the source. The
FIX (one resolver, empty-source refusal) is a separate, unimplemented step —
this experiment is the measured defect.

## Agent Notes
Reproduced the defect through the Python API path (Edit + verb_replace + submit, no manual replace_text) against a fixture payload: status=updated payload_changed=True, numstat 0 1 — line 3 deleted, nothing gained. CLI path same verb/range yields 1 1 (works). Confirms hypothesis claim: only main()'s CLI reader (:1184-1191) turns replace_from into replace_text, so API callers splice '' and _splice_range drops the range. Baseline 87 pass on test_write + test_write_guard. Fix (one shared resolver, empty-source refusal) NOT implemented — separate step.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-fc960ef7): accepted. Verified the repro is the naked API path (no replace_text set by hand) against a fixture, that the CLI control reads 1 1, and that the node honestly scopes itself as defect-only with the fix left open. verdict proved is correct for the defect claim: the hypothesis first asserts the deletion exists, and 0 1 measured on a temp graph is exactly that. No changes made.
<!-- THOUGHT:END -->
