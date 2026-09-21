---
id: hypothesis:l2w6-telemetry-rollup
mint_id: 8ab76841dcd546f8adbdca54ebb790c1
type: hypothesis
parents:
  - goal:g16
next_edges: experiment:a00-6856367d-7b307d
edited_by: ubuntu
scaffold_hash: c6fcbfd659d755ea
season: 1
testable_claim: A roll-up walks each report node's parents field to sum tokens_in/out, cost_usd and accepted_bytes from its descendant kid nodes, attaches the sums to the report (outcome sums its loop's kid nodes, bigger_outcome its LT goal, overview its season), and prints cost-per-aligned-outcome as a ranking number, never read by any agent choosing what to do
title: L2w6 telemetry rollup
---
# hypothesis:l2w6-telemetry-rollup

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/telemetry_rollup.py (new), plus tests. Design: .agi/context/season-ladder-and-morals-brief.md section 5. l2w2-telemetry-stamps (landed round 6) stamps tokens_in, tokens_out, cost_usd, telemetry_source, accepted_bytes on individual kid nodes at done/acceptance -- read that node before starting, do not restamp per-node fields, this hypothesis is the roll-up ONE LEVEL UP only. WALK: for a given report node (outcome, bigger_outcome, or overview), find its descendant kid/experiment nodes for the plan it judges (outcome walks its subgoal's chain nodes for the loop; bigger_outcome walks its long-term goal's outcomes; overview walks its season's bigger_outcomes) and sum their tokens_in, tokens_out, cost_usd, accepted_bytes fields where present, skipping nodes missing them (do not treat missing as zero silently -- count how many were skipped and report it). WRITE: attach the sums to the report node via write.py set (tokens_in_total, tokens_out_total, cost_usd_total, accepted_bytes_total, telemetry_nodes_summed, telemetry_nodes_skipped). RATIOS: bytes_per_token = accepted_bytes_total / (tokens_in_total+tokens_out_total) when nonzero; bytes_per_dollar = accepted_bytes_total / cost_usd_total when nonzero; both printed by a season.py status --cost flag or a new telemetry_rollup.py report subcommand (your call, name it in the experiment) beside aligned-outcome count from season.py judge records. cost_per_aligned_outcome = cost_usd_total / count(outcomes with alignment=aligned) -- the one ranking number the brief names; print it, never gate on it, never let an agent read it to pick work. VERIFY: red-first test with fabricated kid nodes carrying telemetry fields under a temp graph; on this repo run the roll-up on one real outcome from L2 and paste the actual sums (they may be near-zero if telemetry_source was mostly unavailable -- that is an honest first data point, say so). Suite green via commands.py run tests. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list of node ids (pass --evidence-runs), every verify command with its actual output in the body. New engine file goes directly under extensions/agi/bin/. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.