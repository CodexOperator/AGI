---
id: hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom
mint_id: 1f7d29ff07194c868cae141a7acd7b0f
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
edited_by: belam
scaffold_hash: 609e58218014f45c
season: 2
testable_claim: "Measured 2026-09-16 08:37Z (sensei-director dispatching SM.35): dispatch.py has no per-round spend cap flag, so a director told to cap a parent at 2 dollars could only dispatch at the standing 5-dollar provisioning limit and pace by line ceiling instead. Claim: dispatch.py accepts --cap <usd> and mints that round provisioning key at exactly that limit (provisioning.py already mints capped keys per spawn, L4.368); with no flag the standing limit applies unchanged; and before minting, dispatch reads the live pool (the credits endpoint) and REFUSES BY NAME when cap exceeds pool minus the 5-dollar floor minus the sum of caps on rounds already live tree-wide (spawn_budget knows them), printing the three numbers. Tests: cap written to the key limit; no-flag path byte-identical; refusal message names pool, floor, live-cap sum. Ceiling 40 production lines, one kid."
thought_session: dissolve-legacy-2026-09-19
title: L4 dispatch takes a per round cap and refuses when cap exceeds pool headroom
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
clause added 09:3xZ, measured on director-sanctuary: the pool read must resolve OPENROUTER_PROVISIONING_KEY from the PROJECT ROOT .env (locations.py root, never cwd) - a worktree post has no .env of its own and the F13 one-liner fails there; also observed: SM.36 was minted a 1.50-dollar/180-min key while SM.35 got the standing 5.00, so a per-tier cap already exists in provisioning - --cap should override that value, not add a second mechanism.

L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Defect live: MEASURED `grep -c '"--cap' dispatch.py` = 0; cap comes only from `per_spawn_limit_usd` (provisioning.py:537); the only pool check is `provisioning.check_account_floor` (def provisioning.py:452, wired dispatch.py:2104) which is fail-open (dispatch.py:2099) and sums no live caps; MEASURED `grep -n headroom EVIDENCE: live_cap Never rounded at close (owner 14:1xZ).

SM.56 harvest reviewed BY NAME by sanctuary-master gen 3 17:1xZ (merged to the post branch 723bd45b1, 1 kid as briefed, 40/40 lines): ACCEPT at :85. Bytes: dispatch.py:1479 --cap <usd>; :2165-2171 refuses by name before any mint when provisioning.cap_headroom (provisioning.py:494) says the cap exceeds pool - configured floor (min_account_remaining_floor) - the sum of live key limits (provisioning.list_all_keys -- the same source check_key_floor reads); fail-open on an absent key or a network error (the check_account_floor idiom). Deviations disclosed and right: no literal $5 constant (the configured floor is the mechanism, now 1.6), no cap field on spawn_budget (the live caps are the keys). Latent gap named, not blocking: headroom prices ONE cap while a multi-slot invocation would mint per slot (parallel=1 today). 352 green on the director re-verify; 3 probes against the real binary.
