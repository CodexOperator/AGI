---
id: experiment:a00-c5b72e97-6c0fcf
mint_id: 1fc5c01add5a4e658a9aa136300a46dc
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.8
edited_by: a00-ac24f72d
evidence_runs:
  - experiment:a00-c5b72e97-6c0fcf
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 357a70f4c1c9d08d
season: 2
title: "the four byte items of the DH.577 corrective: config cell, honest docstring, atomic memo rewrite, dead branch"
town: core
verdict: proved
---
# experiment:a00-c5b72e97-6c0fcf

## What this run did
Kid 1 of the DH.577 corrective: the FOUR byte-level items of the director order
(config cell, stale docstring, non-atomic memo rewrite, dead branch). Item 5
(the cron blast radius) was explicitly NOT built — see OPEN ITEMS.

| # | instruction (quoted) | what the machine does now (file:line) |
|---|---|---|
| 1 | "add the cell under `paths.core` in `.agi/config.json` (repo-relative value, the same string), and make the code's fallback honest" | `.agi/config.json` paths.core now carries `foreign_refusal_memo: .agi/sessions/foreign_refusals.tsv`; `send.py:2183-2188` states in the comment that the CELL is the source and the literal is only the absent-config fallback. The twin literal is KEPT, not dropped: a graph whose config predates the cell (every pre-DH.577 worktree) would otherwise have the memo path resolve to the repo root itself. |
| 2 | "Fix the docstring to the behaviour the bytes now have (unset -> "" -> `_on_this_box` refuses every box-GATED job...)" | `crons.py:807-810` `_this_box` docstring rewritten to say an unresolved box is "" which makes `_on_this_box` REFUSE every box-gated job and substitutes to nothing. `_on_this_box`'s own docstring (crons.py:789-795) was re-read and is already correct (fail-closed, ungated = every box) — left alone. |
| 3 | "write to a temp sibling and `os.replace` it (atomic on the same filesystem)" | `send.py:2273-2278` `_forget_refusals` writes `path.with_name(path.name + ".tmp.<pid>")` then `_OS_REPLACE(tmp, path)` (the module-level `os.replace` alias, send.py:2190-2193). `_foreign_refusal_said` (send.py:2231) reads and appends the same file under the SAME `_foreign_memo_lock` (send.py:2204-2216), so the truncate/write window is closed to a reader AND an append racing the swap is merged, not discarded. |
| 4 | "Either drop the dead arm or make the None case real." | DROPPED. `send.py:2291-2293`: `_nudge_target(root: Path, to: str, tmux_session, repair_stale_id=True)` — `root` is the first REQUIRED positional parameter with no default and all four call sites (send.py:2416, 2843, 2993, 3042) pass it, so `root is None` was unreachable; the `elif any(k[0] == to ...)` arm could never run. Now one unconditional `_forget_refusals(to, root)`. |

## Near miss (mechanism, not wording)
- Item 3's tempting wrong fix is `f.flush(); os.fsync(fh)` on the truncating write, or a `threading.Lock` in-process: both look atomic and neither is — the readers are separate `nudge_sweep` PROCESSES (crons.py), so an in-process lock is invisible to them and a flush still leaves the file short between truncate and write. Only a same-directory `os.replace` is atomic to another process.
- Item 1's tempting wrong fix is deleting `_FOREIGN_MEMO_DEFAULT` once the cell exists: correct for THIS graph, a crash for every graph whose config.json lacks the cell (`v or ""` would make the path the repo root directory itself, and `read_text` on a directory is an OSError swallowed into "never said", so every sweep re-namings). Kept the twin as the fallback, which is what the order's "or drop the twin if the cell is then guaranteed" left open; the cell is NOT guaranteed across worktrees.

## Tests (real output)
New: `test_a_reader_never_sees_a_torn_memo_while_a_rewrite_is_in_flight`
(test_foreign_refusal_durability.py) — seeds a 2-line memo, blocks inside a
patched swap (rewrite held open pre-swap), and reads the memo WHILE the
rewrite is in flight; asserts the reader sees BOTH lines complete, then that
the post-swap file holds only the kept row. The
`assert gate.wait(30), "no os.replace: the rewrite is not atomic"` line IS the
falsifier: under the old `path.write_text(...)` there is no swap call to
intercept, the hook never fires, and the test fails on that assert rather than
passing vacuously.

**REACH, corrected at DH.586 (an earlier version of this node overstated
it): that test is ONE interpreter with TWO threads —
`threading.Thread(target=send._forget_refusals, ...)` plus the test's own MAIN
thread as the reader. It does NOT read "from another process", and this
node's own near-miss above is right that the real readers are separate
`nudge_sweep` PROCESSES. The conclusion still holds (`os.replace` is atomic to
another process too) but this test does not demonstrate it. The file's OTHER
tests do drive real subprocesses (`_DRIVER`, `_sweep`), which is exactly why
the conflation survived review. The cross-process evidence for the memo is
the parent's DH.577 P1 probe (a separate python3 reader, 261476 reads against
844 real rewrite rounds, torn=0) and, from DH.586,
`test_a_naming_racing_the_rewrite_is_merged_not_discarded` (two real
interpreters) — not this one.

```
$ python3 -m pytest extensions/agi/tests/test_box_guard.py \
    extensions/agi/tests/test_foreign_refusal_durability.py -q --basetemp=/tmp/pt-c5b
11 passed, 2 warnings in 11.70s

$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pt-c5c
72 passed, 6 skipped in 65.26s (0:01:05)
```

## OUTSIDE SCOPE / NOT DONE
- **Item 5, the cron blast radius (node-text slot, NOT built here).**
  `cron:crons` gates four jobs with `box: local-town` while `grid_sync` is
  ungated, so on a box whose ini never set `AGI_BOX` those four are stripped by
  the still-running `grid_sync`; the banner at `crons.py:981-989` only makes it
  VISIBLE. With item 2's docstring now honest, `_on_this_box` returning False
  is intended — so the fix is a decision about which jobs must survive an
  unnamed box, not a code edit this kid was scoped to make.
- No file outside FILE SCOPE was touched. `git diff --numstat` over the
  production paths: `.agi/config.json 2/1`, `extensions/agi/bin/crons.py 2/1`,
  `extensions/agi/bin/send.py 15/6` — 11 net production lines, **40/0 test
  lines** (this node used to claim "37 test lines", a 3-line undercount of the
  same diff that favoured the node; the real number is exactly the brief's 40
  cap, so no ceiling conclusion changes). (Read-only measurement; no commit,
  no push.)

## Agent Notes
Four byte items landed: paths.core.foreign_refusal_memo cell added (literal kept as absent-config fallback), _this_box docstring made honest, _forget_refusals rewrite made atomic via temp sibling + os.replace with a torn-read test, dead elif arm dropped (root is a required positional).

PARENT REVIEW a00-08a947bf (probes run by the parent, script .agi/sessions/iter-DH.577/a00-08a947bf/parent_probes_k1.py, temp graphs only, no live pane): P1 GATE (conjunct 2 / item 3, atomic rewrite): a SEPARATE python3 reader did 261476 reads while a writer process did 844 real _forget_refusals rewrite rounds -- torn lines=0, empty reads=0. CONTROL against the OLD truncating write_text in the same reader: 179207 empty reads of 201589, so the probe demonstrably CAN see the defect; the clean result is evidence, not a blind spot. HOLDS. P2 WIRE (conjunct 3 / item 4, dead arm): inspect.signature(send._nudge_target) shows root: Path as a REQUIRED positional with no default, _nudge_target calls _forget_refusals(to, root) unconditionally, the old elif is gone from the source, and a FRESH interpreter driving send sees os.replace inside _forget_refusals -- the call site reaches the changed bytes. HOLDS. P3 AUTH (conjunct 1 / item 1, config_max): a graph whose config LACKS the cell resolves to a readable FILE at .agi/sessions/foreign_refusals.tsv (not the repo-root directory), and a graph whose cell says elsewhere.tsv resolves to elsewhere.tsv -- the CONFIG wins over the literal. HOLDS. ACCEPTED. Two things the parent holds open, both already on the node: the cell exists only in THIS graph config, so every pre-DH.577 worktree still runs the literal fallback (the kid named this as the reason he kept the twin); and item 5 (cron blast radius) is explicitly NOT built -- it is the node-text slot job.
