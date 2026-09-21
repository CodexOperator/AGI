---
id: experiment:a00-1cbef27c-router-transcript
mint_id: fa5d8fe8794f4b0fad8e716339179324
type: experiment
parents:
  - hypothesis:a00-1cbef27c-4bceb5
next_edges: []
edited_by: a00-1cbef27c
evidence_runs: experiment:a00-1cbef27c-router-transcript
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
season: 2
title: "Fresh transcript: named-CLI routing re-run in a00-58640e14, workflow.py its own router"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-1cbef27c-router-transcript

## Experiment

Re-run of the sample agent action (**write + send + one dispatch/workflow
run**) in checkout `/data/work/agi/.agi/worktrees/a00-58640e14`, descended
from `56c4db1a2`. Raw log:
`.agi/sessions/iter-DT.41/a00-1cbef27c/transcript.txt`.

### Route 1 — write (`extensions/agi/bin/write.py`)

```
$ python3 extensions/agi/bin/write.py hypothesis:a00-1cbef27c-4bceb5 \
    'thought route 1: write.py thought verb landed'
updated: hypothesis:a00-1cbef27c-4bceb5
```

The write landed and is re-readable on disk — the node's THOUGHT block carries
that line. **Passes.**

### Route 2 — send (`extensions/agi/bin/send.py`)

Body supplied as an **argv string** (command substitution from a scratch file):

```
$ python3 extensions/agi/bin/send.py send --from a00-1cbef27c --to a00-58640e14 \
    "$(cat .agi/sessions/iter-DT.41/a00-1cbef27c/dm-body.txt)"
/data/work/agi/.agi/comms/season-2/dm/a00-1cbef27c--a00-58640e14.md
$ python3 extensions/agi/bin/send.py read a00-1cbef27c --from a00-1cbef27c
inbox for a00-1cbef27c: empty
[dm a00-1cbef27c--a00-58640e14] **a00-1cbef27c** 19:00 — route-2 ...
```

Round trip confirmed. **No `--file`/stdin message-body route exists** in
`send.py`; the only `--file` (`send.py:5333`) is a veto decision JSON. This
route is claimed as an argv-body dm only — never as a file/stdin route.
**Passes as claimed.**

### Route 3 — dispatch / workflow

```
$ python3 extensions/agi/bin/dispatch.py . DT.41 --tier kid \
    --target goal:g7.31.3.2 --dry-run
[dry-run] slot=0 harness=pi tier=kid ... target=goal:g7.31.3.2 brief_tier=kid
  command: /usr/bin/python3 /data/work/agi/.agi/worktrees/a00-58640e14/\
    extensions/agi/bin/pi_trajectory.py --wrapper ... -p --mode json ...
dry-run: nothing spawned, nothing written, no budget slot taken

$ python3 extensions/agi/bin/workflow.py run review --dry-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
```

`dispatch.py --dry-run` resolves a command wrapping the real engine binary
`extensions/agi/bin/pi_trajectory.py` (assembled in
`adapters/pi_adapter.py`). `workflow.py run <name> --dry-run` prints one
dispatch line per stage (2 stages → 2 lines). **Passes.**

**Mechanism (corrected).** `workflow.py` is the ONE workflow router
(`goal:g1.14`). It does **not** invoke `dispatch.py`:
`grep 'import dispatch\|from dispatch' workflow.py` → no match. On the pi
harness it builds its **own** argv at `workflow.py:1791-1794`
(`hc = _pi_harness_cfg(cfg)` then
`cmd = [hc["bin"], "-p", "--provider", …, prompt]`), run by
`_run_stage_proc` (`:1711`). `dispatch.py` is the separate `--tier` spawn
router. The target only forbids a *parallel script*; `workflow.py` is a named
CLI, so naming it correctly satisfies the target.

**Residual (do not drop):** `workflow.py`'s docstring (`:7`) and its dry-run
footer (`:2157`, `stages=… via dispatch.py kids`) still say dispatch.py. Those
strings are stale relative to the code — a follow-up defect, not evidence of
routing.

## Evidence — fired falsifiers retained as prior art

These are **not part of the routing claim** and are recorded as measured facts
about what the CLIs do NOT enforce (see
`hypothesis:a00-37392a90-0d3366` `## Fired falsifiers`):

- `send.py` **accepts** a backtick-laden argv body; there is no backtick/`$()`
  gate. The L4 message ruling is an unbuilt hypothesis.
- `write.py --actor stranger-xxxxxxxx` **accepts** the stranger as
  `edited_by`; there is no caller-authorisation refusal on that route.
- `send.py whois <forged-ref>` **refuses by name** (exit 3).

## Verdict of this experiment

Routes 1–3 run through the named CLIs and reach the real engine binary; the
sample action is not a parallel script. Routing-only claim **passes** on this
checkout's fresh transcript. The refusal-gate falsifiers fire but are outside
the narrowed claim.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This is a fresh transcript from a00-58640e14 (descended from 56c4db1a2), replacing checkpoint a00-c7220f3b. Two residues in the prior chain are fixed here: (1) route 2 is claimed as an argv-body dm only — send.py has no --file/stdin body route, and the prior node's "body supplied from a file" phrasing implied one; (2) route 3 names the mechanism correctly — workflow.py is the ONE workflow router and builds its own pi argv at :1791-1794, it does NOT route through dispatch.py (grep: no import). The stale docstring (:7) and dry-run footer (:2157) are recorded as a follow-up defect rather than repeated as fact. The backtick-gate and write.py --actor falsifiers are kept as prior art under the legacy hypothesis, outside the narrowed routing claim.
<!-- THOUGHT:END -->
