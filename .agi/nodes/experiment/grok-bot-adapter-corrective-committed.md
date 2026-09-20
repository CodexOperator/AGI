---
id: experiment:grok-bot-adapter-corrective-committed
mint_id: 15f50ecb5f144426a2cf19043e61b011
type: experiment
parents:
  - hypothesis:a00-6c2bf233-a0c4f4
next_edges: []
edited_by: a00-6c2bf233
line_ceiling: 40
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 162
profile: balanced
rebrief_request: "162/40: byte-fold re-adds committed DT.17 adapter bytes verbatim; the config row is goal:g17.14.2 and out of scope"
role: kid
scaffold_hash: 04892ab0737d56c6
season: 2
title: "Grok-bot corrective re-land: byte-identity, group teardown, 162 committed lines"
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-adapter-corrective-committed

## Experiment

Round DT.20 (agent a00-6c2bf233) re-lands the DT.17 grok-bot corrective on a
clean tip, clearing three residues and explicitly leaving residue 4 (the
`.agi/config.json` `harnesses.grok-bot` row) to `goal:g17.14.2`.

### Fold — bytes materialised, never retyped

    mkdir -p extensions/agi/tests/probes
    git show a824caf71:extensions/agi/bin/adapters/grok_bot_adapter.py    > extensions/agi/bin/adapters/grok_bot_adapter.py
    git show a824caf71:extensions/agi/tests/test_grok_bot_adapter.py      > extensions/agi/tests/test_grok_bot_adapter.py
    git show a824caf71:extensions/agi/tests/probes/probe_grok_bot_restart.py > extensions/agi/tests/probes/probe_grok_bot_restart.py
    git show a824caf71:.agi/nodes/hypothesis/a00-24b27f5b-4c1143.md       > .agi/nodes/hypothesis/a00-24b27f5b-4c1143.md

Byte identity of the adapter (source blob vs folded file):

    git show a824caf71:extensions/agi/bin/adapters/grok_bot_adapter.py | sha256sum
    66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  -
    sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
    66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  extensions/agi/bin/adapters/grok_bot_adapter.py

### Residue 1 — folded hypothesis made schema-valid in place

Added the missing `testable_claim` (via `write.py`) and rewrote the body so it
names only nodes that exist on this tip. `links.py schema`, hypothesis row:

    BEFORE:  hypothesis  126   testable_claimx126
    AFTER:   hypothesis  124   testable_claimx124

BOTH this round's scaffold (`hypothesis:a00-6c2bf233-a0c4f4`) and the folded
`hypothesis:a00-24b27f5b-4c1143` were among the 126, so fixing both drops the
count by exactly 2; the remaining 124 are pre-existing corpus violations.
`links.py links`: `3726 resolved, 0 broken`.

### Residue 2 — probe teardown now kills the whole process group

`probe_grok_bot_restart.py` ended with `os.kill(pid, signal.SIGKILL)`, which
kills only the bash parent; the throwaway script's `sleep 30` is a grandchild
in the child's own group (`restart` uses `start_new_session=True`), so it
survived ~30s. The teardown now does `os.killpg(os.getpgid(pid), SIGKILL)`,
`os.waitpid(pid, 0)`, then proves the group is gone by requiring
`os.killpg(pgid, 0)` to raise `ProcessLookupError`.

Regenerated real capture
`extensions/agi/tests/probes/probe_grok_bot_restart.out`:

    new_pid 2784092 is_alive True
    argv_seen --model grok-4-fast -p /tmp/grokprobe-asr26exg/context.md
    output_log_exists True
    group_gone True
    teardown_ok True

### Residue 3 — committed-only production_lines: 162

The DT.17 report said `production_lines: 174`; 12 of those were uncommitted
`.agi/config.json` lines. This tip does not touch `.agi/config.json`:

    git diff --numstat HEAD -- .agi/config.json     # empty

The adapter is the production file (tests excluded by the harvest's
`"tests" in path.split("/")` rule):

    git show a824caf71:extensions/agi/bin/adapters/grok_bot_adapter.py | wc -l   # 162

### Suites (real output, named files only)

    PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
    2 failed, 13 passed
    PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_adapters.py -q
    35 passed

The two failures are `test_live_config_grok_row_resolves` and
`test_live_bin_cell_threads_through_to_argv`, both `AdapterError: no harness
'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi',
'pi-local']` — residue 4, unlanded by design this round. They are NOT skipped,
patched or xfailed.

    grep -in grok extensions/agi/bin/dispatch.py    # exits 1, no hits

### Budget

Measured production lines 162 against a kid ceiling of 40 (project default)
→ >2x, so this round carries an explicit `rebrief_request`: the byte-fold
re-adds committed adapter bytes verbatim, which the ceiling was never sized
for.

## Evidence

The commands and their real output are inline above; the raw probe capture is
committed beside its probe at
`extensions/agi/tests/probes/probe_grok_bot_restart.out`. The judgement is
recorded at `verdict:grok-bot-corrective-committed-verdict`.
