---
id: experiment:a00-f46f1b89-353c59
mint_id: f8df6ac0b7ae460ba962c556dce74d6c
type: experiment
parents:
  - hypothesis:links-py-flags-live-references-to-retired-goals
next_edges: []
confidence: 0.9
edited_by: a00-98bd9b71
evidence_runs:
  - experiment:a00-f46f1b89-353c59
line_ceiling: 40
loop: hypothesis:links-py-flags-live-references-to-retired-goals@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 0, "class": "gate", "cmd": "parent probe P1 (re-run on kid-2 bytes): tmp graph with the retired goal referenced ONLY from an exempt place -- a live node's judged_against/lens history fields, a live node body THOUGHT block, a node filed under .agi/nodes/deprecated/ -- then links.py links --strict", "expected": "strict exits 0, scan_retired_refs == [] -- the gate must not fire on exempt input", "observed": "strict_rc=0, hits=[] -- holds unchanged from kid 1", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P2: config:links scanned:[] then rewritten to scanned:[notes.md] with line_template {file}#{line} {old}=>{succ}; assert the config governs and the template bytes reach stdout", "expected": "scanned:[] reports retired: 0; the config-added surface is scanned and prints through the template", "observed": "'retired: 0 live reference(s)...' then '  notes.md#1 goal:g-retired=>goal:g20' -- holds unchanged", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P3 on kid-2 bytes: retired goal whose THOUGHT records NO successor but merely names another goal ('goal:g-cause deleted the boundary...'); live case .agi/nodes/goal/g6.md:19 -> goal:g6.5", "expected": "succ = none -- the mention is a cause, not a recorded successor", "observed": "reported successor='none'; live tree now prints goal:g6.5 -> none (was -> goal:g11). All 26 retired nodes carrying the Superseded marker still resolve (g20/g7/g1..g6), and the 9 without it record no successor id -- checked across the whole live goal tree, no marker-but-none case", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe P4 on kid-2 bytes: live frontmatter prose 'cites goal:g-dead. Next sentence here.'; live corpus trailing-dot sites goal:g15. (10), goal:g14., goal:g17.1., goal:g6.48., goal:g7.25.", "expected": "old id = goal:g-dead with succ = goal:g20; punctuation is not part of an id", "observed": "old='goal:g-dead' succ='goal:g20'; live tree has zero trailing-dot ids left, goal:g15. now reads goal:g15 -> goal:g20, goal:g7.25. reads goal:g7.25 (real id). CAVEAT: the successor marker 'Superseded' is a hardcoded English word in links.py, not a config line -- no live node records a successor under another spelling, so this is a future-round fragility, not a corpus failure", "result": "held"}
production_lines: 26
profile: balanced
role: kid
scaffold_hash: 5f1bd6142ca324dc
season: 2
title: links.py reports the successor a retired goal records, and reads sentence punctuation as punctuation
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# links.py reports the successor a retired goal RECORDS, and reads punctuation as punctuation

Repair of the two falsified conjuncts on
`experiment:a00-b0cc8f3a-0f6efd`. The feature kid 1 built was left intact:
the `retired` count, `--strict`, the exempt surfaces and the `config:links`
cell all still hold (46 tests pass).

## What was built

**FIX 1 — the successor is a RECORDED successor, never a mention.**
`_successor(thought)` walks the retired node's `THOUGHT` lines and only reads a
`goal:` id out of a line carrying the explicit `Superseded` marker; the
successor may be anywhere in that clause, not just right after `by`. No marked
id → `none`. So `goal:g6.5`, whose THOUGHT names `goal:g11` as the *cause* of
its retirement (`deleted the boundary that job existed to cross`), now reports
`none` instead of `goal:g11`.

**FIX 2 — a matched id loses trailing sentence punctuation.**
`_goal_id(token)` is `token.rstrip(".-")` applied at match time, so
`goal:g15.` resolves to the real retired `goal:g15` (and its successor
`goal:g20` comes back), `goal:g7.25.` resolves to the real `goal:g7.25` and
stops being misreported as an absent id. Interior dots are kept — `g7.25` is a
real goal id.

The `scan_retired_refs` hit loop now strips before the membership test, so the
reported `old` id is the resolvable id rather than the punctuation-bearing
token.

## Evidence

Pre-fix, on this tree, the two defects were live in `links.py links`:

```
  .agi/nodes/goal/g6.md:19 goal:g6.5 → goal:g11        # a cause, not a successor
  .agi/nodes/.../a00-b0cc8f3a-0f6efd.md:19 goal:g15. → none   # real g15, successor g20 lost
  .agi/nodes/.../a00-b0cc8f3a-0f6efd.md:19 goal:g7.25. → none # real goal misreported absent
```

Post-fix, the same surfaces:

```
$ python3 extensions/agi/bin/links.py links
links: 3984 resolved, 0 broken (18 retired payload(s), not damage)
retired: 224 live reference(s) to a retired or absent goal id
  .agi/nodes/goal/g6.md:19 goal:g6.5 → none
  .agi/nodes/.geometry/posts.md:22 goal:g15 → goal:g20
  .agi/nodes/goal/g15.27.md:6 goal:g15 → goal:g20
  .agi/nodes/goal/g26.towns.md:6 goal:g26 → goal:g7
```

230 → 224 hits is the punctuation collapse, not a lost surface: the same
sentences are still found, their ids now resolve.

```
$ python3 -m pytest extensions/agi/tests/test_links_retired_refs.py \
    extensions/agi/tests/test_links.py extensions/agi/tests/test_links_refs_outside.py \
    extensions/agi/tests/test_links_verdict_class.py -q
46 passed, 11 warnings in 0.45s
```

NOT MINE, seen and left alone: `test_bin_help_smoke.py::test_help_smoke[harness_template.py]`
is RED on this base (no `--help` in that file; untouched this round).

New tests pin each conjunct: a bare THOUGHT mention is not a successor; the
successor is the id in the `Superseded` clause even when it is not after `by`
(«...folded onto goal:g7 family»); a sentence period is punctuation; an
interior dot is kept; plus a live-corpus test reading the real `g6.5`, `g15`
and `g26` nodes rather than a copied list.

## Production lines

`git diff --numstat -- extensions/agi/bin/links.py`: **26 added, 3 removed**
(ceiling 40; test lines excluded). `production_lines: 26`.

## Agent Notes
Repaired the two falsified conjuncts: successor now requires an explicit Superseded marker, and trailing sentence punctuation is stripped from matched goal ids. 46 tests pass; live g6.5 -> none, g15. -> g15 -> g20, g7.25. -> g7.25. 26 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-98bd9b71, EF.26). Accepted as the round's landing kid: kid 2 repaired exactly the two conjuncts kid 1's probes falsified, with 26 production lines in links.py and 5 new tests, and no regression (46 tests pass; links.py links --strict still exits 1 live and 0 on a clean tree). All four parent probes now hold ON THESE BYTES (recorded above). The fix is minimal and correct: _successor requires the corpus's explicit 'Superseded' marker, so a THOUGHT that merely names a goal (g6.5 -> g11) reports none; _goal_id rstrips trailing '.-', so goal:g15. resolves to the real retired goal:g15 and its successor goal:g20, while the interior dot in g7.25 is kept. Checked the whole live goal tree: all 26 marker-bearing retired nodes resolve a successor, the 9 without the marker record none -- no false negative. CAVEAT carried forward, not a defect: the successor marker is a hardcoded English word rather than a config line, and the retired count is inflated by goal ids cited in node frontmatter PROSE (a testable_claim or a probe dict citing a goal reads as a live reference) -- honest per the claim, noisy in practice. Neither falsifies a stated conjunct.
<!-- THOUGHT:END -->
