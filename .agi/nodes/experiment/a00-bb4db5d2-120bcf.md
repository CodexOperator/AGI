---
id: experiment:a00-bb4db5d2-120bcf
mint_id: 56bb4e4a39884ff4aa6b6081777c9929
type: experiment
parents:
  - hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices
next_edges: []
confidence: 0.85
edited_by: a00-1e2bdb76
evidence_runs:
  - experiment:a00-bb4db5d2-120bcf
line_ceiling: 200
loop: hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "fixture body line1 blank, line3 ## A, line5 childless ### A.1, line6 ## B; CLI dry-run replace body 3:5 -", "expected": "admitted with no --force (falsifier (c) fixed)", "observed": "exit 0, admitted, dry-run writes nothing", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "same fixture, CLI dry-run replace body 3:4 - (starts on ## A, stops short)", "expected": "refused, names the heading and --force", "observed": "exit 2: starts on the heading ## A but stops before the end of its section (line 5)", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "printf X | CLI replace body 3:4 --force - on the scratch node, then read body", "expected": "--force threads parse_script -> verb_replace -> submit and lands the partial edit", "observed": "updated: hypothesis:h2; body reads # T / X / ### A.1 / ## B / beta", "result": "PASS"}
  - {"conjunct": 3, "class": "gate", "cmd": "test_replace_body_guard_refuses_ending_on_a_heading_with_content: ### A.1 with a1text, range 4:5", "expected": "refused -- the false-positive boundary", "observed": "EditError naming the heading; node bytes unchanged", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "_body_range_refusal on director fixture '# T/## A/intro/### A.1/## B/beta', range 3:4; and live CLI 'replace body 3:4 -' on a scratch node", "expected": "refused, refusal names the heading split, node bytes unchanged", "observed": "REFUSED: \"starts on the heading '## A' but stops before the end of its section (line 5)\"; CLI exit 2, node unchanged", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "full '## A' section 2:5 of body '## A/intro/### A.1/a1text/## B/beta' (last child HAS content); whole paragraph 4:6 of '# T/## A/alpha one/alpha two/tail/## B/beta'", "expected": "no refusal -- the documented whole-paragraph / whole-section case is unchanged", "observed": "both ADMITTED; CLI 'replace body 3:5 -' landed on the scratch node (exit 0)", "result": "PASS"}
  - {"conjunct": 3, "class": "gate", "cmd": "EF.03 falsifier: full '## A' section 3:5 of '# T/## A/intro/### A.1/## B/beta' (childless deeper-heading tail); boundary: same + 'a1text' under ### A.1", "expected": "childless tail ADMITTED with no --force; with-content boundary REFUSED", "observed": "ADMITTED; REFUSED naming the heading split -- the fix is narrow, not disabled", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "printf X | write.py hypothesis:h2 'replace body 3:4 -'; then 'replace body 3:4 --force -' --root scratch", "expected": "no-force exits 2 and leaves the node unchanged; --force exits 0 and lands exactly the partial edit", "observed": "exit 2 unchanged; exit 0 'updated', body '# T/FORCED/### A.1/## B/beta' (### A.1 survives)", "result": "PASS"}
production_lines: 147
profile: balanced
role: kid
scaffold_hash: 0400e32727482b43
season: 2
thought_session: EF.04
title: "replace body structural guard (fix-forward): refuses heading splits and paragraph tails, admits a whole section ending on a childless deeper heading"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bb4db5d2-120bcf

## Experiment

**G15 build order, not a measurement (fix-forward from EF.03).** The dispatch
is a fix-forward: EF.03 (`experiment:a00-29883877-7abb3b`) built the same guard
and its own falsifier (c) caught it refusing a whole-section replace whose last
line was a childless deeper heading. This branch did not contain that version,
so the guard was built FRESH, correctly, rather than patched.

What I did, in `extensions/agi/bin/write.py`:

1. **`_body_range_refusal(text, rng)`** (new, beside `_splice_range`). It reads
the SAME body text `read body` shows and refuses four shapes before any
splice, each naming the offending line:
   - (a) the range STARTS strictly inside a paragraph (its line and the line
     before are both plain text);
   - (b) the range ENDS strictly inside a paragraph (its line and the line
     after are both plain text);
   - (c) the range STARTS on a heading but stops before the end of that
     heading's own section, orphaning non-blank text (bounded `hi` only —
     `N:` is open to EOF and always covers the section);
   - (d) the range ENDS exactly on a heading whose own section still holds
     non-blank text — the heading is removed while its text survives.
   Heading detection is one strict CommonMark rule, `_HEADING_RE =
   ^ {0,3}#{1,6}(\s|$)`, and `_section_end` walks to the next heading of the
   same-or-higher level (or EOF). `_has_content` ignores blank lines, so a
   heading followed only by blanks is not "orphaned text" — the body always
   ends in a newline and punishing that would be a false positive.
2. **The correction EF.03 named.** The end-on-heading refusal (d) fires ONLY
   when `_section_end(lines, j) > j + 1` AND that section holds a non-blank
   line: a childless deeper heading (`### A.1` with nothing under it before
   the sibling `## B`) is the correct, complete tail of the outer section and
   is ADMITTED with no `--force`. The EF.03 blanket end-on-heading branch is
   gone by construction.
3. **Where the policy lives.** `_splice_range`/`_slice_range` stay pure line
   arithmetic, so `read body N:M` still reads any partial range. The guard
   runs on the WRITE path only, in `submit`, after `_target_text` has the
   current body and before `_splice_range`, and only for `replace_target ==
   "body"`; a payload is arbitrary bytes and is never structure-checked.
4. **`--force`**, the explicit consent: `Edit.replace_force` (new field),
   spelled `replace body 4:9 --force -` (a prefix on the source argument,
   parsed in `verb_replace`, so the positional range/source grammar is
   unchanged). Only a `--force ` prefix is consumed — a bare `--force` stays a
   path and refuses loudly rather than silently deleting the range.
5. **`--dry-run` made truthful.** The guard also runs in main's dry-run
   preview, so a refused body replace exits 2 with the refusal instead of
   printing `admitted` and then failing on the real write.

The `--at` anchor form was not built: the hypothesis's claim is an OR, so the
structural guard alone satisfies it, and `--at`'s repeated-heading half of
falsifier (a) does not apply to code with no `--at`.

The tests, in `extensions/agi/tests/test_write.py` (ten, all green):

- `test_replace_body_guard_refuses_a_heading_split` — the ABL.01 shape; the
  refusal names `heading` and `--force`; node bytes unchanged.
- `test_replace_body_guard_refuses_a_paragraph_tail` — start-interior and
  end-interior each refused, node byte-identical.
- `test_replace_body_guard_allows_a_whole_paragraph` — no false positive.
- `test_replace_body_guard_allows_a_whole_section` — heading to the blank
  before the next heading lands.
- `test_replace_body_guard_admits_a_childless_deeper_heading_tail` — **the
  required new test.** Fixture body `\n# T\n## A\nintro\n### A.1\n## B\nbeta`
  (line 3 is `## A`, line 5 is `### A.1`); range 3:5 is the full `## A`
  section ending on the childless deeper heading; ADMITTED with no `--force`,
  `## B`/`beta` intact.
- `test_replace_body_guard_refuses_ending_on_a_heading_with_content` — the
  false-positive BOUNDARY: the same range is refused when `### A.1` has text
  of its own; a section stopping short of `## A`'s end is refused too.
- `test_replace_body_guard_allows_a_whole_body_open_range` — `1:` admitted.
- `test_replace_body_guard_honours_force` — the refused split lands with
  `--force`, admitting exactly the partial edit asked for.
- `test_replace_body_guard_reflects_in_dry_run` — dry-run exits 2 with the
  refusal, `admitted` absent, node untouched.
- `test_replace_body_guard_leaves_a_payload_alone` — payload policy boundary.

## Evidence

Suite, and output:

```
$ python3 -m pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_master_sensei.py \
    extensions/agi/tests/test_write_guard.py extensions/agi/tests/test_write_actor_rows.py \
    extensions/agi/tests/test_write_dotted_key.py extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_write_veto_gate.py extensions/agi/tests/test_write_ring_cli.py \
    extensions/agi/tests/test_body_patch.py extensions/agi/tests/test_ring_cli_seam.py -q
241 passed, 135 warnings in 2.68s
```

Live CLI probes on the real graph (dry-run writes nothing):

```
$ printf 'X\n' | write.py goal:g14.14.1 'replace body 4:5 -' --dry-run --actor kid --session demo
exit=2
ERR: replace body 4:5 starts on the heading '## Agent Notes' but stops before the end of its
section (line 15) -- that splits the heading from its text. Widen the range or pass --force

$ printf 'X\n' | write.py goal:g14.14.1 'replace body 4:5 --force -' --dry-run --actor kid --session demo
exit=0 admitted
```

Scratch-graph wire probe, the falsifier (c) case and its boundary:

```
--- childless tail 3:5 (must be admitted) ---
exit=0   replace body 3:5 admitted
--- real split 3:4 (must refuse) ---
exit=2   starts on the heading '## A' but stops before the end of its section (line 5)
--- real split 3:4 --force (must admit) ---
exit=0   admitted
--- wire: actually write 3:4 --force, then read body ---
updated: hypothesis:h2
# T
X
### A.1
## B
beta
```

Production lines, measured with the one allowed read-only `git diff --numstat`:

```
$ git diff --numstat -- extensions/agi/bin/write.py
147	4	extensions/agi/bin/write.py     # 147 added, ceiling 200 — under
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, EF.04 — accepted the kid's proved (0.85); no demotion.

WHAT THE INSTRUCTION SAID (director-engine fix-forward): "the end-on-heading refusal must only fire when that heading's OWN section (i.e. _section_end(lines, j) for j = hi-1) extends beyond line j itself -- meaning the heading being cut off actually has trailing content the range would silently orphan."

WHAT THE MACHINE ACTUALLY DOES (read from the committed bytes at 231244dc0, then run by me). The end branch is now: j = end - 1; if _is_heading(lines[j]): sec = _section_end(lines, j); if sec > j + 1 and _has_content(lines, j + 1, sec): return refusal. The unconditional EF.03 branch is gone. On the director's own fixture '# T/## A/intro/### A.1/## B/beta', range 3:5 is ADMITTED (the childless ### A.1 tail); the same range REFUSES when ### A.1 carries 'a1text' -- so the branch was narrowed, not disabled. A full ## A section whose last child HAS content (2:5) is admitted, as is a nested childless chain (2:4). Wire probe: CLI 'replace body 3:4 -' exits 2 with the split named and leaves the node byte-identical; 'replace body 3:5 -' lands; 'replace body 3:4 --force -' lands the partial edit with ### A.1 surviving. The 10 tests are in the diff; I ran the 10-file write suite: 241 passed, so falsifier (b) does not fire.

THE NEAR MISS. A plausible implementation satisfies the words and loses the mechanism: use 'sec > j + 1' alone. That treats a heading followed only by blank lines (a heading at EOF, which the body's trailing newline creates) as a split and re-refuses the childless tail through a different door. The kid's _has_content(lines, j+1, sec) ignores blanks, which is why '## A/### A.1/<blank>' is admitted.

DEVIATIONS, none demoting. (1) The guard is body-only policy in submit plus main's dry-run, not literally inside _splice_range/_parse_range as the claim's wording names -- that is the mechanism preserved, so a partial read stays unguarded and the transform stays pure line arithmetic. (2) No --at anchor was built; the claim is an OR and the guard is (ii). RESIDUAL GAP carried, not demoted: _is_heading is fence-blind -- a '#' line inside a ``` code fence reads as a heading and can move _section_end, so a range cutting a code block in half is not refused; no falsifier in the claim names a fence.
<!-- THOUGHT:END -->

## Agent Notes
Built the body-only structural guard fresh in write.py (147 prod lines, ceiling 200): refuses a body range that splits a heading from its text (start short of section end, or ending on a heading with its own text) or cuts a paragraph at either edge, unless --force; dry-run reflects the refusal. The EF.03 bug is fixed by construction: a whole section ending on a CHILDLESS deeper heading is admitted with no --force, pinned by the required test plus the boundary that the same range with trailing text still refuses. 10 new tests; 241 passed across the 10 write-related files; live CLI probes recorded in frontmatter.
