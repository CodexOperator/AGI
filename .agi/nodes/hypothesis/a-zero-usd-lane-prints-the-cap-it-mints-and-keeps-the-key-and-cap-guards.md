---
id: hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards
mint_id: 6bc640058a4d49d5b89998561ea402df
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 99eefc8ec1496ca4
season: 2
testable_claim: "On a zero_usd lane the banner prints the zero_usd_key_limit_usd cap; check_runtime_key_usable and the --cap guard run for every openrouter lane; only the key and account floors are skipped (assigned: director-engine)"
title: A zero-USD lane prints the cap it mints and keeps the runtime-key and cap guards
town: core
---
# hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards

## Measured
TMM.298 (thought-master 13:31Z 09-27, gating 6f9b9a1d9 = trunk 91ae33672), two residues of the zero-USD mint fix:
(1) dispatch.py:2196 prints `credentials: minting per spawn, limit=$<cred_limit>` (1.0) while a zero_usd lane mints a key capped at provisioning.zero_usd_key_limit_usd (0.01; measured: every DH.533-536 key reads limit=0.01).
(2) dispatch.py:2349-2350 -- the outer `if provider == openrouter and zero_usd is not True` skips check_runtime_key_usable AND the --cap guard for zero_usd lanes; only the key floor and the account floor were ordered exempt (TMM.296 point (d)).

## CLAIM
On a zero_usd lane the credentials banner prints the cap actually minted (the zero_usd_key_limit_usd cell); check_runtime_key_usable and the --cap guard run for every openrouter lane; ONLY check_key_floor and check_account_floor are skipped for a zero_usd lane; paid lanes are byte-for-byte unchanged in behaviour.

## Dispatch line
config-max: none new (read provisioning.zero_usd_key_limit_usd, already a cell) / template-max: none / code: the banner's value + the gate split in dispatch.py.

## FALSIFIERS
- a zero_usd dry-run prints limit=$1.0;
- a zero_usd dispatch with a dead runtime key and provisioning ABSENT passes the pre-flight;
- a zero_usd `--cap 0` is not refused;
- a paid-lane test in test_dispatch.py changes outcome.

## TESTS
extensions/agi/tests/test_zero_usd_mint_floor.py (extend: banner value, runtime-key gate, --cap guard on a zero_usd lane) + neighbourhood test_cli.py test_heal_watch.py test_dispatch.py test_bin_help_smoke.py once. timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE. NEVER a real mint: every provisioning call stubbed.

## FILE SCOPE
extensions/agi/bin/dispatch.py (the banner line + the openrouter gate block only) · extensions/agi/tests/test_zero_usd_mint_floor.py · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines net · <= 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut

## CORRECTIVE DH.546 -- closes mur-director-engine-23 DH.537-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-zero-usd-lane-print-a00-6d2a74c4 tip f109db023 (branch de-base-546; the post-branch zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. --cap guard on a zero_usd lane is charged the account floor the lane is exempt from (provisioning.py:632)
2. The cap guard measures a number the zero_usd round provably cannot spend (dispatch.py:2409 prices the pre-override float(args.cap)*slots while :2196 resolved the lane's real cap to 0.01)
3. CI CANNOT SEE defect 1: the new fixture stubs `credit_balance -> None` and `list_all_keys -> []` in _zero_usd_dispatch (test_zero_usd_mint_floor.py), so cap_headroom always takes its fail-open 'no readable balance' path in all three new tests — the zero_usd-lane headroom path has no committed test at all, which is exactly why the near-miss survived three falsifier runs.
4. Third new test does not discriminate: against the pre-image dispatch.py the run was 2 failed / 6 passed, i.e. test_zero_usd_lane_skips_the_two_dollar_floors passes on BOTH images (the pre-image skips strictly more), so it carries no falsifying power on its own; only the banner and gate tests bind.
5. Falsifier 'provisioning ABSENT' is not exercised: _zero_usd_dispatch stubs prov.available -> True (provisioning LIVE) and replaces check_runtime_key_usable wholesale, so the test proves the call RUNS and its return is honoured, not that the real function refuses a 401 under provisioning-absent (provisioning.py:_verify_provider_key path). UNVERIFIED; the probe I would run is a variant of the committed helper with available -> False and the real check_runtime_key_usable, asserting exit 1 on a 401 runtime key — not run here.
6. Side effect not in the node's accounting: check_runtime_key_usable now runs for zero_usd lanes (dispatch.py:2363, outside the zero_usd wrapper), so with provisioning ABSENT a zero_usd dispatch makes a live provider auth call it never made before (provisioning.py:_read_runtime_key/_verify_provider_key). Dormant while provisioning is live; noted, not a demote.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_zero_usd_mint_floor.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py · extensions/agi/tests/test_zero_usd_mint_floor.py · .agi/nodes/experiment/a00-0d042bef-242bdd.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over f109db023 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.546: mur-director-engine-23 DH.537-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
