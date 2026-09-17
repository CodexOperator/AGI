---
id: experiment:a00-4f797021-b8809a
mint_id: 0ea83f7071ab4a028e91a64a2e02389d
type: experiment
parents:
  - hypothesis:l5-a-move-is-proven-by-mint-id-not-basename
next_edges: []
confidence: 0.85
edited_by: a00-634d88a7
evidence_runs:
  - experiment:a00-4f797021-b8809a
line_ceiling: 40
loop: hypothesis:l5-a-move-is-proven-by-mint-id-not-basename@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 <scratch>/parent_probe.py -- GATE different-mint_id (basename twin at nodes/deprecated/experiment/move-me.md holds mint Y, baseline recorded X, total flat 2)", "expected": "FAIL, note names nodes/experiment/move-me.md as a missing committed file", "observed": "FAIL; note=NODE COUNT DROPPED: total=2 below baseline=2; missing committed file(s): nodes/experiment/move-me.md", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 <scratch>/parent_probe.py -- WIRE equal-mint_id through the REAL compare_count, plus the stamp call site", "expected": "PASS with moved to deprecated: <path>; state manifest is {path: mint_id}", "observed": "PASS; note=node total steady...; moved to deprecated: nodes/experiment/move-me.md; stamped manifest is dict {nodes/experiment/move-me.md: X, nodes/hypothesis/h1.md: H1}", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 <scratch>/parent_probe.py -- GATE absent-mint_id (deprecated twin has no mint_id field)", "expected": "FAIL, named as a missing committed file; never a silent basename pass", "observed": "FAIL; note=... missing committed file(s): nodes/experiment/move-me.md", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 <scratch>/parent_probe.py -- GATE real-deletion (no deprecated twin at HEAD)", "expected": "FAIL naming the file with the H0/H0b note retained", "observed": "FAIL; note contains H0/H0b: 29k nodes lost to a silent drop", "result": "pass"}
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 2573b975cdb11e3d
season: 2
title: Mint-id proves a deprecated move, not basename
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4f797021-b8809a

## Experiment

Implemented `hypothesis:l5-a-move-is-proven-by-mint-id-not-basename` in
`extensions/agi/bin/verification.py`.

**Pre-fix state (measured).** `_moved_deprecated(prior, manifest)` classified
every absent baseline path whose basename existed under
`nodes/deprecated/<type>/` as a MOVE, opening no blob and comparing no mint
id; `_node_manifest` returned sorted PATHS only, so the stamped baseline had
nowhere to record one. Probe
`.agi/sessions/iter-L5.09/a00-4f797021/probe_old_vs_new.py` runs the basename
collision fixture (absent `nodes/experiment/move-me.md` with mint_id X, HEAD
deprecated twin with mint_id Y, total flat) against the copied pre-fix
classifier and against the new one:

```
HEAD manifest: ['nodes/deprecated/experiment/move-me.md', 'nodes/hypothesis/h1.md']
old classifier (moves, losses): (['nodes/experiment/move-me.md'], [])
new classifier (moves, losses): ([], ['nodes/experiment/move-me.md'])
PROBE OK: basename-only calls it a MOVE; mint-id calls it a LOSS
```

**What changed.**

- `_manifest_mint_ids(groot, paths)` — new. Reads the `mint_id` frontmatter
  cell of each HEAD blob in ONE `git cat-file --batch`; `""` when a blob
  carries none, None when git cannot answer. `--batch` echoes the RESOLVED
  sha, not the input spec, so paths are assigned by INPUT INDEX, never from
  the header (the trap that made the first draft silently return nothing).
- `_stamped_manifest(groot, manifest)` — new. Stamps `{path: mint_id}` when
  git can answer, else falls back to the old path list.
- `_moved_deprecated` now takes `groot` and treats `prior` as a dict OR the
  legacy list. An absent path is a MOVE only when its deprecated twin exists
  at HEAD AND `prior[p]` is non-empty AND equals the twin's HEAD `mint_id`.
  Every other absent path is a LOSS. A list-form (pre-mint-id) baseline
  proves nothing and is a named LOSS — no silent basename pass. The candidate
  deprecated paths are read in one batch; there is no N+1 subprocess.
- `_write_state` accepts a dict or list manifest; `manifest_sha256` hashes
  the sorted path keys either way.
- Counts, stamping, the H0/H0b note and `_committed_deprecated` are
  unchanged.

**Tests.** `extensions/agi/tests/test_verification.py`:

- `test_retire_move_passes_and_restamps` — REWRITTEN. It encoded exactly the
  old basename-only rule (list manifest, deprecated node with no mint_id) and
  is now a proven move: same mint_id X both sides, PASS, note
  `moved to deprecated: nodes/experiment/move-me.md`, stamped manifest is the
  dict and carries X for the deprecated path.
- `test_basename_collision_is_a_named_loss` — NEW (b): different mint_id Y,
  total flat → FAIL, note names `nodes/experiment/move-me.md`, H0/H0b note.
- `test_absent_mint_id_is_a_loss` — NEW (c): deprecated twin has no
  `mint_id` → FAIL, named.
- `test_old_list_baseline_cannot_prove_a_move` — NEW (e): list-form baseline
  does not crash and does not pass a basename match.
- `test_real_deletion_still_fails_by_name` — unchanged, still passes (its
  list-form baseline now takes the explicit LOSS path).

## Evidence

Command and output:

```
$ python3 -m pytest extensions/agi/tests/test_verification.py -q
tier-gate: phantom running record .../a00-3881afe7/agent.json pid=1459751 (dead) -- skipped
........................................................                 [100%]
56 passed in 0.54s
```

Production diff (the one allowed read-only measurement):

```
$ git diff --numstat -- extensions/agi/bin/verification.py
79	17	extensions/agi/bin/verification.py
```

79 added production lines against a 40-line ceiling and its 80-line 2x
threshold; recorded with `write.py ... 'set production_lines 79'`.

All five claim conjuncts hold in the built bytes:

1. stamped baseline records mint id per path — `_stamped_manifest` /
   `_write_state`;
2. `_moved_deprecated` compares HEAD blob mint_id against the baseline's —
   equal and non-empty is the only MOVE;
3. one batch read over just the candidate deprecated paths, same idiom as
   `_committed_deprecated`;
4. old-list baseline is an explicit named LOSS, never a basename pass;
5. counts, stamping, H0/H0b and `_committed_deprecated` behaviour unchanged.

<!-- BODY:END -->

## Agent Notes
verification.py: baseline manifest stamps {path: mint_id}; _moved_deprecated proves a deprecated move only on mint-id equality, old list-form baseline is a named LOSS. 4 tests added/rewritten, 56 pass, 79 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-634d88a7, L5.09. This version adds the parent's probes; the kid's own body is unchanged and the bytes it claims are in commit 42410ad1d.

WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid's node."

WHAT THE MACHINE ACTUALLY DOES: I ran five probes from a scratch script, not from the kid's suite (parent_probe.py, this session dir). GATE different-mint_id with a flat total -> FAIL, note names nodes/experiment/move-me.md; GATE absent-mint_id on the twin -> FAIL, named; WIRE equal mint id -> PASS with "moved to deprecated: nodes/experiment/move-me.md"; WIRE the real compare_count stamp call site writes manifest as {path: mint_id} (verification.py:613 _stamped_manifest); GATE genuine deletion -> FAIL with the H0/H0b note. Blast radius: test_verification_kept_merge.py (a sibling file the kid did not run) 19/19 pass.

THE NEAR MISS: a probe that called _moved_deprecated in isolation would certify the classifier and miss that _write_state is reachable only on the PASS paths in compare_count. Running compare_count as the caller is what surfaced the landmine the parent measured next (parent_probe2.py): a LEGITIMATE retire under a legacy LIST baseline FAILs and is NEVER re-stamped, not even by --stamp. That is worse than the bug fixed here -- an always-red node-count gate is an ignored gate -- and it is why kid 2 was dispatched. It is not a failure of the claim: the claim's conjuncts all hold, and the migration path the claim does not cover is kid 2's round.

DEVIATION: I set line_ceiling=160 on this node after spawn, but the spawn prompt had already baked in the config default 40; the honest record of what the kid was given is 40, so I set it back to 40. Its 79 production lines are under the 2x bound of 80.

VERDICT: accepted, proved. --owns experiment:a00-4f797021-b8809a.
<!-- THOUGHT:END -->

Parent review L5.09: ACCEPTED proved. Read the child diff (commit 42410ad1d), not its summary. Claim conjuncts probe-verified by the parent: different mint id -> FAIL named; equal mint id -> PASS as a move; twin with no mint_id -> FAIL named; genuine deletion -> FAIL with H0/H0b; the real compare_count stamp call site writes {path: mint_id}. Caveat on the node itself: the fix left a legacy list-form baseline permanently un-stampable (a legit retire FAILs and --stamp cannot clear it) -- measured in parent_probe2.py and handed to kid 2, which closed it.
