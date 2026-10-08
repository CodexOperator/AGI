---
id: hypothesis:a00-50b210d5-b85ee2
mint_id: e2aa07ffbce84d8b882805c2513f5d9a
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.85
edited_by: a00-807958ea
evidence_runs:
  - experiment:a00-50b210d5-stage-seam-cfg
loop: goal:g7.33.17@s2
model: stealth/space-bunny-alpha
probes: "WIRE: threading proven by IDENTITY on the real seam, not by a copy -- with subprocess.Popen, workflow.subprocess.Popen and workflow._REAL_POPEN all set to ONE recording delegate (so workflow.py's `subprocess.Popen is _REAL_POPEN` guard stays true and the real Popen still launches), _run_stage_proc(..., cap=\"6G\", cfg=<the graph config _load_config(root) gives>) handed mem_cap.wrap_argv that EXACT dict object (True), and the argv the seam really launched was ['prlimit','--as=6442450944','--','/bin/true'] with the forced prlimit verdict. GATE: a legacy caller that passes no cfg gets None into wrap_argv and therefore the shipped defaults, byte-unchanged. AUTH: cap=None -- a caller that asked for no cap -- never reaches the cap helper at all and its argv stays ['/bin/true']. NOT PROBED, and the node says so too: this tree's wrap_argv has no TasksMax (that change is on kid 1's branch), so the cell this seam was dropping on THIS tree is the values.memcap probe-cache pair; the stage is process-bounded only once both branches land."
profile: balanced
role: kid
scaffold_hash: ccb668e51502a839
season: 2
testable_claim: "\"workflow.py:1803 is the only live mem_cap.wrap_argv call handed no cfg; threading the caller s own cfg into _run_stage_proc makes the stage seam read the declared values.memcap cells exactly as dispatch.py does, shipped defaults unchanged when the cell is absent -- proven by a recording systemd_run_usable that sees the caller s dict by identity, plus the stage still dying of its cap\""
title: the stage seam is the ONE cap site that drops the cfg it already holds
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-50b210d5-b85ee2 — the stage seam is the ONE cap site that drops the cfg it already holds

## Claim (buildable, so it is a build order)
`workflow.py:1803` is the only live `mem_cap.wrap_argv` call on this tree that is
handed **no** config. `_run_stage_pi` HAS the cfg (it resolved `cap` from it at
`:1860`), so every `values.memcap.*` cell the operator declares is silently
ignored on every workflow stage launch while `dispatch.py` honours the same cells.
Threading that one argument down makes the stage seam obey the declared cells
with the shipped defaults unchanged when they are absent — and touches no
`mem_cap.py` line.

## Correction to the parent brief (measured on these bytes, not argued)
The brief says the stage seam drops `values.memcap.tasks_max`. **`tasks_max` does
not exist on this tree** — no `TasksMax`, no `tasks_max` anywhere under
`extensions/agi/bin`, `extensions/agi/tests` or `.agi/config.json`:

| grep | hits |
|---|---|
| `tasks_max` / `TasksMax` in bin + tests + config.json | 0 |

It lives on kid 1's branch (the `+TasksMax` it added at `dispatch.py:2851`),
which is not on this tree. So the cell the seam drops *today* is the
`values.memcap` **probe-cache** pair (`probe_cache_dir_name` /
`probe_cache_file`) — the only thing `wrap_argv`'s `cfg` parameter is read
for. The shape of the defect is exactly as briefed; the cell's name is not.
Stated here so a later reader does not go looking for a `tasks_max` seam that
was never on these bytes.

## What proves it
| # | probe | red (today) | green (built) |
|---|---|---|---|
| W1 | real stage launch with a cfg: the child's argv is wrapped by the cfg-aware `wrap_argv` (the `systemd_run_usable(cfg)` call records the CALLER's cfg object by identity) | recorded cfg is `None` | recorded cfg **is** the caller's dict |
| W2 | the same launch still dies of the cap (`is_cap_death`) under `prlimit` | green already (regression guard: the fix must not un-wrap) | green |
| W3 | no cfg in hand (legacy caller) -> shipped defaults, `wrap_argv`'s third arg `None` | green | green |
| W4 | byte pin: the seam reads `mem_cap.wrap_argv(cmd, cap, cfg)` | red | green |

## What would disprove it
`wrap_argv`'s `cfg` being read for something other than the probe cache
(it is not — read it, lines 233-245), or `_run_stage_proc` having no cfg on
hand to pass (it does not: `_run_stage_pi` owns it), or the stage launch not
going through `_run_stage_proc` at all (it does, `:1888`).

## Scope
`extensions/agi/bin/workflow.py` ONLY. `mem_cap.py`, `rotate.py`, `heal.py`
are off-limits this round (other branches carry changes to them). The
`resolve_memory_cap` **validation gap** — a garbage `memory_max` /
`seat_memory_max` cell reaches `systemd-run` verbatim and the child DOES NOT
LAUNCH — stays NAMED, not fixed: it lives inside `mem_cap.py`.

## Evidence
`experiment:a00-50b210d5-stage-seam-cfg` (W1-W4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-807958ea, DH.421) -- ACCEPTED; the proved verdict stands on the claim as written.

(1) WHAT THE BRIEF SAID: the last open item on the row -- workflow.py:1803 calls mem_cap.wrap_argv(cmd, cap) with no cfg, so an operator's cell is silently ignored on every workflow stage launch. Fold it in if it costs a couple of lines; do not re-edit mem_cap.py or rotate.py, whose changes ride other branches.

(2) WHAT THE MACHINE DOES: `_run_stage_proc` grew a `cfg` keyword and hands it to wrap_argv; `_run_stage_pi` passes the `cfg` it already holds -- which is the project's own `_load_config(root)` (workflow.py:2371), the same graph object dispatch.py reads -- so the seam stops dropping it. My probe confirms it by IDENTITY, and confirms the two neighbours the change must not disturb: a no-cfg legacy caller still gets the shipped defaults, and cap=None never reaches the cap helper. The node is honest about the tree it stands on: on THIS tree the cell it recovers is the values.memcap probe-cache pair, because kid 1's TasksMax is not merged here. That sentence is the difference between a claim and a story, and it is why I accept it.

(3) THE NEAR MISS, and it nearly caught me: workflow.py wraps ONLY when `subprocess.Popen is _REAL_POPEN`, so the obvious probe -- swap in a fake Popen to capture the argv -- silently SKIPS the very line under test and reports a false failure. My first probe did exactly that and told me the cfg never arrived. The seam is guarded against stubbed children on purpose ("a test that injected the Popen seam owns its own child"), so the correct probe makes the recorder the _REAL_POPEN as well. A parent reading a failing probe here would have demoted a correct change.

(4) WHERE I DEVIATED: nowhere from the loop rules -- no git mutation, no commit, no config cell written by me.

CARRIED FORWARD, NOT FIXED HERE: (a) mem_cap.resolve_memory_cap validates nothing, so a malformed spawn.memory_max (or the new spawn.seat_memory_max) reaches systemd-run verbatim and the launch fails closed with one log line -- a named hole, on another branch's file; (b) kid 1's TasksMax is still only on its own branch: until it lands, three of the four seams are bytes-bounded and none is process-bounded; (c) the stale demote_reason/demoted_from pair beside verdict: proved still appears on the kids whose first done was demoted by the evidence gate.
<!-- THOUGHT:END -->

## Agent Notes
stage seam now threads the caller's cfg into mem_cap.wrap_argv (red 3/green 4, 15 with the cap files, 175 in the workflow suite, 8/-4 in workflow.py); tasks_max does not exist on this tree, the dropped cell is the values.memcap probe-cache pair
