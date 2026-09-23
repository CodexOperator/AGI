---
id: experiment:a00-bc68178d-bc0947
mint_id: 92d2b2eea3044262a82d6351e0041b46
type: experiment
parents:
  - hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence
next_edges: []
confidence: 0.9
edited_by: a00-59133696
evidence_runs:
  - experiment:a00-bc68178d-bc0947
loop: hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "live: cli.py wait 990 on a parent-only manifest; then --agent ghost; then a terminal kid row", "expected": "rc=4 named no-kid-rows at once; rc=3 named no-agent; rc=0 on a terminal kid", "observed": "rc=4 stderr no tier:kid row exists for iter 990; rc=3 stderr no manifest agent matches --agent: ghost; rc=0 wait 990: k1=done", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "live dispatch._reap_one(restart_ok=False) on a fixture whose output.log ends in turn_end AND carries Stream error: PARENT-PROBE-EVIDENCE-A; and on a clean turn_end", "expected": "stream-error line survives in death.evidence + turn_end_kid set; clean turn-end keeps evidence==turn-end", "observed": "A: class=infra-stream-error evidence=upstream: Stream error: PARENT-PROBE-EVIDENCE-A turn_end_kid=experiment:kid-1; B: evidence=turn-end", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "live heal.py watch --once on the same two fixtures (dead pid past deadline)", "expected": "stream-error line survives + turn_end_kid; clean turn-end keeps turn-end", "observed": "A: evidence=Upstream error: PARENT-PROBE-EVIDENCE-B turn_end_kid=experiment:kid-1; B: evidence=turn-end", "result": "pass"}
production_lines: 37
profile: balanced
role: kid
scaffold_hash: 7b899ba402ee3ba0
season: 2
title: The turn-end reap keeps stream-error evidence and an empty kid set returns the named code 4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bc68178d-bc0947

## Experiment

Round 2 on `hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence` — both conjuncts IMPLEMENTED, not merely measured (a g15 claim is a build order).

### (A) A turn-end no longer blinds `_death_class` evidence

Before: both turn-end reap sites did `evidence = "turn-end"` unconditionally, discarding the exact provider/stream-error line `_death_class` had already found (`class == infra-stream-error`).

Fix — one shared helper, `_mark_turn_end(death, turn)` in `extensions/agi/bin/dispatch.py` (after `_turn_end_with_live_kid`), applied at BOTH sites:
- `dispatch.py` service lane (`not restart_ok`): `_death = _mark_turn_end(_death, _turn)`.
- `heal.py` watch lane (dead pid past deadline): `"death": _mark_turn_end(_death_class(...), _turn)`; helper imported alongside `_turn_end_with_live_kid`.

Rule: the turn-end fact rides in its own key `turn_end_kid`; `evidence` becomes `"turn-end"` ONLY when `_death_class` left it `None`. So a stream-error line survives in `death.evidence` whenever `class == "infra-stream-error"`, and the ordinary (no-error) turn-end still reads `evidence == "turn-end"` — the pre-existing assertions are unchanged.

Proof: `extensions/agi/tests/test_dispatch.py`:
- `test_stream_error_survives_a_turn_end_at_the_reaper` (new, GREEN on built bytes; asserts the fixture is `class=infra-stream-error`, `"stream error" in evidence`, `evidence != "turn-end"`, `turn_end_kid == "experiment:kid-1"`).
- `test_pre_fix_reaper_blinds_a_stream_error_with_turn_end` (new, RED-ON-PRE-FIX: loads `dispatch.py` bytes from the round base sha `6e6ef7fe5ba06fae83918b430cb646e9e52df4ca` via `git show`, and shows those bytes set `evidence == "turn-end"` on the identical fixture).

`extensions/agi/tests/test_heal_watch.py::test_heal_turn_end_keeps_the_stream_error_evidence` (new) runs the REAL `heal.py watch --once` path and asserts the same on the watcher's record (`death.class == infra-stream-error`, `"h2 protocol error" in death.evidence`, `turn_end_kid == experiment:kid-1`).

### (B) Zero kid rows: decided by MEASUREMENT, then a named non-zero code

Measured the spawn race statically against the real `dispatch.py`, artifact `.agi/sessions/iter-EF.39/a00-bc68178d/probe_manifest_race.py` (output `.out`):
- `_merge_manifest` is CALLED at `dispatch.py:2949` (a disk write — `os.replace(tmp_name, manifest_path)` at `dispatch.py:977`);
- the `if not args.detach:` return branch is at `dispatch.py:2956` — AFTER the write.

So the manifest row reaches disk BEFORE dispatch returns, and the parent runs `dispatch --detach` then `cli.py wait` as two synchronous Bash calls (`brief.py:1930`). A zero-`tier: kid`-row `wait` therefore means NO kid was ever spawned — most loudly because a spawn refused as `unadmitted` lands in `manifest["unadmitted"]`, never in `agents`. No sanctioned race exists; the named non-zero code is correct and LOUDER than the silent 0.

Built: `_WAIT_NO_KID_ROWS = 4` in `cli.py`, returned at once with a stderr line `no tier:kid row exists for iter <N> -- no kid was spawned for this round`. `--agent`-absent stays 3, missing manifest stays 1, genuine timeout stays 2.

Proof: `extensions/agi/tests/test_cli_wait.py`:
- `test_wait_empty_kid_set_returns_a_named_code_at_once` (updated from the old expect-0 test; asserts `rc == _WAIT_NO_KID_ROWS`, `rc not in (0,1,2,3)`, no sleep, stderr names the condition and the iter).
- `test_pre_round_base_sha_returns_zero_on_an_empty_kid_set` (new, RED-ON-PRE-FIX: loads the pre-round tip `6e6ef7fe5ba06f...` cli.py via `git show` and shows it returns 0 on the same fixture).
- `test_pre_fix_base_sha_polls_empty_kid_set_to_timeout` updated to expect 4 from the built bytes.

## Evidence

Test run (touch-only files):

```
$ python3 -m pytest extensions/agi/tests/test_cli_wait.py \
    extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_cli.py -q
348 passed, 4 skipped, 1 failed  (26.16s)
FAILED test_bin_help_smoke.py::test_help_smoke[harness_template.py]
      -- `harness_template.py --help` exits 0 with EMPTY stdout
```

That one failure is UNRELATED to this round (no file this round touches `harness_template.py`); it reproduces on the untouched file, so it is a pre-existing defect, reported and left in place.

Focused run of the three files this round changes:

```
$ python3 -m pytest extensions/agi/tests/test_cli_wait.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_heal_watch.py -q
221 passed, 20 warnings in 13.53s
```

`git diff --numstat` over the production paths:

```
17  4  extensions/agi/bin/cli.py
17  2  extensions/agi/bin/dispatch.py
 3  4  extensions/agi/bin/heal.py
```

37 added / 10 deleted = 27 net production lines — under the 40-line ceiling.

## Probes

- `.agi/sessions/iter-EF.39/a00-bc68178d/probe_manifest_race.py` + `.out` — the spawn-race measurement above (static ordering: `_merge_manifest` call < detach return; `os.replace` present).
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Chose a shared `_mark_turn_end` helper over two inline edits because the two reap sites live in different modules (`dispatch.py`, `heal.py`) and heal ALREADY imports `_death_class`/`_turn_end_with_live_kid` from dispatch — one rule, one place, both sites provably identical. Kept `evidence == "turn-end"` for the no-error case (only fill when `None`) so every pre-existing turn-end assertion stays green while the stream-error line survives. For (B), measured the race first rather than guessing: the probe shows the manifest write precedes the detach return, so zero kid rows is a spawn-refusal fact, not a timing race — a named 4 is the louder, correct answer.
<!-- THOUGHT:END -->

## Agent Notes
Built both conjuncts: shared _mark_turn_end keeps the stream-error line in death.evidence at dispatch.py + heal.py (turn-end fact in turn_end_kid), and cmd_wait returns named _WAIT_NO_KID_ROWS=4 at once on zero tier:kid rows after measuring the spawn race (manifest written dispatch.py:2949 < detach return :2956). Red-on-pre-fix tests load base bytes via git show; focused suite 221 passed, one unrelated pre-existing harness_template.py --help empty-stdout failure reported.

Parent review a00-59133696 EF.39 round 2: ACCEPTED proved. Commit 00993286e implements both conjuncts of the target (turn-end reap keeps the stream-error evidence at dispatch.py and heal.py; cmd_wait returns the named _WAIT_NO_KID_ROWS=4 at once on zero kid rows). Three parent-run probes pass (live CLI rc 4/3/0; dispatch._reap_one; real heal.py watch --once with a clean-turn-end control). Focused suite 221 passed. Residue: test_bin_help_smoke harness_template.py --help empty stdout is pre-existing on base bytes and untouched here.
