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
    about: goal:g13 — every node's link resolves; broken_links must be 0
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
      - <iter>
      - "--dry-run"
    about: hypothesis:l4-session-dirs-come-home-when-the-round-is-done — bring a finished round's session dir home from a worktree, COPY-THEN-VERIFY; start every inspection with --dry-run
    workflow: read
  mesh-local-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - local-town
    about: "GPU2070S, the rig (local-town): model bytes under /data, llama-server on 127.0.0.1:18080 there, the town download queue. Append a command to run it remotely."
    workflow: mesh
  mesh-core-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - core-town
    about: "ARM4C, this box (core-town; the alias stream-town is the same box): the Prime, the masters, pi processes. From ARM4C itself this is a loopback."
    workflow: mesh
  mesh-encryption-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - encryption-town
    about: "CPU8G, the secrets hub (encryption-town): the only box with Doppler; CPU-only rounds go here first (agi-run = nice 19 / 4 threads / 4G). Never copy a secret off it."
    workflow: mesh
  mesh-silicon-town:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - silicon-town
    about: "EDGE, the human gate (silicon-town): an ephemeral VM, up only while the owner laptop is; the only writer of box truth. Reachable = the owner is present."
    workflow: mesh
  mesh-gw:
    argv:
      - ssh
      - "-F"
      - <home>/work/.sanctuary/ssh/config
      - gw
    about: "the overlay hub (gw): owner ops only (lock or unlock a farm box); agents have no business here -- listed so a cold session knows the name it sees in the mesh files."
    workflow: mesh
edited_by: thought-master
ordered:
  - verify
# The write.py verb surface (VERBS + create), declared once so
# `commands.py manifest` is the ONE choice set a proposer reads. Keys are
# `<cli>:<verb>`; `argv` keeps `<engine>`/`<node-id>` placeholders and never an
# absolute path. `args` is the schema a proposer validates against.
manifest:
  write.py:create:
    cli: write.py
    verb: create
    argv: [python3, <engine>/extensions/agi/bin/write.py, create, <type>, <slug>]
    args:
      - {name: 'type', type: str, required: true, choices: []}
      - {name: 'slug', type: str, required: true, choices: []}
      - {name: 'parent', type: list, required: false, choices: []}
      - {name: 'payload', type: str, required: false, choices: []}
      - {name: 'body_file', type: str, required: false, choices: []}
    purpose: mint a node of <type>/<slug>, linked to the schema's legal parents
    side_effects: graph-write
    proposable: true
  write.py:set:
    cli: write.py
    verb: set
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "set <key> <value>"]
    args:
      - {name: 'key', type: str, required: true, choices: []}
      - {name: 'value', type: str, required: true, choices: []}
    purpose: set a frontmatter key to a value, one typed coercion
    side_effects: graph-write
    proposable: true
  write.py:unset:
    cli: write.py
    verb: unset
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "unset <key>"]
    args:
      - {name: 'key', type: str, required: true, choices: []}
    purpose: remove a frontmatter key
    side_effects: graph-write
    proposable: true
  write.py:link:
    cli: write.py
    verb: link
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "link <ref>"]
    args:
      - {name: 'ref', type: str, required: true, choices: [self, parent, next]}
    purpose: add a parent/next edge reference to this node
    side_effects: graph-write
    proposable: true
  write.py:thought:
    cli: write.py
    verb: thought
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "thought <prose>"]
    args:
      - {name: 'prose', type: str, required: true, choices: []}
    purpose: replace the authored THOUGHT block with why this version differs
    side_effects: graph-write
    proposable: true
  write.py:note:
    cli: write.py
    verb: note
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "note <prose>"]
    args:
      - {name: 'prose', type: str, required: true, choices: []}
    purpose: append a whole-sentence Agent Notes line to the node
    side_effects: graph-write
    proposable: true
  write.py:sub:
    cli: write.py
    verb: sub
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "sub <old> => <new>"]
    args:
      - {name: 'old', type: str, required: true, choices: []}
      - {name: 'new', type: str, required: true, choices: []}
    purpose: replace exactly ONE literal occurrence anywhere in the node file (0 or 2+ matches refused, nothing written)
    side_effects: graph-write
    proposable: true
  write.py:sub!:
    cli: write.py
    verb: sub!
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "sub! <old> => <new>"]
    args:
      - {name: 'old', type: str, required: true, choices: []}
      - {name: 'new', type: str, required: true, choices: []}
    purpose: replace EVERY literal occurrence in the node file, the count printed
    side_effects: graph-write
    proposable: true
  write.py:payload:
    cli: write.py
    verb: payload
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "payload <path>"]
    args:
      - {name: 'path', type: str, required: true, choices: []}
    purpose: replace the bytes of the file this build node points at
    side_effects: graph-write
    proposable: true
  write.py:payload_text:
    cli: write.py
    verb: payload_text
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "payload_text <text>"]
    args:
      - {name: 'text', type: str, required: true, choices: []}
    purpose: replace the payload with literal text, no file needed
    side_effects: graph-write
    proposable: true
  write.py:read:
    cli: write.py
    verb: read
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "read <target> <N:M>"]
    args:
      - {name: 'target', type: str, required: true, choices: [body, payload]}
      - {name: 'range', type: str, required: true, choices: []}
    purpose: read a body or payload slice; replace's exact inverse
    side_effects: read
    proposable: true
  write.py:replace:
    cli: write.py
    verb: replace
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "replace <target> <N:M> -"]
    args:
      - {name: 'target', type: str, required: true, choices: [body, payload]}
      - {name: 'range', type: str, required: true, choices: []}
      - {name: 'source', type: str, required: true, choices: [stdin]}
    purpose: replace a body or payload slice with text on stdin
    side_effects: graph-write
    proposable: true
  write.py:adopt:
    cli: write.py
    verb: adopt
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, adopt]
    args: []
    purpose: adopt the current on-disk payload/body bytes as this node's version
    side_effects: graph-write
    proposable: true
  cli.py:branch-reshuffle: {cli: cli.py, verb: branch-reshuffle, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'branch-reshuffle'], args: [{name: 'dry_run', type: bool, required: false, choices: []}, {name: 'apply', type: bool, required: false, choices: []}, {name: 'delete_old', type: bool, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}, {name: 'kinds', type: str, required: false, choices: []}, {name: 'season', type: str, required: false, choices: []}, {name: 'plan_out', type: str, required: false, choices: []}], purpose: 'cli.py branch-reshuffle', side_effects: graph-write, proposable: true}
  cli.py:claim: {cli: cli.py, verb: claim, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'claim'], args: [{name: 'node_id', type: str, required: true, choices: []}, {name: 'session', type: str, required: true, choices: []}], purpose: 'cli.py claim', side_effects: graph-write, proposable: true}
  cli.py:detect-stale: {cli: cli.py, verb: detect-stale, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'detect-stale'], args: [{name: 'threshold_seconds', type: str, required: false, choices: []}], purpose: 'cli.py detect-stale', side_effects: read, proposable: true}
  cli.py:done: {cli: cli.py, verb: done, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'done', '<iter_n>', '<agent_id>'], args: [{name: 'iter_n', type: str, required: true, choices: []}, {name: 'agent_id', type: str, required: true, choices: []}, {name: 'verdict', type: str, required: true, choices: []}, {name: 'confidence', type: str, required: false, choices: []}, {name: 'node_id', type: str, required: false, choices: []}, {name: 'parent', type: str, required: false, choices: []}, {name: 'notes', type: str, required: false, choices: []}, {name: 'next_edge', type: str, required: false, choices: []}, {name: 'push_further', type: str, required: false, choices: []}, {name: 'owns', type: str, required: false, choices: []}, {name: 'evidence_runs', type: str, required: false, choices: []}, {name: 'no_evidence_gate', type: bool, required: false, choices: []}, {name: 'no_spawn_gate', type: bool, required: false, choices: []}, {name: 'probes', type: str, required: false, choices: []}, {name: 'deliverables', type: str, required: false, choices: []}, {name: 'salvage', type: bool, required: false, choices: []}, {name: 'dry_run', type: bool, required: false, choices: []}], purpose: 'cli.py done', side_effects: graph-write, proposable: true}
  cli.py:loop-prune: {cli: cli.py, verb: loop-prune, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'loop-prune'], args: [{name: 'apply', type: bool, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'cli.py loop-prune', side_effects: graph-write, proposable: true}
  cli.py:pending: {cli: cli.py, verb: pending, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'pending', '<iter_n>', '<agent_id>'], args: [{name: 'iter_n', type: str, required: true, choices: []}, {name: 'agent_id', type: str, required: true, choices: []}, {name: 'reason', type: str, required: true, choices: []}], purpose: 'cli.py pending', side_effects: graph-write, proposable: true}
  cli.py:post-rename: {cli: cli.py, verb: post-rename, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'post-rename'], args: [{name: 'dry_run', type: bool, required: false, choices: []}, {name: 'apply', type: bool, required: false, choices: []}, {name: 'delete_old', type: bool, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'cli.py post-rename', side_effects: graph-write, proposable: true}
  cli.py:reclaim: {cli: cli.py, verb: reclaim, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'reclaim'], args: [{name: 'node_id', type: str, required: true, choices: []}, {name: 'session', type: str, required: true, choices: []}], purpose: 'cli.py reclaim', side_effects: graph-write, proposable: true}
  cli.py:scaffold: {cli: cli.py, verb: scaffold, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'scaffold', '<iter_n>', '<agent_id>'], args: [{name: 'iter_n', type: str, required: true, choices: []}, {name: 'agent_id', type: str, required: true, choices: []}, {name: 'node_type', type: str, required: true, choices: ['idea', 'hypothesis', 'task', 'experiment', 'verdict', 'mvp', 'outcome', 'bigger_outcome', 'overview', 'vision', 'bigger-outcome', 'app-purpose', 'app_purpose']}, {name: 'parents', type: str, required: false, choices: []}, {name: 'slug', type: str, required: true, choices: []}, {name: 'no_spawn_gate', type: bool, required: false, choices: []}], purpose: 'cli.py scaffold', side_effects: graph-write, proposable: true}
  cli.py:scope-check: {cli: cli.py, verb: scope-check, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'scope-check'], args: [{name: 'agent_id', type: str, required: false, choices: []}, {name: 'own', type: str, required: false, choices: []}], purpose: 'cli.py scope-check', side_effects: read, proposable: true}
  cli.py:session-complete: {cli: cli.py, verb: session-complete, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'session-complete', '<iter_n>'], args: [{name: 'iter_n', type: str, required: true, choices: []}, {name: 'worktree', type: str, required: false, choices: []}, {name: 'dry_run', type: bool, required: false, choices: []}], purpose: 'cli.py session-complete', side_effects: graph-write, proposable: true}
  cli.py:status: {cli: cli.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'status', '<iter_n>'], args: [{name: 'iter_n', type: str, required: true, choices: []}], purpose: 'cli.py status', side_effects: read, proposable: true}
  cli.py:trimguard: {cli: cli.py, verb: trimguard, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'trimguard'], args: [], purpose: 'cli.py trimguard', side_effects: graph-write, proposable: true}
  cli.py:wait: {cli: cli.py, verb: wait, argv: ['python3', '<engine>/extensions/agi/bin/cli.py', 'wait', '<iter_n>'], args: [{name: 'iter_n', type: str, required: true, choices: []}, {name: 'agent', type: str, required: false, choices: []}, {name: 'max_seconds', type: str, required: false, choices: []}], purpose: 'cli.py wait', side_effects: read, proposable: true}
  crons.py:apply: {cli: crons.py, verb: apply, argv: ['python3', '<engine>/extensions/agi/bin/crons.py', 'apply'], args: [{name: 'root', type: str, required: false, choices: []}, {name: 'crontab_file', type: str, required: false, choices: []}, {name: 'unit_dir', type: str, required: false, choices: []}, {name: 'dry_run', type: bool, required: false, choices: []}], purpose: 'crons.py apply', side_effects: graph-write, proposable: true}
  crons.py:audit: {cli: crons.py, verb: audit, argv: ['python3', '<engine>/extensions/agi/bin/crons.py', 'audit'], args: [{name: 'root', type: str, required: false, choices: []}, {name: 'crontab_file', type: str, required: false, choices: []}, {name: 'unit_dir', type: str, required: false, choices: []}], purpose: 'crons.py audit', side_effects: graph-write, proposable: true}
  crons.py:remove: {cli: crons.py, verb: remove, argv: ['python3', '<engine>/extensions/agi/bin/crons.py', 'remove'], args: [{name: 'root', type: str, required: false, choices: []}, {name: 'crontab_file', type: str, required: false, choices: []}, {name: 'unit_dir', type: str, required: false, choices: []}], purpose: 'crons.py remove', side_effects: graph-write, proposable: true}
  crons.py:show: {cli: crons.py, verb: show, argv: ['python3', '<engine>/extensions/agi/bin/crons.py', 'show'], args: [{name: 'root', type: str, required: false, choices: []}, {name: 'crontab_file', type: str, required: false, choices: []}, {name: 'unit_dir', type: str, required: false, choices: []}], purpose: 'crons.py show', side_effects: graph-write, proposable: true}
  envfile.py:: {cli: envfile.py, verb: , argv: ['python3', '<engine>/extensions/agi/bin/envfile.py'], args: [{name: 'start', type: str, required: false, choices: []}, {name: 'what', type: str, required: false, choices: ['env-file', 'template', 'node']}, {name: 'check', type: bool, required: false, choices: []}, {name: 'json', type: bool, required: false, choices: []}, {name: 'set', type: str, required: false, choices: []}], purpose: 'envfile.py', side_effects: graph-write, proposable: true}
  grid.py:commit: {cli: grid.py, verb: commit, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'commit', '<files...>'], args: [{name: 'files', type: str, required: true, choices: []}, {name: 'all', type: bool, required: false, choices: []}, {name: 'session', type: str, required: false, choices: []}, {name: 'prefix', type: str, required: false, choices: []}, {name: 'allow_branch', type: bool, required: false, choices: []}, {name: 'lock_wait', type: str, required: false, choices: []}], purpose: 'grid.py commit', side_effects: graph-write, proposable: true}
  grid.py:cron: {cli: grid.py, verb: cron, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'cron', '<action>'], args: [{name: 'action', type: str, required: true, choices: ['install', 'show', 'remove']}, {name: 'snapshot_mins', type: str, required: false, choices: []}, {name: 'publish_engine', type: bool, required: false, choices: []}], purpose: 'grid.py cron', side_effects: graph-write, proposable: true}
  grid.py:diff: {cli: grid.py, verb: diff, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'diff', '<node_id>'], args: [{name: 'node_id', type: str, required: true, choices: []}, {name: 'back', type: str, required: false, choices: []}], purpose: 'grid.py diff', side_effects: read, proposable: true}
  grid.py:init: {cli: grid.py, verb: init, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'init'], args: [], purpose: 'grid.py init', side_effects: graph-write, proposable: true}
  grid.py:log: {cli: grid.py, verb: log, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'log', '<node_id>'], args: [{name: 'node_id', type: str, required: true, choices: []}, {name: 'n', type: str, required: false, choices: []}], purpose: 'grid.py log', side_effects: read, proposable: true}
  grid.py:payload: {cli: grid.py, verb: payload, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'payload', '<node_id>'], args: [{name: 'node_id', type: str, required: true, choices: []}, {name: 'version', type: str, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}], purpose: 'grid.py payload', side_effects: read, proposable: true}
  grid.py:status: {cli: grid.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'status'], args: [], purpose: 'grid.py status', side_effects: read, proposable: true}
  grid.py:versions: {cli: grid.py, verb: versions, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'versions', '<node_id>'], args: [{name: 'node_id', type: str, required: true, choices: []}], purpose: 'grid.py versions', side_effects: read, proposable: true}
  links.py:links: {cli: links.py, verb: links, argv: ['python3', '<engine>/extensions/agi/bin/links.py', 'links'], args: [{name: 'action', type: str, required: false, choices: ['links', 'schema', 'roles']}, {name: 'root', type: str, required: false, choices: []}, {name: 'broken', type: bool, required: false, choices: []}, {name: 'fix', type: bool, required: false, choices: []}], purpose: 'links.py links', side_effects: read, proposable: true}
  links.py:roles: {cli: links.py, verb: roles, argv: ['python3', '<engine>/extensions/agi/bin/links.py', 'roles'], args: [{name: 'action', type: str, required: false, choices: ['links', 'schema', 'roles']}, {name: 'root', type: str, required: false, choices: []}, {name: 'broken', type: bool, required: false, choices: []}, {name: 'fix', type: bool, required: false, choices: []}], purpose: 'links.py roles', side_effects: read, proposable: true}
  links.py:schema: {cli: links.py, verb: schema, argv: ['python3', '<engine>/extensions/agi/bin/links.py', 'schema'], args: [{name: 'action', type: str, required: false, choices: ['links', 'schema', 'roles']}, {name: 'root', type: str, required: false, choices: []}, {name: 'broken', type: bool, required: false, choices: []}, {name: 'fix', type: bool, required: false, choices: []}], purpose: 'links.py schema', side_effects: read, proposable: true}
  provisioning.py:capture: {cli: provisioning.py, verb: capture, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'capture'], args: [{name: 'action', type: str, required: false, choices: ['status', 'list', 'reap', 'capture', 'diff', 'spend']}, {name: 'root', type: str, required: false, choices: []}, {name: 'yes', type: bool, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}, {name: 'prev', type: str, required: false, choices: []}], purpose: 'provisioning.py capture', side_effects: graph-write, proposable: true}
  provisioning.py:diff: {cli: provisioning.py, verb: diff, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'diff'], args: [{name: 'action', type: str, required: false, choices: ['status', 'list', 'reap', 'capture', 'diff', 'spend']}, {name: 'root', type: str, required: false, choices: []}, {name: 'yes', type: bool, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}, {name: 'prev', type: str, required: false, choices: []}], purpose: 'provisioning.py diff', side_effects: read, proposable: true}
  provisioning.py:list: {cli: provisioning.py, verb: list, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'list'], args: [{name: 'action', type: str, required: false, choices: ['status', 'list', 'reap', 'capture', 'diff', 'spend']}, {name: 'root', type: str, required: false, choices: []}, {name: 'yes', type: bool, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}, {name: 'prev', type: str, required: false, choices: []}], purpose: 'provisioning.py list', side_effects: read, proposable: true}
  provisioning.py:spend: {cli: provisioning.py, verb: spend, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'spend'], args: [{name: 'action', type: str, required: false, choices: ['status', 'list', 'reap', 'capture', 'diff', 'spend']}, {name: 'root', type: str, required: false, choices: []}, {name: 'yes', type: bool, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}, {name: 'prev', type: str, required: false, choices: []}], purpose: 'provisioning.py spend', side_effects: read, proposable: true}
  provisioning.py:status: {cli: provisioning.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'status'], args: [{name: 'action', type: str, required: false, choices: ['status', 'list', 'reap', 'capture', 'diff', 'spend']}, {name: 'root', type: str, required: false, choices: []}, {name: 'yes', type: bool, required: false, choices: []}, {name: 'out', type: str, required: false, choices: []}, {name: 'prev', type: str, required: false, choices: []}], purpose: 'provisioning.py status', side_effects: read, proposable: true}
  rotate.py:autopsy: {cli: rotate.py, verb: autopsy, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'autopsy'], args: [{name: 'seat', type: str, required: true, choices: []}, {name: 'pid', type: str, required: false, choices: []}, {name: 'registry_dir', type: str, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'rotate.py autopsy', side_effects: read, proposable: true}
  rotate.py:bootstrap-block: {cli: rotate.py, verb: bootstrap-block, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'bootstrap-block'], args: [{name: 'seat', type: str, required: true, choices: []}, {name: 'root', type: str, required: false, choices: []}, {name: 'commit', type: str, required: false, choices: []}, {name: 'bounds', type: str, required: false, choices: []}, {name: 'json', type: bool, required: false, choices: []}, {name: 'quiet', type: bool, required: false, choices: []}], purpose: 'rotate.py bootstrap-block', side_effects: graph-write, proposable: true}
  rotate.py:handoff: {cli: rotate.py, verb: handoff, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'handoff'], args: [{name: 'driven', type: bool, required: false, choices: []}, {name: 'seat', type: str, required: false, choices: []}, {name: 'field', type: str, required: false, choices: []}, {name: 'dry_run', type: bool, required: false, choices: []}], purpose: 'rotate.py handoff', side_effects: graph-write, proposable: true}
  rotate.py:harvest-table: {cli: rotate.py, verb: harvest-table, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'harvest-table'], args: [{name: 'seat', type: str, required: false, choices: []}, {name: 'round', type: str, required: false, choices: []}, {name: 'all_live', type: bool, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'rotate.py harvest-table', side_effects: read, proposable: true}
  rotate.py:meter: {cli: rotate.py, verb: meter, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'meter'], args: [{name: 'session_log', type: str, required: false, choices: []}, {name: 'check', type: bool, required: false, choices: []}, {name: 'seat', type: str, required: false, choices: []}, {name: 'pin', type: str, required: false, choices: []}], purpose: 'rotate.py meter', side_effects: read, proposable: true}
  rotate.py:next: {cli: rotate.py, verb: next, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'next'], args: [{name: 'seat', type: str, required: true, choices: []}, {name: 'role', type: str, required: false, choices: []}, {name: 'template', type: str, required: false, choices: []}, {name: 'record', type: str, required: false, choices: []}, {name: 'record', type: str, required: false, choices: []}, {name: 'json', type: bool, required: false, choices: []}, {name: 'gen', type: str, required: false, choices: []}, {name: 'succ_name', type: str, required: false, choices: []}, {name: 'tmux_session', type: str, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'rotate.py next', side_effects: read, proposable: true}
  rotate.py:seq: {cli: rotate.py, verb: seq, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'seq'], args: [], purpose: 'rotate.py seq', side_effects: read, proposable: true}
  rotate.py:status: {cli: rotate.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'status'], args: [{name: 'seats', type: bool, required: false, choices: []}, {name: 'seat', type: str, required: false, choices: []}, {name: 'record', type: str, required: false, choices: []}, {name: 'wait', type: str, required: false, choices: []}], purpose: 'rotate.py status', side_effects: read, proposable: true}
  send.py:ask: {cli: send.py, verb: ask, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'ask', '<text...>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'to', type: str, required: true, choices: []}, {name: 'text', type: str, required: true, choices: []}], purpose: 'send.py ask', side_effects: comms, proposable: true}
  send.py:audience: {cli: send.py, verb: audience, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'audience', '<target>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'target', type: str, required: true, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'morals', type: bool, required: false, choices: []}, {name: 'aud_round', type: str, required: false, choices: []}, {name: 'decision', type: str, required: false, choices: []}], purpose: 'send.py audience', side_effects: comms, proposable: true}
  send.py:escalate: {cli: send.py, verb: escalate, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'escalate', '<text...>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'to', type: str, required: false, choices: []}, {name: 'concern', type: str, required: false, choices: []}, {name: 'text', type: str, required: true, choices: []}], purpose: 'send.py escalate', side_effects: comms, proposable: true}
  send.py:keygen: {cli: send.py, verb: keygen, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'keygen'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'seat', type: str, required: false, choices: []}, {name: 'scheme', type: str, required: false, choices: []}, {name: 'all_live', type: bool, required: false, choices: []}, {name: 'onboard', type: str, required: false, choices: []}, {name: 'sponsor', type: str, required: false, choices: []}, {name: 'sponsor_sig', type: str, required: false, choices: []}, {name: 'sponsor_sign', type: str, required: false, choices: []}, {name: 'charter_hash', type: str, required: false, choices: []}, {name: 'budget', type: str, required: false, choices: []}], purpose: 'send.py keygen', side_effects: comms, proposable: true}
  send.py:peek: {cli: send.py, verb: peek, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'peek'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'target', type: str, required: false, choices: []}, {name: 'room', type: str, required: false, choices: []}, {name: 'dm', type: str, required: false, choices: []}, {name: 'since', type: str, required: false, choices: []}, {name: 'all_', type: bool, required: false, choices: []}, {name: 'me', type: str, required: false, choices: []}, {name: 'wrap', type: str, required: false, choices: []}], purpose: 'send.py peek', side_effects: read, proposable: true}
  send.py:prime-excluded: {cli: send.py, verb: prime-excluded, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'prime-excluded'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'round', type: str, required: true, choices: []}], purpose: 'send.py prime-excluded', side_effects: comms, proposable: true}
  send.py:read: {cli: send.py, verb: read, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'read'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'target', type: str, required: false, choices: []}, {name: 'room', type: str, required: false, choices: []}, {name: 'dm', type: str, required: false, choices: []}, {name: 'since', type: str, required: false, choices: []}, {name: 'all_', type: bool, required: false, choices: []}, {name: 'me', type: str, required: false, choices: []}, {name: 'wrap', type: str, required: false, choices: []}, {name: 'box_local', type: bool, required: false, choices: []}], purpose: 'send.py read', side_effects: read, proposable: true}
  send.py:report: {cli: send.py, verb: report, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'report', '<text...>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'asker', type: str, required: false, choices: []}, {name: 'report_room', type: str, required: false, choices: []}, {name: 'ref', type: str, required: true, choices: []}, {name: 'text', type: str, required: true, choices: []}], purpose: 'send.py report', side_effects: comms, proposable: true}
  send.py:rooms: {cli: send.py, verb: rooms, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'rooms'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'me', type: str, required: false, choices: []}], purpose: 'send.py rooms', side_effects: read, proposable: true}
  send.py:send: {cli: send.py, verb: send, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'send', '<send_args...>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'send_args', type: str, required: true, choices: []}, {name: 'dm_to', type: str, required: false, choices: []}, {name: 'room', type: str, required: false, choices: []}, {name: 'quote_harness', type: bool, required: false, choices: []}], purpose: 'send.py send', side_effects: comms, proposable: true}
  send.py:status: {cli: send.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'status', '<target>'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'target', type: str, required: true, choices: []}], purpose: 'send.py status', side_effects: read, proposable: true}
  send.py:veto: {cli: send.py, verb: veto, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'veto'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'scope', type: str, required: false, choices: []}, {name: 'answer', type: str, required: false, choices: []}, {name: 'room', type: str, required: false, choices: []}, {name: 'file', type: str, required: false, choices: []}], purpose: 'send.py veto', side_effects: comms, proposable: true}
  send.py:vote: {cli: send.py, verb: vote, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'vote'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'room', type: str, required: false, choices: []}, {name: 'target', type: str, required: true, choices: []}, {name: 'vision', type: str, required: true, choices: []}, {name: 'alignment', type: str, required: true, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'morals', type: bool, required: false, choices: []}, {name: 'v_round', type: str, required: false, choices: []}], purpose: 'send.py vote', side_effects: comms, proposable: true}
  send.py:wake: {cli: send.py, verb: wake, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'wake'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'target', type: str, required: false, choices: []}, {name: 'all_local', type: bool, required: false, choices: []}], purpose: 'send.py wake', side_effects: comms, proposable: true}
  send.py:whois: {cli: send.py, verb: whois, argv: ['python3', '<engine>/extensions/agi/bin/send.py', 'whois'], args: [{name: 'from_id', type: str, required: false, choices: []}, {name: 'comms_root', type: str, required: false, choices: []}, {name: 'session_ref', type: str, required: false, choices: []}, {name: 'key', type: str, required: false, choices: []}, {name: 'seat', type: str, required: false, choices: []}, {name: 'claim', type: str, required: false, choices: []}, {name: 'source', type: str, required: false, choices: []}, {name: 'no_fetch', type: bool, required: false, choices: []}, {name: 'sig', type: str, required: false, choices: []}, {name: 'msg', type: str, required: false, choices: []}], purpose: 'send.py whois', side_effects: read, proposable: true}
  snapshot-goals.py:: {cli: snapshot-goals.py, verb: , argv: ['python3', '<engine>/extensions/agi/bin/snapshot-goals.py'], args: [{name: 'strict', type: bool, required: false, choices: []}, {name: 'strict_goals', type: bool, required: false, choices: []}, {name: 'project', type: str, required: false, choices: []}, {name: 'render', type: bool, required: false, choices: []}, {name: 'check', type: bool, required: false, choices: []}, {name: 'from_doc', type: bool, required: false, choices: []}], purpose: 'snapshot-goals.py', side_effects: graph-write, proposable: true}
  spawn_budget.py:pause: {cli: spawn_budget.py, verb: pause, argv: ['python3', '<engine>/extensions/agi/bin/spawn_budget.py', 'pause'], args: [{name: 'action', type: str, required: false, choices: ['status', 'sweep', 'pause', 'resume']}, {name: 'root', type: str, required: false, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'actor', type: str, required: false, choices: []}, {name: 'iter', type: str, required: false, choices: []}, {name: 'wait', type: bool, required: false, choices: []}, {name: 'timeout', type: str, required: false, choices: []}], purpose: 'spawn_budget.py pause', side_effects: graph-write, proposable: true}
  spawn_budget.py:resume: {cli: spawn_budget.py, verb: resume, argv: ['python3', '<engine>/extensions/agi/bin/spawn_budget.py', 'resume'], args: [{name: 'action', type: str, required: false, choices: ['status', 'sweep', 'pause', 'resume']}, {name: 'root', type: str, required: false, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'actor', type: str, required: false, choices: []}, {name: 'iter', type: str, required: false, choices: []}, {name: 'wait', type: bool, required: false, choices: []}, {name: 'timeout', type: str, required: false, choices: []}], purpose: 'spawn_budget.py resume', side_effects: graph-write, proposable: true}
  spawn_budget.py:status: {cli: spawn_budget.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/spawn_budget.py', 'status'], args: [{name: 'action', type: str, required: false, choices: ['status', 'sweep', 'pause', 'resume']}, {name: 'root', type: str, required: false, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'actor', type: str, required: false, choices: []}, {name: 'iter', type: str, required: false, choices: []}, {name: 'wait', type: bool, required: false, choices: []}, {name: 'timeout', type: str, required: false, choices: []}], purpose: 'spawn_budget.py status', side_effects: read, proposable: true}
  spawn_budget.py:sweep: {cli: spawn_budget.py, verb: sweep, argv: ['python3', '<engine>/extensions/agi/bin/spawn_budget.py', 'sweep'], args: [{name: 'action', type: str, required: false, choices: ['status', 'sweep', 'pause', 'resume']}, {name: 'root', type: str, required: false, choices: []}, {name: 'reason', type: str, required: false, choices: []}, {name: 'actor', type: str, required: false, choices: []}, {name: 'iter', type: str, required: false, choices: []}, {name: 'wait', type: bool, required: false, choices: []}, {name: 'timeout', type: str, required: false, choices: []}], purpose: 'spawn_budget.py sweep', side_effects: graph-write, proposable: true}
  viewport.py:: {cli: viewport.py, verb: , argv: ['python3', '<engine>/extensions/agi/bin/viewport.py'], args: [{name: 'project', type: str, required: false, choices: []}, {name: 'anchor', type: str, required: false, choices: []}, {name: 'depth', type: str, required: false, choices: []}, {name: 'emit', type: str, required: false, choices: ['human', 'llm', 'both']}, {name: 'verify', type: bool, required: false, choices: []}, {name: 'iter', type: str, required: false, choices: []}, {name: 'live', type: bool, required: false, choices: []}, {name: 'top', type: str, required: false, choices: []}, {name: 'left', type: str, required: false, choices: []}, {name: 'height', type: str, required: false, choices: []}, {name: 'width', type: str, required: false, choices: []}, {name: 'theme', type: str, required: false, choices: ['graph', 'keep']}, {name: 'layer', type: str, required: false, choices: ['graph', 'hierarchy']}], purpose: 'viewport.py', side_effects: read, proposable: true}
  workflow.py:author: {cli: workflow.py, verb: author, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'author', '<name>'], args: [{name: 'name', type: str, required: true, choices: []}, {name: 'stages', type: str, required: false, choices: []}, {name: 'json', type: str, required: false, choices: []}, {name: 'stdin', type: bool, required: false, choices: []}, {name: 'note', type: str, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py author', side_effects: graph-write, proposable: true}
  workflow.py:link: {cli: workflow.py, verb: link, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'link'], args: [{name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py link', side_effects: graph-write, proposable: true}
  workflow.py:list: {cli: workflow.py, verb: list, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'list'], args: [{name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py list', side_effects: read, proposable: true}
  workflow.py:note: {cli: workflow.py, verb: note, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'note', '<run_key>'], args: [{name: 'run_key', type: str, required: true, choices: []}, {name: 'harness_id', type: str, required: true, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py note', side_effects: graph-write, proposable: true}
  workflow.py:register: {cli: workflow.py, verb: register, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'register', '<name>'], args: [{name: 'name', type: str, required: true, choices: []}, {name: 'script', type: str, required: true, choices: []}, {name: 'from_run', type: str, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py register', side_effects: graph-write, proposable: true}
  workflow.py:run: {cli: workflow.py, verb: run, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'run', '<name>'], args: [{name: 'name', type: str, required: true, choices: []}, {name: 'harness', type: str, required: false, choices: []}, {name: 'args', type: str, required: false, choices: []}, {name: 'dry_run', type: bool, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py run', side_effects: spawn, proposable: true}
  workflow.py:status: {cli: workflow.py, verb: status, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'status'], args: [{name: 'key', type: str, required: false, choices: []}, {name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py status', side_effects: read, proposable: true}
  workflow.py:validate: {cli: workflow.py, verb: validate, argv: ['python3', '<engine>/extensions/agi/bin/workflow.py', 'validate'], args: [{name: 'root', type: str, required: false, choices: []}], purpose: 'workflow.py validate', side_effects: read, proposable: true}
  # Legacy `commands:` entries whose KID 1 default (read) is wrong. Kept
  # keyed by command NAME (not cli:verb) so manifest() applies them to the
  # command the operator actually types; argv stays untouched.
  smoke: {side_effects: graph-write}
  goals-check: {side_effects: graph-write}
  grid-commit: {side_effects: graph-write}
  session-complete: {side_effects: graph-write}
  write: {side_effects: graph-write}
  mesh-local-town: {side_effects: network}
  mesh-core-town: {side_effects: network}
  mesh-encryption-town: {side_effects: network}
  mesh-silicon-town: {side_effects: network}
  mesh-gw: {side_effects: network}
# Excluded verbs are declared BY NAME with a reason and proposable false, so a
# drift test can tell "we chose not to expose this" from "we forgot it".
excluded:
  write.py:patch:
    cli: write.py
    verb: patch
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "patch -"]
    reason: reads a unified diff on stdin (fail-closed) -- not expressible as argv
    side_effects: graph-write
    proposable: false
  write.py:body_patch:
    cli: write.py
    verb: body_patch
    argv: [python3, <engine>/extensions/agi/bin/write.py, <node-id>, "body_patch -"]
    reason: reads a diff on stdin onto the node BODY -- not expressible as argv
    side_effects: graph-write
    proposable: false
  dispatch.py:: {cli: dispatch.py, verb: , argv: ['python3', '<engine>/extensions/agi/bin/dispatch.py', '<project_root>', '<iter_n>'], reason: 'spawns paid model agents; operator-only, never proposed', side_effects: spawn, proposable: false}
  grid.py:checkout: {cli: grid.py, verb: checkout, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'checkout', '<node_ids...>'], reason: 'destructive: overwrites the working tree (retired, never run)', side_effects: destructive, proposable: false}
  grid.py:migrate-mint-refs: {cli: grid.py, verb: migrate-mint-refs, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'migrate-mint-refs'], reason: 'destructive: rewrites grid refs (--write)', side_effects: destructive, proposable: false}
  grid.py:migrate-refs: {cli: grid.py, verb: migrate-refs, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'migrate-refs'], reason: 'destructive: rewrites grid refs (--write)', side_effects: destructive, proposable: false}
  grid.py:migrate-trunk: {cli: grid.py, verb: migrate-trunk, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'migrate-trunk'], reason: 'destructive: rewrites grid refs (--write)', side_effects: destructive, proposable: false}
  grid.py:sync: {cli: grid.py, verb: sync, argv: ['python3', '<engine>/extensions/agi/bin/grid.py', 'sync'], reason: 'network: pushes refs to a remote', side_effects: network, proposable: false}
  provisioning.py:reap: {cli: provisioning.py, verb: reap, argv: ['python3', '<engine>/extensions/agi/bin/provisioning.py', 'reap'], reason: 'destructive: deletes keys (--yes)', side_effects: destructive, proposable: false}
  rotate.py:ack: {cli: rotate.py, verb: ack, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'ack', '<answer>'], reason: 'acknowledges a seat handoff; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:alarms: {cli: rotate.py, verb: alarms, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'alarms'], reason: 'seat alarm watcher; long-running, never-run', side_effects: comms, proposable: false}
  rotate.py:closeout: {cli: rotate.py, verb: closeout, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'closeout'], reason: 'closes out a seat; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:complete: {cli: rotate.py, verb: complete, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'complete'], reason: 'completes a worktree round; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:first-decision: {cli: rotate.py, verb: first-decision, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'first-decision'], reason: 'records a seat first decision; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:launch-wrapper: {cli: rotate.py, verb: launch-wrapper, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'launch-wrapper', '<child>'], reason: 'launches a seat wrapper; never-run', side_effects: spawn, proposable: false}
  rotate.py:loop: {cli: rotate.py, verb: loop, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'loop'], reason: 'super-ralph rotation loop; never-run', side_effects: spawn, proposable: false}
  rotate.py:merge-up: {cli: rotate.py, verb: merge-up, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'merge-up'], reason: 'merges a post up the tree; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:migrate: {cli: rotate.py, verb: migrate, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'migrate'], reason: 'destructive: migrates posts/refs', side_effects: destructive, proposable: false}
  rotate.py:prepare: {cli: rotate.py, verb: prepare, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'prepare'], reason: 'arms a rotation; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:rename-post: {cli: rotate.py, verb: rename-post, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'rename-post', '<old_name>', '<new_name>'], reason: 'renames a post; operator-only', side_effects: graph-write, proposable: false}
  rotate.py:rotate: {cli: rotate.py, verb: rotate, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'rotate'], reason: 'rotates a live seat; never-run by a proposer', side_effects: spawn, proposable: false}
  rotate.py:rotate-self: {cli: rotate.py, verb: rotate-self, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'rotate-self'], reason: 'self-rotation; never-run by a proposer', side_effects: spawn, proposable: false}
  rotate.py:seats-launch: {cli: rotate.py, verb: seats-launch, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'seats-launch'], reason: 'launches seats in tmux; never-run', side_effects: spawn, proposable: false}
  rotate.py:spawn: {cli: rotate.py, verb: spawn, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'spawn'], reason: 'spawns a successor process; never-run by a proposer', side_effects: spawn, proposable: false}
  rotate.py:tile: {cli: rotate.py, verb: tile, argv: ['python3', '<engine>/extensions/agi/bin/rotate.py', 'tile'], reason: 'lays out tmux tiles; never-run', side_effects: spawn, proposable: false}
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
