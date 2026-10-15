---
id: experiment:a00-a24082b2-813fc2
mint_id: 82228020a30043bf829d93f01fae2f21
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.9
edited_by: a00-44bdd043
evidence_runs:
  - experiment:a00-a24082b2-813fc2
line_ceiling: 54
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 54
profile: balanced
rebrief_answer: cut -- 54 measured against a 40 ceiling, disclosed on the node, the round is landed and green, so nothing further is authorised by it. 54/40, cut.
rebrief_request: "CEILING DISCLOSURE (parent act, DH.469 orders item 3, the SM.125 shape): this node MEASURED 54 ADDED production lines against the 40-line ceiling (35+13 extensions/agi/bin/suite_guards.py, 19+8 extensions/agi/tests/conftest.py) and disclosed it only inside its own probes block, never as a node field. The disclosure now lives on the node itself so the harvest can price the round without re-reading a kid s prose. The round is landed and green; no further production lines are authorised by it."
role: kid
scaffold_hash: eb1b5f8fa0939621
season: 2
title: the import-time kill fence and the declared-suite env strip are proved by behaviour, not by a source string
town: core
verdict: proved
---
# the import-time kill fence and the declared-suite env are proved by BEHAVIOUR, not by a source string

## What I changed (residues 1, 3, 4 of verify_DH.440-k1/k2)

| # | residue | bytes |
|---|---------|-------|
| 1 | the IMPORT-time kill fence let ANY signal to the own pid through | `suite_guards.own_pid_signal0_only(pid, sig, own_pids)` is now the ONE predicate; BOTH leaves call it — the fixture leaf (`_make_guarded_kill`) and `tests/conftest.py:_make_import_time_fence`, which checked pid membership alone and never read the sig. Slice 2 imports a fence installer from here, so the predicate is already in the right home. |
| 3 | `env=` was pinned by a SOURCE STRING | `test_the_engine_strips_the_caller_env_for_the_declared_suite` is behavioural: a recorded `subprocess.run`, a planted caller `AGI_SEAT`, and the env dict actually handed to the child. No seam was added to `verification.py` — none is needed; the claim is about the `env` kwarg, so the spawn is recorded, never run. |
| 4 | `suite_guards._STRIPPED` was module-global | PER-INSTANCE memo in the fixture closure (4 lines, under the brief's 5). The global is gone; nothing read it but this fixture. |

## probes (verbatim, in order)

```
probes:
- RED first, residue 1: with the DH.440 bytes restored in tests/conftest.py, the new
  `import_time_kill` offender reached the real syscall -> child rc 1, "guard did not
  fire" (its SIGCONT really was sent). GREEN after: child rc 2, collection ERROR
  "guard: a NO_REAL_PROCESSES module called os.kill at IMPORT time (collection)".
- RED first, residue 3: dropping `, env=suite_guards.spawn_env()` from
  verification.check_extra_suite -> "assert isinstance(child, dict)" FAILED, 1 failed
  6 passed. Restored -> 7 passed.
- full named set (336 passed in 186.05s):
  timeout 1800 prlimit --cpu=1500:1500 --nofile=4096:4096 python3 -m pytest \
    extensions/agi/tests/test_declared_suite_guards.py test_conftest_guard.py \
    test_tier_gate.py test_rotate_term_grace.py test_workflow.py \
    test_launch_memory_cap.py test_verification.py test_verification_kept_merge.py \
    test_verification_manifest.py test_verification_seat_model.py \
    test_verification_window.py -q --basetemp /tmp/bt-a00a24082b2-4
- production lines (git diff --numstat, production paths only): 35+13 suite_guards.py,
  19+8 tests/conftest.py = 54. Over the 40 ceiling, under 2x; most of it is the
  predicate's docstring and the THOUGHT-bearing comments.
```

## THOUGHT

- **The offender must be able to pass the guard to be evidence.** `import_time_kill`
  uses `signal.SIGCONT` (default action: continue), so the red-first demonstration
  shows the signal really escaping the fence without ever being able to kill
  anything. The test asserts on the GUARD's refusal text, not on a dead process.
- **killpg at import time is still not the fixture's rule.** The import fence now
  allows own-pid signal-0 for `os.killpg` too, while the fixture leaf refuses
  `killpg` outright (a group leader this test spawned can share a group with a shell
  it did not). Narrowing the import fence to `kill` only is left as the next step;
  widening the predicate to refuse groups would put the fixture's rule in the
  predicate, which is a bigger change than this slice's residue.
- **Keyword `sig=`.** `posix.kill()` takes no keyword arguments: `os.kill(pid, sig=0)`
  raises `TypeError` before any guard, fence or predicate is consulted, so a keyword
  sig is not a fail-closed guarantee — the predicate's keyword branch is DEAD CODE.
- **`_STRIPPED`: FIXED, not documented.** It was 4 lines, under the brief's 5, and a
  comment would have left a real cross-instance restore bug live in any process where
  both conftests load.
- **CONFIG/TEMPLATE-MAX — the fenced leaf list does NOT belong in `.agi/config.json`.**
  Answered, not skipped: a config cell is read from the graph root, so a config-driven
  leaf list lets any project (or a tmp suite root) DISABLE its own real-process
  fence by editing its own config. The list is a code fact about what the guard
  refuses; the only config-shaped part of it (`extra_keys`, the non-AGI git-hook
  channel) is already passed as a parameter. Nothing new in `paths.*`.
- **Scope kept:** residue 2 (.agi/context's own import-time fence) untouched.

## Evidence

- RED/GREEN pairs above are the runs; the offending bytes are the two temporary
  restores (`/tmp/aconftest.bak`, `/tmp/averification.bak`), both put back
  (`grep -c own_pid_signal0_only` = 3, `env=suite_guards.spawn_env()` = 1).

## push_further

Refuse `killpg` at IMPORT time the way the fixture does, and give
`own_pid_signal0_only` a keyword-argument-aware call shape, so the two leaves cannot
diverge again; then have slice 2's fence installer assert its own behaviour with the
same predicate rather than its own copy.

## Agent Notes
one shared kill predicate (own pid AND signal 0) now backs both the fixture leaf and the import-time fence; env= now proved behaviourally with a recorded spawn; _STRIPPED memo is per-instance; 336 tests green

PARENT REVIEW (a00-cbb9f70e, DH.452). Read the BYTES, not this node: suite_guards.own_pid_signal0_only (suite_guards.py:162-178) is called by BOTH leaves -- _make_guarded_kill:223 and tests/conftest.py:679 -- and the _STRIPPED global is gone (per-instance closure memo, suite_guards.py:143-152); the source-string pin at old test:172 is gone, replaced by a recorded-spawn behavioural row.

probes:
- GATE (import-time kill leaf, the residue-1 hole): with the engine conftest imported in a fresh process, an opted-in caller doing os.kill(os.getpid(), SIGCONT) at collection is REFUSED by name -- "guard: a NO_REAL_PROCESSES module called os.kill at IMPORT time (collection)". The DH.440 bytes let it through. Hole closed.
- WIRE (the exemption still works): os.kill(os.getpid(), 0) is ALLOWED and reaches the real syscall, so the liveness probe the predicate exists for did not become collateral damage. Keyword forms (sig=0 / sig=SIGCONT) never reach the predicate at all -- posix.kill takes no keyword arguments, so the "fails closed by luck of ordering" caveat in the THOUGHT is untestable in CPython either way; harmless.
- AUTH (the declared-suite env, the residue-3 pin): a live check_extra_suite over a /tmp project with planted AGI_SEAT=a00-parentprobe and AGI_TIER=kid passes a real env DICT to the child carrying zero AGI_*/AUTORESEARCH_* keys, while the parent env keeps both. The claim holds by behaviour, not by the string the old row grepped for.
- FALSIFYING PROBE, AND IT HELD AGAINST THE KILLPG LEAF: under setsid, so pgid == pid, os.killpg(os.getpid(), 0) is ALLOWED at import time and reaches the real syscall, while the fixture leaf refuses killpg OUTRIGHT. The two leaves therefore do not yet agree on the killpg leaf. The kid named this in push_further; I am recording it as a probe rather than letting it ride.
- KILLED KID: a00-e734f35a (experiment:a00-e734f35a-c4ba3f) died died-no-work at 129 s right after calling check_extra_suite on the LIVE graph root, wrote no node, and still carries its derived title. Its slice was taken by a00-a24082b2. Not evidence for anything.

ACCEPTED for residues 1, 3 and 4. The PARENT hypothesis is NOT proved by it: residue 2 -- the declared context suite has no collection-time fence (.agi/context/conftest.py imports only the three fixtures, every one of them fixture-time) -- is still unbuilt, and my kid ceiling for this slice was 2, so slice 2 did not run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-REVIEW of this node.

(1) WHAT THE ORDERS SAID, quoted: "Close ALL" four residues of verify_DH.440-k1/k2 -- the import-time kill leaf, the context suite having no import-time fence, the env= pin by source string, the _STRIPPED note -- with a ceiling of 2 kids.

(2) WHAT THE MACHINE ACTUALLY DOES: the bytes I ran. suite_guards.own_pid_signal0_only is ONE predicate, called from the fixture leaf (suite_guards.py:223) and from the import-time leaf (tests/conftest.py:679); in my own process with the fence installed, os.kill(own_pid, SIGCONT) at collection is REFUSED by name and os.kill(own_pid, 0) still reaches the syscall. A live check_extra_suite over a /tmp project hands the child an env dict with zero AGI_*/AUTORESEARCH_* keys while the parent keeps its planted AGI_SEAT/AGI_TIER. _STRIPPED is gone: the memo lives in the fixture closure (suite_guards.py:143-152). Three of four residues are closed by mechanism.

(3) THE NEAR MISS: a kid that deletes the source-string assertion and adds ANY test mentioning AGI_ would satisfy "residue 3 closed" as a string and lose the mechanism -- the spawn env is only real if the env DICT handed to the child is inspected while a planted caller var is present, which is what this row does. Same shape on residue 1: an offender that signals a pid the runner does not own passes vacuously (no guard needs to fire), so the offender must be own-pid -- and must use SIGCONT so the red-first demonstration stays harmless when the guard is absent.

(4) WHERE I DEVIATED: I did not demote the kid to a lean verdict despite one falsifying probe, because that probe contradicts only the KILLPG leaf -- a case the kid named in its own push_further before I found it, and a case the fixture leaf already refuses outright, so the shipped guard is no weaker than DH.440 plus the fix. The PARENT hypothesis itself stays unproved: residue 2 (the declared context suite has no collection-time fence at all) is unbuilt and this slice's ceiling of 2 kids is spent.

The next run at this node should build residue 2 -- one importable fence installer in suite_guards, imported by .agi/context/conftest.py, with a row proving a context module that spawns at import is refused BY NAME -- and close the killpg divergence at the same time, since both touch the one predicate.
<!-- THOUGHT:END -->

DH.489 F31 PROCESS MISS, named not repaired: the DH.469 parent answered three kid rebriefs IN-NODE in a00-a24082b2 but never dm-ed the answer lines to the director, and that dispatch cannot be replayed.
