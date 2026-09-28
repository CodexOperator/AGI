---
id: hypothesis:dispatch-credential-banner-states-the-real-key-cap
mint_id: c09dc0d1f1ed4b3c8b8c18b1f8e72b67
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 1f031b1041e62229
season: 2
status: open
testable_claim: On a zero_usd lane the dispatch banner prints the zero_usd_key_limit the key is minted with (0.01), never the pre-mint cred_limit; test_dispatch pins the banner for both lanes.
title: "The dispatch credential banner states the key cap actually minted (assigned: director-engine)"
town: core
---
# hypothesis:dispatch-credential-banner-states-the-real-key-cap

# hypothesis:dispatch-credential-banner-states-the-real-key-cap

PASS 11 engine-delta-1 missed 3: dispatch.py:2196 prints 'credentials: minting per spawn, limit=$cred_limit' from the PRE-mint value while provisioning.py:873-874 overrides limit_usd to zero_usd_key_limit on a free lane -- the banner reports $1.5 (or --cap) for a key capped at $0.01.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.672 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: the banner reads the provisioning.zero_usd_key_limit cell the mint uses, never a literal 0.01 · template-max: the banner text, if a template carries it · code: the banner takes the post-override limit
FALSIFIERS on a zero-usd lane the banner prints cred_limit or --cap instead of the minted limit · on a paid lane the banner changes
TESTS      test_dispatch.py (pin the banner for both lanes) + test_provisioning.py test_zero_usd_mint_floor.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never a real mint
FILE SCOPE extensions/agi/bin/dispatch.py (the banner at :2196 only) · extensions/agi/tests/test_dispatch.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 8 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.672 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.672; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE DH.EG.75 -- closes mur-eg-20 DH.672 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-dispatch-credential-b-a00-7812f7dc tip eadaf5c19 (branch de-base-EG.75; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. --cap on a zero_usd lane is not pinned by a committed test (test_dispatch.py:2962); the brief's 'or --cap' falsifier is settled only by the branch shape at dispatch.py:2201-2203 -> FIX: ONE committed test in extensions/agi/tests/test_dispatch.py that dispatches a zero_usd lane WITH --cap and asserts the banner states the cap the key was actually minted with.
2. The dispatch-level harness structurally cannot tie the banner to the key: _run_cap_dispatch stubs provisioning.mint (extensions/agi/tests/test_dispatch.py:2886-2887, _Minted(kw['limit_usd']) returns the PRE-override cred_limit), so inside that harness a zero_usd lane's spawn line (extensions/agi/bin/dispatch.py:3095) would print cap=$1.5 while the banner prints limit=$0.02 — the two-line disagreement the round exists to kill is invisible to the committed dispatch test. It is closed in a second layer by the real-mint test at extensions/agi/tests/test_zero_usd_mint_floor.py:53-65, so this is a residue note (the two-layer chain is the honest shape of the evidence), not a defect of the diff. -> FIX: in that test the provisioning.mint stub must record the limit it is CALLED with (not echo the pre-override cred_limit), so the banner-vs-key tie is observable; show the test FAILS when the banner reads the pre-override value (paste the red run, then the green one).
3. DEMOTED by the director (not yours): test_pre_fix_reaper_blinds_a_stream_error_with_turn_end -- the director's run at eadaf5c19 (env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT, TMPDIR + --basetemp under /dev/shm) = test_dispatch.py + test_cli.py + test_heal_watch.py 284 passed. If YOUR run of test_dispatch.py shows it red, paste the run with its env and name it OUTSIDE; never edit that test.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_dispatch.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_dispatch.py · .agi/nodes/experiment/a00-b976c566-4bd35a.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines net over eadaf5c19 · <= 40 test lines net over eadaf5c19 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat eadaf5c19 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.105 -- closes mur-eg-28 EG.75-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-dispatch-credential-b-a00-5648df84 tip 4eac264f4 (branch de-base-EG.105; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. Hypothesis left status: open with no verdict after its falsifier landed (hypothesis:11)
2. 5. mint_calls no longer records the zero_usd flag (test_dispatch.py:2895)
3. Sharper than defect 2: the hypothesis node's merge-up STATUS block is affirmatively false, not merely unfinished — .agi/nodes/hypothesis/dispatch-credential-banner-states-the-real-key-cap.md:35-37 still reads 'STATUS IN PROGRESS, not landed: DH.672 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -', while git merge-base --is-ancestor 6f9b9a1d9 eadaf5c19 is true and the child node is verdict=proved. The graph's memory currently asserts the opposite of the landed bytes.
5. UNVERIFIED, disclosed not re-run: the four ad-hoc probes in the PARENT REVIEW (node:71) are parent-run numbers with no committed bytes behind them, and the GATE probe's stated expectation (a zero_usd lane REFUSING an over-headroom --cap) does not hold by design — dispatch.py:2357-2359 skips the whole pre-flight for zero_usd, commented at :2354-2356. The probe I would run to settle it without dispatch.main is a read of that guard plus `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k headroom` (committed, fixture-only); I ran the latter as part of the full file and it is green, so the claim stands on the committed suite, not on the paste.
DIRECTOR: the hypothesis node (V2 + the false STATUS block at :35-37) is IN FILE SCOPE this round: set its status/verdict and rewrite the STATUS block to the landed truth (git merge-base --is-ancestor 6f9b9a1d9 eadaf5c19 = true; child a00-37e03333 = proved) per .agi/context/schemas/[hypothesis].md, with write.py -- read the schema first.
DIRECTOR (numstat self-reference): measure `git diff --numstat 4eac264f4 <tip BEFORE your paste commit>`, paste it, label it so.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_dispatch.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_dispatch.py · .agi/nodes/experiment/a00-37e03333-50d38e.md · .agi/nodes/hypothesis/dispatch-credential-banner-states-the-real-key-cap.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 0 production lines net over 4eac264f4 (test + node text only) · <= 40 test lines net over 4eac264f4 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 4eac264f4 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.105: mur-eg-28 EG.75-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
