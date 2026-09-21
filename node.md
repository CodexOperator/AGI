---
id: experiment:a00-00207b29-5c9b9a
mint_id: 33fd9a548359422ea0345b52bc140504
type: experiment
parents:
  - hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent
next_edges: []
confidence: 0.6
edited_by: a00-a21fe617
evidence_runs:
  - experiment:a00-00207b29-5c9b9a
loop: hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P4: write.py config:rotations set alerts {audit:...} --dry-run, then node_writer._render_value + yaml.safe_load on the emitted line, then _load_alerts on the read-back", "expected": "the emitted alerts: value reads back as a dict (the routing matrix)", "observed": "dry-run records a plain str; the renderer quotes it; YAML reads a str; json.loads fails on the unquoted keys; _load_alerts returns {} -> alerts treated ABSENT -> broadcast. FALSIFIED", "result": "falsified"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P2: _announce_rotation(record_path=<rotation json>) with monkeypatched send/send_room/wake", "expected": "the rotation record carries announced_to == delivered", "observed": "announced_to=[master-sensei, sanctuary-director, sanctuary-helper] == delivered; held", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P3: cmd_rotate_self call site threads record_path into the announce", "expected": "the released record gets stamped by the real rotate-self path", "observed": "record_path=(record_path if record_path else None) at rotate.py:16644; held", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe P1 rerun: run_after_join(seat=stream-master, type_input=recorder, send_dm=recorder)", "expected": "silent successor: zero machine lines, no seam fires", "observed": "typed=0 sent=0; held", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 37f4ce6b05000280
season: 2
title: A00 00207b29 5c9b9a
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-00207b29-5c9b9a

## Experiment

Fix pass on the SM.16 rotation-alerts routing-matrix work (experiment:a00-b310d0b4-e9cfbd).
Parent probes falsified two conjuncts of hypothesis:l4-rotation-alerts-follow-a-routing-
matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent; this
round IMPLEMENTS both fixes on the built bytes and proves them on the built bytes.

**Fix 1 (conjunct 4 — the ROTATION record must carry `announced_to`).** The rotate-self
rotation record was written at rotate.py:16436 BEFORE `_announce_rotation` at :16590 and
never rewritten, so only the seating record got `announced_to`. Now `_announce_rotation`
gains an optional `record_path` kwarg and stamps the recipients it actually reached (its
`delivered` return) onto that record in place via a new best-effort helper
`_announce_stamp_announced_to` (never a gate). The rotate-self call site (:16590) passes
`record_path=record_path` — the SAME in-place record the ack-rotate rewrote at (5.75) — so
the completed rotation record names who it told. Both delivered-return sites (prime and
non-prime legs) stamp.

**Fix 2 (conjunct 5 — silent must stop the after_join TYPING path too).** In production the
after_join's SECOND input is TYPED into the successor pane through the `type_input` seam
(send_dm is never reached), so gating send_dm alone leaked a machine line to a silent
post's pane. `run_after_join` now short-circuits the delivery decision with
`elif not _alert_allowed(root, seat)` → delivery `{"mode": "silent-refused", ...}` — the
typing seam NEVER fires and the dm is skipped, so stream-master gets zero machine lines.
`seat` is the receiver here (the successor the after_join addresses), the same name the
default and injected send_dm gates consult.

**sensei-wake template line (claim (4), rotations.md:122).** The claim says the
`sensei-wake` after_join entry becomes a TEMPLATE line for master-sensei to drop (the audit
edge now delivers to master-sensei directly, so the old hard-send double-wakes it). The
parent's hard rule is `DO NOT touch the live config:rotations node` — the Prime owns the
config writes at merge-up (the ONE `set alerts` line + the sensei-wake TEMPLATE edit
together). So the round ships the change as SPEC, not as a live-node write: drop the
`sensei-wake` entry in the prime_director template's `startup.after_join` at
`.agi/nodes/.geometry/rotations.md:122` when the `alerts` matrix lands — the code half no
longer needs it. Frankentomitted deliberately touched: none.

## Evidence

New tests added to `extensions/agi/tests/test_rotation_alerts.py`:

```python
# (a) a rotation record carries announced_to -- conjunct 4
def test_rotation_record_carries_announced_to(monkeypatch, tmp_path): ...
```

All ten pass (`10 passed` in 40s), twice — after the Path-vs-str fix in the stamp helper.

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alerts.py -q
..........  [100%]
10 passed in 40.11s

$ python3 -m pytest test_rotate.py test_rotate_startup.py test_rotate_alert_two_tree.py
374 passed, 1 xfailed

$ python3 -m pytest test_rotate_autopsy.py test_sensei_rotate_out_audit.py
41 passed
```

Acceptance vs the two falsifiers-name exactly:
(a) `announced_to` now rides the ROTATION record (test (a)) — the parent probe P3 was
FALSIFIED *before* and is now PROVED.
(b) `run_after_join` to a silent successor with a `type_input` seam fires NO seam (test
test_after_join_type_seam_to_silent_never_fires) — parent probe P1 now PROVED.

The `alerts:` matrix is NOT written to the live config by the round (the Prime's
one-line merge-up act, dry-run-proven in the b310d0b4 node). The sensei-wake TEMPLATE
edit is also deferred to the Prime per the parent's "DO NOT touch the live config node"
rule; the exact edit ships above.

## Agent Notes
Fixed the two parent-falsified conjuncts on the built bytes: (4) the rotate-self rotation record now carries announced_to via a record_path kwarg on _announce_rotation stamped in place; (5) run_after_join gates the type_input coding path on _alert_allowed so a silent successor's pane gets zero machine lines. Two new falsifier tests (record carries announced_to; type seam to silent never fires) + 8 existing = 10 passed; test_rotate+startup+alert_two_tree 374 passed / 1 xfailed; autopsy+sensei_audit 41 passed. sensei-wake TEMPLATE drop + alerts write stay the Prime's merge-up act (round never touches live config).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SM.16 kid 2. Instruction (conjunct 1): config:rotations gains ONE top-level map alerts: written by the Prime as one write.py `set alerts {…}` line, dry-run-proven in the node body. Machine, measured by parent probe P4: verb_set._coerce returns the braces string as a STR (only pure JSON parses to a dict, and the shipped line has unquoted keys), node_writer._render_value quotes it, yaml.safe_load reads a str, json.loads fails in _load_alerts, so _load_alerts returns {} and the whole matrix is treated as ABSENT -> broadcast. The kid test fixture hand-writes valid JSON into YAML, a shape write.py never emits, which is why its suite is green. Near miss: a fixture that writes the map the way the tool DOES (a quoted flow string) would have failed at once. Held probes: P2 the rotation record carries announced_to (delivered == stamped), P3 cmd_rotate_self threads record_path (:16644), P1 rerun a silent successor gets zero after_join machine lines (type seam no longer fires). Verdict demoted proved -> inconclusive_lean_disproved:60 on probe P4.
<!-- THOUGHT:END -->
