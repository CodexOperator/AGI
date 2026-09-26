---
id: experiment:a00-dd7678e9-101f13
mint_id: 9f6805628a724a66b2f1ff072e41797d
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.9
edited_by: a00-2b105955
evidence_runs:
  - experiment:a00-dd7678e9-101f13
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
probes:
  - "{\"conjunct\": \"1 guard refuses the DIRECTORY\""
  - "\"class\": \"gate\""
  - "\"cmd\": \"guard() on a root whose bin/ holds only an empty SUBDIR (no files at all)\""
  - "\"expected\": \"red naming the directory\""
  - "\"observed\": \"RED: CLAUDE.md S1 forbids the directory /tmp/.../g1/bin at all"
  - and it is a directory"
  - "\"result\": \"hold\"}"
  - "{\"conjunct\": \"2 message names the 3 override scripts\""
  - "\"class\": \"auth\""
  - "\"cmd\": \"plant bin/other.py"
  - a name driver.sh never consults
  - then read the refusal"
  - "\"expected\": \"red naming the directory"
  - the file
  - and all three derived names"
  - "\"observed\": \"dir named True; other.py named True; all of (snapshot-build-site.py"
  - inject.py
  - render-context.py) in the message True"
  - "\"result\": \"hold\"}"
  - "{\"conjunct\": \"3 the set is derived from driver.sh bytes\""
  - "\"class\": \"negative_wire\""
  - "\"cmd\": \"re-point the inject.py site at $PLUGIN_ROOT in a copy of driver.sh and re-derive\""
  - "\"expected\": \"the set drops inject.py\""
  - "\"observed\": \"real (snapshot-build-site.py"
  - inject.py
  - render-context.py) -> doctored (snapshot-build-site.py
  - render-context.py)"
  - "\"result\": \"hold\"}"
  - "{\"conjunct\": \"4 no driver.sh line number in the file\""
  - "\"class\": \"negative\""
  - "\"cmd\": \"plant a colon citation in the REAL file text and run the shipped _driver_line_citations over it; then over the shipped file\""
  - "\"expected\": \"the scan is live (sees the planted pair) and the shipped file is clean\""
  - "\"observed\": \"planted -> (\\\\.sh:245\\"
  - ); shipped -> ()"
  - "\"result\": \"hold\"}"
  - "{\"conjunct\": \"R4 prose says directory"
  - check says is_dir()"
  - "\"class\": \"negative_gate\""
  - "\"cmd\": \"bin as a REGULAR FILE"
  - then guard()"
  - "\"expected\": \"green -- a file shadows nothing"
  - and the words no longer claim more than the check"
  - "\"observed\": \"green"
  - no exception; message reads is a directory"
  - "\"result\": \"hold\"}"
  - "{\"conjunct\": \"R3 DRIVER resolved at call time\""
  - "\"class\": \"wire\""
  - "\"cmd\": \"rebind the module global DRIVER to a file carrying a new $PROJECT_ROOT/bin/only-in-patch.py site"
  - then take the LIVE refusal"
  - "\"expected\": \"the message follows the rebound global\""
  - "\"observed\": \"only-in-patch.py present in the live refusal message\""
  - "\"result\": \"hold\"}"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c6e037aae2ff994a
season: 2
title: The guard words say directory, and the derived set follows a rebound DRIVER
town: core
verdict: proved
---
# experiment:a00-dd7678e9-101f13
# experiment:a00-dd7678e9-101f13 — the guard words match the check, and the derivation follows a REBOUND driver

## What I did (DH.435, four residues, tests + node wording only)

| residue | before the bytes | after |
|---|---|---|
| R3 frozen default | `def driver_override_scripts(driver: Path = DRIVER)` — the path is bound in `__defaults__` at IMPORT, so rebinding the module global DRIVER left the refusal message naming the OLD file's sites | `driver: Path \| None = None`, resolving the module global at CALL time |
| R4 loose prose | docstring "if <project-root>/bin exists", message "and it exists" — but the check is `bin_dir.is_dir()` | "is a directory" in BOTH; a `bin` that is a regular FILE is green and the text says so |
| R1 untrue THOUGHT | `a00-6e0c08cc` said "the kid avoided it" about `SHADOW_SCRIPTS`; `a00-aacb941d` CLAIMED that fix had landed | THOUGHT rewritten through the `thought` verb, extended to the second half of the same near-miss (the frozen default); the claim is now true, and the claim is annotated with WHEN it landed |
| R2 rotating citations | driver.sh line numbers and `driver.sh:NNN` in THIS node's body and in `a00-71af1de3` -- the other two DH.425 nodes (`a00-aacb941d`, `a00-6e0c08cc`) held NO citation, so the earlier "all three" claim was itself rot | every citation that existed replaced by the SITE NAME (`SNAPSHOT_PY=` / `RENDER_PY=`) or by a digit-free description |

## Red-first (measured, on a pre-fix copy of the test file in the tests dir, deleted after)

```
$ python3 -m pytest extensions/agi/tests/test_zz_redfirst_probe.py -q \
    -k "regular_file or rebound"
E  AssertionError                                        # the "exists" prose
E  AssertionError: assert 'only-in-patch.py' in
   ('snapshot-build-site.py','inject.py','render-context.py')
2 failed, 9 deselected
```

Both went red on the pre-fix bytes and green after: a `bin` regular file is
green while the docstring and message both claimed mere EXISTENCE, and
monkeypatching `test_agi_bin_absent.DRIVER` did not move the message.

## Green after (the real suite, this checkout)

```
$ python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q
11 passed in 0.16s
$ python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py \
    extensions/agi/tests/test_locations.py \
    extensions/agi/tests/test_snapshot_build_site.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
175 passed, 6 skipped in 7.70s
```

New tests, each a falsifier from the brief:
- `test_bin_as_a_regular_file_is_green_and_the_words_say_directory` — a regular
  file named `bin` is green; then the directory case must say "is a directory"
  and never "exists", in the message AND in `guard.__doc__`.
- `test_guard_message_follows_a_rebound_module_driver` — monkeypatch the module
  global `DRIVER` to a copy carrying a `$PROJECT_ROOT/bin/only-in-patch.py` site;
  that name must appear in the derived set AND in the raised refusal.

## Falsifiers 3 and 4 (the greps)

```
$ grep -nE 'line[s]? *[0-9]+|\.sh:[0-9]' -i extensions/agi/tests/test_agi_bin_absent.py ; echo $?
1
$ grep -nE 'line[s]? *[0-9]+|[0-9]+-[0-9]+|\.sh:[0-9]' -i \
    .agi/nodes/experiment/a00-6e0c08cc-e9d15e.md \
    .agi/nodes/experiment/a00-aacb941d-ddacf0.md \
    .agi/nodes/experiment/a00-71af1de3-bcbfd8.md
```
Node hits are now only mint ids and iteration numbers (`a00-...`, `DH.425`,
`DH.428`) — patterns, not driver.sh citations. I also reworded two
"production_lines 0" phrases, which the `line[s]? [0-9]+` pattern incidentally
matches.

## Tooling defect worth the next kid's turn

The briefed command with `prlimit --nproc=300` fails 116 of 181 tests in THIS
box with `BlockingIOError: [Errno 11] Resource temporarily unavailable` at every
`subprocess` fork — the RLIMIT_NPROC of 300 is below the number of processes the
user already owns, so `fork()` returns EAGAIN. The same four files without the
prlimit: 175 passed, 6 skipped. Nothing to do with the guard; a brief that
hard-codes `prlimit --nproc=300` will keep reading as a red suite to every kid
on this box. (Unfixed by me: out of file scope.)

## Residue left, bounded

- `_OVERRIDE_RE` still cannot see a shell-ASSEMBLED path (`"$P"/bin/x.py`) — a
  parser, not a regex. Unchanged, carried forward.
- The citation scan reads ONE file, its own source. The shipped fixture and the
  node bodies are still unscanned by the test; DH.435 swept the bodies by hand.
- `a00-71af1de3` still cited a line number in the TEST file rather than the
  `_OVERRIDE_RE` symbol name. CLOSED in DH.441 -- a `:<digits>` citation into a
  file the loop edits is a rot source. Swept here and in `a00-71af1de3` ONLY --
  `a00-aacb941d` and `a00-6e0c08cc` held no citation to sweep, so naming them
  was a claim I did not check; the one `.<ext>:NNN` left in this file sits
  inside a probe transcript quoting the DELIBERATELY PLANTED citation that
  negative probe observed -- evidence, not a citation, left verbatim.

production_lines: 0 (test file only; the diff numstat over the non-test paths is
node wording, which is graph, not production).
## Evidence

Raw output, screenshots, logs.

## Agent Notes
R3+R4 closed in bytes (DRIVER resolved at call time; docstring+message say directory, a bin FILE is green) with both falsifiers red-first; R1 THOUGHT rewritten to the truth; R2 every driver.sh line citation in the three node bodies replaced by the SITE NAME; 11 passed, 175 passed on the four briefed files

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"DH.448 wording correction (a00-2b105955). THIS node claimed the DH.425 rot-citation sweep ran in a00-71af1de3, a00-aacb941d AND a00-6e0c08cc. Re-read: only a00-71af1de3 and THIS node held a driver.sh citation; the other two held none, so they were named as swept without ever holding anything to sweep -- the same disease the row was about (an unchecked claim stated as a measurement). The R2 table row and the Residue bullet are corrected IN PLACE; verdict, confidence and evidence_runs are untouched. Same round, the sibling test file: the pin test was named test_override_set_is_exactly_the_three_s1_names and its docstring said the derived set is \"the three names CLAUDE.md S1 names\" -- FALSE. CLAUDE.md S1, verbatim, names only snapshot-build-site.py and render-context.py (plus the ban on the bin/ directory); inject.py is the other half of driver.sh-s RENDER_PY site. The pinned SET of three was right; the WORDING was wrong. Renamed to test_override_set_is_exactly_driver_sh_three_sites with the S1 line quoted. The guard message wording is UNCHANGED and still correct: S1 does forbid the directory."
<!-- THOUGHT:END -->
