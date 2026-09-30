---
id: hypothesis:pb3-close-the-four-residual-falsifier-and-leak-gaps
mint_id: a5d0f584a86143fd8533d34537e9b16f
type: hypothesis
parents:
  - experiment:dg2mvp-g13132-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 3b11c6175a6acb33
season: 2
testable_claim: through write.py only, the goal's falsifier 2 returns 0 hits, the guard's own scan of HEAD tracked blobs carries 0 hardware-class files, the goal's falsifier 1 gates every conjunct, and half b's falsifier no longer requires NEAR MISS inside a THOUGHT that another goal rewrote
title: "goal:g1.31.3.2 closure: name the --data-work pattern shell-split in the half-b prose, scrub the one remaining hardware fragment by class label, repair the two falsifier chains"
town: core
---
# hypothesis:pb3-close-the-four-residual-falsifier-and-leak-gaps

## Measured
At HEAD (counts and classes only): goal falsifier 2 returns 1 hit (hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored Agent Notes :101, prose naming the pattern plain, added by 43c6253ccc); the goal's falsifier 1 bash -c lacks `&&` after the `--data''-work` line, so its first two conjuncts never gate rc (measured rc 0 while falsifier 2 fires); half b's falsifier exits 1 on its last conjunct (`NEAR MISS` inside experiment:a00-6b761b8c-b6ae8b's THOUGHT: the THOUGHT was rewritten by the g1.31.3.1.1 round, the text now lives at body :240); anonymize over HEAD blobs reports 1 tracked file with the hardware class: hypothesis/lm-kv-slot-save-beats-reprefill.md:14 (1 occurrence).

## CLAIM
(1) the :101 prose writes the pattern shell-split (`--data""-work`) so falsifier 2 returns 0 hits; (2) that one node names the card by its class label, read in-process and masked, never typed; `anonymize check` over HEAD blobs then counts 0 hardware-class files; (3) goal:g1.31.3.2's falsifier 1 gains the missing `&&` and stays rc 0 at the corrected tip; (4) half b's falsifier last conjunct reads "the THOUGHT exists and does not contain `Content otherwise unchanged`", since the authored THOUGHT is a later round's.

## Dispatch line
config-max: none. template-max: none. code: none. A node-answer round, write.py verbs sub / replace body / thought; pi-free parent, 1 kid at most.

## FALSIFIERS
F1: `git grep -n -e '--data''-work' -- .agi/nodes ':!.agi/nodes/goal'` returns any hit. F2: the anonymize scan over `git ls-files` blobs (in-process, counts only) still reports the hardware class on any file. F3: the goal's falsifier 1, run verbatim at the corrected tip, exits 0 while F1 or the stale-word check is broken (mutate one conjunct to confirm it now gates). F4: half b's falsifier exits 1 at the corrected tip. Also false: links broken != 0, node count drops, an edit lands outside write.py, or any output carries a hardware, host, user or repo value.

## TESTS
No code. Per node `write.py <id> 'read body L:L'` before/after piped through a masking filter; the four falsifiers; `links.py links`; `python3 -m pytest extensions/agi/tests/test_anonymize_guard.py -q` (one file).

## FILE SCOPE
.agi/nodes/hypothesis/pb3-hw-name-scrubbed-and-four-lost-corrections-restored.md · .agi/nodes/hypothesis/lm-kv-slot-save-beats-reprefill.md · .agi/nodes/goal/g1.31.3.2.md (the falsifier block only)

## CEILING
0 production lines · <= 4 write.py calls per node · kids <= 1 · 0 USD.
