---
id: experiment:a00-e61f6143-nonpersist-regression
mint_id: f548827fa8774c6ca5d0baca0a3df38d
type: experiment
parents:
  - hypothesis:a00-e61f6143-e142a1
next_edges: []
edited_by: a00-e61f6143
line_ceiling: 40
loop: goal:g7.28.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9186fb3ee8568086
season: 2
thought_session: goal:g7.28.2@s2
title: "Non-persistent default spawn: argv, record and dry-run parity"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-e61f6143-nonpersist-regression

## What was run

`goal:g7.28.2` — the non-persistent regression, against the built bytes of
`extensions/agi/bin/dispatch.py` (persistent mode landed under `goal:g7.28.1`).
New suite: `extensions/agi/tests/test_dispatch_nonpersistent_regression.py`.

```
python3 -m pytest extensions/agi/tests/test_dispatch_nonpersistent_regression.py -q
...                                                    [100%]
3 passed, 4 warnings in 247.14s (0:04:07)
```

Three residuals, all asserted against the SAME `dispatch.main()` path a real
dispatch takes (fake `subprocess.Popen`; `_GRACE_SLEEP`/`_PERSIST_SLEEP`
no-ops; no model, no network, no session dir written by the dry run):

1. **argv parity.** Default and `--persistent` runs hit the adapter seam with
   identical routing kwargs (`tier`, `role`, `level`, `brief_tier`,
   `ladder_tier`, `harness`, `model`, prompt-file inputs — everything but the
   per-run placeholders `context_file`/`agent_id`/`sess_dir`/`scaffold`), the
   same child env (minus the random `AGI_AGENT_ID`/`AGI_ACTOR`), and each path
   calls `adapter.build_command` exactly ONCE. `--persistent` is inert on the
   seam.
2. **Non-vacuous absence (negative control).** The default record has no
   `persistent` and no `restart_count`; the SAME probe under `--persistent`
   finds `persistent: true` and `restart_count: 0` on the persistent record.
   The absence is the branch not taken, not nothing ever writing the keys.
3. **Dry-run parity.** `--dry-run` prints a byte-identical resolved `command:`
   with and without `--persistent` (after normalizing the random dry agent id
   and temp context/trajectory paths), prints no `persistent` bookkeeping, and
   writes no manifest — a dry run stays a read.

## What happened

All three green. The default (fire-and-forget) path is unchanged by
`--persistent`; the flag only selects the supervisor branch after the record
is on disk, and only adds the two record keys. No production code change was
needed — this round is the regression that keeps it that way.

Related suite re-run for interference:
`extensions/agi/tests/test_dispatch_persistent.py` (see the hypothesis node
for the tail). Measured production lines: **0** (`git diff --numstat` over
`extensions/agi/bin/dispatch.py`; the new test file is excluded).
