---
id: verdict:measured-argv-independent-verdict
mint_id: 54cef43b505b4e4e9181414a4758c937
type: verdict
parents:
  - experiment:a00-0349f27c-grok-measured-argv
next_edges: []
confidence: 0.9
edited_by: a00-d42c2ceb
evidence_runs:
  - experiment:a00-0349f27c-grok-measured-argv
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 80217757985081eb
season: 2
title: "Independent verdict: grok-bot measured argv holds on landed bytes"
town: core
verdict: proved
---
# verdict:measured-argv-independent-verdict

## Verdict

`proved` (confidence 0.90). The `goal:g7.31.1.1` falsifier holds on the
LANDED bytes of this checkout. Independent re-run by `a00-d42c2ceb`, no code
edits, read-only on the adapter and its test.

## Evidence — falsifier conjunct 1: argv matches the recorded --help

Landed adapter carries no guessed flag (exit 1 = no match):

```
$ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
$ echo grep_exit=$?
grep_exit=1
```

The call site reaches the bytes. Throwaway probe under
`.agi/sessions/iter-DT.98/a00-d42c2ceb/probe_live.py`, importing `adapters`
from `extensions/agi/bin` and calling
`adapters.load("grok_bot").build_command(harness={...bin:/SENTINEL/grok-bot,
tier=kid}, tier="kid", context_file="/tmp/brief.md")`:

```
$ env -u TMUX -u TMUX_PANE python3 .agi/sessions/iter-DT.98/a00-d42c2ceb/probe_live.py
["/SENTINEL/grok-bot"]
```

`['<bin>']` — the bare resolved bin. No `-p`, no `--model`, no context file in
argv.

Re-measured `grok-bot --help` of the recorded package
(`/tmp/grokmeasure`, `grok-bot-cli@0.3.1`):

```
$ /tmp/grokmeasure/node_modules/.bin/grok-bot --help > .../help.txt ; echo $?
0
$ wc -l .../help.txt
46 .../help.txt
$ sha256sum .../help.txt
b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1  .../help.txt
$ grep -nE '(^| )-p( |$)|--model' .../help.txt ; echo grep_exit=$?
grep_exit=1
```

46 lines, exit 0, sha256 matches the recorded measurement, and the help names
neither `-p` nor `--model`.

## Evidence — the landed test file is green and falsifiable (MUR D3)

Full adapter test file on the landed bytes:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
.............................                                            [100%]
29 passed in 14.00s
```

The D3 test runs (not skipped):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider -k test_stat_reader_delegates
.                                                                        [100%]
1 passed, 28 deselected in 5.84s
```

Bite proof on a SCRATCH COPY only (repo file untouched): `real_open =
_REAL_OPEN` -> `real_open = builtins.open` at test line 200,

```
$ PYTHONPATH=$PWD/extensions/agi/bin pytest .../mut_test.py -k test_stat_reader_delegates
...
E       AssertionError: a reader built under an installed fake must NOT chain into it: /tmp/pytest-of-belam/pytest-1828/.../sentinel.txt
.agi/sessions/iter-DT.98/a00-d42c2ceb/mut_test.py:792: AssertionError
FAILED .agi/sessions/iter-DT.98/a00-d42c2ceb/mut_test.py::test_stat_reader_delegates_to_import_open_when_installed_twice
1 failed, 28 deselected in 9.69s
```

## Evidence — MUR residue D1 (list-form `evidence_runs`)

Both committed nodes carry YAML LIST form, not a scalar:

```
hypothesis:a00-0349f27c-4362d3 line 10:  evidence_runs:
                                        11:    - experiment:a00-0349f27c-grok-measured-argv
experiment:a00-0349f27c-grok-measured-argv line 9:  evidence_runs:
                                                   10:    - experiment:a00-0349f27c-grok-measured-argv
```

D3: `test_stat_reader_delegates_to_import_open_when_installed_twice` exists at
test line 771 and is executed (above). D2 (GOALS.md stale vs horizon) is moot
on this base: the node is `status: active` and GOALS.md agrees.

## Confidence

0.90. All four checks re-derived independently from the landed bytes; the only
judgement is that the pasted `--help` measurement is the right reference
surface, which the parent accepted and this run re-verifies byte-for-byte.
0.0 – 1.0

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Independent re-run by a00-d42c2ceb, no code edits. Grep, live probe, --help re-measurement, full test file, D3 mutation bite and D1 list-form check all re-derived from the landed bytes; verdict proved at 0.9.
<!-- THOUGHT:END -->
