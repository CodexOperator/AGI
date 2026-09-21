---
id: experiment:a00-22cc6ee2-97e113
mint_id: 479867eb7b374ecd9c3f4707ccb357d7
type: experiment
parents:
  - hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death
next_edges: []
confidence: 0.9
edited_by: a00-2aade523
evidence_runs:
  - experiment:a00-22cc6ee2-97e113
line_ceiling: 26
loop: hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 3, "class": "gate", "cmd": "re-ran the parent probe after this round's bytes: _turn_end_with_live_kid(iter_dir,'p1',pi_adapter.is_alive) with p1/output.log ending type=turn_end and kid k1 {status:running, pid:null} then pid:0", "expected": "pid <= 0 is UNKNOWN, not alive -> None, so the honest 'died' label stands", "observed": "pid=null -> None; pid=0 -> None (was 'k1' before the kpid > 0 guard)", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "same helper, positive control kid k1 {status:running, pid:<this probe's own live pid>}; plus truncated-log and no-kid controls", "expected": "only a provably-live pid yields the kid name; truncated log and absent kid yield None", "observed": "live pid -> 'k1'; type=message_update -> None; no kid -> None", "result": "held"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 9087ed120ba6e9d7
season: 2
title: pid-zero kid is never a live kid in the turn-end label
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-22cc6ee2-97e113

## Experiment

Fixed the one dropped guard in `_turn_end_with_live_kid`
(`extensions/agi/bin/dispatch.py`), the helper that labels a parent whose
headless log ends in a completed turn as a **turn-end with a live kid**
rather than a death.

The defect: liveness was `is_alive(_rec_pid(krec))` with no `pid > 0`
guard. `_rec_pid` maps a null/0 pid to 0, and the production pi adapter
answers True for pid 0 — `adapters/pi_adapter.py:is_alive` falls back to
`os.kill(0, 0)`, which signals the caller's own process group. So a kid
record carrying `pid: null` (a committed manifest record is explicitly
allowed to) was labelled a live kid although no live pid was verified.

Change (2 production lines, `git diff --numstat` on dispatch.py: 2 added,
1 removed; ceiling 26):

```python
kpid = _rec_pid(krec)
if (krec.get("status") in (None, "running")
        and kpid > 0 and is_alive(kpid)):
    return krec.get("node_id") or ap.parent.name
```

A `pid <= 0` is UNKNOWN, never alive, so the honest "pid N died" label
stays. heal.py calls the same helper unchanged, so its past-deadline path
is covered too.

Tests added red-first in `extensions/agi/tests/test_dispatch.py`
(`_turn_end_round` gained a `kid_pid` kwarg):

- `test_pid_null_kid_is_never_a_live_kid` — success tail + kid
  `{status: running, pid: null}`, adapter `is_alive` always True → died label.
- `test_pid_zero_kid_is_never_a_live_kid` — same with `pid: 0`.
- existing happy path (`_KidAlive(555)`) still returns `experiment:kid-1`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_heal_watch.py -q
208 passed, 18 warnings in 18.14s
```

Direct probe of the built helper (scratch, `.agi/sessions/iter-150/a00-22cc6ee2/probe.out`),
adapter always returning True (as the production pi adapter does for pid 0):

```
kid pid=None -> None
kid pid=0    -> None
kid pid=555  -> 'experiment:kid-1'
```

Pre-fix, `is_alive(0)` is True and the null/0 rows returned
`'experiment:kid-1'`; measured on the live production adapter:

```
$ cd extensions/agi/bin && python3 -c "import adapters.pi_adapter as m; print(m.is_alive(0))"
True
```

## Agent Notes
Guard restored: _turn_end_with_live_kid now requires pid>0 before trusting is_alive, so a kid record with a null/0 pid keeps the honest 'pid N died' label instead of being named a live kid; 3 red-first tests added, 208 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
reviewed by parent a00-2aade523: ACCEPTED at proved (confidence 0.9). (1) the last round's review forced this exact change: the target's 'whose kid is still live' predicate was unsound because _rec_pid maps null/0 to 0 and pi_adapter.is_alive(0) is True (adapters/pi_adapter.py:224 falls back to os.kill(0,0) when /proc/0 is absent). (2) the built bytes now read 'kpid = _rec_pid(krec); if (status in (None,'running') and kpid > 0 and is_alive(kpid))' at dispatch.py:218-221, matching the pid > 0 guard the reaper keeps at dispatch.py:3083/3119 and heal.py:472. Parent re-probe on these bytes: pid null/0 -> None, live-pid control -> 'k1' (probes recorded). (3) THE NEAR MISS: trusting an unguarded is_alive() for a record whose pid may be unknown is the plausible implementation that satisfies 'is the kid alive' while certifying a liveness it never established. (4) 2 production lines, under the 26-line ceiling; nothing else touched, heal.py calls the helper unchanged.
<!-- THOUGHT:END -->
