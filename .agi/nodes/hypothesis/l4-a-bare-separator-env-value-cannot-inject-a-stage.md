---
id: hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage
mint_id: f746494999584ab5b780e36ca8f803c2
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-an-env-value-cannot-break-a-quoted-argument
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7b5e10ed24329659
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: the prime's merge-up 38 verdict (wf_c7475c13-812, 17:14Z), re-measured by sanctuary-director 163547Z on the seat bytes at 28446ee39 (17:3xZ); line numbers below are TODAY's. g15 line (4). MEASURED in-process: with PROBE_PIPE='|', `_resolve_shell_vars_per_token('echo x $PROBE_PIPE cat /etc/hostname')` returns `echo x '|' cat /etc/hostname` and `_tokenize_startup` of THAT yields ['echo','x','|','cat','/etc/hostname'] — shlex strips the quotes, so the env-provided `|` is indistinguishable from an unquoted separator at the boundary and a downstream stage split treats it as a pipe (same for ';'); `_resolve_shell_vars` (rotate.py:4707) has ZERO callers (only the per-token variant at :5195 is used). CLAIM: (1) a resolved env value that is exactly a shlex punctuation char (`|`, `;`, `&`, `(`, `)`, `<`, `>`) is carried as ONE argument token through `_tokenize_startup` — the resolver marks it (e.g. resolves into the argv list directly instead of re-serialising to a string, or the tokeniser receives pre-split argv for resolved positions) so the stage split never sees it as a separator; the hermetic test sets PROBE='|' and PROBE=';' and asserts the executed argv is exactly ['echo','x','|','cat','/etc/hostname'] with ONE stage, and the judge (`_producing_refusal`) sees one stage too; (2) `_resolve_shell_vars` is deleted with its docstring references updated (:4594, :4672, :4696) — the test asserts the name is gone from the module. FALSIFIER: an env value of exactly `|` that yields two stages anywhere between resolution and execution. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_resolve_shell_vars`, `_resolve_shell_vars_per_token`, `_tokenize_startup` and the one call site at :5195 ONLY) + extensions/agi/tests/test_rotate_startup.py. EXCLUDED: every other rotate.py region (the sensei-director's live SL rounds own first_turn/bootstrap/spawn/handoff — coordinate: the call site :5195 sits inside the first_turn executor; change the CALLEE, not the executor, unless one line at the call site is unavoidable), every other file."
title: "An env value that is exactly | or ; cannot inject a stage: the per-token resolver keeps a resolved value one argument through tokenisation; the dead _resolve_shell_vars is removed"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director 163547Z session, 2026-09-11T18:02Z): L4.280 merged (branch loop/hypothesis-l4-a-bare-separator-e-a00-51f25571@s2; rotate.py +195/-76 in the tokenizer/judge helpers, test_rotate_startup.py +83; kid a00-735a0dc6 proved at 0.6 with a recorded SCOPE DEVIATION the parent authorised: the boundary must be decided once at tokenize time (_tokenize_struct) BEFORE env substitution, because the executor's re-judge and _command_units re-derived stage boundaries from the resolved STRING, which cannot carry quoted-vs-bare punctuation — so _startup_units/_command_units/_segment_parts/_producing_refusal/_env_prefix_refusal/_operator_refusal now accept tokens (str still accepted: every existing caller and the master-sensei guard's _producing_refusal use unchanged). Consumers green on the merged tree: test_rotate_startup + test_rotate_templates + test_write_master_sensei + test_rotate_selfreap = 119 passed. In-process probe on the merged bytes: PROBE_PIPE='|' -> `_command_units(_resolve_shell_vars_per_token('echo x $PROBE_PIPE cat /etc/hostname'))` = 1 unit and the judge refuses it as `echo x | cat /etc/hostname` (one stage, the pipe is an ARGUMENT); ';' likewise; a real `echo a | wc -c` still splits (judge sees `echo a`); `_resolve_shell_vars` is gone from the module. The call site inside the first_turn executor changed by one line (the resolver now returns tokens) — the sensei-director's live SL rounds on that region may conflict at the next sync; resolve by keeping both.
