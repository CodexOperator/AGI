---
id: idea:lm-spiking-as-frozen-spectral-snapshots
mint_id: 1b0237a617db4c078b167e5bba0f26cf
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: 1792b285d445979e
season: 2
thought_session: dissolve-legacy-2026-09-19
title: "Deconstruct the spiking model instead of porting its time loop: carry the population as frozen-in-time spectral (Fourier / phase) snapshots so the evolution between snapshots is a parallel map over modes, the shape an interaction-net runtime (Bend/HVM) and a GPU actually reward -- the sequential 1000-step LIF recurrence was the worst shape for both"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-spiking-as-frozen-spectral-snapshots

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 17:4xZ (thought-master pane), verbatim: "But yeah we can keep trying to use bend did we deconstruct the spiking model wel enough. Can we try out some other mathematical algorithmic approximation tricks to comforter transform type stuff to carry the frequencies as frozen in time snapshots etc" (read: Fourier transform). ANSWER so far: NO -- TM.32/TM.35 ported the LIF as its literal time loop (1000 sequential steps over N=10000 neurons, 100 synapses each; lif.bend / lif_gpu.bend), a recurrence where step t+1 needs step t, which serializes an interaction-net runtime and starves a GPU; the 13x / 37.8x are measurements of that shape, not of Bend. FOUR DECONSTRUCTIONS, cheapest first: (1) event-driven LIF -- between spikes the membrane has a closed form (exponential decay toward the input), so integrate exactly spike-to-spike and only touch neurons that receive an event (the classic speedup; still sequential in event time). (2) SPECTRAL SNAPSHOTS (the owner idea): represent each neuron / the population by the Fourier (or phase-amplitude) coefficients of its drive and response at a frozen instant; between snapshots every mode evolves independently as a phase rotation exp(i w dt) and a gain (the LIF is linear below threshold), so the evolution is an embarrassingly parallel map over modes -- threshold crossings are re-inserted at the snapshot boundaries (the nonlinearity happens only there). Cost per snapshot O(modes x neurons) with no dependence chain inside the snapshot. (3) RHYTHM BANK / Kuramoto order parameters (the town C2 line: c2-kuramoto-metronome-rhythm-bank, c2-flip-as-phase-jump-vs-sign-inversion): keep K tone phases + the population order parameter R instead of 10000 membrane potentials -- an approximation that is exact for the readout the town wants (frequencies, phase locks). (4) per-neuron parallel map inside a step (the trivial fix if the kid folded sequentially over neurons; the why-idea experiment (4) decides). FIRST HYPOTHESIS minted: hypothesis:lm-spectral-snapshot-lif-matches-reference.
