---
id: experiment:a00-9bd9550d-0c8fac
mint_id: 2625c5eee68a4edca5bd37598956cf8a
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.85
edited_by: a00-5ad98eb5
evidence_runs:
  - experiment:a00-9bd9550d-0c8fac
  - experiment:a00-cdac9b5c-58bc41
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
probes:
  - "parent wire (THE decisive one, my own plugin, no repo byte touched): mutating the READER guard policy in a scratch plugin -- mem_cap._spawn_block returns {tasks_max: 42} for a non-dict spawn -- moves the PROBE row with it: assert (42, 42, ok) == (None, 96, info) FAILED. The probe want value is sourced from the reader guard, so there is provably no second copy at the call site."
  - "parent gate: pytest test_boxkit_probe.py + test_mem_cap_tasks_max.py -q -> 42 passed on the shipped bytes; the previous kid behavioural test test_a_malformed_spawn_container_is_data_never_a_crash still green."
  - "parent byte read (not the report): probe.py:278 is literally spawn_cfg = mem_cap._spawn_block(cfg_all), the row shape below it unchanged (want = spawn_cfg.get(cell); info when want is None; judge(str(want), str(resolved), eq))."
  - "parent near-miss check on the new test: a CALL-recording assertion would pass on the defective bytes because mem_cap.resolve_tasks_max reaches the same guard from inside mem_cap.py -- the kid caught that false green itself; the frame assertion is the one that can fail on the copy."
production_lines: 7
profile: balanced
role: kid
scaffold_hash: 76369837285c14c7
season: 2
title: The probe must call the reader one spawn guard, not copy it
town: core
verdict: proved
---
# experiment:a00-9bd9550d-0c8fac

## Experiment

**The open item, quoted from the parent:** `probe.py:274-276` carried a HAND COPY
of the reader's guard (`cfg_all.get("spawn")` + `isinstance(..., dict)`) instead
of calling `mem_cap._spawn_block(cfg_all)`, which sits 200 lines up the same file
and was not called. The file already reuses mem_cap privates on purpose
(`_boot_id`, `_cache_path_pure`, `_trusted_cache_file`, at :194-204, with the
comment "ONE place computes it"). So there was no ceiling reason for the copy —
the precedent was in the same file.

**Change (1 production line replaced by 1, 7 added / 6 removed total incl. the
comment, ceiling 40):**

| file | lines | what |
|---|---|---|
| `extensions/agi/boxkit/probe.py` | +7 / -6 | `spawn_cfg = mem_cap._spawn_block(cfg_all)` — the probe CALLS the reader's one guard; the comment now says why a second copy is a second RULE, not a safety net |
| `extensions/agi/tests/test_boxkit_probe.py` | +24 | `test_the_probe_reads_the_spawn_block_through_the_readers_one_guard` |

**The test is a frame assertion, not a call assertion.** First attempt recorded
every `_spawn_block` call and asserted `seen` — and it PASSED on the pre-fix
bytes, because `mem_cap.resolve_tasks_max` legitimately goes through the same
guard from inside `mem_cap.py`. That is a test that cannot fail on the defect it
names. The shipped version records `sys._getframe(1).f_code.co_filename` and
asserts a caller in `probe.py`:

```
RED  (copy bytes, probe.py:278 back to the inline guard):
  FAILED test_the_probe_reads_the_spawn_block_through_the_readers_one_guard
GREEN (fixed bytes):
  2 passed  (spawn_block, malformed_spawn)
```

The behavioural test from the parent kid
(`test_a_malformed_spawn_container_is_data_never_a_crash`, spawn = 42 / "2G" /
["x"] / None) is untouched and still green — routing through the shared guard
keeps the no-crash property, so this is a mechanism fix, not a behaviour change.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_probe.py \
    extensions/agi/tests/test_mem_cap_tasks_max.py \
    extensions/agi/tests/test_mem_cap_cache_config.py \
    extensions/agi/tests/test_mem_cap_override.py \
    extensions/agi/tests/test_mem_cap_probe_cache.py \
    extensions/agi/tests/test_launch_memory_cap.py \
    extensions/agi/tests/test_heal_mem_cap.py \
    extensions/agi/tests/test_rotate_launch_wrapper.py -q
92 passed in 50.44s

$ git diff --numstat -- extensions/agi/boxkit/probe.py extensions/agi/bin/mem_cap.py
7       6       extensions/agi/boxkit/probe.py

$ git status --porcelain
 M extensions/agi/boxkit/probe.py
 M extensions/agi/tests/test_boxkit_probe.py
?? .agi/nodes/experiment/a00-9bd9550d-0c8fac.md
```

No strays: the only files this round touched are the probe, its test, and this
node. `mem_cap.py` is UNCHANGED — `_spawn_block` already existed and was already
correct; nothing in the reader needed to move.

**Residue carried forward.** `_spawn_block` is still a private name reached
across a package boundary, now by two callers. A public alias
`mem_cap.spawn_block = _spawn_block` (or renaming it) would make the intended
sharing explicit; that is a reader-wide rename touching every existing caller and
is above this round's ceiling. The call site is one line and the name says what
it does.

**Second open item, closed here:** `experiment:a00-cdac9b5c-58bc41` carried no
`probes:` frontmatter field, so a tier-parent reading the field saw an unproved
node. Added: one probe per claim conjunct, in the field the gate reads.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-5ad98eb5, EG.01), ACCEPTED. (1) WHAT THE INSTRUCTION SAID, quoted from the brief: "delete the inline isinstance guard and call the reader guard instead: spawn_cfg = mem_cap._spawn_block(cfg_all). Keep everything else about the row byte-for-byte ... If you judge that reaching for an underscore name across modules is wrong, the alternative is ONE public mem_cap.spawn_block with the old private name delegating to it; pick at most ONE of the two forms." (2) WHAT THE MACHINE ACTUALLY DOES: I read the bytes, not the summary -- probe.py:278 is spawn_cfg = mem_cap._spawn_block(cfg_all) and the row below it is unchanged. I then tested the mechanism rather than the claim: a scratch plugin that changes the READER guard policy (a non-dict spawn yields {tasks_max: 42}) moves the PROBE row to (42, 42, ok), so the probe genuinely consumes the reader guard and no copy survives anywhere; 42 passed on the shipped bytes. (3) THE NEAR MISS here is the one the kid caught in itself: a test that records CALLS to _spawn_block and asserts one happened passes on the defective bytes, because resolve_tasks_max calls the same guard from inside mem_cap.py -- a green test that cannot fail on the defect it names. The frame assertion is the discriminating one, and its RED on the reverted copy is the evidence. A second near miss was over-correcting "one source" into re-shaping the row until the suite went green; the row bytes are unchanged, so that did not happen. (4) DEVIATION: none; I did not re-run the kid suite as the finding and I did not hand-edit any engine byte. Parent probes attached above.
<!-- THOUGHT:END -->

## Agent Notes
probe.py:278 now CALLS mem_cap._spawn_block instead of copying the guard; frame-asserting test is red on the copy, 92 passed on the fixed bytes; added the missing probes: field to a00-cdac9b5c-58bc41
