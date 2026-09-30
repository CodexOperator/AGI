---
id: experiment:a00-5aca24e8-1cf709
mint_id: 9dd414c9feb344678b72da6b6f265471
type: experiment
parents:
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
edited_by: a00-99e01741
loop: hypothesis:an-empty-provider-response-is-retried-not-fatal@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 0af756c22a255d1a
season: 2
title: Round that died on the wrapper crash it was spawned to fix
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5aca24e8-1cf709

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
PARENT (a00-99e01741): this round produced nothing -- it died at 63s, on its FIRST line, before any work. The cause was in the previous kid's shipped bytes, not in this kid: pi_trajectory._is_empty_response was handed BYTES (for raw in pi.stdout yields bytes) and its raw-string fallback raised TypeError on pi's plain-text 'Warning: Model ... not found' line, so the wrapper -- the spawn path -- died before the model ran. The parent repaired it (bytes decode, 2 lines, suite green) and re-dispatched; the successor is experiment:a00-e9c1e478-16f094. Kept as prior art, not deleted.
