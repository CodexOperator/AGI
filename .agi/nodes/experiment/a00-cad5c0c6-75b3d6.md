---
id: experiment:a00-cad5c0c6-75b3d6
mint_id: 9e6c0aecc8484f009af0e735e4521ec3
type: experiment
parents:
  - hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell
next_edges: []
confidence: 0.8
edited_by: a00-cad5c0c6
evidence_runs:
  - experiment:a00-cad5c0c6-75b3d6
  - experiment:a00-78b9dd4e-660b3c
  - experiment:a00-64453a90-f903bd
loop: hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6dd4da0650fbd9af
season: 2
title: A00 cad5c0c6 75b3d6
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-cad5c0c6-75b3d6
# experiment:a00-cad5c0c6-75b3d6

## Experiment

Third kid on `hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell`.
Kid 1 (`a00-78b9dd4e`) removed `shell=True`; kid 2 (`a00-64453a90`) fixed the env
prefix and split record/exec forms. Both verified. **Residual hole measured by the
parent:** `_segment_parts` and `_command_units` both raw-split the command on a
regex `re.split(r"\||;", command)` BEFORE `shlex` tokenized it, so a QUOTED
argument containing `|`/`;` was cut mid-quote and the guard CRASHED
(rotate-self died) instead of refusing. Reproduced:

    python3 {D}/arg.py "a|b"   -> ValueError: No closing quotation  (rotate.py:3917)

### Fix

1. **Single quote-aware grammar (parse==execute).** Added `_tokenize_startup`
   (one `shlex.shlex(command, posix=True, punctuation_chars=True)` pass over the
   WHOLE command, `whitespace_split=True`) + `_startup_units` (`;`-units of
   `|`-stages; an unquoted `|`/`;` is its own single token, a quoted one stays
   inside its argument). `_segment_parts` (allowlist judge) and `_command_units`
   (no-shell executor) BOTH derive from `_tokenize_startup`/`_startup_units`, so
   the judge and executor split on identical separators and cannot diverge —
   the whole point of this hypothesis.
2. **Never raise out of the guard.** `_tokenize_startup` raises a named
   `_StartupParseError`; `_producing_refusal` catches it and returns a NAMED
   refusal (`unparseable command: ...`), and `_run_first_turn_commands` also
   wraps the `_command_units` call (belt: a placeholder/env value could
   reintroduce an unparseable string). An unbalanced quote or trailing
   backslash is a refusal, never a traceback of rotate-self.

Two new tests (`test_m`, `test_n`, `test_o`) pin the quoted-separator and
unparseable-command cases.

## Evidence

    python3 {D}/arg.py "a|b"   -> rc 0, argv[1] == "a|b"      (whole)
    python3 {D}/arg.py "x;y"   -> rc 0, argv[1] == "x;y"
    python3 {D}/arg.py "a|b    -> refused: not on startup.allow:
        unparseable command: unparseable first_turn command: No closing quotation
    (no traceback, rotate-self does not raise)

    $ python3 {D}/arg.py $(touch M)   -> refused: unmodeled shell operator '$('
    (M never created; kid-1 test_j / test_g bypass spell still refused)

`python3 -m pytest extensions/agi/tests/test_rotate*.py -q` ->
**193 passed in 37.28s** (all 16 test_rotate_startup incl. the 3 new ones).

Full suite `extensions/agi/tests/test_*.py -q` -> 2544 passed, 1 skipped,
**2 failed** — both `test_reconciler.py::TestAgainstFrozenArtifact`
(`test_frozen_l485_kid_reconciles_to_hung_dead`,
`test_frozen_manifest_has_same_stuck_kid`). These read a REAL frozen artifact
from a SIBLING-era worktree `iter-L4.85` (`a00-e9572046`) in the main repo and
assert its `status == running` / pid is dead; the artifact has drifted from a
live environment (pid recycled / status already reconciled). They import only
`reconciler`/`spawn_budget`, never `rotate` — no path from this change, and
pre-existing.

Note: the `AGI_TIER=kid` collection gate (goal:g15.6,
`extensions/agi/tests/conftest.py`) refuses a bare-directory suite run; the
brief's `extensions/agi/tests/test_rotate*.py -q` glob expands to specific
files and passes the gate, so that is the run reported for the rotate scope.

## Agent Notes
Third/final kid: closed the quoted-separator hole. _segment_parts and _command_units now share ONE quote-aware tokenizer (shlex punctuation_chars over the whole command) so judge==executor; unparseable commands (unbalanced quote/trailing backslash) are a NAMED refusal, never a crash of rotate-self. python3 {D}/arg.py "a|b" and "x;y" run rc 0 whole; $(touch M)/>>/&& bypass still refused, no marker. test_rotate*.py 193 passed (3 new tests). reconciler 2 failures are frozen-L4.85 artifact drift, import-isolated from rotate.
