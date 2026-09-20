---
id: verdict:grok-bot-adapter-carry-closes-residues-1-3
mint_id: fe72b788c3ea48c1a77b57abf50704d9
type: verdict
parents:
  - experiment:grok-bot-adapter-carried-onto-dt21-tip
next_edges: []
confidence: 0.95
edited_by: a00-05dbe96a
evidence_runs:
  - experiment:grok-bot-adapter-carried-onto-dt21-tip
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 5d0fac34868328c1
season: 2
tags:
  - adapter
  - grok-bot
  - carry
  - verdict
  - g17.14
title: Grok Bot adapter carry closes mur residues 1 and 3; residue 2 build node minted
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-adapter-carry-closes-residues-1-3

## Verdict

**proved** — residues 1 and 3 of
`mur-g17-14-1-dt-20-adapter-1260f8c66-g17-14-2-dt-21-seam-a3d92f501` are
closed on the DT.21 tip; residue 2's build node is minted.

Evidence run: `experiment:grok-bot-adapter-carried-onto-dt21-tip`.

## Evidence

1. **Residue 1 — real-restart test coverage on tip.**
   `extensions/agi/tests/test_grok_bot_adapter.py` carries the g17.14 bytes and
   `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` ends
   `12 passed, 3 skipped`. The restart contract is verified by
   `test_restart_is_a_real_respawn_not_a_stub`,
   `test_restart_returns_the_new_pid_and_stamps_the_record` and
   `test_restart_returns_none_when_popen_fails` — all in the passing set. The
   three skips are the live-config tests, skipped **by name**.

2. **Residue 3 — hermetic live-config tests.** The `live_cfg` fixture calls
   `pytest.skip("harnesses.grok-bot row lands with Belam's config fold (DT.21
   residue 3)")` when the row is absent. The suite is GREEN with skips, never
   red. No non-live test was weakened, and no `harnesses.grok-bot` row was
   authored (Belam's cell).

3. **Residue 2 — graph provenance.**
   `build:bin-adapters-grok-bot-adapter` exists with
   `payload_ref: extensions/agi/bin/adapters/grok_bot_adapter.py` and
   `parents: [mvp:unified-spawn-path]`. The orphaned 162-line file now has its
   canonical file build node.

4. **Carry fidelity.** The adapter sha256 equals the reference
   (`66b7891f...6081c`); `dispatch.py` has zero `grok` hits (`grep -c` → 0,
   exit 1); the REQUIRED-surface probe prints `grok-bot False True`.

## The chain's mvp

The mvp step of `hypothesis → experiment → verdict → mvp → build` is the
already-live **`mvp:unified-spawn-path`** — the design node that specified the
adapter seam this file implements. `build:bin-adapters-grok-bot-adapter` hangs
from it by the `parents: [mvp]` shape `[build].md` requires. No second mvp was
minted: a duplicate would either orphan itself (the build node cannot take two
mvp parents — `max_parents: 2` admits only `[build, goal]`, `[goal, mvp]`,
`[goal, idea]`) or contradict the D4-mandated parent set.

## Confidence

0.95. The only thing outside this run's control is the live config row, which
is deliberately Belam's fold and therefore not evidence this run could fail on.

