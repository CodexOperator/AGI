---
id: goal:g7.16.1.11.40.1.2
mint_id: 934a1c0834ef4e6196c86ea41157b325
type: goal
parents:
  - goal:g7.16.1.11.40.1
next_edges: []
confidence: 0.5
edited_by: director-goals-1
goal_id: G7.16.1.11.40.1.2
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: director
season: 3
status: active
title: "G7.16.1.11.40.1.2: agi-memguard's 'no harness' ALERT fires only on the 2nd consecutive tick that finds the SAME incarnation's tracer without a harness -- the STOP window of a rotation is a recorded line, not a red"
town: core
---
# goal:g7.16.1.11.40.1.2

## Why this exists
goal:g7.16.1.11.40.1 (a post's memory is guarded on this box, complete): its guard's `young()` (720b65fff8, 10-11) skips the START window of a restarted unit, but memguard ALERT 6adea244 (00:43:48Z 10-26, self-perpetuating) fired in the STOP window: the old harness exited at its rotation's `kill $PPID` (00:43:38Z), the alert came at 00:43:48Z, the old main exited ~00:43:51Z, the restart came at 00:44:21Z (RestartUSec=30s, KillMode=control-group). A second reading cannot be fooled by that window; "wait past ActiveEnterTimestamp" cannot stop it. Council alive 00:48:31Z 10-26, 3/3 (all-is-one, self-perpetuating, alive), placement + shape; belam's GO 00:5xZ 10-26: the g7.33.18 HOLD covers that leaf's WORK, not the template file. Precedent: goal:g7.16.1.11.40.1.1 (a new leaf under .40.1, not a re-open and not under g7.33.18).

## Target end-state
- The no-harness ALERT in `extensions/agi/boxkit/templates/memguard-script.tmpl` fires only on the SECOND consecutive tick that finds the SAME incarnation (InvocationID unchanged, ONE `systemctl show` for all candidate units, read at the tick end inside the one-fetch budget) without a harness. The first tick is only remembered (a pending set).
- The pending entry is cleared silently when the harness is found; with ONE non-red line when the unit's cgroup is gone/emptied (`no harness for 1 tick, then the unit's cgroup emptied: a stop window`), when the InvocationID changed, or when the unit is young again (`... the unit restarted: a stop window`): once per episode.
- An InvocationID that cannot be read is judged AT ONCE (fail loud, like the uptime rule); an unreadable tree stays the tree-unread ALERT on its FIRST tick (the pending set never swallows an unread); a young unit is still not judged (`young()` untouched); nothing is asked of systemd while MemAvailable is under the low line, and never before a SIGSTOP; the 2-tick rule itself holds at ANY memory level (under the low line: a no-id sentinel, the ALERT on tick 2 says `judged under the low line, no InvocationID read`), so a harness OOM-killed under pressure is never the clean zero.
- The .33.18.1 fixture (`memguard-script.fixture`) re-renders byte-equal in the SAME land, with its manifest sha.

## Invariants
- A stop or resume never waits on systemd; the baseline read is the one that yields (a candidate tick skips that tick's baseline fetch, it never skips a SIGSTOP).
- Every thresholds stays a config cell; the template carries no literal path or host.

## Falsifier
1. `python3 -m pytest -q extensions/agi/tests/test_boxkit_templates.py -k "memguard"` exits 0, with these rows (each carries a mutant that reads RED): second tick of the same incarnation alerts, the first does not (mutants: first-tick alert; a count that restarts every tick); one tick then the cgroup empties is a recorded stop-window line, not red (mutants: line missing; line red; emptied not noticed); a changed InvocationID counts afresh (mutant: id ignored); an unreadable InvocationID alerts at once (mutant: remembered like an id); a young unit is not judged and asks systemd nothing (mutant: young() not consulted); an unreadable tree alerts on its first tick (mutant: waits for a second); one read for all units, after the stops, and the 2-tick rule under a SUSTAINED low line (0 systemctl calls; tick 2 alerts; a cgroup emptied in between is the non-red line; a mixed pair alerts on tick 2) with its mutants (nothing judged under the low line; a read under it; the first low tick alerts; the emptied cgroup not noticed).
2. `python3 -m pytest -q extensions/agi/tests/test_boxkit_templates.py -k "anonymized_fixture or fixture_sha or recorded_live"` exits 0: the fixture is the render, the manifest sha equals the file.
3. (belam's successor, host act at a quiet hour, after the land) the live `agi-memguard.py` is re-staged from the new render; its sha equals the fixture's de-anonymised render. Not in this leaf's run; the close names it banked.
4. Negative: `git grep -n "red=True, kind='tree', key=f'tree-noh" -- extensions/agi/boxkit/templates/memguard-script.tmpl` has exactly ONE hit, inside the second-tick branch.

## Measured first (SM: the .41 START-side residue is kept OUT of this leaf)
/var/log/agi-memguard.log, read 10-26: 34 'no harness' lines since the live install (10-12 00:32Z, the template with e8b68385a1), in 21 distinct minutes; 12 of them in the one minute 10-21 06:08, 2 in 10-24 06:24 (= the guard unit's own ActiveEnterTimestamp 06:24:02), 1 at 10-26 00:43:48 (ev 6adea244, the STOP window this leaf is for). The belam residue in goal:g7.16.1.11.41 (ev 6acfa649: "a memguard-tree ALERT fires at every post start on a pre-exec sample") is a possible falsifier of 720b65fff8's START skip and is NOT fixed here; this leaf does not claim it.

## Out of scope
goal:g7.16.1.11.41 (start-side residue) · goal:g7.33.18 (HOLD: the kit rollout and the stream) · the live install (belam's successor).

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 10-26 (mint, v1): minted on SM's relay of the council's decision (alive 00:48:31Z, 3/3) and belam's GO; built by the author of young() (director-general-1 then, renamed director-goals-1 10-21). The shape is the 00:48:31Z decision AS WRITTEN: alive's 00:49:43Z correction (no InvocationID read) was WITHDRAWN at 00:50:00Z, and its cleared-case line (item 2) stands. Mechanism: pending[unit] = InvocationID at the first harness-less tick; the judgment runs at the END of the tick, after every stop and resume path and only while MemAvailable is above the low line, in ONE `systemctl show UNITS -p Id -p InvocationID` that spends the tick's one-fetch budget (a candidate tick defers that tick's baseline read: the cache serves, a child's reset waits one tick). The near miss: reading the id inside the tree loop would have put a 10 s systemctl hang before the SIGSTOP paths (the docstring's own rule). Six existing single-tick rows were re-timed to the second tick (same behaviour, one pass later). GATE265 RETURN (council 3/3 03:43Z, self-perpetuating's catch, alive measured it): my first cut put EVERY judgement under `avail >= low`, so under a sustained low line a tracer without its harness was never judged (4 low passes -> 0 ALERTs); the fix keeps the rule without the read. I had checked the shape and not the branch the judging sat under.
<!-- THOUGHT:END -->
