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


## CORRECTIVE DH.EG.185 -- TMM.350 + TMM.353: the signatures go INTO the config cell, the code is the reader (EG.183 shipped the reader, never the cell)
BASE      CUT FROM the EG.183 loop tip 2d0b3c8ed (parent a00-11db41a2; branch de-base-EG.185). Never rebase, never merge.
MEASURED  by the director at 2d0b3c8ed: workflow.py _load_geometry_node returns fm.get("pi_transient_signatures") and _pi_transient_re reads it -- but config:workflows (.agi/nodes/.geometry/workflows.md) carries NO pi_transient_signatures key (git grep -n pi_transient .agi/nodes/.geometry/workflows.md = 0 lines), and workflow.py keeps the SAME list as the literal tuple _PI_TRANSIENT_FALLBACK: two sources of one list, and the cell that is supposed to be the source is absent. Every live run today therefore matches on the code literal.
1. THE CELL -- write the five signatures of _PI_TRANSIENT_FALLBACK, byte-identical, as ONE list cell: python3 extensions/agi/bin/write.py config:workflows 'set pi_transient_signatures <the JSON list>' --actor <you>. Paste git grep -n -A6 '^pi_transient_signatures' .agi/nodes/.geometry/workflows.md showing the list landed AS A LIST, not a string.
2. CODE = THE READER -- delete the literal tuple _PI_TRANSIENT_FALLBACK from workflow.py. _pi_transient_re compiles the cell's fragments only. An absent, empty or unreadable cell = NO transient match plus ONE stderr line naming the missing cell (config:workflows pi_transient_signatures) -- loud, never a silent second list. No signature string may remain in workflow.py code: paste `git grep -n "empty response" extensions/agi/bin/workflow.py` and account for every hit (a comment naming the cell is fine; a literal the regex compiles is not).
3. TESTS -- in test_workflow.py: (a) the SHIPPED cell: load config:workflows from the real project root, assert a non-empty list that compiles and matches 'Provider returned an empty response' (the live-config guard; RED if the cell is removed -- paste that red by a fixture copy with the key dropped, never by editing the real node); (b) the cell IS the source: a fixture config:workflows whose list carries one NEW signature -> a stage failing with that text is retried, and the same text with the stock list is not; (c) absent cell -> no retry and the stderr line of item 2. Each new behaviour: paste a run that fails on the cut and passes on the tip.
4. THE EG.183 NODE -- experiment:a00-ca8fa749-b4f2a5 says the list has ONE source; re-state it to what the bytes now do (the cell), with write.py.
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in · ANCHOR RULE: a cite names a function / heading / cell key and adds a line number only where the claim IS the line
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
TESTS     env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/<dir> extensions/agi/tests/test_workflow.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_bin_help_smoke.py (timeout 900) -- paste the summary line
FILE SCOPE extensions/agi/bin/workflow.py (_pi_transient_re + the deleted _PI_TRANSIENT_FALLBACK only) · extensions/agi/tests/test_workflow.py · .agi/nodes/.geometry/workflows.md (write.py set, the ONE key) · experiment:a00-ca8fa749-b4f2a5 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 10 production lines net over 2d0b3c8ed (a deletion-heavy round: the tuple goes) · <= 40 test lines net over 2d0b3c8ed · pi-free tier-0 · 0 USD -- measure git diff --numstat 2d0b3c8ed <tip before the paste commit>, labelled so
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit (the config:workflows node included) on the loop branch before you exit (g7.33.19 row 13) · WRITE THE NODE EARLY and commit after every run: the provider drops turns ('Provider returned an empty response'), and a round that dies mid-turn records nothing

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.185: TMM.353 TMM.350 + TMM.353 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
