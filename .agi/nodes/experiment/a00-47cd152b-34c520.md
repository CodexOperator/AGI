---
id: experiment:a00-47cd152b-34c520
mint_id: 806ed87a0bbc43d09948c104777018ff
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-5ad98eb5
evidence_runs:
  - experiment:a00-47cd152b-34c520
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
probes:
  - "parent gate: env -u TMUX -u TMUX_PANE pytest extensions/agi/tests/test_boxkit_probe.py -q --basetemp=/tmp/p1 -> 26 passed, the named test green as shipped"
  - "parent wire (regression, by MUTATION NOT by re-running the kid suite): a scratch pytest plugin (PYTHONPATH=scratch, -p mut_reader, no repo byte touched) re-pointed mem_cap.resolve_tasks_max at the dead cell values.memcap.tasks_max -> FAILED test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal at :553 assert (150, 96, DRIFT) == (150, 150, ok). The new no-override row is load-bearing; the test is not a tautology."
  - "parent wire: the shipped CLI, not a stub -- AGI_TASKS_MAX=96 python3 extensions/agi/boxkit/probe.py --root .agi --install-root /nonexistent --systemctl /bin/false --held-outside-user-mib 1024 prints spawn.tasks_max 150 96 DRIFT and the line DRIFT: spawn.tasks_max"
  - "parent gate: no --held-outside-user-mib -> reserve (derived) UNKNOWN UNKNOWN UNKNOWN, rc=1; the drift-then-unknown exit precedence is untouched"
  - "parent falsifier 2 (grep): the only surviving mentions of values.memcap.tasks_max are a NEGATIVE assertion (test_the_old_cell_is_read_nowhere, which plants cell+1 and requires the resolver to ignore it) and comments; no path reads it as the bound"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 8dda6e1e1b2d580f
season: 2
title: DRIFT re-driven through AGI_TASKS_MAX, dead values.memcap.tasks_max dropped from the probe fixture
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-47cd152b-34c520

## Claim tested
The boxkit probe's `spawn.tasks_max` row and its test agree on the ONE cell this
hypothesis names (`spawn.tasks_max`, read via `mem_cap.resolve_tasks_max`); a
resolver/cell disagreement is still reported as DRIFT, driven through a path
PRODUCTION can take; and no test or probe path reads `values.memcap.tasks_max`
as the tasks bound.

## What I changed (test bytes only, 0 production lines)
`extensions/agi/tests/test_boxkit_probe.py` -- `git diff --numstat` over the
production paths (`extensions/agi/bin/mem_cap.py`,
`extensions/agi/boxkit/probe.py`) is EMPTY: 0 added / 0 removed. The test file
is +8 / -3.

| site | before | after |
|---|---|---|
| fixture :85 | `"values": {"boxkit": ..., "memcap": {"tasks_max": 150}}` | `"values": {"boxkit": ..., "memcap": {}}` -- the DEAD second bound is gone; the empty container stays because `test_the_real_cached_probe_path_reads_a_planted_verdict_...` (line 435) needs `values.memcap` for the probe-cache dir/file cells |
| test :548-551 (new) | -- | `monkeypatch.delenv("AGI_TASKS_MAX", raising=False)` then `assert row["spawn.tasks_max"] == (150, 150, "ok")` -- pins the resolver to the spawn cell |
| test :552-556 (was :550) | `cfg["values"]["memcap"]["tasks_max"] = 96` | `monkeypatch.setenv("AGI_TASKS_MAX", "96")` -- the disagreement now comes through `mem_cap.resolve_tasks_max`'s documented env override, a path production can take |
| test :557-558 | unchanged | `assert table["spawn.tasks_max"] == (150, 96, "DRIFT")` and `assert _run(...) == 1` KEPT -- the DRIFT case is re-driven, not removed |

No new `tasks_max` cell. `.agi/config.json` untouched (the cell is already right).

## Tests (the named one, then the family)
```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_boxkit_probe.py -q --basetemp=/tmp/...
1 failed, 111 passed, 7 skipped in 14.39s          <-- intermediate: KeyError 'memcap' at :435
$ ... test_boxkit_probe.py test_mem_cap_tasks_max.py test_mem_cap_cache_config.py      test_mem_cap_override.py test_mem_cap_probe_cache.py test_heal_mem_cap.py      test_bin_help_smoke.py -q --basetemp=/tmp/ptk-a00-47cd152b-2
147 passed, 7 skipped in 15.46s
$ ... test_boxkit_probe.py -k spawn_rows -q
1 passed, 25 deselected in 1.96s
```

## Probes (negative first; scratch: .agi/sessions/iter-EG.01/a00-47cd152b/probes.py)
1. RED-FIRST (regression of the reader itself). With the test's DRIFT driven
   through the env override alone, the test still passed against a resolver
   re-pointed at the dead cell -- the env made the DRIFT unconditional. Adding
   the no-override `== (150, 150, "ok")` row pins the cell. Re-pointing
   `resolve_tasks_max` back at `values.memcap.tasks_max` (temporarily, restored
   byte-for-byte from a backup) now gives:
   `FAILED ...::test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal`
   `extensions/agi/tests/test_boxkit_probe.py:553: AssertionError` -- 1 failed,
   25 deselected. Restored: 1 passed.
2. WIRE (the disagreement production can take):
   `WIRE   cell: 150 resolver: 96 -> DRIFT` / `WIRE   no env: resolver: 150 -> ok`
3. NEAR-MISS (why the ROW is the artifact, not the assertion): the pre-fix
   dead-cell cfg no longer moves the resolver --
   `NEARMISS resolver on dead-cell cfg: 150 -> row would read (150, 150, 'ok')`
   so a test that merely kept the old `values.memcap.tasks_max = 96` mutation
   would assert `ok` and stay green; nothing would ever be compared.
4. FALLBACK unchanged: `absent spawn.tasks_max -> 96` (fail-closed).
5. AUTH (unchanged behaviour): `probe.py --root .agi --install-root /nonexistent
   --systemctl /bin/false` with no `--held-outside-user-mib` ->
   `reserve (derived)  UNKNOWN  UNKNOWN  UNKNOWN`, rc=1 (rc=3 once no other row
   drifts); the exit precedence `drift -> 1 else unknown -> 3` is untouched.
   With `AGI_TASKS_MAX=96` the live table prints
   `spawn.tasks_max  150  96  DRIFT` and `DRIFT: spawn.tasks_max` -- the same
   disagreement the test asserts, reached through the real CLI.
6. ROW shape in production is unchanged and still literal-free:
   `probe.py` builds it as `("tasks_max", mem_cap.resolve_tasks_max(cfg_all))`
   vs `spawn_cfg.get(cell)`.

## Verdict reading
All three falsifiers are cleared: the named test passes, no probe/test path sets
or reads `values.memcap.tasks_max` as the bound, and the DRIFT case is
re-driven, not removed. Production bytes needed no change -- the red was a
stale test fixture naming a cell this chain already deleted.

caveats: production_lines = 0; the fix is entirely in test bytes, so nothing in
shipped code moved and a future change to `resolve_tasks_max` is now caught by
the new no-override assertion rather than by the DRIFT case alone.
struggles: dropping `values.memcap` outright from the fixture broke a NEIGHBOUR
test at :435 (`KeyError: 'memcap'`) that legitimately uses the probe-cache
cells -- the brief's "if it is then empty, check the row still behaves" was the
real instruction; and the first DRIFT re-drive (env-only) was a FALSE GREEN
under a resolver regression, which is why the extra `(150, 150, "ok")` row was
needed.

<!-- BODY:END -->

## Agent Notes
Re-drove the probe's spawn.tasks_max DRIFT through AGI_TASKS_MAX and dropped the dead values.memcap.tasks_max from the fixture; 0 production lines, 147 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-5ad98eb5, EG.01). (1) WHAT THE INSTRUCTION SAID, quoted from the hypothesis ROUND EG.1 block: the boxkit probe spawn.tasks_max row and its test "agree with the ONE cell this node names ... a resolver/cell disagreement is still reported as DRIFT, driven through a path production can take (e.g. the resolver env override), and no test or probe path reads values.memcap.tasks_max as the tasks bound." (2) WHAT THE MACHINE ACTUALLY DOES: I did not re-run this kid suite as evidence. I mutated the READER in a scratch pytest plugin (PYTHONPATH at the parent scratch, -p mut_reader, zero repo bytes touched) to read the dead cell again, and the named test went RED at :553 (assert (150, 96, DRIFT) == (150, 150, ok)) -- so the no-override row the kid added is load-bearing, not decorative. The shipped CLI with AGI_TASKS_MAX=96 prints "spawn.tasks_max 150 96 DRIFT" plus "DRIFT: spawn.tasks_max": the disagreement is reachable in production, not only in a fixture. (3) THE NEAR MISS this review had to rule out: a green named test would ALSO have been produced by deleting the DRIFT assertions or by seeding the fixture so the resolver happened to disagree -- both satisfy the words and lose the mechanism. The mutation probe is what separates them: it only reddens if the assertion is still bound to the resolver the cell is compared against. (4) DEVIATION: none; I read the bytes (probe.py:271-277, mem_cap.py:61-86, the test file) and I did not re-run the kid own suite as the finding. ACCEPTED as proved, probes attached above.
<!-- THOUGHT:END -->
