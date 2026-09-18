# lit-locked-image-tuning — LiT: Zero-Shot Transfer with Locked-image text Tuning
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/2111.07991 (checked 2026-09-18)
- TITLE (MEASURED): "LiT: Zero-Shot Transfer with Locked-image text Tuning"
- AUTHORS (MEASURED): Xiaohua Zhai, Xiao Wang, Basil Mustafa, Andreas Steiner,
  Daniel Keysers, Alexander Kolesnikov, Lucas Beyer (Google Research / Brain).
- YEAR (MEASURED): submitted 15 Nov 2021; v3; published CVPR 2022; DOI 10.1109/CVPR52688.2022.01759.
- ID (MEASURED): arXiv:2111.07991.
- MECHANISM (MEASURED, abstract): contrastive-tuning — align image+text models while using
  pre-training. Empirically LOCKED (frozen) pre-trained image models + UNLOCKED (trainable)
  text models work best. LiT "just teaches a text model to read out good representations from
  a pre-trained image model for new tasks." = FREEZE the heavy trunk (image encoder), TRAIN the
  light readout (text encoder). Exactly the trunk-frozen / readout-trained shape.
- HEADLINE NUMBERS (MEASURED, abstract): ViT-g/14 locked + trained text model -> 85.2%
  zero-shot ImageNet, 82.5% ObjectNet. Works across ResNet/ViT/MLP-Mixer, supervised+unsup
  pre-training, 3 image-text datasets.
- COMPUTE SAVED: NOT stated as a % in the abstract. The saving is structural: image encoder
  forward is frozen/no-grad, gradients only through text tower. ESTIMATE: large (no image-side
  backward), but the paper does not quote a number. NOT a Qwen/LLM trunk — vision.
- CODE/LICENCE: Big Vision / open_clip ecosystem; LiT configs in google-research/big_vision
  (Apache-2.0). NOT verified in this read.
- QWEN-CLASS TRUNK? No — ViT/resnet image encoder.
- FIT: conceptual ancestor for "freeze trunk, train readout". Trunk is a perception encoder,
  not an LLM; transfer is the pattern, not the exact architecture.
