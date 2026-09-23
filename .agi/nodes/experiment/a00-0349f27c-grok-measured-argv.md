---
id: experiment:a00-0349f27c-grok-measured-argv
mint_id: 25f3e24204f146b0aa9e210070107d59
type: experiment
parents:
  - hypothesis:a00-0349f27c-4362d3
next_edges: []
edited_by: a00-0349f27c
evidence_runs:
  - experiment:a00-0349f27c-grok-measured-argv
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 66bf70161cf5bfbd
season: 2
testable_claim: On tip f655a6714 with the re-landed measured bytes, adapters.load("grok_bot").build_command(...) emits the bare resolved bin with no -p and no --model (matching the recorded grok-bot --help); and the adapter test stat reader delegates to the open captured at import when a fake open is already installed.
title: Measured grok-bot argv re-landed on f655a6714, plus an executed _stat_reader delegation test
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0349f27c-grok-measured-argv

The DT.98 re-land run for `goal:g7.31.1.1`, under
`hypothesis:a00-0349f27c-4362d3`. It lands the MUR-reviewed measured bytes on
this round's base `f655a6714` and closes MUR residue D3 (the `_stat_reader`
delegation branch was dead code as tested).

## What was done

1. Copied the MUR-reviewed bytes from the accepted round's worktree
   (`.../worktrees/a00-8c0c4372/`) onto this base:
   `extensions/agi/bin/adapters/grok_bot_adapter.py` and
   `extensions/agi/tests/test_grok_bot_adapter.py`. (The brief pointed at a
   `ref/` dump under the parent's session dir; that directory does not exist,
   so the bytes were read from the accepted-round worktree itself.)
2. Appended `test_stat_reader_delegates_to_import_open_when_installed_twice`
   to the adapter test: it installs a first fake `builtins.open`, builds
   `_stat_reader(os.getpid(), "S")` WHILE that fake is live, then opens a real
   temp file through the built reader. The reader must reach the REAL file
   (the `open` captured at import), never the first fake.
3. Re-measured `grok-bot --help` for the recorded package.
4. Ran the adapter test file, then the mutation bite proof.

## Evidence

The adapter now contains no guessed flag (exit 1 = no match):

```
$ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
$ echo grep_exit=$?
grep_exit=1
```

`--help` re-measurement of the recorded package (`/tmp/grokmeasure`,
`grok-bot-cli@0.3.1`), verbatim:

```
$ /tmp/grokmeasure/node_modules/.bin/grok-bot --help > /tmp/help.txt ; echo $?
0
$ wc -l /tmp/help.txt
46 /tmp/help.txt
$ sha256sum /tmp/help.txt
b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1  /tmp/help.txt
$ grep -nE '(^| )-p( |$)|--model' /tmp/help.txt ; echo grep_exit=$?
grep_exit=1
```

Full test file, verbatim (tier-gate phantom-record lines elided; they are
harness noise, not test output):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
.............................                                            [100%]
29 passed in 10.53s
```

## Bite proof (the new test is falsifiable)

`real_open = _REAL_OPEN` was temporarily changed to
`real_open = builtins.open` inside `_stat_reader` (test helper line 200), the
new test run, then the line restored (`grep -n '^    real_open'` -> `200:    real_open = _REAL_OPEN`). The mutated helper delegates into the
first fake:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider -k test_stat_reader_delegates
F                                                                        [100%]
=================================== FAILURES ===================================
________ test_stat_reader_delegates_to_import_open_when_installed_twice ________
...
extensions/agi/tests/test_grok_bot_adapter.py:206: in fake_open
    return real_open(file, *args, **kwargs)
...
    def first_fake(file, *args, **kwargs):
        first_fake_calls.append(str(file))
>       raise AssertionError(
            "a reader built under an installed fake must NOT chain into it: "
            f"{file}")
E       AssertionError: a reader built under an installed fake must NOT chain into it: /tmp/pytest-of-belam/pytest-1810/test_stat_reader_delegates_to_0/sentinel.txt

extensions/agi/tests/test_grok_bot_adapter.py:792: AssertionError
=========================== short test summary info ============================
FAILED extensions/agi/tests/test_grok_bot_adapter.py::test_stat_reader_delegates_to_import_open_when_installed_twice
1 failed, 28 deselected in 16.66s
```

Restored:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider -k test_stat_reader_delegates
.                                                                        [100%]
1 passed, 28 deselected in 2.62s
```

## Scope / honesty

- Production lines (test file excluded): `59 added / 17 removed` on
  `extensions/agi/bin/adapters/grok_bot_adapter.py` = 76 lines, under the 2x
  ceiling of 80. Recorded as `production_lines: 76` / `line_ceiling: 40`.
- No edit to `dispatch.py` or `rotate.py`; no `grok` string special-case.
- `evidence_runs` is a LIST (MUR residue D1), self-cited as the run itself.
- The adapter bytes are a copy of the already MUR-reviewed round; this round
  re-lands them rather than re-authoring them.
