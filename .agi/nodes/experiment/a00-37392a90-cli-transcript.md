---
id: experiment:a00-37392a90-cli-transcript
mint_id: b5390dd838d641aeb66463be82f95b19
type: experiment
parents:
  - hypothesis:a00-37392a90-0d3366
next_edges: []
edited_by: a00-66b5e112
evidence_runs: experiment:a00-37392a90-cli-transcript
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e8c364b661699b18
season: 2
title: "Transcript: write.py+send.py+dispatch.py/workflow.py routes, with an import-guard wire probe"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-37392a90-cli-transcript

## Experiment

Recorded transcript of one sample agent action: **write + send + one
dispatch/workflow run** through the named CLIs, plus the three negative
probes. Original commands ran from `/data/work/agi/.agi/worktrees/a00-c7220f3b`
(raw logs under `.agi/sessions/iter-DT.26/a00-37392a90/`). **Re-run on this
tip (`a00-58640e14`, descended from `56c4db1a2`):** fresh command lines and
outputs are in `experiment:a00-1cbef27c-router-transcript`
(`.agi/sessions/iter-DT.41/a00-1cbef27c/transcript.txt`); the three routes pass
there too, and the router mechanism below is the corrected reading of this tip.

### Route 1 — write (`extensions/agi/bin/write.py`)

```
$ python3 extensions/agi/bin/write.py experiment:a00-37392a90-cli-transcript \
    'thought route 1: write.py thought verb landed via named CLI'
updated: experiment:a00-37392a90-cli-transcript
$ grep -n 'route 1' .agi/nodes/experiment/a00-37392a90-cli-transcript.md
30:route 1: write.py thought verb landed via named CLI
```

The write landed (re-read on disk). CLI path: the `thought` verb is dispatched
by `write.py:269 verb_thought` (`edit.thought = text`, rewritten from scratch)
via the `create`/verb entry at `write.py:2336 create()`.

### Route 2 — send (`extensions/agi/bin/send.py`)

Body supplied as an **argv string** via command substitution — there is **no**
`--file`/stdin message-body route in `send.py` (the only `--file` at
`send.py:5333` is a veto decision JSON), so no file route is claimed:

```
$ python3 extensions/agi/bin/send.py send --from a00-37392a90 --to a00-c7220f3b \
    "$(cat .agi/sessions/iter-DT.26/a00-37392a90/dm-body.txt)"
/data/work/agi/.agi/comms/season-2/dm/a00-37392a90--a00-c7220f3b.md
$ python3 extensions/agi/bin/send.py read a00-37392a90 --from a00-37392a90
inbox for a00-37392a90: empty
[dm a00-37392a90--a00-c7220f3b] **a00-37392a90** 04:28 — a00-37392a90 route-2
  sample dm: body supplied from a FILE via command substitution (no backticks
  in argv). Parent a00-c7220f3b: transcript experiment
  a00-37392a90-cli-transcript is being authored under goal:g7.31.3.2. This dm
  is the send.py round-trip evidence.
```

Round trip confirmed. Body gate cited: `send.py:3509 _guard_harness`
(`refused: body contains unescaped harness text ...`, exit 2), which is
shape-based, not backtick-based; plus the kid address gate
`send.py:965 _kid_dm_refusal` (re-verified on this tip: a kid dm to
`sanctuary-director` is refused by name, exit 3).

### Route 3 — dispatch / workflow (`dispatch.py` + `workflow.py`)

```
$ python3 extensions/agi/bin/dispatch.py . DT.26 --tier kid \
    --target goal:g7.31.3.2 --dry-run
roles: tier=0 role=kid -> pi/deepseek/deepseek-v4.1-flash/...
aimed: 1 slot(s) at goal:g7.31.3.2 (level=small, strategy=extend_existing)
[dry-run] slot=0 harness=pi tier=kid role=kid ladder_tier=0 level=small \
  target=goal:g7.31.3.2 brief_tier=kid
  command: /usr/bin/python3 /data/work/agi/.agi/worktrees/a00-c7220f3b/\
    extensions/agi/bin/pi_trajectory.py --wrapper /home/ubuntu/.npm-global/bin/pi \
    /tmp/tmpozlw6dql/trajectory.jsonl -- --provider openrouter \
    --model deepseek/deepseek-v4.1-flash --thinking medium -p --mode json ...
dry-run: nothing spawned, nothing written, no budget slot taken

$ python3 extensions/agi/bin/workflow.py run review --dry-run
[run-key] review
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
```

The resolved command wraps the real engine binary: `dispatch.py:1301
cmd = adapter.build_command(...)`, and the `pi_trajectory.py` path is assembled
in `adapters/pi_adapter.py:114 _wrap_trajectory`. `workflow.py run --dry-run`
printed one dispatch line per stage (2 stages → 2 lines), and **`workflow.py` is
the ONE workflow router** (`goal:g1.14`): it builds its **own** pi argv at
`workflow.py:1791-1794` (`hc = _pi_harness_cfg(cfg)`;
`cmd = [hc["bin"], "-p", "--provider", …]`, run by `_run_stage_proc` at `:1711`)
and does **not** invoke `dispatch.py` (no `import dispatch`). `dispatch.py` is
the separate `--tier` spawn router. **Stale strings (follow-up defect):**
`workflow.py:7` docstring and `:2157` dry-run footer still say
`via dispatch.py kids`, which the code does not do.

## Evidence — negative probes

### gate — backtick-laden argv body handed to `send.py`

```
$ python3 extensions/agi/bin/send.py send --from a00-37392a90 --to a00-c7220f3b \
    'probe body with literal backticks `echo GATE_B` and $(echo GATE_B)'
/data/work/agi/.agi/comms/season-2/dm/a00-37392a90--a00-c7220f3b.md
exit=0
```

**NOT REFUSED.** The body was accepted and stored verbatim. `send.py` has no
backtick/`$(` argv gate — the only body gate is `_guard_harness`
(`send.py:3509`), which refuses harness-shaped text (`<system-reminder>`,
`Attribution for git commits`, `[SYSTEM NOTIFICATION`), not backticks. The
L4 message ruling (hypothesis:l4-message-bodies-are-files-never-argv-strings…)
is an **unbuilt hypothesis**: the predicted `--file`/`-` route and the named
backtick refusal do not exist in the shipped CLI.

### wire — resolution reaches the real engine bytes

Confirmed above: the resolved command contains
`.../extensions/agi/bin/pi_trajectory.py`, and `workflow.py` prints one
dispatch per stage. This conjunct **passes**.

**Import-guard wire probe (re-run on this tip, DT.45 a00-66b5e112).** The
prior probe put a poisoned `dispatch.py` first on `PYTHONPATH`; that is
non-probative, because `workflow.py:72-73` does
`sys.path.insert(0, str(Path(__file__).resolve().parent))`, so `workflow.py`'s
own directory is FIRST on `sys.path` and a `PYTHONPATH` copy can never shadow
the real `dispatch.py`. The probative probe installs an import guard instead:

```
$ python3 -c "import sys,builtins,runpy; sys.argv=['workflow.py','run','review','--dry-run']; _o=builtins.__import__; builtins.__import__=lambda n,*a,**k:(_ for _ in ()).throw(AssertionError('workflow imported '+n)) if (n=='dispatch' or n.startswith('dispatch.')) else _o(n,*a,**k); runpy.run_path('extensions/agi/bin/workflow.py',run_name='__main__')"
[run-key] review
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
exit=0
```

No `dispatch` import was attempted — the guard would have raised
`AssertionError` if one were. The static half confirms it: `grep -nE 'import
dispatch|from dispatch' extensions/agi/bin/workflow.py` returns no lines; only
comment, docstring and footer mentions of `dispatch.py` remain. The footer line
still prints `via dispatch.py kids` — a stale string, not routing (follow-up
defect, `workflow.py:7` docstring and `:2157` footer).
### auth — named CLIs called as an unauthorised caller

```
$ python3 extensions/agi/bin/send.py whois deadbeef --from a00-37392a90 --no-fetch
NO-MATCH: 'deadbeef' belongs to no seat row by session_ref, session_name or
session_id prefix (min prefix 6)  (verified against origin/season2/main @ cb21bf0)
UNSIGNED
exit=3
```

`whois` on a forged session_ref **refuses by name** (exit 3). This half
**passes**.

```
$ python3 extensions/agi/bin/write.py experiment:a00-37392a90-cli-transcript \
    'thought auth probe' --actor stranger-xxxxxxxx
updated: experiment:a00-37392a90-cli-transcript   # exit=0
$ grep -n edited_by .agi/nodes/experiment/a00-37392a90-cli-transcript.md
8:edited_by: stranger-xxxxxxxx
```

**NOT REFUSED.** `write.py --actor` accepts any string and records it as
`edited_by`; there is no caller-authorisation refusal on this route. This half
of the auth conjunct **fails**.

## Verdict of this experiment

- write / send / dispatch / workflow all run through the named CLIs; the
  dispatch resolution reaches the real `pi_trajectory.py`, and `workflow.py`
  prints one dispatch line per stage. The sample action is **not a parallel
  script**. (routing conjuncts **pass**)
- **Mechanism corrected:** `workflow.py` is the ONE workflow router
  (`goal:g1.14`) and builds its OWN pi argv (`workflow.py:1791-1794`); it does
  **not** route through `dispatch.py`. The earlier "through the ONE router
  (`dispatch.py`)" wording was wrong.
- The fired falsifiers (`send.py` accepts a backtick-laden argv body;
  `write.py --actor` accepts a stranger) are retained above as prior art. They
  are outside the target's routing-only falsifier and are not part of the claim.
- `send.py` has **no** `--file`/stdin message-body route; the dm above is an
  argv-body round trip, not a file route.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.45 corrective round (a00-66b5e112). Replaces the wire probe: the PYTHONPATH-poisoned `dispatch.py` probe recorded here was non-probative — `workflow.py:72-73` inserts its own directory first on `sys.path`, so a PYTHONPATH poison can never shadow the real `dispatch.py`. The new probe installs a `builtins.__import__` guard around `runpy.run_path('extensions/agi/bin/workflow.py', ...)` that raises `AssertionError` on any import of `dispatch`; it ran `run review --dry-run` to `stages=2`, `exit=0`, no AssertionError, so the guard could have failed but did not. Static half: `grep -nE 'import dispatch|from dispatch' workflow.py` returns no lines (only comment/docstring/footer mentions, kept as the stale-string follow-up defect). Title updated to match. The routing claim is unchanged.
<!-- THOUGHT:END -->
