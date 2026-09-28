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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.30 placed EARLY, 03:34Z 09-28, BEFORE the EG.9 chain (TMM.318 ordered it after EG.9). Mechanism: qgEG30.sh waited on `systemctl is-active qgEG29`; gen 35 stopped qgEG29 when the owner cancelled EG.29 (director did the docstring itself, 6d78c51bf), so the wait returned at once and the gate placed EG.30 on the next clean load/io read. Ruling, thought-master TMM.320 verbatim: "(4) EG.30 placed early: KEEP it running. It shares no file with the heal sweep and the box is fine (load1 4.3, io avg60 20). Record the deviation (placed 03:34Z before EG.9, why) in EG.30's node THOUGHT." Near miss for the queue: a chain keyed on is-active of a STOPPED predecessor unit fires at once -- re-key a wait whenever its predecessor is cancelled.
<!-- THOUGHT:END -->
