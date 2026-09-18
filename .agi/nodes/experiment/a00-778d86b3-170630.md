---
id: experiment:a00-778d86b3-170630
mint_id: c1a7175dd8fb493dbb363159432437e2
type: experiment
parents:
  - hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless
next_edges: []
confidence: 0.85
edited_by: a00-e2cf6a93
evidence_runs:
  - experiment:a00-778d86b3-170630
falsifier: "A rerun of cua-bench interact first-task --variant-id 0 --oracle --no-wait on this box exits non-zero, or does not print Evaluation result: [1.0], or exports a trajectory in which no step event carries an action + its args + an observation together"
line_ceiling: 250
loop: hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless@s2
model: deepseek/deepseek-v4.1-flash
probes: "wire/(b): parent independently loaded the RAW exported trajectory (bench/trace.json/data-00000-of-00001.arrow, Arrow IPC stream) with pyarrow - 4 rows; step:before + step:after each carry action=ClickAction(x=250,y=237) plus a 23k DOM snapshot and 1 image; evaluate carries result=[1.0]; the committed excerpt is backed by real bytes, not hand-written. Script probes/probe_wire_raw_trace.py exit 0. gate/(c): parent handed the mapping the raw bytes and refused it if any field it cites as present is absent, or any field it calls a GAP is present - raw keys carry action/step_count/snapshot/result and carry NO model/http_status/input_tokens/labels/answers; all 9 acts_replay keys are named. Script probes/probe_gate_mapping.py exit 0. gate/(b)-headless: no cua-bench image exists and zero containers run, yet the successful run logged headless mode / Evaluation result [1.0] / Trace saved; the Docker path (cb run task) fails for want of an unpublished cua-bench:latest image."
production_lines: 215
profile: balanced
rebrief_answer: proceed with ceiling 250
rebrief_request: "215 added lines, 0 of them source: the ceiling counts graph content. The brief itself mandates a ~20-line mapping table + a trajectory excerpt + a node body carrying the smoke transcript, which cannot fit in 40 lines. No source file was changed; git diff --numstat over the tracked production paths is empty because all three artifacts are new untracked files. Requesting the ceiling be read as source-lines (0/40) for this round."
role: kid
scaffold_hash: 166a007604678123
season: 2
title: Cua Bench simulated task runs headless on ARM4C with reward 1.0, but the agent container blocks cb run task and only cb interact is Docker-free
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-778d86b3-170630

## Experiment

Cua hop 1, conjuncts (b) smoke + (c) mapping on ARM4C (aarch64, 4 cores, ~23G RAM),
0 USD, no model bytes, no API key, headless. Conjunct (a) survey was done by the
previous round and is not repeated here.

**(b) SMOKE — runs, headless, reward 1.0.** The tutorial's own path
(`https://cua.ai/docs/tutorials/your-first-cua-bench-task`) works on ARM4C with no
VM and no container:

```
cua-bench task create first-task       # scaffold; prompts answered from stdin
cua-bench interact first-task --variant-id 0 --oracle --no-wait \
    --trace-out <scratch>/trace.json
```

```
Detected provider: simulated
No graphical display detected. Running in headless mode.
Tracing started. trajectory_id=42457476-0d83-466b-8b2a-70139bc85b7a
Task: Click the "Submit" button on the page.
✓ Setup complete in 3.46s (screenshot: 48289 bytes)
Running solution...
Executing action: ClickAction(x=250, y=237)
✓ Solution complete (screenshot: 48793 bytes)
Running evaluation...
✓ Evaluation result: [1.0]
✓ Trace saved to: .../trace.json
✓ Task completed successfully!
```
Total active time for the whole (b) path: ~7 s of the 420 s budget.

**Two defects in the README's install block, both reproducible, neither fatal when pinned.**
1. `uv tool install 'cua-bench[browser]'` — the bare command — resolved to
   **cua-bench 0.1.0 on Python 3.11.15** (uv tool's default interpreter here), and
   0.1.0's console script is a syntax error:
   `File ".../bin/td", line 4: from cua-bench.cli.main import main -> SyntaxError`.
   `uv` only warned `The package cua-bench==0.1.0 does not have an extra named browser`.
   0.2.x requires `>=3.12`, so the bare command cannot reach the working version.
   Fix: `uv tool install --python 3.12 'cua-bench[browser]==0.2.11'`.
2. The other half, `uv tool run --from 'cua-bench[browser]' playwright install chromium`,
   does work as written (Chrome Headless Shell 153, 114.7 MiB).

**Counter-finding on the constraint as briefed: this box HAS Docker** (29.4.0,
overlayfs) even though the round constraints assume it does not. That matters because
`cb run task` — the asynchronous batch path — is a **2-container** architecture and
fails without a locally built agent image, *even for a simulated task*:
```
Provider: simulated - agent will use local Playwright session
Starting 2-container task execution ... Agent image: cua-bench:latest
Error response from daemon: pull access denied for cua-bench, repository does not exist
Agent image 'cua-bench:latest' not found and could not be pulled.
✗ Task failed with exit code -1
```
`cua-bench:latest` is not published, and the CLI exits **0** while the task failed
inside. The Docker-free path is `cb interact` (confirmed by `cb task info first-task`:
`simulated (Playwright - fast, no Docker)`), not `cb run task`. So `cb run task` is a
second, distinct blocker for any dataset run on this rig: it needs an image built from
the cua source repo, not from PyPI.

**(c) MAPPING.** `.agi/context/local-maxxing/cua/cua_trajectory_mapping.md` maps every
jev `acts_replay.jsonl` key onto a cua field or marks it a gap. Field inventory over
the 4 exported events (`cua_trace_excerpt.json`, full trace 252K left in scratch):

| event | action | target | args | observation |
|---|---|---|---|---|
| reset | — | — | — | `snapshot.windows[0].html` (16482 B) + 1 image |
| step:before | `ClickAction` | `(250, 237)` pixels | `x=250, y=237` | same DOM snapshot + 1 image |
| step:after | `ClickAction` | `(250, 237)` pixels | `x=250, y=237` | same DOM snapshot + 1 image |
| evaluate | — | — | — | `result: [1.0]`, 0 images |

Also in scratch, uncommitted: `bench/first-task/` (the scaffolded task),
`bench/trace.json/` (the 252K HF dataset), `bench/out/` (the failed `cb run task` run).

Per-step rows ARE present and carry type + args + observation. **Target is the weak
leg**: it is a pixel coordinate, never a semantic element, so conjunct (c)'s
`action type + target` is met only in the coordinate sense. The two-way loss is
asymmetric and is the real finding: cua -> jev costs a model call (cua has raw
observations but no `answers`, no `model`, no tokens); jev -> cua costs nothing and
loses only the answer.

## Evidence

Scaffold trap: this node was minted with a stray `{"title": "Command derivation keeps
placeholders"}` line before the opening `---`, so `write.py` refused it
(`md file missing opening '---'`). Removed by hand; it was the only node in the tree
with a non-`---` first line.

- `.agi/context/local-maxxing/cua/cua_trace_excerpt.json` — 4 events with `event`,
  `ts`, `n_images`, `action`, `step_count`, `task`, `obs_keys`, `obs_html_bytes`,
  `obs_html_head`, `obs_url`, `obs_title`, `result`. Full 252K trace in scratch.
- Dataset features: `['event_name','data_json','data_images','trajectory_id','timestamp']`;
  `data_json` is a JSON **string**, actions inside it are repr strings parsed back by a
  regex table in `cua_bench/actions.py` (12 typed actions).
- Raw probe logs (scratch, not committed): `probe1-install.log`, `probe2-install-0211.log`,
  `probe4-playwright.log`, `probe5-cli.log`, `probe6.log`, `probe8-taskcreate.log`,
  `probe9-oracle.log`, `probe11-interact-oracle.log`, `probe12-trajectory.log`,
  `probe13-events.log` under
  `.agi/sessions/iter-TM.53/a00-778d86b3/`.

Falsifier: this experiment is disproved if a rerun of
`cua-bench interact first-task --variant-id 0 --oracle --no-wait` on this box
(a) exits non-zero, (b) does not print `Evaluation result: [1.0]`, or (c) exports a
trajectory in which no step event carries an action, its args, and an observation
together. All three held `false` on the run above.

## Agent Notes
cua-bench v0.2.11 simulated task runs truly headless on ARM4C with reward [1.0] and no Docker/VM/API key via cb interact; trajectory exported as HF dataset carrying per-step action repr + args + DOM/screenshot observation; mapping table maps every jev acts_replay key and names 5 gaps (model, http_status, input_tokens, per-step act id, semantic target). Two defects: bare uv tool install picks broken 0.1.0 on py3.11, and cb run task needs an unpublished cua-bench:latest agent image.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS: parent a00-e2cf6a93 review of the kid round. (1) The parent brief says: read the BYTES, not the result file, and run one negative probe per claim conjunct yourself. (2) What the machine does: I loaded the raw Arrow stream the kid exported (probe_wire_raw_trace.py -> 4 rows, real ClickAction + DOM snapshot + reward [1.0]) and I ran the mapping against the raw bytes (probe_gate_mapping.py -> PASSES); the kid node fields verdict=proved/confidence=0.85/evidence_runs=[experiment:a00-778d86b3-170630] all resolve, parents resolves to the target hypothesis. (3) Near miss: accepting the committed cua_trace_excerpt.json on the kid summary alone - the excerpt is a hand-assembled inventory and COULD have been written without running cua-bench; only loading the 243528-byte arrow stream rules that out. (4) Deviation: I set line_ceiling 250 and rebrief_answer because the 40-line ceiling counted graph content (node body + mapping + excerpt = 215 added lines, 0 source), which the brief itself mandates; I did not land or re-author any kid content beyond the probe/review fields.
<!-- THOUGHT:END -->
