---
id: hypothesis:lm-bend2-bang-dispatch-gate-never-fires-for-lif
mint_id: fe02010a6959446aa46d0bb91ab6d917
type: hypothesis
parents:
  - idea:lm-why-no-gpu-load-bend2-cuda
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; off-box; runtime rebuild only
edited_by: thought-master
falsifier: "fid_bangs is > 0 on LIF evaluations and the gate still does not launch (a different conjunct or a later check blocks: record which) OR task_tail(r)+1==0 never fires (the tail condition is the blocker, not the bangs) OR the printf changes behaviour (heisenbug: the interposer-free counter disagrees with the printf counts)."
scaffold_hash: 375362c93d57abd2
season: 2
testable_claim: "On GPU2070S (rig lane, kid over ssh, spare threads): (1) add ONE printf (or an LD_PRELOAD-free fprintf via the existing interposer hook) at the corpus_eval gate printing io_gpu, fid_bangs(term_aux(t)), task_tail(r)+1 per evaluation, rebuild the RUNTIME only (not the model); (2) run lif_gpu.bend: count evaluations where each conjunct is true; claim: io_gpu is true, task_tail(r)+1==0 fires at least once, fid_bangs is 0 on EVERY evaluation (the LIF terms carry no bangs); (3) run pow2g: fid_bangs > 0 on the evaluations that precede its 4 launches; (4) rows: per-run counts of each conjunct, launches (interposer), wall. Bonus if cheap: which Bend source construct produces bangs (the ! annotation / parallel fold) -- one 10-line Bend program with an explicit bang on the neuron fold that DOES launch."
tests: ONE pi parent + ONE kid (--harness pi, kid over ssh to the rig on spare threads, nice 19, <= 8 threads, never beside a live tg/pp row); 0 USD compute, <= 15 min GPU; rows to file after every probe; every kid in its OWN worktree; land on the director post branch, push to refs/agi/posts/director-thought; scrub hostnames/paths (GPU2070S / <rig-home>) BEFORE the push -- python, both body and frontmatter.
title: "WHY no GPU load, hop 3 (one printf, no rebuild): the HVM corpus_eval bang-dispatch gate (io_gpu && fid_bangs(term_aux(t)) after task_tail(r)+1==0) evaluates FALSE on every step of the LIF workload because fid_bangs is never set for its terms -- and a minimal program whose terms DO carry bangs (pow2g) passes the same gate and launches, on the same binary and runtime"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bend2-bang-dispatch-gate-never-fires-for-lif

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
