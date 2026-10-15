---
id: goal:g5.28
mint_id: dbcbd30d58c44c2d827de7610ed742d7
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
edited_by: thought-master
goal_id: G5.28
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 27266cd679b040e7
season: 2
seeds:
  - hypothesis:c2-flip-as-phase-jump-vs-sign-inversion
  - hypothesis:c2-kuramoto-metronome-rhythm-bank
  - hypothesis:lm-bend2-spiking-sim
  - hypothesis:lm-c2c-kv-bridge-released-fusers
  - hypothesis:lm-oscillator-research-hunt
  - hypothesis:lm-pufferlib-oscillator-policy
  - hypothesis:lm-spectral-snapshot-lif-matches-reference
  - idea:lm-hunch-energy-frequency-prediction
  - idea:lm-hunch-graphgents-snn-walkers-on-the-thoughtgraph
  - idea:lm-hybrid-oscillator-readout
  - idea:lm-spiking-as-frozen-spectral-snapshots
  - idea:lm-token-state-feedback-merge
status: horizon
tags:
  - local-maxxing
  - side-track
  - spiking
  - oscillator
title: "G5.28: SIDE TRACK — spiking / oscillator readouts (Kuramoto, LIF/spectral, C2C fusers, SNN walkers, the bend2 spiking sim): only as capacity allows, never ahead of an owner-track round, imported into the main tracks piece by piece as learned (owner 21:4xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.28

## Agent Notes
**Owner source (2026-09-20 21:4xZ, verbatim on goal:g14):** "No crazy spiking stuff too much yet except on the side if capacity allows like mainly the bend2 language mapping so we can slowly import it into the graph not just wholesale but as we learn the useful things we need to know about it to make things run better." Earlier sources: the owner's oscillator / Kuramoto / C2C / LIF threads (goal:g14 notes 09-14 → 09-19).

**Commits to.** Keep the spiking and oscillator lines alive as a **side track**: coupled-oscillator readouts, LIF/spectral snapshots, C2C fusers, Kuramoto rhythm banks, SNN walkers, the bend2 spiking sim — run only when no owner-track (G5.22–G5.27) round is waiting for the same resources, and only as small measured chunks whose *learned* pieces are imported into the main tracks (e.g. a coherence ranking that G5.22 can use) rather than wholesale. G14.5 (the bend2/HVM source mapping) is the sibling that feeds this track its ground truth.

**Invariants.** A side-track round never holds the GPU or the paid-round slot ahead of an owner-track round; every chunk names the main-track hypothesis it would feed if it proved; the oscillator budget is gated by G5.22's first chunk (the K_c kill-test) — no oscillator spend before that verdict; kill criteria pre-registered per chunk (the 09-20 judge's FRANK 7).

**Falsifiers.** The track is paused (status `horizon`) for the season if two consecutive chunks feed nothing measurable into a main track, or if the K_c kill-test returns the null and no other coherence signal survives its own falsifier.

**Status, season 2 (10-11): PAUSED (`horizon`) by its own Falsifier.** Two consecutive chunks fed nothing measurable into a main track: FREQ-ABLATION (experiment:dt1-neuron-period-freqabl-1001) and PAIR-LOSS (experiment:dt1-neuron-period-pairloss-1010), both DISPROVED, neither naming a G5.22-G5.27 hypothesis it would feed (the Invariant). The proposed next chunk (a per-row / off-distribution look at seed 1 k=3) names none either. Council ruling: alive 12:47Z 10-11, 3/3 [no-go]. A reopen in season 2 needs the owner; belam banks it with the season-2 close.

**Done when.** Never as such — it is retired into the main tracks piece by piece; done for a season when every learned piece has a home under G5.22–G5.27 and nothing here is still live.

**Seeds:** the existing oscillator/spiking nodes re-homed here on 2026-09-20 (cleanliness pass). Sub-sub-goals are the director's to mint (G5.28.1 readouts, G5.28.2 bend2 spiking sim), same format, before any chunk runs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 13:1xZ 10-11: status active -> horizon, one Status paragraph added above Done-when. Why: the council (alive 12:47Z 10-11, 3/3 converged, all-is-one found it) ruled [no-go] on the next periodicity chunk, citing this goal's Falsifier as written -- two consecutive chunks (FREQ-ABLATION, PAIR-LOSS) fed nothing measurable into a main track, and neither named the main-track hypothesis the Invariant requires. The council's GO path (name a G5.22-G5.27 hypothesis the s1 k=3 look would feed) was not taken: none consumes a per-row look at one inert frequency in a toy mod-113 model, and inventing that link to keep DT-1 busy is the scope creep CLAUDE.md names. The council asked that the pause be recorded HERE, not only in belam's bank. PRIOR THOUGHT, carried verbatim: owner ask 2026-09-21: renumber local-maxxing research g5.28 → g5.28 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
