---
id: hypothesis:an-empty-provider-response-is-retried-not-fatal
mint_id: 1e66c41fbaee45b0985f7e24a1860443
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 91bb770a1fb1bf7b
season: 2
testable_claim: an empty-response stopReason=error is retried a bounded, config-set number of times with backoff and logged; other errors end the round as today
title: "An empty provider response is retried, not fatal (EG.30, TMM.317, assigned: director-engine)"
town: core
---
# hypothesis:an-empty-provider-response-is-retried-not-fatal

## ROUND EG.30 (thought-master TMM.317 03:17Z 09-28: the empty-response retry = an engine fix under goal:g7.33, dispatched right after the EG.9 chain, pi-free)
Measured   02:45-03:15Z 09-28: 5 parent rounds (DH.660 EG.18 EG.19 DH.661 EG.20) died with 0 commits, each after 3 x `"stopReason":"error"` / `"errorMessage":"Provider returned an empty response"` in its output.log (director grep over iter-*/<agent>/output.log; dead logs kept as the director's d<N>.dead1.log), plus EG.23's kid died on its last write. Nothing retries: one transient empty response ends a whole round.
CLAIM      an empty-response stopReason=error from the provider is retried a BOUNDED number of times with backoff (count and delays are config cells), each retry counted in the round log; any other error, or the bound exhausted, ends the round exactly as today.
Dispatch line  config-max: the retry count and backoff are cells (a values.* or harness cell next to the existing pi harness settings), never literals · template-max: none · code: the retry in the pi wrapper only
FIRST ACT  MEASURE before any code: find where pi_trajectory.py (or the harness it wraps) sees the provider's stopReason=error, and paste the lines; reproduce with a committed test that feeds a stub pi emitting one empty-response error then a normal stop, RED on the base (the round dies), GREEN after.
FALSIFIERS the retry fires on a non-empty-response error · no bound (an always-empty provider loops forever) · the retry count is a literal · a retried round's log does not show the retries
TESTS      the new test file + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); stub pi only, never the live provider
FILE SCOPE extensions/agi/bin/pi_trajectory.py · its new test under extensions/agi/tests/ · .agi/config.json (the retry cells only) · the kid's own node
CEILING    HARD CAP: 1 kid · <= 25 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- measure against the cut tip, paste the numstat
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit; check git status -s in the KID worktree before you accept


## CORRECTIVE EG.34 -- closes mur-eg-11 EG.30-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-99e01741 tip 9e9d44ee8 (branch de-base-EG.34; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
ORDERS    THIS text is the order set; the loop branch's copy of the hypothesis node does not carry the director's CORRECTIVE sections (the post branch does) -- never report that as a defect.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. values.pi_retry absent from the shipped .agi/config.json, so the live bound is the code default (2/5.0s) and the cell is a no-op
2. 3. test_cancel_while_pi_runs_is_still_forwarded cannot tell forwarding from plain death and never checks the child
3. 4. The parent's hand-landed bytes-decode repair of the spawn path has no committed regression test
4. 5. A discarded attempt's trajectory records survive the retry (append mode per attempt) and the retry has no exit-code guard
5. 7. Unreachable `return code` tail in the retry loop
6. 8. Verdict frontmatter contradicts the node's own THOUGHT (lean_disproved:65 vs the written lean_proved:75) and the title still says proved
7. 10. Hypothesis left verdict-less after a decided round
8. The engine already OWNS a file for exactly this failure: extensions/agi/tests/test_live_config_cells.py ('exactly ONE place in the suite reads the live .agi/config.json ... if a cell is removed from the real config, this goes red'). No test was added there for values.pi_retry, so the absent cell that defect 1 names is the one failure that file exists to catch, and the config-max dispatch line (hypothesis:...not-fatal.md:20) has no guard behind it. This is the actionable form of defect 1.
9. The node's config evidence is unfalsifiable as written: a00-5b8a7c8a-39874b.md:73-78 shows 'The cells resolve live in this worktree: live cells -> (2, 5.0)' - but (2, 5.0) IS the module default (pi_trajectory.py:36-37), so that print is identical whether the cell is read or ignored. Re-run live, the cell is None; the evidence line cannot distinguish the two cases and should not be cited as proof the cell resolves.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_live_config_cells.py test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/config.json (the ONE cell values.pi_retry {empty_response_max_retries, empty_response_backoff_s}; config-max, mur-eg-11: the claim is built on it and it is absent from the shipped config) · extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_live_config_cells.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-5aca24e8-1cf709.md · .agi/nodes/experiment/a00-5b8a7c8a-39874b.md · .agi/nodes/experiment/a00-e9c1e478-16f094.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 9e9d44ee8 · <= 40 test lines net over 9e9d44ee8 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 9e9d44ee8 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.34: mur-eg-11 EG.30-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
