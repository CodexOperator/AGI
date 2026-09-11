---
id: hypothesis:l4-a-spawn-arms-its-own-watch
mint_id: da7dbf07aaaf4a5cacb7081cd2d18a57
type: hypothesis
parents:
  - goal:g4.7
next_edges: []
edited_by: belam-S1-L4-VII
scaffold_hash: c7ad0f2de6715270
season: 2
testable_claim: "OWNER 2026-09-11 01:5xZ (verbatim in doc:l4-owner-decisions): \"also the directors still have to re-arm monitors manually. Could not those be automated as well on parent spawn. Helper forgot about his spawns again and nothing reminded him.\" CLAIM: a spawn ARMS ITS OWN WATCH at dispatch, and the wake comes from OUTSIDE the seat, so no seat ever re-arms an in-session Monitor or remembers a spawn by itself. (1) dispatch.py, at every spawn it stamps dispatched_by (L4.113), registers the watch with the persistent watcher (heal.py watch, L4.116) as data on the manifest/lease: no seat action, no flag. (2) HEARTBEAT: while any spawn of a seat is live the watcher sends that seat ONE dm every watch.heartbeat_minutes (config in .agi/config.json agent_dispatch, default 15) listing live spawns: id, iteration, tier, age, key expiry; nothing when none are live. (3) UNHARVESTED REMINDER: a completion dm that the seat has not read (the inbox `# read up to here` marker is behind it) after watch.unharvested_minutes (default 20) is re-sent ONCE as `unharvested:` with the same facts; then every heartbeat names it until read. (4) ROTATION: rotate-self and the seat brief template list the seat live and unharvested spawns from the manifests (dispatched_by == seat) so a successor inherits them without a hand step. (5) The seat-side Monitor tool becomes optional: the brief tells seats NOT to arm one for spawns. (6) FIXTURES ONLY: fake clock, fake inbox, fake manifests; no real pane, unit or process in tests; the transport is send.send, whose nudge is fixed by hypothesis:l4-a-nudge-is-a-wake-token-not-a-message (SERIAL behind it and behind the L4.116 unit install). FALSIFIERS: a spawn a seat must remember by itself; a heartbeat that fires with no live spawn or off cadence; an unharvested completion older than the window with no reminder; a successor brief that omits a live spawn; a test that reaches a real resource. SCOPE: dispatch.py (registration), heal.py (heartbeat + reminder in the watch loop), rotate.py (successor brief block), .agi/config.json knobs, tests beside them in suite order."
thought_session: belam-S1-L4-VII
title: A spawn arms its own watch — heartbeat and unharvested reminders come from the persistent watcher, never from a seat re-arming a monitor
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-spawn-arms-its-own-watch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
