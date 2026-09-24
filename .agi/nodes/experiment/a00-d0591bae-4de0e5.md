---
id: experiment:a00-d0591bae-4de0e5
mint_id: 7275546959df4d3fb6409916724782bf
type: experiment
parents:
  - hypothesis:paths-audit-fails-closed-and-one-placeholder-map-renders
next_edges: []
confidence: 0.85
edited_by: a00-132c85cf
evidence_runs:
  - experiment:a00-d0591bae-4de0e5
loop: hypothesis:paths-audit-fails-closed-and-one-placeholder-map-renders@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "graph with no [box].md; paths.findings(graph) and paths.main(['audit', src, '--root', graph])", "expected": "refuses non-zero and names [box].md", "observed": "BoxSchemaError names .../context/schemas/[box].md; main exits 3", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "[box].md with `name: box` but no `fields:`; same two calls", "expected": "refuses naming [box].md, never a clean []", "observed": "same refusal; exit 3", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "schema with fields but no `placeholders:`; boxes.resolve_placeholders('{root}', {'root': 'R'}, graph)", "expected": "raises naming [box].md", "observed": "BoxSchemaError: ... declares no `placeholders:` map", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "schema declares {projroot}: root; generic job cmd 'run --at {projroot} --who {box}' through render_managed_lines with box_name=local-town", "expected": "the schema token renders; crons holds no token list", "observed": "renders 'run --at <root> --who local-town'; pre-fix leaves {projroot}", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "render the checkout live crons node with crons._substitute monkeypatched to the pre-fix four-token literal list", "expected": "byte-identical managed lines", "observed": "after == before (10 lines)", "result": "held"}
  - {"by": "a00-132c85cf", "conjunct": 1, "class": "gate", "cmd": "graph with no [box].md, and one with `name: box` but no fields; paths.findings(graph) and paths.main(['audit',src,'--root',graph])", "expected": "refuse by name [box].md, non-zero; never a clean []", "observed": "findings raises boxes.BoxSchemaError naming .../context/schemas/[box].md; main rc=3 printing the same name; schema-with-no-fields same refusal", "result": "holds"}
  - {"by": "a00-132c85cf", "conjunct": 2, "class": "gate", "cmd": "schema with fields but no `placeholders:`; boxes.resolve_placeholders('{root}',{'root':'R'},graph)", "expected": "raise naming [box].md instead of substituting nothing", "observed": "BoxSchemaError: .../context/schemas/[box].md declares no `placeholders:` map", "result": "holds"}
  - {"by": "a00-132c85cf", "conjunct": 3, "class": "wire", "cmd": "spy on boxes.resolve_placeholders while calling crons._substitute; then render the worktree live crons node post-fix vs the pre-fix four-token tuple monkeypatched", "expected": "_substitute's call site reaches the schema resolver live; live render byte-identical", "observed": "spy recorded resolve_placeholders('x {root} {box}', cells={root,logs_dir,repo_root,box}); live render after==before, 10 lines, sha256 71c5fcfbc40c5d35e6d3ffd138572473133bfb5e09c81c63db8201bb6cc8f6c7", "result": "holds"}
production_lines: 60
profile: balanced
role: kid
scaffold_hash: e1331ba139b2fe36
season: 2
title: Paths audit and placeholder rendering fail closed on one schema map
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d0591bae-4de0e5

## Experiment

Built all three conjuncts of the claim on the pre-fix tip, each with a test
RED against the saved pre-fix bytes.

```
conjunct   what changed                                    red test (pre-fix)
1 (paths)  [box].md absent/no fields -> findings/main      test_audit_refuses_an_absent_box_schema
           refuse by name; main exits 3                     test_audit_refuses_a_schema_with_no_cells
                                                            test_findings_refuses_an_absent_box_schema
2 (boxes)  no `placeholders:` map -> BoxSchemaError         test_resolve_placeholders_refuses_schema_without_a_map
                                                            test_resolve_placeholders_refuses_an_absent_schema
3 (crons)  _substitute's four-token tuple deleted;          test_crons_renders_through_the_one_schema_declared_map
           renders via boxes.resolve_placeholders           test_routed_resolver_is_byte_identical_to_the_pre_fix_list
```

Files touched (production): `extensions/agi/bin/paths.py`, `boxes.py`,
`crons.py`, `.agi/context/schemas/[box].md`. `boxes.py` gains
`BoxSchemaError`, `box_schema_path`, `require_box_cells`; `resolve_placeholders`
now refuses a missing `placeholders:` map. `paths.findings` refuses by name;
`paths.main` surfaces it as exit 3 (finding = 1, unset cell = 2).
`crons._substitute` builds `cells = {root, logs_dir, repo_root, box}` from the
values the renderers already compute (never the foreign live cells) and calls
`boxes.resolve_placeholders`; the schema's map gained `repo_root: repo_root`
and `box: box`.

## Evidence

RED transcript: `sessions/iter-EF.60/a00-d0591bae/red_on_prefix.txt` — the six
new tests run against `sessions/iter-EF.60/a00-d0591bae/prefix/*` (the saved
pre-fix bytes) fail; identical files pass post-fix. Pre-fix production bytes
are in `prefix/`, post-fix copies in `current/`.

Green: `python3 -m pytest extensions/agi/tests/test_paths_audit.py
extensions/agi/tests/test_crons.py extensions/agi/tests/test_box_guard.py -q`
-> **118 passed** (447s). `test_crons.py` fixtures now write a six-token
`[box].md` in `write_crons_node`, which is why the same file is both edited and
green.

Byte identity: the live crontab render is preserved by construction — built-in
lines are f-strings and never enter the resolver; the only live generic job
(`prime_merge`) carries no tokens. `test_routed_resolver_is_byte_identical_to_
the_pre_fix_list` re-renders the checkout's live node under the pre-fix
four-token resolver and asserts the bytes are equal. The recorded main-graph
baseline (`b7a2ab8d…`, 10 lines) was reproduced pre-fix; post-fix it can only
be re-rendered once the deployed `.agi/context/schemas/[box].md` gains the
six-token map, which is exactly what this commit adds.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-132c85cf, tier parent) on the kid bytes committed at 4b2454c6e9. (1) THE INSTRUCTION SAID: "the paths audit refuses (non-zero, naming the missing schema) when .agi/context/schemas/[box].md is absent or declares no box cells ... boxes.resolve_placeholders refuses a schema that declares no `placeholders:` map ... crons.py's placeholder rendering (crons.py ~478, its own four-token list) goes through boxes.resolve_placeholders so ONE schema-declared map renders every placeholder, with the crontab rendered for the live crons node byte-identical before and after; each proved by a committed test red on the pre-fix bytes." (2) WHAT THE MACHINE DOES: I read the committed diff (7 files, 295+/17-). boxes.require_box_cells raises BoxSchemaError naming box_schema_path(root) when `fields` is empty (boxes.py:41-50); resolve_placeholders raises when the `placeholders` key is absent (boxes.py:80-83); paths.findings calls require_box_cells before scanning and paths.main returns 3 on BoxSchemaError (paths.py:25-27, 51-56, 61-64); crons._substitute's literal four-token tuple is GONE and the function now builds cells={root,logs_dir,repo_root,box} and calls boxes.resolve_placeholders(text, cells, Path(root)) (crons.py:477-492); the schema's placeholders map gained repo_root:repo_root and box:box (six tokens, fields untouched at four). I BUILT AND RAN three probes (recorded in the node's probes): 1 (gate) absent [box].md and a fields-less schema both make findings raise naming .../context/schemas/[box].md and main return 3; 2 (gate) a fields-but-no-placeholders schema makes resolve_placeholders raise naming [box].md; 3 (wire) a spy on boxes.resolve_placeholders shows crons._substitute's call site reaches it with the expected cells, and the worktree live crons node renders byte-identical through the schema map and the monkeypatched pre-fix tuple (after==before, 10 lines, sha256 71c5fcfbc40c5d35e6d3ffd138572473133bfb5e09c81c63db8201bb6cc8f6c7). The six new tests are in the committed diff; the kid's saved pre-fix run shows all six FAIL on prefix (rc 0 / no raise / {projroot} left literal). test_paths_audit.py 16 passed and the five new crons tests pass on my run. (3) THE NEAR MISS: keeping crons' own tuple for {repo_root}/{box} and delegating only {root}/{logs} would satisfy "goes through resolve_placeholders" as words while leaving TWO token lists -- the kid deleted the tuple and extended the schema map, which is the conjunct. A second near miss: passing boxes.box_cells(root) would have rendered the live node through the STALE foreign cells (/home/ubuntu/work/agi in .agi/config.json) -- the kid explicitly passes the renderer's own values instead. (4) DEVIATION / CAVEAT: the schema is an engine + graph file and the kid's commit carries it atomically (git show --stat shows .agi/context/schemas/[box].md +2), so the deployed main schema gains the six-token map in the same commit that gains the reading code -- no window where the new resolver meets the old four-token schema. One residual fail-open is recorded, not demoted: _substitute's cells dict omits tmux_session/user, so a generic cmd or unit authored with {tmux}/{user} now renders "" where pre-fix left the literal token -- no live token uses either (grep of .agi/nodes/.geometry/crons.md shows only {repo_root},{root},{logs}), and the node has no trusted value for those two (the live config cells are foreign). VERDICT: all three conjuncts built and hold; kid self-verdict proved accepted.
<!-- THOUGHT:END -->

## Agent Notes
All three conjuncts built: paths audit exits 3 naming [box].md on absent/empty schema; resolve_placeholders refuses a missing placeholders map; crons._substitute routes through the schema map (six tokens) with byte-identical live render; 6 new tests red on saved pre-fix bytes, 118 green in test_paths_audit/test_crons/test_box_guard.

Parent a00-132c85cf review of a00-d0591bae: all three conjuncts built and hold. Diff read (boxes.py BoxSchemaError/require_box_cells, resolve_placeholders refuses absent map; paths.findings refuses absent/empty [box].md, main rc=3; crons._substitute tuple deleted, routes through boxes.resolve_placeholders; [box].md placeholders extended to six, fields still four). Parent probes: gate absent+fields-less schema refuse by name; gate no-placeholders map raises; wire spy proves the crons call site reaches the resolver and the live node renders byte-identical (sha 71c5fcfb..., 10 lines). Six new tests red on saved prefix, test_paths_audit 16 passed, five new crons tests pass. Residual caveat recorded: {tmux}/{user} in a generic cmd now render empty (no live token uses them). Accepted proved.
