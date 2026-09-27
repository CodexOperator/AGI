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

## CORRECTIVE DH.565 -- closes mur-director-engine-25 DH.546-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-zero-usd-lane-print-a00-d470d22c tip 87995d360 (branch de-base-565; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. CEILING BREACH, exact: provisioning.py 13/2 + dispatch.py 10/1 = 20 net / 23 added production lines against the hypothesis node's own 'CEILING: HARD CAP: 1 kid, <= 15 production lines net ... a byte or kid over it = the round is cut'. The node's Evidence 4 numstat block counts dispatch.py alone ('10 net production (ceiling 15)'). The parent's D1 said 10+15=25; the true figures are 20 net / 23 added - same conclusion, wrong arithmetic. Procedural, not a mechanism defect.
2. SCOPE: extensions/agi/bin/provisioning.py is outside the round's granted FILE SCOPE. The hypothesis node declares 'FILE SCOPE: extensions/agi/bin/dispatch.py (the banner line + the openrouter gate block only) - extensions/agi/tests/test_zero_usd_mint_floor.py - the kid's own node'. The stage task's file list is the REVIEW scope (derived from the diff), not the round's grant.
3. VACUITY FALSIFIER UNPINNED IN CI: no committed test asserts the --cap guard RUNS on a zero_usd lane. test_zero_usd_mint_floor.py:194-206 asserts only code==0 and [m['limit_usd']]==[0.01]; both hold identically if provisioning.cap_headroom is never called, because provisioning.mint forces the cap on its own. The only call site is dispatch.py:2398-2419, which sits OUTSIDE the 'if dispatch_harness.get("zero_usd") is not True:' skip at dispatch.py:2372; de-indenting it into that branch leaves all 10 tests green while items 1 and 2 are silently reopened - precisely the near-miss the parent THOUGHT names, which only an uncommitted probe caught. Probe I WOULD run (not run): the parent's probeA as a committed test - a live sibling agi- key at limit 5.0 / usage 4.0 with --cap 1.00 on a zero_usd lane must exit 1 naming live headroom. Note the paid lane has that refusal half pinned (test_provisioning.py:1759); the zero_usd lane does not.
4. DOCSTRING CLAIM ABOUT A READER NEVER READ: provisioning.py:620-621 states 'The floor term is then 0.0 and the refusal NAMES that, so a zero-USD lane is visibly priced without it.' The refusal at provisioning.py:651 formats the exempted floor as 'floor $0.00' with no exemption marker - byte-identical to a project that never declared min_account_remaining_usd (cf. test_provisioning.py:1861 test_cap_headroom_with_no_declared_floor_treats_it_as_zero). No reader can distinguish an exempt lane from a floorless pool. Wording by the review rules, but it is the sentence the round's own findings row 1 directs the next guard author to rely on.
5. FALSE PROVENANCE STILL LIVE IN THE BODY (parent's D2, unfixed at the surface a reader lands on): a00-80f7b775 'The two-line production change' and findings row 1 still assert '`exempt_floor` ALREADY existed in provisioning.cap_headroom (provisioning.py:602,643) with a docstring naming this exact hole - it had NO caller'. Refuted by the base commit: f109db023:extensions/agi/bin/provisioning.py:600-601 signature is cap_headroom(cfg, root, cap, slots=1) and :632 reads 'floor = min_account_remaining_floor(cfg) or 0.0'. The THOUGHT block names the falsehood but the BODY a later reader opens still carries it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_zero_usd_mint_floor.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py · extensions/agi/bin/provisioning.py · extensions/agi/tests/test_zero_usd_mint_floor.py · .agi/nodes/experiment/a00-3d7187fc-43d084.md · .agi/nodes/experiment/a00-80f7b775-77837d.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 87995d360 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.572 -- belam [decision] 15:38Z on the zero-usd chain (after DH.565)
BASE      CUT FROM season2/loops/hypothesis-a-zero-usd-lane-print-a00-6020c43a tip 287379efa (branch de-base-572). No merge. Never rebase.
MEASURED  (belam, probed) at 0.606 USD balance OpenRouter mints a key with limit 0.01 and a PAID model is ALSO served through it: the key cap BOUNDS a leak at 0.01 USD per key, it never refuses one. So the sizing invariant is key cap x live spawns < account balance (0.01 x spawn.max_live 30 = 0.30 < 0.606 today; a paid-cap key or a larger max_live breaks it).
1. SIZING GUARD: before a zero-USD-lane mint, provisioning refuses BY NAME when provisioning.zero_usd_key_limit_usd x spawn.max_live (both config cells, read, never literals) >= the live account balance it already reads; the refusal line names all three numbers. A committed test pins refuse and admit on fixture numbers (no real mint, no network: monkeypatch the balance read).
2. PAID LADDER ROW: config:ladder (.agi/nodes/.geometry/ladder.md) row {tier 0, role director} is harness pi + ~z-ai/glm-flash-latest (PAID). Set it to the tier-0 parent row's lane (harness pi-free, model stealth/space-bunny-alpha) with write.py; a committed test asserts every tier-0 row resolves a 0-USD harness.
3. On your node paste: the refusal line from the test, and `python3 extensions/agi/bin/write.py config:ladder 'read frontmatter'` lines for the tier-0 rows after the edit.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; never a key id, never print a key; patterns write <user>
TESTS     test_zero_usd_mint_floor.py test_ladder_node.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/provisioning.py · extensions/agi/tests/test_zero_usd_mint_floor.py · extensions/agi/tests/test_ladder_node.py · .agi/nodes/.geometry/ladder.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = item 1, k2 = item 2) · <= 15 production lines net over 287379efa · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13); a stale .git index.lock with no holder refuses every commit -- name it, never force past it

## CORRECTIVE DH.608 -- closes mur-director-engine-31 DH.572-k1 demote (no verify)
BASE      CUT FROM season2/loops/hypothesis-a-zero-usd-lane-print-a00-14bec45e tip 81eb9fcda (branch de-base-608; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. FIRST: revert every config:ladder edit beyond the tier-0 director row (review demote: .geometry/ladder.md:37 restored a value commit 20283d21b dropped) -- the stale test that wanted it is fixed or named OUTSIDE, never greened by a cell.
1. Out-of-scope cell restores a value commit 20283d21b deliberately dropped, solely to green a stale test -- .agi/nodes/.geometry/ladder.md:37 -- The same logged write puts `settings: "ultracode"` BACK on the tier-3 prime_director row. Commit 20283d21b (belam, 2026-09-27 01:25Z, message verbatim 'ultracode dropped from the config:ladder tier-3 rows') removed it from BOTH tier-3 rows. The value reaches a real launch flag (dispatch.py:2093-2094 `_spec["settings"] -> dispatch_harness["settings"]`), so this changes how the PRIME itself starts, under an orders condition that said 'CHANGES NO PAID/ZERO-USD LANE'. Measured at base: test_ladder_node.py:70 `assert prime.get("settings") == "ultracode"` is the ONLY red assertion (1 failed, 5 passed). The artifact was mutated to satisfy the test; the test was the stale side. Correct repair: assert `== ""` at test_ladder_node.py:70 and drop the ladder cell.
2. Ordered ceiling breached and the round was landed, not cut (DH.565 residue class, unfixed) -- extensions/agi/bin/provisioning.py:222 -- Orders quoted in the node THOUGHT: 'HARD CAP: 2 kids - <= 15 production lines net - <= 40 test lines - a byte or kid over it = the round is cut'. Measured `git diff 287379efa 81eb9fcda --numstat`: provisioning.py +39/-6 = 33 net production (2.2x the cap) and test_zero_usd_mint_floor.py +48 (1.2x). The remedy applied was a verdict demotion (k1 -> inconclusive_lean_proved:65), not the cut the orders named. The round was merged with the breach unfixed.
3. File-scope breach: 100% of the round's production bytes are outside the declared scope (DH.565 second residue, unfixed) -- .agi/nodes/hypothesis/a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards.md:1 -- The hypothesis FILE SCOPE names `extensions/agi/bin/dispatch.py` (banner line + openrouter gate block only), test_zero_usd_mint_floor.py, and the kid's own node. The round's entire production change is in provisioning.py, and its second item is a .geometry/ladder.md write - neither is in scope, and dispatch.py is untouched. The belam decision that redirected the round was never recorded as a deviation in the hypothesis THOUGHT.
4. The hypothesis carries no verdict while its two children carry verdicts against a claim neither of them tests -- .agi/nodes/hypothesis/a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards.md:1 -- hypothesis:a-zero-usd-lane-... has no `verdict` field. Its children k1 (provisioning sizing guard) and k2 (tier-0 ladder row) are parented to it but test belam's two decision items, not the banner/gate claim - which was already satisfied at base by 6f9b9a1d9 and is untested by this round. A harvest reading DH.572 will credit two kids with one claim they never touched. Fix: verdict the hypothesis against dispatch.py:2195/2358/2372/2399, and re-parent or open a hypothesis for the sizing guard and the ladder row.
5. A bodyless probe scaffold was committed as one of the round's three experiment nodes -- .agi/nodes/experiment/a00-5a83d3ce-6679dc.md:1 -- Empty `## Experiment` / `## Evidence` template, no verdict, no evidence_runs, no status. It is the parent's own p4 wire-probe stray (named in a00-c873d4ef's THOUGHT item 4), landed by the director's 81eb9fcda. It reads as a real experiment of the round and has no marker saying it is a probe artefact.
6. Half of the probe pair demoted by engine side-effect and left untracked, with no write-log row -- .agi/nodes/deprecated/experiment/a00-3a7af8ee-82df1c.md:1 -- `git cat-file -e 81eb9fcda:.agi/nodes/deprecated/experiment/a00-3a7af8ee-82df1c.md` -> absent from the branch; it exists only untracked in the parent worktree, under deprecated/, with no write-log row. Answering the Prime's question: the round did NOT mean to deprecate anything as work product - the deprecation is a by-product of the parent's own p4 probe (a00-c873d4ef THOUGHT section 4), and its sibling was committed. So this is a demotion-shaped move with no recorded writer, and the pair is split across the branch boundary. Retire-and-register it with a logged write, or accept the asymmetry explicitly in the round's node.
7. New tier-0 test has no non-empty floor: an empty roles table passes with zero assertions -- extensions/agi/tests/test_ladder_node.py:84 -- `for row in [r for r in roles if r.get("tier") == 0]:` with the assert inside and nothing asserting the list is non-empty. The parent named this (probeP2) and it is unfixed. One line: assert the tier-0 list is non-empty before the loop. Also no blank line between this def and the next (E302).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_ladder_node.py test_zero_usd_mint_floor.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/provisioning.py · extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_zero_usd_mint_floor.py · .agi/nodes/.geometry/ladder.md · .agi/nodes/experiment/a00-5a83d3ce-6679dc.md · .agi/nodes/experiment/a00-6de33435-a37a02.md · .agi/nodes/experiment/a00-c873d4ef-f31742.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 81eb9fcda · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.638 -- closes mur-director-engine-35 DH.608-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-a-zero-usd-lane-print-a00-22577533 tip b239d47a1 (branch de-base-638; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
NOTE      item 1's missing cell = DH.608's ordered ladder revert (config:ladder prime_director settings ultracode -> ""), left UNCOMMITTED and unlogged in worktree .agi/worktrees/a00-22577533 (READ ONLY: git -C .agi/worktrees/a00-22577533 diff -- .agi/nodes/.geometry/ladder.md). Re-apply it THROUGH write.py config:ladder on this branch and commit. The stray root file `the` is REMOVED by the parent (git rm -q the; commit by that path only).
1. The round's own test file is RED at the merge tip: the assertion needs the ladder cell, the diff does not carry it -- extensions/agi/tests/test_ladder_node.py:76 -- assert prime.get("settings", "") == "" but git show b239d47a1:.agi/nodes/.geometry/ladder.md:37 reads "settings": \"ultracode\" (restored by the BASE commit 81eb9fcda) -> test_ladder_node_declares_roles_table fails 1/7; the paired config half exists only as an uncommitted parent-worktree edit (TMM.268 class the round exists to close).
2. Proved node's Evidence quotes a production change the range does not contain -- .agi/nodes/experiment/a00-6273b184-c9048b.md:60 -- The PRODUCTION LINES block cites `git diff --numstat` = `1 1 .agi/nodes/.geometry/ladder.md` and frontmatter production_lines: 1; the range's diffstat has no ladder.md line and the cell reads ultracode at BOTH tips - a byte-claim about a reader never read at the tip.
3. Proved node's test count does not reproduce at the reviewed tip -- .agi/nodes/experiment/a00-6273b184-c9048b.md:50 -- Evidence claims `93 passed, 7 skipped in 132.47s`; measured at b239d47a1: 1 failed, 92 passed, 7 skipped - the self-cited evidence run of a verdict=proved node does not reproduce on the merged bytes.
4. Decisive probe evidence is prose only - no probes: field, no retained artefacts -- .agi/nodes/experiment/a00-6273b184-c9048b.md:30 -- M1/M2/M4 (red) and M3 (vacuous) are the load-bearing evidence for verdict=proved, but they live in body prose with no frontmatter `probes:` entry (493/1966 experiment nodes carry one) and the /tmp mutation copies are gone, so the claim is UNVERIFIED at merge.
5. Committed stray artefact at the repo root, outside the declared file scope -- the:0 -- Empty 0-byte file `the` added by 2c860be9b inside this range; junk in the tree, not a node, not in FILE SCOPE.
6. Item 6 unresolved: a demotion-shaped node file still untracked and outside the graph -- .agi/nodes/deprecated/experiment/a00-3a7af8ee-82df1c.md:0 -- Absent from the tip (git ls-tree -r b239d47a1 -> 0 hits, no history); write.py edits but does not create, so the file cannot be settled by the round - a Prime/director call, named in the node.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_ladder_node.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_ladder_node.py · the · .agi/nodes/.geometry/ladder.md · .agi/nodes/experiment/a00-5a83d3ce-6679dc.md · .agi/nodes/experiment/a00-6273b184-c9048b.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over b239d47a1 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.638: mur-director-engine-35 DH.608-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
