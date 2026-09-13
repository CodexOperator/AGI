---
id: hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes
mint_id: c15c7f0828f44adaa720dfd6fa6391aa
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 027240ffb3272e62
season: 2
testable_claim: "goal:g15.25 SM.19 (OWNER ORDER 09:2xZ via belam XIX, verbatim in doc:l4-owner-decisions tail; config provisioning.min_account_remaining_usd = 5.0 landed 310a5591f; account $24.14 at 09:24Z, ~$1-2/h — land before the floor). MEASURED on season2/main @5f8a00145: dispatch.py:1797-1804 runs provisioning.check_key_floor then check_account_floor (provisioning.py:420) for EVERY tier before the target loop — a kid of a round admitted at $5.50 is refused when its parent reaches its first kid at $4.90, killing the round mid-flight; a kid names its parent by AGI_AGENT_ID (:2247 spawned_by_agent) and the iter manifest (_merge_manifest :655) carries the parent record with its pid; spawn_budget._pid_alive :226 exists. CLAIM: (1) in dispatch, when args.tier == kid AND the manifest of the current iter holds a record whose agent id == os.environ AGI_AGENT_ID (the calling parent) AND spawn_budget._pid_alive(that record pid): SKIP check_account_floor ONLY (print one line `account floor: exempt — kid of admitted live round <parent id> pid <n>`); check_key_floor runs as today; (2) every other case (tier parent, kid with no manifest parent, parent pid dead) -> check_account_floor as today, refusal naming the floor and the balance; (3) --dry-run prints the exemption decision; (4) the exemption is recorded on the kid manifest record (`account_floor: exempt-live-round`). FALSIFIERS: a parent spawn admitted below the floor; a kid admitted whose parent pid is dead; the key floor skipped; a kid admitted with no manifest parent. TESTS (test_dispatch.py <= 4, monkeypatched check_account_floor -> (False, floor msg) + a fixture manifest + monkeypatched _pid_alive): below floor + live parent -> kid admitted, one exempt line; no parent record -> refused with the floor named; parent pid dead -> refused; tier parent -> refused. FILE SCOPE: dispatch.py (the :1801 block + one helper), test_dispatch.py. CEILING: <= 30 lines net, <= 4 tests. ORDER: FIRST — before every queued SM.* round (the floor is hours away)."
title: "a --tier kid spawn whose parent is in the iter manifest with a live pid is exempt from the ACCOUNT floor (the key floor still applies), so a round admitted above the $5 floor completes instead of dying at its first kid; a parent spawn below the floor stays refused with the floor named (OWNER ORDER 09:2xZ: floor $5.00, live rounds finish, no fallback, PAUSED until resumed)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
