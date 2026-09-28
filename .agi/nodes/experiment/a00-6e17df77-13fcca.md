---
id: experiment:a00-6e17df77-13fcca
mint_id: a042793af3354ee89bc737d74297ee04
type: experiment
parents:
  - hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config
next_edges: []
confidence: 0.9
edited_by: a00-efb453b1
evidence_runs:
  - experiment:a00-6e17df77-13fcca
loop: hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 7509e4cdc32f9ee6
season: 2
title: the import-time spawn fence plus os.system exec posix_spawn killpg leaves, each red on the kid-1 bytes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6e17df77-13fcca

Closing PASS 9 items (4) and (5) of the parent brief: the process guard's
UNFENCED stdlib leaves, and the guard's blind spot at import time. All bytes
under `extensions/agi/tests/`; zero bytes under `extensions/agi/bin/`.

## Item (5) — is import time closable by a fixture? MEASURED: no.

| ordering of the fence | a module-level `subprocess.run(["echo",...])` in an opted-in module | probe rc |
|---|---|---|
| function-scoped autouse fixture (today) | NOT REFUSED — `echo` really ran | 1 passed |
| session-scoped autouse fixture | NOT REFUSED — `echo` really ran | 1 passed |
| conftest IMPORT-time install (this fix) | REFUSED, "NO_REAL_PROCESSES ... at IMPORT time" | 1 passed |

Why: pytest imports a test module during COLLECTION, which is after every
fixture setup, session-scoped or not. The only thing that runs earlier is the
conftest module import itself, so the fence is installed by a plain
import-time call (`_install_spawn_fence()` at the bottom of conftest.py) and
undone in `pytest_unconfigure`. It is deliberately NOT a
`pytest_collectstart` hook: a hook in the tests-dir conftest is registered
when that conftest is imported, and the conftest import already precedes
every test module import, so the hook buys nothing and would be a second
place to forget.

The fence is call-time opt-in (`_caller_opted_in()` walks the whole frame
stack for `NO_REAL_PROCESSES`), which is what lets it be installed
unconditionally at import while still passing every non-opted-in spawn
straight through — a session-wide ban would red the 178 files the wider suite
legitimately needs.

## Item (4) — every process-creating stdlib leaf, one list

`_FENCED_SPAWN_LEAVES` is now ONE source per rule, applied by both the
fixture (`_fence_spawn_leaves(monkeypatch.setattr, refuse)`) and the
import-time fence, so the two cannot drift. Before: 6 leaves. Now 14 —
`subprocess.{Popen,run,call,check_output}`, `os.{fork,forkpty,execv,execve,
execvp,execvpe,posix_spawn,posix_spawnp,system}`, `pty.spawn` — plus
`os.kill` and `os.killpg`.

Red-on-old, measured by running this round's offender table against the
POST-kid-1 baseline conftest (af03d8133) and against these bytes:

| offender | old conftest (af03d8133) | these bytes |
|---|---|---|
| `os.system('true')` | NOT REFUSED (rc 0, real shell) | REFUSED |
| `os.execv('/bin/true', ...)` | NOT REFUSED (rc 0 — the pytest process was REPLACED) | REFUSED |
| `os.posix_spawn('/bin/true', ...)` | NOT REFUSED (rc 0) | REFUSED |
| `os.killpg(os.getpgid(0), 0)` | NOT REFUSED (rc 0) | REFUSED |
| import-time `subprocess.run` | NOT REFUSED (rc 5, no collection error) | REFUSED |
| import-time `os.system` | NOT REFUSED (rc 5) | REFUSED |
| `pty.spawn(['true'])` | already refused — it reaches `os.forkpty` | REFUSED (now at the `pty.spawn` leaf itself) |

`os.killpg` is refused OUTRIGHT, and that is the honest rule rather than a
lazy one: a group leader the test spawned can share a group with a shell the
test never spawned (the session group it inherited), so "own pid" is not a
sound exemption for a GROUP. `_make_guarded_killpg` takes the real call as a
parameter and a unit test drives it with a RECORDER that stays empty — no live
group is signalled anywhere in this file, and the only `killpg` probe in the
offender table is signal 0, which delivers nothing.

## Conjunct tests (red when the patch is removed)

One test per new patch point, plus one per mechanism:
* `test_guarded_killpg_refuses_outright_and_arms_no_syscall` — recorder.
* `test_every_fenced_spawn_leaf_exists_and_is_fenced` — every entry in the
  list resolves in this interpreter (a typo or a renamed stdlib leaf is RED
  here, not silently dead weight at runtime).
* `test_spawn_fence_install_and_uninstall_restore_the_module` — install on a
  STUB module (never on os/subprocess, which the running suite is using),
  assert pass-through, assert the original object comes back.
* `test_unit_loading_the_conftest_leaves_the_session_fence_alone` — the
  by-path unit load sets `AGI_TESTS_CONFTEST_UNIT_LOAD=1` and must not
  install-then-remove the process-wide fence under the running suite.
* `test_import_time_fence_lets_a_plain_module_spawn_at_import` — the fence
  is opt-in, not a session-wide ban.
* six new rows in `OFFENDING_SRCS` (above), each red on the old bytes.

## Residue — named, not closed

* **item (3), `os.open("/proc/...")` stays unfenced.** The C `_io.open` never
  calls the Python-level `os.open`, so a hook there catches nothing; the
  `/proc` and live-config checks live on `builtins.open`/`io.open`/
  `os.scandir`/`os.listdir` and those are still FIXTURE-scoped, so an
  import-time `/proc` read in an opted-in module is still uncaught. Widening
  them to import time was out of budget and is the next honest step: it means
  replacing `builtins.open` for the whole session, including pytest's own
  assertion-rewriting and reporting path.
* `os.startfile` (Windows-only, absent here) and third-party spawners
  (paramiko, multiprocessing) are not in the leaf list.
* the import-time fence does not cover bound engine names (`rotate._RUN`,
  `workflow._REAL_POPEN`); those are fenced at fixture level only, so a
  module-level `rotate._RUN([...])` in an opted-in file still escapes.
* engine-side seams remain residue with file:line, per the brief.

## Suite

```
extensions/agi/tests/test_conftest_guard.py test_rotate_term_grace.py
  test_send.py test_credential_none_spawn.py test_agi_env_strip.py  -> 397 passed
extensions/agi/tests/test_rotate.py test_cli.py                      -> 402 passed
```

## Agent Notes
import-time spawn fence (session fixture measured insufficient) + 8 new stdlib process leaves incl. os.killpg refused outright; 6 offenders red on af03d8133, green on these bytes; 799 suite tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-VERSION (a00-efb453b1, DH.422) -- verdict unchanged (proved, 0.9). Five parent-run probes, each with a control, and one flake recorded rather than ridden.

(1) WHAT THE BRIEF SAID, quoted: "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF, NEVER AGAINST ITS THOUGHT OR ITS SUMMARY" and "run one negative probe per claim conjunct yourself". (2) WHAT THE MACHINE ACTUALLY DOES. Diff fff8e4a5c vs af03d8133: conftest.py +152, test_conftest_guard.py +138, node +127 -- three paths, all under extensions/agi/tests/, so production_lines: 0 is true by the diff. The claim under test is a claim about a PROCESS-WIDE, IMPORT-TIME patch of thirteen stdlib leaves in a conftest shared by the whole suite, so the blast radius is the finding, not a formality. My probes, each an independently written module symlinking the REAL conftest, each paired with a non-opted-in control:
  - GATE, item (4), the new leaves: os.system REFUSED, os.posix_spawn REFUSED, os.killpg REFUSED, each with the guard's own message. The CONTROL in a module WITHOUT the opt-in flag: `PARENT-PROBE control os.system rc=0` -- a real shell ran. Without that control the three refusals prove nothing, because a refusal is also what an over-broad patch produces.
  - GATE, item (5), the ordering claim that decides the whole design: a module-level `os.system("true")` in an opted-in file now fails COLLECTION with "a NO_REAL_PROCESSES module called os.system at IMPORT time (collection), where no fixture can guard it"; the same file without the flag collects clean and runs its shell. The kid's table says a session-scoped fixture is exactly as late as a function-scoped one, and that is the load-bearing measurement of this round: it is what forces an import-time install instead of the obvious scope bump. A reader who skipped the table would think a session fixture would have done.
  - BLAST RADIUS, the wider suite named file by file, twice: the ten-file set the two previous parent reviews used gives `1 failed, 896 passed, 5 skipped` on the first run and `897 passed, 5 skipped` on an identical rerun, and test_rotate.py alone is 331 passed. The one failure, test_rotate.py::test_spawn_seating_row_commits_joined_pid_and_session_and_prints, is therefore FLAKY, not caused by the session-wide fence: it did not reproduce on the rerun, nor in the three-file and two-file subsets. I am recording it rather than hiding it, because a shared conftest that patches os.fork and subprocess.Popen for the whole session is exactly the kind of change that earns an honest flake note.
  - The narrower suites the kid claimed reproduce: test_rotate.py 331 passed, term_grace + send + guard subsets green.
(3) THE NEAR MISS, as a counterfactual: the obvious implementation of item (5) -- bump the autouse fixture to session scope -- satisfies the words ("the guard now covers import time") and loses the mechanism, which is what the kid's own table shows: a module-level subprocess.run really ran under a session fixture. The second near miss is the fence's OPT-IN test, a walk of the whole frame stack for a module global. It is correct for the file that declares the flag, and it is the one place where this round could bite a future file: a helper DEFINED in an opted-in module and called by a NON-opted-in test carries the opted-in module's globals on the stack and would be refused. I did not construct that case, so I do not claim it; it is named here as the residual shape to watch, alongside the one the kid named (the import-time fence does not cover bound engine names, so a module-level rotate._RUN([...]) still escapes).
(4) IF I DEVIATED FROM A STANDING RULE: none. Read-only git diff/log; no commits by me; the kid's cli.py done landed fff8e4a5c byte for byte as reviewed.

Item (3), the unfenced os.open on /proc, stays a NAMED RESIDUAL and the kid's reason is the right one and is now on the record: widening the builtins.open hook to import time means replacing it for the whole session, including pytest's own assertion-rewriting and reporting path. That is a design change with its own risk, not a line to add inside this row.'
<!-- THOUGHT:END -->
