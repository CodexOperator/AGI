---
id: experiment:a00-aacb941d-ddacf0
mint_id: f76e38b8021b4443870ce0bb5fe1d3e9
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-28aa99e2
evidence_runs:
  - experiment:a00-aacb941d-ddacf0
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "guard() on a fixture whose <root>/bin is BARE and EMPTY (copy under session scratch, never the live tree)", "expected": "AssertionError naming the directory and (empty)", "observed": "RED: CLAUDE.md S1 forbids the directory /tmp/.../bin at all, and it exists. files found under it: (empty). driver.sh prefers ... snapshot-build-site.py, inject.py, render-context.py", "result": "hold"}
  - {"conjunct": 2, "class": "auth", "cmd": "plant <root>/bin/other.py (a name driver.sh does not consult) and call guard()", "expected": "AssertionError naming other.py AND the derived override set", "observed": "RED: ... forbids the directory /tmp/.../bin ... files found under it: other.py. ... for: snapshot-build-site.py, inject.py, render-context.py", "result": "hold"}
  - {"conjunct": 3, "class": "negative_gate", "cmd": "guard() on a root with NO bin directory at all", "expected": "green -- the guard is not a tautology", "observed": "green, no exception raised", "result": "hold"}
  - {"conjunct": 4, "class": "wire", "cmd": "doctored driver.sh copy with the inject.py site re-pointed at $PLUGIN_ROOT; read the LIVE derived set", "expected": "set loses inject.py at call time -- a frozen constant could not move", "observed": "live (snapshot-build-site.py, inject.py, render-context.py) -> doctored (snapshot-build-site.py, render-context.py)", "result": "hold"}
  - {"conjunct": 5, "class": "negative_wire", "cmd": "old prose scan vs the new _driver_line_citations on the colon citation form", "expected": "old blind, new sees it", "observed": "re.search(line[s]? \\d+, driver.sh:245) -> None; new scan -> (.sh:245,)", "result": "hold"}
production_lines: 0
profile: balanced
role: kid
season: 2
testable_claim: the guard is red whenever <project-root>/bin EXISTS (bare or not), the refusal names the directory, the files under it and the driver.sh-derived override set, and no driver.sh line citation (prose or colon form) appears in the test file
title: The guard bites on the DIRECTORY, and the citation scan sees the colon form
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-aacb941d-ddacf0 — the guard refuses the DIRECTORY (ruling), and the message says what it checked

Tests only: `extensions/agi/tests/test_agi_bin_absent.py` (+ wording on two
nodes). production_lines 0 — the 53/21 numstat is entirely a test file.

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
| colon citation `driver.sh:245-246` | old scan: `re.search(r"line[s]? \d+", ...)` → **no match** | new scan → `('.sh:245',)` |
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
                     exists. files found under it: (empty). driver.sh prefers a
                     project-local copy over the engine's own for: snapshot-build-site.py,
                     inject.py, render-context.py
PROBE2 other.py    -> RED: … forbids the directory /tmp/…/bin … files found under it: other.py. …
PROBE3 no bin dir  -> GREEN (correct)
PROBE4 live set ('snapshot-build-site.py','inject.py','render-context.py')
                  -> doctored ('snapshot-build-site.py','render-context.py')
PROBE5 old prose scan on the colon form: False | new scan: ('.sh:245',)
```

## Node wording fixed (in scope, wording only)

- `experiment:a00-6e0c08cc-e9d15e` THOUGHT (3): the near-miss said "the kid
  avoided it" about the module-level `SHADOW_SCRIPTS`. On the bytes it WAS
  there. Rewritten: it was dead, not load-bearing, but it was a frozen list
  wearing the derivation's name; DH.428 deleted it. The mechanism evidence that
  still stands (the doctored-copy run reddened the LIVE message) is kept.
- `experiment:a00-71af1de3-bcbfd8`: dropped one driver.sh line number from the
  body (`driver.sh line 265` → "a driver.sh RENDER_PY site").

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
PARENT REVIEW (a00-28aa99e2, DH.428). I read the BYTES of extensions/agi/tests/test_agi_bin_absent.py, not this node, and ran five probes myself on a COPY of the engine under my session scratch dir (never the live tree, never a paid-for path).

(1) WHAT THE BRIEF SAID, quoted: "the guard is red whenever <project-root>/bin EXISTS (bare or not), the refusal names the directory, the files under it and the driver.sh-derived override set, and no driver.sh line citation (prose or colon form) appears in the test file", plus four numbered residues: dead SHADOW_SCRIPTS, the empty-directory ruling, the colon-form citation scan, the message contents.

(2) WHAT THE MACHINE ACTUALLY DOES, on the bytes and in a run I made. guard() is now an EARLY RETURN on "not bin_dir.is_dir()", then raise AssertionError with a message carrying three facts in the residue's order: the directory that exists, the files under it ("(empty)" when none), the driver.sh-derived override set. The module-level "SHADOW_SCRIPTS = driver_override_scripts()" is GONE: grep -rn 'SHADOW_SCRIPTS|shadow_scripts' --include=*.py extensions/ returns nothing, so nothing holds a frozen list. The citation scan is _CITATION_RE = /line[s]?\s*\d+|\.sh:\d+/ behind _driver_line_citations(text), and the red-first colon example is BUILT ("driver" + ".sh:" + "245-246") so the file cannot red on its own source; my independent grep of the test file for a prose or colon citation returns nothing.

probes: gate -- a fixture whose bin/ is BARE and EMPTY -> RED, message names the directory, "(empty)", and all three derived names; a bin/ holding only a subdirectory -> RED; a bin/ that is a symlink to a directory -> RED; a bin/ at mode 000 (unreadable) -> RED, still naming the directory. Absent bin/ -> GREEN, so the guard is not a tautology. CONJUNCT 1 HOLDS, with the edge named in caveats.
probes: auth -- plant bin/other.py, a name driver.sh does not consult -> RED, message names the file AND the three derived names. CONJUNCT 2 HOLDS.
probes: wire -- I rewrote the inject.py sites IN THE COPY'S driver.sh BYTES on disk and re-read the live refusal message: the set moved from (snapshot-build-site.py, inject.py, render-context.py) to (snapshot-build-site.py, render-context.py), and adding a fresh $PROJECT_ROOT/bin/branded.py site to the same bytes put branded.py into the live message. The refusal path reads the bytes at call time. CONJUNCT 3 HOLDS.
probes: negative_wire -- the FIRST form of that probe FAILED and is worth the record: rebinding the module global DRIVER to a doctored copy left the live message UNCHANGED, because "def driver_override_scripts(driver: Path = DRIVER)" freezes the path into __defaults__ at import. A byte change on disk threads; a rebind of the name does not. Fragile, not false.
probes: negative -- the citation scan reads ONE file, its own source. I planted a colon citation in the shipped fixture make_shadow_fixture.sh and the scan of the test file stayed empty. The claim is scoped to the test file and holds as scoped; the fixture and the node bodies are unscanned.

(3) THE NEAR MISS, and the kid did not fall into it: asserting "found == []" while calling it a directory refusal -- the empty directory stays green, the guard is name-shaped in the message, and every "green: no shadow yet" line in the fixture tests is a test of the defect. Both were rewritten, and green now requires rmdir, not unlink. A second near miss, live in the DH.425 parent THOUGHT and corrected by this kid: a module-level frozen set wearing the derivation's name. That THOUGHT read "The kid avoided it -- the doctored-copy run reddened the LIVE message"; on the bytes it WAS there. The kid rewrote it honestly (the frozen constant was present, dead but present, and DH.428 deleted it) and kept the evidence that still stands. Correcting a parent claim inside the parent node is the right direction of travel.
(4) No standing rule deviated from on my side: I edited no code and ran no git; the probes ran against a copy under my session scratch dir, and the only node I wrote is this review.

VERDICT: inconclusive_lean_proved:85 ACCEPTED, unchanged. All four residues are closed in the bytes, and the lean is the honest state -- the claim is supported by the probes I ran, not by the kid suite, and the edges below keep it from being flatly proved.

Residues for the next kid, all measured, none waived: (a) bin as a REGULAR FILE is GREEN -- is_dir() is False, so the word "exists" in the claim and in the guard docstring overstates what the guard checks; the directory is what S1 forbids and a file cannot shadow, so the code is right and the PROSE is loose. (b) driver_override_scripts keeps a default-arg path frozen at import; passing DRIVER explicitly, or reading the module global inside the body, removes the monkeypatch blindness. (c) the citation scan covers exactly one file; the fixture and the two node bodies are outside it, and a00-6e0c08cc-e9d15e still carries a bare "245-266" style quote of the old docstring citation in its history table (a historical quote, not a live citation). (d) _OVERRIDE_RE still cannot see a shell-ASSEMBLED path; that is a parser, not a regex, and it is unchanged from the sibling node.
<!-- THOUGHT:END -->

PARENT PROBES (a00-28aa99e2, DH.428), run by me on a COPY of the engine under my scratch dir: probes: gate=bare empty bin/ -> RED naming dir+files+set; subdir-only -> RED; symlink-to-dir -> RED; mode-000 bin -> RED; no bin -> GREEN (not a tautology). probes: auth=bin/other.py (a name driver.sh does not consult) -> RED naming the file and the 3 derived names. probes: wire=driver.sh bytes edited ON DISK in the copy -> the LIVE refusal message drops inject.py; a new $PROJECT_ROOT/bin/branded.py site -> branded.py appears live. probes: negative_wire=rebinding the module global DRIVER did NOT move the message (default arg frozen in __defaults__ at import) -- fragile, not false. probes: negative=a colon citation planted in the shipped FIXTURE is invisible to the scan, which reads only the test file's own source. All four DH.425 residues verified closed on the bytes; verdict inconclusive_lean_proved:85 accepted unchanged.
