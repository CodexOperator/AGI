---
id: experiment:a00-48cb25b8-d5432a
mint_id: b7e3932180c7435e99be32dafd278812
type: experiment
parents:
  - hypothesis:l4-an-env-value-cannot-break-a-quoted-argument
next_edges: []
confidence: 0.85
edited_by: a00-0ac85f04
evidence_runs:
  - experiment:a00-48cb25b8-d5432a
loop: hypothesis:l4-an-env-value-cannot-break-a-quoted-argument@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 69e55befefe89bbc
season: 2
title: "\"env value cannot break a quoted argument — per-token expansion proven; scrub gates added\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-48cb25b8-d5432a

## Experiment

Implemented the FIRST HALF of `l4-an-env-value-cannot-break-a-quoted-argument`
(build order, g15 behaviour) + the scrub's innocen-word half on the built
bytes in `extensions/agi/bin/rotate.py`, proved by tests in
`extensions/agi/tests/test_rotate_startup.py`.

**What I changed (rotate.py):**
1. New `_resolve_shell_var(m)` extracted from the old whole-string resolver;
2. New `_resolve_shell_vars_per_token(command)`: `_tokenize_startup` first,
   then each argv element has its `$VAR`/`${VAR}` replaced by the VALUE as ONE
   literal token, then `shlex.join` — the first_turn executor now calls THIS,
   not the old whole-string `re.sub`. A `shlex.join` round-trip through the
   punctuation_chars grammar is EXACT (verified; standalone `|` / `;` tokens
   re-parse to separators), so what the re-judge sees is what the no-shell
   executor will execute. Handle `_StartupParseError` early (refusal, named).
3. `_scrub_injected_refusal`: a message word is dropped only when it is a
   substring of an env VALUE **AND** `len >= _REFUSAL_MIN_DROP_CHARS (4)`
   **AND** not in `_REFUSAL_TEMPLATE_WORDS` (rotate.py's own refusal prose)
   — short innocent words (`a`/`on`/`me`/`the`/`in`) and the template's own
   prose survive; a >=4-char fragment of a value is still redacted to
   `<expanded value redacted> (expanded from $VAR)`.

**Key finding (drives the tests):** the claim's OWN worked example, template
`git -C "$WT" status -sb`, cannot carry an env value past the TEMPLATE judge —
`_git_arg_refusal` rejects a `$` (backtick/`~`) in the git `-C` PATH value at
template time, so `producer git $WT not on the allowlist` fires before env
expansion. Git is already closed by its ARG allowlist (defence-in-depth).
Claim (a)/(b) are therefore demonstrated on the actually-allowable engine-python
producer (`python3 .../list.py $SEAT`), and git's closure is pinned as its own
test (`test_git_dollar_c_path_is_blocked_at_template_time`).

**Behaviour change (by design, per claim):** an env VALUE is now inert DATA,
not re-parsed syntax. `python3 ... $SEAT` with SEAT=`"x' | touch M"` no longer
REFUSES — the value stays inside the single `$SEAT` element, nothing but the
one producer executes, the record keeps `$SEAT` LITERAL. PLACEHOLDER injection
(`{seat}` = `a | touch M`) is UNCHANGED: placeholders substitute INTO the string
BEFORE tokenization, so the injected `|` is still a real stage still REFUSED
(test_r / test_s4 / new `test_placeholder_injection_still_refuses*` all green).
The re-judge remains load-bearing for placeholders; it no longer has env-stage
injections to regret — there are none.

## Evidence

**Tests (extensions/agi/tests/test_rotate_startup.py): 62 passed.** New/repurposed:
- `test_s_env_value_stays_one_argv_token_no_stage` — captured argv ==
  `['python3','/wt/extensions/list.py','seatA | touch <M>']`, no stage, no marker.
- `test_s2_env_value_semicolon_stays_one_token` — `; cat <secret>` one token.
- `test_s3_env_value_never_in_record_or_output` — value absent from str(res)
  and the rendered STARTUP OUTPUT; record keeps `$SEAT`.
- `test_env_value_cannot_add_argv_element` (claim a) — SEAT=`x" --no-such-flag "y`
  -> argv[3] is the WHOLE value; `--no-such-flag` NOT an extra element.
- `test_env_value_pipe_stays_in_one_arg_no_operator_refusal` (claim b) —
  SEAT=`x | sh` -> ONE token, no operator refusal, rc from mocked git-like run.
- `test_scrub_keeps_short_innocent_words_byte_identical` (claim c) — words <4
  that are substrings pass through byte-identical.
- `test_scrub_redacts_long_env_fragment_still` (claim d) — 12-char $HOME
  fragment still dropped + redacted + `$HOME` named.
- `test_scrub_keeps_template_word_that_coincides_with_env_fragment` — `producer`
  survives even when it's a substring of a value.
- `test_git_dollar_c_path_is_blocked_at_template_time` — pins git's own closure.
- `test_placeholder_injection_still_refuses_with_per_token_env`.

Old `test_s`/`test_s2`/`test_s3` (env-injected `|`/`;` REFUSED) were REWRITTEN
because claim (b) explicitly flips env-injected separators to non-refusing
DATA while the security invariants (no marker, no secret leak, record keeps
`$VAR` literal) are preserved and re-proved under the new mechanism. No such
test of a value-adds-an-argv-element or a stage escapes.

**Full engine suite:** `pytest extensions/agi/tests/test_*.py` -> **2872 passed,
6 skipped, 1 failed** — the single failure is `test_stream_master_semantic_
screen::test_zero_novel_escapes` (`['code-smuggle']` novelty escape), a real-
model `ModelJudge` directive-review flake in `src/stream_master/semantic_screen`
with NO import/control relation to rotate.py first_turn or env expansion
(pre-existing, environmental). Every rotate / dispatch / git-guard / harvest
file is green.

## Agent Notes
Per-token env expansion (_resolve_shell_vars_per_token: tokenize then expand each argv element, shlex.join) so an env value can't add an argv element or inject a stage on ANY allowlisted producer; scrub keeps short innocent words (>=4 chars + not template prose); rewrite test_s/s2/s3 to data-semantics (no marker, record keeps $VAR literal); 62 startup tests + 2872 full-suite pass (1 unrelated ModelJudge flake). Finding: git -C "$WT" is already closed at template time by the git $ -in--C guard.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-0ac85f04, L4.247): accepted proved 0.85. The instruction said implement, not measure ("This kid MUST IMPLEMENT THE FIX"). The machine now does: first_turn calls _resolve_shell_vars_per_token (rotate.py), which tokenizes FIRST via _tokenize_startup then substitutes $VAR per argv element and shlex.joins. I built and ran it on the round bytes: git -C "$WT" status -sb with WT=x" --no-such-flag "y -> 7 tokens on the old whole-string resolver, EXACTLY 4 on the new one with the value whole in argv[2]; $PIPE=x | sh -> 5 tokens containing a bare | and sh old, 3 tokens with 'x | sh' as one element new. Near miss 1: a fix that tokenizes once at the top and re-joins WITHOUT shlex.join would satisfy the words and re-split the value on the next parse; the exact round-trip is what keeps judge and executor identical. Near miss 2: passing the expanded argv list straight to _command_units would satisfy the words and lose the re-judge, which still must run on the joined string for PLACEHOLDER stages. Deviation from the claim text, documented not hidden: claim example (a) used git, but _git_arg_refusal already refuses a $ in the -C path at TEMPLATE time (producer git ... not on the allowlist), so (a) is pinned by test_git_dollar_c_path_is_blocked_at_template_time and the live demonstration moved to the python3 producer that is actually reachable. Test rewrites: test_s/s2/s3 asserted env-injected |/; was REFUSED; the claim explicitly flips that to inert DATA, so the rewrite is the claim, and the security invariants (no marker, value absent from str(res)/STARTUP OUTPUT, record keeps $VAR literal) are re-proved. Verified myself: test_rotate_startup 62 passed; rotate/dispatch/git_guard/harvest 443 passed. Only full-suite failure is test_stream_master_semantic_screen (real-model ModelJudge flake, no import relation).
<!-- THOUGHT:END -->