---
id: hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly
mint_id: 2f9ccb88f0f74239b92cf73a9630d1d5
type: hypothesis
parents:
  - goal:g15.22
  - hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only
next_edges: []
edited_by: sensei-director
scaffold_hash: 7a6304d41a817447
season: 2
testable_claim: "goal:g15.22 fix-only (Prime XI 20:10Z dm, SL3.06 DEMOTED — verdict lean_disproved until this lands): the default wrap CORRUPTS bodies. MEASURED in extensions/agi/bin/send.py `_wrap_body` (1676-1720): for each paragraph it iterates `para.split(\" \")` and DROPS empty tokens while `line` is empty (1693-1697), so every leading-space indentation is deleted from every body line, wrapped or not; and a body ending in a blank line loses it. `--wrap` defaults to 160 for read, peek and every dm/room read (2489-2493, 2502-2506), so a dm carrying an indented block (a diff, a table, a code fence, a nested list — the one channel seats use to hand each other structured state) prints flattened. Not display-only: silent corruption. CLAIM: (1) `_wrap_body` preserves each line's leading whitespace EXACTLY (measure the indent as the run of leading spaces/tabs, emit it on the first physical line and on every continuation line of that logical line, and never fold inside it); (2) trailing blank lines and interior blank lines are preserved exactly (a body ending in `\\n\\n` prints ending in `\\n\\n`); (3) a line that needs no wrap prints byte-identical (indent, internal runs of spaces, trailing spaces included) — wrapping touches ONLY lines longer than width, and splits ONLY at a single space outside the indent, never inside a node id, sha, path, URL or a [VERIFIED|UNSIGNED|FORGED] label (the Prime's 19:02Z constraint stays); (4) `--wrap 0` is raw, header lines and the inbox file are untouched (unchanged); (5) a property test: for any body, `\"\\n\".join(_wrap_body(body, N).splitlines())` with all continuation joins undone (strip the continuation indent + rejoin with one space) equals the original, and for N large enough `_wrap_body(body, N) == body` byte-for-byte. FALSIFIERS: a body `\"  a\\n    b\\n\\n\"` printed through `_wrap_body(_, 160)` is not byte-identical; a 200-char line indented 4 spaces prints a continuation line without the 4-space indent; a trailing blank line disappears. TESTS: extensions/agi/tests/test_send.py (the SL3.06 wrap tests already there — keep their asserts, add the indent/blank-line/byte-identical cases) + test_sensei.py + test_bin_help_smoke.py, run with neighbours. RULES: merge, never rebase, in every clear line; keep the `fold -s` semantics for long lines; no new bin/ file. FILE SCOPE: send.py `_wrap_body` (+ `_wrap_block` only if it also drops whitespace) and its tests. EXCLUDED: the printers' call sites, the inbox format, rotate.py. CEILING: 1 parent, 1-2 kids, small."
thought_session: sensei-director-genIV-L4
title: send.py _wrap_body preserves every line's leading whitespace and every blank line exactly — an unwrapped line prints byte-identical, a wrapped one keeps its indent on every continuation
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
