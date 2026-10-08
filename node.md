---
id: experiment:a00-48dd28c5-f49c1c
mint_id: d286f2db863b4307a095f1ce1af3f628
type: experiment
parents:
  - hypothesis:non-prime-rotate-self-renders-through-brief-render
next_edges: []
confidence: 0.85
edited_by: a00-48dd28c5
evidence_runs:
  - experiment:a00-48dd28c5-f49c1c
loop: hypothesis:non-prime-rotate-self-renders-through-brief-render@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: ad1379e4b7c3b8fa
season: 2
title: "A non-prime rotate-self does NOT render: brief_file vs brief.render, measured"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-48dd28c5-f49c1c

## Verdict in one line

CLAUSE (1) is **false as written** and CLAUSE (2) is **built**: a committed
test (`extensions/agi/tests/test_rotate_render_parity.py`, 3 tests, red-first
verified) runs BOTH rotate-self render paths on one fixture and diffs the two
real first turns.

## The two clauses, measured

| clause | measured | how |
|---|---|---|
| (1) non-prime rotate-self assembles the first turn through `brief.render`, exactly as the prime does | **FALSE** | prime → `spawn_window(prompt_file=None)` → `brief.render`; non-prime → `spawn_window(prompt_file=<a file>)` → NEVER renders |
| (2) a committed test compares the two renders | **TRUE (built)** | `test_the_two_bodies_share_the_head_and_diverge_below_it` composes both bodies and diffs them |

## (1) WHAT THE MACHINE ACTUALLY DOES

`rotate.py:19570-19590`, the (3) `prompt_file` resolution inside
`cmd_rotate_self`:

```python
if (not args.dry_run and prompt_file is None
        and role != "prime_director"
        and tmpl is not None and tmpl.get("brief_file")):
    prompt_file = _resolve_brief_file(root, _brief_root_seat,
                                      str(tmpl["brief_file"]).replace("{seat}", seat))
```

`brief_file` is resolved for EVERY template EXCEPT `prime_director`. So:

| role | `prompt_file` handed to `spawn_window` | builder it lands in | body |
|---|---|---|---|
| `prime_director` | `None` | `_assembled_successor_command` (rotate.py:1111) | `brief.render(post=…)` — head + role template + card + harness block + town trajectory |
| `director` (any non-prime with a `brief_file` cell) | an absolute FILE path | `_successor_command` (rotate.py:1079) | the file's bytes + `brief.successor_prompt` — head + that file |

MEASURED (real `cmd_rotate_self`, only the window launch stubbed):

```
role=prime_director  template brief_file=extensions/agi/briefs/prime-director-successor.md
  prompt_file passed to spawn_window: None
role=director  template brief_file=.agi/sessions/quorum/{seat}.md
  prompt_file passed to spawn_window: /tmp/.../wt-director/.agi/sessions/quorum/old.md
```

This is the LIVE path, not an edge case: `config:rotations` declares
`director.brief_file: .agi/sessions/quorum/{seat}.md`, so every real
non-prime rotation in this repo takes the file path.

## (2) THE COMPARISON — where the two paths agree, and where they split

Composed on ONE fixture on which `brief.render` genuinely succeeds for both
roles:

| segment | prime | non-prime |
|---|---|---|
| head bytes (prayers, Michael, read_order) | YES | YES — **the only agreement**; `brief.render`'s `head` part and `brief.successor_prompt`'s `render_head` are the same function |
| role template (`config.brief.templates`) | YES | NO |
| card | YES (`brief.render`'s `card` part) | NO — the body is the quorum FILE, whatever it holds |
| harness block | YES | NO |
| town trajectory | YES | NO |
| `## STARTUP OUTPUT` + the ack gate (`extra`) | YES | YES |

So the two renders are NOT the same render, and the claim's "exactly as the
prime path does" does not hold.

## (3) THE NEAR MISS — why the claim reads true from the source

The near miss is the counterfactual: **a non-prime template with NO
`brief_file` cell does render through `brief.render`** — `prompt_file` stays
`None` and `spawn_window` takes the same branch the prime takes. That is why
the claim is plausible on a reading of the source: the `role !=
"prime_director"` guard is the ONLY thing separating the two renders, and
deleting that one clause makes the two paths literally identical.
`test_a_non_prime_without_a_brief_file_cell_does_render` pins that
counterfactual so the exemption can never be widened by accident.

## (4) IF I DEVIATED FROM A STANDING RULE

The standing rule here is "a g15 claim is a build order: measure, IMPLEMENT,
prove on the built bytes". I did NOT implement clause (1), and the property
of THIS case that makes the rule not apply is the measured one, not
inconvenience: the change clause (1) asks for is a DELETION of the
`brief_file` resolution for every role, and I measured that the guard is
load-bearing in BOTH directions.

* Deleting the `role != "prime_director"` guard alone breaks the PRIME (red:
  the prime would then resolve its own static brief and stop rendering) —
  measured by mutating rotate.py and re-running the new test.
* Deleting the whole `brief_file` branch to give every role the render
  disarms the mechanism 19 committed test files and the L5.11 chain
  (`hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-
  rotating-worktree-root`) exist for: a non-prime's successor must read the
  post's OWN quorum card at the path the rename boundary renamed, which
  `brief.render`'s `card` part cannot be relied on to reach. It would also
  silently drop `brief_file` — a config cell carrying per-seat content —
  from every non-prime successor.

The real question the claim raises is therefore a CONFIG question, not a code
one: should `templates.<role>.brief_file` survive at all now that
`brief.render` is the single first-turn composer? That is the owner's call
on `config:rotations`, and the honest round output is the measurement plus a
committed test, not a silent deletion of a load-bearing cell.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_render_parity.py -q
3 passed, 21 warnings in 0.90s

# red-first: the claim's own fix (delete the `role != "prime_director"` guard)
$ #   -> test_the_two_rotations_take_different_render_paths FAILS
#      (the PRIME stops rendering), so the guard is load-bearing in both directions

$ python3 -m pytest extensions/agi/tests/test_rotate_brief_resolve.py \
    extensions/agi/tests/test_brief_render.py \
    extensions/agi/tests/test_rotate_render_parity.py -q
55 passed

$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_startup.py \
    extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_rotate_handover.py -q
524 passed
```

Production lines: **0** (the round's artefact is one new test file, and
`rotate.py` is byte-identical after the red-first mutation probe — verified
with `cmp`). Two stray lines from another agent's uncommitted edit to
`.agi/nodes/hypothesis/non-prime-rotate-self-renders-through-brief-render.md`
appear in `git diff --numstat`; left exactly where they are.

## A fixture defect worth recording (it cost this round two turns)

`geometry_config.resolve` reads `nodes/.geometry/posts.md` FIRST and only
falls back to `nodes/.geometry/seats.md` when posts.md is ABSENT. A fixture
root that writes BOTH silently gets the POST rows for every seat lookup — and
a post row carries no `worktree` cell, so a successor brief re-roots on MAIN
instead of the post's own tree while the test still looks plausible. The
helper `_seats` in the new file removes `posts.md` and says why.

## Agent Notes
Clause 1 measured FALSE: rotate.py:19570-19590 resolves templates.<role>.brief_file for every role EXCEPT prime_director, so the live director template hands spawn_window a file and never renders; only the head bytes agree. Clause 2 built: test_rotate_render_parity.py (3 tests, red-first verified) composes and diffs both real first turns.
