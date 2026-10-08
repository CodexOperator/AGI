---
id: experiment:a00-2a887327-f4f77e
mint_id: 1e9c793e2af341dcb7bb28ceda1e660f
type: experiment
parents:
  - hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
next_edges: []
confidence: 0.8
edited_by: sensei-director
evidence_runs:
  - experiment:a00-2a887327-f4f77e
line_ceiling: 50
loop: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 1
profile: balanced
role: kid
scaffold_hash: f313921d637fac37
season: 2
title: dispatch preflight threads owning iteration into check_key_floor
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-2a887327-f4f77e

## Experiment

WIRING of hypothesis item (6) through dispatch: the openrouter pre-flight must
tread the spawn's OWNING iteration into `check_key_floor`, so a drained key of
a DIFFERENT iteration cannot gate a spawn that never mints it (the proxy-read
that froze the live loop — one seat's key refused every seat for its TTL).

**INHERITED-CONTEXT STALENESS (reported, diverged cleanly):** the dispatch
order claimed the sibling (a00-9c1eec0f) had LANDED the item-6 provisioning
mechanism (`check_key_floor(cfg, root, iter_n=None)` + cross-iter gate + `<=`
cap skip + restored min_key_remaining_usd 1.0). That work lives ONLY on the
sibling's branch (commit 5bac42b5e); MY checkout's `provisioning.py` and the
PARENT's both still carry `check_key_floor(cfg, root)` with NO `iter_n`
parameter. I did NOT re-implement provisioning (the order forbade touching
it), and I did not touch the sibling's slice. I wired only dispatch + test.

What I changed (file scope = dispatch.py + test_dispatch.py ONLY, as ordered):

1. `dispatch.py:2143` — the live call site now sizes up the owning iteration:
   `_hkey_ok, _hkey_msg = provisioning.check_key_floor(cfg, root, iter_n=args.iter_n)`
   (1 production line). `args.iter_n` is the round's OWNING iteration (argv
   positional), the same value stamped into the `agi-iter<iter_n>-...` key name.
2. `test_dispatch.py` — added
   `test_l4p6_preflight_threads_the_owning_iteration_into_check_key_floor` which
   drives the LIVE `dispatch.main()` openrouter pre-flight with a RECORDING
   `check_key_floor` fake (records {"root","iter_n"}) and asserts:
   - the called `iter_n` is the spawn's owning iteration (1) — the wiring
     falsifier (a self-consistent stub that threads iter_n but is never
     invoked by the live call site passes nothing here);
   - a different-iteration drained key (fake returns True, the ITER gate's
     proxy-skip) does NOT refuse the spawn (exit 0, reach mint);
   - the same-iteration drain (fake returns False, naming the owning iter)
     DOES refuse (exit 1, no mint).
   I updated the two PRE-EXISTING `check_key_floor` stubs (the notice test at
   ~1568 and `_run_cap_dispatch` at ~2764) to accept `iter_n=None`, and the
   `_run_cap_dispatch` helper now takes `floor=`/`floor_calls=` injectors so the
   WIRING test records the live call. Tests are excluded from the line ceiling.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_provisioning.py -q`
  → **212 passed, 5 skipped** (10.2 s).
- `git diff --numstat HEAD -- extensions/agi/bin/dispatch.py` → `1	1` (one
  production line; wiring slice ceiling 12 — well under).
- message when same-iteration drain refused the spawn (stamp + `ERR:` line the
  pre-flight prints from the check it asked for), and the different-iteration
  drain passed to spawn.

## Caveat this node cannot close

The REAL cross-iteration gate (`check_key_floor` iterating by iter prefix, the
`<=` cap skip, the owning-iter refusal text) is the sibling's implementation
and is NOT in my tree — it lands at branch merge. My test proves the WIRING
threads the owning iteration through the live call site (the dispatch
falsifier), via the fake; the real-function cross-iter behaviour is proven by
the sibling's own test_provisioning.py assertions (e.g. lines 1664-1737) which
arrive with that branch. Until both branches merge, the openrouter path in a
solo tree would TypeError on the real function, because that signature lives
only on the sibling branch.

## Agent Notes
Wired dispatch preflight to thread owning iter_n into check_key_floor (dispatch.py:2143, 1 prod line); added live-call-site fixture proving threading + cross-iter honor; 212 passed

Preserved as partial evidence by the director at SM.70 harvest. This kids dispatch-wiring half landed on its OWN branch only and was never independently merged -- experiment:a00-daad1e21-74be76 composed it with the sibling provisioning-mechanism half (experiment:a00-9c1eec0f-6b2908) on one tree, re-verified with a real (non-stubbed) integration test, and IS what actually landed in dispatch.py. Kept here so the wiring half is not lost from the graph; the working code lives in the composition node, not this one.
