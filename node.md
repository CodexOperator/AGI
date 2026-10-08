---
id: experiment:a00-247b3d01-7eca66
mint_id: a4d736e993d943b49d95afd5d61f8326
type: experiment
parents:
  - hypothesis:l4b23-promptfile-drop
next_edges: []
confidence: 0.85
edited_by: a00-e50bd786
evidence_runs:
  - experiment:a00-247b3d01-7eca66
loop: hypothesis:l4b23-promptfile-drop@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1251aa186ff20ad1
season: 2
title: A00 247b3d01 7eca66
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-247b3d01-7eca66

## Experiment

Decision: **took (b) — refuse loudly.** `dispatch.py --tier parent
--prompt-file X` now exits 2 with a clear stderr message instead of silently
discarding X.

## Why (b) and not (a): the design says the prompt-file channel is kid-only

- `_read_prompt_file` docstring (dispatch.py:617): "The text is passed as the
  **KID'S** `addendum` brief segment".
- `--prompt-file` help text (dispatch.py): "**per-kid brief channel** ...
  threaded into the spawned kid's brief as its OWN labelled segment".
- `_kid`'s addendum label (brief.py:1091): "WHAT THE LAST KID PRODUCED --
  **from your parent**, not from the node" — parent→kid carry-forward.
- `_parent`'s docstring (brief.py:1206): "A loop, not a node" — the parent's
  brief is built fresh from its target node each dispatch; it authors no node
  and consumes no prior work-product the way a kid does.
- The existing test `test_parent_brief_names_the_carry_forward_lever`
  (test_brief.py:196) names `--prompt-file <path|->` as the lever the PARENT
  USES when cutting KID spawns — never something the parent consumes itself.

So threading an addendum into `_parent` (option a) would graft a
kid-semantics segment onto the parent's loop brief for a channel that was
never meant to apply there. Refusal (b) is the honest fix: it is
recoverable at arg-parsing time, before any lease/session dir, and cannot
break a working flow because the old behaviour (silent discard) meant nobody
could have relied on it.

## Code change

`extensions/agi/bin/dispatch.py`, right after the `--role` default block
(before `goal:g11.1` root resolution, so it fires argument-parsing-early,
exit 2, no lease, no iter dir):

```python
    # hypothesis:l4b23-promptfile-drop — `--prompt-file` is the per-KID
    # carry-forward channel (see _read_prompt_file and the --prompt-file
    # help: "threaded into the spawned kid's brief"). A PARENT's brief is
    # built fresh from its target node every dispatch and consumes no
    # carry-forward (brief.assemble() threads addendum into _kid but never
    # into _parent), so `--tier parent --prompt-file X` read X's bytes and
    # silently threw them away. Refuse loudly at argument-parsing time
    # instead of accept-and-drop. The parent says --prompt-file on the KID
    # spawns it cuts, not on its own dispatch.
    if args.tier == "parent" and args.prompt_file is not None:
        print("--prompt-file is a per-KID carry-forward channel and does not "
              "reach a parent's brief (a parent's brief is built fresh from "
              "its target node every dispatch). Pass it to the KID spawns "
              "the parent cuts, not to the parent dispatch itself. Refusing "
              "rather than silently discarding "
              "(hypothesis:l4b23-promptfile-drop).", file=sys.stderr)
        return 2
```

## Verify commands + actual output

Scratch prompt file:
```
echo "DISTINCTIVE PROMPT MARKER l4b23-test" > /tmp/pf_test.txt
```

(1) AFTER the fix — parent + prompt-file refused:
```
$ python3 extensions/agi/bin/dispatch.py . 999 --target hypothesis:l4b23-promptfile-drop \
    --tier parent --harness pi --dry-run --prompt-file /tmp/pf_test.txt
--prompt-file is a per-KID carry-forward channel and does not reach a parent's brief (a parent's brief is built fresh from its target node every dispatch). Pass it to the KID spawns the parent cuts, not to the parent dispatch itself. Refusing rather than silently discarding (hypothesis:l4b23-promptfile-drop).
EXIT=2
```
The distinctive text is NOT in the printed brief — it never reaches a brief.

(2) No-regression — parent WITHOUT prompt-file still assembles (exit 0,
"no budget slot taken"), i.e. refusal is scoped strictly to the flag pair,
not parents in general.

(3) No-regression — kid + prompt-file still threads the addendum: the
recorded command shows the `WHAT THE LAST KID PRODUCED` labelled segment;
verbatim carry is pinned by the pre-existing `test_kid_addendum_lands_as_a_
labelled_segment_and_names_the_flag`.

## New test (in extensions/agi/tests/test_dispatch_dry_run.py)

`test_parent_prompt_file_is_refused_and_never_silently_dropped` runs
dispatch.py as a real subprocess against the scratch `project` fixture,
asserts returncode 2, the refusal text in stderr, and that the marker text
does not leak into stdout.

## Test results

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_brief.py -q
101 passed in 5.49s

$ python3 -m pytest extensions/agi/tests/ -q
2271 passed, 1 skipped in 130s
```

## Evidence

Before attempting any fix, the drop was confirmed in code (not guessed):
`assemble()` (brief.py) receives `addendum=` from all three dispatch call
sites tier-blind, but its `tier == "parent"` branch calls `_parent(...)`
with no `addendum`, and `_parent` has no `addendum` parameter — the bytes die
on the floor. After the fix, the combined flag is refused loudly at
argument-parsing time, which resolves the testable claim ("reaches the
parent brief, **or is refused loudly** — never silently dropped").

## Agent Notes
Took option (b): dispatch.py now refuses --tier parent --prompt-file loudly (exit 2) at arg-parsing time instead of silently discarding the addendum. Decided (b) over (a) from docstring evidence that --prompt-file is the per-KID carry-forward channel (_read_prompt_file: 'the KID's addendum'; _kid label 'from your parent'; parent brief built fresh from its target, authors no node). Added refusal guard in dispatch.py + test_parent_prompt_file_is_refused_and_never_silently_dropped in test_dispatch_dry_run.py. Verified: parent+prompt-file exits 2 with clear stderr; parent alone still exits 0; kid+prompt-file still threads the addendum. 101 (target files) + 2271 full suite pass.

Parent review (a00-e50bd786, L4.30): ACCEPTED as proved. Verified the refusal guard exists in dispatch.py (~line 913) and the new test passes (12 passed in test_dispatch_dry_run.py). parents resolves to hypothesis:l4b23-promptfile-drop; evidence_runs=[self], valid; verify commands with real before/after output present in body. Option (b) justification is code/docstring-evidenced, not guessed. No demotion needed.
