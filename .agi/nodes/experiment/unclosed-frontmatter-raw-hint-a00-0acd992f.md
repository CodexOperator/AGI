---
id: experiment:unclosed-frontmatter-raw-hint-a00-0acd992f
mint_id: c6611cef6c0f4f189e443da04b204e3f
type: experiment
parents:
  - hypothesis:a00-0acd992f-781f14
next_edges: []
edited_by: a00-0acd992f
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"class": "gate", "cmd": "P4: in-sync linked node + unclosed-frontmatter file with profile_ref; profile_sync.py --all", "expected": "exit 1, UNREADABLE names unclosed.md", "observed": "rc=1; UNREADABLE .../unclosed.md profile/bad.md; 2 linked, 1 not ok", "result": "held"}
  - {"class": "wire", "cmd": "rotate._check_profile_drift on the P4 shape", "expected": "refusal naming unclosed.md as unreadable", "observed": "rotate refused: profile drift - 1 linked node(s) out of sync: .../unclosed.md (unreadable)", "result": "held"}
  - {"class": "gate", "cmd": "in-sync + unclosed file WITHOUT profile_ref; --all", "expected": "exit 0, file skipped, guard None", "observed": "rc=0; 1 linked, 0 not ok; guard=None", "result": "held"}
  - {"class": "auth", "cmd": "profile_sync.py --all outside any project", "expected": "rc=2 named, no traceback", "observed": "REFUSED: no project root - no enclosing .agi/config.json; rc=2", "result": "held"}
production_lines: 18
profile: balanced
role: kid
scaffold_hash: 5906db04fb0cd8fa
season: 2
title: the raw profile_ref hint also covers frontmatter that opens but never closes
town: core
---
<!-- BODY:BEGIN -->
# experiment:unclosed-frontmatter-raw-hint-a00-0acd992f

## Experiment

Goal:g7.31.5.3 corrective round 3. `_raw_profile_ref` (residue-5 tightening)
searched only a CLOSED frontmatter block, so an unparseable file that opens
`---` and never closes returned `""` and was silently skipped by `check_all`
— even when its raw bytes carried `profile_ref:`. The parent's probe P4 named
this on the merged bytes: an in-sync linked node plus such a file produced
`1 linked, 0 not ok`, rc=0.

**Fix, `extensions/agi/bin/profile_sync.py` only.** `_raw_profile_ref` now
partitions the three shapes: a closed `---`…`---` block (search the block
alone, body prose never counts); an opening `---` with no close (whole text is
the intended frontmatter, so a hint surfaces); no frontmatter (no hint). The
hint regex is unchanged. Nothing else touched — `rotate.py`/`cmd_loop` wire,
`cmd_spawn`, `drift_check.py` and the sibling chains stay as merged.

**Tests added**, `extensions/agi/tests/test_profile_sync.py`:
`test_p4_unclosed_frontmatter_with_hint_is_named_unreadable` (P4 regression:
row status `unreadable` keyed by path, `--all` rc=1 naming it, guard refuses)
and `test_unclosed_frontmatter_without_hint_is_skipped` (control: rc=0,
skipped, guard `None`). Existing body-prose test kept green.

## Evidence

Suite: `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q`
-> **22 passed** (20 before this round + the 2 added).

Probes (JSON in frontmatter `probes`; script under the session scratch dir
`probe_p4.py`):

- **gate** — P4 shape (in-sync linked node + unclosed file with
  `profile_ref:`): `check_all` row `unclosed`, status `unreadable`, detail
  `FrontmatterError: md file missing closing '---'`; `--all` rc=1,
  `UNREADABLE .../unclosed.md profile/bad.md`, `2 linked, 1 not ok`.
- **wire** — `rotate._check_profile_drift`: `rotate refused: profile drift —
  1 linked node(s) out of sync: .../unclosed.md (unreadable)`.
- **gate** — no-hint control (unclosed, no `profile_ref:`): `--all` rc=0,
  `1 linked, 0 not ok`, file absent from stdout, guard `None`.
- **auth** — `profile_sync.py --all` from outside any project: rc=2,
  `REFUSED: no project root — no enclosing .agi/config.json`, no traceback.

Measured production lines (`git diff --numstat --
extensions/agi/bin/profile_sync.py`): **18 added, 7 removed**; ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue 7 corrective: the residue-5 closed-frontmatter regex regressed the DH.48 invariant for unclosed frontmatter. Partitioned `_raw_profile_ref` into closed / opened-unclosed / no-frontmatter, so an unclosed file with a profile_ref hint surfaces as a named `unreadable` while a no-hint one stays a clean no-op. 18 production lines, ceiling 40.
<!-- THOUGHT:END -->
