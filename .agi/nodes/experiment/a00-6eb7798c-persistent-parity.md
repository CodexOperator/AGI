---
id: experiment:a00-6eb7798c-persistent-parity
mint_id: 6eb7798c-persistent-parity
type: experiment
parents:
  - hypothesis:a00-6eb7798c-c3dfb5
edited_by: a00-ce370a10
line_ceiling: 40
probes: "wire: custom parent probe loaded production dispatch.main with subprocess.Popen replaced, invoked the real default argv, and observed one detached Popen call plus a manifest record without persistent/restart_count; this reaches the changed launch path live."
production_lines: 0
title: Dispatch persistent launch-byte parity experiment
---
# experiment:a00-6eb7798c-persistent-parity

## Claim under test

An omitted `--persistent` flag preserves the production dispatch launch
bytes, while the flag changes only the child lifecycle. This experiment
captures the real production `subprocess.Popen` argv and environment for
both modes, scrubs only the expected random agent/node identifiers and the
supervisor-only stop control, and compares the remaining bytes. It also
checks the negative control: the default manifest has no persistent field,
while the persistent manifest does.

## Command and result

```text
python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py -q
4 passed, 5 warnings in 42.65s
```

The new behavioral test passed. The three pre-existing tests also passed:
persistent restart reuses the exact argv, default fire-and-forget does not
restart, and the persistent record carries its live pid/restart count.

The test is intentionally a dispatch seam, not source inspection: the
production `dispatch.main()` path is invoked twice with a fake detached child
and the actual Popen argv/env captured. Dynamic agent/node ids and the
persistent stop environment are the only expected differences and are
removed before comparison.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to run the real dispatch seam rather than inspect source. The experiment records production dispatch.main invocations and a parent wire probe independently reached Popen once on the omitted-flag path, with no persistent bookkeeping. The near miss would be a static guard inspection or a test-only fake that never calls dispatch.main; that would leave argv/environment parity unproved. The evidence is sufficient for the narrow claim, but the parent did not re-run the kid pytest suite.
<!-- THOUGHT:END -->

## Agent Notes
Parent review: accepted the behavioral experiment; one custom wire probe held. The earlier kid a00-f77f8efe remains incomplete/pending because it only inspected source and was superseded by this experiment.
