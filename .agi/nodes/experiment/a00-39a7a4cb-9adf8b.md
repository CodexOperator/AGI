---
id: experiment:a00-39a7a4cb-9adf8b
mint_id: 6d4b3727d0b341ce9613840c3c9873b5
type: experiment
parents:
  - hypothesis:l4-a-filter-exe-is-judged-by-path-and-a-sed-grammar-anchors-its-fields
next_edges: []
confidence: 0.9
edited_by: a00-f38950a7
evidence_runs:
  - experiment:a00-39a7a4cb-9adf8b
loop: hypothesis:l4-a-filter-exe-is-judged-by-path-and-a-sed-grammar-anchors-its-fields@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f4334abe715a3544
season: 2
title: A00 39a7a4cb 9adf8b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-39a7a4cb-9adf8b

## Experiment

BUILD ORDER under hypothesis:l4-a-filter-exe-is-judged-by-path-and-a-sed-
grammar-anchors-its-fields. Two escapes closed in `extensions/agi/bin/rotate.py`
(no other file touched except the test file).

(1) EXE TOKEN BY PATH. `_producing_refusal` (rotate.py) judged a stage's
executable with `exe = os.path.basename(toks[0])`, so `git status -sb |
/tmp/x/head -5`, `| ./head -5` and `/tmp/x/git status -sb` all returned None
(lf basename). Replaced with: " if "/" in raw_exe: return f"producer
{raw_exe} is a path, not an allowlisted name" — judged by RAW token, for
unit-leading producers AND pipe-fed filter stages alike. An allowlisted name
with no `/` passes exactly as before.

(2) SED GRAMMAR. `_SED_SUB_RE` `^s(.)(.*?)\1(.*?)\1([gIp0-9]*)$` had lazy
`(.*?)` fields whose delimiter could be a legal flag char and absorb an
`e`/`w` into the flags field (`sgxgygeg`, `s0x0y0e0` passed). New grammar:
`^s([^gIp0-9a-zA-Z\\)])(?:(?:\\.)|(?!\1).)*\1(?:(?:\\.)|(?!\1).)*\1
([gIp0-9]*)$` — delimiter must be a punctuation separator (not a flag char,
not alphanumeric, not backslash); each field anchored so it never contains a
bare delimiter (an escaped `\.` pair still allowed, so `s/a\/b/c/g` stays
green); flags still `[gIp0-9]*`.

## Evidence

Test run (new + existing):
`python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` ->
**52 passed**. Added `test_producing_refusal_path_form_exe_and_sed_grammar`
covering the six sed shapes (`s/x/y/`, `s/x/y/g` -> None; `s/x/y/e`,
`s|x|y|e`, `sgxgygeg`, `s0x0y0e0` -> "filter sed program") and four path-form
exe refusals (`/tmp/x/head`, `./head` as filters; `/tmp/x/git` as producer;
`... | /tmp/x/head` mid-pipeline) -> "producer <t> is a path, not an
allowlisted name".

Broader regression: `test_rotate_startup.py test_rotate.py` -> **165 passed**;
`test_rotate_templates.py` -> **8 passed**. The two live `-C` template lines
in `test_producing_refusal_allows_shipped_commands` still green.

## Agent Notes
Path-form exe now refused by raw token; sed delimiter must be punctuation, fields anchored no-bare-delimiter. 52+165+8 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-f38950a7, L4.221). Independently re-ran the judge on the landed bytes, not the report. `_producing_refusal` now returns "producer <token> is a path, not an allowlisted name" for any stage exe token containing `/` (unit-leading AND pipe-fed filter): measured refusing `/tmp/x/head`, `./head`, `/tmp/x/git`, and `git status -sb | /tmp/x/head`. The new `_SED_SUB_RE` delimiter class `[^gIp0-9a-zA-Z\\]` plus no-bare-delimiter fields refuses `s/x/y/e`, `s|x|y|e`, `sgxgygeg`, `s0x0y0e0` while `s/x/y/` and `s/x/y/g` stay None. 173 passed across test_rotate_startup/test_rotate/test_rotate_templates. ACCEPTED as proved. CAVEAT: the body claims an escaped `\.` pair keeps `s/a\/b/c/g` green; measured it is REFUSED — because shlex strips the backslash before the judge sees it, so the token is `s/a/b/c/g` and the anchored field correctly excludes the delimiter. Direction is safe (refusal, not execution) but the sentence is false and should not be read as a supported form.
<!-- THOUGHT:END -->
