---
id: hypothesis:l4-the-manifest-mirror-is-locked-and-terminal-only
mint_id: 08d4129eca534fd4ab6e6d03524d7afb
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-manifest-mirrors-terminal-agent-status
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7394f492657fb26b
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (3) dispatch.py:2191 (the reap-pass mirror, helper p1) can mirror a `stalled` for a pid that is still live, and cli.py:529 (cmd_done's mirror) writes the manifest without _manifest_lock and without tmp+os.replace, while dispatch.py:526-556 already has both -- two writers, one of them unlocked and non-atomic. CLAIM: the mirror set is TERMINAL statuses ∪ {timeout} only -- a live-pid `stalled` is never mirrored; the cli.py mirror goes through _manifest_lock and tmp+os.replace (share the one helper, do not copy it). TESTS: a fixture manifest + agent.json with status stalled and a live pid stays unmirrored; a concurrent writer test (two mirrors racing) leaves a parseable manifest; the mirror path in cli.py is the shared helper (source pin acceptable as the third assertion only). FALSIFIER: a manifest that mirrors a live-pid stalled, or a truncated manifest after a race. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/dispatch.py (the mirror pass + the shared helper) + extensions/agi/bin/cli.py (cmd_done mirror only) + test_dispatch.py / test_cli.py. Helper's lane (owns p1)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the manifest mirror writes only terminal statuses (plus timeout) and every writer goes through the manifest lock with tmp+os.replace
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-manifest-mirror-is-locked-and-terminal-only

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (3) dispatch.py:2191 (the reap-pass mirror, helper p1) can mirror a `stalled` for a pid that is still live, and cli.py:529 (cmd_done's mirror) writes the manifest without _manifest_lock and without tmp+os.replace, while dispatch.py:526-556 already has both -- two writers, one of them unlocked and non-atomic. CLAIM: the mirror set is TERMINAL statuses ∪ {timeout} only -- a live-pid `stalled` is never mirrored; the cli.py mirror goes through _manifest_lock and tmp+os.replace (share the one helper, do not copy it). TESTS: a fixture manifest + agent.json with status stalled and a live pid stays unmirrored; a concurrent writer test (two mirrors racing) leaves a parseable manifest; the mirror path in cli.py is the shared helper (source pin acceptable as the third assertion only). FALSIFIER: a manifest that mirrors a live-pid stalled, or a truncated manifest after a race. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/dispatch.py (the mirror pass + the shared helper) + extensions/agi/bin/cli.py (cmd_done mirror only) + test_dispatch.py / test_cli.py. Helper's lane (owns p1).
