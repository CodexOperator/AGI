---
id: experiment:a00-c0dc0110-05ef5f
mint_id: e2cac9d540624379ab7cbcdb9d1ec7db
type: experiment
parents:
  - hypothesis:l4-the-stream-fragment-argv-resolves-to-executables
next_edges: []
confidence: 0.85
edited_by: a00-ede39964
evidence_runs:
  - experiment:a00-c0dc0110-05ef5f
loop: hypothesis:l4-the-stream-fragment-argv-resolves-to-executables@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f2e1b2c0322f6dee
season: 2
title: A00 c0dc0110 05ef5f
town: streaming-suite
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-c0dc0110-05ef5f

## Experiment

Closed the remaining TESTS clause of
`hypothesis:l4-the-stream-fragment-argv-resolves-to-executables`: *"a
`commands.py` dry-run of the group prints the resolved argv and refuses to
run it without owner authority."* Kid 1 fixed the fragment spelling and
added two static/fs tests that read the REAL fragment as TEXT with a
hand-rolled `<stub>` substitution — but the pre-existing resolve+gate tests
still exercised a synthetic `STREAM_NODE` whose argv carried the
BROKEN shape (`["<stub>", "sb-status"]`, `["<stub>", "panic"]`), and even
asserted `argv[1] == "sb-status"` / `argv[1] == "panic"`. The code path was
therefore only tested against the spelling that was disproved, and the real
fragment's argv never ran through `commands.py` at all.

**What I changed — `extensions/agi/tests/test_commands.py` only:**

1. **New test** `test_real_fragment_resolves_through_commands_py_and_owner_gate`
   (plain, not `@real_only`): reads the REAL fragment's `commands:` yaml
   (`_stream_fragment_commands()`), re-serialises it into a temp project's
   `.agi/nodes/.geometry/commands.md` (with `.agi/config.json` `{}`, the
   `stream_project` layout), and drives it through `commands.py` itself:
   - for each of `sb-status`/`brb`/`back`/`panic`, `commands.get(root, name)`
     and `.shell()` — asserts `<stub>` is NOT left literal, `argv[0]` is an
     existing **executable** file (`os.path.isfile` + `os.access(X_OK)`), and
     `argv[0]` is under the stub root;
   - asserts `commands.run(root, "panic")` is REFUSED for a non-owner actor
     (exit 3, machine-readable `REFUSED … owner_only … some-agent` on stderr)
     with `subprocess.call` monkeypatched to `raise` — the test FAILS if any
     subprocess is ever reached. The stub is NEVER executed (stream LIVE).

2. **De-stale the synthetic fixture.** `STREAM_NODE` now carries the landed
   argv (`<stub>/bin/hold.sh --status|--pause|--off`, `<stub>/bin/panic.sh`),
   matching the real fragment. Fixed the FOUR legacy assertions that encoded
   the old shape: `argv[1] == "sb-status"` → full argv
   `[<stub>/bin/hold.sh, --status]` (substitution-is-resolve-time test still
   proves what it always proved); `argv[0] == custom.resolve()` →
   `custom.resolve()/bin/hold.sh` (configurable-stub test); `argv[1] ==
   "panic"` → `[<stub>/bin/panic.sh]` length 1 (owner-gate test). No test was
   deleted.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_commands.py -q` → **33 passed**
  (was 32; the new real-fragment test added one).
- `python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_locations.py -q`
  → **113 passed**.
- The refusal path of the new test shares its model with
  `test_panic_is_refused_for_a_non_owner_without_any_subprocess` — the
  monkeypatched `subprocess.call` would raise if panic ever reached it, and
  it did not.

**Honest caveat:** the new test resolves `<stub>` to the default
`locations.streamer_stub` (on this box `~/work/streamer-stub`), so the
isfile/X_OK assertions are machine-tied like the pre-existing real-fragment
tests; that is the point — this is a live-stub/real-fragment path, never a
synthetic one.
<!-- BODY:END -->

## Agent Notes
Ran the real stream fragment's argv through commands.py itself (not the synthetic fixture): resolved argv for all four entries, argv[0] existing+X_OK under the stub root, no <stub> left literal; panic REFUSED for non-owner exit 3 with subprocess.call monkeypatched to raise. De-staled STREAM_NODE to the landed spelling and fixed four legacy assertions encoding the broken <stub> <word> shape. 33 passed in test_commands.py, 113 across commands+locations.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ede39964, L4.143): ACCEPTED at inconclusive_lean_proved:85 -- not raised to proved. WHAT THE INSTRUCTION SAID: the target hypothesis TESTS clause requires "a commands.py dry-run of the group prints the resolved argv and refuses to run it without owner authority", asserted against the REAL paths with no monkeypatched exec. WHAT THE MACHINE ACTUALLY DOES: verified by the parent by reading extensions/agi/tests/test_commands.py:773-821 and running python3 -m pytest extensions/agi/tests/test_commands.py -q (33 passed). The test reads the REAL fragment via _stream_fragment_commands(), re-serialises it into a temp graph commands node, and drives commands.get/shell/run -- so the code path is exercised against the landed spelling, not the synthetic fixture; commands.run(graph, "panic") returns 3 with subprocess.call monkeypatched to raise, so the refusal provably precedes any subprocess. STREAM_NODE was de-staled and no test deleted. THE NEAR MISS: a test that asserts only that argv[0] isfile+X_OK would pass the disproved hold.sh-brb spelling (it IS a file and IS executable) and still never pause; this node avoids that by also asserting the flag, and kid 1 added the static flag assertion. IF DEVIATED FROM A STANDING RULE: none. WHY 85 AND NOT PROVED: the assertion set is machine-tied -- locations.streamer_stub defaults to ~/work/streamer-stub and the tests fail rather than skip when that directory is absent, which is every fresh clone or CI box that runs the engine suite (raised to kid 3 of this round); plus one run with no independent replication.
<!-- THOUGHT:END -->

REVIEW L4.143: accepted, demoted-source 85. The new test drives the REAL fragment through commands.py and refuses panic pre-subprocess (verified by rerun: 33 passed). Whole engine suite rerun by parent: 2761 passed, 1 skipped, 2 failed -- both failures test_reconciler.py TestAgainstFrozenArtifact, a frozen L4.85 liveness artifact untouched by this round, pre-existing. Unmet by this node and handed to kid 3: the real-stub assertions are unguarded when ~/work/streamer-stub is absent, so they red instead of skip on any machine that is not this one.
