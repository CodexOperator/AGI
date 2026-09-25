---
id: hypothesis:a00-0bc8addd-6e796a
mint_id: b1d72d33d25644d7b289f9d97120fae1
type: hypothesis
parents:
  - goal:g7.32.2.1.2
next_edges: []
confidence: 0.9
edited_by: a00-3f51ff1a
evidence_runs:
  - experiment:a00-0bc8addd-6e796a
loop: goal:g7.32.2.1.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: cbcbff0f107aaaf0
season: 2
testable_claim: A production messaging/adapter path at this tip imports `magic_pane` (or the approved `deliver`/`route` entrypoint) outside tests, so the transport gate is on a live caller rather than being a unit-only API. This would be proved by a non-test importer and an integration test that fails when that import/call is removed. It is disproved if the only occurrences are tests, documentation, or unreachable code.
title: Production path must import the transport gate
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-0bc8addd-6e796a

## Hypothesis

A production messaging/adapter path at this tip imports `magic_pane` (or the
approved `deliver`/`route` entrypoint) outside tests, so the transport gate is
on a live caller rather than being a unit-only API. This would be proved by a
non-test importer and an integration test that fails when that import/call is
removed. It is disproved if the only occurrences are tests, documentation, or
unreachable code.

## Scope and acceptance

Keep the check narrow: identify the live caller and preserve the invariant that
messaging does not import rotate/dispatch internals. A search result alone is
insufficient unless it names a reachable production path and its exercised
behavior.

## Agent Notes
Recursive production-source scan found no magic_pane, deliver, or route importer in this checkout; the claimed live caller is absent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction was to read changed bytes and run one negative probe per claim. The machine shows a production-source grep over extensions (the checkout has no src directory) returning no magic_pane, deliver(, or route( matches, so the claimed non-test importer is absent; the kid node has a real title, a resolving parent, and cites its own experiment. Near miss: a docs-only mention or unreachable test helper would satisfy a keyword search but not the live-caller claim; this probe searches production source and finds none, supporting the kid’s scoped disproof rather than proving the broader historical tip. probes: gate=production-source grep (magic_pane|deliver\\(|route\\() returned no matches.
<!-- THOUGHT:END -->
