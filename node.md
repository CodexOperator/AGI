---
id: hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan
mint_id: d049166055d2465ba4b7ecb188cf871e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-reaper-is-one-persistent-service
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 36710b2cf8514829
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI 06:3xZ, ACCEPTED by the prime 06:35Z as proposed. p8, MEASURED 06:27Z: `test_reconciler.py` (2 tests at :201/:213) reads a FROZEN L4.85 worktree artifact whose agent record must be the lie `running`; the reaper SERVICE (`heal.py watch --root /home/ubuntu/work/agi`, live since 05:06Z) scans `.agi/worktrees/*/.agi/sessions/iter-*/manifest.json` and reconciled that frozen record `running → stalled` on its first pass, so the two tests FAIL in every worktree where the artifact resolves (`AssertionError: the frozen record must be the lie / assert 'stalled' == 'running'`) and SKIP in MAIN (`frozen L4.85 worktree not present; evidence is elsewhere`). CLAIM: frozen evidence never sits where the live reaper writes — EITHER (A) the test freezes its OWN copy of the L4.85 artifact under `extensions/agi/tests/fixtures/` (committed, read-only, the record `running` by construction) and no longer resolves a live worktree path, OR (B) the reaper honours a `.frozen` marker file in an iter dir and skips it with one log line, and the artifact carries the marker. Prefer (A) (evidence in the suite, no reaper special case); (B) only if the artifact must stay where it is — say why. TESTS: the two reconciler tests green in MAIN AND in a worktree (paste both runs); with (B), a fixture round carrying `.frozen` is untouched by one watch pass. FALSIFIER: a reaper pass that mutates the frozen record. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_reconciler.py + fixtures (A) / heal.py `_discover_rounds` (B) + tests. EXCLUDED: rotate.py, dispatch.py, the live reaper unit (never `heal.py watch` against the live sessions dir). Serial behind p1 (`hypothesis:l4-the-manifest-mirrors-terminal-agent-status`) only if (B) touches heal.py."
title: The reconciler tests' frozen L4.85 artifact is outside the reaper service's scan path (or the test freezes its own copy)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI 06:3xZ, ACCEPTED by the prime 06:35Z as proposed. p8, MEASURED 06:27Z: `test_reconciler.py` (2 tests at :201/:213) reads a FROZEN L4.85 worktree artifact whose agent record must be the lie `running`; the reaper SERVICE (`heal.py watch --root /home/ubuntu/work/agi`, live since 05:06Z) scans `.agi/worktrees/*/.agi/sessions/iter-*/manifest.json` and reconciled that frozen record `running → stalled` on its first pass, so the two tests FAIL in every worktree where the artifact resolves (`AssertionError: the frozen record must be the lie / assert 'stalled' == 'running'`) and SKIP in MAIN (`frozen L4.85 worktree not present; evidence is elsewhere`). CLAIM: frozen evidence never sits where the live reaper writes — EITHER (A) the test freezes its OWN copy of the L4.85 artifact under `extensions/agi/tests/fixtures/` (committed, read-only, the record `running` by construction) and no longer resolves a live worktree path, OR (B) the reaper honours a `.frozen` marker file in an iter dir and skips it with one log line, and the artifact carries the marker. Prefer (A) (evidence in the suite, no reaper special case); (B) only if the artifact must stay where it is — say why. TESTS: the two reconciler tests green in MAIN AND in a worktree (paste both runs); with (B), a fixture round carrying `.frozen` is untouched by one watch pass. FALSIFIER: a reaper pass that mutates the frozen record. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_reconciler.py + fixtures (A) / heal.py `_discover_rounds` (B) + tests. EXCLUDED: rotate.py, dispatch.py, the live reaper unit (never `heal.py watch` against the live sessions dir). Serial behind p1 (`hypothesis:l4-the-manifest-mirrors-terminal-agent-status`) only if (B) touches heal.py.
