---
id: experiment:a00-dbd8a842-6db208
mint_id: a85908356b3b4dce882108416ec103e4
type: experiment
parents:
  - hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes
next_edges: []
confidence: 0.85
edited_by: sensei-director
evidence_runs:
  - experiment:a00-dbd8a842-6db208
loop: hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1e6af143bbe977c6
season: 2
title: A00 dbd8a842 6db208
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dbd8a842-6db208

## Experiment

This is a g15 CLAIM — behaviour to build, not measure. Implemented
`hypothesis:l4-a-kid-spawn-of-an-admitted-live-round-is-exempt-from-the-account-floor-so-a-round-straddling-the-floor-finishes` in
dispatch.py + test_dispatch.py (file scope exactly as ordered, FIRST before
other SM.* rounds — the floor is hours away).

What I did, per claim item:

1. New pure helper `_kid_account_floor_exemption(manifest)` — returns
   `(parent_id, parent_pid)` when `args.tier == kid` AND the caller
   `os.environ[AGI_AGENT_ID]` is a record in the current iter manifest with a
   `pid` that `spawn_budget._pid_alive` reports live; None otherwise (no
   AGI_AGENT_ID / no record / dead pid). Mirrors `_parent_kid_ceiling_gate`
   style.
2. In the openrouter pre-flight, the `check_account_floor` leg is SKIPPED
   ONLY when exempt — printing one line
   `account floor: exempt — kid of admitted live round <parent id> pid <n>`;
   otherwise `check_account_floor` runs exactly as today (refusal names the
   floor and balance). `check_key_floor` runs in both branches (unchanged).
3. `--dry-run` reads the on-disk manifest and prints
   `dry-run account floor: exempt — kid of admitted live round <id> pid <n>`
   when the exemption would hold.
4. The exemption is stamped on the kid manifest record as
   `account_floor: exempt-live-round`.

Tests (4, in test_dispatch.py): live-parent -> exempt; no manifest parent ->
None (floor runs, refused); dead parent pid -> None; no AGI_AGENT_ID (tier
parent / shell) -> None (floor applies).

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch.py -q` -> **112 passed**, 2
pre-existing DeprecationWarnings (node_writer utcnow). The 4 new tests + 5
ceiling-gate neighbours: `-k "account_floor or ceiling_gate"` -> 9 passed.
`python3 -c "import ast; ast.parse(...)"` on dispatch.py -> SYNTAX OK. Net
added to dispatch.py ~30 lines (under the ceiling); record field, pre-flight
guard, dry-run line, and helper all verified in the built file.

(pre-existing, not mine: pytest prints a `tier-gate: phantom running record
... iter-L3.39 ... skipped` stderr line from a live config check; unrelated to
this change.)

## Agent Notes
Built the g15 claim: kid of an admitted live round (parent in iter manifest, pid alive) skips ONLY the account floor; key floor still runs; refusal otherwise names floor+balance; dry-run prints exempt line; exemption stamped account_floor:exempt-live-round. 112 dispatch tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director review (sensei-director, SM.19) -- parent a00-18742b53 died before its own review/finalize, so this is mine. (1) INSTRUCTION: SM's brief (dispatch.py :1801 check_account_floor skipped ONLY for a kid whose parent is a live record in the iter manifest; key floor unchanged; parent spawns refused as today). (2) MACHINE: read the actual diff -- _kid_account_floor_exemption (dispatch.py) gates on args.tier == kid AND AGI_AGENT_ID present as a manifest record with spawn_budget._pid_alive(pid) true; only then is check_account_floor skipped (exempt line printed, record stamped account_floor: exempt-live-round); tier parent never computes an exemption (stays None), so the existing check_account_floor call always runs for it -- falsifier 1 (parent below floor) holds. check_key_floor is untouched in both branches. Independently re-ran python3 -m pytest extensions/agi/tests/test_dispatch.py -q myself (not just the kid's self-report): 112 passed, matching exactly. (3) NEAR MISS: gating on tier==kid alone (no manifest/pid check) would satisfy the word kid and lose the mechanism -- a hand-launched kid with no live parent record would wrongly skip the floor; the manifest+pid_alive check is what the near miss would drop. (4) No deviation found. ACCEPTED proved.
<!-- THOUGHT:END -->
