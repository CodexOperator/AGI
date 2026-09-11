---
id: experiment:a00-fc329e39-146073
mint_id: 40c43c4f219e42ccb1042cd67dc6ca7a
type: experiment
parents:
  - hypothesis:l4-the-stream-fragment-argv-resolves-to-executables
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-fc329e39-146073
scaffold_hash: 228a1e27d2cb1d4e
title: A00 fc329e39 146073
verdict: proved
---
# experiment:a00-fc329e39-146073

## Experiment

**Goal (parent handoff, L4.143):** the real-fragment stream tests landed by
`experiment:a00-c0dc0110-05ef5f` are machine-tied and unguarded — they resolve
`<stub>` through `locations.streamer_stub(graph)` (default `~/work/streamer-stub`)
and assert `os.path.isfile` / `os.access(X_OK)` / `.is_dir()` on those paths. On
a fresh clone / CI / any box without the stub they FAIL (not skip), a real red
suite. Deliverable: one skip guard, applied to the real-fragment tests, proven
to fire, without weakening any assertion or moving to a fake stub.

**What I changed** — `extensions/agi/tests/test_commands.py` only:

1. Added, right after the existing `real_only` marker:
   ```python
   STREAM_STUB_PRESENT = (
       REAL_ROOT is not None
       and locations.streamer_stub(REAL_ROOT).is_dir()
   )
   stub_only = pytest.mark.skipif(
       not STREAM_STUB_PRESENT,
       reason=("streamer stub not installed under locations.streamer_stub "
               "(default ~/work/streamer-stub); the executable-FILE evidence "
               "these assertions check lives on the operator's box, not in a "
               "fresh clone (cf. test_reconciler.py `not present; evidence "
               "is elsewhere`)"))
   ```
   The skip-reason follows the reconciler convention the parent cited
   (`test_reconciler.py:201` `test_frozen_manifest_has_same_stuck_kid`). It
   names the dependency, the default location, and where the evidence lives.
   `@real_only` alone did NOT cover this: it skips only when `REAL_ROOT is
   None` or this project's own commands node is missing — both true on any
   machine, including ones with no stub.

2. Applied `@stub_only` to the three real-fragment tests:
   - `test_stream_fragment_argv_resolves_to_executable_files` (now
     `@real_only @stub_only`)
   - `test_real_fragment_resolves_through_commands_py_and_owner_gate` (this
     one was NOT `@real_only` — it drives a temp `tmp_path` graph, so it was
     the most exposed of the three; got `@stub_only`)
   - `test_stream_panic_is_declared_owner_only_and_never_executed`
     (`@real_only @stub_only`)

   No assertion in any test was weakened. No fake/synthetic stub was
   substituted — when the stub IS present the real-path assertions still run
   unchanged.

   **Honest caveat, recorded because a reader should know:** of the three,
   `test_stream_panic_is_declared_owner_only_and_never_executed` reads only the
   fragment's yaml (`_stream_fragment_commands()` → `FRAGMENT.read_text()`,
   `commands.stream.fragment.md` in the engine repo) and asserts nothing
   against the stub on disk, so its `@stub_only` is a cohort-level skip, not a
   dependency-forced one. Applied anyway because the parent enumerated all
   three as "the three real-fragment tests" and the cohort should read as one
   unit. The other two genuinely need the guard. Flagging this so a future
   reader can drop the redundant marker if they prefer the narrower skip.

**Guide-fires proof (guard is real, not decorative).** Evaluated the guard
expression against a nonexistent stub path without uninstalling anything — a
temp `.agi/config.json` with `locations: {streamer_stub: /nonexistent-stub}`:

```
STREAM_STUB_PRESENT (this box, stub installed): True
skip decision on this box: False
nonexistent stub path resolves to: /tmp/tmpg7rdi7q5/nonexistent-stub
STREAM_STUB_PRESENT (fresh, no stub): False
skip decision (guard fires): True
GUARD FIRES: assert OK
```

So: stub installed → `STREAM_STUB_PRESENT=True`, no skip (real assertions run);
fresh project, no stub → `STREAM_STUB_PRESENT=False`, `skipif` fires → the
three tests skip with a reason naming the missing stub and where evidence lives.

## Evidence

**Targeted suite (this box, stub present — guard must NOT skip):**
```
$ python3 -m pytest extensions/agi/tests/test_commands.py -q
.................................                                        [100%]
33 passed in 1.91s
```

**Whole engine suite** (parent required a repo-suite run after changing code):
```
$ AGI_TIER= AGI_ROLE= python3 -m pytest extensions/agi/tests/ -q
2 failed, 2761 passed, 1 skipped in 231.72s
```
Both failures are `test_reconciler.py::TestAgainstFrozenArtifact` — the frozen
L4.85 worktree/pid-liveness artifact. Identical to the parent's pre-existing
baseline (reported in the L4.143 handoff); unrelated to and untouched by this
round. No new failure introduced.

**On a box with the stub installed, all three real-fragment tests still PASS
(run above, 33 passed).** On a box without it, the two disk-touching tests
skip with an actionable reason instead of failing, per the demonstrated guard
decision.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ede39964, L4.143): ACCEPTED at proved. WHAT THE INSTRUCTION SAID: the parent brief said add ONE skip guard for the external-stub dependency, apply it to the three real-fragment tests, prove the guard fires, and "Do NOT weaken any assertion and do NOT make the tests pass against a fake/synthetic stub". WHAT THE MACHINE ACTUALLY DOES: verified by the parent independently, not by reading the report. extensions/agi/tests/test_commands.py:239-249 defines STREAM_STUB_PRESENT (guarding REAL_ROOT is None) and stub_only; grep shows exactly three applications at :756, :797, :850; python3 -m pytest extensions/agi/tests/test_commands.py -q = 33 passed (unchanged count, stub present, so the guard did not silently absorb a test); the parent re-evaluated the guard expression through locations.py itself -- locations.streamer_stub(engine_root).is_dir() is True as installed and False against a config declaring /nonexistent-stub-xyz -- so skipif fires exactly when the stub is absent. The isfile/X_OK and refusal assertions at :799-821 are unchanged from the reviewed state. THE NEAR MISS: a guard applied with pytest.importorskip or a try/except around the file read would turn a MISSING STUB into a PASSING test, silently deleting the evidence; a guard written as `if not stub.is_dir(): return` would do the same without even a skip. Both satisfy the words "make it not fail" and lose the mechanism -- the reason has to be a mark so the skip is visible in -q output. This node uses skipif with a reason naming the dependency and pointing at the reconciler convention, which is the shape that keeps the absence visible. IF DEVIATED FROM A STANDING RULE: none. Note the node self-reports the one redundancy (the panic-declaration test asserts only yaml, so its stub_only is cohort-level) -- that is honest and does not need a fourth kid.
<!-- THOUGHT:END -->

## Agent Notes
Added STREAM_STUB_PRESENT + stub_only skip guard to test_commands.py and applied to all three real-fragment tests; guard proven to fire via temp config with nonexistent stub; 33 passed targeted, full suite matches baseline (2761 passed, 2 pre-existing reconciler failures)

REVIEW L4.143: accepted proved. Guard verified independently by the parent (three markers at test_commands.py:756/797/850; guard expression evaluated False against a declared /nonexistent-stub-xyz through locations.streamer_stub; 33 passed with the stub installed). Round closes: the fragment argv resolves to executable files reaching their modes, the real fragment is driven through commands.py, panic stays owner_only and is refused before any subprocess, and a machine without the stub now skips with a reason instead of reddening the engine suite.

**2026-09-11T06:04:34Z director review at harvest (sanctuary-director gen XI, L4.143).** The round deviated from the claim's literal argv (`~/bin/sb-status`, `hold.sh brb|back`) with a MEASURED reason and I confirmed it against `/home/ubuntu/work/streamer-stub/bin/hold.sh:21-25` — `case "${0##*/}"` dispatches on the basename (`brb` → `--pause`, `back` → `--off`, default `--status`), so a bare `hold.sh brb` falls to the usage error; the explicit flags `--status/--pause/--off` are the real interface. `python3 -m pytest extensions/agi/tests/test_commands.py -q` → 33 passed; the new tests assert `os.access(argv0, X_OK)` on the REAL resolved paths and the subprocess seam is a never-reached guard, not a bypass. Verdict `proved` stands; merged into seat/sanctuary-director@s2 for merge-up 29.
