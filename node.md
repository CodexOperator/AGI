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
BASE      CUT c2404cc17 = the EG.183 loop tip 2d0b3c8ed merged with the town trunk (values.pi_retry 12 x 60 s, 86bbc1bd8; TMM.354/360); branch de-base-EG.185. Never rebase, never merge again.
MEASURED  by the director at 2d0b3c8ed: workflow.py _load_geometry_node returns fm.get("pi_transient_signatures") and _pi_transient_re reads it -- but config:workflows (.agi/nodes/.geometry/workflows.md) carries NO pi_transient_signatures key (git grep -n pi_transient .agi/nodes/.geometry/workflows.md = 0 lines), and workflow.py keeps the SAME list as the literal tuple _PI_TRANSIENT_FALLBACK: two sources of one list, and the cell that is supposed to be the source is absent. Every live run today therefore matches on the code literal.
1. THE CELL -- write the five signatures of _PI_TRANSIENT_FALLBACK, byte-identical, as ONE list cell: python3 extensions/agi/bin/write.py config:workflows 'set pi_transient_signatures <the JSON list>' --actor <you>. Paste git grep -n -A6 '^pi_transient_signatures' .agi/nodes/.geometry/workflows.md showing the list landed AS A LIST, not a string.
2. CODE = THE READER -- delete the literal tuple _PI_TRANSIENT_FALLBACK from workflow.py. _pi_transient_re compiles the cell's fragments only. An absent, empty or unreadable cell = NO transient match plus ONE stderr line naming the missing cell (config:workflows pi_transient_signatures) -- loud, never a silent second list. No signature string may remain in workflow.py code: paste `git grep -n "empty response" extensions/agi/bin/workflow.py` and account for every hit (a comment naming the cell is fine; a literal the regex compiles is not).
3. TESTS -- in test_workflow.py: (a) the SHIPPED cell: load config:workflows from the real project root, assert a non-empty list that compiles and matches 'Provider returned an empty response' (the live-config guard; RED if the cell is removed -- paste that red by a fixture copy with the key dropped, never by editing the real node); (b) the cell IS the source: a fixture config:workflows whose list carries one NEW signature -> a stage failing with that text is retried, and the same text with the stock list is not; (c) absent cell -> no retry and the stderr line of item 2. Each new behaviour: paste a run that fails on the cut and passes on the tip.
4. THE EG.183 NODE -- experiment:a00-ca8fa749-b4f2a5 says the list has ONE source; re-state it to what the bytes now do (the cell), with write.py.
5. ONE RETRY SOURCE (TMM.360 item 3) -- the workflow-stage retry reads THE SAME values.pi_retry cells the parents read: call pi_trajectory.py _retry_cells (import it the bin-script way, as workflow.py imports its other bin modules) for the bound and the backoff, and delete the literal _PI_RETRY_BACKOFF_S. No second reader, no second default. A mur stage then gets the parents' tolerance (12 x 60 s today). Test: a fixture config with values.pi_retry = 3 x 0.0 s -> a stage failing on the empty-response signature runs exactly 4 attempts; paste it failing on the cut, passing on the tip. (EG.186 will extend _retry_cells itself -- consecutive budget + growing backoff -- so this call is the only hook it needs.)
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in · ANCHOR RULE: a cite names a function / heading / cell key and adds a line number only where the claim IS the line
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
TESTS     env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/<dir> extensions/agi/tests/test_workflow.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_bin_help_smoke.py (timeout 900) -- paste the summary line
FILE SCOPE extensions/agi/bin/workflow.py (_pi_transient_re + the deleted _PI_TRANSIENT_FALLBACK + the deleted _PI_RETRY_BACKOFF_S and the stage retry loop that read it, item 5) · extensions/agi/tests/test_workflow.py · .agi/nodes/.geometry/workflows.md (write.py set, the ONE key) · experiment:a00-ca8fa749-b4f2a5 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 20 production lines net over c2404cc17 (the tuple goes; item 5 adds the shared reader call) · <= 40 test lines net over c2404cc17 · pi-free tier-0 · 0 USD -- measure git diff --numstat c2404cc17 <tip before the paste commit>, labelled so
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit (the config:workflows node included) on the loop branch before you exit (g7.33.19 row 13) · WRITE THE NODE EARLY and commit after every run: the provider drops turns ('Provider returned an empty response'), and a round that dies mid-turn records nothing


## CORRECTIVE DH.EG.188 -- TMM.361: the transient signatures live in values.pi_retry.transient_signatures (.agi/config.json), not config:workflows -- one source for the whole pi retry policy
BASE      CUT 27beb2eb0 = the EG.185 loop tip 0789fd376 (parent a00-6ccb7e1d, kid a00-be655ee1) merged with the town trunk, which carries the cell (thought-master, trunk ee40e8211). Never rebase, never merge again.
MEASURED  by the director at 0789fd376: _pi_transient_re reads pi_transient_signatures from config:workflows through _load_geometry_node, a config node only owner / prime_director may write (goal:g12: the EG.185 kid's write.py set was refused), so test_workflow::test_the_shipped_signature_cell_is_present_and_matches_empty_response is RED on the tip. thought-master put the five signatures where the retry policy already lives: values.pi_retry.transient_signatures, read the way _pi_retry_policy reads values.pi_retry.
1. THE READER -- _pi_transient_re compiles values.pi_retry.transient_signatures read through _loc.load_config, the same reader path _pi_retry_policy uses; config:workflows is no longer consulted.
2. THE GUARD -- keep the no-fallback rule and its ONE stderr line, now naming values.pi_retry.transient_signatures.
3. THE TEST -- re-pin test_the_shipped_signature_cell_* (and any test naming config:workflows pi_transient_signatures) to the config.json cell; paste the orders' TESTS red on 0789fd376 and green on your tip.
4. THE GEOMETRY KEY -- drop the pi_transient_signatures key from _load_geometry_node's return.
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in · ANCHOR RULE: a cite names a function / heading / cell key and adds a line number only where the claim IS the line
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
TESTS     env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/<dir> extensions/agi/tests/test_workflow.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_bin_help_smoke.py (timeout 900) -- paste the summary line; help_smoke[zoom.py] ERRORS on the cut already (pre-existing, not yours)
FILE SCOPE extensions/agi/bin/workflow.py (_pi_transient_re, its guard line, _load_geometry_node's return) · extensions/agi/tests/test_workflow.py · hypothesis:a-workflow-pi-stage-retries-an-empty-provider-response-from-one-signature-cell (write.py) · the kid's own node · NEVER .agi/config.json (the cell is thought-master's, already on the cut)
CEILING   HARD CAP: 1 kid · <= 10 production lines net over 27beb2eb0 · <= 20 test lines net over 27beb2eb0 · pi-free tier-0 · 0 USD -- measure git diff --numstat 27beb2eb0 <tip before the paste commit>, labelled so
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13) · WRITE THE NODE EARLY and commit after every run


## CORRECTIVE DH.EG.205 -- closes mur-eg-x313175-a5d950 EG.185-k1 demote + EG.188-k1 accept_with_residue (the whole EG.185 chain: c2404cc17..3ec61d27e)
BASE      CUT FROM season2/loops/hypothesis-a-workflow-pi-stage-r-a00-62aba04c tip 3ec61d27e (branch de-base-EG.205 = the EG.188 tip; the chain merges clean onto the trunk a3065abc4: git merge-tree rc 0). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. THE CLAIM TEXT (murq288 EG.185-k1 V6 + EG.188-k1 R1 R2): the hypothesis title, testable_claim, claim and falsifier 3 still name config:workflows pi_transient_signatures and 'the same list as its code fallback' -- both are gone by order (TMM.361: the cell is values.pi_retry.transient_signatures in .agi/config.json; no code fallback, ONE loud stderr line). Rewrite them through write.py to what the bytes do; the title is edited in frontmatter via write.py set, the mint id never changes.
2. ONE ROOT (EG.185-k1 V4 + EG.188-k1 R3): workflow.py reads the retry NUMBERS through pi_trajectory._retry_cells (root = cwd) but the SIGNATURES from run_args project_root -- a run launched from another cwd reads two different configs. Make both read the SAME root (the stage's project_root), in the smallest change: pass the root through, or have _pi_retry_policy take the start it is given. A test: a tmp project root whose config differs from the cwd's -> both values come from the project root.
3. THE PRIME COMMAND (EG.185-k1 V3): experiment:a00-be655ee1-a37a78 prints a command that would create a SECOND copy of the signature list -- replace it with the one-line pointer to values.pi_retry.transient_signatures (the cell exists on the trunk, ee40e8211).
4. A VACUOUS GUARD TEST (EG.185-k1 M1 + EG.188-k1 M3): test_the_shipped_cell_guard_bites_when_the_key_is_dropped re-implements the guard's assert inline -- make it CALL the shipped guard (the same function/assert the shipped-cell test uses) on a fixture tree without the key, and show it fails there.
5. THE SLEEP SEAM (EG.185-k1 M3): the stage retry now sleeps the REAL cell value (60 s) and _RETRY_SLEEP is patched only inside test_workflow.py -- run `git grep -n _pi_retry_policy -- extensions/agi` and every test module that can reach a transient stage retry; any that can must patch the sleep or pin a tiny policy. Paste the grep and name each module checked.
6. A BAD FRAGMENT CRASHES (murq274 mur-eg-x4060725-17afb3 EG.183-k1 V5, still true at 3ec61d27e): _pi_transient_re compiles the cell's fragments with no guard -- one malformed regex in values.pi_retry.transient_signatures raises re.error inside a live stage. Catch it: the bad fragment is skipped (or the whole cell treated as unreadable) with the SAME one loud stderr line naming the cell; a test with a malformed fragment.
7. EG.183's CEILING BREACH (murq274 V8 V9: 27 net production vs 15, 69 net test vs 50) = a RECORDED residue (TMM.315): state it once on the hypothesis node with the measured numstat fffe01959..2d0b3c8ed and why, if not already recorded (paste the grep that shows whether it is).
DEMOTED   by the director at triage (murq288 + murq274 EG.183-k1: V1 V2 V3 V6 V10 V11 closed down the chain -- the cell exists, no second list, the shipped-cell guard, the loud line, the title = item 1; V4 = item 2): EG.185-k1 V1 V2 + M4 = CLOSED by EG.188 (the reader lands; the shipped-cell test FAILS at 27beb2eb0 and PASSES at 3ec61d27e, EG.188-k1 M4; the stale comment was deleted in its diff) · V5 (empty_response_* cells govern every transient stage) = BY DESIGN, TMM.360 item 3: ONE retry policy · M2 (a green test pins 'absent cell => never retried') = BY DESIGN, EG.188's loud no-fallback guard · M5 (merge-state) = REFUTED: git merge-tree --write-tree 3ec61d27e local-maxxing/season2/main (a3065abc4) exits 0
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANCHOR    every cite you write or touch names a heading, a function or a cell key; add a line number ONLY where the claim IS that line (TEXT-FIX CHURN: line pointers go stale on the next edit). A pointer you cannot anchor that way, delete it.
NUMSTAT   a commit never pastes a numstat that includes itself: measure <cut>..<the tip BEFORE the paste commit>, labelled so. A write.py range edit keeps every heading it spans (read the range first).
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_workflow.py test_pi_trajectory_retry.py test_live_config_cells.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tests you WRITE use tmp repos only (test_bin_help_smoke.py is the one exempt read-only check: --help over the committed bin); never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/bin/pi_trajectory.py (item 2 only, the root parameter) · extensions/agi/tests/test_workflow.py · test modules item 5 names (sleep patch only) · via write.py: .agi/nodes/hypothesis/a-workflow-pi-stage-retries-an-empty-provider-response-from-one-signature-cell.md · .agi/nodes/experiment/a00-be655ee1-a37a78.md · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 3ec61d27e · <= 40 test lines net over 3ec61d27e · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 3ec61d27e <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.205: mur-eg-x313175-a5d950 EG.185-k1 + EG.188-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
