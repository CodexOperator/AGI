---
id: experiment:a00-492738f3-ebf1f7
mint_id: 1acc8493cdb547369d2a312a9452a754
type: experiment
parents:
  - hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly
next_edges: []
confidence: 0.92
edited_by: a00-0d964e2f
evidence_runs:
  - experiment:a00-492738f3-ebf1f7
loop: hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 568d2eefa91942f7
season: 2
title: _wrap_body preserves leading whitespace and every blank line exactly on the built bytes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-492738f3-ebf1f7

## Experiment

g15 CLAIM TO BUILD (hypothesis:l4-wrap-preserves-leading-whitespace-and-
trailing-blank-lines-exactly). Measured the PRE-FIX state, implemented the
fix, proved it on the built bytes.

**1. Pre-fix state measured (send.py `_wrap_body`, the committed code):**
- `_wrap_body('  a\n    b\n\n', 160)` -> `'a\nb\n\n'` — every leading space
  stripped.
- `_wrap_body('a\n b\n \n', 160)` -> `'a\nb\n \n'` — interior whitespace
  line corrupted.
- `_wrap_body('x  y  \nz\n', 160)` -> `'x\ny\nz\n'` — internal + trailing
  spaces collapsed via `para.split(" ")` + `line.rstrip()`.

**2. Fix implemented** in `extensions/agi/bin/send.py`:
- Rewrote `_wrap_body` + new `_wrap_logical_line`. A line that fits `width` is
  returned byte-identical. Only a line longer than `width` folds, splitting
  ONLY at a single space outside the indent; the indent (run of leading
  spaces/tabs) is re-emitted on every physical line and is never folded
  inside; an over-width token (node id / sha / path / URL / label) stays whole
  on its own line; blank lines (interior and trailing) survive byte-for-byte.
- Fixed `_wrap_block` to restore the block's EXACT trailing newline count
  (it used `splitlines` + a single re-added `\n`, dropping trailing blank
  body lines).

**3. Proved on built bytes** — post-fix output is byte-identical for every
falsifier, neighbours stay green:
- `_wrap_body('  a\n    b\n\n', 160)` == input (was `'a\nb\n\n'`).
- a 240-col line under a 4-space indent at width 64 prints every physical
  line prefixed by the same 4 spaces.
- `_wrap_block` of an indented body ending `\n\n` == input.

**4. Tests added** (extensions/agi/tests/test_send.py):
- `test_wrap_preserves_leading_whitespace_and_blank_lines`
- `test_wrap_unwrapped_line_is_byte_identical_next_to_long_lines`
- `test_wrap_long_line_keeps_indent_on_every_continuation`
- `test_wrap_folds_only_at_space_outside_indent_keeps_labels_whole`
- `test_wrap_block_preserves_trailing_blank_lines_and_indented_body`
- `test_wrap_large_width_is_byte_identity_and_property_roundtrip` (1500 random
  bodies: large-N byte identity + per-logical-line word round-trip)

## Evidence

```
python3 -m pytest extensions/agi/tests/test_send.py -q
176 passed in 2.00s
python3 -m pytest extensions/agi/tests/test_sensei.py -q
7 passed in 0.05s
python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
59 passed, 1 skipped in 5.41s
```

All three files passed (test_sensei.py and test_bin_help_smoke.py are the
neighbours the hypothesis lists). Every falsifier from the hypothesis now
prints byte-identical.

Note: the guard `test_whois_reuses_shared_loader_not_new_parse` asserts
`"re.split" not in send.py` — my first edit used a local named `core`
(`co**re.split**`), a false positive; renamed the local to `body_txt`.

## Agent Notes
g15 CLAIM built+labled: rewrote send.py _wrap_body (preserves leading indent on every line/continuation, blank lines byte-exact, only folds lines>width at a single space outside indent) and fixed _wrap_block trailing-newline drop; 5+ tests + 1500-random property; test_send.py/test_sensei.py/test_bin_help_smoke.py all green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-0d964e2f, SL4.02): ACCEPTED proved. (1) INSTRUCTION: hypothesis clause 1-5 + "THIS KID MUST IMPLEMENT THE FIX"; the kid measured the pre-fix corruption, rewrote _wrap_body and added _wrap_logical_line, fixed _wrap_block trailing-newline collapse. (2) MACHINE: I re-ran the falsifiers myself on the built bytes, not the report: _wrap_body("  a\n    b\n\n",160)=="  a\n    b\n\n"; "a\n b\n \n", "x  y  \nz\n", "  \tcode\n" all byte-identical; a 240-col 4-space-indented line folds with the 4-space indent on every physical line and max len 38 at width 40; a 200-char token stays whole; width 0 is raw. 242 passed across test_send.py + test_sensei.py + test_bin_help_smoke.py (1 skipped). (3) NEAR MISS: a fix that emits the indent only on the FIRST physical line (or re-derives indent from the original line instead of re-emitting it per continuation) satisfies the words "preserves leading whitespace" and loses clause 1s continuation case; test_wrap_long_line_keeps_indent_on_every_continuation is the guard. A second near miss: keeping the OLD _wrap_block (splitlines + one re-added \n) would pass every _wrap_body test while still dropping a trailing blank body line, so clause 2 would be half-built; _wrap_block was fixed and is covered. (4) VERDICT: proved stands, evidence_runs names this experiment (it IS the run). CAVEAT recorded not fatal: _wrap_block still round-trips through str.splitlines(), so a body containing \r or \x0c would be re-joined with \n; pre-existing, outside this claim, low risk for send.py bodies.
<!-- THOUGHT:END -->
