---
id: hypothesis:a00-cef02d4e-d5ac79
mint_id: 621facaf95674c80800bf0ae8bc559d9
type: hypothesis
parents:
  - goal:g7.31.3.1
next_edges: []
confidence: 0.85
edited_by: a00-48ff817a
evidence_runs:
  - hypothesis:a00-cef02d4e-d5ac79
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep -nF -e \"write | read | send | dispatch|workflow | rotate|spawn\" .agi/nodes/doc/director-grok-internals.md", "expected": "all five contract route names present on the cold-seat brief artifact", "observed": "L152 carries all five inside SECTION:PROFILE (boundary L55..L194, next SECTION header L195); rebuilt block L152-L154", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "grep -Ein grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py", "expected": "zero hits attributable to a sixth special grok route", "observed": "exit 1, zero matches", "result": "pass"}
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 52154dd66652753b
season: 2
testable_claim: The cold-seat custom-instruction surface doc:director-grok-internals SECTION:PROFILE lists all five pane routes under their contract names (write|read|send|dispatch|workflow|rotate|spawn) and records the seat-spelling rename old->new; falsified if any contract name is absent or an unrecorded seat spelling stands alone
title: Cold-seat PROFILE brief lists the five routes by contract names with the seat rename recorded
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# hypothesis:a00-cef02d4e-d5ac79

## Claim (the whole job)
A cold-seat brief / custom-instruction surface lists the five pane-facing routes under their CONTRACT names from the `goal:g7.31.3` table (`write | read | send | dispatch|workflow | rotate|spawn`) and records the deliberate seat-spelling rename old→new wherever it uses seat words.

## Measured — candidate surfaces a cold seat receives
Grep of the only two doc surfaces carrying a routes line (`.agi/nodes/doc/`):
- `doc:director-grok-internals` `SECTION:PROFILE` (header: "copy into agent description" — the custom-instruction surface): `routes: write.py · read · send · dispatch/workflow · rotate/spawn` at file L152 pre-fix.
- `doc:unified-director-brief` L36: `routes write·read·send·dispatch/workflow·rotate/spawn` — the ROLE brief masters hand by node id.
- `doc:belam-grok-internals` `SECTION:PROFILE`: no routes line.

**Gap (both surfaces, pre-fix).** All five route *words* were present, but routes 4/5 used the seat spelling `/` where the contract names them with `|`, route 1 was `write.py`, and no contract→seam→seat rename was recorded anywhere (grep `old->new|contract|seam|rename` on the three surfaces = 0 hits).

## Chosen artifact
`doc:director-grok-internals` `SECTION:PROFILE` — the block literally stamped "copy into agent description", i.e. the custom-instruction surface a cold seat is handed.

## Fix (sanctioned writer, in-graph)
`python3 extensions/agi/bin/write.py doc:director-grok-internals 'replace body 131:132 -'` (new text on stdin) inserted the compact contract→seam→seat block. Doc lines: +4/-2 (git diff --numstat `4 2`). No engine code touched.

## Built-artifact proof (`grep -nF` on `.agi/nodes/doc/director-grok-internals.md`)
- `write` → L152 (contract list) / L154 (seat spelling)
- `read` → L152 / L153 / L154
- `send` → L153
- `dispatch|workflow` → L152
- `rotate|spawn` → L152

Block as it now stands:
```
L152 routes: write | read | send | dispatch|workflow | rotate|spawn   ← CONTRACT names (goal:g7.31.3 table)
L153   seam: write.py · commands.py/viewport · send.py · dispatch.py+workflow.py · rotate.py
L154   seat spelling: write.py · read · send · dispatch/workflow · rotate/spawn  (rename recorded old→new)
L155   (engine routes wording — prefer named CLIs / write.py route over raw tools)
```

## Negative check (leaf invariant: no sixth "special grok route")
`grep -Ein 'grok' extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py` → **zero hits** (exit 1). No sixth route.

## Probes
- **wire** — the grep reaches the real artifact: `grep -nF 'dispatch|workflow' .agi/nodes/doc/director-grok-internals.md` → L152. PASS.
- **gate** — no sixth route: grok grep on `dispatch.py` / `rotate.py` → 0 hits. PASS.

## Honest gaps
- `doc:unified-director-brief` L36 is **not** edited; it still carries `dispatch/workflow` / `rotate/spawn` without a recorded rename. The falsifier is satisfied by the chosen PROFILE surface, but the sibling brief surface keeps the same gap — a follow-up at this leaf should mirror the block there or retire one surface as the SoT.
- No engine code changed; nothing exercised a live route.

## Agent Notes
PROFILE surface (director-grok-internals) now lists all five routes by contract names at L152 + records contract->seam->seat rename at L153-154; grep wired, no sixth grok route in dispatch.py/rotate.py

PARENT ACCEPT (a00-48ff817a DH.86): kid a00-cef02d4e changed doc:director-grok-internals SECTION:PROFILE L152-L154 to the five contract route names plus engine seams and recorded the deliberate seat rename; two parent probes pass (wire grep inside PROFILE; zero grok route in dispatch.py/rotate.py). Verdict stays inconclusive_lean_proved:85, a doc/grep proof with no live sync exercised. Residue nested: doc:unified-director-brief L36.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-48ff817a, DH.86). (1) INSTRUCTION: run one negative probe per claim conjunct yourself and record them as probes; a kid that passes its own suite but fails your probe is lean_disproved. (2) MACHINE: git diff shows .agi/nodes/doc/director-grok-internals.md +4/-2. L152 now lists the five CONTRACT names (write | read | send | dispatch|workflow | rotate|spawn), L153 names the engine seams, L154 records the seat spelling old->new; the edit arrived through write.py replace body 131:132, the sanctioned writer, not a hand edit. My wire probe finds L152 inside SECTION:PROFILE (the block literally stamped copy into agent description, boundary L55..L194); my gate probe greps grok in dispatch.py and rotate.py and gets exit 1. I declined to trust the kid transcript and re-read the bytes. (3) NEAR MISS: accepting the kid grep transcript and its line numbers as evidence; re-running on the bytes is what confirms the block sits INSIDE the pasted PROFILE region and not in a sibling STANDING block a sync could skip. (4) DEVIATION: none. The kid named a real residue: doc:unified-director-brief L36 is a second cold-seat brief that still carries dispatch/workflow and rotate/spawn with no recorded rename. Nested as kid 2 under this same goal rather than left to ride.
<!-- THOUGHT:END -->
