---
id: experiment:a00-1b4d6db0-04de8a
mint_id: e2188ac9bc3d435088e5d6192d5a9e6c
type: experiment
parents:
  - hypothesis:lm-every-experiment-path-is-a-config-variable
next_edges: []
confidence: 0.6
edited_by: director-thought
evidence_runs:
  - experiment:a00-1b4d6db0-04de8a
line_ceiling: 120
loop: hypothesis:lm-every-experiment-path-is-a-config-variable@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "inspect committed config paths block + reader anchor against TMM.42", "expected": "paths.local_maxxing namespace, repo-relative values, box.root anchor", "observed": "un-namespaced paths, 9/9 absolute values; reader anchors at nearest .agi", "result": "refuted"}
  - {"conjunct": 1, "class": "wire", "cmd": "reader get(rel) on a fixture whose box.root={root}", "expected": "{root}/.agi/worktrees/a00-2f819956", "observed": "<fixture>/.agi/worktrees/a00-2f819956 (nearest-.agi anchor)", "result": "refuted"}
production_lines: 133
profile: balanced
role: kid
scaffold_hash: 70feaf82e15e1cb7
season: 2
title: "CONFIG-MAX in local-maxxing: one shared reader, 9 path literals become config variables, values byte-identical"
town: local-maxxing
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# CONFIG-MAX IN local-maxxing: one shared reader, every path in a variable, values byte-identical

Kid 1 of CFG.01. Scope: `.agi/context/local-maxxing/**` only (kid 2 owns `datasets/**`).
Prior bytes cited below are those at HEAD `1be529faeee50ba197f03ff3e19262f787caac2f`.

## What I did

1. **Reader** `paths.py` (new, 72 lines, `.agi/context/local-maxxing/paths.py`) — callable from
   `.py` and `.sh`. It walks UP from its own `__file__` to the nearest `.agi/config.json`,
   takes `paths.<key>`, returns absolute values unchanged and joins relative values onto the
   repo root (the directory holding that `.agi/`). `box.root` is never consulted. Unknown key ->
   stderr + exit 1. CLI: `python3 .agi/context/local-maxxing/paths.py <key>` prints the resolved
   value, exit 0. Importable accessor `get(key)` / `resolve(key)`.
2. **Config** — added `paths` to `.agi/config.json`; one key per literal, each value the EXACT
   literal it replaces. No existing config key renamed or re-keyed.
3. **Converted 9 scripts** (below). Each reaches the reader by a path DISCOVERED from `__file__`
   (walk up until a sibling `paths.py`), never by a new absolute literal.

## Evidence — per key: reader output == the exact old bytes

| key | reader prints | old bytes | cite (HEAD) |
|---|---|---|---|
| `models_dir` | `/data/ml/models` | `WORK = "/data/ml/models"` | `.agi/context/local-maxxing/athena/fetch_parallel.py:14` |
| `models_qwen35_9b` | `/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf` | `'/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf'` | `telepathy/tel02/tel02_probe.py:6` |
| `tmp_kidB` | `/tmp/kidB` | `'/tmp/kidB/spk_in.npy'`, `'/tmp/kidB/e3_results.json'` | `e3/e3_lut.py:79,116` |
| `agi_root` | `/data/work/agi` | `ROOT = "/data/work/agi"` | `magic-pane/detect.py:11` |
| `worktree_a00_2f819956` | `{root}/.agi/worktrees/a00-2f819956` | `ROOT = Path("{root}/.agi/worktrees/a00-2f819956")` | `ws-raw/run_gpu_probe.py:23`, `ws-raw/run_kidC.py:20` |
| `worktree_a00_48ed5e56_nodes` | `{root}/.agi/worktrees/a00-48ed5e56/.agi/nodes` | `ROOT = "{root}/.agi/worktrees/a00-48ed5e56/.agi/nodes"` | `kidc_verdict_corpus_trainability.py:19` |
| `tmp_tm58drv_c` | `/tmp/tm58drv.c` | `src_c, exe = "/tmp/tm58drv.c", ...` | `spectral/lif_spectral_driven.py:66` |
| `tmp_tm58drv` | `/tmp/tm58drv` | `..., "/tmp/tm58drv"` | `spectral/lif_spectral_driven.py:66` |
| `tmp_lifref` | `/dev/shm/lifref` | `d = "/dev/shm/lifref"` | `spectral/lif_spectral.py:69` |

Raw run: `for k in ...; do python3 .agi/context/local-maxxing/paths.py $k; done` printed all nine
rows above, exit 0 each; `paths.py nope` printed the KeyError message and exited 1.

**Relative branch** (no live caller — all nine values are absolute): in a scratch fake repo
`.agi/sessions/.../fakeroot/.agi/config.json = {"paths":{"rel":"datasets/thing","abs":"/abs/thing"}}`
with a copy of the reader, `paths.py rel` -> `<fakeroot>/datasets/thing` and `paths.py abs` ->
`/abs/thing`; the `.sh` form `V="$(python3 ... paths.py rel)"` returned the same. Repo root was
the fakeroot, not the real one.

## Evidence — per converted script (smallest honest check)

Probe `.agi/sessions/iter-CFG.01/a00-1b4d6db0/probe_paths.py` (scratch, not committed): for each
file it (a) asserts the old literal is gone from the file bytes, (b) execs THAT FILE'S OWN loader
block with `__file__` set to the real path and asserts `_lm.get(key) == old literal`, (c) really
imports where deps allow. Result `FAILURES=0`:

- `athena/fetch_parallel.py` loader PASS + **import PASS** (stdlib only) — its own pytest also run:
  `python3 -m pytest .agi/context/local-maxxing/athena/test_fetch.py -q` -> **9 passed in 0.05s**.
- `magic-pane/detect.py` loader PASS + **import PASS** (stdlib only; `main()` is guarded).
- `ws-raw/run_gpu_probe.py`, `ws-raw/run_kidC.py` loader PASS + **import PASS** (httpx/websockets
  present; both modules are all-definitions under an `if __name__` guard).
- `e3/e3_lut.py`, `spectral/lif_spectral_driven.py`, `spectral/lif_spectral.py`,
  `kidc_verdict_corpus_trainability.py`, `telepathy/tel02/tel02_probe.py` loader PASS,
  **import SKIP — numpy/torch/snntorch/sklearn are NOT installed on this box** (verified by
  `python3 -c "import numpy"` failing). `tel02_probe.py` additionally has top-level network code,
  so importing it would be a live probe, not a check. All five `py_compile` clean.
- every converted file `python3 -m py_compile` clean.

## Evidence — grep falsifier

`grep -rn -E '/data/|/home/|/tmp/|/opt/|/mnt/|/root/|/dev/shm' .agi/context/local-maxxing
--include='*.py' --include='*.sh'` -> **zero matches** (exit 1). No converted literal survives in
any file in scope.

`git status --porcelain -- extensions` -> empty. Nothing under `extensions/` touched.

## Node commands corrected (write.py, in place)

One node in the graph calls a converted script on an old literal:

- `experiment:a00-0a374caa-7e0acd` body line 136 used to read
  ``Command: `python3 /tmp/kidB/e3_lut.py` ...``; now
  ``Command: `python3 "$(python3 .agi/context/local-maxxing/paths.py tmp_kidB)/e3_lut.py"` ...``.
  `paths.tmp_kidB` resolves to exactly `/tmp/kidB`, so the command is unchanged in value.
  Prose mentioning `/tmp/kidB/e3_results.json` (a result path, not a command) was left as-is.

No node in the graph quotes the converted files' **bytes** (grepped every old assignment line
verbatim across `.agi/nodes/`), so no byte-evidence note was owed.

## Literals left + why

- `/proc/loadavg`, `/proc/meminfo`, `/proc/net/dev` (`ws-raw/*`, `d1/d1_ablation.py`,
  `athena/fetch_parallel.py`, `c2/*`) — kernel pseudo-filesystem, invariant across machines and
  not a storage location a project config names.
- `Path.home() / ".cache/lm-models/..."` and `Path.home() / "src/llama.cpp/..."`
  (`ws-raw/*`) — computed from the environment, not a literal; converting them would change
  behavior for a different user, which the claim forbids.
- `magic-pane/detect.py` `OUT = os.path.join(dirname(__file__), "../../../../datasets/magic-pane")`
  — a location-independent JOIN off `__file__`; likewise `event/event_port.py`'s `HERE` joins and
  `spectral/lif_spectral.py`'s `BEND`/`BENCH`. Left by the brief.
- `magic-pane/detect.py` `"/nodes/"`, `"/sessions/"` — substring fragments matched against a path,
  not a location literal.
- `telepathy/probe_kv_surface.py` `"/slots"`, `"/v1/models"` etc. — HTTP routes, not filesystem
  paths.

## Deviation / note

`.agi/config.json` already carried one unrelated added line (`spawn.production_line_ceiling: 120`)
from another writer when I opened it; I left it exactly where it was and appended `paths` after
`grid`. The 12-line config diff therefore includes that line.

## Recorded line count

`git diff --numstat -- .agi/context/local-maxxing .agi/config.json` -> 12+6+6+5+5+6+6+5+5+5 = **61**
added tracked lines, plus the new untracked `paths.py` = **72** -> `production_lines: 133`,
`line_ceiling: 120`. Under the 2x stop line (240), so the round completed.

## Agent Notes
local-maxxing half: paths.py reader + 9 config keys + 9 scripts converted, per-key/loader proof FAILURES=0, grep falsifier zero literals, test_fetch.py 9 passed, extensions/ untouched; datasets/ half is kid 2

CFG.01 rebrief correction: paths keys are now namespaced paths.local_maxxing.<key> and every value is box-root-relative, so this node's two surviving worktree rows are converted to paths.local_maxxing.worktree_a00_2f819956 and paths.local_maxxing.worktree_a00_48ed5e56_nodes, values identical (same bytes as the old literals); the absolute scratch/model/town roots (models_dir, models_qwen35_9b, tmp_kidB, agi_root, tmp_tm58drv_c, tmp_tm58drv, tmp_lifref) were reverted to literals and are proposed box cells instead of paths keys.

PARENT REVIEW (a00-e9111187, CFG.01): demoted proved -> inconclusive_lean_disproved:60. The TMM.42 rebrief landed mid-round and governs this design (namespaced paths.local_maxxing, repo-relative values against box.root, absolute roots left as literals); this node does the opposite on all three. Its script conversions are technically clean and superseded by experiment:a00-3f66ba67-f5c25c. Named probes: gate (rebrief policy), wire (reader anchor).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-e9111187, CFG.01) -- why this node now says what it says. (1) THE INSTRUCTION: "one negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node"; a kid that passes its own suite and fails my probe is lean_disproved, with the probe NAMED. (2) THE MACHINE: the kid committed 4c32dc0cd -- a working reader plus an un-namespaced paths block of NINE absolute values; I extracted that commit to scratch and ran its reader on a fixture: get(rel) returned the fixture own .agi anchor, not box.root. The governing TMM.42 rebrief (director-thought 08:51, mid-round) requires values namespaced paths.local_maxxing.<key>, REPO-RELATIVE, resolved against box.root, with absolute box roots LEFT as literals. The kid satisfies the old orders on all counts and the rebrief on none. (3) THE NEAR MISS: a reviewer would accept this node because its exact-value test PASSED -- and it did, for the nine absolute values it wrote; the rebrief falsifier is not value equality but naming+absolute policy, which no value test can catch, so passing tests is exactly the wrong lens here. (4) DEVIATION: none -- I did not rewrite the kid production bytes; the correction kid experiment:a00-3f66ba67-f5c25c re-implemented them under the rebrief and I record the demotion here.
<!-- THOUGHT:END -->
