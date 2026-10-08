---
id: hypothesis:a00-373ec687-7bb58a
mint_id: 9bbc19220d224e7db4bf45a8bbcf562b
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 8f714deeda819771
season: 1
testable_claim: "Given a dispatch configuration with distinct parent and kid model settings (e.g., `harnesses.parent.models.parent = \"anthropic/claude-sonnet-4\"` and `harnesses.kid.models.parent = \"google/gemini-3-flash\"`), a spawned dispatch process for the parent tier carries its model identifier in the process launch command — not in the LLM call's runtime payload — and is verifiable by `ps`-level inspection of the spawned process tree. This verification is structural, not statistical: either the command contains the correct model switch or it does not."
thought_session: season
title: Model tiers verified by command inspection — the fifth falsifier clause of g4.8
verdict: pending
---
# hypothesis:a00-373ec687-7bb58a

## Hypothesis

**Model tier enforcement through command inspection — spawned dispatch commands for parent and kid tiers carry distinct model identifiers, and a tier mismatch (parent silently running the kid model) is detectable by inspecting the spawned process's argv, not by inspecting the output. Without this check, a parent that falls back to the kid model passes every other falsifier clause while destroying the economic case for tiering.**

### Testable claim

Given a dispatch configuration with distinct parent and kid model settings (e.g., `harnesses.parent.models.parent = "anthropic/claude-sonnet-4"` and `harnesses.kid.models.parent = "google/gemini-3-flash"`), a spawned dispatch process for the parent tier carries its model identifier in the process launch command — not in the LLM call's runtime payload — and is verifiable by `ps`-level inspection of the spawned process tree. This verification is structural, not statistical: either the command contains the correct model switch or it does not.

Formally: for any dispatch run with `--tier parent`, the spawned command must contain the parent-tier model identifier at launch time. For any `--tier kid`, it must contain the kid-tier identifier. A run where a parent-tier dispatch contains the kid-tier identifier (or no tier-specific identifier at all) is a *tier escape* — it is verifiably running the wrong model, and must be flagged without examining any LLM output.

### What would prove it

An experiment with two configurations:

**Config A (correct tiering):**
1. Dispatch a parent-tier agent against `goal:g4.8` with distinct model configs: parent model = Claude Sonnet, kid model = Gemini Flash.
2. Capture the spawned command (`ps aux | grep dispatch` + `cat /proc/$PID/cmdline`).
3. Verify the spawned command contains the parent model identifier (`claude-sonnet-4`), not the kid model identifier (`gemini-3-flash`).
4. Separately, verify that a kid spawned from that parent also contains the kid model identifier, not the parent one.
5. The relative order of parent and kid spawns must not matter — a kid spawned first must carry kid model, a parent spawned first must carry parent model.

**Config B (tier escape — deliberately misconfigured):**
1. Set the parent-tier config to use the kid model (removing the distinct config, simulating a fallback).
2. Dispatch a parent-tier agent.
3. Inspect the spawned command: it carries the kid model identifier (the only one available).
4. The experiment **passes** when it correctly identifies this as a tier escape — meaning the inspection method is sensitive enough to catch the mismatch.

**Proved if:**
- Config A: parent process argv contains parent model; kid process argv contains kid model. Never mixed. Verified by `ps` + `proc/pid/cmdline` reads.
- Config B: inspection detects the tier escape and flags it.
- The inspection is deterministic (no sampling, no averaging — either the flag is present or it is not).

The second config is the critical test: it proves the inspection is not a tautology ("of course the model flag is there, it's the only one") by demonstrating that the same inspection *also* detects when the flag is wrong.

### What would disprove it

- The spawned command does not carry any model identifier that survives to `ps`-level inspection — the model is set inside the dispatch process at runtime (e.g., via environment variable or config read) and is not visible in argv → the inspection method cannot verify the tier from the outside.
- A parent-tier process with a correct model flag in argv can still hand-pick a kid model for the actual LLM call — the argv flag is cosmetic, not binding, and inspection of the command is not inspection of the call → proving the claim meaningless for actual tier enforcement.
- Both Config A and Config B produce identical argv (model not set at launch, resolved at call time) → no tier separation is visible at the process level.
- The `ps`-level inspection produces false positives: a parent running the correct model is flagged as wrong because a shared default leaks into argv.
- Config A cannot be produced with live dispatch (dispatch crashes before spawning when parent and kid models differ) — the tiering is untestable because the harness does not actually support distinct models.

### Relation to g4.8

Directly tests the **model tier verification clause** (the last sentence of g4.8's falsifier, which names it as the 5th sub-condition): *"Model tiering is verified by inspection of the spawned commands, not assumed — a parent silently running on the kid model would pass every other clause."*

This clause exists because the other four falsifier clauses — no collisions, process bound, parent review gate, sub-linear delegator spend — are all *model-agnostic*. A parent running on the cheap model could pass all four while producing lower-quality output, silently destroying `goal:g4.8`'s objective function ("functional output per token spent"). The objective function requires that the parent runs on the expensive model and the kid runs on the cheap one — and that this is *enforced*, not just assumed.

**Why no existing sibling hypothesis covers this:**

| Sibling | Covers |
|---|---|
| `a03-280a21b7-6d6841` | Clause 1: no file collisions |
| `a00-8d238338-ec4dff`, `shared-lease-bounds-the-tree` | Clause 2: concurrency bound |
| `a00-07b2223d-b21977`, `a05-bc3ad321-131bbc` | Clause 3: parent review gate |
| `a00-003fffb0-388249`, `a01-2a74553c-ae68b4`, `a02-02affc6b-dc0c54`, `a04-7bb380cb-2a7d9b`, `a06-4714fa2c-c75aec`, `a07-1850cc5d-39f57c` | Clause 4: sub-linear delegator spend |
| `a00-dec78137-07daab` | Prerequisite: target diversity for clause 4 value |
| `a00-a54f694b-b20b78` | Parent review (mistyped, is actually a review node) |
| **this node** | **Model tier verification — the remaining sub-condition of the falsifier** |

The falsifier says "Requirements, all four of which must hold" — but the paragraph immediately adds the tier verification as a co-equal gate. A falsifier with an unmentioned fifth clause that in practice invalidates the run has the same weight as the four numbered ones, and the falsifier's own text says so.

### Why command inspection and not runtime logging

Command inspection (`ps` + `/proc/$PID/cmdline`) has one property that runtime logging does not: it is **external**. It does not require the dispatch process to cooperate, instrument its calls, or survive a crash. It works on a process that is actively running, has crashed, or is hung. A log statement inside the dispatch that prints "running model X" is a self-report and can lie without being caught; the OS-level argv is the process's public launch contract and cannot be forged by the process itself (it must be set at `execve(2)` time). This is the property g4.8 requires: verification that does not trust the process to self-report.

### Caveat

The experiment requires actual live dispatch with distinct parent/kid models configured. If `dispatch.py` or `pi_adapter.model_args` raises an error when models differ (the guard `goal:g4.8`'s THOUGHT block mentions), Config A may fail at the spawn step — which itself is evidence ("tiering is unimplemented") but proves the wrong hypothesis. The hypothesis is about *detectability given that tiering works*, not about whether tiering works at all. If dispatch cannot spawn distinct models, the hypothesis is unfalsifiable without first fixing the harness.

## Agent Notes
Model tier verification hypothesis — fills the 5th sub-condition of g4.8 falsifier (model tiering verified by command inspection). No sibling covers this gap. Claims spawned dispatch process argv carries tier-specific model identifier, making tier escape detectable by ps-level inspection without trusting self-reports.


## Agent Notes
Model tier verification hypothesis — fills the 5th sub-condition of g4.8 falsifier (model tiering verifiable by command inspection). No sibling hypothesis covers this. Claims spawned dispatch process argv carries tier-specific model identifier, detectable by ps-level inspection without trusting process self-reports.