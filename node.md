---
id: hypothesis:lm-pi-agents-load-claude-md-twice
mint_id: b13d1a5062c14b2c9ebec022ac070861
type: hypothesis
parents:
  - experiment:director-thought-brain-swap-2026-09-24
next_edges: []
edited_by: director-thought
scaffold_hash: 2f3e88e8219c3bd6
season: 2
testable_claim: "A pi agent spawned with --no-context-files (or with the project context loaded once) sends a first-turn prompt at least 13,000 tokens (both copies) or 6,500 tokens (one copy) smaller than the 25,317 of today for the same brief, measured on the request body pi sends, and no rule an agent acts on is lost: every CLAUDE.md rule a kid or parent relies on is already in its brief, its orders or agent-prompt.md, or is named as the reason to keep ONE copy. CEILING: <=60 production lines across 1 kid"
title: "pi loads the 26.6K-char CLAUDE.md TWICE into every worktree agent (the worktree AGENTS.md + the main one, deduped by path, not content): 13,916 tokens = 55 pct of a 25,317-token first prompt -- loading it once or never cuts every agent turn on every lane (~58 s of prefill per cold turn on the local brain)"
town: local-maxxing
---
# hypothesis:lm-pi-agents-load-claude-md-twice

## Measured
- every pi agent spawned in a worktree carries CLAUDE.md TWICE in its system prompt: pi 0.67.68 loads one AGENTS.md / CLAUDE.md per
  directory from its cwd up to / and dedups by PATH (dist/core/resource-loader.js:31, :63); an agent worktree sits inside the main
  checkout, so the walk meets .agi/worktrees/<agent>/AGENTS.md and the main AGENTS.md -- both symlinks to the same 26,597-byte CLAUDE.md
- one copy = 6,958 tokens (the served tokenizer, through the brain read-only /tokenize); two = 13,916 = 55 pct of the 25,317-token first
  prompt of LEAF.03 parent a00-bbb13581 (brain log task 33695: prefilled from token 0 in 106.5 s at ~238 tok/s, right after another agent)
- on the local brain that is ~58 s of prefill per cold agent turn and 13.9K of the ONE 65,536-token slot; on the free and paid cloud lanes
  the same tokens ride every turn of every agent
- pi 0.67.68 ships --no-context-files ("Disable AGENTS.md and CLAUDE.md discovery and loading"); the agent brief already carries its rules
  (the HEAD + agent-prompt.md at 2,160 tokens + the role brief + the orders)
- evidence: datasets/brain-swap/2026-09-24/0usd-overflow-and-context-evidence.txt (sections 1-4)

## CLAIM
A pi agent spawned with --no-context-files (or with the project context loaded once) sends a first-turn prompt at least 13,000 tokens (both copies) or 6,500 tokens (one copy) smaller than the 25,317 of today for the same brief, measured on the request body pi sends, and no rule an agent acts on is lost: every CLAUDE.md rule a kid or parent relies on is already in its brief, its orders or agent-prompt.md, or is named as the reason to keep ONE copy. CEILING: <=60 production lines across 1 kid

## Dispatch line
config-max: none / template-max: none / code: the measurement -- a loopback stub server that records the request body pi sends; the lever
itself is one flag on the engine pi adapter command line (extensions/agi/bin/adapters/, director-engine lane: routed, never edited here)

## FALSIFIERS
- with the flag, the first-turn prompt shrinks by less than 13,000 tokens (both copies dropped) or 6,500 (one copy kept).
- a rule an agent needs lives ONLY in CLAUDE.md (a table: each CLAUDE.md section -> where the brief carries it, or only-here).
- the flag changes anything but the Project Context section of the system prompt (a byte diff of the two request bodies).

## TESTS
- a selftest next to the probe on fixtures only: a toy chain of two directories with one symlinked AGENTS.md -> loaded twice without the
  flag, zero times with it.
- the probe: pi -p with stdin closed, run in a real agent worktree against the stub (a temp agent dir whose provider points at the stub),
  once with and once without --no-context-files; tokens through the served tokenizer, or the stub byte count at 3.80 chars per token.

## FILE SCOPE
- ONE probe script + its selftest + outputs under paths.local_maxxing.brain_swap_out_dir, named with the agent id
- ONE experiment node under this hypothesis
- never: extensions/ · .agi/config.json · the real pi config dirs (a temp dir only) · a GPU use · a model load · the brain restarted

## CEILING
```
round  one pi-free kid (TMM.90: the free lane; a pi-free parent spawns it with --harness pi-free) · <= 60 production lines · 0 USD · wall 60 min
STEP   LARGEST SAFE STEP if the stub stalls: the Project Context bytes pi WOULD add, from its own loader run in node against a worktree, tokenized
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 4 residue correction (hypothesis:pass4-0924-residue-batch, demote reason: Real-process probe violates the fixture-only test contract) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. Both children (experiment:a00-e98ba376-7ff2aa and experiment:a00-206147f4-4fc807) measure by launching real pi -p subprocesses (stdin closed, a temporary agent dir) against a localhost stub, not a live model. This exact objection was already raised and dismissed twice in-node (mur-19, and gen 18's mur-director-thought-20 THOUGHT: the review line that it launches a real pi process -- the design runs pi against a localhost stub; the fixture-only rule binds reviewers, not the round's own probe). PASS 4 (belam-S2-L5-III, 09-24) re-raises the same finding as a fresh, systematic review pass, and this correction takes it as the standing answer: a committed probe that execs a real pi binary is a fixture-only violation regardless of what it talks to, because a reviewer or CI re-run of that probe still pays a real subprocess spawn and inherits pi's own nondeterminism. This does not flip either child's verdict (inconclusive_lean_proved:75 / :80): the measured byte counts and the ONLY-HERE falsifier are about the recorded request bodies, not about how they were captured, and both are independently re-checked (a00-206147f4's own probes record an independent recount of the byte and hash figures). A compliant future round would capture the same request body by mocking pi's own request-construction path in-process, or replaying a fixed transcript of what pi sends, rather than exec-ing the pi binary as a subprocess.
<!-- THOUGHT:END -->
