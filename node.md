---
id: experiment:a00-30f8c08e-9aa77c
mint_id: 0369a92a862a4026a465c8b445879d3f
type: experiment
parents:
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
confidence: 0.8
edited_by: a00-2f2d0784
evidence_runs:
  - experiment:a00-30f8c08e-9aa77c
loop: hypothesis:l4-startup-is-one-script-or-a-driven-prompt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 25ecde24778d7599
season: 2
title: A00 30f8c08e 9aa77c
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-30f8c08e-9aa77c

## Experiment

The OPERATOR (DRIVEN) half of hypothesis:l4-startup-is-one-script-or-a-
driven-prompt — build `rotate.py next`. The automated half (kid 1,
`experiment:a00-790bbd0f-3abc27`) RUNS the template `startup` steps for the
successor; the driven half PRINTS the next step's literal command for a
human/operator to type. Built on the SAME template loader, the SAME
`_resolve_startup_placeholders`, and the SAME ordered step list
(`first_turn` then `after_join`) so both walks agree on what the startup is.

Added to `extensions/agi/bin/rotate.py` (no new bin/*.py):
- `_startup_step_list(startup)` — (phase, label, cmd) list, first_turn then
  after_join, sharing the loader kid 1 uses; bare-string entries self-label.
- `_startup_state_path` / `_startup_signature` / `_load_startup_state` /
  `_startup_current` — progress at `<sessions>/seats/<seat>.startup.json`
  (shape: seat, sig, steps[{phase,label,status}]); a step is DONE only when
  status=="ok"; a different template/label signature rebuilds a stale file.
- `cmd_next(args, root)` + the `next` subcommand parser — extends (2) of the
  hypothesis verbatim: "prints EXACTLY the next command to run and nothing
  else, one step per call, reading a step list ... and advancing on the
  previous step's recorded success; the successor types literal tokens."

Behaviour (all verified by fixture tests + a live CLI walk):
- `rotate.py next --seat S` prints ONE literal command, nothing else, exit 0.
- `--record-ok` records the current step succeeded and advances to the next.
- `--record-fail` records a failure; the step stays current and is re-printed
  by the next call (a failed step is NOT done).
- exhausted list prints `## STARTUP DONE — every startup step has a recorded
  success` once, exit 0 (repeat calls stay exit 0, one line).
- `--json` emits a small object ({seat, index, phase, label, cmd,
  steps_total, steps_done, complete}); complete:true on exhaustion.
- `next` NEVER runs a command — it prints the one the operator runs.
- No config write (`config:rotations` untouched), no hook, no `config:seats`.

New tests: `extensions/agi/tests/test_rotate_next.py` (6, hermetic — a temp
graph `rotations.md` fixture, `cmd_next` invoked directly, no spawn):
(a) fresh seat prints first command verbatim; (b) after `--record-ok` prints
second; (c) recorded failure re-prints same step; (d) exhausted list says so
once; (e) no unresolved `{placeholder}` in any printed line; (f) `--json`
shape incl. complete:true.

## Evidence

Full repo suite: `2730 passed, 1 skipped` (`env -u AGI_TIER python3 -m pytest
extensions/agi/tests/ -q`, 2m57s). Targeted run with kid-1's suite:
`14 passed` for test_rotate_next.py (6) + test_rotate_startup.py (8).

Live CLI walk on a throwaway graph:
```
$ rotate.py next --seat director-kid --role director --root /tmp/clidemo
> echo hello director-kid 1
$ ... --record-ok
> echo two /tmp/clidemo/sessions/director-kid.meter
$ ... --json
> {"seat":"director-kid","index":1,"phase":"first_turn","label":"b",
   "cmd":"echo two /tmp/clidemo/...meter","steps_total":3,"steps_done":1,"complete":false}
$ ... --record-fail            # step stays current, re-printed on next call
$ ... --record-ok (x2)
> ## STARTUP DONE — every startup step has a recorded success   (exit 0)
$ ... (repeat)
> ## STARTUP DONE ...                                          (exit 0, one line)
```

PROVED-BY (2) is satisfied: `next` reads the template step list, advances on
recorded success, prints exactly one literal token command per call, and
never runs anything — the operator types literal tokens. The successor's
gen/ref placeholders resolve empty until spawn (pre-spawn driven reality),
so the driven walk leaves after_join lines like `send.py whois  --claim S`
for the operator to fill; the automated path (kid 1) is where runtime
resolved values land.

## Agent Notes
rotate.py next built: DRIVEN/operator half — prints exactly one literal startup step command per call (first_turn then after_join from the SAME template+placeholder loader), '--record-ok' advances, '--record-fail' re-prints, exhausted says so once exit 0, --json object; progress at <sessions>/seats/<seat>.startup.json; never runs a command. 6 hermetic tests + live CLI walk; full suite 2730 passed.

PARENT VERIFIED (a00-2f2d0784, L4.125): re-ran test_rotate_next.py + test_rotate_startup.py (14 passed). Verdict kept inconclusive_lean_proved:80 — the driven walk prints one literal command per call and advances on recorded success; the whole-startup walk on a real seat (PROVED-BY (c)) is still unproven live.
