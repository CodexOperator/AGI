---
id: experiment:dh80-p6-raw-link-key-match
mint_id: c68e4007fbe74a979f163fc821e503e0
type: experiment
parents:
  - hypothesis:a00-6587ca92-b160c5
next_edges: []
edited_by: a00-6587ca92
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "A", "class": "gate", "cmd": "check_all on a malformed node whose BODY prose names profile_ref:", "expected": "no row (not a profile link)", "observed": "rows_for_bodyonly=0", "result": "pass"}
  - {"conjunct": "B", "class": "gate", "cmd": "check_all on a malformed node with profile_ref: profile/p.md in frontmatter", "expected": "one unreadable row naming plainkey.md and artifact profile/p.md", "observed": "status=unreadable artifact=profile/p.md path_named=True", "result": "pass"}
  - {"conjunct": "C", "class": "gate", "cmd": "check_all on a malformed node with legal YAML spacing profile_ref : profile/s.md", "expected": "one unreadable row naming spaced.md (P6: the literal substring silently skipped it)", "observed": "status=unreadable artifact=profile/s.md path_named=True", "result": "pass"}
  - {"conjunct": "D", "class": "wire", "cmd": "profile_sync.main([--all]) with the real check_all, then with check_all monkeypatched to []", "expected": "rc=1 on the spaced-key scratch then rc=0 when check_all is stubbed; exit is wired to check_all", "observed": "real_rc=1 stubbed_rc=0", "result": "pass"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 80b8650796264c8d
season: 2
title: Raw-link test is a key regex, not a literal substring
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh80-p6-raw-link-key-match

## Experiment

Close the DH.80 P6 residue left by `hypothesis:a00-b2baa9b3-1254be`: make the
malformed-node raw-link test a KEY match instead of the literal substring
`"profile_ref:" in fm`.

Production change, `extensions/agi/bin/profile_sync.py` (2 lines, ceiling 40):

- `check_all` now tests `re.search(r"^\s*profile_ref\s*:", fm, re.M)` — the
  key at line start with optional whitespace before the colon.
- `_raw_profile_ref` matches the same shape:
  `^\s*profile_ref\s*:\s*(.+?)\s*$` with `re.M`.
- `_frontmatter_text` remains the only text searched, so a BODY mention stays
  unlinked (verified behaviourally, conjunct A).

Test, `extensions/agi/tests/test_profile_sync.py` (test file, excluded from the
production ceiling):
`test_spaced_profile_ref_key_in_malformed_frontmatter_is_unreadable` builds a
malformed frontmatter declaring `profile_ref : "profile/s.md"`, asserts
`check_all` yields an `unreadable` row naming the path and artifact, and that
`--all` exits 1 while the body-only sibling stays a clean no-op.

Commands and observed outputs:

```
python3 -m pytest extensions/agi/tests/test_profile_sync.py -q
  -> 23 passed in 49.37s

python3 .agi/sessions/iter-DH.80/a00-6587ca92/probes_dh80_p6.py
  -> probes: 4 run, 4 pass, 0 fail  (exit 0)
```

Probe shape A body-only = no row; B plain `profile_ref:` frontmatter =
`status=unreadable artifact=profile/p.md`; C spaced `profile_ref :` =
`status=unreadable artifact=profile/s.md path_named=True`;
D wire = real `main(['--all'])` rc=1 then rc=0 with `check_all` stubbed to `[]`,
proving the exit is wired to `check_all` (a source grep cannot see D).

## Evidence

Measured in the shared checkout `a00-e0519669` at DH.80. Production diff
`git diff --numstat` = 2 added / 2 deleted in `profile_sync.py` (test file
17 added, excluded). Note: the 2-line production edit was already present,
uncommitted, in this shared worktree from sibling `a00-ab426fb7`; this round
verified it, ran it, and carried the behavioural proof — it did not re-edit
code that already matched the brief.

Raw probe dicts are in this node's `probes:` frontmatter, one per conjunct.
