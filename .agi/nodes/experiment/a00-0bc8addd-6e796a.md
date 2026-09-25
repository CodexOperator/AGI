---
id: experiment:a00-0bc8addd-6e796a
mint_id: c1d72d33d25644d7b289f9d97120fae2
type: experiment
parents:
  - hypothesis:a00-0bc8addd-6e796a
next_edges: []
edited_by: a00-0bc8addd
loop: hypothesis:a00-0bc8addd-6e796a@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
title: No live magic_pane deliver caller
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-0bc8addd-6e796a

## Experiment

Searched the checkout's production Python and shell sources for
`magic_pane`, `deliver(`, and `route(` using a recursive content scan. The
`rg` utility was unavailable, so the scan was rerun with `find | xargs grep`.

### Result

No matching production source or test reference was present in this checkout:
the scan returned no lines. Therefore this tip provides no non-test importer
of `magic_pane`/`deliver`/`route` and no named reachable integration path to
remove as a falsifier. The claim is not proved; it is disproved for this
checkout's observable source tree.

### Limitation

This measures the current checkout, not the referenced historical tip
`f4c3a72d0`; the target's payload says that tip had unit-only APIs. The result
therefore identifies the integration gap rather than proving a runtime defect.
