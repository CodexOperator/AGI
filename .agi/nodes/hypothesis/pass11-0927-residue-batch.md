---
id: hypothesis:pass11-0927-residue-batch
mint_id: 4af032c7eb634ec3933c7328c34430ce
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: b2a2369f824ed2e8
season: 2
status: open
testable_claim: The falsifier grep of goal:g1.27 returns 0 hits and each row below is fixed at its cited line.
title: "PASS 11 doc and skill residue batch: no text names the paid route, points past its block, cites a wrong line, or hand-copies the skill index (assigned: director-engine)"
town: core
---
# hypothesis:pass11-0927-residue-batch

# hypothesis:pass11-0927-residue-batch

PASS 11 residue table (verify-upheld; run mur-p11chunk1of1):
| # | where | residue |
|---|---|---|
| 1 | skills/agi-rotate/SKILL.md:12 | facts pointer `read body 37:64` -- the region is 37:57 since cdcfe5c0b |
| 2 | skills/agi-master-gate/SKILL.md:55 | cites rotate.py:16159 (a bare pass); the mirror gate is rotate.py:4053 branches.mirror_and_prove in _prepare_merge_target |
| 3 | extensions/agi/briefs/director-belam-duties.md:5, master-sensei-duties.md:5, sensei-director-duties.md:3 | 'a review by name on pi' (the PAID harness) + a hand-copied skills index that the startup `skills` entry now loads (owner 05:33Z: no duplication) |
| 4 | extensions/agi/workflows/round-research-review.json:7 | description still 'Requires --harness pi' against its own provider pi-free |
| 5 | .agi/config.json:200,205,210 | workflows notes still name provider pi / the pi harness |
| 6 | .agi/nodes/build/bin-provisioning.md:121 | BUILD-CONTRACT stale: can_fund at line 177 with the old signature |
| 7 | skills/agi-dispatch/SKILL.md:36 | hardcodes '<= 8 live parents' while values.local_maxxing.de_live_parents is the cell |

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.670 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11; evidence run mur-p11chunk1of1 verify_engine-delta-{1,2}.json)
Dispatch line  config-max: row 7 cites the cell values.local_maxxing.de_live_parents, never a number · template-max: rows 1-5 are template/doc text, fixed there · code: none
ORDER      ROW 3 FIRST (belam: "the duty briefs still say review on pi = PAID -- do that row first"): name pi-free for a review by name, and replace the hand-copied skills index with a pointer to the startup skills entry. Then rows 1 2 4 5 7.
ROW 6      a BUILD-CONTRACT is regenerated, never hand-edited: regenerate it with the engine's regenerator and paste the command + its output on your node; if none regenerates it in scope, NAME it on your node for the director (file:line), never hand-edit.
FALSIFIERS each row's cited string still present at its line (paste the grep per row, before and after) · any row fixed by hand-editing a derived block
TESTS      test_bin_help_smoke.py + every test that pins these files' bytes (git grep -l the edited file names in extensions/agi/tests, run those) once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE skills/agi-rotate/SKILL.md · skills/agi-master-gate/SKILL.md · extensions/agi/briefs/director-belam-duties.md · extensions/agi/briefs/master-sensei-duties.md · extensions/agi/briefs/sensei-director-duties.md · extensions/agi/workflows/round-research-review.json · .agi/config.json (the workflows notes only) · skills/agi-dispatch/SKILL.md · .agi/nodes/build/bin-provisioning.md (regenerated only) · the kid's own node
CEILING    HARD CAP: 1 kid · 0 production code lines · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.670 brief added by director-engine: belam minted this node as a measured stub (claim + evidence line) and queued it to this post ([decision] 23:0xZ, goal:g1.27); the schema's round brief (dispatch line, falsifiers, tests, file scope, ceiling) was missing, and the director template says the director writes it when the master did not.
<!-- THOUGHT:END -->
