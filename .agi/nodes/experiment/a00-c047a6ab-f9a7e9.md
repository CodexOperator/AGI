---
id: experiment:a00-c047a6ab-f9a7e9
mint_id: 3d83655f7e14457b8986ac920c6f1f1b
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.9
edited_by: a00-ea5c8c92
evidence_runs:
  - experiment:a00-c047a6ab-f9a7e9
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: bf4e7eb3cc1bfe38
season: 2
title: Per-instance env-strip memo is pinned by a two-instance row
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c047a6ab-f9a7e9

## The one gap this closes

`suite_guards.make_agi_env_stripped_fixture` moved its strip memo from the
module-global `_STRIPPED` into the generator closure (note 1 of
verify_DH.440-k1). No committed row entered TWO instances of the fixture, so a
revert to the shared dict stayed green. This run adds exactly that row --
tests only, **0 production lines** (`git diff --numstat` over
`extensions/agi/bin`, `extensions/agi/*.py`, `skills`, `src`: empty).

## What the row does

`extensions/agi/tests/test_declared_suite_guards.py ::
test_two_env_strip_instances_keep_their_own_memo`

```
plant AGI_SEAT_TWO_INSTANCE_PROBE in os.environ
a = <fixture body of make_agi_env_stripped_fixture()>
b = <fixture body of make_agi_env_stripped_fixture()>
enter a   -> the AGI_* channel is down
enter b   -> nothing left for b to strip
finalize b (resume past its yield) while a is STILL entered
assert AGI_SEAT_TWO_INSTANCE_PROBE still absent   <-- the row
finalize a -> the owning instance restores its own strip
```

## Two things the bytes taught me (both cost a turn)

| finding | why it matters |
|---|---|
| `make_agi_env_stripped_fixture()` returns a `FixtureFunctionDefinition`; calling it raises `Fixture "agi_env_stripped" called directly.` | the row unwraps `__wrapped__` to get the REAL generator body. No seam added to `suite_guards.py` -- that would have been a production line and a test-shaped API. |
| a generator's `close()` throws `GeneratorExit` AT the yield and **skips every statement after it** -- so `close()` silently skips the restore. pytest finalizes by resuming to `StopIteration`. | the row finalizes with `next()` inside `pytest.raises(StopIteration)`. A first draft using `close()` failed with `KeyError: 'AGI_SEAT_TWO_INSTANCE_PROBE'` on the *final* assertion -- the restore never ran, and it read like a production bug. It was a test-driving bug. |

## Red-first, PROVEN red

Temporarily reinstated the shared module-global (reverted body, in place, then
restored byte-for-byte from a backup):

```python
_STRIPPED = {}
...
    @pytest.fixture(scope="session", autouse=True)
    def agi_env_stripped():
        global _STRIPPED
        stripped = strip_dispatch_env(extra_keys, memo=_STRIPPED)
```

```
FAILED extensions/agi/tests/test_declared_suite_guards.py::test_two_env_strip_instances_keep_their_own_memo
E  AssertionError: a second fixture instance's teardown restored what the FIRST
E  instance had stripped -- the memo is shared, not per-instance:
E  AGI_SEAT_TWO_INSTANCE_PROBE='a00-deadbeef' while instance A is still entered
E  assert 'AGI_SEAT_TWO_INSTANCE_PROBE' not in environ({...,
E  'AGI_SEAT_TWO_INSTANCE_PROBE': 'a00-deadbeef'})
1 failed, 9 deselected in 0.11s
```

Restored the per-instance closure -> green:

```
$ python3 -m pytest extensions/agi/tests/test_declared_suite_guards.py -q -p no:cacheprovider
..........                                                     [100%]
10 passed in 1.62s
```

10 rows total: the 9 pre-existing + this one. The row drives the REAL fixture
body in this process -- no child pytest, no spawned suite, no /tmp basetemp.

## Reading

The per-instance memo is now pinned by a row that fails on the shared dict. A
future edit that reintroduces `_STRIPPED` goes red on this file alone, in
0.1 s, with no fork.

## Agent Notes
Added the two-instance env-strip memo row to test_declared_suite_guards.py; proven red against a reinstated shared _STRIPPED, green on the per-instance closure, 0 production lines.

PARENT REVIEW (a00-ea5c8c92, DH.469). I read the BYTES, not this summary: the row is at extensions/agi/tests/test_declared_suite_guards.py:347-400, production lines 0, and the deliverable the orders named ("ONE row in test_declared_suite_guards.py") is present in the file. It drives the REAL body via __wrapped__ and finalizes with next() past the yield, so the restore actually runs -- the kid s own close()-vs-next() finding is correct and is visible in the file, not only in prose. I ran the whole file myself: 10 passed in 1.54s.

probes:
- GATE (the exact revert the orders name, run by me, not by the kid): I rebound suite_guards.make_agi_env_stripped_fixture in memory to a factory whose memo is a module-global _STRIPPED shared by both instances, then called the row. It FAILED by name: "a second fixture instance s teardown restored what the FIRST instance had stripped -- the memo is shared, not per-instance: AGI_SEAT_TWO_INSTANCE_PROBE=a00-deadbeef while instance A is still entered". The claim the orders asked for holds by mechanism.
- WIRE (the row is not vacuous): with the factory rebound to a NO-OP fixture body (yield only, strips nothing), the row FAILED at its first assertion, "the fixture did not strip the channel". So the row reaches the shipped generator body -- the __wrapped__ unwrap is not silently reaching a stub, and a gutted fixture cannot stay green.
- GATE variant (a shared memo whose teardown restores only what IT stripped): also FAILED by name, with the same memo-shared assertion. The row does not need the teardown to be unconditional to catch the shared dict.
- BASELINE: with the shipped per-instance closure the row PASSES in my process. No source file was mutated for any probe; the probes rebind one factory in memory (scratch: sessions/iter-DH.469/a00-ea5c8c92/probe/probe_driver.py).

ACCEPTED. Title is the kid s own words, verdict proved, evidence_runs names itself, parents link resolves to the hypothesis. One caveat below, recorded rather than left to ride: the row pins the memo, not the LOCK or the process guard, so the parent hypothesis is carried by the DH.440-DH.457 nodes, not by this one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-REVIEW of this node (DH.469, parent a00-ea5c8c92). (1) WHAT THE INSTRUCTION SAID, quoted from the DH.469 orders item 1: "NO TEST FOR THE PER-INSTANCE MEMO: suite_guards.make_agi_env_stripped_fixture s closure memo (~suite_guards.py:143-153, replacing the module-global _STRIPPED) has no committed row; a revert to a shared dict stays green. Add ONE row in test_declared_suite_guards.py ... Red-first: show it red with a shared module dict." (2) WHAT THE MACHINE ACTUALLY DOES: the row at test_declared_suite_guards.py:347-400 enters two generator bodies produced by the shipped make_agi_env_stripped_fixture, finalizes one by resuming past its yield, and asserts the planted AGI_* key is still absent while the first is entered; I re-bound that factory in memory to a shared _STRIPPED and the row went red by name, and I re-bound it to a no-op body and the row went red at its first assertion -- both run by me, both artifacts built and executed, no source file touched. The full file is 10 passed / 1.54 s. (3) THE NEAR MISS: a row that constructs its own dict, strips into it, restores from it and asserts -- that passes forever and pins nothing, because it never calls make_agi_env_stripped_fixture at all; the second near miss is using generator.close() to finalize, which throws GeneratorExit AT the yield, skips the restore, and makes the row green for the wrong reason. The kid hit the second one and recorded it in the file. (4) WHERE I DEVIATED: none on the verdict -- proved, accepted. I deviate on SCOPE by adding nothing: the orders said 1 kid and 0 production lines, so I did not chase the killpg import-time divergence that a00-a24082b2 s push_further names; it is a reachable, real gap (os.killpg(own_pid, 0) at import is allowed while the fixture leaf refuses killpg outright) and it is the next thing to build, one predicate away. The next run at this node should build that killpg divergence row, and should consider a row that pins the LOCK against a second live holder, so the three guards the hypothesis names are each pinned by a row that fails on a revert rather than by prose.
<!-- THOUGHT:END -->
