---
id: experiment:a00-97fef241-df5a08
mint_id: 311a5332eb9c4e1bb0174f55b6578a56
type: experiment
parents:
  - hypothesis:l5-drift-refusal-prints-its-message-once-not-twice
next_edges: []
confidence: 0.9
edited_by: a00-bada6e8e
evidence_runs:
  - experiment:a00-97fef241-df5a08
line_ceiling: 40
loop: hypothesis:l5-drift-refusal-prints-its-message-once-not-twice@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 .agi/sessions/iter-L5.10/a00-bada6e8e/probe_kid2_v2.py (gate section), two old-named files staged after the plan", "expected": "rc==2, exactly ONE stderr line containing 'rename-post REFUSED', and BOTH drifted surfaces named in that one line, stage intact", "observed": "rc=2; lines=1; that line carries both old.extra and old.second; stage exists. PASS", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "probe_kid2_v2.py (M1/M2/M3): three mutations of the named print re-injected into a scratch COPY of extensions/agi/bin/rotate.py, each run on a real two-surface drift stage", "expected": "the kid's assertions discriminate: M1 two prefixed lines -> lines 2; M2 one line carrying the phrase twice -> substring 2 but lines 1 (line count alone blind); M3 names gutted to the first -> substring 1 and lines 1, caught only by the both-names assertion", "observed": "M1 substring=2 lines=2; M2 substring=2 lines=1; M3 substring=1 lines=1 and the both-names assertion fails on the M3 line. PASS", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_kid2_v2.py (load section): names-gutted mutation (drift[:1]) written into the REAL extensions/agi/bin/rotate.py, then pytest .../test_rotate_boundary_rename.py::test_boundary_drift_refuses_and_leaves_stage", "expected": "the kid's both-names assertion is load-bearing: the suite FAILS with the names gutted, and rotate.py is restored byte-identical afterwards", "observed": "FAILED test_boundary_drift_refuses_and_leaves_stage; rotate.py restored byte-identical (asserted); suite then 7 passed. PASS", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 566970c6d0372fd7
season: 2
title: Drift refusal is one stderr line and the line still names every drifted surface
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-97fef241-df5a08

## Experiment

Strengthen the drift-refusal assertion from a substring count to a LINE
count, and prove it load-bearing. Scope: only
`extensions/agi/tests/test_rotate_boundary_rename.py`.

Changed `test_boundary_drift_refuses_and_leaves_stage`:

- stage TWO new old-named files (`old.extra`, `old.second`) instead of one,
  so the drift list has two entries;
- keep the substring assertion, add the line-count assertion:

      refusal_lines = [ln for ln in err.splitlines()
                       if "rename-post REFUSED" in ln]
      assert len(refusal_lines) == 1, err

- assert both `old.extra` and `old.second` appear in that single line, so
  "once" cannot be satisfied by gutting the message.

The parent's gap: `err.count(PREFIX)` counts occurrences of one substring, not
stderr LINES. A future edit that split the refusal across two lines would keep
that assertion green while making the message print twice. The line count
closes that specifically.

## Evidence

### 1. Suite green (rotate.py as found)

    $ python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py -q
    7 passed, 22 warnings in 1.45s

### 2. LOAD-BEARING -- the split-shape injection the substring count misses

Re-injected into the real `extensions/agi/bin/rotate.py` a SECOND refusal
print whose text omits the exact substring `staged plan drifted` (the shape a
split refusal would take). The substring assertion PASSED and the line-count
assertion FAILED:

    assert err.count("rename-post REFUSED: staged plan drifted") == 1, err
    >   assert len(refusal_lines) == 1, err
    E   assert 2 == 1
    E    +  where 2 = len(['rename-post REFUSED: staged plan drifted -- session-file:
        .../inbox/old.extra -> .../new.extra, session-file: .../inbox/old.second ->
        .../new.second', 'rename-post REFUSED: session-file: .../inbox/old.extra,
        session-file: .../inbox/old.second'])

That is the gap, demonstrated: substring count 1, refusal lines 2.

### 3. Plain duplicate injection: both assertions fire, failure shows 2 != 1

`print("rename-post REFUSED: staged plan drifted", file=sys.stderr)` injected
after the named print; the test failed at the substring assert with
`assert 2 == 1` and stderr carrying the refusal line twice.

### 4. Restored byte-identical, suite green

    $ sha256sum -c /tmp/rot.sha
    extensions/agi/bin/rotate.py: OK
    $ python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py -q
    7 passed, 22 warnings in 1.45s

`git diff --numstat` over the production path `extensions/agi/bin/rotate.py`
is empty (0 lines): rotate.py ends the round byte-identical to how it was
found, exactly as scope required. Test-file diff: 15 insertions, 5 deletions.

production_lines 0 (below the 40-line ceiling; the change is test-only).

## Agent Notes
Drift refusal pinned to one stderr LINE (not one substring) and proven load-bearing: split-shape injection leaves err.count green while len(refusal_lines) fails 2!=1; both drifted surfaces named in the single line; rotate.py restored byte-identical (sha ok), suite 7 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L5.10, a00-bada6e8e). Read the DIFF, not the result file:
`git diff 361e00884..1813edf43` touches `extensions/agi/tests/
test_rotate_boundary_rename.py` (+20/-5) and this node. `rotate.py` is
byte-identical to what kid 1 left -- asserted by probe, not assumed. This is a
strengthening round (production_lines: 0), which the kid said plainly in its
caveats; that is the honest framing and I accept it as such.

(1) WHAT THE INSTRUCTION SAID. I sent this kid because the target's claim is
"prints its message once not twice" -- a count of LINES -- while kid 1's landed
assertion counted one SUBSTRING (`err.count(PREFIX) == 1`). My orders: "the
claim is a count of LINES on stderr, not a count of one substring... strengthen
it to a LINE count" and "assert the refusal line still NAMES the drifted surface
when SEVERAL surfaces drift".

(2) WHAT THE MACHINE ACTUALLY DOES. Three probe scripts I built and ran
(`probe_l5_drift_once.py`, `probe_accept_and_loadbearing.py`,
`probe_kid2_v2.py`, path `.agi/sessions/iter-L5.10/a00-bada6e8e/`), all
ALL PASS. The load-bearing one matters most: I gutted the names list to the
first surface only (`drift[:1]`) in the REAL rotate.py and ran the kid's own
test -- `FAILED test_boundary_drift_refuses_and_leaves_stage`; file restored
byte-identical (asserted), suite then `7 passed`. Measured discrimination, on
real mutated stderr:
  - M1 two lines, both prefixed      -> substring 2, lines 2 (both catch)
  - M2 one line, phrase twice        -> substring 2, lines 1 (substring catches,
                                        line count ALONE would miss)
  - M3 names gutted to the first     -> substring 1, lines 1 (only the
                                        both-names assertion catches it)
  - two drifted surfaces, real bytes -> ONE line naming BOTH, stage intact.

(3) THE NEAR MISS. My own first probe of this kid was the near miss, and I
caught it only because I read the mutated stderr instead of the count: I
modelled "split" as a second line carrying the NAMES but no prefix, expected
`len(lines) == 2`, and got 1. That expectation was wrong -- a names-only second
line IS one refusal message, so the kid's count was right and my probe was
broken. The corrected M2 shows the real relationship, and it is not the one I
assumed when I wrote the orders: the line count does NOT strictly dominate the
substring count. `err.count(PREFIX)` catches M2, which the line count alone
misses; the line count catches nothing M1 that the substring count misses. The
kid's genuine added value is therefore NOT the line count -- it is the
both-names assertion (M3), which is load-bearing, plus the fact that it kept
BOTH assertions, making the pair strictly stronger than either alone.

(4) DEVIATION, WITH THE PROPERTY THAT JUSTIFIES IT. My orders told this kid the
substring count was "a weaker assertion than the claim it is supposed to pin".
That was overstated and the probe disproved it: M2 is a case where the substring
count is the stronger of the two. I record the correction here rather than
re-cutting the kid, because the deliverable asked for (line count + both names)
is present and correct, and the kid's kept-substring choice is what makes the
test cover both M1/M2 and M3. No numbered `(1) (2)` conjuncts exist in this
hypothesis, so cli.py's `_parent_probe_gate` (cli.py:1190-1234) resolves an
empty conjunct set and is inert; I recorded the probes anyway.

caveats: this round adds no production bytes -- the fix is kid 1's, and this
node's `proved` covers an assertion, not new behaviour. Zero-line mutational
coverage means M3 was never observed on a shipped code path, only on a
parent-injected one.
<!-- THOUGHT:END -->

Parent review L5.10 kid 2: test-only round (+20/-5), rotate.py byte-identical to kid 1's (asserted). Probes v1 and v2 run: v1 was MY mis-design (names-only second line is legitimately one message); v2 ALL PASS -- gate (2 surfaces -> 1 line naming both), M1/M2/M3 mutational discrimination, and load-bearing: gutting the names in the real rotate.py FAILS the kid's test, file restored, suite 7 passed. Correction to my own orders recorded: the line count does NOT strictly dominate the substring count (M2), so the kid's real added value is the both-names assertion. Verdict proved accepted.
