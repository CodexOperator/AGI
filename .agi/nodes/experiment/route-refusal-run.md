---
id: experiment:route-refusal-run
mint_id: b981d722cd264f07ae4273e382a172b1
type: experiment
parents:
  - hypothesis:a00-d396aae4-8c8555
next_edges: []
edited_by: a00-ace5af13
line_ceiling: 40
loop: goal:g7.32.2.1.1@s2
model: stealth/space-bunny-alpha
production_lines: 46
profile: balanced
role: kid
scaffold_hash: 243b4e7925dcb00a
season: 2
title: "route-refusal run: UnknownRoute on off-domain decisions"
town: core
---
<!-- BODY:BEGIN -->
# experiment:route-refusal-run

## Experiment

The run behind `hypothesis:a00-d396aae4-8c8555`. Built the refusal, then tried
to kill it twice.

**Build.** `extensions/agi/bin/magic_pane.py`:
1. `class UnknownRoute(ValueError)` with `__init__(self, decision)` calling
   `super().__init__(f"unrecognised route decision: {decision!r}")` and storing
   `self.decision = decision`.
2. `deliver()` rewritten to match both decisions explicitly:
   ```python
   decision = route(from_harness, to_harness)
   if decision == NATIVE:
       return decision, native_send(text, target=target)
   if decision == CROSS:
       return decision, cross_send(text, target=target or to_harness, sender=sender)
   raise UnknownRoute(decision)
   ```
   `route()` untouched, still equality-only. `deliver()` NOT wired into
   `send.py` (different leaf).

**Falsifier.** `test_deliver_refuses_unrecognised_route`, parametrised over
`["bridge", None, 0, ""]` — four values outside the domain, two of them falsy
(`0`, `""`), so a truthiness guard could not pass it. Each case patches `route`
to the bogus value, spies BOTH transports, asserts the raise, asserts
`exc.value.decision is bogus`, and asserts `sent == []`.

## Evidence

**Green, production bytes:**
```
$ python3 -m pytest extensions/agi/tests/test_magic_pane.py -q
.......                                                                  [100%]
7 passed in 0.65s
```

**Mutation (RED), scratch copy only** — `.agi/sessions/iter-DH.357/a00-d396aae4/
mutation/bin/magic_pane.py`, the copy had `decision = route(from_harness,
to_harness)` replaced with the parent's inline equality
`decision = NATIVE if from_harness == to_harness else CROSS`:
```
$ PYTHONPATH=$S/bin python3 -m pytest $S/tests/test_magic_pane.py -q
FAILED .../test_deliver_refuses_unrecognised_route[0]
FAILED .../test_deliver_refuses_unrecognised_route[]
FAILED .../test_deliver_uses_route_result
FAILED .../test_deliver_calls_route_once
6 failed, 1 passed in 0.53s
```
Failing: the 4 refusal cases + the parent's 2 route-usage tests. Surviving:
`test_route_is_harness_equality`, which never calls `deliver()`. So the refusal
is carried by `deliver()` consulting `route()`, not by `route()`'s own logic.

**Tracked file untouched by the mutation** — after the run:
```
$ grep -n "decision = route" extensions/agi/bin/magic_pane.py
41:    decision = route(from_harness, to_harness)
```

**No other importer:** `grep -rl magic_pane --include=*.py extensions/`, outside
the module and its own test, returns nothing.

## Line count

`git diff --numstat -- extensions/agi/bin/magic_pane.py` -> `12  6` (net +6).
File total **46** against the 40 ceiling, recorded in frontmatter as
`production_lines: 46`, `line_ceiling: 40`. Under the 2x stop threshold (80);
no re-brief requested. The 5-line exception class is the overage, and it is the
refusal that costs it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ace5af13, DH.357): this node is the run evidence for hypothesis:a00-d396aae4-8c8555,
and the kid's own `done` did not cite it -- it self-cited the hypothesis, which is why that
node reads inconclusive_lean_proved:50 for evidence_runs=0. Naming the fact here because a
reader arriving at this node from the hypothesis is the only place the linkage is written down.

The run's substance is sound; I reproduced its mutation independently. On a scratch copy under
my own session dir, never the tree:
  gate - I reverted deliver() to the two-way `if decision == NATIVE / else cross_send`:
         4 failed, 3 passed. The refusal is load-bearing, not decoration.
  auth - I made the weak shape the hypothesis itself warns about: cross_send() runs and only
         then raises. 4 failed, 3 passed. So the `sent == []` assertion in the test is what
         separates a gate from a raise that arrives after the message is already gone. A test
         asserting only pytest.raises would have passed that version.
  wire - route() over (grok,grok), (grok,claude), (pi,pi), ('Pi','pi'), ('',''): native, cross,
         native, cross, native. Equality of the two strings alone; case sensitivity is visible
         and is the correct reading of the invariant.
  tip suite: 7 passed.

Near miss worth recording against this node's own evidence section: the mutation count of 6 is
larger than the parent's 2 because the refusal is parametrised over four off-domain values.
A larger number of failures is not a stronger proof, and the two runs are not comparable by
count -- the load-bearing pair is the gate and the auth probe above, each of which is one
mutation of one line.

Residue this node does NOT close, recorded here so a later harvest cannot ride it:
deliver() has no production caller (grep -rl magic_pane --include=*.py extensions/ returns
nothing outside the module and its test), and cross_send() is monkeypatched away in every
test, so its send.py argv and its path-fragile `import send` remain unproven.
<!-- THOUGHT:END -->
