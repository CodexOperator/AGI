---
id: hypothesis:core-sync-0923-residues
mint_id: b16a3090787c4770a9f3c250774fa233
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: belam
scaffold_hash: a5a2d179194861fd
season: 2
testable_claim: "Every residue the 09-23 core sync measured is closed by name: the four engine items (anonymize loopback, pi_bin env test, tty-hangup flake, secrets optional-key FAIL) land with committed tests on the town side, the two core-side test reds and core's g17.14.x dangling parents land on core and arrive at the next sync, and a full suite on the next synced trunk shows 0 of these 7."
title: "Residues of the Prime's core sync 09-23 (core @f655a6714 into the town trunk, 8451055b5): 7 items, 0 caused by the sync (assigned: director-engine; core-side items flagged for grok)"
town: core
---
<!-- BODY:BEGIN -->
# Residues of the Prime's core sync 09-23 (core/season2/main @f655a6714 → local-maxxing/season2/main = 8451055b5)

```
sync ─▶ 145 core commits in · 82 goal ids renumbered by core (mint ids kept) · 8 town goals renumbered to match · 22 nodes' frontmatter remapped
     ─▶ links 3945/0 · GOALS 309 byte-identical · 3964 nodes, 0 duplicate mint ids (trunk 3823 · core 3922)
     ─▶ suite 5937 passed / 5 failed ─▶ 0 caused by the sync (the one sync-caused failure — two THOUGHT blocks in doc:lm-town-trajectory — fixed before landing)
```

| # | residue | where it already fails | owner |
|---|---|---|---|
| R1 | `anonymize` treats loopback `127.0.0.1` as a box identifier (FAIL on a thought-master note re-rendered into GOALS.md) | engine, both sides | director-engine: `anonymize.py box_tokens` skips loopback / link-local |
| R2 | `test_bin_help_smoke[harness_template.py]` — core's new harness_template.py misses the help contract | core tip f655a6714 | core (grok) |
| R3 | `test_brief::test_g15_rule_with_no_project_root_keeps_the_current_fallback` | core tip f655a6714 | core (grok) |
| R4 | `test_adapters::test_pi_bin_env_var_wins_over_config` | BOTH tips (trunk 332d63a0e + core) | director-engine (same family as L1, pi bin precedence) |
| R5 | `test_rotate_launch_wrapper::test_wrapper_tty_hangup_forwards_to_the_child` — fails under full-suite load, passes alone ×2 | flake | director-engine |
| R6 | 37 dangling frontmatter goal refs, all pre-existing: g11.2 ×4 · g8.4 ×4 · g99 ×1 (both sides) · g17.14.1/2/3 ×26 (core's grok-bot mvps: core renumbered g17.14 → g7.25 but not these parents) · g7.33.8 ×2 (the town's G14.14.8, never minted) | both | core for g17.14.x · director-engine for g7.33.8 (mint it or drop the ref) · g11.2/g8.4/g99 = retired-goal refs, retire-or-repoint |
| R7 | verification `secrets` FAILs on an optional-key note (MINIMAX_API_KEY) | engine | director-engine (a note must not fail the check) |

NOT residues: the `crons` check refuses in a linked worktree by design; `bin-suite-fresh` stamps only on an integration branch.

Done when: R1, R4, R5, R7 land with tests (director-engine) · R2, R3, R6(g17.14.x) land on core and arrive at the next sync · one batch mur over the landed rounds returns no demote.

## Agent Notes
assigned: director-engine (owner 01:4xZ 09-21) for R1 R4 R5 R7 and g7.33.8; R2 R3 and g17.14.x are core's (grok), carried here so the next sync can close them.

R8 (owner 07:36Z 09-23 'Separate rows is fine'): per-box Prime rows -- one config:posts Prime row per box (core's belam keeps its row; local-town's Prime gets its own), which needs the engine's seat resolution (rotate / whois / send / key files) to stop assuming one belam row; owner of the work = core's engine bundle goal:g7.33 (parked). Until it lands: each side keeps its own belam row at every sync.
