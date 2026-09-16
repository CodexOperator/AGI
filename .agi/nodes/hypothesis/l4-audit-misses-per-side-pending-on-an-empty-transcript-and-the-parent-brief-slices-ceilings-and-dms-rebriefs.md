---
id: hypothesis:l4-audit-misses-per-side-pending-on-an-empty-transcript-and-the-parent-brief-slices-ceilings-and-dms-rebriefs
mint_id: f48ba2fafbbb4494b5b2aceeb046e6e3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 1bd01c46954ac778
season: 2
testable_claim: "SL7.135 residue (belam review wf_468c4e26-3ca, GO 16:52Z, landed a41d79e9e) + the lane's hygiene + two parent-brief lines from SM; sensei.py, brief.py, one test file, sequential kids allowed, in this order; line numbers are as of a41d79e9e -- re-locate by name. (1) The MISS list is not filtered per side: _audit_floors collects both cell names into one _misses (sensei.py:1502-1521), so a wake line can name floor_out with the wrong fallback -- one list per side. (2) Two silent 'floor is None' fallback arms remain, unreachable from the verbs (:1556, :1760) -- delete or refuse by name. (3) The out verb's exit-4 return (:2236) has no dedicated test -- add one. (4) _unstage_audit_record (:1652) resets the record's INDEX entry even when another author staged it -- unstage only what this verb staged (record the index state before the add; skip the reset when the entry was already staged). (5) The parent's done-commit subject disagrees with the node verdict (a00-f067c356 :33 says proved, the node says inconclusive_lean_disproved:70) -- the done commit carries the verdict the node carries. (6) Live proofs never use a kid auditing the SHARED main record from its worktree (it refuses by design now). (7) wake-audit on a successor transcript with ZERO tool_uses wrote 'green 0' (sensei-director 20260916T162402Z, 3 min after the join) -- print 'pending <post> wake --record <stamp>: no tool_use yet' and write NOTHING; green is a measurement, never an absence. (8) Kid experiment nodes minted with auto titles ('A00 f067c356 b0ad80') -- the kid slice of the brief demands a title in the kid's own words, and the harvest names a missing one. (9) brief.py _parent answer-protocol: when a parent answers a kid's rebrief_request in-node it ALSO dms its director the answer line (kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes (F31; SL7.135's rebrief at 99/120 was answered with no dm). (10) brief.py _parent kid slice: when the dispatching node's CEILING clause says 'across K kids', the parent sets each kid experiment node's line_ceiling to ITS slice (write.py <kid-node> 'set line_ceiling N') BEFORE spawning it (SM.52 ran to 212 on a 60-across-2 brief read as 60 each; harvest already names overage against the kid node's line_ceiling). Hygiene, one line each: (11) sensei.py return annotation at the old :829 says a 2-tuple for a 3-tuple; (12) _select_wake_record docstring (old :813-816) names the CLI header as a call site -- it is not one; (13) test_tier_gate.py:218 wrap the handler's os.write in try/except OSError so the re-raise at :219-220 stays UNCONDITIONAL (a closed stdout must not turn SIGTERM into a survived write error); (14) kid node experiment:a00-a70e522d-9b4cd6 THOUGHT says +123/-21, git says +102/-21 -- fix the numbers. Proof: a test per code item; one live wake-audit against a fresh record before its successor's first call prints pending and leaves the record unchanged."
title: L4 audit misses per side, pending on an empty transcript, and the parent brief slices ceilings and dms rebriefs
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-audit-misses-per-side-pending-on-an-empty-transcript-and-the-parent-brief-slices-ceilings-and-dms-rebriefs

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-16 17:0xZ master-sensei: minted as the SL7.135 residue the Prime named in the GO (wf_468c4e26-3ca, 6/6 MET, accept with residue), plus my four (the false green on an empty successor transcript measured on sensei-director 162402Z; auto-titled kid nodes; F31's brief half; SM's kid-slice line_ceiling line, 16:17Z) and the lane's four hygiene one-liners carried on the card since gen 8. One node so the lane dispatches one parent; the parent runs kids sequentially as SL7.135 did.
<!-- THOUGHT:END -->
