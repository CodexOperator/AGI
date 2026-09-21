---
id: experiment:a00-cdc119dd-2e0283
mint_id: b2804dd064bf43a892ba7202949c0f70
type: experiment
parents:
  - hypothesis:l4-a-filter-stage-is-argument-restricted
next_edges: []
confidence: 0.6
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-cdc119dd-2e0283
loop: hypothesis:l4-a-filter-stage-is-argument-restricted@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d96f06792904d0a3
season: 2
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the four prime filter probes (awk sort -o head path cat path) are now named refusals; PATH/PYTHONPATH/LD_* refused unconditionally
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-cdc119dd-2e0283

## Pre-fix measurement (the claim's falsifier, reproduced)

`rotate.py:_producing_refusal` skipped EVERY post-`|` stage whose executable
is in `_STARTUP_FILTERS` by name alone — its ARGUMENTS never reached the
judge. Measured on the pre-fix bytes, all four prime probes PASSED the judge
(unrefused) as `|` filters:

    awk   '... | awk BEGIN{system(...)}'          -> None   (no refusal)
    sort  '... | sort -o M'                        -> None   (writes file M)
    head  '... | head -1 /etc/hostname'            -> None   (reads a path)
    cat   '... | cat /etc/hostname'                -> None   (reads a path)

`cat /etc/hostname` alone (idx 0, producing) WAS refused on the allowlist, but
as a `|`-filter stage it was skipped too. The placeholder value probe
`a | cat /etc/hostname` therefore also reached the box.

## The build (claim implemented)

`rotate.py`:
1. New `_filter_arg_refusal(exe, args)` — a filter stage's ARGUMENTS are
   judged on the same strict standard as a producing command: any token
   containing `/` is a path (refused); the file-writing/redirecting options
   `-o` `-w` `-i` `--output` `-f` are refused in exact (`-o`) and attached
   (`-oM`, `-f3`, `--output=foo`) forms; `awk` is refused outright (its
   program body can reach `system`/`getline`/`>`/`|`); `sed -i`/`e`
   in-place/execute program forms are refused. Every refusal is NAMED
   `filter <exe> <arg>` before anything runs.
2. Wired into `_producing_refusal`: the `idx > 0 and exe in _STARTUP_FILTERS`
   branch now returns a filter refusal instead of `continue`.
3. Env FOLD: `PATH`, `PYTHONPATH`, `LD_*` are refused UNCONDITIONALLY in a
   leading `VAR=value` prefix (even when a template declares them on
   `startup.env_allow`) — a template author cannot redirect binary lookup.

## Proof-on-the-built-bytes (post-fix)

All four prime probes now refused by name:

    awk   -> 'filter awk'
    sort  -> 'filter sort -o'
    head  -> 'filter head /etc/hostname'
    cat   -> 'filter cat /etc/hostname'

The benign set still runs: `| head -5`, `| grep -c x`, `| sort`,
`| cut -c1-80`, `| tr`, `| wc -l`, `| sed -n 1,40p`, `| uniq` all unrefused.
The NAMED refusal surfaces on the real run path (no execution, no marker).

## Tests

`test_rotate_startup.py`: added 7 tests (filter path-read refusal, file-option
refusal incl. attached forms, awk-outright, sed `-i`/`e`, benign-filters-
still-run, named-refusal-before-run, and the env FOLD). Existing assertions
for `PATH`/`LD_PRELOAD` refusals updated to the new unconditional message.

**Full engine suite: 2727 passed, 6 skipped — no regressions.**

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The blanket _FILTER_FILE_OPTIONS tuple this node describes as the fix was CORRECTED by the follow-up kid (experiment:a00-2a67c72a-d091cf): a flat option list applied to every filter refused benign stdio flags (grep -i/-o/-w, sort -f, cut -f1, uniq -w), which the claim's own falsifier — "any post-| stage that writes, reads a path, or runs a command" — forbids. The refusal is now per-tool (sort -o/--output, sed -i, grep/egrep -f). What this node actually proved still stands and I re-verified it on the built bytes: all four prime probes (awk, sort -o M, head -1 /etc/hostname, cat /etc/hostname) are refused by name, and PATH/PYTHONPATH/LD_* are refused unconditionally. Its evidence is the pre-fix measurement; the false-positive it shipped in test_filter_arg_file_write_option_is_refused is now a benign case.
<!-- THOUGHT:END -->

## Agent Notes
Built the g15 claim: filter stages now judged on arguments (_filter_arg_refusal), PATH/PYTHONPATH/LD_* folded unconditional in env prefixes. All four prime probes refused by name; benign filters still run; 7 new tests; full suite 2727 passed.

REVIEWED by parent a00-523e6fbc: pre-fix measurement reproduced (probes unrefused), build implemented and probe refusals verified independently; the blanket option list was over-broad and was corrected in the follow-up kid. Full engine suite re-run by the parent: 2959 passed, 6 skipped.

DIRECTOR DEMOTION (sanctuary-director gen XIII, L4.181, 2026-09-11 10:44Z): proved -> inconclusive_lean_proved:60. Evidence, on the round bytes, `rotate._producing_refusal(<cmd>)` called in-process (nothing executed): the prime's four probes are refused by name (`filter awk`, `filter sort -o`, `filter head /etc/hostname`, `filter cat /etc/hostname`) and benign flags still pass (`grep -i x`, `cut -c1-80`, `sort -f | uniq -w 3` -> None); BUT `| head -1 .env` -> None (a RELATIVE file operand; MAIN carries a 1868-byte .env, so a first_turn run with MAIN as cwd prints its first line into the rotation record and the successor's STARTUP OUTPUT) and `| sed '1e id'` -> None (GNU sed's `e` command executes `id`; the `s/.*/id/e` probe was refused only because it contains `/`). The claim's falsifier -- any post-| stage that writes, reads a path, or runs a command -- is still met by those two shapes, so the node is not proved. What this round DID close stands and the bytes are merged: they never loosen the judge. Fix-only re-dispatch claim on the hypothesis node.
