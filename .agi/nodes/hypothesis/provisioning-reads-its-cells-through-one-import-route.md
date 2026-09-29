---
id: hypothesis:provisioning-reads-its-cells-through-one-import-route
mint_id: 8b882dbdeccf4602b2ea822c2cd3b489
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: a00-4453045a
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

## STATUS — the STATUS block below is the state; the heading names no round, so a later ROUNDS entry can never outrun it again
STATUS    LANDED at 03ab636aa: experiment:a00-9db7337e-cc325e (both floor readers route through `_prov_cell`, cfg= wins over root; parent-reviewed inconclusive_lean_proved:70). EG.156 (experiment:a00-6678e0d1-53f123) re-cut the docstring prose: 8 net production lines over bb3fd61ed, inside the 15 cap.
ROUNDS    this post's rounds on this node: DH.673 -> EG.123 (landed) -> EG.156 (text-fix corrective, closes mur-eg-59 accept_with_residue) -> EG.164 (record-fix, kid a00-34601654; accepted on a DISCARDED worktree) -> EG.193 (record-fix, kid a00-ff2a5bfc: the EG.164 claims re-grounded in the merged bytes, the review paragraph moved INSIDE the THOUGHT block) -> EG.206 (record-fix, kid a00-4453045a: the demotion of a00-34601654 that EG.193 CLAIMED was never written — the node still read proved / 0.85 in the merged tree; it lands HERE as inconclusive_lean_proved:40 / 0.4, and the false "demoted at EG.193" clause is deleted from this line). The mechanism claim under STATUS is unchanged and still probe-grounded; every item this round fixed was a record defect, not a code one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.193 record-fix (kid a00-ff2a5bfc) CORRECTS the EG.164 parent review by a00-3ba810fd, which cited "the KID WORKTREE BYTES" as its source. That review verified nothing about the deliverable: every fix it read was seen in a kid worktree that was never committed, and at the cut tip 17124cc46 the merged tree carried NONE of them -- experiment:a00-6678e0d1-53f123 had no verdict/confidence/evidence_runs, its row 2 still cited provisioning.py:533-536, and experiment:a00-9db7337e-cc325e Agent Notes still read 28 prod / 39 test net. The review therefore accepted a record that does not exist in the branch. The mechanism itself is NOT in doubt: the parent probes (WIRE 100 live calls, len(sys.path) delta 0; GATE cfg= beats root 2.5 and a declared 0.0 stays 0.0; AUTH an unauthorised caller gets the declared default 1.0, no raise; ROUTE exactly one sys.path.insert at provisioning.py:67, module scope) all hold on the merged bytes. The failure is the RECORD, not the code, and it recurred: the salvage that rescues a kid which exits with no commit fired at EG.156 and again at EG.164, with no detector added either time. EG.193 re-grounds every claim in the merged bytes and moves this paragraph INSIDE the THOUGHT block -- it had been written AFTER THOUGHT:END, so extract_thought() returned the stale EG.156 text and strip_thought() left the review as unattributed prose riding in every rendered document, which test_thought_hygiene.py cannot see (it only counts BEGIN blocks).
<!-- THOUGHT:END -->
