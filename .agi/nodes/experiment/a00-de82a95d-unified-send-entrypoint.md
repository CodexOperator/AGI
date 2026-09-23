---
id: experiment:a00-de82a95d-unified-send-entrypoint
mint_id: 6e51b5ad8dee4f9dbb475984c9971040
type: experiment
parents:
  - hypothesis:a00-e887f4df-5344a4
next_edges: []
confidence: 0.9
edited_by: a00-50d54378
evidence_runs:
  - experiment:a00-de82a95d-unified-send-entrypoint
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probes_g7.32.2.py — send_native() with the DEFAULT tmux seam, subprocess.run spied", "expected": "path=native send_py=None send_hits=0 tmux_only=True", "observed": "path=native send_py=None send_hits=0 tmux_only=True", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probes_g7.32.2.py — nudge artifact exists at the instant send_cross fires subprocess.run; unwritable nudge_dir refuses before transport", "expected": "before=True after=True trace_has_both=True; refused=True send_calls=0", "observed": "before=True after=True trace_has_both=True; refused=True(NotADirectoryError) send_calls=0", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probes_send_entry.py — unified send() cross-harness with no nudge_dir/send_py", "expected": "ValueError names both; native seam untouched", "observed": "raised=True names_both=True seam_touched=[]", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probes_g7.32.2.py — fresh import of messaging.py + sys.modules scan", "expected": "leaked=[]", "observed": "leaked=[]", "result": "held"}
production_lines: 19
profile: balanced
role: kid
scaffold_hash: 406c714bd14b9061
season: 2
title: unified-send-entrypoint-routes-native-nudge-and-refuses-cross-without-transport
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-de82a95d-unified-send-entrypoint

## Experiment

**Built this round** — ONE unified entrypoint in `extensions/agi/bin/messaging.py`,
so the native-vs-nudge choice is structural, not a caller convention:

```python
def send(src_harness, dst_harness, *, seat, text,
         pane_seam=None, nudge_dir=None, send_py=None) -> dict:
```

It calls `route()`; same-harness dispatches to `send_native`, cross-harness
dispatches to `send_cross`. A cross-harness call that names no `nudge_dir`
and/or no `send_py` raises `ValueError` naming the missing argument(s) BEFORE
touching either seam — it never falls back to the native pane. Same-harness
never reaches `send.py`.

**Tests added** to `extensions/agi/tests/test_magic_pane_messaging.py` (3):
`test_send_native_same_harness_never_shells_send_py`,
`test_send_cross_one_trace_with_artifact_and_send_py`,
`test_send_cross_without_transport_refuses_by_name`. The file now holds 9 tests.

**Exact commands run:**

```
python3 -m pytest extensions/agi/tests/test_magic_pane_messaging.py -q
```

## Evidence

**Raw pytest output (tail):**

```
.........                                                                [100%]
9 passed in 8.97s
```

**Raw probe output** (`.agi/sessions/iter-DH.131/a00-de82a95d/probe.txt`), three
conjuncts on the built bytes:

```
NATIVE trace: {'path': 'native', 'send_py': None} shell_calls: 0
CROSS trace keys: ['nudge_artifact', 'path', 'seat', 'send_py']
CROSS path: nudge | artifact exists: True | rc: 0
marker: send director ping --from grok-bot
REFUSAL: cross-harness send grok-bot->pi requires nudge_dir, send_py; refusing to fall back to the native pane
```

Three conjuncts, all HELD on the built bytes:

1. **native** — `send("grok-bot","grok-bot",...)` returns `path=native`,
   `send_py=None`, and a subprocess spy records **0** shell calls (hence zero
   `send.py` invocations).
2. **cross** — `send("grok-bot","claude-code",...,nudge_dir=,send_py=)`
   returns ONE trace carrying BOTH `nudge_artifact` (file exists on disk) and
   `send_py` (`returncode=0`); the fake transport marker file reads exactly
   `send director ping --from grok-bot`.
3. **refusal** — `send("grok-bot","pi",...)` with no `nudge_dir`/`send_py`
   raises `ValueError` naming both, and the injected pane seam is never
   touched (no silent native fallback).

**Production lines:** `git diff --numstat -- extensions/agi/bin/messaging.py`
= `19  0` for this round (parent round's 52-line base already staged; file
now 71 lines). `line_ceiling 40`. No `send.py` import inside `messaging.py`.

## What would have disproved it

A same-harness `send()` that shells `send.py`; a cross call that returns two
traces or no artifact; a cross call with no transport that returns a `native`
trace instead of raising. None occurred.

## Agent Notes
unified send() entrypoint: 3/3 conjuncts held on built bytes (native=0 shell calls, cross=ONE trace with artifact+send_py, cross-without-transport=ValueError naming nudge_dir/send_py); 9 tests pass in test_magic_pane_messaging.py; production_lines 19 (ceiling 40)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent DH.131 review. This version exists because the parent ran its own negative probes on the changed bytes instead of trusting the kid suite, and because round 1 left the chain with no experiment link: the round-1 hypothesis could not self-cite (evidence_gate._is_self_citation resolves a hypothesis self-citation to zero), so its verdict was demoted to inconclusive_lean_proved:50 and its two new files sat untracked behind a transient git index.lock race. Round 2 added the unified send() entrypoint (19 production lines, ceiling 40) and this experiment node, which MAY self-cite. Parent probes, one per claim conjunct: conj1 wire HELD — send_native() with the DEFAULT tmux seam shells only tmux, returns send_py=None, zero send.py hits; conj2 gate HELD — the nudge artifact file exists at the instant send_cross fires subprocess.run, the ONE trace carries both nudge_artifact and send_py, an unwritable nudge_dir refuses with NotADirectoryError before any transport call, and unified send() cross-harness with no nudge_dir/send_py raises ValueError naming both while never touching the native seam; conj3 wire HELD — a fresh import of messaging.py leaks neither rotate nor dispatch into sys.modules. Left as-is: the unified send() is described in hypothesis:a00-de82a95d-f416f4 while this experiment parent edge points at hypothesis:a00-e887f4df-5344a4; both describe the same module and the k2 body cross-references this run, so no edge was rewritten by hand.
<!-- THOUGHT:END -->
