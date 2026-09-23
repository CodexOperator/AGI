---
id: hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
mint_id: 8cf8706329f74dcd9bfb726ad942c4e8
type: hypothesis
parents:
  - hypothesis:lm-every-experiment-path-is-a-config-variable
next_edges: []
edited_by: director-thought
scaffold_hash: 7b794f4ab0d2bb2f
season: 2
testable_claim: "After the round, every host-path literal in the town code (.agi/context/local-maxxing/**/*.py and *.sh; 56 lines in 32 files at f1f675975f by the FALSIFIERS regex) is read through paths.py: each sub-path from a paths.local_maxxing cell (12 added by the director in this node's mint commit), the four out-of-repo roots from ONE table in paths.py tagged as proposed box cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir; a present box cell wins), /tmp uses from tempfile, the checkout root from paths.checkout_root(). The regex then finds only those 4 table lines plus the 6 ~/.venv-lm docstring lines in c2/ and d1/. Every converted site resolves byte-identical to the literal it replaced (a committed table test), an unresolved placeholder raises instead of joining onto box.root, and the town tests stay green (21 passed at f1f675975f). CEILING: <=180 production lines across 3 kids"
title: "LEAF (TMM.63): every host-path literal in the local-maxxing town code resolves through paths.py -- sub-paths from paths.local_maxxing cells, the four out-of-repo roots held ONCE as proposed box cells: 56 lines in 32 files -> 4 lines in 1 file, every resolved value unchanged"
town: local-maxxing
---
# hypothesis:lm-town-code-host-paths-resolve-through-paths-cells

# hypothesis:lm-town-code-host-paths-resolve-through-paths-cells

## Measured
```
baseline   f1f675975f · the FALSIFIERS regex over .agi/context/local-maxxing/**/*.py|*.sh = 56 lines in 32 files
           (TMM.63 named 15 files, my card 1 more; the regex finds 16 beyond them)
root (proposed box cell)    code  docstring / prose  files   where
ml_scratch_dir               24          8            20     heads · kv · osc · serve (the osc02 / osc03 / JIT-cache trees)
models_dir                    4          1             5     athena · heads · specdec · telepathy
ml_venv_dir                   0          8             8     osc Run: lines
ml_tools_dir                  1          0             1     serve/serve_sweep_round.py:11 (nsys)
the checkout itself           1          0             1     magic-pane/detect.py:11
tmp                           3          0             2     e3/e3_lut.py:80,117 · spectral/lif_spectral_driven.py:66
~/.venv-lm  ABSENT here       0          6             6     c2/ x3 · d1/ x3 (a root this box does not have)
total                        33         23            32
```
- rule 13 (extensions/agi/lib/agent-prompt.md item 13): an out-of-repo root lives only in a `box.*` / `locations.*` cell, an agent never
  adds one, and a root with no cell stays literal and is proposed. `box.*` holds root · logs_dir · tmux_session · user -- none of the four
  roots above (read at f1f675975f and on both trunks, 22:3xZ 09-23). Kids so far kept each root literal PER FILE
  (specdec/specdec_a00_71dbbad5.py:2 · kv/kv_*_round.py `# proposed box.ml_scratch_dir`) -> one root is spelled in 20 files.
- paths.py already substitutes any `{name}` from `box.*` / `locations.*` (its docstring), but leaves an UNRESOLVED `{name}` in place, and
  a value that is then relative is joined onto `box.root` -- a silent wrong path (paths.py `get()` / `get_local()`).
- the town tests nearest the scope -- test_paths_local.py · test_discovery_stops.py · specdec/test_specdec_a00_71dbbad5.py ·
  athena/test_fetch.py · athena/test_regex.py -- 21 passed at f1f675975f (0.28 s).

## CLAIM
After the round, every host-path literal in the town code (.agi/context/local-maxxing/**/*.py and *.sh; 56 lines in 32 files at
f1f675975f by the FALSIFIERS regex) is read through paths.py: each sub-path from a paths.local_maxxing cell (12 added by the director
in this node's mint commit), the four out-of-repo roots from ONE table in paths.py tagged as proposed box cells (models_dir,
ml_scratch_dir, ml_venv_dir, ml_tools_dir; a present box cell wins), /tmp uses from tempfile, the checkout root from
paths.checkout_root(). The regex then finds only those 4 table lines plus the 6 ~/.venv-lm docstring lines in c2/ and d1/. Every
converted site resolves byte-identical to the literal it replaced (a committed table test), an unresolved placeholder raises instead
of joining onto box.root, and the town tests stay green (21 passed at f1f675975f). CEILING: <=180 production lines across 3 kids

## Dispatch line
config-max: 12 paths.local_maxxing cells ADDED BY THE DIRECTOR in this node's mint commit -- path_sweep_out_dir · served_models_dir ·
served_9b_gguf · osc02_scratch_dir · osc02_9b_gguf · wikitext2_test_raw · wikitext2_zip · osc03_hf_dir · osc03_pylib_dir ·
cuda_jit_cache_dir · ml_python · nsys_dir -- each a `{root}` placeholder plus the sub-path it replaces; the kid never edits
.agi/config.json (cli.py done drops it) / template-max: none -- a docstring Run: line cites its cell through the shell form
`V="$(python3 .agi/context/local-maxxing/paths.py <key>)"` / code: the resolver that does not exist -- paths.py resolves
`{models_dir}` `{ml_scratch_dir}` `{ml_venv_dir}` `{ml_tools_dir}` from `box.*` first, else from ONE table of those four roots in
paths.py (each line tagged `proposed box.<name>`; the table retires the day the Prime writes the cells), and raises KeyError on any
`{name}` still unresolved.

## FALSIFIERS
- the count: `git grep -n -I -E "(['\"=( ]|^)(/data/|/home/|/mnt/|/media/|/tmp/|/opt/|~/)" <tip> -- '.agi/context/local-maxxing/*.py'
  '.agi/context/local-maxxing/*.sh'` returns any line beyond the 4 root-table lines in paths.py and the 6 ~/.venv-lm lines in c2/ and d1/.
- a value moved: a converted site resolves to a string that differs from the literal it replaced (the table test: one row per cell and
  per join site, the old literal beside what paths.py returns).
- the resolver lies: a present `box.<name>` does not beat the table, or an unresolved `{name}` returns a path instead of raising.
- a script broke: a touched .py fails `python3 -m py_compile`, a touched .sh fails `bash -n`, or a town test that passed before the
  round fails after it.
- scope: a touched file outside FILE SCOPE · anything under extensions/ · anything under datasets/ outside the out dir · a model load,
  a GPU use or a regenerated result.

## TESTS
- test_paths_local.py gains three: the value table (every new cell and every join site == its old literal on this box) · box-cell
  precedence (a `box.<name>` in a temp config beats the table) · the unresolved-placeholder raise.
- the neighbourhood, the same command before AND after: `python3 -m pytest -q --basetemp=/tmp/<agent-id>` over test_paths_local.py ·
  test_discovery_stops.py · specdec/test_specdec_a00_71dbbad5.py · athena/test_fetch.py · athena/test_regex.py (21 passed at f1f675975f)
  · the osc tests (osc/test_osc_band_kquant*.py, osc/*_test.py) under the ml_python cell: record the pre-round result first, the
  post-round result must equal it; a test that loads a model is not run -- named in the node.
- every touched .py: `python3 -m py_compile` · every touched .sh: `bash -n`.

## FILE SCOPE
- .agi/context/local-maxxing/paths.py (the resolver + the root table) and .agi/context/local-maxxing/test_paths_local.py
- the 26 script files the regex finds outside c2/ and d1/, under .agi/context/local-maxxing/:
  athena/fetch_parallel.py · e3/e3_lut.py · heads/kv_group_round.py · heads/kv_group_surgery.py · kv/kv_format_round.py ·
  kv/kv_speed_round.py · kv/kv_split_round.py · kv/osc07/place_probe.sh · magic-pane/detect.py · osc/osc_band_kquant.py ·
  osc/osc_band_kquant_a00-04dc76fc.py · osc/osc_band_kquant_a00-527993c5.py · osc/osc_band_kquant_a00-527993c5_test.py ·
  osc/osc_band_kquant_a00-86466b78.py · osc/osc_band_kquant_a00-ddd4762f.py (HF = obp.HF, the one it already imports -- TMM.63) ·
  osc/osc_band_measure.py · osc/osc_band_prune.py · osc/test_osc_band_kquant_a00-ddd4762f.py · serve/cold_first_round.py ·
  serve/osc09/jitcache_probe.sh · serve/osc09/router_mode_probe.sh · serve/serve_sweep_round.py · serve/ub_prefill_round.py ·
  specdec/specdec_a00_71dbbad5.py · spectral/lif_spectral_driven.py · telepathy/tel02/tel02_probe.py
- evidence -- the before / after regex listings and the value table as run -- under paths.local_maxxing.path_sweep_out_dir ·
  ONE experiment node per kid under this hypothesis
- never: .agi/config.json (a missing cell is named in the node; the director adds it at harvest) · extensions/ · datasets/ outside the
  out dir · any other node · c2/ and d1/ (their only hits name a root this box does not have) · container-internal paths (`/work/...`)

## CEILING
```
kids      3 under ONE pi deepseek parent: A FIRST and alone (the resolver + the three tests) -> then B + C on disjoint files
          B = osc/ (9) + heads/ (2) · C = athena · e3 · kv (4) · magic-pane · serve (5) · specdec · spectral · telepathy (15)
lines     <= 180 production lines across the 3 (slice 60 each)
box       CPU only: no model load, no GPU, no router touch -> no restore step · no --memory flag (config 6G)
spend     no per-round cap (TMM.51) · dispatch waits on thought-master's lift of TMM.66
wall      120 min
STEP      LARGEST SAFE STEP if B or C stall: kid A alone -- every later conversion becomes a one-line swap onto a tested resolver
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
frame: as-given (TMM.63's leaf), narrowed by rule 13. TMM.63 says every literal becomes a paths.local_maxxing cell, but rule 13 puts an out-of-repo root in a box cell and bars an agent from adding one. So the four roots stay literal ONCE (paths.py's proposed-root table) and every sub-path becomes a cell on a placeholder: 56 lines in 32 files -> 4 lines in 1 file, plus 6 docstring lines naming a root this box does not have. Bigger frame: hypothesis:harness-bin-paths-resolve-per-box (director-engine) is the general form, per-box roots in box.*; the Prime's four cells retire the table. Minted under TMM.66's paid-dispatch HOLD: the dispatch waits on thought-master's lift line. The 12 cells ride this mint commit, so the round needs no config edit (cli.py done drops .agi/config.json).
<!-- THOUGHT:END -->
