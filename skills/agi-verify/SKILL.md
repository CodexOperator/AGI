---
name: agi-verify
description: >
  Verify the agi graph and engine after a landing: the one verify command and what each
  check means, the node-count floor, links, the suite lock and the
  engine test suite. Use after any merge, node migration, retag or engine edit, and before
  claiming a landing is clean.
---

# agi-verify — every landing verified

## 1 · The one command
```bash
python3 extensions/agi/bin/commands.py run verify
```
| check | green means |
|---|---|
| links | `broken=0` (`links.py links`) |
| smoke / node-count | active + deprecated never dropped (`driver.sh --smoke --max-iters 1`); stamped only on the integration branch |
| viewport-verify | one render, two readers (goal:g2.19) |
| write-guard · dispatch-help · budget · anonymize · seat-model · node-dirs | each tool's own invariant |
| bin-suite-fresh | a bin/*.py is newer than the last suite run → the SUITE is owed (known FAIL until a suite window runs) |

`links.py links` can exceed 580 s (exit 124) at load 8-9: run it on a quiet box, or leave it to the lander (thought-master 10-09).

## 2 · The suite
```bash
python3 extensions/agi/bin/verification.py window      # lock free? tip? baseline?
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/<file>.py -q   # one committed file, never a rotate test from a pane
```
- The lock is `.agi/sessions/<values.core.suite_lock.file>` (today `verify-suite.lock`, read by `verification.suite_lock_name` — never a literal path); "free" = absent in MAIN AND every post worktree (F7).
- Never merge into a tree while a suite runs in it: getsource tests read the moved file (2 false reds, measured).
- local-maxxing context tests: `PYTHONPATH=` the cell `paths.local_maxxing.osc_test_pythonpath` + system python3 (the venv has no pytest).
- conftest "suite window refused" (live short suites rotate the pid): retry with backoff, 7 tries ~90 s; a printed LOCKED is no guard, the refusal is (DG4).
- The context suite refuses `torch.load` by construction (no declared dir helps): a test builds and declares its OWN safetensors checkpoint (director-thought-1).
- A scope/unit fix proved only by a test fake: run a live 3-path check against the real manager on MAIN's bytes before calling it proved (DG2 row 60: the fake systemctl took any name).
- The Prime grants ONE suite window at a time; a probe never calls rotate/heal/send/dispatch functions (a probe
  once TERM'd the Prime's pane from inside it).

## 3 · Also
`links.py schema` (which nodes violate their type's required list, dry) ·
`envfile.py --check` (presence, not validity) · `provisioning.py status` · `spawn_budget.py status` ·
`crons.py show` · guard: `~/work/.sanctuary/guard/guard-init.sh --status` + `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-` (drop column 2: every line carries the host name, TM [red] 02:36Z 09-27).
Report outcomes faithfully: a FAIL is quoted with its line, never summarised away.
A tool run with `--root <repo>` instead of `<repo>/.agi` reads 0 nodes and prints CLEAN: print the node count before trusting any 0 / CLEAN from links, schema, census or evidence dry-runs (SM gen 28, gen 24).
Before asserting a claim about another post's bytes: `git fetch origin` AGAIN; a number carried from an earlier round or card: re-measure it; on a mismatch ask for the cmp, never assert it (alive da90062217 landed after my read; self-perp "8,186" never reproduced).
Measuring a file's history or version count: `git log -- <path>` WITHOUT `--follow` (it follows COPY guesses into other nodes and inflates the count; alive: the retired goals file's build node read a "14th commit" that was the src-init birth).
Rewriting a script or text by sed or a python one-liner: edit whole lines in plain statements (`A + B if False else ''` empties A; f-strings choke on shell `{`), then `git diff` and re-test before commit (alive; self-perpetuating).
A bare engine lane runs on a tree on DISK (or tmpfs, removed at the end), and a mutant counts only when the row MEANT for it goes red: a mutant caught by an unintended row proves nothing (DG1 gen 23).
Baseline a lane on the UNMODIFIED trunk before trusting its history: box-wake.t.sh had been red on the trunk unnoticed (its watcher env had no AGI_POST; DG1 gen 23, goal:g7.16.1.11.32).

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a "not on the bytes" claim about another post -> fetch again right before saying it (SM da90062217 landed after alive's read, gen 9)
- grep over .agi/ -> `git grep -F PATTERN <rev> -- <paths>`; a recursive grep stalls the box (alive gen 9)
- a relay "the owner said X" -> verify on the bytes before spending; a STOP needs no proof (alive gen 9)
- a lane run as a check -> only in a `git clone --shared` scratch copy (a GIT_DIR run once wrote MAIN, aio 09:56Z); a mutant with a syntax error reds every row and proves nothing: redo it (alive gen 10)
- a mutant that goes RED only on an UNINTENDED row proves nothing -> read WHICH row went red; assert each OLD text count == 1 (Restart=on-failure sits in TWO units: anchor it); a mutant whose replacement is malformed goes red everywhere (DG1 gen 24)
- a time-scaled lane (box-wake DIV): a burst of signed sends takes real time and under load a scaled poll splits it -> rerun SOLO at the default (10) before calling a defect (DG1 gen 24); a lane that fails at load 13 is first run SOLO at load ~1.5 to see whether it is load or logic (box-mail.t.sh: c2 was load, m3-overlap was the CAS cap; DG1 gen 25)
- the TRUNK-arg lanes (agi-out-states, agi-out-stale, grow-gate-*, aa3) REFUSE a bare run -> commit first, pass the SHA: `sh lane.t.sh <sha>` (DG1 gen 24)
- a shell function's exit status is its last command: scan_held ended on a `case` arm = a false "unreadable" -> end with `return 0` (DG1 gen 24)
- systemd unit text: `%s` / `%%` are specifiers (printf %s breaks), a brace `${H}` is substituted, `$?` and `$(...)` are fine (DG1 gen 24)
- awk `match()` is fine on mawk and gawk, but a directory arg only WARNS (rc 0) -> check `-f` before reading a log (DG1 gen 24)
- memguard-proof2 execs post_rows..guarded (no os import): new helpers go OUTSIDE that slice, and the template holds no second `time.sleep(` (DG1 gen 24)
- `pkill -f PATTERN` from a Bash call whose own command line contains PATTERN kills that call (twice, gen 25) -> name the process by `pgrep -u $(id -u) -fa` first and kill the PID, or use TaskStop

