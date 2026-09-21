---
id: hypothesis:a00-652a7e70-1adcde
mint_id: b1bf250ead2e41bf99d28146a0a26c68
type: hypothesis
parents:
  - goal:g4.3
confidence: 0.5
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: A00 652a7e70 1adcde
verdict: pending
wired_at: 1788204776
wired_from: a00-652a7e70
---

# hypothesis:a00-652a7e70-1adcde

## Hypothesis

**Claim:** the CC dispatcher's cheap mode (spawn N kids directly, one node each,
`kid_model` per kid) can be built as a thin adapter on top of the *existing*
pi path — reusing `dispatch.py`'s target selection, the spawn gate, the
evidence gate, `post_wire` and the node format unchanged — such that no gate
acquires a CC-specific copy. The runtime is resolved by one flag/config lookup
(`agent_dispatch` vs `cc_dispatch`) at the point of process spawn, and nowhere
else.

**Testable shape:** a `--max-iters 1` run with `runtime: claude-code` set in
`.agi/config.json` dispatches a kid through the shared gates and produces a
node indistinguishable in format from a pi-dispatched one, where the only
code difference is the spawn call (`claude -p` with the same node-fill prompt
that `agent-prompt.md` carries, replacing the pi process invocation).

**Proves it:** one iteration completes end-to-end on the CC runtime; the node
it writes is wired by the same `post_wire` call; `diff` of the gate-invocation
path shows zero new branches beyond the single runtime lookup.

**Disproves it:** any gate needing runtime-specific logic (e.g. CC's question
channel, model-tier enforcement, or output parsing diverging enough that
`heal.py` cannot close the node), or the CC kid failing to write nodes because
some shared assumption (cwd, file paths, prompt format) is pi-bound. H9's
asymmetry — the kid→parent question channel exists only for CC — is the
 likeliest place it breaks; if the pi path needs its own channel to reach
parity, that is a real fork, and the claim fails in its strong form.

**Scope:** mode 1 only (direct kids). Mode 2 (parents spawning kids) is a
separate hypothesis — layering it here would make one node carry two
arguments.