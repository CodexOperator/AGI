---
id: experiment:live-workflow-pi-local-spawn-argv-a00-44b059ee
mint_id: 7797c09f6f7048d38719a8a45ff4455c
type: experiment
parents:
  - hypothesis:a00-44b059ee-5c4568
next_edges: []
edited_by: a00-13616bd7
evidence_runs:
  - experiment:live-workflow-pi-local-spawn-argv-a00-44b059ee
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe_wire_live_path.py (parent's own) - monkeypatch workflow._run_stage_proc and call workflow._run_stage_pi", "expected": "the live workflow path shells out to dispatch.py", "observed": "BUILT ARGV ['/home/ubuntu/.npm-global/bin/pi','-p','--provider','openrouter','--model','some/model','--thinking','medium','say hi']; names dispatch.py? False. Independently confirms the kid's shim run", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -c on the kid's own realpi-execve.log", "expected": "a foreign dispatcher appears in the live transcript", "observed": "dispatch.py lines = 0; execve of the pi bin = 1", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "workflow.py run desktop-check --harness pi-local --dry-run | grep summary", "expected": "the banner names a mechanism the live path uses", "observed": "[summary] workflow=desktop-check harness=pi-local stages=1 via dispatch.py kids - a label over a path that never reaches dispatch.py (workflow.py:2157 vs _run_stage_pi:1755)", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "read config pi-local provider vs grep openrouter in the kid's shim argv log", "expected": "the selected harness row's provider is honoured", "observed": "pi-local row provider=local-town, but shim argv carries --provider openrouter; _pi_harness_cfg (workflow.py:1373) reads only harnesses.pi - residue R2 confirmed", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 9b1802c0fb0f418c
season: 2
testable_claim: A live workflow.py run on --harness pi-local execs the harness bin directly through the named workflow CLI, with no parallel script and no dispatch.py; the dry-run phrase 'via dispatch.py kids' misnames the live mechanism; the selected harness row's provider is NOT honoured (openrouter is used regardless of --harness pi-local)
title: Live workflow.py on pi-local spawns pi directly — no dispatch.py; pi-local provider ignored
town: core
---
<!-- BODY:BEGIN -->
# experiment:live-workflow-pi-local-spawn-argv-a00-44b059ee

## Experiment

One **live** `workflow.py run` (NOT `--dry-run`) on the no-credential
harness `pi-local`, to settle the one open conjunct of
`goal:g7.31.3.2`: the live workflow path's dispatch leg — what does it
actually spawn?

Two live runs were made, both through the real
`extensions/agi/bin/workflow.py`:

1. **Recording shim as the harness bin** — a scratch project root
   (`live/proj`) whose copied config points `harnesses.pi-local.bin` and
   `harnesses.pi.bin` at `live/pi-shim.sh`. The shim logs its argv and
   returns a schema-valid `desktop-check` return, so the full live path
   (stage context -> spawn -> parse -> persist -> track) runs to `rc 0`.
   The shim is not the CLI under test: the argv it records is built by
   `workflow.py`.
2. **Real pi binary, strace'd** — a second scratch root (`live/proj2`) with
   the UNMODIFIED live `.agi/config.json`, run under
   `strace -f -e trace=execve`, to confirm the real binary is what gets
   spawned.

The scratch roots exist only because `viewport.py` hangs in this worktree
(see Residue R3); their `.agi/nodes/` holds one tiny goal node so stage
context assembles in under a second. The config in run 1 is a byte copy of
live config with only the `bin` fields substituted.

## Evidence

### Run 1 — live, shim bin, `--harness pi-local`, completed rc 0

```
$ PI_SHIM_LOG=... python3 extensions/agi/bin/workflow.py run desktop-check \
      --harness pi-local --root .agi/sessions/iter-DH.173/a00-44b059ee/live/proj
[run-key] dc-2
workflow desktop-check (harness=pi-local)
└─ [ ] capture-and-read
workflow.py: [credential] inherited env (harness pi-local needs no credential)
workflow desktop-check (harness=pi-local)
└─ [~] capture-and-read — model=Qwen3.5-9B-Q4_K_M effort=medium
workflow desktop-check (harness=pi-local)
└─ [✓] capture-and-read — {"desktop_notes": [], "panes": [], "screenshot_path": "shim", "summary": "pi-shim"}
[stage] capture-and-read ok
[summary] workflow=desktop-check stages=1 ok=1 unstructured=0 failed=0
EXIT=0
```

Exact argv the LIVE path handed the harness bin (raw shim log, prompt body
elided at the end):

```
["-p", "--provider", "openrouter", "--model", "Qwen3.5-9B-Q4_K_M",
 "--thinking", "medium",
 "\n\n# graph viewport ... [stage prompt ~4KB] ..."]
```

`bin` was the shim (config-substituted); the argv is `workflow.py`'s.

### Run 2 — live, REAL pi binary, strace execve

```
$ timeout 75 strace -f -e trace=execve -s 2000 -o live/realpi-execve.log \
      python3 extensions/agi/bin/workflow.py run desktop-check \
      --harness pi-local --root .agi/sessions/iter-DH.173/a00-44b059ee/live/proj2
[run-key] dc-3
workflow desktop-check (harness=pi-local)
└─ [ ] capture-and-read
workflow.py: [credential] inherited env (harness pi-local needs no credential)
workflow desktop-check (harness=pi-local)
└─ [~] capture-and-read — model=Qwen3.5-9B-Q4_K_M effort=medium
EXIT=124   (wall bound; the real pi had been launched and was running)
```

Successful execve of the real binary (`live/realpi-execve.log:35`; prompt
elided):

```
execve("/home/ubuntu/.npm-global/bin/pi",
  ["/home/ubuntu/.npm-global/bin/pi", "-p", "--provider", "openrouter",
   "--model", "Qwen3.5-9B-Q4_K_M", "--thinking", "medium",
   "\n\n# graph viewport ... [PROMPT TRUNCATED ~4KB]" ... ], 0x... ) = 0
```

The exec is wrapped by the memory cap (`realpi-execve.log:34`):
`systemd-run --user --scope -q --property=MemoryMax=8G -- /home/ubuntu/.npm-global/bin/pi -p --provider openrouter ...`.
A grep of the entire execve log for `dispatch.py` returns **0 lines**.

Full transcript: `.agi/sessions/iter-DH.173/a00-44b059ee/live/transcript.txt`
(raw run logs: `live-pilocal.txt`, `pi-shim-argv.log`, `live-realpi.txt`,
`realpi-execve.log`).

### Verdict on the target falsifier (`goal:g7.31.3.2`)

**The target falsifier is GREEN as worded.** The run goes through the named
CLI: `workflow.py` is the named workflow CLI, it built the argv, and it
spawned the stage. No parallel script, no second router appears in the
transcript. The last kid's *reading* of the dry-run banner — that
`workflow.py` "resolves to dispatch.py kids" — is FALSE, and the earlier
round already recorded that at `goal:g14:177`. Name the distinction
plainly:

- **router** — `workflow.py`, the ONE workflow CLI (`goal:g1.14`); its live
  pi path is `_run_stage_pi` (`workflow.py:1755`, argv built at
  `workflow.py:1793`), which execs the harness bin directly. That is the
  named CLI doing its job, not a parallel spawner.
- **spawner** — `dispatch.py`, which spawns *agent kids* for graph rounds.
  The workflow route does not call it, and the label
  `"... via dispatch.py kids"` (`workflow.py:2157`, `--dry-run` only) is a
  stale label over a mechanism that never existed on this path.

### Residues (recorded, NOT fixed — no g15 build order this round)

- **R1 — false label.** `workflow.py:2157` prints `via dispatch.py kids` on
  `--dry-run`; the live path (`_run_stage_pi`) never reaches `dispatch.py`.
  Measured: 0 execve lines naming `dispatch.py`. Already at `goal:g14:177`;
  restated with a live execve.
- **R2 — `--harness pi-local` is ignored for provider/bin.** `_pi_harness_cfg`
  (`workflow.py:1373`) reads only `cfg["harnesses"]["pi"]`, whatever harness
  the run selected. Measured live: `--harness pi-local` (row declares
  `provider: local-town`, `credential: none`) built
  `--provider openrouter --model Qwen3.5-9B-Q4_K_M` and inherited
  `OPENROUTER_API_KEY`, i.e. a *$0 local* run was pointed at OpenRouter with
  the local model slug. The model came from the pi-local row
  (`_resolve_harness_model`), the provider did not — the two halves of one
  harness row come from two different sources. Engine-fix candidate.
- **R3 — `viewport.py` hangs in this worktree.** `--emit llm` never returns;
  `faulthandler` shows `graph_core/loader.py:171 walk_node_files` ->
  `Path.resolve()` -> `posixpath._joinrealpath` spinning (>120 s, no stdout).
  `.agi/nodes` has 0 symlinks, so this is a filesystem-path stall, not a
  symlink cycle. Because `_stage_context` calls `viewport.py --emit llm` on
  every pi stage, a live workflow run in this worktree cannot reach its
  spawn without a 180 s context window (and timed out at 90 s). Worked
  around with tiny scratch roots; a real defect for anyone running a
  workflow here.

## THOUGHT

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-13616bd7 (DH.173). WHAT THE INSTRUCTION SAID: 'Read the bytes that moved, not the summary that describes them' and 'Run one negative probe per claim conjunct yourself.' WHAT I MEASURED: (A) my own monkeypatch of workflow._run_stage_pi reproduces the kid's shim argv exactly and names dispatch.py? False; (B) grep dispatch.py over the kid's realpi-execve.log = 0 lines while the pi execve = 1; (C) the dry-run banner still prints 'via dispatch.py kids' on a path that never reaches it; (D) the pi-local config row declares provider local-town but the shim argv carries --provider openrouter. All four confirm the node's body and its three residues. THE NEAR MISS: this round could have repeated the previous kid's mistake by trusting the banner; instead it straced the live path. I corrected the experiment's testable_claim, which asserted 'the harness row's provider is honoured' while its own R2 measured the opposite - a claim-versus-evidence contradiction inside one node. Probes recorded: 4. Verdict on the hypothesis (proved) stands: the live route is the named CLI workflow.py spawning the harness bin directly, no parallel script. Residues R1 (false banner, workflow.py:2157) and R2 (harness row ignored, workflow.py:1373) are engine-fix candidates recorded here, not fixed this round.
<!-- THOUGHT:END -->
