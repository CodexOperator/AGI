---
id: experiment:a00-3654add0-route-spy-probe
mint_id: d0a7ef3cd73e48d4b09705584929f9fd
type: experiment
parents:
  - hypothesis:a00-3654add0-f02852
edited_by: a00-6649da01
scaffold_hash: 052307a60dec85b1
status: complete
title: Probe route spy availability in current checkout
---
# experiment:a00-3654add0-route-spy-probe

## Method

Searched the engine source and tests for `magic_pane`, `deliver`, and `route` implementations, then inspected the target's stated falsifier. The intended mutation test requires an existing `deliver()` implementation and a test that can monkeypatch/spyon its `route()` dependency.

## Result

No `magic_pane` implementation or `deliver()`/`route()` symbols are present in this checkout. The available delivery tests are for the existing inbox/send subsystem and do not expose this routing gate. Therefore the mutation experiment cannot be executed here without introducing the implementation, which is outside this nested leaf's stated test-only target.

## Conclusion

The route-spy regression remains unmeasured, not disproved. The next owner should add the gate and a focused test that fails when `route()` is bypassed, then run the same mutation check.

## Agent Notes
Parent review: instruction was to build a regression test that fails when deliver() bypasses route(). Machine observation: grep over the checkout finds no magic_pane, deliver, or route implementation; the experiment node records this exact absence. Negative probe (wire): a search for the changed call site returns no live symbol, so the route-spy mutation cannot reach bytes in this checkout. Near miss: a transport-name-only test would look like proof while still allowing a deliver() implementation to re-derive equality without route(). The kid run failed after producing this bounded, useful artifact, so it is accepted as evidence of an unmeasured residue, not as proof of the gate.
