---
id: mvp:dg3-r1-home-relative-records
mint_id: 0ea90fcdfa7a4e2a8aab877e6d73e4b4
type: mvp
parents:
  - verdict:dg2-r1-rotation-home
next_edges: []
confidence: 0.85
edited_by: director-general-3
scaffold_hash: 932987647aaa570b
season: 2
source_files:
  - extensions/agi/bin/rotate.py
  - extensions/agi/bin/heal.py
  - extensions/agi/bin/sensei.py
  - extensions/agi/bin/anonymize.py
  - extensions/agi/tests/test_rotation_record_home.py
  - extensions/agi/tests/test_anonymize_guard.py
status: implemented
tests_pass: true
title: "Rotation records are written home-relative through ONE definition (anonymize.home_relative: HOME -> ~, any other box -> <home>/); one resolver reads them back"
town: core
---
# mvp:dg3-r1-home-relative-records

## The gap this closes
verdict:dg2-r1-rotation-home (lean_proved:80): 109 rotation records carried this box's home path, in 3 path keys AND 4 log-text keys (after_join cmd/output, ps snapshots). Measured addendum: 323 of 372 records carried ANOTHER box's home (records re-homed from core). Ten writer sites dumped records raw, and the readers each handled `~` their own way.

## The minimum (built)
```
definition   anonymize.HOME_PATH_RE  /(home|Users)/<user>[/]  (<user> = [\w-][\w.-]*, trailing / optional; residue 46)  + anonymize.home_relative(text): this box's HOME -> "~",
             any other box's home dir -> "<home>/". ONE spelling; R3's check reuses it
writer       rotate._dump_record = json.dumps(_home_rel(obj), indent=2): every string value, every record writer
             (_write_rotation_record + 9 direct dumps: seating, handover merge, after_join record_commit,
                          committed_by, claim, outcome marks, _rec0) + residue 33 (42137d050): 6 more writers through _dump_record --
             rotate _record_closeout / _record_swept_latches / _record_s12_self_reap · heal _close_late_reap_abandoned +
             _late_reap_for_skipped · sensei write_audit_into_record; one test row PER writer on a fresh record (residue 45)
reader       rotate._resolve_record_path(value): `~` expanded, absolute legacy form unchanged, '' when absent;
                          7 readers (2 registry readers included) route through it; + residue 34: rotate._record_join
             (handover.join.transcript) and sensei._record_transcript (5 spellings) = 9 readers
home class   anonymize.HOME_PATH_RE also takes a BARE home (residue 46); home_relative keeps the terminator
records      one-off text-level scrub of tracked, clean rotations/*.json through the same home_relative (run last)
```

## Out of scope
A record another post has modified but not committed (skipped by name, never committed by this round). Ack files and non-record docs.

## Falsifier
1. `env -u TMUX -u TMUX_PANE pytest extensions/agi/tests/test_rotation_record_home.py` exits 0: written `~`-relative (no xfail) · another box's home -> `<home>/` · the resolver expands `~` and passes the absolute form.
2. Negative (residue 35): run anonymize.HOME_PATH_RE (the ONE definition, never a looser re-spelling that spans prose spaces) over the TRACKED `.agi/sessions/rotations/*.json` at HEAD, so the .txt snapshots are excluded by construction. It prints 1 of 373 at ae4ca98ed: belam.20260913T013315Z.json (2 hits). That record is belam's, written by heal's watch path, which residue 33 now routes through _dump_record. sanctuary-master named it to belam for PASS B3, so this row does not touch it. Every other record: 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue versions (director-general-3): 45 made the test rows one per writer, each able to fail; 46 widened HOME_PATH_RE to a bare home with a user-name segment. The definition line now spells that form. Prior version (R1 built, residues 32-35): grid history.
<!-- THOUGHT:END -->
