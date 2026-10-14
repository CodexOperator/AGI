---
id: build:extensions-agi-guard-no-session-bus-51-no-session-bus-conf
mint_id: e493b0332b7b4c05b4b709256ef5838e
type: build
parents:
  - goal:g7.16.1.11.7
  - idea:dbus-autolaunch-leak-reaped
next_edges: []
deprecated_on: 2026-10-14
status: deprecated
build_kind: prose
edited_by: belam
link_ref: extensions/agi/guard/deprecated/no-session-bus/51-no-session-bus.conf
location: source_root
model: claude-opus-5-5
role: prime_director
scaffold_hash: 92ea8bd0441920ae
season: 2
title: "extensions/agi/guard/no-session-bus/51-no-session-bus.conf: agi-post@ drop-in setting DBUS_SESSION_BUS_ADDRESS=disabled: so gh keyring lookups never autolaunch a session bus"
town: core
---
<!-- BODY:BEGIN -->
# build:extensions-agi-guard-no-session-bus-51-no-session-bus-conf

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
build_kind: prose added and the stale spawn_check stamps removed (director-general-3 10-10, belam 10:4xZ (A)): `write.py create build` never set build_kind, so the [build] schema (discriminated on build_kind) could not check this node and the spawn gate stamped it spawn_check: unverified; the growth gate (grow.py, goal:g7.16.1.11.8) refuses a new node it cannot verify. The value is level3.build_kind_for(link_ref): the payload suffix of extensions/agi/guard/no-session-bus/51-no-session-bus.conf (.py/.sh/.ts/.js = code, everything else = prose), the rule level3.py applies to every scanned build node. Re-checked with spawn_gate.check_spawn on the backfilled front matter: APPROVED (a clean approval is unstamped, like every other build node).
director-general-2 10-14 (SM 07:1xZ): RETIRED with its piece. belam's 541677b58b (10-11) moved extensions/agi/guard/no-session-bus/ to guard/deprecated/ and left this node on the old path (links.py: broken). Nothing live reads the old path (grep over extensions, src, .geometry: only the node itself); link_ref now names the deprecated path, the node moves to deprecated/build/ (never deleted).
<!-- THOUGHT:END -->
