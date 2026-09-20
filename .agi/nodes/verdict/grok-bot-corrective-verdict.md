---
id: verdict:grok-bot-corrective-verdict
mint_id: ba906ec20335434fb45479ff48c51a42
type: verdict
parents:
  - experiment:grok-bot-adapter-corrective-committed-evidence
next_edges: []
confidence: 0.85
edited_by: a00-24b27f5b
evidence_runs:
  - experiment:grok-bot-adapter-corrective-committed-evidence
line_ceiling: 40
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "name": "V1", "class": "wire", "cmd": "git show e554c440c:extensions/agi/bin/adapters/grok_bot_adapter.py | sha256sum  vs  sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py", "expected": "identical sha256", "observed": "both 66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c", "result": "held"}
  - {"conjunct": 2, "name": "V2", "class": "wire", "cmd": "comm -23 <(test names of e554c440c|ca330ac35) <(branch test names)", "expected": "empty for both sources", "observed": "empty; counts branch/e554/ca33 = 15/11/12; union contained", "result": "held"}
  - {"conjunct": 3, "name": "V3", "class": "wire", "cmd": "grep -in 'monkeypatch|FakeProc' probe.py ; cat probe_grok_bot_restart.out", "expected": "no mock hits; real live pid + is_alive True", "observed": "rc=1; new_pid 1733710 is_alive True; output_log_exists True", "result": "held"}
  - {"conjunct": 4, "name": "V4", "class": "wire", "cmd": "PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q ; ... test_adapters.py -q", "expected": "green", "observed": "15 passed in 0.81s; 35 passed in 0.30s", "result": "held"}
  - {"conjunct": 5, "name": "V5", "class": "gate", "cmd": "grep -in grok extensions/agi/bin/dispatch.py", "expected": "no hits, rc=1", "observed": "no output, rc=1", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4dbe4ae616760be7
season: 2
title: "Kid-2 verdict: grok-bot corrective is byte-honest; the grok-bot config row stays g17.14.2's"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-corrective-verdict

## Verdict

**`inconclusive_lean_proved:85`, confidence 0.85.**

The corrective bytes at `HEAD` (`1b015a7b6`) are byte-honest and the adapter
surface holds: V1–V5 all held under my own independent run, so the three MUR
residues (R1 committed probe evidence, R2 honest `production_lines=174`, R3
superset test file) are cleared **on the committed bytes**. What keeps this
short of a bare `proved` is one conjunct that is deliberately NOT landed here:
the `harnesses.grok-bot` row is worktree-only (absent from `HEAD`), so a fresh
checkout of this branch still fails `test_live_config_grok_row_resolves`. That
row is `goal:g17.14.2`'s deliverable; the merge plan below names it.

## Evidence (independently re-run on this worktree, `HEAD=1b015a7b6`)

### V1 — adapter is byte-identical to `e554c440c` (held)
```
$ git show e554c440c:extensions/agi/bin/adapters/grok_bot_adapter.py | sha256sum
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  -
$ sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  extensions/agi/bin/adapters/grok_bot_adapter.py
$ wc -l extensions/agi/bin/adapters/grok_bot_adapter.py
162
```
Equal sha256 → the branch file IS the committed DT.14 blob. A live import
confirms the REQUIRED surface: `NAME == 'grok-bot'`, all five `adapters.REQUIRED`
names callable, `resolve_bin` present, `needs_credential(...) is False`,
`model_args` returns `[]` with no `models` block and raises `KeyError` naming
`parent` for a missing tier, and stub
`build_command -> ['grok-bot', '--model', 'grok-4-fast', '-p', '/tmp/ctx.md']`.

### V2 — the test file is a true superset (held)
Branch file: **15** test names. `e554c440c`: **11**. `ca330ac35`: **12**.
`comm -23` of each source set against the branch set printed **nothing** — no
name from either source is missing, and the union is contained in the branch:
```
missing vs e554:      (empty)
missing vs ca330ac35: (empty)
counts branch/e554/ca33: 15 / 11 / 12
```
15 = 11 (restart/base) + 4 live-config-only names
(`test_dispatch_still_has_zero_grok_hits`, `test_live_bin_cell_threads_through_to_argv`,
`test_live_config_grok_row_resolves`, `test_live_config_peers_still_resolve`).
R3 cleared: no live-config peer test is deleted by the fold.

### V3 — the respawn probe is real and its output is committed (held)
`grep -in "monkeypatch\|FakeProc" extensions/agi/tests/probes/probe_grok_bot_restart.py`
→ **no hits (rc=1)**. The probe (68 lines) writes a throwaway `grok-bot` shell
script and drives `grok.restart` through the real `subprocess.Popen`, then
kills the child. The committed `.out` (15 lines, tracked) carries a live pid:
```
new_pid 1733710 is_alive True
argv_seen --model grok-4-fast -p /tmp/grokprobe-xrjai2w1/context.md
output_log_exists True
```
A stub cannot produce a live pid + `is_alive True`. R1 cleared: the evidence
lives in-tree at a path the merge target resolves, not under gitignored
`.agi/sessions/`.

### V4 — both suites green (held)
```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
15 passed in 0.81s
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_adapters.py -q
35 passed in 0.30s
```

### V5 — zero `grok` hits in `dispatch.py` (held)
```
$ grep -in grok extensions/agi/bin/dispatch.py ; echo rc=$?
rc=1
```
The adapter is reached through config + `adapters.load`, never by teaching the
dispatcher about the harness.

### Gate probe — the residue, proven from the committed tip (held, as designed)
```
$ git show HEAD:.agi/config.json  →  harnesses keys: ['claude-code','copilot-cli','pi','pi-local']
adapters.resolve(cfg, "grok-bot")  →  AdapterError:
  no harness 'grok-bot' in config; declared: ['claude-code','copilot-cli','pi','pi-local']
```
Worktree config, by contrast: keys `[... 'grok-bot' ...]` and
`resolve` returns the row. So the row exists ONLY in the worktree.

## The one residue and the merge plan

The `harnesses.grok-bot` row in `.agi/config.json` is **worktree-only**.

- **Mechanism (cited):** `extensions/agi/bin/cli.py` `_round_scope_ok` →
  `if p == ".agi/config.json": return False`. A kid/parent round's `done`
  commit may never add `.agi/config.json`, so no round here can land that row.
- **Owner:** the row is `goal:g17.14.2`'s deliverable; it is present on the
  live-config line at `ca330ac35` / `ca3b2da28`.
- **Consequence:** a fresh checkout of this branch fails
  `test_live_config_grok_row_resolves` (and would fail
  `test_live_bin_cell_threads_through_to_argv` / `test_live_config_peers_still_resolve`
  only in their grok assertion; the peer assertion is fine).
- **Merge plan:** the fold must take the `grok-bot` config row from the
  live-config line (`ca330ac35` / `ca3b2da28`). Because this branch's test file
  is a SUPERSET of the live-config file's, taking that row deletes no peer test
  — the two merge cleanly, and `test_live_config_grok_row_resolves` then passes
  on the merged tip.

## What this verdict does NOT prove

- It does **not** prove the `grok-bot` row is landed. It is not, on `HEAD`.
- It does **not** prove the adapter's `build_command` argv matches any real
  `grok-bot` CLI — the argv is a documented stub, deliberately (see
  `goal:g17.14.1` "stub measurable argv"). Real flag parity is later work.
- It does **not** re-derive `production_lines=174`; that is taken from the
  experiment's frontmatter (162 adapter + 12 config lines in the worktree).
- It does **not** prove the probe child always exits — the probe kills it with
  `SIGKILL`, so `is_alive True` is measured before the reap, which is the point.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version: this verdict is the missing second angle on kid 1's corrective. V1–V5 were re-run by me, not copied from kid 1's experiment body; V2 is a set-containment proof (`comm -23`), V3 reads the committed `.out`, and the gate probe loads `git show HEAD:.agi/config.json` specifically to make the residue mechanical rather than asserted. The verdict stops at `inconclusive_lean_proved:85` because one conjunct (the config row) is unlanded and `cli.py _round_scope_ok` structurally forbids this round from landing it.
<!-- THOUGHT:END -->

## Agent Notes
Independent V1-V5 verification of kid 1's grok-bot corrective on HEAD=1b015a7b6: adapter sha256 == e554c440c blob, test file is a set-superset of e554c440c+ca330ac35, in-tree probe unmocked with live pid 1733710/is_alive True, suites 15+35 green, dispatch.py zero grok hits. Gate probe on git show HEAD:.agi/config.json yields AdapterError: the harnesses.grok-bot row is worktree-only, so test_live_config_grok_row_resolves fails on a fresh checkout until goal:g17.14.2 lands that row; merge plan: fold the row from ca330ac35, no peer test lost because our test file is a superset.
