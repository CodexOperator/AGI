---
id: hypothesis:provisioning-reads-its-cells-through-one-import-route
mint_id: 8b882dbdeccf4602b2ea822c2cd3b489
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: a00-3ba810fd
scaffold_hash: 64e9569c214cb9cf
season: 2
status: open
testable_claim: "provisioning._prov_cell no longer inserts into sys.path per call: len(sys.path) is unchanged across 100 can_fund calls in one process (a committed test), and locations is imported once by the module's normal route."
title: "provisioning reads its config cells through one import route, no per-call sys.path growth (assigned: director-engine)"
town: core
---
# hypothesis:provisioning-reads-its-cells-through-one-import-route

# hypothesis:provisioning-reads-its-cells-through-one-import-route

PASS 11 engine-delta-1 missed 4: provisioning.py:203 `_prov_cell` does sys.path.insert(0, ...) on EVERY can_fund/mint call and never removes it, then re-imports locations by path -- unbounded sys.path growth per process and a second import route.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.673 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: none new (the cells stay where they are) · template-max: none · code: provisioning imports locations once by the module route; _prov_cell (provisioning.py:203) stops inserting into sys.path per call
FALSIFIERS len(sys.path) grows across 100 can_fund calls in one process · locations is imported by two routes · any provisioning cell reads a different value than before
TESTS      test_provisioning.py (the 100-call sys.path test) + test_zero_usd_mint_floor.py test_credential_none_spawn.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never a real mint
FILE SCOPE extensions/agi/bin/provisioning.py · extensions/agi/tests/test_provisioning.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 10 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## STATUS after EG.123 landing (03ab636aa) + EG.156 corrective
STATUS    LANDED at 03ab636aa: experiment:a00-9db7337e-cc325e (both floor readers route through `_prov_cell`, cfg= wins over root; parent-reviewed inconclusive_lean_proved:70). EG.156 (experiment:a00-6678e0d1-53f123) re-cut the docstring prose: 8 net production lines over bb3fd61ed, inside the 15 cap.
ROUNDS    this post's rounds on this node: DH.673 -> EG.123 (landed) -> EG.156 (text-fix corrective, closes mur-eg-59 accept_with_residue).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.156 text-fix kid a00-6678e0d1: the OPEN block said "IN PROGRESS, not landed ... DH.673 QUEUED" on the very tip (03ab636aa) that landed its child experiment:a00-9db7337e-cc325e (mur-eg-59 M4). Replaced with the landed status and the round chain; no claim text changed.
<!-- THOUGHT:END -->

parent review a00-3ba810fd EG.164 of kid a00-34601654 (experiment:a00-34601654-0c56e6), accepted, no demotion. Evidence read from the KID WORKTREE BYTES: provisioning.py byte-identical to this checkout (production delta 0, inside the 15/40 caps); a00-6678e0d1-53f123 frontmatter now carries verdict inconclusive_lean_proved:60, confidence 0.6, evidence_runs [experiment:a00-6678e0d1-53f123] (order item 1 fixed in bytes); its row 2 names the kept KEY-PRESENCE comment at :525-528 and states that EG.164 corrected the :533-536 citation (item 2); a00-9db7337e-cc325e.md:91 Agent Notes now reads 28 added / 12 removed = 16 net at bb3fd61ed, re-cut to 8 net (20/12), 39 test net, and the round node row 1 now says PARTIAL naming the Agent Notes half (item 3, the half-fix). Only surviving "533-536" / "28 production lines net" strings are quotes OF the corrected defect. Probes run by me (sessions/iter-EG.164/a00-3ba810fd/probe_parent_164.py): WIRE 100 live calls moved len(sys.path) by 0; GATE undeclared key floor 1.0, undeclared account floor None, declared 0.0 stays 0.0, cfg= beats root (2.5); AUTH empty provisioning cell -> declared default 1.0, no raise; ROUTE exactly one sys.path.insert at provisioning.py:67, module scope, zero importlib refs. Caveat: the kid pasted no git diff --numstat 0ae4b7171 (deviation, accepted for a record-only round with a provable zero production delta -- a kid with nothing to measure can otherwise satisfy the ceiling clause vacuously). The full review THOUGHT could not be written into the kid node from this checkout (write.py: no node file for experiment:a00-34601654-0c56e6 -- the node lives in the kid worktree branch), so it is recorded here.
