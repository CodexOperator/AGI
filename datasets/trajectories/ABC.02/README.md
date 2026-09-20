# ABC.02 trajectories

Parent + kid tool-call trajectories (trajectory.jsonl) and agent metadata (agent.json) for the ABC.02 round (harness re-runnability fix, owner's C2 scale-2 null result, arm A re-run through the fork), landed per the standing datasets/ landing rule before the round's worktrees were removed. Scrubbed with the shared `datasets/tools/scrub.py` (span-based redactor).

**NOT landed: raw output.log** (65MB parent / 21MB kid1) -- same reasoning as ABC.01 (see `datasets/trajectories/ABC.01/README.md`): dominated by token-by-token streaming deltas, already captured structurally in trajectory.jsonl.

| agent | role | verdict | mur |
|---|---|---|---|
| a00-b2deb33c | parent | harvest accepted=1 demoted=0 failed=0 | accept_with_residue |
| a00-c4441397 | kid1 | disproved conf=0.85 | accept_with_residue |

Total redactions across the round: {"ip_decimal": 157, "ip_hex": 627, "hex40_key": 42, "ip_dotted": 49, "email": 2}
