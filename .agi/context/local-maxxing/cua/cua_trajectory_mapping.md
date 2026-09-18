# Cua-Bench trajectory  ->  jev `acts_replay.jsonl` typed-acts map

Source: cua-bench v0.2.11, simulated task `first-task`, oracle run, ARM4C headless, reward 1.0.
Trajectory = HF dataset (`event_name`, `data_json`, `data_images`, `trajectory_id`, `timestamp`).
jev row = `act`, `kind`, `repeat`, `model`, `http_status`, `latency_s`, `input_tokens`, `labels`, `answers`.

| jev key | cua field | verdict |
|---|---|---|
| `kind`     | `data_json.action` prefix (`ClickAction` -> click) | DERIVABLE: split `ClassName(`; closed set of 12 actions in `cua_bench/actions.py` |
| `act`      | none (no act/node id in the trace) | GAP: cua has `trajectory_id` per run, no per-step id; mint from `trajectory_id + step_count + event_name` |
| `repeat`   | `data_json.step_count` | DERIVABLE: `step_count` gives index, not repeat count; repeat=1 constant unless replayed |
| `model`    | none | GAP: cua records actions, not the model that emitted them; `--model` lives in CLI args, never in the trace |
| `http_status` | none | GAP: no HTTP layer in the trace |
| `latency_s` | `timestamp` (ISO, per event) | DERIVABLE: diff successive `timestamp`s; no per-action duration of its own |
| `input_tokens` | none | GAP: no token accounting |
| `labels`   | `event_name` (`reset`/`step:before`/`step:after`/`evaluate`) + `evaluate.result` | PARTIAL: event names map to labels fairly directly; reward `1.0` is an outcome, not a label |
| `answers`  | `data_json.snapshot.windows[0]` (`html`,`url`,`title`,`x`,`y`,`width`,`height`) + `data_images` | GAP-as-ANSWER: cua's observation is raw DOM+screenshot, not a typed/scored answer object |
| target     | `action` args only — `ClickAction(x=250, y=237)` | GAP: pixel coords, no semantic target (no selector/role/name); not recoverable from the DOM without a resolver |
| args       | `action` repr args | DERIVABLE: regex table already ships in `actions.py`; store args as a JSON object, not a repr string |

## Gaps, named

1. **`model` has no counterpart at all.** Cua traces are model-blind; the agent that emitted the step is not in the record.
2. **`http_status` / `input_tokens` / `latency_s` have no counterpart.** Cua is a computer-use trace, not an LLM call log.
3. **No typed `target`.** Actions carry coordinates, never a semantic element reference.
4. **`act` identity is per-run, not per-step.** `trajectory_id` is a run key; a per-step act id must be minted.
5. **The reverse direction is also lossy:** jev rows carry `answers` (typed, scored, probabilistic); cua carries the raw observation they would have been inferred *from*. Mapping cua -> jev therefore costs a model call; mapping jev -> cua costs nothing but drops the answer.
