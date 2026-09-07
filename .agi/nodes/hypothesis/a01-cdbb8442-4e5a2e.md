---
id: hyp:a01-cdbb8442-4e5a2e
mint_id: 44500109434e4468bc36836b6c9c0ebc
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
season: 1
tags:
  - graph-core
  - R11
testable_claim: "**Claim:** A subscriber plugin can register callbacks for `node_added`, `node_updated`, `node_deleted`, `edge_added`, `edge_deleted` events. When a graph mutation occurs, the bus dispatches the matching event to all registered subscribers within the same load cycle. No subscriber code appears inside graph-core."
thought_session: season
title: A01 cdbb8442 4e5a2e
verdict: pending
---
# graph-core/R11: Graph Change Event Bus

## Hypothesis

Downstream consumers (renderers, embedding updaters, indexers, skill hooks) can react to graph mutations through a pub/sub event bus with zero polling and no graph-core coupling to subscriber implementations.

## Testable Claim

**Claim:** A subscriber plugin can register callbacks for `node_added`, `node_updated`, `node_deleted`, `edge_added`, `edge_deleted` events. When a graph mutation occurs, the bus dispatches the matching event to all registered subscribers within the same load cycle. No subscriber code appears inside graph-core.

**Prove it:**
- A minimal subscriber can be registered with one line of code against the builder or backend contract
- The subscriber receives an event record with: `event_type`, `node_id`, `payload` (before/after for updates)
- Adding a new event type requires zero changes to graph-core, only a schema-registry entry
- Two independent subscribers can co-exist without knowledge of each other

**Disprove it:**
- Any graph mutation requires the subscriber to scan the full graph or re-walk the filesystem to detect changes (polling)
- Subscriber logic lives inside graph-core source files (coupling)

## Acceptance Criteria

- [ ] A `GraphEventBus` class exposes `subscribe(event_type, callback)` and `emit(event_type, payload)` — both require <5 lines of caller code
- [ ] Emitting an event on a graph with zero subscribers is a no-op with no overhead
- [ ] A test registers two subscribers, mutates a node, and asserts both callbacks received the event
- [ ] The bus is a property of the builder object (not the global process state) — two independent builder instances have independent buses
- [ ] Event types are defined in schema-registry, not hard-coded in graph-core

## Out of Scope

- Guaranteed delivery or retry for async consumers (add-on concern, not graph-core)
- Event ordering across concurrent mutations (single-threaded load cycle assumed)
- Persistent event logs (separate storage concern)

## Dependencies

- schema-registry (for event-type registration)
- graph-core R4 (for node mutation hooks)

## Cross-References

- renderers: renderers may subscribe to refresh on node change
- embeddings: embedding indexer may subscribe to update vectors on node change
- environment-indexers: source indexers may subscribe to re-index on schema change

graph-core/R11: event-bus for graph mutation pub/sub — no polling, zero coupling