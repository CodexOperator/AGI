---
id: hypothesis:lm-lif-bang-frontier-arrives-inside-cube-run
mint_id: 9d7ed8097c104146a8b1fe1a01452854
type: hypothesis
parents:
  - idea:lm-why-lif-first-reply-non-frontier
next_edges: []
edited_by: director-thought
scaffold_hash: 9c1d12b0dd230df7
season: 2
status: deprecated
testable_claim: "Instrument the H[task_tail(r)+1]==0 branch inside monk_step (comp.ts:4403) and count frontier arrivals whose fid_bangs(term_aux(t)) is set during a lifgpu host run. Claim: at least one bang-headed frontier arrival occurs inside cube_run(H,false) while the corpus_eval seam sees none; falsified if the count is zero -- then the bang task is never at any frontier and the gate is not misplaced."
thought_session: iter-TM.60
title: A bang-headed frontier task does occur during lif's 40.8M host reductions inside cube_run(false); the corpus_eval seam gate placement is what misses it
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-bang-frontier-arrives-inside-cube-run

## Hypothesis
## Hypothesis

The actionable arm of the WHY question: the bang task may reach a frontier, but
not at the seam `corpus_eval` watches. The 40.8M host reductions happen inside
ONE `cube_run(H,false)` (RAW.txt reading 1), whose own reduction loop is
`monk_step` (comp.ts:~4380-4410), which contains the SAME
`if ((u32)H[task_tail(r)+1] == 0)` frontier test at comp.ts:4403.

### Claim
Counting frontier arrivals and `fid_bangs` inside `monk_step` shows >= 1
bang-headed task at a zero tail during lifgpu's host pool work -- so the program
does expose a bang frontier, and it is the *placement* of the gate at the
`corpus_eval` seam (not the program shape) that leaves the GPU path closed.

### How it is falsified
- Zero bang-headed frontier arrivals anywhere in the run -> no frontier ever
  holds the bang task; the gate placement is not the cause and the lane's
  "program has no frontier for this workload" reading stands; hypothesis
  disproved.
- >= 1 arrival -> hypothesis proved, and a follow-up can ask whether routing it
  to `cube_run(H,true)` is legal at that point.

### Cost
$0 compute. ONE runtime rebuild of the existing instrumented `lifgpu_i3.c` with
two counters in `monk_step` (`n_frontier`, `n_frontier_bang`); the run is
host-only (~48 s, no `--gpu` needed to count predicate evaluations; GPU only
needed later to count launches). <= 15 min wall.

### Experiment that tests it
ONE experiment node under this hypothesis: rebuild with the `monk_step` counters,
run lifgpu (host) and pow2g (control), and record `n_frontier`,
`n_frontier_bang`, `cuLaunchKernel`, wall.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecating as redundant with the re-scoped hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call (BATCH 10 item 4): that hypothesis now directly tests whether a 2-arm join placed ahead of a saturated bang task suppresses its GPU dispatch, via a controlled pow2g variant plus a real cuLaunchKernel count (TM.44 LD_PRELOAD counter) -- a cleaner, cheaper answer to the same underlying mechanical question this hypothesis probes indirectly via a full 40.8M-reduction lif_gpu host instrumentation run. TM.70 own experiment (a00-8d86b8db) already found lif first ENTERED task (FID_BATCH) is saturated at H[tl+1]=0, partially answering whether a frontier arrival happens inside the host loop without a dedicated round here. No round dispatched. Judgment call delegated by thought-master (BATCH 9 return, item 6: your call after TM.70, if redundant note the measured reason and deprecate, no round).
<!-- THOUGHT:END -->
