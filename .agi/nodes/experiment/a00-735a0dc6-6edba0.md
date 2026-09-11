---
id: experiment:a00-735a0dc6-6edba0
mint_id: 0e19197653ad44a9a0ff3ebb049ca32f
type: experiment
parents:
  - hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage
next_edges: []
confidence: 0.6
edited_by: a00-51f25571
evidence_runs:
  - experiment:a00-735a0dc6-6edba0
loop: hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ed0d0e9a8fd513af
season: 2
title: A00 735a0dc6 6edba0
town: core
verdict: proved
---
# experiment:a00-735a0dc6-6edba0

## Experiment

g15 CLAIM — the claim is behavior to BUILD, not a hypothesis to measure
(hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). Measured the
pre-fix defect, then IMPLEMENTED the claim and proved it on the built bytes.

**Pre-fix defect (measured, confirmed the parent note's PRIOR repro):**

`_resolve_shell_vars_per_token` resolved env vars per token and re-joined with
`shlex.join`. For an env VALUE exactly equal to a shlex punctuation char, that
round-trip lost the quoted-vs-bare distinction:

    PROBE_PIPE='|'  -> tokens [('arg','echo'),('arg','x'),('arg','|'),('arg','cat'),('arg','/etc/hostname')]
    `_startup_units` SPLITS on the `|` -> TWO stages  [[['echo','x'],['cat','/etc/hostname']]]

Root cause: `shlex.join('|')` -> "'|'", but re-tokenizing with
`shlex.shlex(..., punctuation_chars=True)` returns token TEXT `|` for the quoted
char — indistinguishable from a bare separator. Verified there is NO lossless
string serialization that preserves it (backslash-escape also collapses to a
bare `|` token). The distinction cannot live in the string; it had to move into
the STRUCTURE.

**Fix (rotate.py):**

1. `_resolve_shell_vars_per_token` now returns the STRUCTURAL token list
   `[("sep", p) | ("arg", value)]` instead of a re-serialized string. The
   boundary decision (`sep` vs `arg`) is fixed by the new `_tokenize_struct`
   BEFORE env substitution, so an env value that is exactly `|`/`;` stays one
   `("arg","|")` element and cannot become a stage boundary.
2. `_startup_units`/`_command_units`/`_segment_parts`/`_producing_refusal`/
   `_env_prefix_refusal`/`_operator_refusal` accept a command STRING (tokenized
   UNexpanded, preserving the old test-facing behavior incl. `$HOME` literal)
   or a resolved structural token list (what the executor passes). Shared
   grammar via `_as_tokens`.
3. The executor's `exec_cmd` string became `exec_tokens` — the resolved
   structure threaded into the re-judge and `_command_units` unchanged in
   order.
4. `_resolve_shell_vars` (whole-string, ZERO callers) DELETED; docstring
   references at the filter sweep (`_resolve_shell_vars_per_token`), the
   `_STARTUP_SHELL_OPS` comment, and `_resolve_shell_var`'s docstring updated.

Scope deviation (recorded per THOUGHT): touched `_startup_units`, `_command_units`,
`_segment_parts`, `_producing_refusal`, `_env_prefix_refusal`, `_operator_refusal`
— the separator-consuming half a structural fix cannot avoid (the parent's
authorized deviation). Did NOT touch `_run_units_no_shell` semantics,
`_announce_rotation`, or first-turn bootstrap/spawn/handoff.

## Evidence

Built result (post-fix, in-process):

    PROBE='|' : _command_units -> [[(['python3','/wt/extensions/list.py','|'], {})]]   # ONE unit, ONE stage
    PROBE=';' : _command_units -> [[(['python3','/wt/extensions/list.py',';'], {})]]   # ONE unit, ONE stage
    PROBE='|' : _producing_refusal -> None   # judge sees ONE allowed stage
    PROBE=';' : _producing_refusal -> None
    PROBE='&&': _command_units -> ONE unit/arg '&&', _producing_refusal -> "unmodeled shell operator '&&'" (correct)
    "echo x $PROBE cat /etc/hostname" with PROBE='|'
        -> _startup_units [[['echo','x','|','cat','/etc/hostname']]]   # was TWO stages before

`_resolve_shell_vars` name-gone: `not hasattr(rotate, "_resolve_shell_vars")` -> True.

Tests (added to extensions/agi/tests/test_rotate_startup.py):
- `test_probe_bare_separator_value_stays_one_stage` — ONE unit/stage, argv carries `|`/`;` whole
- `test_probe_bare_separator_full_runner_one_argv` — end-to-end runner, mocked
  subprocess receives ONE argv element = the bare char, nothing injected
- `test_probe_judge_sees_one_stage_on_allowlisted_producer` — judge on resolved
  structure sees ONE stage, no refusal
- `test_resolve_shell_vars_whole_string_gone` — name absent from module

Pytest results:
    python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q           -> 67 passed
    + test_rotate.py test_write.py test_write_guard.py                         -> 292 passed
    + test_rotate_templates.py test_rotate_complete.py test_write_master_sensei.py
      test_node_writer.py test_rotate_tail.py                                  -> 120 passed
All green; changed-file covering suites pass.
<!-- THOUGHT:BEGIN — authored, not derived; the reasoning behind THIS version. -->
SCOPE DEVIATION (authorized by the parent's build brief): the minimal structural
fix required touching _startup_units/_command_units/_segment_parts/_producing_
refusal/_env_prefix_refusal/_operator_refusal — the separator-consuming half.
A fix that only changed the resolver could not help: the executor's re-judge
and _command_units re-derived boundaries from the resolved STRING, and a string
cannot carry the quoted-vs-bare punctuation distinction. So the boundary must
be decided once, at tokenize time (_tokenize_struct), before env substitution,
and the resolved STRUCTURE threaded to every consumer (string entry kept for
tests/write.py and tokenized UNexpanded so $HOME-style literals judge as
before). Not touched: _run_units_no_shell execution semantics, _announce_
rotation, first-turn bootstrap/spawn/handoff. A quirk worth noting: a token in
the TEMPLATE that is itself exactly `'|'` was ALREADY a stage edge before this
change (token text loses the quote) and remains one — only env-EXPANDED values
become data.
<!-- THOUGHT:END -->

## Agent Notes
Built the structural fix: _resolve_shell_vars_per_token now resolves env into a structural (sep/arg) token list (boundary fixed at tokenize time, never re-parsed), threaded through _startup_units/_command_units/_segment_parts/_producing_refusal/_env_prefix_refusal/_operator_refusal; deleted ZERO-caller _resolve_shell_vars. An env value exactly '|' or ';' now executes as ONE argv element in ONE stage; judge sees one stage. 4 tests added, 67+292+120 pass.

PARENT REVIEW (a00-51f25571, L4.280): accepted as proved. Read the artifact, not the report: re-ran extensions/agi/tests/test_rotate_startup.py -q -> 67 passed, and the covering set test_rotate.py+startup+templates+complete+tail+write+write_guard+write_master_sensei+node_writer -> 412 passed in 33.81s. Independent in-process probe post-fix: PROBE=| -> _startup_units [[[echo,x,|,cat,/etc/hostname]]] and _command_units ONE unit/ONE stage; PROBE=; -> same, one stage; _producing_refusal(tokens) is None; hasattr(rotate,_resolve_shell_vars) False. The scope deviation (touching the separator-consuming half) is the authorised one and is correctly recorded. CAVEAT FOUND IN REVIEW (narrow, conservative, NOT re-cut): _operator_refusal on a structural token list joins tokens with "" instead of a space, so it can FABRICATE an operator across a token boundary that the old shlex joined string could not: printf %s $A $B with A=x| and B=|y joins to text containing || and returns unmodeled shell operator || in first_turn command (verified at rotate.py:4688-4694). Direction is safe (over-refusal, never under), so the primary claim stands; the next round at this node should join with a space, which detects every within-token operator and fabricates none.
