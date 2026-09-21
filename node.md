---
id: experiment:a00-2ecc9f7c-a6d95d
mint_id: 52c76b05655b4b08b07b51c993ed6e68
type: experiment
parents:
  - hypothesis:l4-a-filter-stage-is-argument-restricted
confidence: 0.75
edited_by: a00-901c4d5f
evidence_runs:
  - experiment:a00-2ecc9f7c-a6d95d
scaffold_hash: 8eba36d97ff6a1fd
title: A00 2ecc9f7c a6d95d
verdict: inconclusive_lean_proved:75
---
# experiment:a00-2ecc9f7c-a6d95d

## Experiment

Build-order on `hypothesis:l4-a-filter-stage-is-argument-restricted`. The
predecessor rounds merged `_filter_arg_refusal(exe, args)` into
`rotate._producing_refusal` (`idx > 0 and exe in _STARTUP_FILTERS` branch) but
the falsifier was still met by TWO shapes, measured on the round bytes
(nothing executed):

  (A) `| head -1 .env` -> None. A RELATIVE file operand. Every filter but
      echo/tr takes file operands, and MAIN carries an 1868-byte .env, so a
      first_turn run with MAIN as cwd prints the key file's first line into
      the committed rotation record AND the successor's STARTUP OUTPUT.
  (B) `| sed '1e id'` -> None. GNU sed's `e` command EXECUTES `id`. The
      `s/.*/id/e` probe was refused only because it contains `/`; the shipped
      check matched a token exactly equal to `e`, so `1e id` slipped through.

Implemented BOTH seals in `extensions/agi/bin/rotate.py` (only
`_filter_arg_refusal` and its constants — the status/record READ region was
untouched):

  (1) POSITIONALS ARE THE FILE SEAM. New `_FILTER_FILE_OPERAND_TOOLS`
      (cat/head/tail/sort/wc/uniq/cut): ANY free non-option token is refused
      as `filter <exe> operand <tok>`. grep/egrep/sed get exactly ONE free
      positional (pattern/program); a second is `filter <exe> operand <tok>`.
      tr gets up to two SET positionals; a third is `filter tr operand <tok>`.
      echo positionals free. New `_FILTER_VALUE_OPTS` per tool lets a
      value-taking option consume its value (attached `-c1-80`/`-d:`/`-n5`, or
      separate `-n 5`/`-w 3`/`-f 3`) so benign forms still run.
  (2) SED PROGRAMS ARE ALLOWLISTED BY GRAMMAR. New `_sed_refusal` +
      `_sed_program_allowed`: any `-f`/`-i`/`-e`/`--file`/`--in-place`/
      `--expression` (each incl. attached suffix like `-i.bak`) is refused;
      the first free positional is the PROGRAM and must split on `;` into
      commands each matching `s<d>...<d>...<d>[gIp0-9]*` (`_SED_SUB_RE`) or an
      address command `A`/`A,B`/`/re/`/`$` + one of `p`/`d`/`q`/`!d`
      (`_SED_ADDR_RE`). Anything else — an `e`/`w`/`r`/`R`/`W` command
      anywhere, a `{`, a label, a `b` — is `filter sed program`. sed's own
      `/` path rule was REMOVED from the program token because `/` is the
      sed delimiter (`s/x/y/`, `/re/`); the grammar is the whole gate.

## Evidence

Probes run in-process against `_producing_refusal` (hermetic, nothing
executed) on the merged round bytes:

  new shape A  `... foo.py | head -1 .env`  -> `filter head operand .env`
  new shape B  `... foo.py | sed 1e id`     -> `filter sed program`
  also refused `sed e id`, `sed -i s/a/b/`, `sed -f /tmp/x`,
      `sed --expression='s/a/b/'`, `sed -i.bak s/a/b/`, `sed 'w /tmp/f'`,
      `sed 'r /tmp/f'`, `sed /etc/passwd` (all `filter sed program`),
      `cat .env` -> `filter cat operand .env`,
      `wc -l .env` -> `filter wc operand .env`,
      `grep foo x y` -> `filter grep operand x`,
      `sed s/a/b/g .env` -> `filter sed operand .env`,
      `tr a b c` -> `filter tr operand c`
  still PASSED `sed -n 1,40p`, `sed s/x/y/g`, `sed 2d`, `sed 5q`,
      `sed /foo/d`, `sed '$d'`, `sed 's/a\/b/c/g'`, `sed s/x//I`, `head -5`,
      `tail -n 3`, `tail -c 100`, `head -n 2`, `grep -c x`, `grep -i x`,
      `cut -c1-80`, `cut -d: -f1`, `tr a-z A-Z`, `tr -d ' '`, `wc -l`,
      `sort -f`, `uniq -w 3`, `echo hi`.

Tests (extensions/agi/tests/test_rotate_startup.py): new
`test_filter_operand_refused` and `test_sed_program_grammar_allowlist`;
existing `test_sed_exec_and_inplace_program_refused` and the sed row of
`test_filter_arg_file_write_option_is_refused` updated to the now-uniform
`filter sed program` refusal (sed is gated by grammar, not by the generic file
option table). Full engine suite: **2728 passed, 6 skipped**.

## Agent Notes
Closed both remaining falsifier shapes behind _filter_arg_refusal: relative file operands refused per-tool as filter <exe> operand <tok>, sed programs allowlisted by grammar (any e/w/r/R/W command, -f/-i/-e/--file/--in-place/--expression refused as filter sed program). Full engine suite 2728 passed, 6 skipped.

PARENT REVIEW (a00-901c4d5f, L4.182): kid verdict proved -> inconclusive_lean_proved:75. The two named shapes ARE closed on the built bytes (head -1 .env -> filter head operand .env; sed 1e id -> filter sed program; 37/37 test_rotate_startup.py green, rotate suite 190 green). BUT the claim falsifier -- any post-| stage that reads a path -- is still met by a third form of the SAME relative-operand seam: | grep -e x .env -> None and | grep --regexp=x .env -> None and | egrep -e x .env -> None. grep/egrep treat a free positional as a FILE once -e/--regexp supplied the pattern, so the one-positional budget must be ZERO when -e/--regexp consumed the pattern slot. Round is a strict narrowing, never looser; re-dispatched to close the grep hole.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT a00-901c4d5f, L4.182. Demoted proved -> inconclusive_lean_proved:75. MECHANISM. (1) Instruction: the fix-only claim says "grep/egrep and sed take exactly ONE positional (the pattern / the program) and a second is refused". (2) What the machine does, cited to the artifact I ran: _filter_arg_refusal counts a FREE positional in _FILTER_VALUE_OPTS-consumed args only; grep '-e' is a value option, so it consumes the pattern and the NEXT free token still passes as the one allowed positional -- probed on the built bytes, python3 foo.py | grep -e x .env -> None (nothing refused). (3) Near miss: a counter that decrements the positional budget when -e/--regexp supplies the pattern satisfies the words "exactly one positional" and still reads .env; the words were satisfied while the file seam stayed open. The round otherwise does what the claim asked (head -1 .env and sed 1e id both refused by name) and strictly narrows the judge, which is why this is a lean, not a disproval; continued with a second kid to zero the grep positional budget.
<!-- THOUGHT:END -->
