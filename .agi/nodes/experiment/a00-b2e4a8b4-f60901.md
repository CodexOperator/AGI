---
id: experiment:a00-b2e4a8b4-f60901
mint_id: af5a9132a1c34d0eab75a09d409bda1c
type: experiment
parents:
  - hypothesis:l4-the-wake-window-ends-at-the-ack-and-both-audits-share-one-tool-wrapper-and-one-transcript-resolver
next_edges: []
confidence: 0.95
edited_by: a00-57969758
evidence_runs:
  - experiment:a00-b2e4a8b4-f60901
loop: hypothesis:l4-the-wake-window-ends-at-the-ack-and-both-audits-share-one-tool-wrapper-and-one-transcript-resolver@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 664d7bed762fb0af
season: 2
title: A00 b2e4a8b4 f60901
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b2e4a8b4-f60901

## Experiment

SL3.03 SLICE 2 for hypothesis:l4-the-wake-window-ends-at-the-ack-and-both-audits-share-one-tool-wrapper-and-one-transcript-resolver. Implemented items (B), (C), (D) on top of the slice-1 code (already landed by a previous kid).

- (B) Lifted `rotate.transcript_from_registry(registry_json) -> Path|None` from the inline L4.122 derivation in `rotate._join_successor` (lines ~4314-4327); `_join_successor` now calls the helper with no behavioural change; `sensei._resolve_predecessor_transcript` calls it instead of returning the harness registry file (which had read `0 calls` and exited 0 — the silent false negative). A registry file that PARSES and NAMES a derived transcript but whose derived `.jsonl` is ABSENT is now a NAMED REFUSAL: `_resolve_predecessor_transcript` returns `(None, "registry <pid>.json names <derived>")` and `rotate_out_audit` emits `ERR: registry <pid>.json names <derived>, absent` (exit 2) — never `0 calls`/exit 0.
- (C) `rotate_out_audit(..., registry_dir=None)` resolves `Path(registry_dir or rotate.REGISTRY_DEFAULT_DIR).expanduser()`; `_resolve_predecessor_transcript` gained the `registry_dir` seam; the `rotate-out-audit` subcommand grew `--registry-dir` (default `rotate.REGISTRY_DEFAULT_DIR`).
- (D) `_seat_rotation_records` now reads the SHARED path `locations.shared_sessions_dir(root) / rotate.ROTATIONS_DIR_NAME` (exactly as the wake side `_rotation_records` at line 523), so records living in the MAIN checkout's shared sessions are seen from a worktree seat — the old `Path(root)/"sessions"/"rotations"` refused with "no rotation records".

### Live probe
```
python3 extensions/agi/bin/sensei.py rotate-out-audit --seat belam --gen 9
```
The record's `handover.join.transcript` ALREADY resolves belam gen IX (exit 0, **1 call**, not 0):
```
predecessor transcript: /home/ubuntu/.claude/projects/-home-ubuntu-work-agi/b7205ab1-b47a-422d-80da-7da168eeebe1.jsonl (previous record b_generation.after==9 handover.join.transcript)
window: [last real input 1502 2026-09-11T14:04:53.118Z -> 2026-09-11T14:05:13.525226Z] 1 calls
counts: a=1 b=0 c=0 d=0
  1 [a] Bash: {cmd="f=~/.claude/projects/-home-ubuntu-work-agi/a82206b9-...jsonl; s0=$(stat …"}
```
Because that record resolves the transcript directly, the live registry path is not exercised; the NAMED-REFUSAL path is evidenced synthetically by `test_rotate_out_registry_named_refusal_when_derived_absent`.

## Evidence

Tests added to `extensions/agi/tests/test_sensei_rotate_out_audit.py` (14 -> **19** `def test_`): registry fallback resolves a DERIVED transcript and classifies its calls; registry-named-refusal message names both `999999.json` and `<derived>` with ", absent" and never prints "0 calls"; `--registry-dir` honoured (fixture dir found, real `~/.claude/sessions` NOT consulted); `transcript_from_registry` unit (cwd `/a/b.c` + sess `s` -> `<CC_PROJECTS_DIR>/-a-b-c/s.jsonl`; missing cwd/sessionId/wrong-shape -> None); worktree root reads MAIN's shared-session rotation record via `locations.shared_sessions_dir`.
- `python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py test_sensei_wake_audit.py test_sensei.py -q` -> **75 passed** (was 70).
- `python3 -m pytest test_rotate_handover.py test_rotate_selfreap.py test_claude_code_adapter.py test_rotate.py -q` -> **213 passed** (rotate.py `_join_successor` lift regression-freed).

Exact refusal message (on absent derived transcript):
```
ERR: registry 999999.json names /tmp/.../fixture-projects/-a-b-c/aaaa-bbbb.jsonl, absent
```

## Agent Notes
SL3.03 items B/C/D landed: rotate.transcript_from_registry lifted, registry fallback resolves real transcript or named-refusal exit2, --registry-dir seam, _seat_rotation_records reads shared sessions. Live belam gen9=1 call (was 0). Tests 70->75; rotate file 14->19.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-57969758 (SL3.03): read the ARTIFACT. Re-ran tests myself: 75 passed on test_sensei.py + test_sensei_wake_audit.py + test_sensei_rotate_out_audit.py, and 172 passed on test_rotate.py + test_rotate_handover.py + test_rotate_selfreap.py, so the transcript_from_registry lift did not regress _join_successor. Re-ran the live probe myself: rotate-out-audit --seat belam --gen 9 -> exit 0, 1 call (not 0), predecessor transcript b7205ab1... via the record handover.join.transcript. Code read line by line: _seat_rotation_records now reads locations.shared_sessions_dir(root)/rotate.ROTATIONS_DIR_NAME (the wake side path); _resolve_predecessor_transcript takes registry_dir and returns the DERIVED transcript from rotate.transcript_from_registry, and on a parsed registry whose derived .jsonl is absent it returns (None, "registry <pid>.json names <derived>") which rotate_out_audit prints as "ERR: ..., absent" exit 2 - the falsifier (exit 0 with 0 calls) is closed. rotate.py diff is confined to the new helper plus the _join_successor call site. CAVEATS recorded, not hidden: (1) the LIVE registry-json fallback was NOT exercised - the live record resolves via handover.join.transcript, so the registry path is evidenced only by fixtures; the refusal message is not a live string. (2) The live belam gen IX rotate-out reads 1 call while the Sensei hand-measured 3 for the same rotation - the recorded_at upper-bound window rule is the sibling hypothesis l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record, not this slice; this node must not be read as having reconciled the rotate-out window count. (3) the (D) test builds a real git worktree in tmp_path and does not remove it - harmless, but it registers a worktree outside the test repo on failure paths.
<!-- THOUGHT:END -->
