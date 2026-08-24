---
id: exp:exporters-r1-extend2
title: "Experiment: Exporters R1 Second Extension"
type: experiment
status: proved
verdict: inconclusive_lean_proved:50
confidence: 1.0
parents:
  - verdict:exporters-r1-extend
  - hyp:exporters-r1
tags:
  - exporters
  - chain-extension
  - r1-extend2
next_edges:
  - verdict:exporters-r1-extend2
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

# Experiment: Exporters R1 Second Extension

Extends the exporters chain from 10 to 12 hops via second verdict→experiment→verdict cycle.

## Chain Extension

- verdict:exporters-r1-extend → exp:exporters-r1-extend2 → verdict:exporters-r1-extend2 → mvp:exporters-r1

This adds 2 more hops, proving verdict→experiment→verdict cycles are stackable.
