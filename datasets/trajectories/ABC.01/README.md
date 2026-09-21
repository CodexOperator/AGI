# ABC.01 trajectories

Parent + kid tool-call trajectories (trajectory.jsonl) and agent metadata (agent.json) for the ABC.01 round (Bonsai2-27B A/B/C HumanEval coding eval), landed per the standing datasets/ landing rule before the round's worktrees were removed.

**NOT landed: raw output.log.** Measured 158MB (parent) / 61MB (kid1) / 52MB (kid2) -- sampled structure shows ~99% of lines are `message_update` token-by-token streaming deltas, already captured structurally in trajectory.jsonl (one entry per real tool call + result) at 349KB/118KB/97KB. Flagged to thought-master rather than committing ~270MB of near-duplicate streaming noise; using trajectory.jsonl as the landed trajectory per that reasoning.

| agent | role | verdict | mur |
|---|---|---|---|
| a00-944318b2 | parent | harvest accepted=2 demoted=0 failed=0 | accept_with_residue |
| a00-6ce9cb00 | kid1 | inconclusive_lean_proved:70 | accept_with_residue |
| a00-bb10233d | kid2 | disproved conf=0.9 | accept_with_residue |

## Scrub (v2, span-based)

Patterns: dotted/hex/decimal-encoded IPs, sk-or- keys, OPENROUTER_*KEY mentions, hex>=40 (ed25519-style keys), emails. Spans collected directly from the source text (never a derived token list) and redacted by exact position, so a short flagged span can never corrupt an unrelated longer run that happens to share a prefix/suffix -- the v1 approach (global string-replace per token) had exactly that bug, caught in review (an 8-char truncated-sha256 hash fragment coincidentally decoded as an IP and clobbered the prefix of an unrelated 16-char truncated hash elsewhere; benign content in that instance, but the mechanism was wrong). Redaction counts per agent in each `label.json`.

Total redactions across the round: {"ip_decimal": 381, "ip_hex": 1070, "hex40_key": 50, "ip_dotted": 109}
