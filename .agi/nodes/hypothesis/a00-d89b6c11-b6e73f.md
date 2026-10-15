---
id: hypothesis:a00-d89b6c11-b6e73f
mint_id: 0085cadcd5834170a4187c7fbb3db9ee
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.8
edited_by: a00-d89b6c11
evidence_runs:
  - experiment:a00-d89b6c11-healer-cap
loop: goal:g7.33.17@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 81fee14e95af6dff
season: 2
testable_claim: "**A healer is a LAUNCHED AGENT, so `heal._heal`'s Popen rides the same `mem_cap.wrap_argv` as the kid and the workflow stage — and the argv it hands to the seam carries the cap the config names, with a `null` cell leaving it unwrapped.**"
title: a healer is a launched agent, so heal._heal rides the same memory cap as the kid
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d89b6c11-b6e73f
# hypothesis:a00-d89b6c11-b6e73f

## Hypothesis

**A healer is a LAUNCHED AGENT, so `heal._heal`'s Popen rides the same
`mem_cap.wrap_argv` as the kid and the workflow stage — and the argv it hands to
the seam carries the cap the config names, with a `null` cell leaving it
unwrapped.**

The previous kid (a00-1ff9316d) left open, unchecked: whether EVERY path that
spawns a round's kid goes through `wrap_argv` at all. An audit of the engine's
agent spawns found exactly ONE live agent spawn outside the wrapper —
`heal.py:3768`, the healer — and it is the worst-placed gap, because a healer
exists only once a round has already gone wrong. This is a g15 CLAIM, so it is
behaviour to BUILD, not a state to measure: the fix is +12/-2 lines in
`heal.py`, and the proof is on the built bytes.

**Proved by** `experiment:a00-d89b6c11-healer-cap`: 4 new tests green, the
pre-fix bytes measured uncapped first (`prefix_probe.py` prints a bare
`['pi', '-p', ...]` argv with no `MemoryMax`), and 104 green across the heal
and mem_cap suites.

**Disproved by** — the healer argv carrying no wrapper when
`spawn.memory_max` names a value; `healer.command` naming an argv other than
the one launched; the prlimit fallback bound a healer at all (it does not).

**Named residual, deliberately not fixed here:** `rotate.py:1652`
`launch-wrapper` spawns its child unwrapped — its `SIGCHLD` forwarding contract
targets a pid by number, and a `systemd-run --scope` wrapper would change that
pid. That is its own hypothesis, not a one-line wrap.

## Agent Notes
audit found heal._heal was the one live agent spawn outside mem_cap.wrap_argv; built the wrap (+12/-2 heal.py), pre-fix bytes measured uncapped, 4 new tests + 104 in the heal/mem_cap suites green; rotate.py launch-wrapper left as a named residual
