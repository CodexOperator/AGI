---
id: command:commands
mint_id: b7e4f0a91c2d4e8fa63b5d7c8e1f2a04
type: command
parents:
  - goal:g1.10
commands:
  smoke:
    argv:
      - bash
      - <engine>/extensions/agi/driver.sh
      - "--smoke"
      - "--max-iters"
      - 1
    about: snapshot + render + metrics, no dispatch — verify the node count did not drop
    workflow: verify
  tests:
    argv:
      - python3
      - "-m"
      - pytest
      - <engine>/extensions/agi/tests/
      - "-q"
    about: the engine's own suite
    workflow: verify
  goals-check:
    argv:
      - python3
      - <engine>/extensions/agi/bin/snapshot-goals.py
      - "--render"
      - "--check"
    about: GOALS.md and the goal nodes are byte-identical inverses
    workflow: verify
  viewport-verify:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - "--verify"
    about: goal:g2.19 — one render, two readers
    workflow: verify
  grid-commit:
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - commit
      - "--all"
    about: version every changed node and its payload
    workflow: verify
  links:
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - links
    about: every node's link resolves; broken_links must be 0
    workflow: read
  schema:
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - schema
    about: goal:s31 — which nodes violate their type's required list (dry)
    workflow: read
  budget:
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - status
    about: goal:g4.8 — live agents against the tree-wide bound
    workflow: read
  credentials:
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - status
    about: goal:g1.11 — whether per-spawn keys are being issued
    workflow: read
  secrets:
    argv:
      - python3
      - <engine>/extensions/agi/bin/envfile.py
      - "--check"
    about: goal:g1.8 — required keys present, forbidden keys absent
    workflow: read
  crons:
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - show
    about: the crontab the graph declares
    workflow: read
  write-guard:
    argv:
      - python3
      - <engine>/extensions/agi/bin/write_guard.py
      - check
    about: goal:g4.18 — unsanctioned node writes; silent is healthy
    workflow: verify
  dispatch-help:
    argv:
      - python3
      - <engine>/extensions/agi/bin/dispatch.py
      - "--help"
    about: dispatch --help exits 0 — agents can be spawned
    workflow: verify
  verify:
    argv:
      - python3
      - <engine>/extensions/agi/bin/verification.py
    about: the ONE rotation check — levels quick|rotation|full, --suite opt-in (hypothesis:l4-unified-verification)
    workflow: verify
  verify-suite:
    argv:
      - python3
      - <engine>/extensions/agi/bin/verification.py
      - "--suite"
    about: the PRIME's rotation check — the rotation level plus the engine suite; the suite window is granted, one runner at a time
    workflow: verify
  view:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - "--live"
    about: the live graph, agents drawn as spiders where they are working
    workflow: see
  view-llm:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - "--emit"
      - llm
    about: goal:g2.19 — exactly what a kid is handed, from the same frame stream
    workflow: see
  view-both:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - "--emit"
      - both
    about: human and llm views side by side, from ONE stream
    workflow: see
  write:
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
    about: goal:g4.18 — named node operations; a hand edit becomes an engine action
    workflow: see
  session-complete:
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - session-complete
      - <iter_n>
      - "--dry-run"
    about: hypothesis:l4-session-dirs-come-home-when-the-round-is-done — bring a finished round's session dir home from a worktree, COPY-THEN-VERIFY; start every inspection with --dry-run
    workflow: read
  mesh-local-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - local-town
    about: "a mesh peer: model bytes and the town download queue live there; append a command to run it remotely."
    workflow: mesh
  mesh-core-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - core-town
    about: "a mesh peer: the Prime, the masters, pi processes; a loopback from that box itself."
    workflow: mesh
  mesh-encryption-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - encryption-town
    about: "the secrets hub: the only box with Doppler; CPU-only rounds go here first (agi-run = nice 19 / 4 threads / 4G). Never copy a secret off it."
    workflow: mesh
  mesh-silicon-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - silicon-town
    about: "the human gate: an ephemeral VM, up only while the owner laptop is; the only writer of box truth. Reachable = the owner is present."
    workflow: mesh
  mesh-gw:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - gw
    about: "the overlay hub (gw): owner ops only (lock or unlock a farm box); agents have no business here -- listed so a cold session knows the name it sees in the mesh files."
    workflow: mesh
edited_by: director-engine
excluded:
  write.py:patch:
    cli: write.py
    verb: patch
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - patch -
    reason: reads a unified diff on stdin (fail-closed) -- not expressible as argv
    side_effects: graph-write
    proposable: false
  write.py:body_patch:
    cli: write.py
    verb: body_patch
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - body_patch -
    reason: reads a diff on stdin onto the node BODY -- not expressible as argv
    side_effects: graph-write
    proposable: false
  node_writer.py::
    cli: node_writer.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/node_writer.py
    args: []
    reason: library module with no main or argparse; imported by other CLIs, not a choice
    side_effects: graph-write
    proposable: false
  metrics.py::
    cli: metrics.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/metrics.py
    args: []
    reason: manual argv, no argparse parser; loop metrics renderer, not a choice
    side_effects: read
    proposable: false
  dispatch.py::
    cli: dispatch.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/dispatch.py
      - <project_root>
      - <iter_n>
    reason: spawns paid model agents; operator-only, never proposed
    side_effects: spawn
    proposable: false
  grid.py:checkout:
    cli: grid.py
    verb: checkout
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - checkout
      - <node_ids...>
    reason: "destructive: overwrites the working tree (retired, never run)"
    side_effects: destructive
    proposable: false
  grid.py:migrate-mint-refs:
    cli: grid.py
    verb: migrate-mint-refs
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - migrate-mint-refs
    reason: "destructive: rewrites grid refs (--write)"
    side_effects: destructive
    proposable: false
  grid.py:migrate-refs:
    cli: grid.py
    verb: migrate-refs
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - migrate-refs
    reason: "destructive: rewrites grid refs (--write)"
    side_effects: destructive
    proposable: false
  grid.py:migrate-trunk:
    cli: grid.py
    verb: migrate-trunk
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - migrate-trunk
    reason: "destructive: rewrites grid refs (--write)"
    side_effects: destructive
    proposable: false
  grid.py:sync:
    cli: grid.py
    verb: sync
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - sync
    reason: "network: pushes refs to a remote"
    side_effects: network
    proposable: false
  provisioning.py:reap:
    cli: provisioning.py
    verb: reap
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - reap
    reason: "destructive: deletes keys (--yes)"
    side_effects: destructive
    proposable: false
  rotate.py:ack:
    cli: rotate.py
    verb: ack
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - ack
      - <answer>
    reason: acknowledges a seat handoff; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:alarms:
    cli: rotate.py
    verb: alarms
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - alarms
    reason: seat alarm watcher; long-running, never-run
    side_effects: comms
    proposable: false
  rotate.py:closeout:
    cli: rotate.py
    verb: closeout
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - closeout
    reason: closes out a seat; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:complete:
    cli: rotate.py
    verb: complete
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - complete
    reason: completes a worktree round; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:first-decision:
    cli: rotate.py
    verb: first-decision
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - first-decision
    reason: records a seat first decision; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:launch-wrapper:
    cli: rotate.py
    verb: launch-wrapper
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - launch-wrapper
      - <child>
    reason: launches a seat wrapper; never-run
    side_effects: spawn
    proposable: false
  rotate.py:loop:
    cli: rotate.py
    verb: loop
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - loop
    reason: super-ralph rotation loop; never-run
    side_effects: spawn
    proposable: false
  rotate.py:merge-up:
    cli: rotate.py
    verb: merge-up
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - merge-up
    reason: merges a post up the tree; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:migrate:
    cli: rotate.py
    verb: migrate
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - migrate
    reason: "destructive: migrates posts/refs"
    side_effects: destructive
    proposable: false
  rotate.py:prepare:
    cli: rotate.py
    verb: prepare
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - prepare
    reason: arms a rotation; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:rename-post:
    cli: rotate.py
    verb: rename-post
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - rename-post
      - <old_name>
      - <new_name>
    reason: renames a post; operator-only
    side_effects: graph-write
    proposable: false
  rotate.py:rotate:
    cli: rotate.py
    verb: rotate
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - rotate
    reason: rotates a live seat; never-run by a proposer
    side_effects: spawn
    proposable: false
  rotate.py:rotate-self:
    cli: rotate.py
    verb: rotate-self
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - rotate-self
    reason: self-rotation; never-run by a proposer
    side_effects: spawn
    proposable: false
  rotate.py:seats-launch:
    cli: rotate.py
    verb: seats-launch
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - seats-launch
    reason: launches seats in tmux; never-run
    side_effects: spawn
    proposable: false
  rotate.py:spawn:
    cli: rotate.py
    verb: spawn
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - spawn
    reason: spawns a successor process; never-run by a proposer
    side_effects: spawn
    proposable: false
  rotate.py:tile:
    cli: rotate.py
    verb: tile
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - tile
    reason: lays out tmux tiles; never-run
    side_effects: spawn
    proposable: false
  boxes.py::
    cli: boxes.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/boxes.py
    args: []
    reason: "library module: which box a checkout is; its __main__ builds a bare parser and does no work -- not a choice"
    side_effects: read
    proposable: false
  mem_cap.py::
    cli: mem_cap.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/mem_cap.py
    args: []
    reason: "library module: the one memory cap for launched children; bare parser under __main__"
    side_effects: read
    proposable: false
  migrate_channel.py::
    cli: migrate_channel.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/migrate_channel.py
    args: []
    reason: "library module: the cross-box migrate record kind; bare parser under __main__"
    side_effects: read
    proposable: false
  ws_raw.py::
    cli: ws_raw.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/ws_raw.py
    args: []
    reason: long-running websocket relay; manual argv, no argparse; never proposed
    side_effects: spawn
    proposable: false
  pi_edit_forgiveness.py::
    cli: pi_edit_forgiveness.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/pi_edit_forgiveness.py
    args: []
    reason: manual argv, no argparse parser; spawn-time install gate
    side_effects: graph-write
    proposable: false
  pi_trajectory.py::
    cli: pi_trajectory.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/pi_trajectory.py
    args: []
    reason: manual argv, no argparse parser; spawns pi and tees its stream
    side_effects: spawn
    proposable: false
  backfill-mint-ids.py::
    cli: backfill-mint-ids.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/backfill-mint-ids.py
    args:
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "write", "type": "bool", "required": false, "choices": []}
    reason: one-time additive backfill; --write mints node frontmatter, operator-only
    side_effects: graph-write
    proposable: false
  decompose-engine.py::
    cli: decompose-engine.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/decompose-engine.py
    args:
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "engine_root", "type": "str", "required": false, "choices": []}
      - {"name": "goal_map", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    reason: generates idea nodes from the engine tree and prunes stale ones; operator-only
    side_effects: graph-write
    proposable: false
  derive-commands.py::
    cli: derive-commands.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/derive-commands.py
    args:
      - {"name": "files", "type": "list", "required": false, "choices": []}
      - {"name": "all", "type": "bool", "required": false, "choices": []}
      - {"name": "check", "type": "bool", "required": false, "choices": []}
    reason: rewrites marker-guarded prose files in the repo; operator-only
    side_effects: graph-write
    proposable: false
  failures.py:ledger:
    cli: failures.py
    verb: ledger
    argv:
      - python3
      - <engine>/extensions/agi/bin/failures.py
      - ledger
      - <root>
    args:
      - {"name": "root", "type": "str", "required": true, "choices": []}
      - {"name": "since", "type": "str", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "write_node", "type": "str", "required": false, "choices": []}
    reason: appends ledger rows on disk and can land a payload via --write-node; operator-only
    side_effects: graph-write
    proposable: false
  failures.py:sensei:
    cli: failures.py
    verb: sensei
    argv:
      - python3
      - <engine>/extensions/agi/bin/failures.py
      - sensei
      - <root>
    args:
      - {"name": "root", "type": "str", "required": true, "choices": []}
      - {"name": "by", "type": "str", "required": false, "choices": ["role", "model", "harness", "agent_id"]}
      - {"name": "in_path", "type": "str", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
    reason: writes the derived rate table to disk; operator-only
    side_effects: graph-write
    proposable: false
  glitch_master.py:format-record:
    cli: glitch_master.py
    verb: format-record
    argv:
      - python3
      - <engine>/extensions/agi/bin/glitch_master.py
      - format-record
      - "--iter"
      - <iter_data>
    args:
      - {"name": "iter_data", "type": "str", "required": true, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
    reason: reads workflow JSON on stdin and writes review/results.json; seat machinery, operator-only
    side_effects: graph-write
    proposable: false
  graphweb.py:serve:
    cli: graphweb.py
    verb: serve
    argv:
      - python3
      - <engine>/extensions/agi/bin/graphweb.py
      - serve
    args:
      - {"name": "host", "type": "str", "required": false, "choices": []}
      - {"name": "port", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    reason: binds a port and serves the dashboard until killed; long-running server, never proposed
    side_effects: spawn
    proposable: false
  inject.py::
    cli: inject.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/inject.py
    args:
      - {"name": "nodes_dir", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "frames", "type": "str", "required": false, "choices": []}
      - {"name": "stdout", "type": "bool", "required": false, "choices": []}
    reason: writes context/INJECTION.md; the writer half of the viewport seam, operator-only
    side_effects: graph-write
    proposable: false
  lm_bench.py::
    cli: lm_bench.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/lm_bench.py
      - "--model"
      - <model>
    reason: runs llama-bench and spends local model compute; writes a benchmark JSONL row
    side_effects: spend
    proposable: false
  mail_alert.py::
    cli: mail_alert.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/mail_alert.py
    reason: stamps an alerted_at state record per seat+thread; hook-invoked side channel
    side_effects: graph-write
    proposable: false
  plan_master.py:record-run:
    cli: plan_master.py
    verb: record-run
    argv:
      - python3
      - <engine>/extensions/agi/bin/plan_master.py
      - record-run
    reason: appends a run line to the seat-local log
    side_effects: graph-write
    proposable: false
  stall_detect.py::
    cli: stall_detect.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/stall_detect.py
      - <iter_dir>
    reason: "--record notes the stalled state on the agent.json record; detection-only"
    side_effects: graph-write
    proposable: false
  success_metrics.py::
    cli: success_metrics.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/success_metrics.py
    reason: writes the seven-metric recorded place by default; --json is the no-write path
    side_effects: graph-write
    proposable: false
  telemetry_rollup.py::
    cli: telemetry_rollup.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/telemetry_rollup.py
      - <report_id>
    reason: attaches summed telemetry to a report node via write.py; --dry-run only previews
    side_effects: graph-write
    proposable: false
  ws_raw_client.py::
    cli: ws_raw_client.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/ws_raw_client.py
    reason: streams against a live model server and writes measurement rows
    side_effects: network
    proposable: false
  verification.py::
    cli: verification.py
    verb: ""
    argv: [python3, <engine>/extensions/agi/bin/verification.py]
    reason: the rotation check carries --suite, --stamp and --ring-* flags -- a proposer must not demand the engine suite under the one-runner lock, stamp the baseline or sign a ring
    side_effects: read
    proposable: false
  verification.py:window:
    cli: verification.py
    verb: window
    argv: [python3, <engine>/extensions/agi/bin/verification.py, window]
    reason: the merge-up window shares verification.py's --suite-ring/--ring-sig signer flags -- excluded with the bare check
    side_effects: read
    proposable: false
  write_guard.py:hook:
    cli: write_guard.py
    verb: hook
    argv: [python3, <engine>/extensions/agi/bin/write_guard.py, hook]
    reason: prints a pre-commit hook that installs itself -- an install, not a choice
    side_effects: graph-write
    proposable: false
manifest:
  write.py:create:
    cli: write.py
    verb: create
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - create
      - <type>
      - <slug>
    args:
      - {"name": "type", "type": "str", "required": true, "choices": []}
      - {"name": "slug", "type": "str", "required": true, "choices": []}
      - {"name": "parent", "type": "list", "required": false, "choices": []}
      - {"name": "payload", "type": "str", "required": false, "choices": []}
      - {"name": "body_file", "type": "str", "required": false, "choices": []}
    purpose: mint a node of <type>/<slug>, linked to the schema's legal parents
    side_effects: graph-write
    proposable: true
  write.py:set:
    cli: write.py
    verb: set
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - set <key> <value>
    args:
      - {"name": "key", "type": "str", "required": true, "choices": []}
      - {"name": "value", "type": "str", "required": true, "choices": []}
    purpose: set a frontmatter key to a value, one typed coercion
    side_effects: graph-write
    proposable: true
  write.py:unset:
    cli: write.py
    verb: unset
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - unset <key>
    args:
      - {"name": "key", "type": "str", "required": true, "choices": []}
    purpose: remove a frontmatter key
    side_effects: graph-write
    proposable: true
  write.py:link:
    cli: write.py
    verb: link
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - link <ref>
    args:
      - {"name": "ref", "type": "str", "required": true, "choices": ["self", "parent", "next"]}
    purpose: add a parent/next edge reference to this node
    side_effects: graph-write
    proposable: true
  write.py:thought:
    cli: write.py
    verb: thought
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - thought <prose>
    args:
      - {"name": "prose", "type": "str", "required": true, "choices": []}
    purpose: replace the authored THOUGHT block with why this version differs
    side_effects: graph-write
    proposable: true
  write.py:note:
    cli: write.py
    verb: note
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - note <prose>
    args:
      - {"name": "prose", "type": "str", "required": true, "choices": []}
    purpose: append a whole-sentence Agent Notes line to the node
    side_effects: graph-write
    proposable: true
  write.py:sub:
    cli: write.py
    verb: sub
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - sub <old> => <new>
    args:
      - {"name": "old", "type": "str", "required": true, "choices": []}
      - {"name": "new", "type": "str", "required": true, "choices": []}
    purpose: replace exactly ONE literal occurrence anywhere in the node file (0 or 2+ matches refused, nothing written)
    side_effects: graph-write
    proposable: true
  write.py:sub!:
    cli: write.py
    verb: sub!
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - sub! <old> => <new>
    args:
      - {"name": "old", "type": "str", "required": true, "choices": []}
      - {"name": "new", "type": "str", "required": true, "choices": []}
    purpose: replace EVERY literal occurrence in the node file, the count printed
    side_effects: graph-write
    proposable: true
  write.py:payload:
    cli: write.py
    verb: payload
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - payload <path>
    args:
      - {"name": "path", "type": "str", "required": true, "choices": []}
    purpose: replace the bytes of the file this build node points at
    side_effects: graph-write
    proposable: true
  write.py:payload_text:
    cli: write.py
    verb: payload_text
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - payload_text <text>
    args:
      - {"name": "text", "type": "str", "required": true, "choices": []}
    purpose: replace the payload with literal text, no file needed
    side_effects: graph-write
    proposable: true
  write.py:read:
    cli: write.py
    verb: read
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - read <target> <range>
    args:
      - {"name": "target", "type": "str", "required": true, "choices": ["body", "payload"]}
      - {"name": "range", "type": "str", "required": true, "choices": []}
    purpose: read a body or payload slice; replace's exact inverse
    side_effects: read
    proposable: true
  write.py:replace:
    cli: write.py
    verb: replace
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - replace <target> <range> <source>
    args:
      - {"name": "target", "type": "str", "required": true, "choices": ["body", "payload"]}
      - {"name": "range", "type": "str", "required": true, "choices": []}
      - {"name": "source", "type": "str", "required": true, "choices": ["-"]}
    purpose: replace a body or payload slice with text on stdin
    side_effects: graph-write
    proposable: true
  write.py:adopt:
    cli: write.py
    verb: adopt
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
      - <node-id>
      - adopt
    args: []
    purpose: adopt the current on-disk payload/body bytes as this node's version
    side_effects: graph-write
    proposable: true
  cli.py:branch-reshuffle:
    cli: cli.py
    verb: branch-reshuffle
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - branch-reshuffle
    args:
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "apply", "type": "bool", "required": false, "choices": []}
      - {"name": "delete_old", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "kinds", "type": "str", "required": false, "choices": []}
      - {"name": "season", "type": "str", "required": false, "choices": []}
      - {"name": "plan_out", "type": "str", "required": false, "choices": []}
    purpose: cli.py branch-reshuffle
    side_effects: graph-write
    proposable: true
  cli.py:claim:
    cli: cli.py
    verb: claim
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - claim
      - "--node-id"
      - <node_id>
      - "--session"
      - <session>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
      - {"name": "session", "type": "str", "required": true, "choices": []}
    purpose: cli.py claim
    side_effects: graph-write
    proposable: true
  cli.py:detect-stale:
    cli: cli.py
    verb: detect-stale
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - detect-stale
    args:
      - {"name": "threshold_seconds", "type": "str", "required": false, "choices": []}
    purpose: cli.py detect-stale
    side_effects: read
    proposable: true
  cli.py:done:
    cli: cli.py
    verb: done
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - done
      - <iter_n>
      - <agent_id>
      - "--verdict"
      - <verdict>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "agent_id", "type": "str", "required": true, "choices": []}
      - {"name": "verdict", "type": "str", "required": true, "choices": []}
      - {"name": "confidence", "type": "str", "required": false, "choices": []}
      - {"name": "node_id", "type": "str", "required": false, "choices": []}
      - {"name": "parent", "type": "str", "required": false, "choices": []}
      - {"name": "notes", "type": "str", "required": false, "choices": []}
      - {"name": "next_edge", "type": "str", "required": false, "choices": []}
      - {"name": "push_further", "type": "str", "required": false, "choices": []}
      - {"name": "owns", "type": "str", "required": false, "choices": []}
      - {"name": "evidence_runs", "type": "str", "required": false, "choices": []}
      - {"name": "no_evidence_gate", "type": "bool", "required": false, "choices": []}
      - {"name": "no_spawn_gate", "type": "bool", "required": false, "choices": []}
      - {"name": "probes", "type": "str", "required": false, "choices": []}
      - {"name": "deliverables", "type": "str", "required": false, "choices": []}
      - {"name": "salvage", "type": "bool", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: cli.py done
    side_effects: graph-write
    proposable: true
  cli.py:loop-prune:
    cli: cli.py
    verb: loop-prune
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - loop-prune
    args:
      - {"name": "apply", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: cli.py loop-prune
    side_effects: graph-write
    proposable: true
  cli.py:pending:
    cli: cli.py
    verb: pending
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - pending
      - <iter_n>
      - <agent_id>
      - "--reason"
      - <reason>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "agent_id", "type": "str", "required": true, "choices": []}
      - {"name": "reason", "type": "str", "required": true, "choices": []}
    purpose: cli.py pending
    side_effects: graph-write
    proposable: true
  cli.py:post-rename:
    cli: cli.py
    verb: post-rename
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - post-rename
    args:
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "apply", "type": "bool", "required": false, "choices": []}
      - {"name": "delete_old", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: cli.py post-rename
    side_effects: graph-write
    proposable: true
  cli.py:reclaim:
    cli: cli.py
    verb: reclaim
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - reclaim
      - "--node-id"
      - <node_id>
      - "--session"
      - <session>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
      - {"name": "session", "type": "str", "required": true, "choices": []}
    purpose: cli.py reclaim
    side_effects: graph-write
    proposable: true
  cli.py:scaffold:
    cli: cli.py
    verb: scaffold
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - scaffold
      - <iter_n>
      - <agent_id>
      - "--type"
      - <node_type>
      - "--slug"
      - <slug>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "agent_id", "type": "str", "required": true, "choices": []}
      - {"name": "node_type", "type": "str", "required": true, "choices": ["idea", "hypothesis", "task", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "overview", "vision", "bigger-outcome", "app-purpose", "app_purpose"]}
      - {"name": "parents", "type": "str", "required": false, "choices": []}
      - {"name": "slug", "type": "str", "required": true, "choices": []}
      - {"name": "no_spawn_gate", "type": "bool", "required": false, "choices": []}
    purpose: cli.py scaffold
    side_effects: graph-write
    proposable: true
  cli.py:scope-check:
    cli: cli.py
    verb: scope-check
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - scope-check
    args:
      - {"name": "agent_id", "type": "str", "required": false, "choices": []}
      - {"name": "own", "type": "str", "required": false, "choices": []}
    purpose: cli.py scope-check
    side_effects: read
    proposable: true
  cli.py:session-complete:
    cli: cli.py
    verb: session-complete
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - session-complete
      - <iter_n>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "worktree", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: cli.py session-complete
    side_effects: graph-write
    proposable: true
  cli.py:status:
    cli: cli.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - status
      - <iter_n>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
    purpose: cli.py status
    side_effects: read
    proposable: true
  cli.py:trimguard:
    cli: cli.py
    verb: trimguard
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - trimguard
    args: []
    purpose: cli.py trimguard
    side_effects: graph-write
    proposable: true
  cli.py:wait:
    cli: cli.py
    verb: wait
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - wait
      - <iter_n>
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "agent", "type": "str", "required": false, "choices": []}
      - {"name": "max_seconds", "type": "str", "required": false, "choices": []}
    purpose: cli.py wait
    side_effects: read
    proposable: true
  crons.py:apply:
    cli: crons.py
    verb: apply
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - apply
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "crontab_file", "type": "str", "required": false, "choices": []}
      - {"name": "unit_dir", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: crons.py apply
    side_effects: graph-write
    proposable: false
    reason: writes the real crontab / systemd units; operator-only
  crons.py:audit:
    cli: crons.py
    verb: audit
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - audit
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "crontab_file", "type": "str", "required": false, "choices": []}
      - {"name": "unit_dir", "type": "str", "required": false, "choices": []}
    purpose: crons.py audit
    side_effects: graph-write
    proposable: true
  crons.py:remove:
    cli: crons.py
    verb: remove
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - remove
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "crontab_file", "type": "str", "required": false, "choices": []}
      - {"name": "unit_dir", "type": "str", "required": false, "choices": []}
    purpose: crons.py remove
    side_effects: graph-write
    proposable: false
    reason: removes the real crontab / systemd units; operator-only
  crons.py:show:
    cli: crons.py
    verb: show
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - show
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "crontab_file", "type": "str", "required": false, "choices": []}
      - {"name": "unit_dir", "type": "str", "required": false, "choices": []}
    purpose: crons.py show
    side_effects: read
    proposable: true
  envfile.py::
    cli: envfile.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/envfile.py
    args:
      - {"name": "start", "type": "str", "required": false, "choices": []}
      - {"name": "what", "type": "str", "required": false, "choices": ["env-file", "template", "node"]}
      - {"name": "check", "type": "bool", "required": false, "choices": []}
      - {"name": "json", "type": "bool", "required": false, "choices": []}
      - {"name": "set", "type": "str", "required": false, "choices": []}
    purpose: envfile.py
    side_effects: graph-write
    proposable: true
  grid.py:commit:
    cli: grid.py
    verb: commit
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - commit
      - <files>
    args:
      - {"name": "files", "type": "str", "required": true, "choices": []}
      - {"name": "all", "type": "bool", "required": false, "choices": []}
      - {"name": "session", "type": "str", "required": false, "choices": []}
      - {"name": "prefix", "type": "str", "required": false, "choices": []}
      - {"name": "allow_branch", "type": "bool", "required": false, "choices": []}
      - {"name": "lock_wait", "type": "str", "required": false, "choices": []}
    purpose: grid.py commit
    side_effects: graph-write
    proposable: true
  grid.py:cron:
    cli: grid.py
    verb: cron
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - cron
      - <action>
    args:
      - {"name": "action", "type": "str", "required": true, "choices": ["install", "show", "remove"]}
      - {"name": "snapshot_mins", "type": "str", "required": false, "choices": []}
      - {"name": "publish_engine", "type": "bool", "required": false, "choices": []}
    purpose: grid.py cron
    side_effects: destructive
    proposable: false
    reason: install / remove write the real crontab; operator-only
  grid.py:diff:
    cli: grid.py
    verb: diff
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - diff
      - <node_id>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
      - {"name": "back", "type": "str", "required": false, "choices": []}
    purpose: grid.py diff
    side_effects: read
    proposable: true
  grid.py:init:
    cli: grid.py
    verb: init
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - init
    args: []
    purpose: grid.py init
    side_effects: graph-write
    proposable: true
  grid.py:log:
    cli: grid.py
    verb: log
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - log
      - <node_id>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
      - {"name": "n", "type": "str", "required": false, "choices": []}
    purpose: grid.py log
    side_effects: read
    proposable: true
  grid.py:payload:
    cli: grid.py
    verb: payload
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - payload
      - <node_id>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
      - {"name": "version", "type": "str", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
    purpose: grid.py payload
    side_effects: read
    proposable: true
  grid.py:status:
    cli: grid.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - status
    args: []
    purpose: grid.py status
    side_effects: read
    proposable: true
  grid.py:versions:
    cli: grid.py
    verb: versions
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - versions
      - <node_id>
    args:
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
    purpose: grid.py versions
    side_effects: read
    proposable: true
  links.py:links:
    cli: links.py
    verb: links
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - links
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "broken", "type": "bool", "required": false, "choices": []}
      - {"name": "fix", "type": "bool", "required": false, "choices": []}
    purpose: links.py links
    side_effects: read
    proposable: true
  links.py:roles:
    cli: links.py
    verb: roles
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - roles
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "broken", "type": "bool", "required": false, "choices": []}
      - {"name": "fix", "type": "bool", "required": false, "choices": []}
    purpose: links.py roles
    side_effects: read
    proposable: true
  links.py:schema:
    cli: links.py
    verb: schema
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - schema
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "broken", "type": "bool", "required": false, "choices": []}
      - {"name": "fix", "type": "bool", "required": false, "choices": []}
    purpose: links.py schema
    side_effects: read
    proposable: true
  provisioning.py:capture:
    cli: provisioning.py
    verb: capture
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - capture
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "prev", "type": "str", "required": false, "choices": []}
    purpose: provisioning.py capture
    side_effects: graph-write
    proposable: true
  provisioning.py:diff:
    cli: provisioning.py
    verb: diff
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - diff
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "prev", "type": "str", "required": false, "choices": []}
    purpose: provisioning.py diff
    side_effects: read
    proposable: true
  provisioning.py:list:
    cli: provisioning.py
    verb: list
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - list
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "prev", "type": "str", "required": false, "choices": []}
    purpose: provisioning.py list
    side_effects: read
    proposable: true
  provisioning.py:spend:
    cli: provisioning.py
    verb: spend
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - spend
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "prev", "type": "str", "required": false, "choices": []}
    purpose: provisioning.py spend
    side_effects: read
    proposable: true
  provisioning.py:status:
    cli: provisioning.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - status
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "prev", "type": "str", "required": false, "choices": []}
    purpose: provisioning.py status
    side_effects: read
    proposable: true
  rotate.py:autopsy:
    cli: rotate.py
    verb: autopsy
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - autopsy
      - "--seat"
      - <seat>
    args:
      - {"name": "seat", "type": "str", "required": true, "choices": []}
      - {"name": "pid", "type": "str", "required": false, "choices": []}
      - {"name": "registry_dir", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: rotate.py autopsy
    side_effects: read
    proposable: true
  rotate.py:bootstrap-block:
    cli: rotate.py
    verb: bootstrap-block
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - bootstrap-block
      - "--seat"
      - <seat>
    args:
      - {"name": "seat", "type": "str", "required": true, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "commit", "type": "str", "required": false, "choices": []}
      - {"name": "bounds", "type": "str", "required": false, "choices": []}
      - {"name": "json", "type": "bool", "required": false, "choices": []}
      - {"name": "quiet", "type": "bool", "required": false, "choices": []}
    purpose: rotate.py bootstrap-block
    side_effects: graph-write
    proposable: true
  rotate.py:handoff:
    cli: rotate.py
    verb: handoff
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - handoff
    args:
      - {"name": "driven", "type": "bool", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "field", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: rotate.py handoff
    side_effects: graph-write
    proposable: true
  rotate.py:harvest-table:
    cli: rotate.py
    verb: harvest-table
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - harvest-table
    args:
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "round", "type": "str", "required": false, "choices": []}
      - {"name": "all_live", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: rotate.py harvest-table
    side_effects: read
    proposable: true
  rotate.py:meter:
    cli: rotate.py
    verb: meter
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - meter
    args:
      - {"name": "session_log", "type": "str", "required": false, "choices": []}
      - {"name": "check", "type": "bool", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "pin", "type": "str", "required": false, "choices": []}
    purpose: rotate.py meter
    side_effects: read
    proposable: true
  rotate.py:next:
    cli: rotate.py
    verb: next
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - next
      - "--seat"
      - <seat>
    args:
      - {"name": "seat", "type": "str", "required": true, "choices": []}
      - {"name": "role", "type": "str", "required": false, "choices": []}
      - {"name": "template", "type": "str", "required": false, "choices": []}
      - {"name": "record", "type": "str", "required": false, "choices": ["ok", "fail"]}
      - {"name": "json", "type": "bool", "required": false, "choices": []}
      - {"name": "gen", "type": "str", "required": false, "choices": []}
      - {"name": "succ_name", "type": "str", "required": false, "choices": []}
      - {"name": "tmux_session", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: rotate.py next
    side_effects: read
    proposable: true
  rotate.py:seq:
    cli: rotate.py
    verb: seq
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - seq
    args: []
    purpose: rotate.py seq
    side_effects: read
    proposable: true
  rotate.py:status:
    cli: rotate.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/rotate.py
      - status
    args:
      - {"name": "seats", "type": "bool", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "record", "type": "str", "required": false, "choices": []}
      - {"name": "wait", "type": "str", "required": false, "choices": []}
    purpose: rotate.py status
    side_effects: read
    proposable: true
  send.py:ask:
    cli: send.py
    verb: ask
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - ask
      - "--to"
      - <to>
      - <text>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "to", "type": "str", "required": true, "choices": []}
      - {"name": "text", "type": "str", "required": true, "choices": []}
    purpose: send.py ask
    side_effects: comms
    proposable: true
  send.py:audience:
    cli: send.py
    verb: audience
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - audience
      - <target>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": true, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "morals", "type": "bool", "required": false, "choices": []}
      - {"name": "aud_round", "type": "str", "required": false, "choices": []}
      - {"name": "decision", "type": "str", "required": false, "choices": []}
    purpose: send.py audience
    side_effects: comms
    proposable: true
  send.py:escalate:
    cli: send.py
    verb: escalate
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - escalate
      - <text>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "to", "type": "str", "required": false, "choices": []}
      - {"name": "concern", "type": "str", "required": false, "choices": []}
      - {"name": "text", "type": "str", "required": true, "choices": []}
    purpose: send.py escalate
    side_effects: comms
    proposable: true
  send.py:keygen:
    cli: send.py
    verb: keygen
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - keygen
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "scheme", "type": "str", "required": false, "choices": []}
      - {"name": "all_live", "type": "bool", "required": false, "choices": []}
      - {"name": "onboard", "type": "str", "required": false, "choices": []}
      - {"name": "sponsor", "type": "str", "required": false, "choices": []}
      - {"name": "sponsor_sig", "type": "str", "required": false, "choices": []}
      - {"name": "sponsor_sign", "type": "str", "required": false, "choices": []}
      - {"name": "charter_hash", "type": "str", "required": false, "choices": []}
      - {"name": "budget", "type": "str", "required": false, "choices": []}
    purpose: send.py keygen
    side_effects: comms
    proposable: true
  send.py:peek:
    cli: send.py
    verb: peek
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - peek
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "dm", "type": "str", "required": false, "choices": []}
      - {"name": "since", "type": "str", "required": false, "choices": []}
      - {"name": "all_", "type": "bool", "required": false, "choices": []}
      - {"name": "me", "type": "str", "required": false, "choices": []}
      - {"name": "wrap", "type": "str", "required": false, "choices": []}
    purpose: send.py peek
    side_effects: read
    proposable: true
  send.py:prime-excluded:
    cli: send.py
    verb: prime-excluded
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - prime-excluded
      - "--round"
      - <round>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "round", "type": "str", "required": true, "choices": []}
    purpose: send.py prime-excluded
    side_effects: comms
    proposable: true
  send.py:read:
    cli: send.py
    verb: read
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - read
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "dm", "type": "str", "required": false, "choices": []}
      - {"name": "since", "type": "str", "required": false, "choices": []}
      - {"name": "all_", "type": "bool", "required": false, "choices": []}
      - {"name": "me", "type": "str", "required": false, "choices": []}
      - {"name": "wrap", "type": "str", "required": false, "choices": []}
      - {"name": "box_local", "type": "bool", "required": false, "choices": []}
    purpose: send.py read
    side_effects: read
    proposable: true
  send.py:report:
    cli: send.py
    verb: report
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - report
      - "--ref"
      - <ref>
      - <text>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "asker", "type": "str", "required": false, "choices": []}
      - {"name": "report_room", "type": "str", "required": false, "choices": []}
      - {"name": "ref", "type": "str", "required": true, "choices": []}
      - {"name": "text", "type": "str", "required": true, "choices": []}
    purpose: send.py report
    side_effects: comms
    proposable: true
  send.py:rooms:
    cli: send.py
    verb: rooms
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - rooms
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "me", "type": "str", "required": false, "choices": []}
    purpose: send.py rooms
    side_effects: read
    proposable: true
  send.py:send:
    cli: send.py
    verb: send
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - send
      - <send_args>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "send_args", "type": "str", "required": true, "choices": []}
      - {"name": "dm_to", "type": "str", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "quote_harness", "type": "bool", "required": false, "choices": []}
    purpose: send.py send
    side_effects: comms
    proposable: true
  send.py:status:
    cli: send.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - status
      - <target>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": true, "choices": []}
    purpose: send.py status
    side_effects: read
    proposable: true
  send.py:veto:
    cli: send.py
    verb: veto
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - veto
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "scope", "type": "str", "required": false, "choices": []}
      - {"name": "answer", "type": "str", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "file", "type": "str", "required": false, "choices": []}
    purpose: send.py veto
    side_effects: comms
    proposable: true
  send.py:vote:
    cli: send.py
    verb: vote
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - vote
      - "--target"
      - <target>
      - "--vision"
      - <vision>
      - "--alignment"
      - <alignment>
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": true, "choices": []}
      - {"name": "vision", "type": "str", "required": true, "choices": []}
      - {"name": "alignment", "type": "str", "required": true, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "morals", "type": "bool", "required": false, "choices": []}
      - {"name": "v_round", "type": "str", "required": false, "choices": []}
    purpose: send.py vote
    side_effects: comms
    proposable: true
  send.py:wake:
    cli: send.py
    verb: wake
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - wake
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "target", "type": "str", "required": false, "choices": []}
      - {"name": "all_local", "type": "bool", "required": false, "choices": []}
    purpose: send.py wake
    side_effects: comms
    proposable: true
  send.py:whois:
    cli: send.py
    verb: whois
    argv:
      - python3
      - <engine>/extensions/agi/bin/send.py
      - whois
    args:
      - {"name": "from_id", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "session_ref", "type": "str", "required": false, "choices": []}
      - {"name": "key", "type": "str", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
      - {"name": "claim", "type": "str", "required": false, "choices": []}
      - {"name": "source", "type": "str", "required": false, "choices": []}
      - {"name": "no_fetch", "type": "bool", "required": false, "choices": []}
      - {"name": "sig", "type": "str", "required": false, "choices": []}
      - {"name": "msg", "type": "str", "required": false, "choices": []}
    purpose: send.py whois
    side_effects: read
    proposable: true
  snapshot-goals.py::
    cli: snapshot-goals.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/snapshot-goals.py
    args:
      - {"name": "strict", "type": "bool", "required": false, "choices": []}
      - {"name": "strict_goals", "type": "bool", "required": false, "choices": []}
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "render", "type": "bool", "required": false, "choices": []}
      - {"name": "check", "type": "bool", "required": false, "choices": []}
      - {"name": "from_doc", "type": "bool", "required": false, "choices": []}
    purpose: snapshot-goals.py
    side_effects: graph-write
    proposable: true
  spawn_budget.py:pause:
    cli: spawn_budget.py
    verb: pause
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - pause
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "iter", "type": "str", "required": false, "choices": []}
      - {"name": "wait", "type": "bool", "required": false, "choices": []}
      - {"name": "timeout", "type": "str", "required": false, "choices": []}
    purpose: spawn_budget.py pause
    side_effects: graph-write
    proposable: true
  spawn_budget.py:resume:
    cli: spawn_budget.py
    verb: resume
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - resume
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "iter", "type": "str", "required": false, "choices": []}
      - {"name": "wait", "type": "bool", "required": false, "choices": []}
      - {"name": "timeout", "type": "str", "required": false, "choices": []}
    purpose: spawn_budget.py resume
    side_effects: graph-write
    proposable: true
  spawn_budget.py:status:
    cli: spawn_budget.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - status
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "iter", "type": "str", "required": false, "choices": []}
      - {"name": "wait", "type": "bool", "required": false, "choices": []}
      - {"name": "timeout", "type": "str", "required": false, "choices": []}
    purpose: spawn_budget.py status
    side_effects: read
    proposable: true
  spawn_budget.py:sweep:
    cli: spawn_budget.py
    verb: sweep
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - sweep
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "reason", "type": "str", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "iter", "type": "str", "required": false, "choices": []}
      - {"name": "wait", "type": "bool", "required": false, "choices": []}
      - {"name": "timeout", "type": "str", "required": false, "choices": []}
    purpose: spawn_budget.py sweep
    side_effects: graph-write
    proposable: true
  viewport.py::
    cli: viewport.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
    args:
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "anchor", "type": "str", "required": false, "choices": []}
      - {"name": "depth", "type": "str", "required": false, "choices": []}
      - {"name": "emit", "type": "str", "required": false, "choices": ["human", "llm", "both"]}
      - {"name": "verify", "type": "bool", "required": false, "choices": []}
      - {"name": "iter", "type": "str", "required": false, "choices": []}
      - {"name": "live", "type": "bool", "required": false, "choices": []}
      - {"name": "top", "type": "str", "required": false, "choices": []}
      - {"name": "left", "type": "str", "required": false, "choices": []}
      - {"name": "height", "type": "str", "required": false, "choices": []}
      - {"name": "width", "type": "str", "required": false, "choices": []}
      - {"name": "theme", "type": "str", "required": false, "choices": ["graph", "keep"]}
      - {"name": "layer", "type": "str", "required": false, "choices": ["graph", "hierarchy"]}
    purpose: viewport.py
    side_effects: read
    proposable: true
  workflow.py:author:
    cli: workflow.py
    verb: author
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - author
      - <name>
    args:
      - {"name": "name", "type": "str", "required": true, "choices": []}
      - {"name": "stages", "type": "str", "required": false, "choices": []}
      - {"name": "json", "type": "str", "required": false, "choices": []}
      - {"name": "stdin", "type": "bool", "required": false, "choices": []}
      - {"name": "note", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py author
    side_effects: graph-write
    proposable: true
  workflow.py:link:
    cli: workflow.py
    verb: link
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - link
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py link
    side_effects: graph-write
    proposable: true
  workflow.py:list:
    cli: workflow.py
    verb: list
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - list
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py list
    side_effects: read
    proposable: true
  workflow.py:note:
    cli: workflow.py
    verb: note
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - note
      - "--harness-id"
      - <harness_id>
      - <run_key>
    args:
      - {"name": "run_key", "type": "str", "required": true, "choices": []}
      - {"name": "harness_id", "type": "str", "required": true, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py note
    side_effects: graph-write
    proposable: true
  workflow.py:register:
    cli: workflow.py
    verb: register
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - register
      - "--script"
      - <script>
      - <name>
    args:
      - {"name": "name", "type": "str", "required": true, "choices": []}
      - {"name": "script", "type": "str", "required": true, "choices": []}
      - {"name": "from_run", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py register
    side_effects: graph-write
    proposable: true
  workflow.py:run:
    cli: workflow.py
    verb: run
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - run
      - <name>
    args:
      - {"name": "name", "type": "str", "required": true, "choices": []}
      - {"name": "harness", "type": "str", "required": false, "choices": []}
      - {"name": "args", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py run
    side_effects: spawn
    proposable: false
    reason: spawns a workflow subprocess; operator-only, never proposed
  workflow.py:status:
    cli: workflow.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - status
    args:
      - {"name": "key", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py status
    side_effects: read
    proposable: true
  workflow.py:validate:
    cli: workflow.py
    verb: validate
    argv:
      - python3
      - <engine>/extensions/agi/bin/workflow.py
      - validate
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: workflow.py validate
    side_effects: read
    proposable: true
  brief.py:head:
    cli: brief.py
    verb: head
    argv:
      - python3
      - <engine>/extensions/agi/bin/brief.py
      - head
    args:
      - {"name": "tier", "type": "str", "required": false, "choices": []}
      - {"name": "role", "type": "str", "required": false, "choices": []}
      - {"name": "project_root", "type": "str", "required": false, "choices": []}
    purpose: print a tier constitution head
    side_effects: read
    proposable: true
  brief.py:readings:
    cli: brief.py
    verb: readings
    argv:
      - python3
      - <engine>/extensions/agi/bin/brief.py
      - readings
    args:
      - {"name": "tier", "type": "str", "required": false, "choices": []}
      - {"name": "role", "type": "str", "required": false, "choices": []}
      - {"name": "project_root", "type": "str", "required": false, "choices": []}
    purpose: print the on-demand constitution readings for a tier
    side_effects: read
    proposable: true
  brief.py:render:
    cli: brief.py
    verb: render
    argv:
      - python3
      - <engine>/extensions/agi/bin/brief.py
      - render
    args:
      - {"name": "post", "type": "str", "required": false, "choices": []}
      - {"name": "role", "type": "str", "required": false, "choices": []}
      - {"name": "harness", "type": "str", "required": false, "choices": []}
      - {"name": "project_root", "type": "str", "required": false, "choices": []}
    purpose: print the whole first user turn for a seat; writes no file
    side_effects: read
    proposable: true
  level3.py::
    cli: level3.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/level3.py
    args:
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "engine_root", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "from_grid", "type": "bool", "required": false, "choices": []}
      - {"name": "mint_missing_only", "type": "bool", "required": false, "choices": []}
      - {"name": "mvp_map", "type": "str", "required": false, "choices": []}
    purpose: derive one level-3 node per code file
    side_effects: graph-write
    proposable: false
    reason: default scan prunes stale level3-scan build nodes; operator-only
  season.py:status:
    cli: season.py
    verb: status
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - status
    args: []
    purpose: print per-tier plan/report counts
    side_effects: read
    proposable: true
  season.py:judge:
    cli: season.py
    verb: judge
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - judge
      - <report_id>
    args:
      - {"name": "report_id", "type": "str", "required": true, "choices": []}
      - {"name": "against", "type": "str", "required": false, "choices": []}
      - {"name": "debug", "type": "bool", "required": false, "choices": []}
      - {"name": "quorum", "type": "bool", "required": false, "choices": []}
      - {"name": "room", "type": "str", "required": false, "choices": []}
      - {"name": "judge_round", "type": "str", "required": false, "choices": []}
      - {"name": "comms_root", "type": "str", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "session", "type": "str", "required": false, "choices": []}
    purpose: stamp a judgment record on a report node
    side_effects: graph-write
    proposable: true
  season.py:rollover:
    cli: season.py
    verb: rollover
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - rollover
    args:
      - {"name": "dry_run_explicit", "type": "bool", "required": false, "choices": []}
      - {"name": "debug", "type": "bool", "required": false, "choices": []}
      - {"name": "visions_from", "type": "str", "required": false, "choices": []}
      - {"name": "name", "type": "str", "required": false, "choices": []}
      - {"name": "branch", "type": "bool", "required": false, "choices": []}
      - {"name": "allow_unjudged", "type": "bool", "required": false, "choices": []}
      - {"name": "align", "type": "bool", "required": false, "choices": []}
      - {"name": "global_rollover", "type": "bool", "required": false, "choices": []}
      - {"name": "town", "type": "str", "required": false, "choices": []}
      - {"name": "align_apply", "type": "bool", "required": false, "choices": []}
      - {"name": "delete_old", "type": "bool", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "session", "type": "str", "required": false, "choices": []}
    purpose: print or perform season rollover
    side_effects: graph-write
    proposable: false
    reason: rewrites the ladder and can open a branch; operator-only
  season.py:retag:
    cli: season.py
    verb: retag
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - retag
    args:
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "actor", "type": "str", "required": false, "choices": []}
      - {"name": "session", "type": "str", "required": false, "choices": []}
    purpose: backfill season on every node that lacks it
    side_effects: graph-write
    proposable: false
    reason: graph-wide batch stamp; operator-only
  season.py:merge-kids:
    cli: season.py
    verb: merge-kids
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - merge-kids
    args:
      - {"name": "branches", "type": "str", "required": true, "choices": []}
      - {"name": "suite", "type": "str", "required": false, "choices": []}
    purpose: merge kid branches --no-ff into the current branch
    side_effects: graph-write
    proposable: false
    reason: merges branches and can leave a merge in progress; operator-only
  season.py:merge-up:
    cli: season.py
    verb: merge-up
    argv:
      - python3
      - <engine>/extensions/agi/bin/season.py
      - merge-up
    args:
      - {"name": "branch", "type": "str", "required": true, "choices": []}
      - {"name": "target", "type": "str", "required": false, "choices": []}
      - {"name": "suite", "type": "str", "required": false, "choices": []}
      - {"name": "worktree", "type": "str", "required": false, "choices": []}
      - {"name": "record", "type": "str", "required": false, "choices": []}
      - {"name": "round", "type": "str", "required": false, "choices": []}
      - {"name": "seat", "type": "str", "required": false, "choices": []}
    purpose: merge a loop branch into its base behind a suite gate
    side_effects: graph-write
    proposable: false
    reason: merges branches behind a suite gate; operator-only
  heal.py::
    cli: heal.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/heal.py
    args:
      - {"name": "project_root", "type": "str", "required": true, "choices": []}
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "poll_interval_s", "type": "str", "required": false, "choices": []}
      - {"name": "max_wait_mins", "type": "str", "required": false, "choices": []}
    purpose: "live-seat repair: watch / sweep / pin-reap / inline wait"
    side_effects: graph-write
    proposable: false
    reason: touches live agent leases and the session registry; operator-only
  zoom.py::
    cli: zoom.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/zoom.py
      - <project_root>
      - <iter_n>
      - <agent_id>
    args:
      - {"name": "project_root", "type": "str", "required": true, "choices": []}
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
      - {"name": "agent_id", "type": "str", "required": true, "choices": []}
      - {"name": "level", "type": "str", "required": true, "choices": []}
      - {"name": "target", "type": "str", "required": false, "choices": []}
      - {"name": "runtime", "type": "str", "required": false, "choices": []}
      - {"name": "tier", "type": "str", "required": false, "choices": []}
      - {"name": "push_further", "type": "bool", "required": false, "choices": []}
    purpose: render a zoom context for an agent
    side_effects: graph-write
    proposable: true
  locations.py::
    cli: locations.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/locations.py
    args:
      - {"name": "start", "type": "str", "required": false, "choices": []}
      - {"name": "json", "type": "bool", "required": false, "choices": []}
      - {"name": "what", "type": "str", "required": false, "choices": []}
      - {"name": "claim_iter", "type": "bool", "required": false, "choices": []}
      - {"name": "loop", "type": "str", "required": false, "choices": []}
      - {"name": "explicit_iter", "type": "str", "required": false, "choices": []}
      - {"name": "after", "type": "str", "required": false, "choices": []}
      - {"name": "numeric", "type": "bool", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: resolve agi project locations / allocate an iteration id
    side_effects: graph-write
    proposable: true
  commands.py:list:
    cli: commands.py
    verb: list
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - list
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: list the declared commands by workflow
    side_effects: read
    proposable: true
  commands.py:show:
    cli: commands.py
    verb: show
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - show
      - <name>
    args:
      - {"name": "name", "type": "str", "required": true, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: print one declared command argv
    side_effects: read
    proposable: true
  commands.py:json:
    cli: commands.py
    verb: json
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - json
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: print every declared command as JSON
    side_effects: read
    proposable: true
  commands.py:manifest:
    cli: commands.py
    verb: manifest
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - manifest
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: print the one machine-readable choice set
    side_effects: read
    proposable: true
  commands.py:propose:
    cli: commands.py
    verb: propose
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - propose
      - <name>
    args:
      - {"name": "name", "type": "str", "required": true, "choices": []}
      - {"name": "args_json", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: validate args and return an argv; never runs it
    side_effects: read
    proposable: true
  commands.py:run:
    cli: commands.py
    verb: run
    argv:
      - python3
      - <engine>/extensions/agi/bin/commands.py
      - run
    args:
      - {"name": "action", "type": "str", "required": false, "choices": ["list", "show", "json", "manifest", "propose", "run"]}
      - {"name": "name", "type": "str", "required": false, "choices": []}
      - {"name": "extra", "type": "str", "required": false, "choices": []}
      - {"name": "args_json", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "workflow", "type": "str", "required": false, "choices": []}
      - {"name": "start_from", "type": "str", "required": false, "choices": []}
    purpose: run a declared command
    side_effects: spawn
    proposable: false
    reason: executes an arbitrary declared command; operator-only
  stitch.py::
    cli: stitch.py
    verb:
    argv:
      - python3
      - <engine>/extensions/agi/bin/stitch.py
    args:
      - {"name": "project", "type": "str", "required": true, "choices": []}
      - {"name": "out", "type": "str", "required": false, "choices": []}
      - {"name": "engine_root", "type": "str", "required": false, "choices": []}
      - {"name": "force", "type": "bool", "required": false, "choices": []}
      - {"name": "version", "type": "str", "required": false, "choices": []}
      - {"name": "from_grid", "type": "bool", "required": false, "choices": []}
      - {"name": "grid_version", "type": "str", "required": false, "choices": []}
      - {"name": "publish", "type": "bool", "required": false, "choices": []}
      - {"name": "verify", "type": "bool", "required": false, "choices": []}
      - {"name": "strict", "type": "bool", "required": false, "choices": []}
    purpose: materialize level-3 nodes into a tree, or verify drift
    side_effects: graph-write
    proposable: false
    reason: materializes or overwrites a tree and --publish writes into the engine repo; operator-only
  paths.py:audit:
    cli: paths.py
    verb: audit
    argv:
      - python3
      - <engine>/extensions/agi/bin/paths.py
      - audit
    args:
      - {"name": "dir", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: audit that paths live in config, not as literals
    side_effects: read
    proposable: true
  evidence_gate.py:enforce:
    cli: evidence_gate.py
    verb: enforce
    argv:
      - python3
      - <engine>/extensions/agi/bin/evidence_gate.py
      - enforce
    args:
      - {"name": "action", "type": "str", "required": false, "choices": ["enforce"]}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: demote unevidenced verdicts on disk
    side_effects: graph-write
    proposable: false
    reason: demotes verdicts on disk; the commit path already runs it, operator-only
  sensei.py:pick_worst:
    cli: sensei.py
    verb: pick_worst
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - pick_worst
    args:
      - {"name": "ledger", "type": "str", "required": false, "choices": []}
      - {"name": "rows", "type": "str", "required": false, "choices": []}
    purpose: pick the worst failure-ledger row
    side_effects: read
    proposable: true
  sensei.py:propose:
    cli: sensei.py
    verb: propose
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - propose
    args:
      - {"name": "target", "type": "str", "required": true, "choices": []}
      - {"name": "change", "type": "str", "required": false, "choices": []}
      - {"name": "supervisor", "type": "str", "required": false, "choices": []}
    purpose: ping a seat and its supervisor for a proposed change
    side_effects: comms
    proposable: true
  sensei.py:wake-audit:
    cli: sensei.py
    verb: wake-audit
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - wake-audit
    args:
      - {"name": "seat", "type": "str", "required": true, "choices": []}
      - {"name": "gen", "type": "str", "required": false, "choices": []}
      - {"name": "record", "type": "str", "required": false, "choices": []}
      - {"name": "transcript", "type": "str", "required": false, "choices": []}
      - {"name": "redact", "type": "bool", "required": false, "choices": []}
      - {"name": "no_record", "type": "bool", "required": false, "choices": []}
      - {"name": "settled", "type": "bool", "required": false, "choices": []}
    purpose: classify a rotation wake tool calls
    side_effects: read
    proposable: true
  sensei.py:rotate-out-audit:
    cli: sensei.py
    verb: rotate-out-audit
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - rotate-out-audit
    args:
      - {"name": "seat", "type": "str", "required": true, "choices": []}
      - {"name": "gen", "type": "str", "required": false, "choices": []}
      - {"name": "record", "type": "str", "required": false, "choices": []}
      - {"name": "transcript", "type": "str", "required": false, "choices": []}
      - {"name": "registry_dir", "type": "str", "required": false, "choices": []}
      - {"name": "no_record", "type": "bool", "required": false, "choices": []}
      - {"name": "settled", "type": "bool", "required": false, "choices": []}
    purpose: classify the outgoing predecessor rotate-out calls
    side_effects: read
    proposable: true
  sensei.py:apply:
    cli: sensei.py
    verb: apply
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - apply
    args:
      - {"name": "target", "type": "str", "required": true, "choices": []}
      - {"name": "node_id", "type": "str", "required": false, "choices": []}
      - {"name": "change", "type": "str", "required": false, "choices": []}
      - {"name": "since", "type": "str", "required": false, "choices": []}
      - {"name": "supervisor", "type": "str", "required": false, "choices": []}
      - {"name": "owner_approved", "type": "bool", "required": false, "choices": []}
    purpose: apply a change once both threads reply
    side_effects: graph-write
    proposable: false
    reason: applies a supervisor-approved change; owner-approval gate, operator-only
  sensei.py:calls:
    cli: sensei.py
    verb: calls
    argv:
      - python3
      - <engine>/extensions/agi/bin/sensei.py
      - calls
      - <transcript>
    args:
      - {"name": "transcript", "type": "str", "required": true, "choices": []}
      - {"name": "from_", "type": "str", "required": false, "choices": []}
      - {"name": "to", "type": "str", "required": false, "choices": []}
      - {"name": "width", "type": "str", "required": false, "choices": []}
    purpose: list a transcript assistant tool calls
    side_effects: read
    proposable: true
  post_wire.py::
    cli: post_wire.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/post_wire.py
    args:
      - {"name": "project_root", "type": "str", "required": false, "choices": []}
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
    purpose: wire agent verdicts back into the node graph
    side_effects: graph-write
    proposable: false
    reason: bulk-wires agent verdicts into the graph from the harness; loop-owned, operator-only
  unify.py::
    cli: unify.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/unify.py
      - "--engine"
      - <engine>
    args:
      - {"name": "engine", "type": "str", "required": true, "choices": []}
      - {"name": "tree", "type": "str", "required": false, "choices": []}
      - {"name": "rollback", "type": "bool", "required": false, "choices": []}
      - {"name": "yes", "type": "bool", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
      - {"name": "this_is_the_real_migration", "type": "bool", "required": false, "choices": []}
      - {"name": "force", "type": "bool", "required": false, "choices": []}
      - {"name": "report_json", "type": "bool", "required": false, "choices": []}
    purpose: merge the two-repo layout into one
    side_effects: destructive
    proposable: false
    reason: destructive one-repo migration and rollback; owner-ops, never proposed
  hierarchy.py:render:
    cli: hierarchy.py
    verb: render
    argv:
      - python3
      - <engine>/extensions/agi/bin/hierarchy.py
      - render
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "check", "type": "bool", "required": false, "choices": []}
    purpose: render the hierarchy view
    side_effects: read
    proposable: true
  handoff.py:sections:
    cli: handoff.py
    verb: sections
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - sections
    args:
      - {"name": "whole", "type": "bool", "required": false, "choices": []}
    purpose: list stable handoff sections with their cost
    side_effects: read
    proposable: true
  handoff.py:claim:
    cli: handoff.py
    verb: claim
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - claim
      - <section>
    args:
      - {"name": "section", "type": "str", "required": true, "choices": []}
      - {"name": "holder", "type": "str", "required": false, "choices": []}
      - {"name": "write", "type": "bool", "required": false, "choices": []}
      - {"name": "force", "type": "bool", "required": false, "choices": []}
    purpose: claim a shared handoff section lease
    side_effects: graph-write
    proposable: false
    reason: claims a shared handoff lease; touches the shared scratchpad, operator-only
  handoff.py:release:
    cli: handoff.py
    verb: release
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - release
      - <section>
    args:
      - {"name": "section", "type": "str", "required": true, "choices": []}
      - {"name": "holder", "type": "str", "required": false, "choices": []}
    purpose: release a shared handoff section lease
    side_effects: graph-write
    proposable: false
    reason: releases a shared handoff lease; touches the shared scratchpad, operator-only
  handoff.py:read:
    cli: handoff.py
    verb: read
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - read
    args:
      - {"name": "section", "type": "str", "required": false, "choices": []}
      - {"name": "holder", "type": "str", "required": false, "choices": []}
      - {"name": "prime", "type": "bool", "required": false, "choices": []}
      - {"name": "whole", "type": "bool", "required": false, "choices": []}
    purpose: read one claimed handoff section
    side_effects: read
    proposable: true
  handoff.py:write:
    cli: handoff.py
    verb: write
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - write
      - <section>
    args:
      - {"name": "section", "type": "str", "required": true, "choices": []}
      - {"name": "holder", "type": "str", "required": false, "choices": []}
      - {"name": "prime", "type": "bool", "required": false, "choices": []}
      - {"name": "content", "type": "str", "required": false, "choices": []}
      - {"name": "content_file", "type": "str", "required": false, "choices": []}
      - {"name": "stdin", "type": "bool", "required": false, "choices": []}
    purpose: replace one held handoff section
    side_effects: graph-write
    proposable: false
    reason: replaces a shared handoff section; touches the shared scratchpad, operator-only
  handoff.py:show:
    cli: handoff.py
    verb: show
    argv:
      - python3
      - <engine>/extensions/agi/bin/handoff.py
      - show
    args: []
    purpose: show the current handoff claims
    side_effects: read
    proposable: true
  benchmark.py::
    cli: benchmark.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/benchmark.py
      - <chain_id>
    args:
      - {"name": "chain_id", "type": "str", "required": true, "choices": []}
      - {"name": "model", "type": "str", "required": false, "choices": []}
      - {"name": "timeout", "type": "str", "required": false, "choices": []}
      - {"name": "dry_run", "type": "bool", "required": false, "choices": []}
    purpose: judge a chain with a local model
    side_effects: spend
    proposable: false
    reason: spends model budget judging a chain; operator-only
  anonymize.py:check:
    cli: anonymize.py
    verb: check
    argv:
      - python3
      - <engine>/extensions/agi/bin/anonymize.py
      - check
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "text", "type": "str", "required": false, "choices": []}
      - {"name": "diff_file", "type": "str", "required": false, "choices": []}
    purpose: check bytes for physical-token leaks
    side_effects: read
    proposable: true
  anonymize.py:install-hook:
    cli: anonymize.py
    verb: install-hook
    argv:
      - python3
      - <engine>/extensions/agi/bin/anonymize.py
      - install-hook
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "hooks_dir", "type": "str", "required": false, "choices": []}
    purpose: install the anonymize git pre-commit hook
    side_effects: graph-write
    proposable: false
    reason: writes a git pre-commit hook; operator-only
  smoke:
    side_effects: graph-write
  goals-check:
    side_effects: graph-write
  grid-commit:
    side_effects: graph-write
  session-complete:
    side_effects: graph-write
    args:
      - {"name": "iter_n", "type": "str", "required": true, "choices": []}
  write:
    side_effects: graph-write
  mesh-local-town:
    side_effects: network
  mesh-core-town:
    side_effects: network
  mesh-encryption-town:
    side_effects: network
  mesh-silicon-town:
    side_effects: network
  mesh-gw:
    side_effects: network
    proposable: false
    reason: owner-ops overlay hub; agents have no business here
  branches.py::
    cli: branches.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/branches.py
    args:
      - {"name": "names", "type": "str", "required": false, "choices": []}
    purpose: parse branch names into the season grammar
    side_effects: read
    proposable: true
  completion.py::
    cli: completion.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/completion.py
      - <root>
      - <node_id>
    args:
      - {"name": "root", "type": "str", "required": true, "choices": []}
      - {"name": "node_id", "type": "str", "required": true, "choices": []}
    purpose: is the node finished? exit 0 complete, 1 not, 2 root unresolvable
    side_effects: read
    proposable: true
  geometry_config.py::
    cli: geometry_config.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/geometry_config.py
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: resolve the posts geometry config and its rows
    side_effects: read
    proposable: true
  spawn_gate.py:check:
    cli: spawn_gate.py
    verb: check
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_gate.py
      - check
      - "--type"
      - <node_type>
    args:
      - {"name": "node_type", "type": "str", "required": true, "choices": []}
      - {"name": "parents", "type": "str", "required": false, "choices": []}
      - {"name": "node_id", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "sets", "type": "str", "required": false, "choices": []}
      - {"name": "no_spawn_gate", "type": "bool", "required": false, "choices": []}
      - {"name": "season_parents", "type": "str", "required": false, "choices": []}
      - {"name": "current_season", "type": "str", "required": false, "choices": []}
    purpose: validate a spawn against the parent-shape gate; exit 2 on rejection
    side_effects: read
    proposable: true
  spawn_gate.py:rules:
    cli: spawn_gate.py
    verb: rules
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_gate.py
      - rules
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
    purpose: print the parent-shape rules and their schemas
    side_effects: read
    proposable: true
  towns.py::
    cli: towns.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/towns.py
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "tuples", "type": "bool", "required": false, "choices": []}
    purpose: load town:* super nodes and their derived branch names
    side_effects: read
    proposable: true
  briefing.py::
    cli: briefing.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/briefing.py
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "compact", "type": "bool", "required": false, "choices": []}
    purpose: the nine sections of briefing every agent is handed
    side_effects: read
    proposable: true
  dashboard.py::
    cli: dashboard.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/dashboard.py
    args:
      - {"name": "project", "type": "str", "required": false, "choices": []}
      - {"name": "watch", "type": "str", "required": false, "choices": []}
      - {"name": "no_color", "type": "bool", "required": false, "choices": []}
      - {"name": "section", "type": "str", "required": false, "choices": ["goals", "metrics", "health", "activity"]}
    purpose: read-only terminal view of the graph, built for a human
    side_effects: read
    proposable: true
  drift_check.py::
    cli: drift_check.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/drift_check.py
    args:
      - {"name": "start", "type": "str", "required": false, "choices": []}
      - {"name": "engine_dir", "type": "str", "required": false, "choices": []}
      - {"name": "strict", "type": "bool", "required": false, "choices": []}
    purpose: compare the pinned engine_commit to the engine HEAD; warn, never block
    side_effects: read
    proposable: true
  frontier.py:list:
    cli: frontier.py
    verb: list
    argv:
      - python3
      - <engine>/extensions/agi/bin/frontier.py
      - <cmd>
    args:
      - {"name": "cmd", "type": "str", "required": true, "choices": ["list"]}
      - {"name": "nodes", "type": "str", "required": false, "choices": []}
      - {"name": "count", "type": "bool", "required": false, "choices": []}
      - {"name": "schemas", "type": "str", "required": false, "choices": []}
      - {"name": "no_anchor", "type": "bool", "required": false, "choices": []}
    purpose: print every active chain tip and the successor types its schema allows
    side_effects: read
    proposable: true
  grid_coverage_check.py::
    cli: grid_coverage_check.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid_coverage_check.py
    args:
      - {"name": "engine", "type": "str", "required": false, "choices": []}
      - {"name": "exclusions", "type": "str", "required": false, "choices": []}
      - {"name": "verbose", "type": "bool", "required": false, "choices": []}
    purpose: every tracked engine file is inside the grid; exit nonzero on a remainder
    side_effects: read
    proposable: true
  failures.py:rates:
    cli: failures.py
    verb: rates
    argv:
      - python3
      - <engine>/extensions/agi/bin/failures.py
      - rates
      - <root>
    args:
      - {"name": "root", "type": "str", "required": true, "choices": []}
      - {"name": "by", "type": "str", "required": true, "choices": ["model", "role", "harness"]}
      - {"name": "in_path", "type": "str", "required": false, "choices": []}
    purpose: per-axis failure counts from the ledger; exit 2 if they do not sum
    side_effects: read
    proposable: true
  payload_boundary.py::
    cli: payload_boundary.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/payload_boundary.py
    args:
      - {"name": "repo", "type": "str", "required": false, "choices": []}
    purpose: classify every tracked engine file as a payload candidate (in) or out
    side_effects: read
    proposable: true
  plan_master.py:trend:
    cli: plan_master.py
    verb: trend
    argv:
      - python3
      - <engine>/extensions/agi/bin/plan_master.py
      - trend
    args:
      - {"name": "last", "type": "str", "required": false, "choices": []}
      - {"name": "tol", "type": "str", "required": false, "choices": []}
      - {"name": "log", "type": "str", "required": false, "choices": []}
    purpose: classify fixes_per_draft over the last N seat runs
    side_effects: read
    proposable: true
  reconciler.py::
    cli: reconciler.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/reconciler.py
      - <iter_dir>
    args:
      - {"name": "iter_dir", "type": "str", "required": true, "choices": []}
      - {"name": "style", "type": "str", "required": false, "choices": ["status", "ids"]}
    purpose: derive an iteration agent records against the process table; repairs nothing
    side_effects: read
    proposable: true
  rolslice.py::
    cli: rolslice.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/rolslice.py
    args:
      - {"name": "role", "type": "str", "required": false, "choices": []}
      - {"name": "tier", "type": "str", "required": false, "choices": []}
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "skill", "type": "str", "required": false, "choices": []}
      - {"name": "measure", "type": "bool", "required": false, "choices": []}
      - {"name": "all", "type": "bool", "required": false, "choices": []}
    purpose: slice SKILL.md for one role from the machine-readable hierarchy
    side_effects: read
    proposable: true
  seat_status.py::
    cli: seat_status.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/seat_status.py
    args:
      - {"name": "root", "type": "str", "required": false, "choices": []}
      - {"name": "list", "type": "bool", "required": false, "choices": []}
    purpose: one live read of every seat, the spawn budget and the telemetry roll-up
    side_effects: read
    proposable: true
  verify_unified.py::
    cli: verify_unified.py
    verb: ""
    argv:
      - python3
      - <engine>/extensions/agi/bin/verify_unified.py
      - "--before"
      - <before>
      - "--after"
      - <after>
    args:
      - {"name": "before", "type": "str", "required": true, "choices": []}
      - {"name": "after", "type": "str", "required": true, "choices": []}
      - {"name": "json", "type": "bool", "required": false, "choices": []}
    purpose: "before vs after: did the goal:g11 migration lose anything? read-only"
    side_effects: read
    proposable: true
  write_guard.py:check:
    cli: write_guard.py
    verb: check
    argv: [python3, <engine>/extensions/agi/bin/write_guard.py, check]
    args: []
    purpose: goal:g4.18 — unsanctioned node writes; silent is healthy
    side_effects: read
    proposable: true
  verify-suite:
    cli: verification.py
    verb: "--suite"
    argv: [python3, <engine>/extensions/agi/bin/verification.py, "--suite"]
    args: []
    reason: runs the whole engine suite under the one-runner suite lock -- opt-in, never proposed
    side_effects: read
    proposable: false
ordered:
  - verify
placement:
  defaults: true
  parents:
    kind: option
    flag: "--parent"
  start:
    kind: positional
  n:
    kind: option
    flag: "-n"
  from_id:
    kind: option
    flag: "--from"
  target:
    kind: positional
  all_:
    kind: switch
    flag: "--all"
  aud_round:
    kind: option
    flag: "--round"
  asker:
    kind: option
    flag: "--to"
  report_room:
    kind: option
    flag: "--room"
  dm_to:
    kind: option
    flag: "--to"
  v_round:
    kind: option
    flag: "--round"
  session_ref:
    kind: positional
  rotate.py:next.record:
    kind: const
    consts:
      ok: "--record-ok"
      fail: "--record-fail"
  workflow.py:status.key:
    kind: positional
  commands.py:propose.args_json:
    kind: option
    flag: "--args"
  locations.py:.explicit_iter:
    kind: option
    flag: "--iter"
  paths.py:audit.dir:
    kind: positional
  season.py:judge.judge_round:
    kind: option
    flag: "--round"
  zoom.py:.target:
    kind: option
    flag: "--target"
  sensei.py:propose.target:
    kind: option
    flag: "--target"
  sensei.py:calls.from_:
    kind: option
    flag: "--from"
  handoff.py:read.section:
    kind: positional
  branches.py:.names:
    kind: positional
  towns.py:.root:
    kind: positional
  spawn_gate.py:check.node_id:
    kind: option
    flag: "--id"
  spawn_gate.py:check.sets:
    kind: option
    flag: "--set"
  spawn_gate.py:check.season_parents:
    kind: option
    flag: "--season-parent"
  briefing.py:.root:
    kind: positional
  frontier.py:list.cmd:
    kind: positional
  failures.py:ledger.root:
    kind: positional
  failures.py:rates.root:
    kind: positional
  failures.py:sensei.root:
    kind: positional
  failures.py:ledger.in_path:
    kind: option
    flag: "--in"
  failures.py:rates.in_path:
    kind: option
    flag: "--in"
  failures.py:sensei.in_path:
    kind: option
    flag: "--in"
  glitch_master.py:format-record.iter_data:
    kind: option
    flag: "--iter"
  inject.py:.nodes_dir:
    kind: positional
  payload_boundary.py:.repo:
    kind: positional
  seat_status.py:.root:
    kind: positional
season: 1
status: active
tags:
  - geometry
  - command
  - structural
thought_session: sanctuary-director-genIII-L4
title: Standard command declaration
workflows:
  verify:
    - smoke
    - tests
    - goals-check
    - viewport-verify
    - grid-commit
  read:
    - links
    - schema
    - budget
    - credentials
    - secrets
    - crons
  see:
    - view
    - view-llm
    - view-both
    - write
  mesh:
    - mesh-local-town
    - mesh-core-town
    - mesh-encryption-town
    - mesh-silicon-town
    - mesh-gw
---
**The commands the engine cannot run without, declared once.** Every other
thing a run does is configuration — metrics, dispatch, harnesses, schemas,
cron cadences, the spawn budget, credentials. The commands an operator types
were declared nowhere: they lived in `CLAUDE.md` prose, `SKILL.md`'s table,
`QUICKSTART.md`, and whatever the last `HANDOFF.md` wrote down. Four copies,
drifting independently — `goal:s17`'s shape, and this repo has already paid
for it once with the ancestor walk restated eleven times.

## Scope, and it is narrow on purpose

The owner's words: *"not a command for every custom test call, just the
commands that are used during standard workflows."* **This is not a
shell-alias dumping ground.** A command that saves one person one keystroke
does not belong here. A command a cold session has to be *told* does.

Two workflows today, and they are the two halves `goal:g13` names:

- **`verify`** — the known-good sequence, in order. It was prose in
  `HANDOFF.md` §5, which is a file the next director deletes by default.
- **`read`** — the inspection surface. Each entry answers one question about
  the graph's health, and each belongs to a goal that made it answerable.

Only `verify` is listed under `ordered`. `read` is a **set**, and rendering it
as a sequence would put a false instruction into `INJECTION.md`, which every
agent is handed — the same class of mistake as the contradictory kid contract
`goal:s8` records.

## What reads this

`bin/commands.py` resolves and runs (`list`, `show`, `run`), and
`render-context.py` writes the set into `context/INJECTION.md` so **every
agent is handed the commands rather than expected to remember them**.

That second reader is why this node is allowed to exist. `goal:g2.25`'s rule
is that a `.geometry` node must be the input a code path resolves against,
never documentation about one — and a command table nothing reads is a fifth
copy of the prose rather than the deletion of the other four.

## `argv`, never a shell string

A shell string invites `&&`, pipes and quoting, and then this node stops being
data and becomes a program the resolver interprets. `goal:g2.19`'s argument one
layer down: the form a human reads and the form the engine runs must be the
same object. `<root>` and `<engine>` are substituted at resolve time, so no
absolute path — machine state `goal:g1.24` keeps out of the graph — appears
here.

## Mesh — the farm, reached through `<home>/work/.sanctuary`

**Owner order 2026-09-19 05:4xZ (thought-master pane):** a cold session must be
able to reach every box without being told how, and nothing that identifies a
box may reach the graph. The truth lives in **`~/work/.sanctuary/`** on every
box — `README.md` (where the iron is, rules, ops cheatsheet), `BOOTSTRAP.md`
(rebuild runbook), `hosts.json` (per-town cells), `ssh/config` + pinned
`ssh/known_hosts` + the mesh key. **That directory is never committed, never
synced; its only off-box copy is a Doppler bundle on the secrets hub.** The
graph carries only what is below: the alias, the label, and the one command.

| ssh alias (as in `ssh/config`) | graph label | what it is | reach |
|---|---|---|---|
| `local-town` | **GPU2070S** — the rig | 8 GB GPU, 16 threads, `/data` model store, llama-server `127.0.0.1:8080` on the box (`:18080` = the core-town tunnel view) | `ssh -F ~/work/.sanctuary/ssh/config local-town` |
| `core-town` (= `stream-town`) | **ARM4C** — this box | 4-core arm cloud, 23 GB, no GPU; the Prime and the masters live here | `ssh -F ~/work/.sanctuary/ssh/config core-town` |
| `encryption-town` | **CPU8G** — the secrets hub | 2c/4t, 8 GB, encrypted disk; the only box with Doppler; CPU-only rounds first | `ssh -F ~/work/.sanctuary/ssh/config encryption-town` |
| `silicon-town` | **EDGE** — the human gate | ephemeral arm64 VM on the owner laptop; the only writer of box truth | `ssh -F ~/work/.sanctuary/ssh/config silicon-town` (only while up) |
| `gw` | the overlay hub | owner ops only (lock/unlock a farm box) | agents never |

- **Anonymized on purpose, exactly as the mesh files say it should be:** no
  hostname, user, address, region or secret name appears here or in any node,
  dm or commit — the label (`CPU8G · GPU2070S · ARM4C · EDGE`) and the town
  alias are the whole vocabulary. Host keys are pinned in the mesh files; a
  mismatch means stop and ask, never `StrictHostKeyChecking=no`.
- `commands.py run mesh-<town>` opens the shell; the same `argv` with a
  trailing command runs it remotely (`ssh -F <cfg> local-town 'df -h /data'`).
  `<home>` resolves at run time, so no absolute path lives in the graph.
- Box-local shortcuts that exist only on ARM4C (`cpu8g`, `agi-run`) are
  conveniences over the same mesh; the `-F` form is the one that works from
  every box and every worktree.
- `bin/boxes.py` names THIS box from `AGI_BOX`; the mesh names the OTHER boxes.
  A box added to the farm gets a row here, a label, and nothing else.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
09-23 EF.21 kid a00-deb4f918: added the `manifest:` and `excluded:` frontmatter maps declaring the write.py verb surface (VERBS + create) so `commands.py manifest` has ONE typed choice set to print. The 25 `commands:` entries are untouched byte-for-byte (`manifest:` only ADDS metadata; the manifest action DERIVES cli/verb from a command's own argv when no override is present, so no existing entry needed editing). Deviation from the kid brief: it asked the manifest to contain no `<home>`, but the five mesh entries carry `<home>/work/.sanctuary/ssh/config` by design and the same brief forbids editing them -- `<home>` is a clone-agnostic placeholder resolved at run time, not a box value, so it stays. Frontmatter written directly because write.py has no verb for a nested map entry (patch = payload only); disclosed here, not silent.
<!-- THOUGHT:END -->
