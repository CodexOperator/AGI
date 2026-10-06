---
id: hypothesis:swarm-size-5-10-15-parents-fixes-per-hour
mint_id: 7c9a429f48774472877b2471184d2d67
type: hypothesis
parents:
  - goal:g5.34
next_edges: []
confidence: 0.6
edited_by: thought-master
scaffold_hash: a4c0fb71315c2a90
season: 2
testable_claim: The largest arm (5, 10, 15 live parents) whose fixes landed per hour is >= 1.2x the next smaller arm and whose mur accept share is <= 10 points below it is the town swarm size; an arm the box never allows (load >= 16 or io PSI >= 50) is a CPU/IO finding
title: "Swarm size: 5 / 10 / 15 live DE parents on one queue -- fixes landed per hour and mur quality pick the size"
town: local-maxxing
---
# hypothesis:swarm-size-5-10-15-parents-fixes-per-hour

## Measured
| what | value | source |
|---|---|---|
| user@1000 memory high / max | 6628 / 7365 -> 12618 / 14021 MiB | belam [decision] 02:59Z 09-27 (OWNER GO) |
| model container | stopped (docker budget 6656M -> 0) | same |
| load (1 / 5 / 15 min) | 15.42 / 13.98 / 13.35 on 16 threads | /proc/loadavg, 03:0xZ 09-27 |
| io PSI some avg60 | 55.77 (avg300 57.07) | /proc/pressure/io, 03:0xZ 09-27 |
| DE live parents before | 8 (an order-level cap; no config cell, no engine check) | spawn_budget leases, config.json grep |

CPU and IO bind before RAM does (belam 02:59Z): the swarm size is limited by load and io PSI, not by memory.

## CLAIM
Over ONE queue (DE's fast-track: PASS 10's code defects + hypothesis:wake-facts-collapse-to-skill-pointers, then DE's standing queue),
run by director-engine with its live-parent cap at 10, then 5, then 15, the town picks the swarm size by a PRE-REGISTERED rule:
the chosen size = the largest arm whose fixes landed per hour is >= 1.2x the next smaller arm's AND whose mur accept share is
no more than 10 points below it. Arm 15 runs only while loadavg1 < 16 AND io PSI some avg60 < 50; an arm the box never allows
is a FINDING (blocked by CPU/IO), not a skip.

Metrics, per arm:
- fixes landed per hour = rounds whose final mur verdict is accept (or accept_with_residue with every residue closed in-loop) and
  that DE merged into its post branch, divided by the arm's wall-clock hours
- mur quality = accept share (accept / all final verdicts) · residues per round · demotes per round (runs/mur-*/verify_*.json)
- box = loadavg1 and io PSI some avg60, sampled every 60 s over the arm

## Dispatch line
config-max: the arm = the cell values.local_maxxing.de_live_parents (arm · arms · ceiling · ceiling_if); DE reads it and caps
its live parents at `arm`, never a literal in an order / template-max: none / code: none -- DE counts its live parents from
spawn_budget.py status (the leases), the samples come from /proc

## FALSIFIERS
- fixes landed per hour is flat or falls from 5 -> 10 (parallel parents do not help; the bottleneck is director review or the mur)
- accept share falls by more than 10 points, or residues per round rise by more than 50 pct, from 5 -> 10 or 10 -> 15
- arm 15's box samples stay under both thresholds and it still lands fewer fixes per hour than arm 10

## TESTS
None in code. The evidence is an experiment node under this hypothesis carrying, per arm: start / end timestamps, the
merged round ids, each round's final verify_*.json verdict, the /proc samples log, and the rule's arithmetic.

## FILE SCOPE
the experiment node + its samples log under datasets/swarm-size/ · DE's card · the de_live_parents cell (the arm moves ONLY there)

## CEILING
pi-free parents and kids (0 USD) · kids <= spawn.parent_max_kids · each arm >= 2 h AND >= 6 finished rounds, whichever is later ·
arm order 10 -> 5 -> 15 (throughput first; the order confound -- queue items differ over time -- is named in the verdict) ·
the ceiling 16 only while loadavg1 < 16 AND io PSI some avg60 < 50 (belam 02:59Z)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by thought-master 03:0xZ 09-27 on the OWNER GO relayed by belam 02:59Z, verbatim from that [decision]: "Swarm-size test (owner): mint it on your board -- same queue, parents 5 / 10 / 15, measure fixes landed per hour + mur quality (accept share, residues per round, demotes)." and "DE live-parent cap in steps 8 -> 12 now -> 16 only while load < 16 AND io PSI some avg60 < 50 (today: load 16.9, io60 40-70 -- CPU/IO bind before RAM does)". Why this shape: the cap had no cell (an order-level 8), so the arm moves into values.local_maxxing.de_live_parents (config-max); arm order 10 -> 5 -> 15 keeps throughput near the GO's 12 first, and the rule is pre-registered here before any arm runs so the size is picked by the numbers, not after them.
<!-- THOUGHT:END -->
