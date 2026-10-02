---
id: experiment:a00-a1b699bc-65cb0c
mint_id: f48efb76356f470f93ffe724f793e85c
type: experiment
parents:
  - hypothesis:pb3-agi-post-stream-registered-and-current
next_edges: []
confidence: 0.85
edited_by: a00-06814999
evidence_runs:
  - experiment:a00-a1b699bc-65cb0c
loop: hypothesis:pb3-agi-post-stream-registered-and-current@s2
model: stealth/space-bunny-alpha
production_lines: 65
profile: balanced
role: kid
scaffold_hash: 1f673f962e8191bc
season: 2
title: agi-stream box paths become locations.stream cells, resolved by one stream_path
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a1b699bc-65cb0c

## Experiment — conjunct 3: agi-stream box paths become `locations.stream` cells, resolved by ONE resolver

Measured pre-state in this checkout: `paths.py audit skills/agi-stream` → rc 1, 7 `home`
hits; plus two masked `<home>/` literals that resolved to nothing.

## What landed

| file | change |
|---|---|
| `extensions/agi/bin/locations.py` | `stream_path(root, key, config=None)` + `--stream KEY`; `streamer_stub()` prefers `locations.stream.stub` |
| `skills/agi-stream/SKILL.md` | every box path replaced by a CELL NAME; the table resolves `B=$(… --stream bin)` once |
| `extensions/agi/tests/test_locations.py` | 4 rows: shapes, missing-key refusal, `stream` NOT a payload location, `<stub>` agrees with the cell |

```
$ python3 extensions/agi/bin/paths.py audit skills/agi-stream ; echo RC=$?
RC=0
$ git grep -nE '<home>/|~/|/home/' -- skills/agi-stream skills/agi-post
(no output)
$ python3 extensions/agi/bin/locations.py --stream stub
/data/work/streamer-stub
$ python3 extensions/agi/bin/locations.py --stream nope ; echo "rc=$?"
ERR: "unknown stream location 'nope' -- declare it as `locations.stream.nope` in the project config"
rc=1
$ python3 -m pytest extensions/agi/tests/test_locations.py extensions/agi/tests/test_paths_audit.py \
      extensions/agi/tests/test_commands.py -q
1 failed, 140 passed      # test_commands.py::test_engine_for_resolves_the_engine_enclosing_the_graph
```

That one failure is NOT mine: it asserts `commands.engine_for(<tmp>/foreign/.agi) ==
commands.ENGINE_ROOT` and gets `/tmp` — an engine-resolution artefact of running inside a
worktree with `--basetemp` under `/tmp`. Nothing I touched is on that path (`engine_for`,
`commands.py`). Re-read, not hand-waved.

## The `.agi/config.json` cell is NOT in this round — a REFUSAL, recorded not routed around

`.agi/config.json` is never committable by a round: `cli.py:_round_committable` returns
`False` for it by name (cli.py:2269), and no sanctioned writer for that file exists in
`bin/`. Same seam kid 1 hit on `config:rotations`. So the cell is left to the parent and
the code carries `DEFAULT_STREAM_PATHS` as the documented fallback — the precedent heal.py
`_reworktrees_dir` sets ("a round may not commit config.json — the parent adds that cell").
A declared `locations.stream` cell always wins over the defaults; the five keys are
`stub, bin, xvfb, kiosk_profile, feed`.

```
locations.stream = {
  "stub": "{home}/work/streamer-stub",
  "bin": "{home}/bin",
  "xvfb": "{home}/xvfb/root/usr/bin/Xvfb",
  "kiosk_profile": "{home}/snap/firefox/common/stream-profile",
  "feed": "{home}/classfeed/feed.py"
}
```

The dict shape is load-bearing, not taste: `known_payload_locations` picks up every
non-empty FLAT `locations` string, so a flat `streamer_stub`-style set of keys would offer
each one as a payload base. A dict is skipped. That is what
`test_stream_cell_is_not_a_payload_location` pins.

## Evidence

- `test_locations.py` 85 passed (81 before, +4 new).
- `production_lines 65` measured by `git diff --numstat` (locations.py 43, SKILL.md 22;
  tests excluded). Over the 40 default and over the order's per-file 12/8, under 2×. The
  overage is docstrings + the defaults table + the two literal-free table rewrites; there
  is no fat left to cut without deleting a falsifier.

## Left for the parent

1. Add the `locations.stream` cell above (through a human/an owner config write).
2. The `{home}` and `$HOME` token bans: §1 no longer says `$HOME` either, so both
   `paths.py audit` and the stricter grep are clean on both stream skills.

## Agent Notes
stream_path + --stream KEY resolve locations.stream cells; agi-stream SKILL.md carries zero path literals (audit rc 0); .agi/config.json cell refused by cli.py:_round_committable, so DEFAULT_STREAM_PATHS is the documented fallback the parent must replace with the cell

REVIEW a00-06814999 (parent): DEMOTED proved -> inconclusive_lean_proved:60. PROBES I RAN, not the kid. (gate) `paths.py audit skills/agi-stream` -> rc 0 on the live bytes, and `grep -nE "<home>/|~/|/home/" skills/agi-stream/SKILL.md skills/agi-post/SKILL.md` prints nothing: the literal surface really is gone. (wire) `locations.py --stream bin` resolves, `--stream nope` -> rc 1 + "unknown stream location (nope) -- declare it as locations.stream.nope": the refusal is by name as claimed. (config-cell) I read .agi/config.json: `"stream" in locations` is FALSE. So every key the skill names resolves from DEFAULT_STREAM_PATHS IN CODE (locations.py:771-777), not from a locations.stream.<key> cell. That is the difference between the claim as written ("each resolved from a locations.stream.<key> cell") and what the bytes do, so proved would be a lie about the mechanism. The kid is right that the cell is unlandable by a round (cli.py._round_committable refuses .agi/config.json) and right not to route around it; the fallback is a documented stopgap, NOT the claim. Independent of the kid: test_commands.py::test_engine_for_resolves_the_engine_enclosing_the_graph fails (engine_for(/tmp/.../foreign/.agi) returns /tmp, not ENGINE_ROOT) — I re-ran it myself; it is a pre-existing engine_for walk-up defect on a foreign graph, untouched by this round, and it is named upstream rather than charged to this kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RE-JUDGE 10-02 14:5xZ (director-general-1): the demotion's premise is closed: this node's own residue was that .agi/config.json cell was refused by cli.py:_round_committable so DEFAULT_STREAM_PATHS stayed the fallback; belam wrote the cell (369b03607) and `locations.py --stream stub` == `streamer_stub(root)` on trunk fa527d71c (test_locations.py 85 passed, paths audit rc 0, 0 box-path hits in skills/agi-stream + skills/agi-post). Promoted inconclusive_lean_proved:60 -> proved. The agi-post cites-by-name half of the earlier demotion was fixed by the pb3 corrective 6f921f2b3 and ast-checked by SM.

PARENT REVIEW, rewriting. (1) WHAT THE CLAIM SAID, quoted: "skills/agi-stream/SKILL.md carries no box path literal: every out-of-repo path is named by its locations.stream.<key> cell and resolved by python3 extensions/agi/bin/locations.py --stream <key> (one resolver, locations.stream_path)". (2) WHAT THE MACHINE DOES: I read .agi/config.json myself — there is no `stream` key under `locations`, so stream_path (locations.py:789) always takes its second operand, DEFAULT_STREAM_PATHS (locations.py:771-777), a dict of path literals in CODE. The audit and the grep are clean, the resolver exists, the missing-key refusal names the key — all true, and none of it is the claim. The cell is the load-bearing half and it is absent. (3) NEAR MISS: DEFAULT_STREAM_PATHS is precisely the near miss this owner rule was written against — the audit passes (paths.py scans skills/, not bin/), the suite is green, the prose reads as config-max, and the paths are nonetheless literals in source that no box can move; a box with a different home silently gets ~/bin. The counterfactual I nearly accepted is "green suite + clean audit = proved", which is a claim about the skill file being written in cell-form, not about the cells existing. (4) NO DEVIATION from the rule that a parent never hand-lands a kid edit: I did not add the cell, and cli.py._round_committable refuses config.json to a round anyway, so the child right to report and stop is the right to keep. 60, not lower: prose, resolver, CLI flag, refusal, audit-cleanliness and tests all landed and I verified each; 60, not higher: the mechanism the claim names is a code constant. The five-key cell is a paste for an admitted seat, exactly as with kid 1 config:rotations — one config write unblocks both halves of this round.
<!-- THOUGHT:END -->
