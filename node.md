---
id: hypothesis:a-workflow-pi-stage-retries-an-empty-provider-response-from-one-signature-cell
mint_id: e52afffc852a48d0996987e6a4294892
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: 046352ccf4b35ed9
season: 2
testable_claim: A workflow pi stage whose output carries 'Provider returned an empty response' is retried under the bounded backoff and named, like a 5xx; the signatures are ONE cell (config:workflows pi_transient_signatures) that workflow.py only reads, with the same list as its code fallback.
title: A workflow pi stage retries an empty provider response; the transient signatures live in one config:workflows cell (TMM.350)
town: core
---
# hypothesis:a-workflow-pi-stage-retries-an-empty-provider-response-from-one-signature-cell

## Measured
- 20:0x-20:4xZ 09-28 (director-engine, pi-free lane): 6 merge-up-review stages died `pi exited rc=1` on the line `Provider returned an empty response` (murq269 verify, murq270 verify, murq271 x2, murq272, murq273); 5 parents died 0-commit with no output in the same window (EG.148 163 164 166 173). Clean stages in the window: murq267, murq268. Box quiet (load1 about 2, io avg60 about 25).
- workflow.py `_PI_TRANSIENT_RE` (module constant) is the ONLY signature source for `_pi_failure_is_transient`: 5xx codes, stream / h2 protocol / upstream error, connection reset. It carries no empty-response signature, so such a stage takes the `rc != 0 WITHOUT the transient signature` branch: failed, never retried.
- `config:workflows` (.agi/nodes/.geometry/workflows.md) is already read by workflow.py `_load_geometry_node` (default_harness, types, workflows) -- the natural home for a signature cell.
- The EG.151 chain (hypothesis:an-empty-provider-response-is-retried-not-fatal) fixes the PARENT adapter's retry (pi_trajectory.py), not workflow stages; it is not yet on the post.

## CLAIM
A workflow pi stage whose output carries `Provider returned an empty response` is retried under the existing bounded backoff (`_PI_RETRY_BACKOFF_S`) and named in the attempts record, exactly like a 5xx. The signatures live in ONE cell, `pi_transient_signatures` on config:workflows (a list of regex fragments), whose value = today's `_PI_TRANSIENT_RE` fragments + the empty-response line; workflow.py only READS it (compiled once), falling back to the same list in code when the cell is absent, so the next signature is a cell edit, not code.

## Dispatch line
config-max: the signature list moves to config:workflows `pi_transient_signatures` / template-max: none / code: the reader in `_pi_failure_is_transient` (cell -> compiled regex, code fallback = the same list).

## FALSIFIERS
- a stage whose pi output is `Provider returned an empty response` with rc 1 is NOT retried, or its attempts record names no signature
- a non-transient rc (no signature) IS retried (test_non_transient_rc_is_never_retried must stay green)
- removing the cell leaves a stage with an empty response un-retried (the code fallback must carry the same list)
- a second source of the list survives in code (git grep for a signature literal outside the fallback)

## TESTS
test_workflow.py (the transient/retry family: test_transient_5xx_retries_bounded_and_named, test_non_transient_rc_is_never_retried, test_timeout_is_one_attempt_no_retry, test_transient_5xx_exhausts_at_three_attempts) + one new test per falsifier 1 and 3 + test_bin_help_smoke.py; --basetemp under /tmp; env -u TMUX -u TMUX_PANE; never a live pi call

## FILE SCOPE
extensions/agi/bin/workflow.py (`_PI_TRANSIENT_RE` / `_pi_failure_is_transient` only) · extensions/agi/tests/test_workflow.py · .agi/nodes/.geometry/workflows.md (write.py set pi_transient_signatures, the ONE new key) · the kid's own node. OUTSIDE: pi_trajectory.py (EG.151 chain) -- name on your node how it would read the same cell; the director folds that in when that chain merges.

## CEILING
1 kid · <= 15 production lines net · <= 50 test lines net · pi-free tier-0 · 0 USD · measure with a TWO-operand numstat <cut>..<tip before the paste commit>, labelled so · every cite names a function, heading or cell key

## ORDERS DH.EG.183 -- first round (TMM.350: dispatch now, jumps the queue)
BASE      CUT FROM the director-engine post tip fffe01959 (branch de-base-EG.183). No merge. Never rebase.
BRIEF     the node body above (Measured · CLAIM · Dispatch line · FALSIFIERS · TESTS · FILE SCOPE · CEILING) is the order; the kid answers the Dispatch line FIRST, before any code.
CELL      the signature list is a write.py set on config:workflows (key pi_transient_signatures, a list): a node, so cli.py done commits it -- never .agi/config.json.
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
ANON      no user name, home or repo path value, host or IP; patterns write <user>
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.183: TMM.350 TMM.350 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
