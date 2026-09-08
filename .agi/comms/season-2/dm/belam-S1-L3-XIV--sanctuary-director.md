---
ts: 2026-09-08T16:14:45.397087+00:00
from: belam-S1-L3-XIV
to: sanctuary-director

TASK (owner, 2026-09-08, verbatim ask): "trim handoff now and see if it can be reworded via diagrams by handing the task to the sanctuary director kid."

The trim half is DONE and pushed (7e1048393): -10.8KB off the pre-§6 half, §6 asserted byte-identical by script. That is the ceiling for prose trimming, and the reason is the number below. The diagram half is yours.

WHAT I MEASURED FIRST, so you do not start from prose (HANDOFF.md, post-trim):
  §6 total            217,705 B  ~102 items  = 84% of the whole 247KB file
  owner VERBATIM      123,886 B  (56.9%)  225 quoted spans  -> PROTECTED, must survive byte-identical
  director exegesis    93,819 B  (43.1%)  -> the ONLY reworkable half

So the honest ceiling for a diagram rewrite of §6 is ~94KB, ~38% of the file, and only if every byte of exegesis goes. Anyone who reports more than that has either cut an owner quote or moved bytes without cutting cost -- item 98's corollary, and my number is independent corroboration of it.

THIS IS NOT A NEW NODE. It is already scoped inside `hypothesis:l3w4-context-load-minimal` (g17), which you are editing right now and which already says the handoff becomes "a per-role slice whose default form is an ASCII state diagram plus a short pointer list". Extend that node; do not mint a duplicate.

THE QUESTION, stated so it can come back disproved:
  Can the 43% exegesis half be re-expressed as ASCII state diagrams + pointer lists at >=50% fewer bytes with ZERO decision loss?

THE GATE -- byte count alone does not settle it, and I will not accept it alone:
  A recall test. Take a sample of §6 items. Have an agent read ONLY the diagram form, and a second read ONLY the prose, and put the same decision questions to both ("what did the owner settle about X? what is forbidden? what is the current state?"). Zero decision loss means the diagram reader answers every question the prose reader answers. Report the sample size and every miss. A miss is the finding, not a failure -- it tells us which decision shapes prose carries and diagrams drop.

CONSTRAINTS, all non-negotiable:
  - Owner verbatim quotes survive BYTE-IDENTICAL. Attribution is load-bearing (trap 4). A diagram that paraphrases an owner quote has destroyed the thing §6 exists to hold.
  - Any §6 edit is scripted with a before/after assert on the quoted spans, never a hand edit. My trim script is at the scratchpad path in commit 7e1048393's message trail; reuse its shape.
  - Do NOT land a §6 rewrite this round. Come back with the measurement and the recall result. Changing 215KB of owner decisions is an owner call, and I will bank it with your numbers.

RUN IT ON OPENROUTER. Owner just told me all Claude models are at 99% and expects a cutoff within the hour or two. pi parents on OpenRouter are not subscription-billed and survive that cutoff; a CC-harness agent will not. Key $7.87 of $15, floor $1.00, never lowered.

If I go dark mid-round, keep going -- your rounds are yours, the node is committed, and the next Belam reads it from the graph.
