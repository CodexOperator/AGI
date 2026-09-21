---
id: experiment:a00-763e629b-5c04ad
mint_id: 1b71b2bc83fd4ce0b9d355264b8a495e
type: experiment
parents:
  - hypothesis:pi-parent-tier-mode2
confidence: 0.65
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: A00 763e629b 5c04ad
verdict: inconclusive_lean_proved:65
wired_at: 1788233448
wired_from: a00-763e629b
---
# experiment:a00-763e629b-5c04ad

## Experiment

**What.** Static trace of the full dispatch path — the exact falsifier the
parent hypothesis names — against `extensions/agi/bin/` as of 2026-09-01,
to establish where the tier boundary would have to land and whether anything
already on the path would fight it. No live `--max-iters 1` run was executed
(iteration budget; this node is the evidence the live run should build on).

**Inputs.** `dispatch.py`, `heal.py`, `post_wire.py`, `lib/agent-prompt.md`;
`.agi/config.json` (`agent_dispatch` and `cc_dispatch` blocks).

**What happened.**

1. **Falsifier grep: passed trivially, but informatively.** `grep -rn tier`
   over `dispatch.py`, `heal.py`, `post_wire.py`, `agent-prompt.md` returns
   **zero** hits. The gate-invocation path has no tier-keyed branch today —
   the shared half of the claim is unburdened by construction. This is
   necessary, not sufficient: it shows nothing *prevents* one-lookup tiering;
   only a live parent run shows nothing *requires* more.

2. **The spawn call is already parameter-shaped.** `_build_pi_args` assembles
   pi flags from three orthogonal pieces: `pi_model_args(cfg)` (model), the
   brief (`--append-system-prompt`, scaffold + completion contract), and the
   initial user message. A parent tier is a fourth value on exactly two of
   these axes — a different model string and a different brief text. The
   process boundary the hypothesis worried about is one `subprocess.Popen`
   call with `start_new_session=True`; the parent's shell-out to
   `dispatch.py --tier kid` reuses the identical entry point, so no second
   dispatcher exists even at the process level.

3. **The config already encodes tiers with zero readers.** `cc_dispatch`
   carries `kid_model: claude-sonnet-5`, `parent_model: claude-opus-5`;
   `grep -rln 'parent_model\|kid_model' extensions/agi` returns **nothing**.
   `agent_dispatch` (what pi actually reads) has `provider/model/thinking` but
   no tier axis. So the tier parameter would read
   `dispatch_cfg[tier + "_model"]`-style keys that must be **added** to
   `agent_dispatch` — the CC keys cannot be borrowed without coupling the two
   runtimes' configs, which g4.3's invariant argues against.

4. **Serialization constraint confirmed in code, and it is dispatcher
   property, not brief property.** `n = cfg.agent_dispatch.claude_max_parallel`
   (= 1 here) is enforced *before* any prompt is built (`main`, line ~169) and
   gates the whole target loop. A parent that ignores its brief cannot cause a
   parallel-kid collision if the parent itself is dispatched through this `n`;
   but the parent's *own* spawns run outside this gate — the parent shells out
   to `dispatch.py` on its own, so the `claude_max_parallel: 1` guarantee does
   not transitively cover grandchildren. The known constraint in the
   hypothesis resolves toward "property of the dispatcher" for the parent slot
   itself, and **remains open** for the parent→kid spawn step: that is the one
   place a second parallelism knob could be needed, which would be a real
   (if small) fork.

5. **`heal.py` timeout risk narrowed.** heal's manifest carries
   `timeout_seconds` globally, not per agent, and neither heal.py nor
   post_wire.py contains any tier concept — neither can distinguish parent
   from kid today. That cuts both ways: no tier-specific scheduler exists, but
   a long-lived parent (running its kids sequentially) will trip the same
   `agent_timeout_mins` a kid would. Predicted fix is a per-agent
   `timeout_seconds` override in `agent.json` set at scaffold time — still a
   data field, not a code branch.

**Verdict shape.** The claim survives static inspection: zero existing tier
branches, one spawn call, brief and model already isolated as parameters. The
unproven residue is live-behavioural: (a) does a parent brief assembled from
the same `agent-prompt.md` source actually instruct shell-out spawning
reliably, and (b) does the grandchild-parallelism gap in (4) need a knob.
Both are one `--max-iters 1` run with a parent-dispatched slot away from being
settled.

## Evidence

```
$ grep -rn tier extensions/agi/bin/dispatch.py extensions/agi/bin/heal.py \
      extensions/agi/bin/post_wire.py extensions/agi/lib/agent-prompt.md
(no output — zero tier-keyed branches on the gate path)

$ grep -rln 'parent_model\|kid_model' extensions/agi
(no output — cc_dispatch tier keys have no reader anywhere)

$ python3 -c "import json;print(json.load(open('.agi/config.json')).get('agent_dispatch'))"
{'claude_max_parallel': 1, 'ollama_max_parallel': 0, 'ollama_model': 'qwen3:4b',
 'provider': 'openrouter', 'model': 'z-ai/glm-5.3-flash', 'thinking': 'medium'}

$ python3 -c "import json;print(json.load(open('.agi/config.json')).get('cc_dispatch'))"
{'iterations_per_run': 5, 'max_goals_active': 3, 'kids_per_iter': 2,
 'kid_model': 'claude-sonnet-5', 'parent_model': 'claude-opus-5'}
```

Code anchor for (4): `dispatch.py main()` — `n = int(cfg.get("agent_dispatch",
{}).get("claude_max_parallel", 1))` applied to the target loop only; the
spawned parent's own `dispatch.py` invocation (via its shell-out) starts a
fresh process whose parallelism the original `n` does not bound.

## Agent Notes
Static trace: zero tier branches on gate path, spawn already parameter-shaped; open residue is live parent brief + grandchild parallelism