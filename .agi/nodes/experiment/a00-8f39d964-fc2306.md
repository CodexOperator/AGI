---
id: experiment:a00-8f39d964-fc2306
mint_id: 59ad83d22af649d78c89e3fb7e8ccfaa
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.8
edited_by: a00-619731a3
evidence_runs:
  - experiment:a00-8f39d964-fc2306
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 6e53a9b8015221a1
season: 2
title: The spawned id set is dispatch-written and expires with its iteration
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-8f39d964-fc2306

## Experiment — kid 1, production bytes only (`extensions/agi/bin/cli.py`)

### 1 · What the instruction said (verbatim from the corrective orders)

> "`_round_spawned_node_ids` returns ids dispatch RECORDED (`dispatch_node_id`
> only) — drop the `rec.get("node_id")` leg — and carries an iteration bound so
> an id a round spawned in an OLD iteration cannot widen a later round's set
> forever. Where the iteration id comes from is yours to choose from what is
> already in hand (`args.iter_n` is in `cmd_done`); no new path literal, no new
> config cell, no hard-coded string."

> "the spawned union is computed only on the route that needs it — i.e. not for
> a round that passed no `--owns` — or is otherwise gated on the parent asking"

### 2 · What the machine ACTUALLY did, measured on the bytes

Fixture: tmp graph, two iteration dirs stamped by the SAME seat name —
`sessions/iter-DH.551/a00-old/agent.json` and
`sessions/iter-DH.552/a00-mine/agent.json`, both
`"spawned_by_agent": "director-engine"`, both carrying
`dispatch_node_id: experiment:a00-<…>-kid` AND `node_id:
hypothesis:kid-writable`. Probe (throwaway, tmp only):
`.agi/sessions/iter-DH.552/a00-8f39d964/probe.py`; the last line inlines the
DH.514 form verbatim so before and after sit on the SAME fixture.

```
$ python3 .agi/sessions/iter-DH.552/a00-8f39d964/probe.py      # POST-FIX
item 4  _round_spawned_node_ids(root,'director-engine','DH.552') = ['experiment:a00-mine-kid']
item 4b two-arg call (no iteration in hand) = []
item 1  ..._spawned_node_ids(root,None) = []
PRE-FIX (inlined DH.514 form) = ['experiment:a00-old-kid', 'hypothesis:kid-writable', 'experiment:a00-mine-kid']
```

The PRE-FIX line is the finding, and it settles items 1, 4, 7, 8 in one run:
a seat-name `spawned_by_agent` over an unbounded `iter-*` glob returned
**another iteration's** kid id, and the `rec["node_id"]` leg returned a
**kid-writable `hypothesis:`** that dispatch never named. Post-fix both are
gone; the seed refusal of DH.514 (no `agent_id` → refuse by name) is untouched
and still returns `[]`.

Bytes changed (one file, `extensions/agi/bin/cli.py`):
- `_round_spawned_node_ids` takes `iter_n` and globs
  `locations.iteration_dir(root, iter_n)` instead of `(root / "sessions").glob("iter-*")`;
  reads `r.get("dispatch_node_id")` only; `iter_n is None` → `[]` (refuses by
  name rather than sweeping the glob). **No new config cell and no new path
  literal** — the iteration id is a value already in `cmd_done` as
  `args.iter_n`, and the dir is reached through `locations.iteration_dir`,
  the one place that spelling lives.
- The call site in `cmd_done` computes the union **only when `args.owns`**:
  `_named = _round_named_node_ids(rec, args.parent)`, then
  `if args.owns: _named = _named + _round_spawned_node_ids(root, args.agent_id, args.iter_n)`.
  This is the item-11 arm: `named` is what exempts an id from the `--node-id`
  SEED guard, so splicing the spawned set in unconditionally armed that
  exemption for a round that never asked for it. Gated, the guard's exemption
  is again only what dispatch itself named.

Production lines: ~24 net added in `cli.py` (2 signature, ~10 of the two
bounds in code, ~10 docstring carrying the mechanism, ~5 at the call site).
Below the 25-line slice ceiling, above zero. I ran no `git` at all — the
number is counted from the edit, not from a numstat read.

### 3 · The near miss

The counterfactual that satisfies the instruction and loses the measurement:
keep the signature `(root, agent_id)`, keep `iter-*`, and add only the
`dispatch_node_id`-only leg. That removes the kid-writable value and still
leaves the seat-name leak — a director seat that spawned a kid in iteration 1
keeps widening its set in iteration 552, forever, because `spawned_by_agent`
is a SEAT name, not a round id. The second near miss: bound the glob to the
iteration but pass `iter_n` as a string literal built at the call site; that
re-spells a path rule code already owns in `locations.iteration_dirname`, and
`paths.py audit` is right to call it. The third: gate the union on `args.owns`
but *also* drop the id from `named` and pass it as a separate
`spawned` argument, so the seed exemption is untouched — larger, for a
separation the `if args.owns` already buys.

### 4 · Deviation from a standing rule

None. `git` was not run at all (not even the permitted numstat read), because
the round-level contract for this seat is "no git"; the line count is therefore
an edit count and is labelled as such above. `extensions/agi/tests/**` and the
two DH.514 node files were not touched — kid 2 owns them.

### RESIDUE, named for the director (not fixed here)

- `extensions/agi/tests/test_round_own_path_set_fails_closed.py:133-156` calls
  `_round_spawned_node_ids` with TWO positional args. Those calls now return
  `[]` by design (no iteration in hand → refuse). **Kid 2 must pass the
  iteration id** — and the fixture's `iter-1` directory is not a spelling
  `locations.iteration_dirname` produces for `1` (it emits `iter-001`), so
  that fixture needs the canonical dir name too, or the bound will read as
  "empty set" for the wrong reason.
- Item 11 with `--owns` PASSED: a parent that asks for `--owns` and passes
  `--node-id <one of its own spawned kids>` still rides the seed exemption.
  I judge that legitimate (that id is a node this round's own dispatch
  created, and a parent round legitimately mints it), and I did not tighten
  it. Left as residue, not claimed closed.

### Suite state on the bytes (kid 2's file, not mine to edit)

```
$ python3 -m pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py -q
E  AssertionError: assert [] == ['experiment:a00-kid-1']
   extensions/agi/tests/test_round_own_path_set_fails_closed.py:133
1 failed, 6 passed
```

That one failure IS the residue above: the fixture calls the helper with no
iteration in hand, and the new contract refuses by name instead of sweeping
`iter-*`. The other six pass, so the DH.514 seed refusal and the `--owns`
refusal-by-name messages are intact.

## Agent Notes
spawned id set now reads dispatch_node_id only and is bounded to the round's own iteration dir; union computed only when --owns passed; probe output pasted on node

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.604 rewrite. This node had no reasoning block at all -- its review paragraph was sitting in the BODY, under Agent Notes, where it looked like a note and was read as a note. It is reasoning, so it lives here now, and what it says is only about this node.

WHAT THIS NODE CLAIMED AND WHY IT IS ONLY A LEAN: the set of ids a round may sweep should come from what dispatch recorded, and it should stop being usable once the round moves on. It took the dispatch_node_id field only, dropped the fallback onto the child own node_id line, added an iteration bound, and computed the union only when --owns was actually passed. Honest verdict: the shape is right, one conjunct is not fully closed.

THE PART OF IT THAT WAS STILL OPEN, and the part every later reader should know about: item 11 with --owns still passed. A parent that asks for --owns and simultaneously passes a --node-id naming one of the kids it spawned rides the seed exemption rather than the --owns guard. This node judged that legitimate, argued why, and did not tighten it. That judgement is the reason the current tip still carries a seed exemption, and it is named again in the DH.604 block on the node that owns the pin, so the exemption does not quietly become a closed item.

THE OTHER HALF OF THIS NODE IS A LESSON, not a mechanism. Its suite state shows a single failure, and the node is right that the failure is the fixture: the helper was called with no iteration in hand, so the new contract refused by name and returned an empty set -- identical to what a correct bound returns. This node wrote the residue down instead of quietly widening the glob to make it green, and that is the whole reason the bound is trustworthy now. The successor fixed the fixture. The trap survives in a second form: the same file re-spelled the sessions path segment by hand, which is one more way for a query to mean something other than it looks, and it also left a RED-proof seam in place that the suite quietly disarmed -- the same mutated cli.py measured 8 passed from inside extensions/agi/tests and 1 failed from outside it. Both are closed now, and the skip that replaces the seam is a refusal to answer, not a proof.

STILL OPEN: the seed exemption above, and the caveat that an empty result from a mis-shaped call is indistinguishable from a correctly closed door.
<!-- THOUGHT:END -->
