---
id: hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime
mint_id: 3bb99057832840819dc2e87af42cdaaf
type: hypothesis
parents:
  - goal:g15.20
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 94ad90aad3a063c6
season: 2
testable_claim: "OWNER 2026-09-11 18:1xZ (via prime XI, verbatim): 'consolidate g15.19 + g15.20 into a wave or two and hand off to sanctuary-director'. Minted by sanctuary-director 163547Z 18:2xZ from the prime's WAVE 1 order; the prime's measurement is the claim's mechanism. CAUSE OF X's DEATH, MEASURED by prime XI in belam.log:58240-58290: at 17:45:45.070Z a review subagent of wf_ba530baa-dab (agent-aaf904e3ae944d163 under ~/.claude/projects/-home-ubuntu-work-agi/e18063bd-…/subagents/workflows/) ran pytest on a hand-written probe (X's scratchpad test_probe_postjoin.py) that calls rotate.cmd_rotate_self(args, tmp_path) for a NON-chain fixture seat adv-alive with spawn_window + _read_ack patched but NO --own-chain seam; 0.9 s later (17:45:45.992Z) X began an ORDERLY teardown with no error line (SIGTERM path: uds shutdown, MCP SIGINT, presence clear, 'refusing end_session: this process is exiting', bridge torn down archive=200, .claude.json written by pid 3526521 at 17:45:48Z). MECHANISM (rotate.py ~6488-6520, the else-branch for a non-numeral seat): own_window_id absent -> pane_pid = _pane_pid($TMUX_PANE) = X's pane @281 (pytest ran INSIDE X's pane) -> _derive_own_chain(pane_pid) = bash -> claude 3526521 -> … -> TERM deepest-first; _reap_chain refuses only os.getpid() (test_reap_chain_refuses_own_pid), never the host claude above it. Preventable, in-loop. CLAIM = FIX: (a) the own-chain reap is REFUSED with a named reason when PYTEST_CURRENT_TEST is set and no --own-chain seam is given (mirror of L4.155 provisioning-under-pytest); (b) a derived chain is TERM'd only if it contains the seat ROW's own pid (authority against the graph) — a row with no pid or a mismatching pid -> SKIPPED, named in the record and on stdout; (c) tests/test_rotate_tail.py's _fix supplies a throwaway --own-chain seam by default so no future probe can reach a live pane; (d) the production path is unchanged when the row's pid is in the chain and pytest is absent (pinned by a test). EXPERIMENT: reproduce on a THROWAWAY tmux pane holding a sleep process — the same probe TERMs the sleep pre-fix, refuses post-fix (paste both). FALSIFIER: a cmd_rotate_self call under pytest with no seam that still derives a chain from $TMUX_PANE; or a chain without the row's pid that is TERM'd. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py reap region (~3390-3700 + the 6480-6540 branch) + extensions/agi/tests/test_rotate_tail.py. EXCLUDED: every other rotate.py region (first_turn/bootstrap/spawn/handoff are the sensei-director's; harvest-table is L4.279 live), every other file. SERIAL with this seat's other rotate.py rounds — the director orders the merges."
title: "rotate-self under pytest reaps the host prime: the own-chain reap refuses without a seam under PYTEST_CURRENT_TEST, TERMs only a chain holding the seat row's own pid, and test_rotate_tail supplies a throwaway --own-chain by default"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
