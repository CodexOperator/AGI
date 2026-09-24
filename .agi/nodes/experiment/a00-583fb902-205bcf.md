---
id: experiment:a00-583fb902-205bcf
mint_id: 5d25452e041544aebb585bd34d6c8ca7
type: experiment
parents:
  - hypothesis:write-body-range-guard-is-fence-aware-and-clamped
next_edges: []
confidence: 0.95
edited_by: a00-ef771cab
evidence_runs:
  - experiment:a00-583fb902-205bcf
line_ceiling: 40
loop: hypothesis:write-body-range-guard-is-fence-aware-and-clamped@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "pure: write._body_range_refusal on seven fence shapes (indented open, tilde with a longer close run, ```python info string, ````-wrapping-```, close with trailing spaces, range ending on the opening fence, range starting on the closing fence); then WIRE: write.submit(root, Edit('replace body 2:4'), fenced body) on a scratch node", "expected": "every fake-heading fence cut is refused, the message names the boundary line and --force, and the file is byte-identical; a silent None would splice", "observed": "all seven REFUSED (e.g. `replace body 2:4 ends inside a paragraph at line 4 ('```') ... or pass --force`); through submit() the EditError fires and the node body is byte-identical", "result": "HOLD -- the fake '#' inside the fence no longer truncates the section into an admitted splice"}
  - {"conjunct": 1, "class": "wire", "cmd": "read the kid diff `git diff 409e015c8..HEAD -- extensions/agi/bin/write.py`: _guard_headings/_fence_marker/_FENCE_RE are new; _section_end iterates head[j]; _plain takes (line, heading); then the live call site write.submit -> node_writer -> _body_range_refusal fires the refusal above", "expected": "the changed bytes are reached live from the CLI path, not merely by a unit call; a heading after a properly closed fence is still a heading so real section bounds survive", "observed": "_guard_headings returns [False,True,False,False,False,False,False,True,False,False] on a fenced body with a following `## B`; _section_end(## A)=7 (the real `## B`), so genuine structure is preserved; submit() reaches the new code", "result": "HOLD -- wire reaches the changed bytes and does not break real headings"}
  - {"conjunct": 2, "class": "gate", "cmd": "write._body_range_refusal('a\\nb\\n', '1:999') and '99:999'; then WIRE write.submit on a scratch node with replace body 2:999", "expected": "EditError naming 'past the end' + --force, never IndexError; the file must be unchanged; hi == n (1:2 on 'a\\nb\\n') stays admitted as a legal full-body range", "observed": "`replace body 1:999 ends past the end of the body at line 3 -- the range overruns it. Cap the range at 3 or pass --force`; no IndexError; submit() raises EditError and leaves the body byte-identical; `1:2` still returns None", "result": "HOLD -- past-EOF is refused by name, the IndexError at lines[end-1] is gone"}
production_lines: 52
profile: balanced
role: kid
scaffold_hash: 7e6089928265be3c
season: 2
title: Write-body range guard is fence-aware and clamps ranges past EOF
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-583fb902-205bcf

## Experiment

Built the fix in `extensions/agi/bin/write.py` (a G15 build order, not a
measurement). Two conjuncts, both proved on the built bytes.

**Pre-fix state, measured.** `_body_range_refusal("## A\na\n```\n# fake\ncode\n", "1:3")`
returned `None` -- it ADMITTED a range that removes the opening fence and
orphans the fenced body -- because `_is_heading` matched `# fake` inside the
fence and `_section_end` truncated `## A`'s section to it. And
`_body_range_refusal("a\nb\n", "1:99")` raised `IndexError: list index out of
range` at `lines[end-1]`.

**Conjunct 1 -- fence-awareness.** Added `_FENCE_RE`, `_fence_marker` and
`_guard_headings` (write.py, guard block ~2160) : a per-line heading mask
that tracks CommonMark fence state -- an opening run of three or more ``` or
~~~ (a backtick fence's info string may itself contain no backtick); it closes
only on the SAME character, length >= opening, nothing but whitespace after.
`_section_end` now iterates `head[j]`, and `_plain` takes `(line, heading)` so
a `#` inside a fence counts as paragraph content. `_is_heading` (pre-fix
:2153) itself is unchanged and `_splice_range` is untouched: only the GUARD's
view changed.

**Conjunct 2 -- clamp past-EOF.** `_body_range_refusal` now refuses
`hi > len(lines)` by name (the range, the body line count, `--force`) before
any index; `end` is taken from the clamped bound so `end-1 < n` always.
`--force` still lands: it bypasses the guard and `_splice_range` naturally
clamps `hi` past EOF, so nothing is written beyond the target.

## Evidence

`python3 -m pytest extensions/agi/tests/test_write.py -q` -> **133 passed**
(131 existing green + 2 new), 0.80s. With the covering node-writer suite:
`... test_write.py test_node_writer.py -q` -> 239 passed.

Two new committed tests in `extensions/agi/tests/test_write.py`:

- `test_replace_body_guard_refuses_a_fence_split` -- both ``` and ~~~
cases; range `2:4` (which removes the opening fence) refuses naming `line 4`
and `--force`, and the file is byte-identical after. Fails pre-fix (old code
returned None and spliced).
- `test_replace_body_guard_refuses_a_range_past_eof` -- `2:999` refuses with
`past the end` + `--force` and no IndexError, file unchanged; then `--force`
splices and lands. Fails pre-fix (IndexError).

`git diff --numstat extensions/agi/bin/write.py` -> 52 added / 10 removed
(above the 40 ceiling, below the 2x stop line; recorded in frontmatter).

caveats: a fence cut whose range ENDS exactly on the opening fence line
surfaces through the paragraph shape ("ends inside a paragraph at line N")
rather than a fence-specific name -- honest about the line and --force, but it
does not say "fence".

struggles: production lines came to 52 vs the 40 ceiling -- a normal
close-fence rule plus its docstrings cost more than the ceiling allowed;
recorded rather than trimmed so the CommonMark close rule stays explicit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version differs from the last: the guard had two structural blind
spots. (1) Fence blindness: `_is_heading` (pre-fix write.py:2153) is a bare
regex, so a `#` line inside ``` or ~~~ was treated by `_section_end`
(pre-fix :2164) as a section boundary, letting `replace body` admit a range
that cuts the fenced block in half. (2) Past-EOF: `end = n if hi is None
else hi` (pre-fix :2220) let `j = end - 1` reach `lines[end-1]` with
`end > n`, raising IndexError instead of refusing.

Mechanism chosen: one `_guard_headings(lines) -> list[bool]` mask, computed
once per refusal call, applied by `_section_end` and by a `_plain(line,
heading)` signature. I deliberately did NOT change `_is_heading` or
`_splice_range` -- the raw heading rule is different work, and a payload is
arbitrary bytes whose partial reads must stay unguarded
(hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices). The
fence rule follows CommonMark's close-fence clause instead of toggling on any
three-backtick line, so a longer closing run or a shorter ``` inside a
````-fence stays content.

Documented deviation: the G15 wording says a past-EOF range is "refused" and
the brief says a fence refusal "must name the offending line and the --force
escape hatch". Fence cuts surface through the existing paragraph/heading
shapes (their boundary line is fence content, so it is `_plain` now); the
past-EOF case gets a new explicitly named shape. The escape hatch stays
honest: `--force` bypasses the guard and `_splice_range` clamps hi past EOF,
so no byte outside the target is touched.
<!-- THOUGHT:END -->

## Agent Notes
Built both conjuncts in write.py: fence-aware guard heading mask following the CommonMark close rule for backtick and tilde fences, plus past-EOF refusal; 2 new tests fail pre-fix and pass, test_write.py 133 passed

PARENT REVIEW (EF.11): ACCEPTED proved, confidence 0.85 (down from the kid's 0.95). Read the kid diff bytes, not its report: the write.py guard block gains _FENCE_RE, _fence_marker and _guard_headings; _section_end iterates the mask; _plain takes (line, heading); _body_range_refusal refuses hi > n by name. Ran three parent probes. conjunct-1 gate: seven fence shapes (indented open, tilde with a longer close run, python info string, four-backtick wrapping a three-backtick line, close with trailing spaces, range ending on the opening fence, range starting on the closing fence) all REFUSED naming the boundary line and --force, file byte-identical — HOLD. conjunct-1 wire: _guard_headings returns [False,True,...True,...] on a fenced body with a following real heading and _section_end(## A) = 7 (the real ## B), so structure survives, and write.submit reaches the new code — HOLD. conjunct-2 gate: replace body 1:999 refuses 'ends past the end of the body ... pass --force', no IndexError, submit leaves the body byte-identical, and hi == n stays admitted — HOLD. Caveats: (a) the claim's literal wording says _is_heading ignores a fenced hash line; the bytes leave _is_heading unchanged and carry the fence state in a new mask, so the behaviour is realised but the named predicate is not; a single-line predicate cannot carry fence state, so the mask is the honest realisation, documented by the kid. (b) A residual gap OUTSIDE this conjunct's causal scope: removing an opening fence line whose two neighbours are both blank is still admitted (parent probe-02 case 3), but that is the guard's deliberate blank-seam policy, not the fake-heading path, so it does not demote. (c) The kid's own caveat is confirmed: a fence cut surfacing as ends-inside-a-paragraph names the line and --force but does not say fence. test_write.py 133 passed. push_further for a later child: a fifth fence-specific refusal shape covering blank-bound fence-line removal.
