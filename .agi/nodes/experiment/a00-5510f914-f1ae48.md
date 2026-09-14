---
id: experiment:a00-5510f914-f1ae48
mint_id: 0e6ecc3cf4de454abccc1ed6258368f0
type: experiment
parents:
  - hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi
next_edges: []
confidence: 0.9
edited_by: a00-cd9b4aa1
evidence_runs:
  - experiment:a00-5510f914-f1ae48
loop: hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 551a6ec2b8e46c80
season: 2
title: "rotate.py spawns a copilot-cli seat: --harness builds copilot --model auto --allow-all-tools -i <card>, claude path byte-identical, 4579 suite green"
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-5510f914-f1ae48

**BUILD, not measurement.** Conjunct 6 of the parent build order: `rotate.py`'s
ONE launch path (`spawn_window`) now carries a third harness. `--harness
copilot-cli` builds an INTERACTIVE copilot seat; the default/absent/`claude-
code` path returns today's `claude --remote-control` argv **byte-identically**.
Proven on the built command (dry-run) and by 8 new fixture-only tests, with the
full engine suite green.

## The CLI fact the shape rests on (quoted from `copilot --help`, v1.0.83)

```
  -i, --interactive <prompt>            Start interactive mode and automatically
                                        execute this prompt
```

A copilot seat is therefore `copilot --model <M> --allow-all-tools -i '<card>'`:
interactive, the card executed as the first prompt, the process STAYING UP in
the tmux window. **There is NO `claude --remote-control` equivalent** — no
remote-control mode, no app-GUI session, no debug file to read the continuation
back from. So the owner watches the post **BY TMUX**; the pane is the watch
surface. `send.py`'s inbox + nudge still work unchanged because they are
pane-based and the window is a normal tmux window. The claude path's RC
read-back is simply skipped on the copilot branch; nothing is faked in its
place.

## The built command (dry-run, quoted)

```
$ python3 extensions/agi/bin/rotate.py spawn --name cop-test \
      --harness copilot-cli --tier director --dry-run

export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && \
  /home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -i '─── CONSTITUTION HEAD ───
  ... <the assembled brief: constitution head + zoom context + tier brief +
       skill prompt + closing line> ...
  Nobody scores how well you write this ...'
```

- the binary is the `harnesses.copilot-cli.bin` config cell;
- `--model auto` is `harnesses.copilot-cli.models['director']`, carried verbatim;
- `--allow-all-tools` is present; `-i` is present with the card as its value;
- `grep -c remote-control` on that output is **0** and there is **no
  `--debug-file`** — the two claude-only flags are absent by construction.

The default path is unchanged:

```
$ python3 extensions/agi/bin/rotate.py spawn --name cc-test --tier director --dry-run
... claude --remote-control cc-test --permission-mode bypassPermissions \
    --debug-file /home/ubuntu/work/agi/.agi/sessions/cc-test.log \
    --model claude-fable-5-1 --effort max '<card>'
```

…and `--harness claude-code` produces a byte-identical line to no `--harness`
(asserted by `test_explicit_harness_claude_code_matches_absent`).

## Code changed

| File | Change |
|---|---|
| `extensions/agi/bin/rotate.py` | `--harness` on `spawn` + `loop`; `_harness_row`, `_build_copilot_command`, `_build_harness_command`; `spawn_window(harness=...)` resolves the copilot model/bin from the `harnesses.copilot-cli` row and routes through `_build_harness_command`; the copilot watch line replaces the RC URL line |
| `extensions/agi/tests/test_rotate_copilot_harness.py` | **NEW** — 8 fixture-only tests |

Resolution rule: on the `copilot-cli` branch `spawn_window` reads
`harnesses.copilot-cli.models[tier]` (falling back to `models['director']`) and
`harnesses.copilot-cli.bin` — **never** `harnesses.claude-code` and never the
ladder via `load_role()`. The claude branch is untouched. The seat export
(`AGI_SEAT`/`AGI_POST`), the reaper-knob export and the window-name refusal are
all inherited because the copilot argv is routed through the same `_shell_cmd`
and `_launch_window`; a missing token is left to fail in the pane as itself
(the adapter's `child_env` resolves `GH_TOKEN`; rotate does not invent one).

**Scope stated plainly:** `--harness` is wired into `spawn` and `loop` (the two
verbs the brief named). `rotate-self` and `seats-launch` still pass no harness,
so they keep launching claude — that wiring is not claimed here.

## Tests

8 new fixture-only tests (no test starts a live `copilot`; the argv is read
from a dry-run string or built directly, and the config rows are written into a
tmp graph root so a copied live model list would certify nothing):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_copilot_harness.py -q
8 passed in 0.16s
```

Covering rotate/adapter/dispatch files:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_copilot_harness.py \
    extensions/agi/tests/test_spawn_name.py extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_copilot_cli_adapter.py \
    extensions/agi/tests/test_dispatch_dry_run.py -q
365 passed, 331 warnings in 40.69s
```

Full engine suite (explicit file list — the kid-tier gate refuses a bare
directory run):

```
$ python3 -m pytest <every extensions/agi/tests/test_*.py> -q
4579 passed, 15 skipped, 1 xfailed, 1581 warnings in 455.69s (0:07:35)
```

## Evidence

- Built-command dry-run above; `grep -c remote-control` on it is 0.
- `test_copilot_model_comes_from_its_own_row_never_claude`: a copilot spawn on
a root whose copilot row says `gpt-copilot-x` emits `--model gpt-copilot-x`
while the claude-code row says `claude-fable-5-1` — the claude name never
appears.
- `test_cmd_spawn_passes_harness_through` / `test_cmd_loop_passes_harness_through`:
the flag reaches `spawn_window` as `harness`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version exists because the parent is a BUILD ORDER, not a measurement
(`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`). Kid 2 made the
dispatch adapter spawn copilot non-interactively (`-p`, exits when done); that is
right for a fire-and-forget kid and WRONG for a seat, which must stay up and be
nudgeable. So the rotate path uses `-i`, not `-p`: same binary, different
contracts, and I state the distinction rather than reusing kid 2's argv.

The seam I chose is the SMALLEST one that satisfies the brief. I did not
rewrite `spawn_window` or its claude builder; I added a `harness` keyword whose
absent/`claude-code` value returns `_build_claude_command` byte-for-byte, and a
single `_build_harness_command` dispatch. The model resolution is branched INSIDE
`spawn_window` rather than left to `load_role()`, because `load_role()` falls back
to `harnesses.claude-code` and would silently hand a copilot seat a claude model
name — the exact failure the brief names.

I did NOT wire `--harness` into `rotate-self`/`seats-launch`: those are the
live seating verbs for the rolling fleet, and widening their flag surface at the
same time as adding a third harness would make one node responsible for two
unproven changes. The brief asked for `spawn` (+ `loop` if trivial), and that is
exactly what was built.
<!-- THOUGHT:END -->

## Agent Notes
rotate.py --harness copilot-cli ships: --harness on spawn+loop, spawn_window builds copilot --model auto --allow-all-tools -i <card> from harnesses.copilot-cli (never claude-code), claude path byte-identical when absent, no RC/debug-file on the copilot branch (watch by tmux; send.py pane-based still works); 8 new fixture-only tests, 365 covering + 4579 full suite green.

PARENT GATE PROBE (a00-cd9b4aa1, 2026-09-14) — DEMOTED from proved. Wire probe HOLDS: "rotate.py spawn --name cop-test-a00 --harness copilot-cli --tier director --dry-run" emits "/home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -i <card>" with zero remote-control and no --debug-file; default path still emits "claude --remote-control cc-test-a00". GATE PROBE FAILED: "rotate.py spawn --name bogus-test-a00 --harness does-not-exist --tier director --dry-run" SILENTLY fell back to "claude --remote-control bogus-test-a00" instead of refusing by name. A typo in --harness (e.g. copilot_cli, copilot) seats a claude post and burns the 3% CC budget the claim exists to conserve; dispatch refuses an unknown harness by name (adapters.resolve), rotate must too. Verdict demoted to inconclusive_lean_disproved:60 with this probe named. NOT let to ride: kid 4 is dispatched to add the named refusal and re-prove.
