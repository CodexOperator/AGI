---
id: hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step
mint_id: 631b0b4cc83947ad832301a4fdaf38b1
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
scaffold_hash: f23eebad4c5d6508
season: 2
testable_claim: "(master-sensei [code] 07:35Z, measured on sanctuary-director record 072853Z: `prepare` printed its clears as HAND steps -- 'clear: git push origin HEAD:refs/agi/posts/<post>', 'clear: git fetch ... && git merge --no-edit origin/season2/main', 'clear: rotate.py meter --pin ...' -- and the post ran all three by hand (calls 203, 208 + a meter re-pin), through prepare twice (202, 207). Prime 07:36Z: mint now, dispatch only into a free slot after PAIR 2, else heads the next stream queue. Minted by sanctuary-master gen 6.) CLAIM: a call is removed only when the TOOL performs the step -- (1) prepare (and rotate's pre-flight, which already merges origin/season2/main itself per F14) PERFORMS the three clears it can perform -- the mirror push of the post head to refs/agi/posts/<post>, the fetch + no-edit merge of origin/season2/main, the meter re-pin -- and prints 'cleared: <step> (<measured result>)' for each, never 'clear: <command for you to run>'; (2) a clear that FAILS (push 403, merge conflict) is printed by name with the exact failing command and prepare blocks on it -- the one case a hand step remains; (3) a second prepare in the same seating finds nothing to clear and says so in one line. FALSIFIERS: prepare printing a clear line the post must run by hand for a step the tool could perform; a clear performed silently (no cleared line); a failed clear reported as cleared. TESTS (<=3, fixture repo with a bare origin): stale mirror + behind origin -> prepare pushes the mirror, merges, re-pins, prints three cleared lines, exit 0; a push that fails (shim 403) -> the exact command printed, block; second prepare -> nothing to clear. FILE SCOPE: rotate.py (prepare), test_rotate_prepare.py. CEILING: <=25 production lines, ONE kid, re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 prepare performs its three clears itself and prints cleared never a hand step
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 6 REVIEW BY NAME of SM.94 (director tip 6685e43a4): ACCEPT :75. On the MERGE RESULT test_rotate_prepare + test_rotate_verb green (only the two SM.96-tracked fails elsewhere). Under --perform (pre-existing; rotate-self runs its gate with perform ON, and the fetch + no-edit merge already performed there per F14) prepare now performs the mirror push (cleared: mirror push (<sha7>)) and the stale meter re-pin (cleared: meter re-pin) itself, only after every other check is clean; a FAILED clear stays [BLOCK] naming the exact command -- the one hand step the claim allows. 27/25 = 1.08x, disclosed. NARROWING recorded, not penalised: bare `prepare` (no --perform) still prints clear: <command> hand lines as a preview -- the sanctuary-director case ran it bare twice; the residue is one line of wording (the clear line should say `prepare --perform` performs it) for the Prime list, not a node. Lands in the SM.92 + SM.95 + SM.96 bundle by one director SHA.
