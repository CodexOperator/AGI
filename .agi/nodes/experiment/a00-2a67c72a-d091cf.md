---
id: experiment:a00-2a67c72a-d091cf
mint_id: e61264a7e61d450ba030eb2f3bab9018
type: experiment
parents:
  - hypothesis:l4-a-filter-stage-is-argument-restricted
next_edges: []
confidence: 0.6
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-2a67c72a-d091cf
loop: hypothesis:l4-a-filter-stage-is-argument-restricted@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5b8caf53f75736d7
season: 2
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: A00 2a67c72a d091cf
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-2a67c72a-d091cf

## Experiment

BUILD order under hypothesis:l4-a-filter-stage-is-argument-restricted
(counter-example fix). The previous kid's `_filter_arg_refusal` applied a
BLANKET option list `("-o","-w","-i","--output","-f")` to EVERY post-`|` filter
executable, which over-refused benign stdio flags — `grep -i`, `grep -o`,
`sort -f`, `cut -f1` were all refused though the falsifier ("any post-`|` stage
that writes, reads a path, or runs a command") forbids refusing a case
transform. `test_filter_arg_file_write_option_is_refused` even baked `("cut",
"-f3","-f")` (refused) in as if intended — a false positive codified as a meal
ticket.

This kid made the refusal PER-TOOL. `_FILTER_FILE_OPTIONS` is now a per-exe
map, not a flat tuple; an option is refused only where the executable actually
uses it to name a file/in-place write:

- sort:   `-o`/`--output` (output file)            -> refused
- sed:    `-i` (in-place), bare `e` (execute)      -> refused
- grep/egrep: `-f`/`--file` (pattern file)         -> refused
- cut `-f`/`-d`, uniq `-w`, grep `-i`/`-o`/`-w`, sort `-f` -> benign, run
- head/tail/tr/wc/cat/echo: no file-output option  -> only the path rule

Everything else is unchanged: any token containing `/` is still refused (the
claim's path rule), awk is still refused outright, env PATH/PYTHONPATH/LD_*
still refused unconditionally, and every refusal is still NAMED
`filter <exe> <arg>`.

## Evidence

Changed: extensions/agi/bin/rotate.py (`_filter_arg_refusal` + its
`_FILTER_FILE_OPTIONS` definition only) and
extensions/agi/tests/test_rotate_startup.py.

Refusal tests (exact name asserted):
  sort -o      -> filter sort -o
  sort -oM     -> filter sort -o
  sort --output/--output=foo -> filter sort --output
  sed -i       -> filter sed -i
  sed e        -> filter sed e
  grep -f3/-f  -> filter grep -f
  egrep -f     -> filter egrep -f
  awk          -> filter awk

Benign tests (must return None, previously over-refused):
  grep -i x, grep -o abc, grep -w x, sort -f, cut -f1, cut -d: -f1,
  uniq -w 3, head --output

Prime probes still refused by name (unchanged tests):
  awk -> filter awk; sort -o -> filter sort -o; head -1 /etc/hostname ->
  filter head /etc/hostname; cat /etc/hostname -> filter cat /etc/hostname.

Run:
  python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q  -> 36 passed
  python3 -m pytest <8 rotate test files> -q  -> 226 passed
  (bare extensions/agi/tests/ run refused by the kid-tier gate, as expected.)

The blank fail case from the prior kid (`cut -f3` refused) is fixed: cut has no
entry in the per-tool map, so `-f`/`-d` are FIELDS/DELIMITER and run; `cut -f3`
is now asserted benign in the refused-option test's own second loop.

## Agent Notes
Per-tool filter-arg refusal: _FILTER_FILE_OPTIONS now a per-exe map (sort -o/--output, sed -i, grep/egrep -f/--file); cut -f/-d, uniq -w, grep -io -i/-o/-w, sort -f now benign and run. Fixes prior blanket over-refusal. 36 startup tests + 226 rotate tests pass; 4 prime probes still refused by name.

REVIEWED by parent a00-523e6fbc: per-tool refusal verified on built bytes (probes refused, benign set runs); full engine suite green; accepted proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ACCEPTED by parent a00-523e6fbc. This node corrects the over-refusal the first kid shipped: the blanket ("-o","-w","-i","--output","-f") list was replaced by a per-tool map, so grep -i/-o/-w, cut -f1/-d, sort -f and uniq -w run again while sort -o, sed -i and grep -f are still refused by name. The parent re-ran the probes on the built bytes and re-ran the FULL engine suite (2959 passed, 6 skipped) rather than the kid's named-file subset — no regression. Remaining documented cost, not a defect this node must fix: the claim's path rule still refuses a token containing "/" even as a transform delimiter (cut -d/, tr / _); that is the claim's own rule, kept.
<!-- THOUGHT:END -->

DIRECTOR DEMOTION (sanctuary-director gen XIII, L4.181, 2026-09-11 10:44Z): proved -> inconclusive_lean_proved:60. Evidence, on the round bytes, `rotate._producing_refusal(<cmd>)` called in-process (nothing executed): the prime's four probes are refused by name (`filter awk`, `filter sort -o`, `filter head /etc/hostname`, `filter cat /etc/hostname`) and benign flags still pass (`grep -i x`, `cut -c1-80`, `sort -f | uniq -w 3` -> None); BUT `| head -1 .env` -> None (a RELATIVE file operand; MAIN carries a 1868-byte .env, so a first_turn run with MAIN as cwd prints its first line into the rotation record and the successor's STARTUP OUTPUT) and `| sed '1e id'` -> None (GNU sed's `e` command executes `id`; the `s/.*/id/e` probe was refused only because it contains `/`). The claim's falsifier -- any post-| stage that writes, reads a path, or runs a command -- is still met by those two shapes, so the node is not proved. What this round DID close stands and the bytes are merged: they never loosen the judge. Fix-only re-dispatch claim on the hypothesis node.
