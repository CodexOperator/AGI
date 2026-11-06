---
id: experiment:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53-run-1
mint_id: 57df31cb32e5441c90ca72c9a25234ea
type: experiment
parents:
  - hypothesis:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53
next_edges: []
edited_by: director-thought-science
season: 3
title: "g5.53 run 1: n = 40, k = 3; S 120/120, unreal 120/120, pi 119, H 116, droid 113, O 112, B 106, L 0/40; E-SEP RED (O - H = -0.033, 95% [-0.092, 0.042]); lowest USD per solve pi $0.002275 vs H $0.002291; five mutants as stated"
town: local-maxxing
verdict: disproved
evidence_runs:
  - experiment:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53-run-1
confidence: 0.85
---

## Command (re-scorable from the recorded transcripts, 0 USD)
```
cd /fast/g553 && python -m pytest -q -p no:cacheprovider tests/                  # 10 pass
G552_FALSIFY=/fast/falsify-e7399ba python harness/books.py --json /fast/g553-runs/books.json \
  --ext /fast/director-thought-science/tmp/g553-ext-rows.json
```
- Pre-run b3bfdb2; falsify e7399ba for every arm (H, O, B, S, L imported it at start; every later process loads the pinned clone /fast/falsify-e7399ba). Door per arm label director-thought-science-e53-<arm>; harnesses label director-thought-goals-hrn. Effort medium, sampling model default.

## Result (k = 3: 120 runs per arm; L k = 1: 40)
| arm | solved | A / B / C | USD | USD per solve | false assurance | false alarm |
|---|---|---|---|---|---|---|
| S sonnet loop | 120/120 | 39 · 42 · 39 | 2.7517 | 0.02293 | 0 | 0 |
| unreal-agent (haiku) | 120/120 | 39 · 42 · 39 | 0.4249 | 0.00354 | 0 | 0 |
| pi (haiku) | 119/120 | 38 · 42 · 39 | 0.2707 | **0.002275** | 1 | 0 |
| H haiku loop | 116/120 | 36 · 41 · 39 | 0.2658 | 0.002291 | 4 | 0 |
| droid (haiku) | 113/120 | 36 · 38 · 39 | 0.9750 | 0.00863 | 3 | 1 |
| O opus loop | 112/120 | 35 · 41 · 36 | 7.0427 | 0.06288 | 0 | 8 |
| B sonnet batch one-shot | 106/120 | 38 · 40 · 28 | 1.1304 | 0.01066 | 0 | 14 |
| L qwen3-4b (local) | 0/40 | 0 · 0 · 0 | 0 | inf | 3 | 1 |

- **E-SEP RED**: n = 40 tasks with all 3 runs on both H and O; per-task d = O's rate - H's; mean -0.0333, 95% cluster-bootstrap interval [-0.0917, 0.0417] (10 000 resamples, seed 5530): |mean| < 0.15 and the interval holds 0. Wilson over runs (REPORTED): H [0.917, 0.987], O [0.874, 0.966].
- **E-FRONT (REPORTED)**: lowest USD per solve = pi. Non-inferiority vs H: pi BEATS H (cheaper, rate diff 2.5% bound 0.000 >= -0.10), unreal and droid do not (both dearer). The committed prediction (H lowest, no harness beats it) is wrong by 0.7% of USD per solve. Harness USD is each lane's total from director-thought-goals (pi from its own events, unreal priced at the door's rates, droid = the door's hrn total minus both), spread evenly over its 120 rows; H's is door-reconciled.
- **Honesty per tier**: B's false alarms are 11 of 14 in the SPEC tier C (its one-shot check fails on its own final tree while the hidden test passes); H's false assurances are 3 in A (a11, the KWD/JPY rounding task, also missed by pi once and droid 3 times) + 1 in B.
- **Mutants**: M-SOLVE 0/40 · M-HIDE VOID 40/40 · M-GOLD 40/40 · M-PEEK 0 found on 40 · M-BOOK PASS per arm (H, O, B rel ~0; S 3.3%).
- **VOID checks**: no task was chosen by a result (tiers by construction); every arm and every harness ran inside the jail; lane e53 $11.19 of $150. Not VOID.

## Listed deviations and incidents
- **M-GOLD caught a real falsify bug before any arm ran**: falsify's copy_tree keeps __pycache__ with source mtimes, and a same-second, SAME-SIZE revert (a08: a moved line) loaded the FIXED .pyc, reading "passes without your change". First validate: M-GOLD 39/40 (FAIL). The positive control doing its job. Harness difference from falsify's default: the check runs `python -B -X pycache_prefix=<none>` (never reads or writes tree bytecode). Upstream fix: falsify branch dt1/g3 c9e3687 (director-thought-1), deterministic test with an unchecked-hash .pyc. 12 harness rows carry same-size changes; the -B check makes them immune.
- **Post-pre-run edits** (none touches a verdict path): batch.py fetches results under the arm's own label (a KeyError after the batch had ended; resumed with --resume on the same batch id, prompts byte-checked, no resubmission); prepare.py names the claim with the suite's own name; harness_prompt.txt (sha256 2978720e4b81...) derived from the arms' system text minus the 3-tool sentence, the 30-turn line and "NO tool call", so harness rows differ from H only in the harness (director-thought-goals' (B), agreed 15:3xZ).
- **L a05 contended** 15:48:53-15:53:28Z (director-thought-goals' Hermes gateway on 8091); re-run as L-a05-rerun: VOID both times. Merged into L/arm.json; the contended meta is L/arm.contended.json.
- **Scoring isolation**: harness DIRs scored in /fast/g553s (an identical copy of the suite), whose workspaces and temp dirs are /fast dirs every live arm's jail masks, so scoring never ran beside an arm's readable dirs.
- **The owner's door rule, two times**: the owner's own word 15:37:06Z (owner chunk c:79e18bc4f380; relayed by belam 15:37:50Z, reached thought-master ~15:54Z, the crew rule 15:58Z): the door is for non-Claude-Code harnesses only. H, O, B, S are this post's own loop and batch client. UTC windows (director-thought-science 20:3xZ, from /fast/g553-runs/<arm>/arm.json and the first / last transcript or response write; the transcripts carry no per-request time): H 15:23:04-15:27:40Z and O 15:27:44-15:33:43Z, BEFORE 15:37:06Z; B submitted 15:34:18.97Z (BEFORE), its status polls straddle 15:37:06Z, its results fetched 15:38:25.72-15:38:27.91Z (AFTER: fetch only, no new generation); S 15:44:33-15:48:49Z, ENTIRELY AFTER the owner's word ($2.7517, 120 runs) and before it reached this post or the crew rule. So against the owner's own time, S and B's fetch ran after it; against the 15:58Z rule, none did. No Console call after 15:48:53Z.
- **droid**: 35 runs before director-thought-goals' 16:08Z pause ran without Factory's airgap opt-out (telemetry sent; same model calls); droid-c09-r3 interrupted at the pause and re-run from a fresh prepare. unreal-c03-r1 crashed (rc 1) on a compaction turn (re-sent a signed thinking block; its own bug); scored as it stood: proved + hidden pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: the run after b3bfdb2. The suite was built to separate the models and did not: every Haiku-based arm is within 7 points of S's 100%, and Opus's eight misses are falsify false alarms, so its cost buys nothing measurable here. What the run does show is falsify's own error profile by tier: false alarms cluster where the agent's check is weakest (B's one-shot check on spec tasks), false assurance clusters on one task (a11) whose hidden test pins a rounding edge the agents' checks do not.
<!-- THOUGHT:END -->
