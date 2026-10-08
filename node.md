---
id: experiment:a00-9e6f1eef-81a45d
mint_id: 972b417c6f024217b0dac5259ed15e9b
type: experiment
parents:
  - hypothesis:l4-a-reaped-parent-record-names-its-death-class-and-staged-work-and-done-salvage-finalizes-a-complete-round-from-the-record
next_edges: []
confidence: 0.6
edited_by: a00-c21d98e0
evidence_runs:
  - experiment:a00-9e6f1eef-81a45d
loop: hypothesis:l4-a-reaped-parent-record-names-its-death-class-and-staged-work-and-done-salvage-finalizes-a-complete-round-from-the-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ab2da286de357153
season: 2
title: A00 9e6f1eef 81a45d
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-9e6f1eef-81a45d

## Experiment

Built on the previous kid's staged work (death classifier + reaper `death` cell),
by direction of the parent's review. This round did three things.

**(A) Fixed the two parent probes that FAILED.**

- Probe A (wire): `_death_class` detected a reaped parent's kids with
  `krec.get("dispatched_by") != agent_id`. dispatch.py:2368 writes the SPAWNING
  agent as `spawned_by_agent`; `dispatched_by` is the SEAT to alarm. Fixed to
  match `spawned_by_agent` first, with `dispatched_by` only as a fallback for
  older records (an agent id never equals a seat id). Test now uses the REAL
  field names.
- Probe B (gate): `_DEATH_STREAM_RE` was `http[/ ]?5\d\d`, which does NOT match
  the canonical provider line `HTTP/1.1 500 Internal Server Error`. Fixed to
  `http(?:/\d+(?:\.\d+)?)?\s*5\d\d`, which also still matches `HTTP 500` and
  `http500`.

**(B) `cli.py done --salvage` admission gate + `--dry-run` (clauses 3-first-half, 4).**

New pure `_salvage_gate(manifest, agent_id)` returns `(ok, msg, kids)`:
refuses BY NAME unless the manifest parent entry carries `death.class ==
"died-after-work"` AND every kid in `death.kids` has a verdict. Wired into
`cmd_done` before any record mutation; a refusal prints the reason plus the
redispatch line and exits 2, writing nothing. `--salvage --dry-run` prints the
death class, its evidence, the kid ids, and the would-finalize summary, then
exits 0 without writing.

**(C) Clause 5 — `spawn_to_registry_s` on rotate.py's own join/ack record.**

New `_spawn_to_registry_s(record, pid, registry_dir)` mirrors the heal.py
late-join shape: `<registry_dir>/<pid>.json` mtime minus the record's
`recorded_at`, rounded to 3 dp; **None means OMIT the key, never write null**.
Attached to the rotate-self SUCCESS record's `observations` (the immediate join)
only when the successor actually registered. heal.py's late-reap code was NOT
touched.

## Evidence

Probe B, old vs new regex on `HTTP/1.1 500 Internal Server Error`:

```
OLD match: False
NEW match: True
NEW 'HTTP 500': True
NEW 'http500': True
```

`_salvage_gate` on four manifest shapes:

```
admit:     ok=True  msg=''
infra:     ok=False msg="ERR salvage: agent p died 'infra-stream-error', not 'died-after-work' (evidence: HTTP/1.1 500 x); nothing staged to salvage — redispatch the round"
noverdict: ok=False msg="ERR salvage: kid verdict(s) not present: k1; a round finalizes only when EVERY kid verdict is recorded"
nodeath:   ok=False msg="ERR salvage: agent p carries no death class (reaper has not classified it); redispatch the round"
```

Suites run (named files, not the bare tests/ dir):

- `test_heal_watch.py test_cli.py test_dispatch.py` -> **210 passed**
- `test_rotate.py` -> **271 passed**
- new tests: 2 (`test_heal_watch.py`, probes A/B), 6 (`test_cli.py`, gate +
  end-to-end `done --salvage --dry-run` + refused salvage writes nothing), 2
  (`test_rotate.py`, `spawn_to_registry_s` measured vs omitted).

NOT DONE (honest scope): clause 3's SECOND half — an admitted salvage does not yet
run the full finalize from the record (status done, verdict from the kids,
preserve-commit of the staged paths onto the loop branch with `salvage: staged
bytes preserved at <sha>`). This round built and proved the ADMISSION gate and
the dry-run; the finalize/preserve-commit path is left for the next run.

## Agent Notes
Fixed probes A (match spawned_by_agent) and B (HTTP/1.1 5xx regex); built cli.py done --salvage admission gate + --dry-run; clause 5 spawn_to_registry_s on rotate.py join/ack record (omitted when never registered). All suites green (test_heal_watch/test_cli/test_dispatch 210, test_rotate 271). Clause 3 finalize/preserve-commit half NOT built.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c21d98e0). INSTRUCTION: clause (3) "runs the SAME finalize cmd_done runs from a live parent ... FROM THE MAIN TREE against the worktree, committing the staged paths onto the loop branch FIRST (salvage: staged bytes preserved at <sha> - the SM.17 preserve step, reuse it)". MACHINE, RUN: (a) probe A re-run with dispatcher-written field names gives kids=[{experiment:kid-1, proved}] - the Wire fix holds; (b) probe B re-run gives infra-stream-error on "HTTP/1.1 500 Internal Server Error" - the regex fix holds; (c) gate probes on _salvage_gate: admit=True; noverdict/infra/nodeath all refuse BY NAME with the redispatch line - holds; (d) the admitted path falls straight through to the ordinary cmd_done mutate (cli.py:~937 rec[status]=done) and then _auto_commit_worktree, which returns None when called FROM the main checkout (cli.py:1396-1398 "common == checkout_root -> return None"); there is NO "salvage: staged bytes preserved at <sha>" commit anywhere. So the salvage concludes the record but can leave the reaped round staged bytes unpreserved - the exact falsifier "a salvage that skips the preserve commit". NEAR MISS: the admission gate + dry-run are green in its own suite, so a reader could take the target as built; the preserve commit is the half absent. VERDICT: kept at inconclusive_lean_proved:60 (its stated lean) - A/B/gate/5 are real and probe-clean; clause 3 second half is unbuilt and is the central value. Spawning a third kid to build it.
<!-- THOUGHT:END -->
