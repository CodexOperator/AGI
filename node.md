---
id: experiment:a00-78af34ab-55e826
mint_id: c2a8e9cd55444a96881573264cefba7d
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.88
edited_by: a00-d74c1e04
evidence_runs:
  - experiment:a00-78af34ab-55e826
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "live bytes, REAL .agi root: _round_own_node_paths(root, root, node_id=\"hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent\", owns=None, named=[], agent_id=\"a00-78af34ab\") -- an EXISTING foreign hypothesis the round never minted, on the kid own --node-id, agent id in hand", "expected": "refused and NAMED on stderr (this is the probe kid 1 failed)", "observed": "[] with: round-commit gate: refusing hypothesis:a-rounds-... - a --node-id seeds this round commit only if dispatch named it or its filename carries the agent id", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "the two regressions everyone fears, live: (a) the round own minted node experiment:a00-78af34ab-55e826 with named=[] and agent_id in hand; (b) the round own node when it IS its dispatch target (human slug) and therefore IS in named", "expected": "both land", "observed": "(a) nodes/experiment/a00-78af34ab-55e826.md; (b) nodes/hypothesis/a-rounds-....md -- both in the set, neither refused", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "live, REAL .agi root: _round_own_node_paths naming doc:geometry-towns-core, command:commands, cron:crons, ladder:ladder, config:posts, goal:g7, doc:unified-goals, town:local-maxxing; plus _round_committable(doc:geometry-towns-core)", "expected": "every one refused by name; the towns table is the case kid 2 missed", "observed": "only the round own experiment node returned; stderr names all eight; _round_committable(doc:geometry-towns-core) = False (was True under 2e1813bf4)", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "no over-refusal: _round_own_node_paths naming hypothesis:tgt, doc:goals-preamble, experiment:a00-23213e43-66d8da", "expected": "ordinary graph nodes still land", "observed": "all three returned, empty stderr", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "edge I did not author and the kid did not claim: the SAME foreign --node-id with agent_id=None (a direct call / a test fixture, never the done path)", "expected": "note the shape", "observed": "the foreign hypothesis is still swept, in silence -- the guard is skipped when no agent id is in hand. cmd_done always passes args.agent_id, so the live path is closed; a caller that omits it keeps the old behaviour by the kid own stated design", "result": "caveat"}
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 1668461135066a63
season: 2
title: the --node-id seed and the structural join are both refused, and both regressions stay green
town: core
verdict: inconclusive_lean_proved:88
---
# experiment:a00-78af34ab-55e826

## Both measured residues, one round, on the live bytes

| # | residue | pre-fix probe (red) | post-fix |
|---|---|---|---|
| a | the `--node-id` SEED | `_round_own_node_paths(r, r, "hypothesis:foreign", None, ["experiment:a00-me-1"])` -> `{nodes/hypothesis/foreign.md, nodes/experiment/a00-me-1.md}`, **stderr empty** | `{nodes/experiment/a00-me-1.md}` + `refusing hypothesis:foreign — a --node-id seeds this round's commit only if dispatch named it or its filename carries a00-me's agent id` |
| b | the structural JOIN | `_round_committable(<real .agi>, "doc:geometry-towns-core")` -> **True**; `_round_own_node_paths` -> `{nodes/.geometry/towns/core.md}`, **stderr empty** | `False`; `set()` + `refusing doc:geometry-towns-core — not round-committable` |

Probe: `extensions/agi/bin/cli.py` read only, tmp roots (real `.agi/context/schemas` COPIED in, and the real `.agi` for the `doc:` reading). No git, no live `done`.

## The two fixes (extensions/agi/bin/cli.py, the two helpers + the one call site)

**Residue (a) — the seed.** `node_id` is the KID's line. It is admitted into `own_paths` only if DISPATCH named that id (it is in `named`) or the resolved node file's basename carries this round's agent id — the same agent-id rule `_round_scope_ok` applies, which the seed used to short-circuit. `agent_id` is a new keyword-only-in-practice parameter, threaded from `_auto_commit_worktree` (which already has it). With **no** agent id in hand (a direct call, a fixture) the pre-existing behaviour stands and the type gate still runs; the real `done` path always has one.

**Residue (b) — the join.** The structural rule guessed: "a dotted dir of `nodes/` holding a file whose STEM equals the id's type or slug". The real seat table is `doc:geometry-towns-core` at `nodes/.geometry/towns/core.md` — type `doc`, stem `core`, two levels down — so nothing matched and the seat table was swept in silence. The join is now the real one: resolve the node FILE BY ID (`_find_node_file`, the reader already in hand) and refuse when the resolved path runs under a dotted directory of `nodes/`. The `structural: true` schema cell stays; the stem guess stays as the FALLBACK for an id no file resolves (a fixture, a type minted this run) — it can over-refuse, never under-refuse.

## The near miss, named

Both times the words were satisfied and the MECHANISM lost. "The named set reads only dispatch-time ids" while the `--node-id` FLAG seeded the commit by a second path; "a structural dir is denied" while the join that finds the file was a name guess. **Counterfactual:** any future reading of this code that re-adds a second, ungated route into `own_paths` (a new flag, a new record key, a new heuristic on the id string) re-opens the same hole with the prose unchanged — the named set is only as strong as the ONE place that decides membership.

## Regressions proven green (the cases everyone fears)

1. a kid's own minted scaffolded experiment (`experiment:a00-me-1.md`, dispatch named nothing) — lands;
2. a PARENT whose own node is a human slug (`hypothesis:a-rounds-named-node-set`) that DISPATCH named — lands;
3. a hypothesis round editing its own dispatch target in place (`--node-id` differs from `target`, but dispatch named it) — lands;
4. `seats:cadence` under `nodes/.geometry/` with no resolvable id path — still denied by the stem fallback; `doc:goals-preamble` still committable.

## Tests

| test id | red on old bytes | green on new |
|---|---|---|
| `test_cli.py::test_node_id_seed_needs_dispatch_or_the_agent_id_in_the_filename` | FAILED | passed |
| `test_cli.py::test_a_node_under_a_dotted_nodes_dir_is_never_round_committable` | FAILED | passed |

Red was measured by inverting both hunks in a scratch copy of `cli.py` (no git), running the two ids, restoring. Whole file: **`python3 -m pytest extensions/agi/tests/test_cli.py -q` -> 70 passed** (68 before these two).

production lines: `git diff --numstat -- extensions/agi/bin/cli.py` = **48 added / 12 removed** (ceiling 40, over 2x would have forced a re-brief; it is not).
# experiment:a00-78af34ab-55e826

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Both DH.414 residues fixed in cli.py: the --node-id seed now needs a dispatch-time id or the round's agent id in the basename (named on stderr when refused), and the structural gate joins the dotted dir to the id by resolving the file (_find_node_file) instead of guessing from the stem. 2 new tests red on old bytes / green on new; test_cli.py 70 passed. 48 added / 12 removed production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d74c1e04, DH.414) -- diff 2e1813bf4..3251dd214 read byte by byte, then five probes of my own on the live bytes against the REAL .agi root. Its suite is reported, not trusted: 70 passed in test_cli.py, which I ran once as a regression read, not as evidence.

WHAT THE ORDER SAID: "node_id may seed the round own paths only if it is a DISPATCH-TIME id or the node file basename carries this round agent id ... judge it, NAME it on stderr as refused, and do not sweep it"; and "resolve the node FILE BY ID and refuse when the resolved path is under a dotted directory".

WHAT THE MACHINE DOES, each conjunct measured:
(1) _round_own_node_paths takes a new agent_id (passed by _auto_commit_worktree from cmd_done) and, for nid == node_id not already in `named`, refuses unless the resolved node file basename carries the agent id. Probe: an EXISTING foreign hypothesis on --node-id, not dispatch-named, agent id in hand -> [] and "round-commit gate: refusing hypothesis:a-rounds-... - a --node-id seeds this round commit only if dispatch named it or its filename carries ...". That is exactly the probe kid 1 failed, now closed at the second path.
(2) _round_committable now resolves the node by id first (_find_node_file) and refuses when the resolved path runs under a dotted dir, keeping the stem guess only as the no-file fallback. Probe: doc:geometry-towns-core -- the seat table kid 2 let through -- is now False, and a named set carrying eight forbidden ids (geometry towns/commands/crons/ladder, config:posts, goal:g7, doc:unified-goals, town:local-maxxing) returns only the round own node, each refusal NAMED.
(3) The regressions I went looking for, all three on the live bytes: the round own minted node lands with named=[] (the agent-id branch admits it); the round own node that IS its dispatch target lands through the `named` branch; hypothesis: / doc: / experiment: ids are not over-refused.

THE NEAR MISS, avoided: "check the seed against the type gate" (what kid 1 shipped) satisfies "the --node-id cannot widen" for goals and towns and loses it for hypothesis, because hypothesis IS round-editable and the type gate is not an authorship test. And "match the structural dir by file stem" (what kid 2 shipped) denies the three type names and loses the furniture the graph actually stores as a doc: node. The two fixes that hold are the two that ask WHERE a thing came from (dispatch record) and WHERE a file LIVES, not what it is called.

ONE CAVEAT, recorded on the node: with agent_id absent (a direct call, a fixture) the seed guard is skipped and a foreign --node-id still sweeps in silence. cmd_done always supplies args.agent_id, so no live path is open; a future caller that forgets it re-opens the hole. The honest hardening is to default the missing agent id to the round record rather than to "no check".

VERDICT: accepted, inconclusive_lean_proved:88 -- every conjunct I could construct against the live bytes holds, the two measured residues of DH.390/411 and of PASS 9 are closed, and what remains is the agent_id-absent edge plus the never-exercised live `cli.py done` path (all probes were helper-level in tmp/real roots, per the standing no-live-done rule).
<!-- THOUGHT:END -->
