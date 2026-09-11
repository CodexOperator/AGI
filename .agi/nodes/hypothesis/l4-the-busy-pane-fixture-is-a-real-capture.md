---
id: hypothesis:l4-the-busy-pane-fixture-is-a-real-capture
mint_id: 17b9e117c91a46ddb57fcf52452cfa15
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-nudge-is-a-wake-token-not-a-message
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 68a5aefc87af5feb
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-5: extensions/agi/tests/test_send.py:152-160 — the busy fixture drops the `❯` input box the real pane keeps, so the input-region-scoped busy check (L4.126) is tested against a pane shape the live pane never has; the prime's real-pane measurement PASSED (helper @248 busy: region starts at the ❯ box, 'pane busy (spinner)') but a narrower region could stay green on the fixture. CLAIM: the fixture carries a REAL capture (paste an actual `tmux capture-pane -p` of a busy Claude Code pane with the ❯ box and a spinner, and one of an idle pane, as fixture files or literals — scrub nothing that shapes the region, redact only text content), the busy/idle tests read them, and a mutation that narrows the region to exclude the ❯ box FAILS the busy test (paste the run). FALSIFIER: the busy test stays green with the region narrowed. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_send.py (+ fixture files under extensions/agi/tests/fixtures/ if used) ONLY; send.py is byte-identical unless the real capture exposes a defect — say so with the failing run. SERIAL behind g15-9 (hypothesis:l4-the-nudge-carries-the-dm-body-inline) on test_send.py — do not start until it is harvested. EXCLUDED: send.py logic, rotate.py."
title: test_send's busy-pane fixture is a real tmux capture (with the ❯ box) so a narrower region cannot stay green
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-busy-pane-fixture-is-a-real-capture

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-5: extensions/agi/tests/test_send.py:152-160 — the busy fixture drops the `❯` input box the real pane keeps, so the input-region-scoped busy check (L4.126) is tested against a pane shape the live pane never has; the prime's real-pane measurement PASSED (helper @248 busy: region starts at the ❯ box, 'pane busy (spinner)') but a narrower region could stay green on the fixture. CLAIM: the fixture carries a REAL capture (paste an actual `tmux capture-pane -p` of a busy Claude Code pane with the ❯ box and a spinner, and one of an idle pane, as fixture files or literals — scrub nothing that shapes the region, redact only text content), the busy/idle tests read them, and a mutation that narrows the region to exclude the ❯ box FAILS the busy test (paste the run). FALSIFIER: the busy test stays green with the region narrowed. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_send.py (+ fixture files under extensions/agi/tests/fixtures/ if used) ONLY; send.py is byte-identical unless the real capture exposes a defect — say so with the failing run. SERIAL behind g15-9 (hypothesis:l4-the-nudge-carries-the-dm-body-inline) on test_send.py — do not start until it is harvested. EXCLUDED: send.py logic, rotate.py.
