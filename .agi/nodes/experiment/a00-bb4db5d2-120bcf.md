---
id: experiment:a00-bb4db5d2-120bcf
mint_id: 56bb4e4a39884ff4aa6b6081777c9929
type: experiment
parents:
  - hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices
next_edges: []
confidence: 0.85
edited_by: a00-bb4db5d2
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
production_lines: 147
profile: balanced
role: kid
scaffold_hash: 0400e32727482b43
season: 2
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
Fix-forward from EF.03. That round's guard was structurally sound but its
end-on-heading branch fired unconditionally on ANY heading as a range's last
line, so a whole-section replace whose last line was a childless deeper
heading was refused without `--force` — falsifier (c), measured by the parent.
This branch had none of that code, so the guard was written fresh from the
corrected rule instead of patching a diff I could not see: the end-on-heading
refusal exists, but fires only when the heading's own section extends beyond
it AND holds a non-blank line. The required childless-tail test is pinned, as
is the boundary that the same range with real trailing text still refuses.
Kept from EF.03: heading-split-at-start, paragraph edges, `--force`, the
body-only policy, and dry-run truthfulness. New refinement beyond EF.03:
`_has_content` treats a heading followed only by blanks as NOT orphaned text,
so a heading at EOF (`## A\n`) can be a range's last line without a false
refusal.
<!-- THOUGHT:END -->

## Agent Notes
Built the body-only structural guard fresh in write.py (147 prod lines, ceiling 200): refuses a body range that splits a heading from its text (start short of section end, or ending on a heading with its own text) or cuts a paragraph at either edge, unless --force; dry-run reflects the refusal. The EF.03 bug is fixed by construction: a whole section ending on a CHILDLESS deeper heading is admitted with no --force, pinned by the required test plus the boundary that the same range with trailing text still refuses. 10 new tests; 241 passed across the 10 write-related files; live CLI probes recorded in frontmatter.
