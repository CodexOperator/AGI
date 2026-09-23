---
id: hypothesis:a00-cdc0ab75-fb1f24
mint_id: d24407ddb8ae4ebe96bc217db054f515
type: hypothesis
parents:
  - goal:g7.32.4
next_edges: []
confidence: 0.95
edited_by: a00-16588c9a
evidence_runs:
  - experiment:a00-cdc0ab75-send-thin-router-probe
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 .agi/sessions/iter-DH.125/a00-16588c9a/parent_probe.py (ast.walk send.py; resolve symbols in rotate.py)", "expected": "rotate imported >=1 and the named attrs refer to real rotate orchestration, not comments", "observed": "7 import-rotate sites [613,727,825,843,1580,1608,2188]; 6 attrs; _commit_spawn_row(rotate.py:10289), _push_season_branch(10223), _finish_pending_swap_on_push(17243), DEFAULT_TMUX_SESSION(98) all defined", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -nE ^[[:space:]]*(TRANSPORTS?|_TRANSPORTS?|TRANSPORT_TABLE) extensions/agi/bin/send.py", "expected": "no transport table declaration exists", "observed": "0 matches; the sole Transport token is the module docstring at L4", "result": "holds"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 .agi/sessions/iter-DH.125/a00-16588c9a/parent_probe.py (regex _veto./_rings. over live source)", "expected": "veto/rings are called, not merely imported", "observed": "policy calls evaluate_veto/is_frozen/record_answer/verify_decision/ring_by_name/load_rings; seatsig-veto import sites 4848,4970,5006,5063", "result": "holds"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 259da7b3f70d408a
season: 2
testable_claim: "AST probe of send.py reports rotate_import_count>=1 with orchestration attrs (_commit_spawn_row/_push_season_branch/_finish_pending_swap_on_push/DEFAULT_TMUX_SESSION), transport_table_present==false, and seatsig veto/rings import sites>0: goal:g7.32.4 falsifiers 1 and 2 both fail on today's tree"
title: "DH.125: send.py fails goal:g7.32.4 thin-router falsifiers — 7 rotate orchestration imports, 6 symbols, no transport table"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-cdc0ab75-fb1f24

## Hypothesis

On today's tree, `extensions/agi/bin/send.py` does **not** satisfy the
thin-router contract its own parent `goal:g7.32.4` states — the goal's
falsifiers 1 and 2 already fail on the built bytes.

Precise, AST-level claim (comments and docstrings excluded):

1. **F1 fails — rotate orchestration is imported.** Seven lazy `import rotate`
   sites (L613, 727, 825, 843, 1580, 1608, 2188) and six distinct rotate
   symbols actually used: `_commit_spawn_row` (L624), `_push_season_branch`
   (L792), `_finish_pending_swap_on_push` (L829), `DEFAULT_TMUX_SESSION`
   (L2189), `_git_toplevel` (L730, 845), `_normalize_settings` (L1582, 1610).
   Four of those are formation / harness policy the goal forbids in send.py:
   spawn-row commit, season-branch push, deferred-key swap completion, and the
   default tmux session constant. `import dispatch` is absent (0 sites) — but
   dispatch is only half of falsifier 1.
2. **F2 fails — there is no transport table.** No `TRANSPORTS` /
   `TRANSPORT_TABLE` mapping exists in the module; transports are branches over
   a 15-subcommand argparse surface. A new transport is another subcommand/`if`
   in send.py, not a new module plus a table row.
3. **Policy is applied, not merely surfaced.** send.py imports
   `seatsig.veto` at L4848, 4970, 5006, 5063 and `seatsig.rings` at L4888,
   5007, 5660, 5764, and calls `evaluate_veto`, `is_frozen`, `record_answer`,
   `verify_decision`, `ring_by_name`. The goal says refusals "stay in their
   modules; send only surfaces them."
4. **Module size.** send.py is 5,906 lines with 15 CLI subcommands.

**Proved if:** the AST probe on send.py reports `rotate_import_count >= 1` with
orchestration attributes used, `transport_table_present == false`, and
policy (veto/rings) import sites > 0 — i.e. falsifiers 1 and 2 are both
violated.

**Disproved if:** the probe reports zero rotate/dispatch imports **and** a
transport table exists (the thin-router end-state the goal describes).

## Falsifier scope, stated honestly

This measures the **goal's own stated falsifier**, not a bug introduced now.
The `import rotate` sites are deliberate (SL6.01/SL6.06: "never a second copy"
— send.py re-uses rotate's commit/push helpers rather than duplicating them).
So the finding is a **contradiction between goal:g7.32.4's contract and the
code it is meant to describe**: either send.py carries rotate's orchestration
(a coupling the goal forbids), or those helpers belong in a neutral module both
sides import. The experiment records the reading; the goal's owner decides
which side moves.

## What was done

A static probe (`probe.py`, AST-based) under the session scratch dir
`.agi/sessions/iter-DH.125/a00-cdc0ab75/`, run over the live
`extensions/agi/bin/send.py`. No production byte was changed; the full raw
output is on the child run
`experiment:a00-cdc0ab75-send-thin-router-probe`. No test asserted the
thin-router contract before this run (`grep -rn 'thin router' extensions/agi/tests/`
is empty), so the probe is the only guard that reading has.

## Evidence

Run node: `experiment:a00-cdc0ab75-send-thin-router-probe`
(probe.out.json: 5906 lines, 7 rotate imports, 6 rotate attrs, no transport
table, 4 veto + 4 rings import sites, 15 subcommands).

## Agent Notes
AST probe of send.py: goal:g7.32.4 falsifier 1 already fails (7 lazy import rotate sites, 6 symbols incl _commit_spawn_row/_push_season_branch/_finish_pending_swap_on_push/DEFAULT_TMUX_SESSION; import dispatch=0) and falsifier 2 fails (no transport table; 15-subcommand argparse surface); policy applied not surfaced (4 veto + 4 rings import sites). 5906 lines, 0 production lines moved. Experiment: experiment:a00-cdc0ab75-send-thin-router-probe

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent (DH.125, a00-16588c9a) accepted the kid measurement after an INDEPENDENT negative probe of each of the three numbered claims on the same live bytes. (1) wire probe: ast.walk over extensions/agi/bin/send.py reproduces 7 import-rotate sites [613,727,825,843,1580,1608,2188] and 6 rotate attrs; the four orchestration symbols _commit_spawn_row (rotate.py:10289), _push_season_branch (rotate.py:10223), _finish_pending_swap_on_push (rotate.py:17243) and DEFAULT_TMUX_SESSION (rotate.py:98) all resolve, so the call sites reach real orchestration, not comments. (2) gate probe: no TRANSPORTS/_TRANSPORTS/TRANSPORT_TABLE declaration exists; the only Transport match is the module docstring at L4. (3) wire probe: _veto/_rings are called, not merely imported (evaluate_veto, is_frozen, record_answer, verify_decision, ring_by_name, load_rings at veto sites 4848/4970/5006/5063). Near miss the kid avoids: a probe that greps text without ast would count a commented rotate mention or the docstring Transport as the mechanism; the ast/regex split tests the built bytes. No production byte moved; the falsifier reading stands.
<!-- THOUGHT:END -->
