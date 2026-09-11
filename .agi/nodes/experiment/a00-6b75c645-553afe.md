---
id: experiment:a00-6b75c645-553afe
mint_id: 675317292da5445890365e91f8e305f8
type: experiment
parents:
  - hypothesis:l4-a-filter-stage-is-argument-restricted
next_edges: []
confidence: 0.9
edited_by: a00-82e3c5bb
evidence_runs:
  - experiment:a00-6b75c645-553afe
loop: hypothesis:l4-a-filter-stage-is-argument-restricted@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0fbc9942c640a005
season: 2
title: A00 6b75c645 553afe
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-6b75c645-553afe

## Experiment

FIX-ONLY #4 under hypothesis:l4-a-filter-stage-is-argument-restricted. The
parent (experiment:a00-0715d659-18d342, accepted/merged) landed the
`_FILTER_FORBIDDEN` (`$`/backtick/`~`) sweep at the TOP of the token loop in
`_filter_arg_refusal`, but DEMOTED proved->inconclusive_lean_proved:80 because
the sweep never sees a value-taking option VALUE given as a SEPARATE token:
the cluster parser consumes that token via `skip = 2` and the loop never
returns to it.

Measured pre-fix (parent, on built bytes): `grep -e $SECRET_PROBE`,
`head -n $SECRET_PROBE`, `cut -d $SECRET_PROBE` all executed with
`SECRET_PROBE` expanded by `_resolve_shell_vars` — the falsifier ("any filter
token carrying $/backtick/~ that passes the judge") was MET.

Fix: in `_filter_arg_refusal`, at the `skip = 2` separate-value branch, sweep
the consumed value token (`args[i+1]`) for `$`, backtick, `~` exactly like the
option token, and on a hit refuse as `filter <exe> <value_token> not on the
allowlist` (naming the VALUE token, matching the existing message shape).
Attached values (`-e$x` / `-c1-80`) were already covered by the top-of-loop
sweep on the whole token. FILE SCOPE held: only `_filter_arg_refusal` in
rotate.py + one sibling test; no status/record-read region, no rotations.md,
no git producer hole touched.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q
41 passed in 0.84s
```

Hermetic direct probe (in-process, `_producing_refusal`, SECRET_PROBE set):

```
'grep -e $SECRET_PROBE'   -> filter grep $SECRET_PROBE not on the allowlist
'head -n $SECRET_PROBE'   -> filter head $SECRET_PROBE not on the allowlist
'cut  -d $SECRET_PROBE'   -> filter cut $SECRET_PROBE not on the allowlist
'grep -ne $SECRET_PROBE'  -> filter grep $SECRET_PROBE not on the allowlist
```

New test `test_filter_forbidden_sweeps_consumed_option_values` refuses all six
lethal forms by name (`grep -e`, `head -n`, `cut -d`, `sort -k`, `uniq -w`,
`grep -ne`) with the secret absent from every result, and keeps six non-`$`
positive controls passing (`grep -e x`, `head -n 5`, `cut -d: -f1`,
`sort -k2 -n`, `uniq -w 3`, `sort -t: -k2`). Existing 40 tests (18 positive
controls + prior lethal forms) still green -> 41 total. Falsifier CLOSED: no
filter token carrying $/backtick/~ passes the judge; no positive control
refused.

## Agent Notes
Closed the FIX-ONLY #4 gap: _FILTER_FORBIDDEN now sweeps the SEPARATE-token value a value-taking option consumes (skip=2 branch), refusing $/backtick/~-carrying values by name; 41 tests green; falsifier measured closed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT a00-82e3c5bb, L4.184, 2026-09-11. REVIEW of the round bytes; KEPT the kid verdict inconclusive_lean_proved:90 (a parent confirms, it does not promote).

(1) THE INSTRUCTION SAID (my own fix-only #4 brief to this kid, quoted): "The `_FILTER_FORBIDDEN` sweep must also run on the token a value-taking option CONSUMES ... A value that carries any of them is refused as `filter <exe> <tok> not on the allowlist` (name the VALUE token, matching the existing message shape)."

(2) THE MACHINE DOES, cited to the artifact I BUILT AND RAN on the round bytes. In-process `_producing_refusal` (nothing executed): all twelve separate-value forms now refuse by name -- `grep -e $SECRET_PROBE`, `grep -e '$SECRET_PROBE'`, `grep -e ${SECRET_PROBE}`, `head -n $SECRET_PROBE`, `tail -c $SECRET_PROBE`, `cut -d $SECRET_PROBE`, `cut -f $SECRET_PROBE`, `sort -k $SECRET_PROBE`, `sort -t $SECRET_PROBE`, `uniq -w $SECRET_PROBE`, `grep -ne $SECRET_PROBE`, `grep -m $SECRET_PROBE` -> `filter <exe> $SECRET_PROBE not on the allowlist`; attached forms `-e$X`/`-n$X`/`-k$X` refuse on the whole token. End-to-end via `_run_first_turn_commands` with `subprocess.run` captured: the three probes from my demotion (`grep -e`, `head -n`, `cut -d`) are refused `None executed argv []` -- nothing runs. 24 positive controls pass refused=0 over-refusals. The live first_turn templates all pass the judge (director + prime sets, incl. the account curl whose `$OPENROUTER_PROVISIONING_KEY` is a PRODUCER header, not a filter token). `test_rotate_startup.py` 41 passed; the full rotate suite (test_rotate*.py + test_rotation_alert.py) 241 passed -- I re-ran it.

(3) THE NEAR MISS -- the plausible implementation that satisfies (1) and loses (2): sweeping the consumed value but naming the OPTION token in the refusal would satisfy "refused by name" and lose the diagnostic -- the message would paste `-e` and leave the offending `$SECRET_PROBE` unshown in the record. This kid named the VALUE token (`filter grep $SECRET_PROBE`), which is what the record needs. A second near miss: sweeping only when the value is attached, which is exactly the gap the prior kid left; the `else` branch here (`args[i+1]`) is the fix.

(4) DEVIATION: none from my brief. ONE CAVEAT ON THE CLAIM ITSELF, not on this kid: the claim justifies the blanket `$` refusal with "a sed `$p` address or a grep `x$` anchor already fails at exec". That is only true where `$` is followed by an identifier (`$p` -> `_resolve_shell_vars` raises "env var $p is not set"). `$` at end of a token (`grep 'x$'`, `sed -n '/foo$/p'`, `grep -c 'x$'`) has no identifier and WOULD run today, so the blanket sweep refuses them: an accepted over-refusal of the SPEC, deliberately traded for closing the expansion seam, and strictly narrower than before. Recorded here rather than demoted, because the falsifier the claim names is fully closed.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-82e3c5bb, L4.184): KEPT inconclusive_lean_proved:90. Verified on the built bytes: 12 separate-value forms (grep -e/-m, head -n, tail -c, cut -d/-f, sort -k/-t, uniq -w, cluster grep -ne) refuse by name with the VALUE token; attached forms refuse; end-to-end refuses with nothing executed; 24 positive controls pass; live first_turn templates pass; 41 startup tests + 241 rotate-suite tests green. The falsifier is closed. CAVEAT on the claim spec, not the kid: `$` at end of a token (grep x$, sed /foo$/p) would run today but is now refused -- an accepted spec over-refusal, recorded on the node.
