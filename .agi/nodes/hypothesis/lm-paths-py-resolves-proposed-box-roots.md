---
id: hypothesis:lm-paths-py-resolves-proposed-box-roots
mint_id: d90c201aa3d6464eb5603ea555e29c71
type: hypothesis
parents:
  - hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
next_edges: []
edited_by: director-thought
scaffold_hash: ec864863f72ce106
season: 2
testable_claim: "paths.py resolves the four proposed box roots ({models_dir} {ml_scratch_dir} {ml_venv_dir} {ml_tools_dir}) from box.* first, else from ONE table in paths.py whose four entries each carry the comment \"proposed box.<name>\" (values = the four roots the town scripts spell today), and raises KeyError naming any {name} still unresolved after substitution; with it all 11 cells resolve byte-identical to the literals they will replace, pinned by a value-table test, and test_paths_local.py gains 3 tests (the value table, box-cell precedence, the unresolved raise) while the 21-test neighbourhood stays green. CEILING: <=60 production lines across 1 kid"
title: "LEAF.01 leaf A (TMM.76 step 2, the first pi-local leaf): paths.py resolves the four proposed box roots from box.* or ONE tagged table and refuses an unresolved placeholder -- all 11 path cells resolve to their literals"
town: local-maxxing
---
# hypothesis:lm-paths-py-resolves-proposed-box-roots

# hypothesis:lm-paths-py-resolves-proposed-box-roots

## Measured
- the parent, hypothesis:lm-town-code-host-paths-resolve-through-paths-cells (LEAF.01), is split per TMM.76 step 2 (one leaf = one pi-local kid on
  OrcaBonsai-27B-C2, 0 USD): THIS leaf = its kid A, the resolver; the 26 script conversions (its kids B and C) become later leaves.
- .agi/context/local-maxxing/paths.py `get()` / `get_local()` substitute `{name}` from `box.*` / `locations.*` (`_placeholders`) and leave an
  UNRESOLVED `{name}` in place; the then-relative value is joined onto `box.root` -- a silent wrong path.
- the 11 cells added at 827d4212c0 (served_models_dir · served_9b_gguf · osc02_scratch_dir · osc02_9b_gguf · wikitext2_test_raw · wikitext2_zip ·
  osc03_hf_dir · osc03_pylib_dir · cuda_jit_cache_dir · ml_python · nsys_dir) use `{models_dir}` `{ml_scratch_dir}` `{ml_venv_dir}` `{ml_tools_dir}`;
  `box.*` holds none of the four, so TODAY every one of them resolves wrong.
- test_paths_local.py has 3 tests; the town neighbourhood below = 21 passed at f1f675975f.

## CLAIM
paths.py resolves the four proposed box roots ({models_dir} {ml_scratch_dir} {ml_venv_dir} {ml_tools_dir}) from box.* first, else from ONE table in
paths.py whose four entries each carry the comment "proposed box.<name>" (values = the four roots the town scripts spell today), and raises KeyError
naming any {name} still unresolved after substitution; with it all 11 cells resolve byte-identical to the literals they will replace, pinned by a
value-table test, and test_paths_local.py gains 3 tests (the value table, box-cell precedence, the unresolved raise) while the 21-test neighbourhood
stays green. CEILING: <=60 production lines across 1 kid

## Dispatch line
config-max: none new -- the 11 cells exist (827d4212c0); the four roots are box cells only the Prime writes (rule 13), so they live ONCE in paths.py's
table until then / template-max: none / code: the resolver fallback + the unresolved raise -- the resolver that does not exist.

## FALSIFIERS
- any of the 11 cells resolves to a string other than its literal (the value-table test).
- a `box.<name>` present in a temp config does not beat the table.
- an unresolved `{name}` returns a path instead of raising.
- a test in the neighbourhood that passed before fails after.
- any file outside FILE SCOPE touched.

## TESTS
- test_paths_local.py gains: the value table (11 rows, key -> expected literal: the expected literals are TEST FIXTURES, the only place they may be
  spelled besides the root table) · precedence (a temp config with a box.models_dir cell wins over the table) · the unresolved raise.
- the neighbourhood, BEFORE the first edit and after, the same command:
  `python3 -m pytest -q --basetemp=/tmp/<agent-id> .agi/context/local-maxxing/test_paths_local.py .agi/context/local-maxxing/test_discovery_stops.py
  .agi/context/local-maxxing/specdec/test_specdec_a00_71dbbad5.py .agi/context/local-maxxing/athena/test_fetch.py .agi/context/local-maxxing/athena/test_regex.py`

## FILE SCOPE
- .agi/context/local-maxxing/paths.py · .agi/context/local-maxxing/test_paths_local.py · ONE experiment node under this hypothesis
- never: .agi/config.json · extensions/ · any script that USES a cell (those are the later leaves) · any other node

## CEILING
```
round     (TMM.90) the standard line on the free lane: one pi-free parent + ONE kid spawned with --harness pi-free · <= 60 production lines ·
          read <= 3 files by line range (paths.py, test_paths_local.py, the paths block of .agi/config.json) · ONE experiment node
box       CPU only · 0 USD · wall 60 min
record    turns · tool calls · wall · the before / after test counts · the model the round ran on
STEP      LARGEST SAFE STEP if the tests stall: the resolver alone with the unresolved raise, proven by hand on two cells
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
frame: smaller (unchanged) -- LEAF.01 kid A, the resolver: the smallest self-contained piece, and it unblocks every later leaf that reads a {root} cell. THIS version: the round moves to the free lane (TMM.90, owner 02:3xZ: normal operations on the free OpenRouter endpoint, no more special 0-USD runs). Attempts so far, all 0 USD and 0 commits: LEAF.02 (pi-free parent a00-e309c592) refused in 6 s by the account filter (allowed providers = deepseek only); LEAF.03 (a local PI_CODING_AGENT_DIR parent a00-bbb13581) overflowed the 65,536-token slot on its 12th call (one unbounded grep) before spawning its kid, compacted, and was cancelled by the owner mid-retry at 02:28:57Z -- both now research hypotheses under the brain-swap experiment. The expected literals in the value-table test are fixtures, not paths code relies on (noted on the parent).
<!-- THOUGHT:END -->
