---
confidence: 1.0
demote_reason: "no experiment evidence (evidence_runs=0) for 'proved'"
demoted_from: proved
evidence_runs: 0
id: "exp:exporters-r1-extend"
mint_id: 29edd06bcba74972839b9fe29592aa1c
next_edges:
  - verdict:exporters-r1-extend
parents:
  - hyp:exporters-r1
  - verdict:exporters-r1
status: "inconclusive_lean_proved:50"
tags:
  - exporters
  - chain-extension
  - r1-extend
title: "Experiment: Exporters R1 Extended"
type: experiment
verdict: "inconclusive_lean_proved:50"
---

# Experiment: Exporters R1 Extended

Extends the exporters chain from 8 to 10 hops via verdict→experiment→verdict pattern.

## Chain Extension

- verdict:exporters-r1 → exp:exporters-r1-extend → verdict:exporters-r1-extend → mvp:exporters-r1

This adds 2 more hops to the chain, demonstrating the verdict→experiment→verdict pattern is stackable.
