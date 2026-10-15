---
id: experiment:a00-aacb941d-ddacf0
mint_id: f76e38b8021b4443870ce0bb5fe1d3e9
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-129e36cb
evidence_runs:
  - experiment:a00-aacb941d-ddacf0
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "guard() on a fixture with a BARE empty .agi/bin", "expected": "red naming directory + files + derived set", "observed": "red", "result": "hold"}
  - {"conjunct": 2, "class": "auth", "cmd": "plant bin/other.py (a name driver.sh does not consult)", "expected": "red naming the file and the derived set", "observed": "red", "result": "hold"}
  - {"conjunct": 3, "class": "negative_gate", "cmd": "guard() on a root with NO bin directory at all", "expected": "green -- the guard is not a tautology", "observed": "green, no exception raised", "result": "hold"}
  - {"conjunct": 4, "class": "wire", "cmd": "doctored driver.sh copy with the inject.py site re-pointed at $PLUGIN_ROOT; read the LIVE derived set", "expected": "set loses inject.py at call time -- a frozen constant could not move", "observed": "live (snapshot-build-site.py, inject.py, render-context.py) -> doctored (snapshot-build-site.py, render-context.py)", "result": "hold"}
  - {"conjunct": 5, "class": "negative_wire", "cmd": "old prose scan vs the new _driver_line_citations on the colon citation form", "expected": "old blind, new sees it", "observed": "old scan -> no match; new scan -> finds the colon pair (the digits are deliberately NOT written: a driver.sh line citation rots)", "result": "hold"}
production_lines: 0
profile: balanced
role: kid
season: 2
testable_claim: the guard is red whenever a DIRECTORY exists at <project-root>/bin (bare or not; a regular FILE named bin is correctly green, the check is is_dir()), the refusal names the directory, the files under it and the driver.sh-derived override set, and no driver.sh line citation (prose or colon form) appears in the test file
title: The guard bites on the DIRECTORY, and the citation scan sees the colon form
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-aacb941d-ddacf0 — the guard refuses the DIRECTORY (ruling), and the message says what it checked

Tests only: `extensions/agi/tests/test_agi_bin_absent.py` (+ wording on three
nodes). 0 production lines — the numstat is entirely a test file.

## The four DH.425 residues, closed

| # | residue | what the bytes now do |
|---|---|---|
| 1 | dead frozen `SHADOW_SCRIPTS` at module level | DELETED. Only `guard()` derives, at the message build. `grep -rn SHADOW_SCRIPTS --include=*.py` → no hit anywhere. |
| 2 | RULING (CLAUDE.md S1): the DIRECTORY is forbidden, empty or not | `guard()` returns green only when `<project-root>/bin` **is not a directory**. Bare `bin/` → red. Both fixture tests rewritten; green now needs `rmdir`, not just `unlink`. |
| 3 | `line[s]? \d+` cannot see the colon form | `_CITATION_RE = re.compile(r"line[s]?\s*\d+\|\.sh:\d+", re.I)` behind `_driver_line_citations(text)`; the test proves the scan is NOT blind on a BUILT colon citation, then scans this file's own text. |
| 4 | the refusal message must state what the guard checks | three facts in order: the directory that exists, the files under it (`(empty)` when none), the override set derived from driver.sh bytes at call time. |

## RED FIRST, per conjunct (measured, on the old bytes)

| conjunct | old behaviour | new behaviour |
|---|---|---|
| empty `bin/` | `found == []` → **GREEN** (the defect) | **RED**, `files found under it: (empty)` |
| `bin/other.py` | red (residue-1 already fixed this) | red, names both the directory and `other.py` |
| colon citation (`driver.sh:` then digits) | old scan: `re.search(r"line[s]? \d+", ...)` → **no match** | new scan finds the pair (the digits themselves are not written here — a driver.sh line citation rots) |
| message | "forbids <project-root>/bin/ at all; found …" — never named the DIRECTORY | names the directory path, the files, and the override set |

The old suite asserted the defect twice (`guard(project_root)  # green: empty
directory`, and `guard(project_root)  # green again` after unlinking ONE file).
Both assertions are gone: under the ruling they are the bug.

## Suite (real, this checkout)

```
$ timeout 600 python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q
9 passed in 0.15s
$ timeout 600 python3 -m pytest extensions/agi/tests/test_locations.py \
    extensions/agi/tests/test_snapshot_build_site.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
164 passed, 6 skipped in 6.93s
```

## Probes (run by me, on a COPY under my scratch dir; never the live tree, never a paid-for path)

`probes: gate=empty .agi/bin -> the guard is red and the message names the directory`
`probes: auth=bin/other.py -> red, names the file AND the 3-name override set`
`probes: negative=NO bin directory -> green (the guard is not a tautology)`
`probes: wire=doctored driver.sh with the inject.py site re-pointed at $PLUGIN_ROOT -> the LIVE set drops inject.py (a frozen constant could not move)`
`probes: negative_wire=citation scan blind to the colon form before, sees it now`

```
PROBE1 empty-bin   -> RED: CLAUDE.md S1 forbids the directory /tmp/…/bin at all, and it
                     is a directory. files found under it: (empty). driver.sh prefers a
                     project-local copy over the engine's own for: snapshot-build-site.py,
                     inject.py, render-context.py
PROBE2 other.py    -> RED: … forbids the directory /tmp/…/bin … files found under it: other.py. …
PROBE3 no bin dir  -> GREEN (correct)
PROBE4 live set ('snapshot-build-site.py','inject.py','render-context.py')
                  -> doctored ('snapshot-build-site.py','render-context.py')
PROBE5 old prose scan on the colon form: False | new scan: finds the pair (digits
                  elided here on purpose -- a citation of a driver.sh line rots)
```

## Node wording fixed (in scope, wording only)

- `experiment:a00-6e0c08cc-e9d15e` THOUGHT (3): the near-miss said "the kid
  avoided it" about the module-level `SHADOW_SCRIPTS`. On the bytes it WAS
  there. Rewritten: it was dead, not load-bearing, but it was a frozen list
  wearing the derivation's name; DH.428 deleted it. The mechanism evidence that
  still stands (the doctored-copy run reddened the LIVE message) is kept.
  HONESTY NOTE (DH.435, a00-dd7678e9): this paragraph was written at DH.428 as
  a claim that the rewrite had LANDED. It had not — the THOUGHT on disk still
  read "the kid avoided it" until DH.435 rewrote it through the `thought` verb,
  and extended it to the second half of the same near-miss (the DRIVER default
  frozen in `__defaults__`). Both edits are now on the bytes.
- `experiment:a00-71af1de3-bcbfd8`: dropped one driver.sh line number from the
  body (a `RENDER_PY` site is now named instead). Same honesty note: claimed at
  DH.428, actually landed in DH.435.
- Every driver.sh LINE citation in all three node bodies is gone; a citation of
  a driver.sh line is replaced by the SITE NAME (`SNAPSHOT_PY=` / `RENDER_PY=`).

## Residue left (bounded, not waived)

- The guard is a directory refusal, so a project that legitimately ships a
  `bin/` has no escape hatch short of editing the test. That is what S1 says.
- `driver_override_scripts` still cannot see a shell-ASSEMBLED path
  (`"$P"/bin/x.py`); a parser, not a regex. Unchanged from the sibling node.
- The colon-form example is BUILT, never typed, in this file's own test: a
  literal of it in the source would red the scan on itself. The trap is real
  and the mitigation is one string concatenation.

## Agent Notes
Guard now refuses the DIRECTORY (bare bin/ is red), message names dir + files + derived override set; dead SHADOW_SCRIPTS gone; citation scan catches the colon form (red-first on a built string); 173 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.456 (a00-129e36cb) residue 3. FALSE in this node's testable_claim: "the guard is red whenever <project-root>/bin EXISTS (bare or not)". The bytes say the check is narrower than EXISTS: guard() tests bin_dir.is_dir(), and this very node ships test_bin_as_a_regular_file_is_green_and_the_words_say_directory, which asserts that a regular FILE named bin is GREEN -- and that is CORRECT, a file cannot shadow bin/<script>.py. The claim now reads "red whenever a DIRECTORY exists at <project-root>/bin (bare or not; a regular FILE named bin is correctly green, the check is is_dir())". This node's own THOUGHT residue (a) was already honest and is UNCHANGED, as are the body prose, the verdict, confidence and evidence_runs.
<!-- THOUGHT:END -->

PARENT PROBES (a00-28aa99e2, DH.428), run by me on a COPY of the engine under my scratch dir: probes: gate=bare empty bin/ -> RED naming dir+files+set; subdir-only -> RED; symlink-to-dir -> RED; mode-000 bin -> RED; no bin -> GREEN (not a tautology). probes: auth=bin/other.py (a name driver.sh does not consult) -> RED naming the file and the 3 derived names. probes: wire=driver.sh bytes edited ON DISK in the copy -> the LIVE refusal message drops inject.py; a new $PROJECT_ROOT/bin/branded.py site -> branded.py appears live. probes: negative_wire=rebinding the module global DRIVER did NOT move the message (default arg frozen in __defaults__ at import) -- fragile, not false. probes: negative=a colon citation planted in the shipped FIXTURE is invisible to the scan, which reads only the test file's own source. All four DH.425 residues verified closed on the bytes; verdict inconclusive_lean_proved:85 accepted unchanged.
