# deq — Deep Equilibrium Models
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/1909.01377 + NeurIPS 2019 (checked 2026-09-18)
- TITLE (MEASURED): "Deep Equilibrium Models"
- AUTHORS (MEASURED): Shaojie Bai, J. Zico Kolter, Vladlen Koltun (CMU / Bosch).
  YEAR: submitted 30 Sep 2019; NeurIPS 2019. ID: arXiv:1909.01377.
- MECHANISM (MEASURED, abstract): hidden layers of deep sequence models converge to a fixed
  point; DEQ directly FINDS that equilibrium via root-finding. Equivalent to an infinite-depth
  weight-tied feedforward net; backprop through the equilibrium by IMPLICIT DIFFERENTIATION.
  Constant memory regardless of effective depth.
- HEADLINE NUMBERS (MEASURED, abstract): up to 88% memory reduction on WikiText-103; matches
  or improves SOTA at similar parameter counts; similar compute.
- COMPUTE SAVED (MEASURED): 88% memory reduction (training). NOT a training-compute % per se.
- CODE/LICENCE (MEASURED): github.com/locuslab/deq — MIT (repo listing).
- QWEN-CLASS TRUNK? No — self-attention transformer + trellis, trained from scratch.
- FIT: answers "if equilibrium is literal". DEQ's equilibrium = fixed point of the WHOLE
  network, solved at every forward. The owner's equilibrium = plateau of the encoder's loss
  before freezing. DIFFERENT use of "equilibrium": DEQ is an architecture, not a freeze
  schedule. Cite as the literal-equilibrium reference; do not conflate.
