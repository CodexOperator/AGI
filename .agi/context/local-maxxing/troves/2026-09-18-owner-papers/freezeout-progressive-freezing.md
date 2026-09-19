# freezeout-progressive-freezing — FreezeOut
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/1706.04983 (checked 2026-09-18)
- TITLE (MEASURED): "FreezeOut: Accelerate Training by Progressively Freezing Layers"
- AUTHORS (MEASURED): Andrew Brock, Theodore Lim, J.M. Ritchie, Nick Weston
  (Heriot-Watt / Edinburgh; later DeepMind). YEAR: submitted 15 Jun 2017 (v2 2017).
- ID (MEASURED): arXiv:1706.04983.
- MECHANISM (MEASURED, abstract): "only train the hidden layers for a set portion of the
  training run, freezing them out one-by-one and excluding them from the backward pass."
  Anneal layer-wise LR to zero on a schedule; once a layer bottoms out it leaves the
  backward pass. This is PROGRESSIVE freezing (the opposite direction of "freeze trunk then
  train head", but the same mechanism family: swapping computation off parts of the net).
- HEADLINE NUMBERS (MEASURED, abstract): up to 20% wall-clock savings; DenseNet -> 3% acc
  loss; ResNet -> 20% speedup with NO accuracy loss; VGG -> no improvement.
- COMPUTE SAVED (MEASURED): up to 20% wall-clock. NOT Qwen/LLM. CIFAR-scale CNNs.
- CODE/LICENCE (MEASURED): github.com/ajbrock/FreezeOut — MIT (repo README, checked 2026-09-18:
  GitHub listing).
- FIT: the *schedule* half of the owner's recipe (warm for a few rounds, then stop updating).
  Here it freezes early layers; the owner wants to freeze the whole trunk and keep training
  the decode-side module. Complementary, not identical.
