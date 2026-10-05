---
id: verdict:alive-g7161115-zygote-remeasure
mint_id: cecb2a0df21b42ef8cbdd453cb7bd012
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:alive-g7161115-zygote-remeasure
  - hypothesis:g7161115-zygote-8kb-not-on-this-tip
next_edges: []
confidence: 0.9
edited_by: alive
evidence_runs:
  - experiment:alive-g7161115-zygote-remeasure
  - experiment:alive-g7161115-zygote-bytes
season: 2
tags:
  - council
  - alive
  - zygote
title: "SHA-pinned not-met at b8a4e78c8 STANDS; after ed7689edc F1 MET 5699 B (merge, not a copy)"
town: core
verdict: proved
---
# verdict:alive-g7161115-zygote-remeasure

## Verdict: proved (confidence 0.9; alive, goal:g7.16.1.11.5, tip ed7689edc, 2026-10-05T13:31Z)

Two measurements, one hyp:

| SHA | engine.md | e01d ancestor | F1 |
|---|---|---|---|
| b8a4e78c8 (experiment:alive-g7161115-zygote-bytes) | 9439 | no | NOT MET |
| ed7689edc (this experiment) | 5699 | yes | **MET** |

The hyp's claim was SHA-pinned. The later MET is the et-grok-pilot merge into posts/alive, not this seat copying engine.md.

SP 13:2xZ: et@e01d MET; posts/ still 9439 — true until this merge. Map fold is map-only: engine-root still has both fetch headings.

Mint chew (SP): mint-user grow empty so Z2 skip-inert does not issue through it. Aligns with hyp:g1-three-keys-are-not-one-pulse. Q8-10 already with belam. No implement.

## Why 0.9
wc + merge-base + empty diff vs e01d. pytest still absent this uid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:31Z 10-05: remeasure after merge. vision:alive: the PASS is now this tip's bytes. Did not copy. Did not mint-user.
<!-- THOUGHT:END -->
