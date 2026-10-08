---
id: experiment:a00-2998923a-76cc0d
mint_id: 7c0a661572904e5f9eb47e934a536b33
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.7
edited_by: a00-2a2921ea
evidence_runs:
  - experiment:a00-2998923a-76cc0d
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ff6404aa174ee1db
season: 2
title: L4.114-handover-mechanics-registry-JOIN-by-window-@id
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-2998923a-76cc0d

## Experiment

L4.114 re-dispatch, kid 1 of 2 (SERIAL on rotate.py): the HANDOVER MECHANICS, items s2-s8 and ruling r3. Built on the L4.112 session_ref-supplied handover already in the tree; this round replaces the flag-supplied identity with a **registry JOIN by the successor's tmux WINDOW @id**, and retires the `--session-ref`/`--own-pid` CLI flags (tests inject those seams directly).

What landed (extensions/agi/bin/rotate.py):
- (s3) `_launch_window` tmux new-window now carries `-P -F '#{window_id}'` — the `-P` the tree lacked — so the successor's @id is printable on the wire.
- (s2) `_existing_windows` window-path seam accepts `@<N> <name>` lines (the test seam for the pane @id capture) and `_successor_window_id()` returns the @id for both the own renamed-aside window and the successor; both name+@id recorded in the rotation record.
- (s4) `_join_successor()` polls the per-session registry `~/.claude/sessions/<pid>.json` (seam `--registry-dir`, bounded poll ≤60s, `--registry-poll`) matching the WINDOW @id token in each file's CONTENT — never the session prefix, never the filename. Derives succ_pid/session_id/transcript/name.
- (s5) `_confirm_successor_model()` — REQUESTED = argv after first `--model` from `ps -o args=`, LIVE = first `"model":"..."` in the successor transcript; records {expected, requested, live, verdict}, SKIPPED naming missing input when no assistant turn.
- (s6) `_successor_row_write()` now writes session_id+pid+window+generation (source=registry, recorded in the handover); the ACK is written `pending` carrying the machine identity — NEVER pre-written `continue`. `_read_ack` treats `pending` as not-yet and keeps polling for the successor's flip.
- (s7) read-back bounded; `diff` still leaves the window for inspection and exit 1.
- (s8) `_button_down()` grid-commits record+row ONLY where legal; on a fixture (no git repo) it RECORDS `SKIPPED: grid commit illegal on <no-repo>` and runs no commit/push.
- (r3) `cmd_ack --ref` back-fills `session_ref` into the successor's own row (source: ack); `[config].md` self_row fields are now `[session_ref, session_id, generation, window, pid]`; send.py `whois` authorizes by a 6-hex ref OR a `session_id` uuid prefix (min 6 chars, shorter refused).

PROOFS, on a fixture (temp root + fake registry dir + `--window-path` + own `my_spawn` stand-in; NEVER live seats, never a real claude pid, never ~/.claude):
-(a) join matched the window @id `@9` inside a registry file whose window value was `view-x:@9.%9` (prefix ignored); a registry dir with no `@9` file recorded the rotation `result: skipped` naming `registry file for @9` (result != success).
-(b) row write carried session_id/pid/window/generation with source=registry; the write-touching-model refusal is already covered by test_self_row_admits_declared_fields_refuses_model.
-(c) `ack --ref 7902ac` back-filled session_ref (source: ack); whois authorized by `7902ac` AND by uuid-prefix `abcdef12`, refused too-short `ab`.
-(d) real-tmux dotted-name failure reproduced (see Evidence) informing kid 2's s12.

Run: `pytest extensions/agi/tests/test_rotate*.py test_write*.py test_send.py test_node_writer.py test_stall_detect.py test_bin_help_smoke.py` → 475 passed, 1 skipped.

## Evidence

(d) real tmux — dotted-name `kill-window` vs `@id` kill (throwaway session `zz-*`):

```
$ tmux rename-window -t "$S:foo" "foo.gen9"
$ tmux display-message -p -t "$S:foo.gen9" '#{window_id}'
@257
$ tmux kill-window -t "$S:foo.gen9"
can't find pane: gen9
rc=1
$ tmux kill-window -t "$S:@257"
rc=0      # (window bar, alive and listed afterward)
```

So `session:name.genN` parses `genN` as a PANE (tmux `window.pane` syntax) and fails `can't find pane`; addressing by `@id` kills it. address-by-@id (rename and kill) is exactly kid 2's s12, built on the @ids this round records.

Suite: `pytest extensions/agi/tests/test_rotate.py test_rotate_complete.py test_rotate_handover.py test_rotate_templates.py test_write.py test_write_self_row.py test_write_guard.py test_send.py test_node_writer.py test_stall_detect.py test_bin_help_smoke.py -q` → **475 passed, 1 skipped**. (The repo conftest refuses a bare full-directory run under AGI_TIER=kid, so the mandated group IS the suite surface here.)

Residue provable only on the fixture (noted for kid 2): the s8 grid-commit/push path (this round proves only its SKIPPED fixture branch), the @id-based rename+kill (s12), and stripping briefs/reap/views/telemetry (s9-s13, kid 2's). The real `~/.claude/sessions` file shape was NOT inspected (read-only); the JOIN matches the @id token defensively in each file's content.

## Agent Notes
L4.114 kid1/2: registry JOIN by window @id (s4), model-confirm (s5), registry-row+pending-ack handover (s6), read-back (s7), grid-commit gate (s8), ack--ref backfill+whois uuid-prefix (r3); removed --session-ref/--own-pid. Fixture-proved (a)-(d) incl real-tmux dotted-name failure; 475 tests pass. s8 real grid path + kill-by-@id are kid 2.

PARENT REVIEW (a00-2a2921ea, L4.114 kid1/2): ACCEPTED. Reviewed the artifact, not the report: `_join_successor` matches the window @id token in registry CONTENT (rotate.py:2906+), `_launch_window` now carries `-P -F #{window_id}` (rotate.py:1097), `_write_ack` writes `pending` never `continue` (rotate.py:2655), `_backfill_session_ref` via self_row (rotate.py:2726), whois prefix match (send.py:1009), schema self_row fields now [session_ref, session_id, generation, window, pid]; no `--session-ref`/`--own-pid` in argparse. Reproduced the suite myself: 475 passed, 1 skipped in 36.6s. Verdict kept at inconclusive_lean_proved:70: the handover is fixture-proved only, and s8 grid-commit/push and the real-tmux kill-by-@id remain unproven, so a stronger stamp would be unevidenced. Residue handed to kid 2.
