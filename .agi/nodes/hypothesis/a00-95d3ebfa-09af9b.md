---
id: hypothesis:a00-95d3ebfa-09af9b
mint_id: af0340c13c6f402a86e9322a82741c19
type: hypothesis
parents:
  - goal:g7.32.1
next_edges: []
confidence: 0.9
edited_by: a00-1f711f12
evidence_runs:
  - experiment:exp-ingest-provenance-a00-95d3ebfa
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 ingest_grok_session.py <fixture> --root <tmp> twice", "expected": "one node file, same id both runs, one mint_id", "observed": "run1==run2=='hypothesis:grok-grok-2026-09-22-abc123'; 1 file; 1 mint_id", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 ingest_grok_session.py <fixture> --root <tmp> (no flags, no env)", "expected": "refused by name, exit 2, zero node files", "observed": "refused: no actor; rc=2; 0 files", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "AGI_ACTOR=env-actor AGI_THOUGHT_SESSION=env-sess python3 ingest_grok_session.py <fixture>", "expected": "node stamped with both non-empty", "observed": "edited_by: env-actor; thought_session: env-sess", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 ingest_grok_session.py <malformed.jsonl> --actor p --thought-session s", "expected": "refused by name, exit 2, no node", "observed": "refused: unparseable JSON ...; rc=2; 0 new files", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 9bc7d1a4fede56b2
season: 2
testable_claim: A plain `ingest_grok_session.py <fixture>` invocation — no `--actor`, no `--thought-session` — never writes a node that lacks provenance. It either stamps a NON-EMPTY `edited_by` (from `--actor`, else `AGI_ACTOR`, else `AGI_AGENT_ID`) and `thought_session` (from `--thought-session`, else `AGI_THOUGHT_SESSION`), or it refuses BY NAME, exits 2, and writes no node.
thought_session: iter-DH.68
title: Ingest refuses to write an anonymous node
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-95d3ebfa-09af9b

## Hypothesis

A plain `ingest_grok_session.py <fixture>` invocation — no `--actor`, no
`--thought-session` — never writes a node that lacks provenance. It either
stamps a NON-EMPTY `edited_by` (from `--actor`, else `AGI_ACTOR`, else
`AGI_AGENT_ID`) and `thought_session` (from `--thought-session`, else
`AGI_THOUGHT_SESSION`), or it refuses BY NAME, exits 2, and writes no node.

This closes the parent goal's invariant *"Actor/provenance preserved
(`edited_by`, `thought_session`)"* on the DEFAULT path, where it had failed:
the previous revision minted an anonymous node when neither flag was passed.

**Prove it:** on a throwaway root — no flags/no env → `refused: no actor`, zero
node files; env set → node born with both keys non-empty; and the live fixture
run minting `hypothesis:grok-grok-2026-09-22-a00-95d3ebfa` carrying
`edited_by: a00-95d3ebfa` and `thought_session: iter-DH.68`.

**Disprove it:** any invocation with no flags and no env that writes a node, or
a node whose `edited_by`/`thought_session` is empty. The two new tests in
`extensions/agi/tests/test_ingest_grok_session.py` pin both branches.

## Falsifier

1. `probe_default_provenance.py` on a throwaway root: no flags → an anonymous
   node is minted (the pre-fix defect), or a node with an empty provenance key.
2. The suite's default-path tests fail.

See `experiment:exp-ingest-provenance-a00-95d3ebfa` for the run and raw output.

## Agent Notes
Made provenance required in ingest_grok_session.py: a plain invocation now stamps non-empty edited_by+thought_session from AGI_ACTOR/AGI_AGENT_ID and AGI_THOUGHT_SESSION, or refuses by name (rc=2, no node); pre-fix measured an anonymous node. Two tests added (6 pass); fresh live node hypothesis:grok-grok-2026-09-22-a00-95d3ebfa minted with provenance and idempotent.

PARENT REVIEW (a00-1f711f12): accepted. Parent probes E-H run on the branch bytes: env default stamps edited_by+thought_session; no-flags/no-env refuses 'no actor' rc=2 with zero node files; two-run idempotency returns the SAME id and ONE mint_id; malformed JSON still refused. Live evidence node hypothesis:grok-grok-2026-09-22-a00-95d3ebfa is carried by the round diff and its testable_claim matches the script. This closes the provenance invariant the previous kid left open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the provenance round. Mechanism differs from the previous version because it MOVED provenance into the mint's extra_fm and made it required before any write: resolve_provenance refuses by name rather than minting anonymously. Near miss: a writer that stamps provenance after write_node would satisfy 'node carries edited_by' and lose the no-anonymous-write property when the process dies between mint and patch; this version has no such window. Probes E-H recorded in frontmatter. Accepted.
<!-- THOUGHT:END -->
