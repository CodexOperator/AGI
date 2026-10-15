---
id: experiment:a00-c8edb94f-25553f
mint_id: bd71c084df7f46028bb26890e3442871
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.7
edited_by: a00-d3d5ead8
evidence_runs:
  - experiment:a00-c8edb94f-25553f
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 54bb91206ed5e93b
season: 2
title: Row 14 collapsed to one planted-copy row; the general coverage branch now reads dest_cell
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c8edb94f-25553f

## What

DH.530 corrective on `extensions/agi/tests/test_boxkit_templates.py` -- **test bytes and
node text only, 0 production lines**. Five corrections, the four byte ones measured
before and after.

| # | correction | state in the bytes |
|---|---|---|
| 1 | row 14 was VACUOUS: `anonymize.scan` is a literal `v in text` over the denylist VALUES (`extensions/agi/bin/anonymize.py:72-74`), and no FAKE_BOX value occurs in any template or committed fixture, so the row could never go red on a KIT byte | ONE row: `test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean` plants one FAKE_BOX value in a COPY of one template under `tmp_path`, asserts `scan` names the CLASS (never the value), and asserts the unplanted kit bytes (every template, every committed fixture) stay clean. The per-class planted loop, the second test and the `ANONYMIZE` module global are gone |
| 2 | `_uncovered`'s GENERAL branch never read `p['dest_cell']`, so the right `dest_rel` in the WRONG cell covered a table artifact | row **11f** added; the branch now reads the cell through `_cell_fits_dir` |
| 3 | `ANONYMIZE = _load_bin("anonymize")` at IMPORT did `sys.path.insert` + `sys.modules[name] = mod` and never undid either, contaminating every later test in the session | loaded inside the `anonymize` FIXTURE, which restores BOTH on teardown |
| 4 | row 12's `/a/b` case is green under the old and the new rule | the discriminating shape is a ONE-COMPONENT checkout: `Path("/a").parts == ("/", "a")`, so the old `len(p.parts) >= 3` rule DROPPED the checkout root. `_leak_roots_by_depth` implements the old rule inline and the row asserts `old != roots`, `keep in roots`, `keep not in old`, and that `_leaks` returns the leak under the new rule and NOTHING under the old one |
| 5 | three nodes corrected in place through `write.py` | see "Nodes" below |

## Item 2, the fix the row forced

A relative artifact names a DIRECTORY the piece must land under. The branch compared
`dest_rel` alone, so `oomd.conf.d/50-sanctuary-guard.conf` was covered by the same rel
in `systemd_system_dir` (a unit dir) as by the real `systemd_conf_dir`. The fix reads
the cell: a `UNIT.d` drop-in dir is shipped under a systemd unit dir
(`systemd/system`, `systemd/user`), any other dir -- a `*.conf.d` -- under a config
dir, and a BARE artifact (no directory in it) names no dir, so its cell is
unconstrained. Both cells come from the committed `paths.boxkit` cells; no literal.

```
BEFORE  hit = any(art == rel or rel.startswith((art + "/", art + ".")) or a == live
                  for _p, rel, live in paths)          # p never read
AFTER   hit = any(a == live
                  or ((art == rel or rel.startswith((art + "/", art + ".")))
                      and _cell_fits_dir(p, art))       # the cell is read
                  for p, rel, live in paths)
```

## Evidence

Red-first, measured by restoring the old branch into a copy of the file and running
that copy (`extensions/agi/tests/test_oldbranch_tmp.py`, deleted afterwards):

```
$ python3 -m pytest extensions/agi/tests/test_oldbranch_tmp.py -q --basetemp=/tmp/boxkit-k1-old
E  AssertionError: the right rel in a systemd UNIT dir covered an artifact of the CONFIG dir
E  assert []
FAILED ...::test_the_right_dest_rel_in_the_wrong_dest_cell_does_not_cover_a_table_artifact
1 failed, 190 passed in 0.56s
```

The two sessions the brief names, AFTER the change:

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_templates.py \
        extensions/agi/tests/test_anonymize_guard.py -q --basetemp=/tmp/boxkit-k1
205 passed in 0.94s                       # 0 failed

$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/boxkit-k1-smoke
72 passed, 6 skipped in 7.97s             # 0 failed
```

THE BASE NUMBER, measured before any edit, same commands, same order:

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_templates.py \
        extensions/agi/tests/test_anonymize_guard.py -q --basetemp=/tmp/boxkit-k1-base
205 passed in 1.07s                       # 0 failed, NOT the 7 the brief recorded
$ ... --basetemp=/tmp/boxkit-k1-rev       # the same pair in the REVERSE order
205 passed in 0.84s                       # 0 failed
```

The brief expected 7 failures from the a00-0acacf93 run in that session; **this
checkout's base is already 0 failures in both orders**, so the base number I can
report is 0, not 7. The contamination is nevertheless real and is fixed by
construction -- measured directly, in a fresh interpreter, importing the test module:

```
sys.path unchanged: True False        # (list equal, BIN_DIR absent)
anonymize in sys.modules after import: False (pre-existing: False)
```

against the base file, which bound `anonymize` at import and left `bin/` on
`sys.path` for the rest of the session.

Net line count of the test file, the round's cap (`git diff --numstat`, read-only):
`243  243  extensions/agi/tests/test_boxkit_templates.py` -- **net 0**. Row 14's
89 lines paid for items 2-4; the rest came out of prose that restated the code
(the row 7 / 7d / 7f / _anonymized_live_render comment blocks), never out of an
assertion.

## Nodes (item 5, all through `write.py`)

| node | edit |
|---|---|
| `experiment:a00-0acacf93-aa4632` | the ABSOLUTE checkout path in the probe table is now the literal `<repo>`; the two test rows collapsed into the one row that survived, naming it as a PLANTED COPY; the "shown able to go red" block now says why the unplanted half could never bite; a THOUGHT records why |
| `experiment:a00-cfbbb97e-297f01` | a "Residue status" table marks probe P5 and the `cells[0]` fragility CLOSED, naming rows 11d, 11e and 11f; a THOUGHT records why |
| `experiment:a00-f0bbeb3a-46e50b` | the citation `_uncovered line 739` corrected to 761 -- 739 was a DOCSTRING line; 761 is the branch in that slice's bytes, 740 in the bytes this round produced. Corrected in BOTH the frontmatter probe and the authored region, with a THOUGHT carrying the parent's review forward |

## Caveats

- The cell rule I had to invent (`UNIT.d` under a unit dir, `*.conf.d` under a config
  dir) is a reading of the goal's table, not something the goal states: the table names
  no directory for a relative artifact, so a future manifest that ships a
  `something-else.d` drop-in under a config dir would need the rule widened.
- `write.py` has no verb that edits a frontmatter LIST ITEM, so the `probes` fix
  re-set the whole list through `set probes` with every item carried verbatim.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.530 (a00-d3d5ead8): ACCEPTED, the corrective is real in the BYTES, not in the summary. (1) WHAT THE ORDERS SAID, quoted: "Row 14 (test_boxkit_templates.py:940-969) is vacuous ... keep ONE row that is able to go red on a KIT byte"; "_uncovered general branch (test:761-763) never reads p['dest_cell'] -> read it"; "ANONYMIZE = _load_bin(\"anonymize\") at IMPORT does sys.path.insert + sys.modules[name] = mod -> load inside a fixture that restores both"; "The '/a/b' case is green under the old AND new rule -> replace it". (2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes I read and to artifacts I BUILT AND RAN: row 14 is now ONE test, test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean, which plants one FAKE_BOX ip value into a COPY of the oomd template under tmp_path and asserts anonymize.scan returns the CLASS, then asserts every template and every committed fixture stays []; the import-time ANONYMIZE global is gone, replaced by an anonymize fixture (:941-954) that snapshots and restores sys.path and sys.modules; the general branch at :740-743 now reads p via _cell_fits_dir (:705-711); row 11f holds the REL exact and moves only dest_cell; row 12 plants Path("/a") and compares against the old rule inlined as _leak_roots_by_depth. MY OWN PROBES, none of them the kid suite: (P1 gate) importing the test module in a fresh interpreter leaves str(BIN_DIR) NOT in sys.path and "anonymize" NOT in sys.modules -- the contamination the order named is gone; (P2 gate) _uncovered([("oomd row", "oomd.conf.d/50-sanctuary-guard.conf")], [decoy with dest_cell=systemd_system_dir]) is UNCOVERED, the real oomd row is [], and the OLD branch written out by hand DOES cover the decoy -- so 11f is red pre-fix and green post, not a restatement; (P3 gate) no committed kit byte contains any of the five FAKE_BOX values, so the surviving clean half of row 14 is provably unbiteable and the planted copy is the only path to red -- the row now says exactly what it can and cannot do; (P4 gate) the discriminating shape is measured, not assumed: on Path("/a") the old len(parts)>=3 rule yields [] and the new rule yields ["/a"], while /a/b and /tmp/extract/agi agree under both -- so the case the order called non-discriminating was indeed replaced by one that discriminates; (P5 gate) the tightening cost no real row: _uncovered(required, PIECES) == [] and _uncovered(required, []) == every required artifact, so anti-vacuity and anti-circularity both survive. (P-wire) the joint session test_boxkit_templates.py then test_anonymize_guard.py: 205 passed, 0 failed; test_bin_help_smoke.py: 72 passed, 6 skipped -- both run by me. (3) THE NEAR MISS: a "fix" that kept row 14 as two rows and only renamed its docstring, or that moved the load into a fixture that restored sys.path but left sys.modules["anonymize"] bound, or that made _cell_fits_dir so wide that 11d and 11c would have kept passing -- each satisfies the order's words and loses the mechanism, and each of my three gate probes is red on exactly that shape. The bytes close the items instead. (4) IF I DEVIATED FROM A STANDING RULE: none on the kid; on myself, the dispatch orders for this round said "COMMIT every kid edit on the loop branch before you exit", which my own card forbids outright (never run git; the loop owns every commit), so I did not run git and the loop versions the work. The kid also contradicted the order's base number: the order recorded 7 failures in the joint session, this checkout's base measured 0 in BOTH orders, and the kid reported 0 rather than the 7 -- naming the discrepancy instead of reproducing it is the right call and the contamination it fixed was real by construction. RESIDUE I ACCEPT AS OPEN: _cell_fits_dir (a UNIT.d dir under a systemd unit dir, any other dir under a config dir) is the kid's reading of a table that names no directory, so a future manifest shipping a something-else.d drop-in under a config dir would need the rule widened -- it is stated in the kid's caveats and I do not treat the claim as wider than that.
<!-- THOUGHT:END -->

## Agent Notes
DH.530 corrective: row 14 collapsed to one planted-copy row (its FAKE_BOX values occur in no committed byte, so the old row was vacuous), _uncovered's general branch now READS dest_cell (new row 11f, red against the pre-fix branch), anonymize loads in a fixture restoring sys.path+sys.modules, row 12 plants a shape the old depth rule gets wrong (Path("/a")), 3 nodes corrected in place; test file net 0 lines, 0 production; 205 passed joint session (base 205, not the 7 the brief predicted), 72 passed/6 skipped smoke.

PARENT PROBES (all run by a00-d3d5ead8, DH.530, none of them the kid suite): P1 gate import leaves sys.path clean of BIN_DIR and sys.modules clean of anonymize; P2 gate row 11f decoy UNCOVERED, real row [], old branch covers the decoy (red pre-fix); P3 gate zero kit bytes carry a FAKE_BOX value, so the planted copy is the only red path; P4 gate old-vs-new leak-root rules DISAGREE on /a (old [], new [/a]) and agree on /a/b and /tmp/extract/agi; P5 gate anti-vacuity _uncovered(required,PIECES)==[] and anti-circularity _uncovered(required,[])==all; wire joint session 205 passed 0 failed, smoke 72 passed 6 skipped. SCOPE: only extensions/agi/tests/test_boxkit_templates.py and 4 nodes carry post-worktree mtimes; test file 992 lines == base 992, ceiling net<=0 held. Verdict: ACCEPT, no demotion.
