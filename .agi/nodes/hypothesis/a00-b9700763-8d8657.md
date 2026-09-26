---
id: hypothesis:a00-b9700763-8d8657
mint_id: 5e7bcdeee15a405aa17244affa79935f
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.85
edited_by: a00-613b8582
evidence_runs:
  - experiment:a00-b9700763-8d8657-exp
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: ba80a79aa5bfdbea
season: 2
testable_claim: "**The goal's count-based falsifier (\"0 grep hits outside the frozen fixture\") can be enforced as a committed test without deleting a single prose warning, provided the test keys its exemptions by (relpath, exact line text) and enforces the CLASS of each exemption — and the guard must mark docstring SPANS, not first lines, or it fails on prose forever.**"
title: the class-based retired-box-prefix guard test
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-b9700763-8d8657

## Hypothesis

**The goal's count-based falsifier ("0 grep hits outside the frozen fixture")
can be enforced as a committed test without deleting a single prose warning,
provided the test keys its exemptions by (relpath, exact line text) and
enforces the CLASS of each exemption — and the guard must mark docstring
SPANS, not first lines, or it fails on prose forever.**

Disproved by: a first-line-only docstring mark making the guard flag prose it
should not (the 7 false positives `experiment:a00-600cf080-0cd865-exp`
recorded), or a keying scheme (line numbers) that fails on every file shift.

## Why

Kid 1 measured all 22 live hits: 0 executable, 11 prose, 5 negative
assertions, 4 inert fixture strings, 1 `@live`-skipped constant, 1 config
cell. A count gate can only reach 0 by deleting the warnings — the goal's own
stated near-miss. A class gate reaches its target by naming each hit and
saying why.

## Result

PROVED on built bytes — `extensions/agi/tests/test_retired_box_prefix.py`,
5 tests, measured in `experiment:a00-b9700763-8d8657-exp`:

```
| test | locks |
|---|---|
| T1 | no live hit outside EXEMPT; entry = (relpath, exact line text) + reason |
| T2 | every EXEMPT entry is still live — no stale blanket waiver |
| T3 | class accuracy: P is comment/docstring-span, F and B are not; BOX_BOUND == 5 |
| T4 | the frozen-fixture exemption is by name and still exists |
| T5 | the guard carries the prefix only in PREFIX/EXEMPT/BOX_BOUND (ast spans) |
```

Keying by line TEXT rather than line number is what makes it survive the
refactors this subgoal is causing; T2 is what makes it honest as they land.

## Agent Notes
class-based guard test built: 5 tests key exemptions by (relpath, exact line text) with reasons, docstring SPANS marked, 0 production bytes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-613b8582) -- ACCEPTED, with one design wart named.

(1) WHAT THE KID CLAIMED: the count-based falsifier is enforceable as a committed test without deleting prose, keyed by (relpath, exact line text), with docstring SPANS marked; verdict proved, evidence experiment:a00-b9700763-8d8657-exp.
(2) WHAT THE MACHINE ACTUALLY DOES: I read the diff (367 insertions: the 208-line guard + 2 nodes) and RAN the guard, then tried to break it three ways, restoring the tree byte-for-byte after each (md5sum -c OK every time).
  GATE PROBE 1 -- vacuity + bite: appended RETIRED_PREFIX_PROBE = "/home/ubuntu/work/agi" to extensions/agi/bin/commands.py:673. T1 FAILED naming the file:line and the remedy. So _scanned() is not vacuous and a NEW executable hit is caught.
  GATE PROBE 2 -- the honest-refactor direction: rewrote one prose warning in commands.py (dropping the prefix from the text, the action the goal WANTS). T2 FAILED: "exemption no longer matches any line; drop it". So the warning cannot be cleaned up without touching the table -- the friction is in the right place, keyed on text so a moved line does not break it.
  GATE PROBE 3 -- self-reference: appended a stray prefix constant inside the guard file itself. T5 FAILED naming guard:210. The guard cannot quietly grow its own exemption.
  Baseline before any probe: 5 passed.
(3) THE NEAR MISS this design avoids, stated as the counterfactual: keying EXEMPT by LINE NUMBER. That satisfies "the goal asks for zero hits" and loses the refactors -- every unrelated file shift turns 22 exemptions into 22 failures, and the cheapest repair is to delete the warnings, which is the exact outcome goal:g73314-a-nonworkflow-residue exists to prevent. Keying on (relpath, stripped text) makes the table survive a move and makes a REWORD loud, which is what probe 2 measured.
(4) THE ONE WART: T3 ends in assert len(BOX_BOUND) == 5. A magic count inside a gate is the same brittleness the claim argues against -- when the coupled test_unify literals are repointed the number moves to 2 and the test breaks for a reason that is not a defect. The property to assert is "every non-prose exemption carries a reason", not a tally. Left for the next kid, named here so it is not rediscovered as a surprise.

Accepted as delivered. The guard does not yet cover .claude/ (0 hits today, so the gap is latent, not live) and the coupled test_unify.py literals are still class B in the table -- that is the next kid's work, not a defect in this one.
<!-- THOUGHT:END -->

PARENT PROBES (a00-613b8582), three, all run against the built bytes and all restored after:
probes: gate: append a live literal to extensions/agi/bin/commands.py -> T1 fails naming commands.py:673. Bites, and the scan is not empty.
probes: gate: rewrite one prose warning to drop the prefix (the action the goal wants) -> T2 fails "exemption no longer matches any line". Bites in the refactor direction, which is the one that matters.
probes: gate: append a stray prefix constant inside the guard file -> T5 fails naming test_retired_box_prefix.py:210. The guard cannot exempt itself silently.
probes: wire: baseline `pytest extensions/agi/tests/test_retired_box_prefix.py -q` -> 5 passed; each probe left the tree byte-identical (md5sum -c OK on commands.py and on the guard).
probes: auth: NONE POSSIBLE for this claim and that is the point -- there is no seat or role that may add a prefix occurrence without either removing it or naming it in EXEMPT with a reason. The gate is the authorisation.
Known gap, not a defect: the guard scans extensions/agi/{bin,hooks,briefs,tests} + .agi/config.json, not .claude/ (0 hits today).
