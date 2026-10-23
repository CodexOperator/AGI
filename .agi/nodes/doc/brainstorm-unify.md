---
id: doc:brainstorm-unify
mint_id: b9610b1c803543b8b0c450714da00b31
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
season: 3
tags:
  - brainstorm
  - reference
title: "doc:brainstorm-unify -- the owner's 10-22/23 Fable brainstorm: one matrix family for the graph interface (§0-§39; reference, never placement)"
town: core
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 10-23, Wave 0 of the owner's hand-off): the Fable fork's brainstorm, committed whole as REFERENCE (§38 invariant 1: a doc node is never placement; an owner ask is placed only when its leaf, idea or decision line exists). The open asks are the 60 rows of doc:card-belam §7 ATOMS. Label note from the hand-off: §22 is the authoritative leaf table (V0-V9, U1-U8); "V3'" (§25 compose/split) reads as the new leaf G1 compose/split, and "V7 (python out)" in §34.7/§36.4 reads as §22's V8. One edit from the fork's file: the box's hostname is written <host> (anonymize guard). The waves (0-4) that run this doc are in the card's §1.
<!-- THOUGHT:END -->
# Brainstorm (fork, Fable, 10-22 ~18:3xZ): one matrix family for the graph interface

Read before writing: the whole of `CodexOperator/matrix-skills` (MX v0.4: cells, trust algebra, pick/hop, the MCP front),
the live engine on this box (config:engine + engine-post/wrap/grow/capsule/root, the 24 post pieces in ~/bin, `box`,
agi-turn/at/wt/flush, capsule, grow.py, agi-brief, cccc.ts), the council's unlanded designs in doc:radically-simple-engine
(§G complex brief, §T one script + one matrix, §Y1 node keys, §Z1 grow mask, §Z2 scope certs, §AA2 the lap, §AC rollover),
rse-z4 §Z4.11 (the kid's content-addressed IN commit), the move tooling in ~/tools, and what systemd is actually running.
Nothing was written or sent. Facts about other harnesses and MCP push are in §8 (a researcher's report, sourced).

## 0 · The one-line answer

Yes, it unifies further, and the axis is already the one you chose: **every rule is a matrix cell in `.geometry`,
projected into a ≤ 8 KB piece that reads it**. Today the graph holds five such matrices (the 5-row `matrix`, `growth.tsv`,
the box adjacency computed inside `box`, the ring, the load row) and is missing exactly two: **the scope matrix (who may
grow what, where)** and **the route matrix (where a package goes by its type)**. MX's real lesson is not its code (6 k
lines of Python; the agi post engine is ~35 KB of shell and already lives in the graph) but two of its shapes:
**an explicit ownership matrix O that `check` refuses against**, and **one api module with the CLI and the MCP as two thin
fronts over the same functions** (its MCP server is 94 lines). Import those two shapes, not the engine.

## 1 · The two systems side by side (so the mapping is explicit)

| MX (matrix-skills) | agi v4 (this box) | note |
|---|---|---|
| cell = typed bundle, `kind` knowledge / action / composite | node = typed file; `[type].md` schema | same thing, agi has 22 types and 5.7 k nodes |
| `F` types×types: an out type fits an in type | `growth.tsv`: child type may hang under parent types (grow-project, from the schemas) | both are the type-fit matrix; agi's already projected |
| `A = Out·F·In`, closures over (or,and) / (max,min) / (min,+) | nothing; `brief.py` walks the parent edges with a complex weight (§G) | the semiring closures are the right tool for scope/route; complex stays for the brief |
| `O` bots×cells from `bots.json`; `mx check` REFUSES a cell whose owner is not its namespace's bot | implicit: `edited_by`, a `ring:` cell on some nodes, `owning_goal` (measured: 71 % of real adds fall outside it, §Z1) | **the gap you named**: director-goals can mint a build node because nothing is O |
| `mx pick` → a plan; `mx_plan_bots` → per-bot hand-off with a real sample envelope | dispatch = brief + card + seeds; a kid's IN = ONE content-addressed commit (slice + .kid/prompt + .kid/model, §Z4.11) | agi already has "the package is a graph slice", for kids only |
| trust ≤ 0.2 is a flag; a run exits 4 | signatures (G / U / N) + ckpt quorum; no trust propagation | different axis; agi's "trust" is the signer + its scope chain |
| gated side effects: `--approve` per run and per path | `[owner-do]`, GO lines, `box town` belam-only, ring-ruled paths | same idea, agi's is keyed to identity, which is stronger |
| route memory (which links ran ok) | `.agi/drift`, verdicts, agi-frontier (each goal's falsifier) | agi's falsifier line IS the done-check a package should carry |
| MCP server = 7 tools, read-only unless env flags | none; `box`, `agi-at`, `agi-wt`, `sect` are the fronts | agi's "MCP" today is the shell + the pane fifo |
| `library_digest` on every result | `AGI_TRUNK` sha + `agi-gate` (the tip regrows the same body) | agi's is stronger (signed, bit-exact) |

Verdict on "more grounded in the matrix operators": MX is more *uniform* (one algebra module, every verb reads it);
agi is more *grounded* (the matrices are signed graph data, projected by pieces, with identity). Keep agi's grounding, take
MX's uniformity.

## 2 · The guardrail: a post may add only what its scope matrix admits (council §Z1 + §Z2, designed and tested, unlanded)

The design exists and passed its scratch tests; it was never wired (W1–W4 in §Z1). It is exactly your sentence:

```
SCOPE(p) = grow(p) × G  ∩  closure(roots(p))
  grow(p)   the child TYPES a post may mint (a row cell on config:posts; * = any)         — the O matrix, posts × types
  G         growth.tsv (child type · legal parent types · ring)                            — already projected
  roots(p)  the subtree(s) the post works in; a dispatch ISSUES them, the row holds only the ceiling (§Z1: owning_goal ≠ scope)
GATE at every write (grow.py, which agi-at and agi-turn already call on the staged tree):
  type ∈ grow(p)  ·  EVERY parent ∈ closure(roots(p))  ·  the node's key = its growth row (Y1)  ·  the scope chain verifies (Z2)
```

- **Inheritance is attenuation.** §Z2's links are `sub · iss · roots · grow · nb · na · par`, each a SUBSET of the issuer's,
  signed by the issuer, chained to the owner anchor; a revocation or a re-parent kills the subtree. A parent spawned by a
  director gets `roots ⊆ director's, grow ⊆ director's`; a kid gets ⊆ the parent's. The prototype (`agi-scope`, 3.9 KB)
  refused every widening, every sibling forgery and every self-move in the test table (F50 PASS). This is "parents/kids
  inherit that post's node-creation guardrails" with no new concept.
- **Mechanics, not prose.** The check is boolean matrix algebra: `grow` is one row of O; `closure(roots)` is the (or,and)
  closure of the parent adjacency from the roots; the gate is `O[p][type] ∧ (A*·roots)[parent] ∀ parent`. MX's `closure()`
  is 12 lines; agi's `grow-scope` is a 510 B awk that does the same walk (parity 1,558/1,558 on the live graph).
- **Owner → council / SM routing is the same matrix read the other way.** A row cell `route: {design: council, build:
  sanctuary-master}` (or a `route.tsv` projected from the posts tree + the lap) answers "where does this package go" by the
  package's node type / tag: a `[design]` package has no legal writer but council; a `[build]` one lands with SM. `box send -`
  (no recipient) looks it up, the way `[lap]` mail in §AA2 names no recipient and the gate refuses a dart PHI does not send.
- **Complex vs boolean.** Keep the complex plane for the brief (§G: phase = level, interference where paths disagree; that
  is information). For permission and routing a 0/1 matrix and its semiring closures are complete; a rotation adds nothing
  a check can use. Same family, two semirings.

## 3 · The hand-off package IS a capsule, with two new MANIFEST lines

`capsule pack subtree MINT | list MINT.. | post P` already makes ONE signed ref whose tree is the slice at repo paths,
attached by mint id, moved as a thin bundle, regrown with `regrow`, re-pointed with `repoint`. The council wrote that
"season rollover and box moves are the same pack / unpack". Make dispatch the third:

```
MANIFEST adds:  scope <link-hash>          the §Z2 link the issuer signed for this work (roots · grow · life)
                reach closed | open        closed = the post may pull ONLY the members (+ its own card/post docs); open = any mint
                at <mint_id>               where the work happens (the frontier node; `attach` stays the graft point)
```
- `agi-brief` takes a CID in `AGI_SEEDS` (today it takes node ids): the first turn = the head + the card + the capsule's
  members, in the complex-brief order. The falsifier of the `at` goal rides in the slice, so the package carries its own
  done-check (`agi-frontier` already runs falsifiers).
- `agi-wt pull` honours `reach closed`: a mint outside the members' closure is refused by name (one `case` arm). That is
  your "yes you can bring in other grid sections / no, only what you were given" switch, as ONE cell, enforced where the
  tree is pulled, never by prose.
- A kid's IN commit (§Z4.11) is already this minus the MANIFEST. Same bytes, one format: `capsule pack` for a kid writes
  `.kid/prompt` + `.kid/model` as members. Zero refs for kids stays (content-addressed), a ref for posts.
- The grid question: v4 posts write NO `refs/grid` (no piece names it; the 9,798 grid refs are the old setup's, still moved
  by the :28 board job and write.py). One commit per node tree on `posts/P`, merged up, IS the grid. Retire `refs/grid`
  writes when the last old-setup writer rotates out; nothing in v4 reads them.

## 4 · "Engine updates reach the seeds with no re-project step": make root a fixpoint, like the posts already are

What is true today, measured:
- **Post pieces** re-extract from `$AGI_TRUNK` at EVERY unit start (`ExecStartPre` loop over `AGI_PIECE_GLOB`), and the
  brief (card + seeds + claims) is walked at every SessionStart / compact. So an engine edit reaches a post at its next
  rotation or compact, automatically; a running session keeps the pieces it started with. That is the right behaviour
  (a tool must not change under a turn), not a missing step.
- **The root body** (users, units, drop-ins) is `agi-project`, run by `agi-project.path` on a WRITE to `/etc/agi/carry.env`.
  On this box that path unit is `enabled-runtime` and `inactive`; the Prime found projection never fired by itself and added
  the `projected` check row plus an explicit `systemctl start agi-project.service` to the move recipe. That is the
  "separate re-project step" you feel.
- The posts have the fixpoint already: `tick.sh` = `diff(project.sh, observe.sh)`; equal = alive, differ = start the own
  unit + a drift commit. Root does not.

The change, one cell and one unit edit, no new piece:
```
agi-project.path:   PathChanged=/etc/agi/carry.env      ->   PathChanged=<git-dir>/refs/heads/<trunk>  (+ packed-refs)
root tick (timer):  agi-gate $TRUNK  &&  diff -r project(trunk) observe(system)  ->  apply (sysusers, daemon-reload, start/stop)
```
Then there is no verb "re-project": the body is `Π(graph@trunk)`, the only input that moves `Π`'s argument is the trunk ref,
and a new post or a shuffle is just a larger non-empty diff. `agi-gate` already proves "this tip regrows the same body", so
the apply is safe by the same check the land gate runs. (Pre-projection seeds = the `seeds` + `engine` cells on the row;
they are read at projection time, so they are current by construction once the trigger is the trunk.)

## 5 · Post moves with fewer pieces: a move is pack → row → tick → in, and identity is the key, not the uid

Today a rename is: usermod + groupmod, ring close/open, retired-key dir, a grep-old sweep over six system dirs, the hooks
path, `known_marketplaces.json` (absolute home paths inside a Claude plugin file), a 134-line `sitting.sh`, `move.sh`,
`post-move-checks.sh` with ~20 rows, `box-move.sh` (ssh to the target, which fails to itself), `host-act`, and the Prime's
standing gate to add yet another rewrite. All of it outside the graph (`~/tools`), none of it a matrix.

Under §3 + §4 a move is four existing verbs:
```
1. capsule pack post OLD                       the post's refs (posts/, box/, held/, archive/) + its cards, signed
2. the row lands (name / parent / box cell)    ruled by the ring (posts.md's ruler = old AND new parent), gated as any landing
3. root tick                                   Π(trunk) ≠ observe → the NEW user/unit appear, the OLD stop (sysusers + daemon-reload)
4. capsule in + repoint on the new identity    the new post regrows ~/t from refs; the old home is never edited
```
The decision to put to council (it is the same question you asked this morning about reusing users): **identity = signing
key + refs, never the uid or the home.** A rename is "NEW regrows from OLD's capsule; OLD retires", identical to a box move
and a season rollover. Consequences: no `grep-old`, no `known_marketplaces` rewrite (a fresh home has no stale absolute
paths), no hooks-path repair; the ~20 check rows collapse to `agi-gate` parity (project == observe) plus `capsule verify`.
The Prime's standing gate items (1) become moot under this ruling; the gate-template item (2) stays, since any landing still
gates. Recommend: the Prime builds nothing on `sitting.sh`/`move.sh` until council re-cuts move as pack/row/tick/in.

Honest cost: the login. A new identity is a new Claude login unless the credential rides the capsule as a `kind secret`
(quorum-sealed, §2 of the capsule doc). That is the one real reason to keep a uid across a rename; decide it explicitly.

## 6 · MCP: a thin second front, never the transport; the wake stays the pane

- **Transport.** Mail is signed commits on refs; turns are signed commits on `posts/P`; rotation is `agi-meter` → `.fresh`
  → a fresh successor. None of it needs a harness feature: it needs (a) text injected at session start, (b) a command at
  turn end, (c) a wake on mail. Claude Code gives (a)(b) as hooks and (c) through the pane fifo (`agi-boxwake` types
  `mail: box read`); pi gets all three from `cccc.ts` (it translates the SAME hook scripts and calls `sendUserMessage`).
  The pane + fifo is the honest universal adapter: it works for any TUI harness by construction. So "the MCP tells agents how
  to send mail" is already the weaker option; the wake is a typed line, which already feels like a system call.
- **Where an MCP earns its place.** Harnesses with no shell and no hooks (a web/grok bot), and a typed, scope-filtered
  *view*: `agi://node/<mint>` resources whose root set = `closure(roots(p))` from the post's scope link, and six tools
  (`send`, `read`, `pull`, `at`, `pick`, `route`) that call the same functions the CLI calls. MX proves the shape: `api.py`
  once, `cli.py` and `server.py` as fronts, the server read-only unless an env flag says otherwise.
- **Identity.** The server starts INSIDE the post's unit (`AGI_POST`, the post's key in `~/.ssh`): it IS the post. On a fresh
  start with no key, assume **visitor**, not Prime: read = the public trunk, write = none, until the owner or the Prime
  issues a scope link (§Z2: only the owner anchors). The Prime is a key on the ring, never the absence of one; a default
  of "Prime" is the one hole a stranger would walk through.
- **Auto-start and push (sourced in §8).** Claude Code CAN take a push now: an MCP server that declares the
  `claude/channel` capability emits `notifications/claude/channel`, and the model sees `<channel source=…>…</channel>`
  queued into the next turn (research preview, v2.1.80+; per-session opt-in by a launch flag: `--channels plugin:…` for
  allowlisted plugins, `--dangerously-load-development-channels server:<name>` for a bare `.mcp.json` server; "being in
  `.mcp.json` isn't enough to push"). There is also cross-session messaging over a per-session Unix socket (v2.1.224+),
  no MCP needed: idle → a new turn, busy → read between tool calls, always tagged "from another session, not from you".
  pi has `sendUserMessage` (cccc.ts uses it). Codex has hooks but no documented push. So: THREE native wake paths
  (channel, socket, pi extension) and ONE universal fallback (the pane fifo). Make the wake line an abstraction with a
  per-harness cell (`wake: channel|socket|pane`), default pane; the unit's ExecStart gains the flag where the cell says
  `channel`. Nothing above depends on push existing; it only gets quieter where it does.
- **Packaging.** A skill cannot carry an MCP server; a plugin can (skills + hooks + MCP in one folder, servers started
  automatically when the plugin is enabled; subagents may carry inline `mcpServers`). Grok Build says it is fully
  compatible with Claude Code plugins. So ship the api front as ONE plugin directory in the repo, and the skills under
  `.agents/skills` as well as `.claude/skills` (the lowest common denominator across Codex, pi, Gemini, Cursor, OpenCode,
  Grok; `~/.claude/skills` is read natively only by Claude Code, Cursor and OpenCode).
- Is the layer noise? As a transport, yes. As the one place the scope view is enforced for shell-less harnesses, no, and it
  is cheap. Do not buy an orchestrator ("t3"): the thing every swarm harness lacks is the coordination surface you already
  have; what you lack is O and the package format, not a scheduler.

## 7 · The order of work (leaves for the Prime to put to council; each falsifiable, none new in kind)

| # | leaf | done when |
|---|---|---|
| U1 | `grow` + `roots` cells on every v4 row; grow.py SCOPE check in REPORT mode (a `[scope]` notice, no refusal) | one day of reports with 0 unexplained hits (§Z1 W2) |
| U2 | §Z2 links issued down the live tree; a dispatch issues the round's link; enforce in grow.py | an out-of-scope add refused by name; a legal one lands (Z1.2) |
| U3 | capsule MANIFEST `scope`, `reach`, `at`; `agi-brief` reads a CID; `agi-wt pull` honours `reach closed` | a closed package refuses an outside mint; an open one pulls it |
| U4 | `route` cells / `route.tsv`; `box send -` routes by package type; `[design]` → council, `[build]` → SM | a mis-routed package is refused at the receiving ref |
| U5 | root fixpoint: path unit on the trunk ref + root tick; `projected` check row retired | a row lands, the unit appears with no hand start |
| U6 | move = pack/row/tick/in; retire `~/tools/*` and `post-move-checks.sh`; identity ruling (key vs uid) | one rename end to end with 0 edits in the old home |
| U7 | `api` module + CLI + MCP fronts (MX shape), shipped as ONE plugin dir; resources = scope closure; visitor default | the same call gives the same bytes through both fronts |
| U8 | harness cells: `wake: channel\|socket\|pane`, hooks registered per harness (Codex `.codex/hooks.json` takes the SAME event names; pi via cccc.ts; `.agents/skills` symlink) | a post runs a full turn (brief, mail wake, turn commit, rotate) on claude-code, codex and pi |

Go: not now. The shell pieces are the right size and the smoothest run so far; write the matrix algebra ONCE (a ≤ 500-line
stdlib module, MX's `algebra.py` is the model) behind the api, and port that one module to Go only if per-call latency on
the box ever matters. Never the scaffold.

## 8 · Other harnesses and the MCP facts (a researcher's report, 10-22; sources in parentheses)

**What the others coordinate through** — every one of them is a pane-typer or a task-list + mailbox; none has a signed
package, an attenuating scope, or identity = key.

| harness | coordination surface | hand-off | guardrails | restart / rotation | MCP |
|---|---|---|---|---|---|
| **OpenRig** (github.com/mvschwarz/openrig, v0.6.14, docs openrig.dev; "built on tmux") | a local daemon (SQLite) + `rig` CLI; every agent slot = a tmux session; RigSpec YAML pods → members → edges `delegates_to / spawned_by / can_observe / escalates_to` (launch order + where stuck findings go, NOT who may message) | `rig send / broadcast / chatroom`: **typed into the receiving pane**; typing guard `off / draft-aware / hold`; a held send is "retained", "no automatic retry"; a separate task queue (`rig queue`) | "bakes NO allow/ask/deny policy": harness-native permissions; per-agent slot `floor / full_bypass / inherit`; it edits `~/.claude.json`, `~/.codex/config.toml` and "doesn't guarantee it can … roll back" | `rig down --snapshot / up`; `resume_if_possible / relaunch_fresh`; no compaction-driven rotation | an MCP server with `rig_up / rig_ps / rig_send` "so agents can manage their own topology"; runtimes claude-code, codex, pi, omp; no grok; ~90 agent slots saturate the daemon (issue #161) |
| **herdr** (herdr.dev, "one rust binary") — NOT built on OpenRig: `rig setup` installs herdr; "OpenRig owns the semantics; herdr owns the surface" | a background server that owns agent terminals (tiles = nested `tmux attach`); reads every pane and marks agents **working / blocked / idle** (blocked = waiting on a permission); survives SSH drop; after reboot restores layout, "the original processes do not survive" | agents drive it over a CLI/socket: spawn panes, prompt each other, "wait until another agent is genuinely blocked" | none of its own | layout restore only | detects claude, codex, cursor, opencode, grok (22); **no mailbox, queue, guardrail or hand-off protocol** |
| **Claude Code agent teams** (code.claude.com/docs/en/agent-teams.md, experimental) | shared task list `~/.claude/tasks/{team}/` (file-locked claims, dependency unblock) + mailbox JSON per agent | lead spawns by name; `SendMessage`; idle notice carries the answer; `TeammateIdle / TaskCreated / TaskCompleted` hooks (exit 2 pushes back) | teammates inherit the lead's permission mode; a message "came from another Claude session, not from you" and cannot approve a prompt; an auto-mode classifier screens inter-agent messages | one team per session, no nesting, lead fixed | teammates load project MCP servers. Related: **workflows / ultracode** (JS `agent() / pipeline() / parallel()`, 16 concurrent, 1,000 per run, gated by the Workflow permission) |
| **Gas Town** (github.com/steveyegge/gastown, Go + tmux) | Beads: a git-backed issue tracker; a git worktree per agent; "built-in mailboxes, identities, and handoffs"; convoys | Mayor `gt sling`s beads; Polecats = persistent identity, ephemeral sessions; Witness detects stuck agents; Refinery merge queue, "polecats never push directly to main"; P0–P2 escalation | role-based; the merge queue is the gate | worktrees "survive crashes and restarts"; Seance reads predecessor logs | none; presets claude, gemini, codex, kiro, cursor, pi, omp, … |
| **T3 Code** (github.com/pingdotgg/t3code; the likely "t3") | a control plane: one agent per thread on its own branch/worktree; providers Claude Code, Codex, Cursor, Grok Build, OpenCode | **no agent-to-agent hand-off** | permission modes Supervised / Auto-accept / Auto / Full per provider; "a thread it starts cannot run with more permissions than the mode you chose" | — | T3 is itself an MCP **server** (HTTPS + OAuth, Read-only … Full, 30-day sign-in) |

Read against agi: the pane fifo you already use is exactly OpenRig's and herdr's delivery; the task list + mailbox is a
weaker form of `posts/P` + `refs/box`; nobody attenuates scope down a tree or signs a package. Two things worth stealing,
both small: OpenRig's **typing guard** (hold a wake while the pane shows an unsubmitted draft — `agi-boxwake` types into
the fifo blind today) and herdr's **blocked-on-permission reading of the pane** (a `blocked` state next to the Prime's
"silent > 12 h", from the bytes of `~/o`; agi-desktop-check is the screenshot cousin). Nothing to buy: T3 does no
hand-off at all, so it would be one more surface in front of the same graph.

**MCP and harness facts**
- Claude Code reads MCP config at startup and spawns each server as a subprocess; interactive sessions **prompt for
  approval** of project-scoped `.mcp.json` servers (`claude mcp reset-project-choices`; `claude -p` and the SDK load them
  without asking; `enableAllProjectMcpServers` is ignored in an untrusted folder). Plugins start their MCP servers
  automatically when enabled. A skill has **no MCP frontmatter**; a skill folder with `.claude-plugin/plugin.json` loads as
  a plugin with agents, hooks and MCP servers; subagents take inline `mcpServers`, connected for their lifetime (mcp.md,
  skills.md, sub-agents.md).
- Push: **channels** (channels.md, research preview, v2.1.80+, not Bedrock/Vertex/Foundry): the server declares
  `capabilities.experimental['claude/channel']` and sends `notifications/claude/channel {content, meta}`; the model sees
  `<channel source="name" …>content</channel>`; events queue and are delivered together on the next turn; per-session
  opt-in `--channels plugin:<n>@<marketplace>` (Anthropic allowlist) or `--dangerously-load-development-channels
  server:<n>`; a permission relay exists (v2.1.234+). **Cross-session messaging** (v2.1.224+): per-session Unix socket
  (`CLAUDE_CODE_MESSAGING_SOCKET` / `_TOKEN`), `crossSessionInbound accept|hold|refuse`, always labelled as from another
  session. This box runs 2.1.295; the channel flag did not appear in `claude --help` here, so verify before a cell relies on it.
- Resources: `@server:protocol://path` mentions, `ListMcpResourcesTool` / `ReadMcpResourceTool` (no permission prompt);
  roots = the launch dir + `--add-dir` (`roots/list_changed` sent). Subscriptions and resource templates: not in the docs.
- Clients: **Codex** `[mcp_servers.<n>]` in `~/.codex/config.toml` or a trusted `.codex/config.toml`, stdio + streamable
  HTTP, `default_tools_approval_mode`. **Grok Build** `[mcp_servers.<n>]` in `~/.grok/config.toml`, `grok mcp add`, ACP;
  plugins "fully compatible with Claude Code". **pi** native now: `~/.pi/agent/mcp.json` / `.pi/mcp.json`, stdio + HTTP,
  exposure `codemode` (default) / `deferred` / `direct` (MX's README already says "pi: add exposure direct"), resources
  via `list_mcp_resources` / `read_mcp_resource`. **Cursor** `.cursor/mcp.json` (tools, prompts, resources, roots,
  elicitation). **Gemini CLI** `settings.json mcpServers`, `trust:true` bypasses confirmations.
- Hooks: **Codex** has them, with the SAME event names (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse,
  PreCompact, Stop, SessionEnd, …) in `~/.codex/hooks.json` or `.codex/hooks.json`, handlers `command | mcp_tool`,
  enabled by default (learn.chatgpt.com/docs/hooks.md). So the agi hook scripts register on Codex unchanged; cccc.ts is
  needed only for pi (TypeScript extensions: `session_start, input, before_agent_start, tool_call, turn_end`,
  `pi.sendUserMessage()`).
- Skills: Claude Code `~/.claude/skills`, `.claude/skills`, plugins. Codex `.agents/skills`, `~/.agents/skills`,
  `/etc/codex/skills` (not `~/.claude/skills`). pi `~/.pi/agent/skills`, `.pi/skills`, `~/.agents/skills`,
  `.agents/skills`. Gemini `.gemini/skills` | `.agents/skills`. Cursor its own + `.claude/skills` + `.codex/skills`.
  OpenCode `.opencode/skills`, `.claude/skills`, `.agents/skills`. Grok `.grok/skills`, `~/.agents/skills`, "reads Claude
  Code skills". **Lowest common denominator: `.agents/skills` / `~/.agents/skills`** (Codex, pi, Gemini, Cursor,
  OpenCode, Grok); the repo already commits `.claude/skills → skills/`; add `.agents/skills → skills/` beside it.
- Confidence: OpenRig / herdr identity high ("herdr on top of openrig" is backwards). Claude Code resource subscriptions:
  not documented. Grok Build's hook list: not fetched. "t3" = T3 Code is an inference. Docs read cite up to v2.1.305.

---

# Part II (fork, Fable, 10-23 ~16:xxZ): identity as a chain, hashes as time, symbols over numbers, root on loan, spiders, IOMap

Read for this part: config:key-authority · config:secrets · config:vetoes · config:links · config:census · the ring (agi-signers:
append-only allowed_signers with valid-after/valid-before per key generation) · ckpt (k-of-n quorum blocks, level-adjacent
signers, `AGI_CKK` per level) · agi-land (root ff-lands a signed range on the strength of the parent cells) · agi-kid (kids are
already headless pi: `pi --provider openrouter -p`, `-e cccc.ts`) · rse §G (links as symlinks; brief = one complex multiplication)
· §AC (rollover = goal-tree collapse, `nest:`) · rse-aa1 §F (flows: `refs/spawn/<flow>/<i>-<sha12(flow,i,ARGS,prev)>`, a hash
chain) · goal:g2.2 (IO maps; the owner's 09-24 shape/imap/omap verbatim) · g4.4 (specialists own regions) · g2.21 (spider skin)
· g7.16.1.11.18 (K spawn classes) · s3-plan ("custodian ROOT: closed vocabulary, no shell") · sudoers (only agi-belam: ALL).
Census: 39 rows, 15 on engine.v 4, 0 posts on pi; every v4 post is claude-code; kids are pi. The §8 facts stand.

## 9 · Identity is a chain of piece-sets, not a key and not a uid

What you described is a Merkle chain, and git already is one. Make it explicit:

```
refs/id/P                       one commit per identity version of post P; the CHAIN is the identity, no tip is
  tree:                         the piece-set, every entry a mint id pinned to a grid version (a gitlink or blob)
    key.pub   role   harness   model   brief   card   perms   slot(uid,home,box)   cred -> capsule CID (kind secret)
  commit message: `id P v<n> swap <piece> <old>-><new>`     parent = v<n-1>
  signature:      by the key of v<n-1>   (continuity: the old self vouches for the new self; v1 is signed by the spawner)
```
- **A swap is a new commit.** Re-key, re-brief, new harness, new model, new box, new uid: each is one `swap` line and one
  signature by the previous key. The principal name stays `P@agi` (agi-signers already keeps every key generation of `P@agi`
  with `valid-after`/`valid-before`; this is the same record, one level up, over ALL the pieces instead of the key alone).
- **The identity check is three matrix facts, no new primitive:** (1) the piece-set ⊆ the row's allowed piece TYPES (one row of
  the same O matrix §1 imports: role × piece-type); (2) every link is signed by its parent link's key (`agi-scope`'s
  attenuation-only chain, §Z2, with "key" as one more attenuating field); (3) the birth link is signed by the parent post
  (the spawn). `ckpt check` already walks a signed chain exactly like this; the identity walker is the same 20 lines.
- **A rename or a box move is a merge:** `refs/id/NEW` v1 has TWO parents: the spawner's grant and `refs/id/OLD`'s tip. Lineage
  is a graph fact; the new post inherits OLD's scope by attenuation; OLD retires. This replaces §5's "identity = key" ruling
  with the stronger one: **identity = the chain; the key is a piece of it.** The uid is also a piece (`slot`), projected by
  root at the tick from the row, so "slide a new identity into the same slot" = a swap of every piece but `slot` — legal,
  cheap, and recorded.
- **The credential rides as a piece.** The Claude login (`~/.claude/.credentials.json`, 524 B here, plus the OAuth state
  in `~/.claude.json`) is a `kind secret` capsule (quorum-sealed, §2 of the capsule doc) referenced from the tree; root places
  it with `LoadCredential` at the tick, the way K1 hands a kid its minted key. It is bound to your Claude ACCOUNT, not to a
  uid, so it moves with the chain. Risk to measure first (one post, one evening): whether Claude Code accepts the pair in a
  fresh home without a device re-auth. If it does, the login cost in §5 disappears; if not, the slot piece is the one you
  keep across renames and nothing else changes. A second subscription is then a second `cred` capsule and an `account`
  label on it; which posts carry which = one column of the route matrix (U4), balanced by quota.
- **Ship-of-Theseus, stated as the invariant:** a post is alive iff `refs/id/P` has an unbroken signature chain to its birth
  and its tip's piece-set passes (1). Nothing else about it needs to be the same as yesterday. That is your sentence
  ("attached not to any single piece but to the history of those pieces being switched out") as a check that runs.

Today's incident is the first leaf of this section. The reboot's unit ran `claude -c go`, which means "the most recently
modified transcript", and the newest one was this fork's, so the fork woke at the Prime's post. The session id is a piece of
identity and must be resumed BY NAME: `agi-run` resumes `--resume $(cat ~/.session)` (written at first start, swapped on
rotation), never `-c`. Fifteen bytes of shell; it closes a class of post theft (a stray session, a fork, a kid's transcript).

## 10 · Hash-only identifiers, signatures only at the boundary, and time as chain height

The honest math first. A hash chain gives you **integrity and order** (nobody can rewrite link k without changing every link
after it) and **commitment**, but not **origin**: anyone can extend a chain with a perfectly valid hash. Origin needs a secret
somewhere: a signature (public key), a MAC (a shared secret; no third party can tell who wrote it), or a delayed-disclosure
scheme over a hash chain (TESLA-style: commit now, reveal the key later; authentication from hashes alone, at the price of
clock sync and verification that is always one interval late). And "hash-based" and "signature" are not opposites:
Lamport/Winternitz one-time signatures and XMSS/LMS/SLH-DSA are signatures built from nothing but hashes
(sizes, from the standards: SLH-DSA/FIPS 205 7.9-49.9 KB per signature, stateless; XMSS/RFC 8391 ≈ 2.5-2.8 KB and
LMS/RFC 8554 ≈ 1.5-1.8 KB, stateful, 2^h signatures per key and "no security guarantees remain" if a state is reused, which
is why SP 800-208 wants them in hardware; RFC 4082 §2.2: TESLA itself "MUST be bootstrapped through a regular data
authentication system", i.e. a signature). So the design question is not "hashes instead of keys" but **where origin matters**.

Where the system is already hash-only, and correctly so: mint ids; the kid's content-addressed IN commit; flow positions
`refs/spawn/<flow>/<i>-<sha12(flow,i,ARGS,prev)>` ("the position is DERIVED, never stored"); capsule CIDs; every git object.
Inside ONE uid's own refs a signature adds nothing the kernel does not already guarantee, which is why a one-shot "has no
identity of its own" (AA1.F) and that is right.

Where origin is irreducible, the boundary set **B = {land, box send, ckpt block, capsule out, id link}**: a byte crosses from
one uid to another, or to root, or off the box. Keep ed25519 exactly there, one key per post, rotated as a piece (§9).
Everything else: hash. That is already close to true; the one change is to STOP signing what never crosses (a post's own
worktree commits, kid results inside the launcher's uid) so the signature count tells the truth about trust boundaries.
Post-quantum, if that is the motive for "minimise public keys": SLH-DSA is the hash-only signature, git/ssh cannot verify it
yet, signatures are kilobytes; season 4, behind the `AGI_SIGN` algorithm list ckpt already has ("hybrid = AND").

**Time.** You already have two clocks and should stop using the third. A post's clock = its chain height on `refs/id/P` and
`posts/P` (a Lamport clock: "after" is provable, "when" is not). The town's clock = ckpt block height (quorum-sealed, and
anchored to wall time only by the Sigstore sealer every 30 min). Rules that say "4-hourly", "after 24 h", `expiry_seconds`
in config:vetoes, `rotate_pct` should be re-cut in heights where they can be (rotate at N turns of the post's chain; a veto
expires after K blocks; a season third = a block height). Wall time stays only where the outside world imposes it
(API windows, the sealer). That is "a nonstop outpouring of hashes marking moments" with the moments ordered by the chain,
not by a clock a reboot can lie about (this box's local clock prints 12 h off UTC right now).

## 11 · Memory horizons: optmem / optchat as a row cell, not a harness feature

The facts (researcher, 10-23, sources in §8b): **neither optmem nor optchat is a pi feature.** OptChat is Victor Taelin's
recipe (now "UniiChat"): an append-only JSONL log, a binary tree of ≤ 512-byte summary lines over it, a bounded 64-128 KB
VIEW per turn, and `zoom` to reopen any line; files `main/<date>.jsonl`, `tree/…`, `view.json`; harness-agnostic by
construction. OptMem is his separate repo: a 426-token prompt + `memo note|wake|recall|zoom` over `~/.optmem/memory/`,
regex recall, no embeddings, no server (no licence file as of 07-30). `pi-optchat` (third party, MIT) wraps OptChat as a pi
extension: one endless chat per PROFILE, `pi install npm:pi-optchat`, headless needs `--optchat-profile <name>`, the
compactor is a second model call (default Sonnet 5.5) billed to your credentials, and it requires pi ≥ 1.0.2 under the
RENAMED package `@earendil-works/pi-coding-agent` (1.4.0, 10-21). This box runs `@mariozechner/pi-coding-agent` 0.73.1,
deprecated on npm since 05-07: it will not load here. pi 0.73.1 has only compaction (`reserveTokens`/`keepRecentTokens`,
`session_before_compact`) and the extension API (`sendUserMessage`, `appendEntry`, `session_start`, `turn_end`, …).

So the thing to adopt is the SHAPE, not the package: OptChat's log + summary tree + bounded view is §AC's `nest:` applied
to a conversation (a container per subtree, a baked summary line, zoom = open the member). It is files, so it is nodes.
OptMem adds nothing the graph does not already do better (a memo is a node; `recall` is the brief); skip it.

What the design needs regardless of the mechanism: a **memory horizon** per post, as a cell, and a store the horizon keys.
```
posts.md row:   mem: always | season | goal | none         (Prime: always · council/keep: season · directors: goal · kids: none/optchat)
store:          refs/mem/P/<horizon-id>      horizon-id = season for `season`, the dispatched goal's mint id for `goal`, `-` for always
reset:          a new horizon-id = an empty store; the old one is kept (a retired piece, never deleted); nothing is "cleared"
```
- The store is a node tree, so a memory is a graph slice: chats are nodes (g2.24), the finest zoom is the chat (g2.7). A
  memory reset is then the §AC collapse applied to one post: the old horizon folds into a `nest:` container with its baked
  metrics; the new horizon starts from the brief alone.
- For pi it is an extension (the harness already has the hooks and `sendUserMessage`); for claude-code the same two moments
  exist as hooks (SessionStart injects the store's render; Stop/PreCompact extracts). One store, two adapters, the §6 shape.
- The brief is where recall enters: §G's multiplication with the memory nodes as extra seeds (their weight is the α term;
  a horizon reset is α → 0 for the old horizon). No second retrieval system.
- Kids "fully inside optchat": a kid's horizon is the flow (`refs/spawn/<flow>`), so the chat IS the flow's chain; that is
  cheap and already content-addressed. Batchable kids (§13) have no chat at all by definition; keep both classes.

## 12 · Nodes as coordinates, actions as vectors: the model writes symbols, the engine does the algebra

The question you asked is the right one and the answer is firm: a transformer is reliable at **naming** positions and
**composing named operators**, and unreliable at **emitting numbers** that must be exactly right (tokenised digits, no
verification inside the forward pass, errors compound through a product). So never make a model write or read a matrix.
Make it write a **word** and let the engine multiply.

```
alphabet  Σ = edge labels {up, down, near, member, …} ∪ verbs {read, mint:<type>, send, spawn, land, …}
position  p = a one-hot (or sparse) vector over nodes: where the post stands (its card, its dispatched goal)
step      each label a has a matrix M_a (P_up, P_down = Pᵀ, P_near, …) read off the symlinks (§G) — nothing is stored twice
program   a word w = a1 a2 … ak;  its effect is  p' = M_ak ⋯ M_a1 · p   (a traversal vector, as you said)
legality  the word is accepted iff  mask(p') ≠ 0  under the scope matrix (§Z1) and the transition matrix T[a→b]
```
- **This is a regular language.** The allowed programs are the words a finite automaton accepts; the matrices are its
  transition matrices; scope is a mask; refusal is the zero vector. "A programming language before it becomes one" has a
  name: the free monoid over Σ cut by a regular constraint. jev's grammar (goal:g1.25, "one choice surface") is Σ; this gives
  it a semantics. MX's `hop`/`pick` are the same objects under the boolean semiring; §Z1's grow mask is `mask`.
- **Smoothness is three cheap constraints, not a new idea:** (i) no teleport = every step is along an existing edge, which a
  product of adjacency matrices cannot violate; (ii) no hard cornering = a bound on word length per turn (k hops) and on
  T (which label may follow which); (iii) under §G's complex phase, "no violent rotation" = the total phase per turn ≤ Θ,
  one scalar. Creativity ("unhinged combos") is the `near/` latent edges, which only the sleeper writes, with a temperature
  on how many are admitted into T. Taste, in your sense, is the choice of T and Θ per role; it is a cell.
- **Workflows = spawns = subagents = posts** falls out: a flow manifest (AA1.F) is a word whose letters are `(node, verb)`;
  a one-shot stage is `spawn` inside the caller's uid, a `post:` stage is `send` up or down the post tree; the lap (§AA2) is a
  permutation, which is a word too. One runner, one checker. The nesting you want is word concatenation.
- **Mail as a vector:** `box send TO` is already the unit step `up` or `down` (adjacency = levels differ ≤ 1); the vector is
  the CHECK, the text stays the carrier. Do not make a human-or-model read a vector where a sentence does the same job.
- **Rendering the position:** addresses (paths) and glyphs, never numbers. The post sees `goal/g7.16.1.11.44 ↑2 →near 3`,
  not `[0.17+0.41i]`. The encode-attention-decode loop you worried about never has to carry a matrix through tokens.
- What to measure before believing any of it: give three posts the word form for one day (a hook that logs the word each
  turn was equivalent to) and count how many real turns are words of length ≤ 4 over Σ. If > 90 %, the surface is right.

## 13 · The Console credits: a batch lane for the no-tool spawn class, never for a post

The facts (researcher, 10-23; §8b): the credits are real and yours: **Max 20x = $200/month**, claimed by linking ONE
Console org after 7 days, expiring each cycle, no rollover; they cover the API, Managed Agents, the Agent SDK, the
Playground and `claude -p` **when run with an API key from the linked org**; they do NOT cover interactive Claude Code.
The Batches API: 50 % off every token, ≤ 100,000 requests or 256 MB per batch, "most batches complete within 1 hour",
results at completion or 24 h (unfinished requests expire unbilled), results kept 29 days; ALL active models (Fable 5
$5/$25, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5, Haiku 5.5 $0.05/$0.25 per M tokens in batch); tool use, extended thinking,
multi-turn and prompt caching (1-h TTL) all work in a batch; `speed` (fast mode) does not. Batch rate limits at the Start
tier: 1,000 RPM / 200,000 queued. The Admin API cannot CREATE keys (only read, rename, disable), so there is no OpenRouter-
style provisioning: one Console key with a spend cap, held root-side. Neither pi 0.73 nor Claude Code nor the Agent SDK
submits batches; the lane is curl, which is what `agi-infer` already is.

The larger consequence is not the batch: **a tool-loop kid on `claude -p` with the Console key is covered by the credits.**
That is the K2(a) class (its own uid, `LoadCredential`), today on OpenRouter; moving it to the Console lane spends the
$200 on real kids, not only on no-tool items, and Claude Code's `-p` "always uses the key" in non-interactive mode, so
the subscription is never touched by accident. The forbidden-key rule stays for every POST uid.

Where batching fits is already decided by K2 (g7.16.1.11.18): **K2(b), the no-tool spawn** (one inference request, context in,
text out: reviews with the diff in the prompt, digests, brief drafts, critiques, spider test generation, chain summaries) is
exactly a batch item; **K2(a), a tool-loop kid** (pi with tools) cannot be batched, each needs a live loop. So:
- `agi-infer` (829 B, curl, OpenAI-compatible) gains `--batch`: N requests → one JSONL → submit → poll → each result lands
  as `refs/spawn/<flow>/<i>-<sha12(…)>`. The flow design already decouples request from result (a paused flow waits on a
  ref), so a batch is just a slow lane; the gate and the hand-off are unchanged.
- A director parallelises by emitting a VECTOR of kid words (§12) and submitting once; results land as commits over the
  window; the director's turn is not held. Fable for council reviews = the same lane with a model cell, used by the
  `[design]` route only (U4). The credits are spent where latency does not matter, which is most of the review volume.
- The key: `ANTHROPIC_API_KEY` is a **forbidden key** in config:secrets for a good reason (a post on the subscription must
  never bill the Console by accident, and vice versa). Keep that for every post uid. The batch lane gets the Console key
  the K1 way: minted/held root-side, `LoadCredential` into the `agi-infer` unit only, never in a post's env. If the Admin
  API can mint scoped keys, that is the provisioning analogue; if not, one key with a spend cap read from the graph.
- Headless pi for parents: a parent is a tool loop; it benefits from batching only through its kids. Memory per headless pi
  on this box is small (kids run that way today); the bound is `spawn_budget`, not RAM.

## 14 · Root on loan: no sudo moves; the parent cells, a quorum height and a held-reason set

Today exactly one uid has root: agi-belam, `ALL NOPASSWD`. Nobody else, and that is the right number of shells. What
already exists is better than a loan: root acts only as a **projection** of landed state (agi-land ff-lands a signed range
when the parent cells allow it; the tick of §4 stands up users and units from the row; agi-signers appends keys). So
"let SM do graph moves" and "let council do anything on unanimity" are two matrix edits and one new piece:
```
who may land what:   the `lands` cell on the parent row (exists) + a scope row over .geometry paths (U1): SM: posts.md box/boot/
                     parent cells, crons, units — the maintenance set; council: any row
how many must sign:  AGI_CKK per level (exists in ckpt; "0:2 1:2 …"): council rows need k = 3 of 3 — a landing by the council
                     is a ckpt block all three members sign over the sha; root applies iff `ckpt check` holds
owner rows:          a `needs: owner` column in the route matrix (U4): season rollover, spend above the cap, a new top-level goal,
                     an identity ruling, anything that touches sudoers — root holds these until a row signed by the owner key lands
```
The s3-plan already names this object: "custodian ROOT (closed vocabulary, no shell)". The vocabulary is the set of verbs
the tick can produce (sysusers, unit, ref, hook, signers); there is never a shell. belam's own `ALL` shrinks to the same
vocabulary once the tick covers it (the TSS 2-of-3 with your device, later).

**Reporting a held action** is the part you asked for, and it is one line per hold on the box of the requester and in the
owner's room, from a closed set so you can grep it:
```
[root] held <verb> <sha>  quorum 2/3 (signed: alive, all-is-one; missing: self-perpetuating)
[root] held <verb> <sha>  refused 3/3 (a signed `no` block from each)       <- the unanimous-no you were curious about
[root] held <verb> <sha>  veto (config:vetoes active_gate <id>)
[root] held <verb> <sha>  owner-gate (route row needs: owner)
[root] held <verb> <sha>  gate: <grow-gate / agi-gate refusal text>
```
A refusal is itself a signed block (`no` instead of a sig over the sha), so the record of disagreement is the ckpt chain and
nothing has to be remembered. With this in place belam runs on Fable and is bothered at the owner rows only: the season
thirds, rollover, spend. Everything else is a landing the tick applies or holds with a named reason.

## 15 · Closing season 3 on its own: what this brainstorm promotes and what waits

The horizon list is long (≈ 170 `status: horizon` goals). The closing mechanism exists (§AC: collapse by goal tree, `nest:`,
baked metrics). What the system lacks is the PICK, and the pick is a route-matrix exercise the Prime + council can run
without you: every open goal gets one of {promote now, season 4, retire}. From this document:
- promote: U1-U8 (Part I) · V0 resume-by-id · V1 identity chain · V2 credential capsule test · V3 root verbs + held reasons +
  council k=3 · V4 mem cell + store · V5 batch lane · V6 IOMap rows on the pieces · V7 spider v0 · V8 grow.py → grow-check,
  links.py behind §G · V9 seed capsule = project init.
- season 4: hash-based (PQ) signatures · the numeric control surface beyond symbols · the hardware type alphabet (§19) ·
  income (stream, games, avatars) beyond the stream-master row that exists · kids "fully inside optchat" until V4 is measured.
The rule for the pick: a goal is promoted only if one of the V-leaves is its falsifier's shortest path; otherwise it waits.
Your involvement points become the owner rows of §14: one third, two thirds, rollover.

## 16 · Other projects, other people: a project is a season-0 capsule

g1.24 ("the engine must never need to know which project it is running"; fantasia already ran) and g1.5/g1.23 (init,
distribution shape) are the open goals; §T (one script + one matrix) and the capsule give them their answer:
```
season 0  = the ZYGOTE: config:engine + the matrix + schemas + growth.tsv + 0 post rows      (a capsule, `pack subtree .geometry`)
init      = `capsule in <seed>` into an empty repo  +  ONE row (the owner's first post)       -> the tick stands it up
season 0→1 rollover = the first landing that adds post rows; nothing else is special about it
the engine's source = a second capsule, pinned by sha and attached by mint id (g1.23's answer: the distribution shape is the
                      capsule; it fixes L9's "unpinned, silently stale clone" because a capsule has a CID)
```
`agi.sh start` (landed, .44.8) is already the one script; what another person needs on top is §9's credential story and a
Quickstart that is the seed capsule's README. Importing an existing project = pack its tree as nodes under one `mvp` (the
build-node parent shapes allow `[mvp]`), land, let a spider (§18) write the IO maps.

## 17 · grow.py and links.py: one shell check at both points; links become symlinks

Facts: `grow.py` is 31 lines but imports `spawn_gate.py` + `frontmatter.py` (the Python graph library) at every turn;
`grow-check` (1.3 KB shell + awk over growth.tsv) already does the same order-and-key check at the LAND, inside `grow-gate`
(7 KB). `links.py` is 1,040 lines and the old setup's; §G turns parents into `p/` symlinks, so the broken-link check is
`find .agi -xtype l` and the schema gate reads `ls p/`. So:
- turn-time check = the same `grow-check`, run by agi-turn over the temp index (`git archive` of the index tree is what the
  gate already reads); `grow.py` retires for v4 posts. One check, two moments, zero Python in the hot path.
- "matrix/hash-chain check": that is what grow-check IS. growth.tsv rows (`nid · child · variant · parents · ring`) are the
  F matrix (which parent shapes admit which child type), the `ring` column is the hash/key part (who may sign the add), and
  §Z2's chain adds where (scope). A node grows iff F admits the shape AND the signer is in the ring AND the scope cert
  covers the place. Three multiplications; the refusal names the one that was zero.
- auto-written links: in §G a parent IS a symlink written at mint by the owner of the new node; make agi-turn derive it from
  the dispatch package (`at <mint>` in the MANIFEST, §3) so a kid never types a parent at all. The link is correct by
  construction because the package named where the work hangs.
- self-summarising chains: §AC's `nest:` + baked metrics per container is the summary; "talk to a chain" is a no-tool spawn
  (§13, batchable) whose context is `agi-brief` with the chain's goal as the only seed; a chain's memory is the `goal` horizon
  of §11. Nothing new to build once V4 and V5 exist.

## 18 · Spiders: a standing flow per region, acting only on a red or a mismatch

g4.4 already wants specialists that own a region; g2.21 draws them as spiders. Make a spider a **flow with a standing
trigger**, not a post:
```
region   a scope cert (§Z2) over a subtree or a piece set; regions do not overlap by construction (attenuation)
trigger  a NEW or CHANGED node in the region (the tick's diff, or grow-gate's event) — the sleeper (§A) is the first spider
stages   1 IOMap check (§19: imap/omap/shape vs its hypothesis and its goal)   2 run the node's tests (shell .t.sh per piece)
         3 red or mismatch → a fix kid in its own uid with scope = that node's cone, landing through the normal gate
         4 write `near/` edges and the container's metrics (the sleeper's job today)
class    stages 1, 2, 4 are no-tool (batchable, §13); only stage 3 spends a uid kid; all bounded by spawn_budget
```
- Honest line: gating does not disappear (the land IS the gate, and it takes milliseconds); what disappears is a human or a
  director WAITING on a test. The loop closes where the change landed.
- The trap, named now: a spider that "improves" without a red or a mismatch is scope creep with legs. Rule: a spider may act
  only on a failing test or an IOMap mismatch; it may mint `idea` nodes (growth.tsv admits it) and never goals; a goal is a
  director's or the Prime's word. "Launch new ideas for optimisation" = ideas, routed to council by U4.
- v0, one evening: ONE spider over the 24 post pieces in `.geometry` (they have `.t.sh` tests already, .11.16); trigger =
  a piece changed on the trunk; stage 2 only; a red opens `[red]` mail and a fix kid. Measure reds caught per week vs the
  CHECK cadence today.

## 19 · IOMap: goal:g2.2 wakes up, and it is MX's port algebra

Your 09-24 verbatim on g2.2 already fixed the rows: `imap` (calls that may/must enter, mandatory vs optional, their shapes),
`omap` (nodes and functions this node calls or may call, mandatory vs potential), `shape` (its output). Those are, exactly,
MX's typed ports and matrices: `imap` = a row of **In**, `omap` = a row of **Out**, `shape` = the type of the output port,
and `F` (type × type fit) says which shapes connect. Then:
- **"predict where each node reaches any other node before building it"** = `A = Out · F · In` and its closure `A*`
  (Floyd-Warshall over the boolean semiring, MX `closure()`), computed from the DECLARED maps alone. Reachability is a
  table before a line of the build exists; a build is then checked against its declaration (MX `check` refuses a cell whose
  ports do not fit; the spider's stage 1 is that check).
- **where the map lives:** on the hypothesis (the claim "this node will take X and produce Y"), inherited by the build as a
  contract slice (g2.2's own title); the build's rows must equal or ATTENUATE the hypothesis's (the same attenuation-only
  rule as scope); the goal holds the coarser map its hypotheses refine. The MVP node is where the first `shape` is drawn.
- **the primitive transport layer** = the port-type alphabet. Start with what the 24 pieces actually have: env vars and
  stdin in; refs, files under ~/t and exit codes out. Declare those 24 maps first (they are ≤ 8 KB shell each; the maps
  are a few lines), compute A*, and measure how many real calls fall outside the declared map, the way §Z1 measured 71 % of
  adds outside the owning goal. That number decides the enforcement order (report-only → key → enforce, §Z1's ladder).
- the "inverse" abstraction (hardware units, logic, assembly) is the same algebra over a different type alphabet; nothing in
  the engine changes for it, which is why it can wait for season 4 without being designed twice.

## 20 · Streaming, games, avatars, a second subscription: the dependencies, not the design

The facts (researcher, 10-23; §8b): `mystudio.fun` does not resolve to a product; the site is **mystudios.fun, "Studios by
Claw Hunter"** (ex-clawhunter.fun): a RESALE API for chat/image/video models at about half of list price, OpenAI format at
`/api/v1`, Anthropic format at `/api`, 1 credit = $1, pay-per-call in USDC also offered, 10 % off paid in its `$CLAWHUNTER`
token, a grants form with no amounts, and a founder interview (10-20) claiming "holding CLAWHUNTER earns a dollar in
credits daily", ~$3,500 revenue and 105 paying users, self-reported. **It has no avatar product**: the only character
endpoint is `POST /api/v1/videos/recast` (cast a character into a preset clip, per render); no lip-sync, talking head,
VTuber or real-time endpoint. So it is at best a cheap model reseller with a token attached, not an avatar service; an
animated streaming avatar needs a different tool, and "hold tokens for credits" is a treasury decision for the owner rows
of §14, not an engine fact.

Not designed here (council leaves), but the order is clear: income work needs V3 (root on loan, so it runs without you),
V4 (an always-on horizon for stream-master), V5 (the cheap lane for the review volume it will generate) and V2 (a credential
that can move). The stream-master row exists (local-town, v4) and `agi-stream` is a skill; an avatar service is an output
adapter on the stream display, which the skill already fences (nothing but the dashboard and the masked feed). Your own
verification goal ("confirm I can purchase the additional subscriptions and it makes sense") is answered by the §13 lane's
first month of numbers: credits spent, turns moved off the subscription, reviews per dollar.

## 8b · Sources for Part II (researcher, 10-23)
OptChat gist (VictorTaelin, "OptChat – HOW TO REPLICATE MY SETUP") · github.com/VictorTaelin/OptMem · github.com/jonaslsaa/pi-optchat
(npm 0.9.0, 10-22; peer deps `@earendil-works/pi-*`) · npm: `@mariozechner/pi-coding-agent` deprecated → `@earendil-works/pi-coding-agent`
1.4.0 · pi docs: providers.md (auth.json `anthropic` api_key; `/login` Claude Pro/Max, "third-party harness usage draws from extra
usage"), compaction.md, extensions.md, usage.md · platform.claude.com/docs/en/build-with-claude/batch-processing ·
…/api/rate-limits · …/about-claude/api-credits-for-subscribers (rolled out 10-07) · support.claude.com 17154008 (monthly credits) ·
support.claude.com 15036540 (Agent SDK with your plan) · …/manage-claude/admin-api ("The Admin API can only read, rename, and
change the status of existing keys") · code.claude.com/docs/en/authentication (precedence AUTH_TOKEN → API_KEY → apiKeyHelper →
OAUTH_TOKEN → /login; "In non-interactive mode (-p), the key is always used") · mystudios.fun/llms.txt, /grants, the 10-20
founder interview (mcgsignal) · FIPS 205, RFC 8391, RFC 8554, SP 800-208, RFC 4082.

## 21 · Decisions for you (each is one line in a node once decided)

1. Identity = the chain `refs/id/P`; the key, the uid (`slot`) and the credential are pieces of it (§9). Replaces §5's ruling.
2. The credential rides as a `kind secret` piece — test on ONE post before it is a rule (§9).
3. Signatures only at the boundary set B; hash-only inside a uid; PQ signatures are season 4 (§10).
4. Rules move from wall time to chain/block height where they can (§10).
5. `mem:` is a row cell with four values; the store is OptChat's SHAPE as nodes (log + summary tree + bounded view), not
   the package; pi moves to 1.x first if any pi extension is to be used at all (§11).
6. The control surface is symbolic: words over Σ, matrices in the engine, never numbers in a prompt (§12).
7. Link the Console org now (the $200 expires monthly); the key lives root-side and reaches two lanes by `LoadCredential`:
   `agi-infer --batch` (no-tool class, 50 % off) and `claude -p` kids in their own uid (K2(a)); no post uid ever holds it (§13).
8. Root is never loaned as a shell; SM/council widen through cells and a quorum height; holds are reported from the
   closed set (§14).
9. Spiders act only on a red or a mismatch; they mint ideas, never goals (§18).
10. IOMap lives on the hypothesis, attenuates into the build; g2.2 goes horizon → active (§19).
11. The season-3 pick runs as a route exercise by the Prime + council; your rows are the thirds and the rollover (§15).

## 22 · The work order, Part I and II merged

| # | leaf | done when |
|---|---|---|
| V0 | agi-run resumes by session id from `~/.session`, never `-c` | a fork started beside a post cannot take its post after a restart |
| V1 | `refs/id/P` chain: piece tree + continuity signature; `id check` (20 lines, ckpt's walker) | a swap of every piece but `slot` passes; a link signed by a foreign key fails by name |
| V2 | credential as a `kind secret` piece placed by `LoadCredential` at the tick | one post logs in on a fresh home with 0 device re-auth (or the result says it cannot) |
| V3 | root verbs as tick projections + `[root] held` lines from the closed set + `AGI_CKK` council 3/3 + `needs: owner` | SM lands a box move with no sudo; a 2/3 council landing prints `held quorum 2/3` |
| V4 | `mem:` cell + `refs/mem/P/<horizon>` in OptChat's shape + CC hooks (+ a pi extension after pi → 1.x) | a director's store resets at a new goal and the old one is a `nest:` container |
| V5 | Console org linked; key root-side; `agi-infer --batch` + `claude -p` kids via `LoadCredential`; results on `refs/spawn/…` | 50 reviews land through the batch lane in one window; one kid runs on credits; no post env contains the key |
| V6 | imap/omap/shape rows on the 24 pieces; `A*`; the outside-the-map count | the count is measured and the ladder step (report/key/enforce) is chosen from it |
| V7 | spider v0 over the pieces: change → `.t.sh` → `[red]` + fix kid | one red caught and fixed with no director turn |
| V8 | agi-turn calls `grow-check` on the index; `grow.py` retired for v4; links = `p/` symlinks (§G) on one town first | the turn check and the land check are the same bytes; `find -xtype l` = 0 |
| V9 | the season-0 seed capsule + `capsule in` init + the engine as a pinned capsule | a third project reaches a running post from an empty repo with one row |
| U1-U8 | Part I, unchanged | as listed in §7 |

Order: V0 (today, trivial) → U1 → V3 → V1/V2 → U3/U4 → V5 → V4 → V6 → V7 → V8 → U5-U8 → V9. Everything named "season 4" in
§15 stays out of this table on purpose.

---

# Part III — the owner's ten questions on reading the doc (10-23, fork)

Facts checked on the box before answering (read-only): `refs/grid/local-maxxing/node/<mint>` 5,991 + `refs/grid/node/<mint>`
3,807 refs, each a one-commit tree `node.md [+ payload/]` — a branch per node ALREADY exists, by mint id. No v4 piece writes
them (only old-setup python: grid.py, cli.py, rotate.py, stitch.py, level3.py); v4 history lives on `posts/P` + the trunk.
`agi-wt pull ID` already extracts ONE node's tiny tree (node + payload) into a RAM dir, and `agi-turn` lands each changed
node tree as ONE signed commit on `posts/P`. `refs/spawn/*` = 0 (flows designed, never run). Live nodes: experiment 2,374 ·
hypothesis 1,509 · goal 710 · build 314 · verdict 304 · idea 153 · mvp 101 · doc 89; towns: core 3,232 · local-maxxing 591 ·
streaming-suite 13 · web-app-suite 4 · sanctuary 1. Tests: 62 `.t.sh` in the trunk tree, 386 pytest files in
`extensions/agi/tests/`. Tools on the box: openssl 3.0.13, ssh-keygen, jq, awk; no `age`. pi 0.73.1 (deprecated package).

## §23 Q1 — which python is left, and can it go

What the v4 pieces still call (everything else python is the OLD setup: write.py, grid.py, links.py, spawn_gate.py 65 KB):

| python | bytes | what it does | shell/graph replacement | cost |
|---|---|---|---|---|
| grow.py (in engine-post) | 3,228 | growth-order check at turn; **imports spawn_gate.py (65 KB)** | grow-check over growth.tsv (already written for the gate) run at turn too | V7, 0 new code |
| brief.py (in engine-post) | 810 | personalized PageRank with phase e^{±i/2} over parents: edges, 30 iterations | §G walk (symlinks) + `agi-brief` as a word walk (§12); until then keep it: it is one numeric kernel | after §G |
| the seal `$y` in agi-out | ~900 | X25519 + ChaCha20-Poly1305 via python `cryptography` (capsule secret wrap) | **age with ssh recipients**: `age -R <post>.pub` / `age -d -i id_ed25519` — the post's ed25519 key becomes the seal key; one fewer keypair, one static binary, 0 python | V3 (capsule out) |
| alarm_spool.py, xai-proxy (root side, /opt/agi/bin) | — | alarm spool; xai proxy | spool = `systemd-cat` + a path unit; proxy = not needed once the harness cell carries the provider | U8 |

Key generation and hashing are ALREADY shell: `ssh-keygen -ted25519`, `git hash-object`, `sha256sum`, `openssl dgst`.
`openssl enc` cannot do ChaCha20-Poly1305 (no AEAD on the CLI), so the seal's honest shell replacement is `age`, not
openssl. After V3 + V7 + §G the v4 engine has zero python; the old setup's python stays only for the <4 posts and dies
with them (the §16 season-0 seed carries none of it).

Rule to write down: **a piece may contain python only when it is a numeric kernel with no shell equivalent, and then it
is ≤1 KB with no imports outside the stdlib.** brief.py passes; grow.py fails (65 KB import); the seal fails (`cryptography`).

## §24 Q2 — one spawn path

Agreed, and §5 already says it for moves; make it total: **every change of a post's shape is `capsule pack → row → tick
→ in`** — stand-up (pack = the seed), rename (pack with a new `slot`), box move, branch move (pack with a new `at`), parent
spawn, kid spawn. The only variable is the MANIFEST (§3): `scope` (what it may write) · `reach` (what it may read) · `at`
(where it lands) · `pull` (**the one setting you asked for**: `graph | director | none`).

```
pull: graph     the capsule may `agi-wt pull` any node inside its scope cert        (posts, directors)
pull: director  it pulls nothing; it asks its director by box (adjacency ≤1 is already the rule), and a
                sibling kid by box through the director's ring                       (parents, kids)
pull: none      one inference request, no tools, the package IS its world            (K2(b), batch lane)
```
The K classes (K1 minted keys, K2(a) tool-loop uid, K2(b) no-tool request) stop being code paths and become the three
values of one cell. `agi-kid` and the dispatch skill collapse into `agi-in <capsule>`; what differs is the row the
capsule carries. Done-when: one verb, three MANIFEST values, `grep -c 'case.*K[12]' ~/bin/*` = 0.

## §25 Q3 — the grid as the monolith, a branch per node, posts as slices

Your vision is the inversion of what runs today, and the pieces are closer than the doc said:

```
today (v4)    posts/P (whole tree)  ──agi-turn──▶  one commit per changed node ON posts/P  ──land──▶ trunk
              refs/grid/<mint>: written by the old setup only; stale for v4 work
vision        refs/grid/<mint> (one tiny branch per node, the ONLY history)  ◀──land (ff per node)──┐
              post package = a LIST OF MINTS + scope cert  ──compose──▶ posts/P = a VIEW (scratch)  ┘
```
Mechanics, all plain git:
- **compose** (at `capsule in`, and at every `agi-wt pull`): for each mint in the package, `git read-tree --prefix=.agi/n/<mint>/
  refs/grid/<mint>` into a temp index, `write-tree`, one commit = the post's view. The §G layout (`.agi/n/<mint>/`) IS this
  checkout; `<type>/<id>.md` becomes a symlink into it, so every reader keeps working. 5,000 read-trees ≈ seconds.
- **dynamic pull**: a mint outside the package but inside the scope cert → compose adds it (`pull: graph`); outside the
  cert → refused by `check` (§2), the refusal line names the cert.
- **land** = split, not merge: each changed `.agi/n/<mint>/` tree → one commit on `refs/grid/<mint>`, parent = the tip the
  post pulled (recorded in `.b`, as agi-wt does now). Tip unchanged → ff. Tip moved → **a non-standard merge**: the land of
  that one node is held, a `merge` row is minted (both tips, the base, the diff), and a spider takes it (§27). Everything else
  in the land goes through. No whole-tree merge ever again; `agi-sync` (merge trunk into posts/P) becomes recompose.
- **the post branch** stays as scratch and as the one place a WHOLE-tree reader (a harness, `git grep`) looks; it is
  rebuilt from the grid, never the other way round. The trunk = the composed view of ALL mints = a cron-free derived ref.
- **history**: one monolithic grid, 9,798 refs today, ~30 k at season 4; git handles 100 k packed refs; `git for-each-ref
  --points-at` is the only slow op (index it in `.geometry/census` once per lap).
- **the pack** (§3, g716111-44) packs the grid refs the package names, so a capsule = a slice of the one history, which
  is what you asked for: "sliced up and packed up for each post".

Jurisdictions: **spiders are the council's** (minted under council's scope cert, their lands under council's 3/3 quorum
height, §14) as **directors are the Keep's**. A non-ff merge a spider cannot settle by rule (both sides inside one scope,
both signed, no cell says which wins) goes to council as one `merge` row with the spider's recommendation; council answers
by landing one side or minting a third commit. Red-team spiders (abliterated / uncensored models via openrouter) run as
`pull: director` kids under their own uid with scope = `refs/spider/red/*` only, never a land; what they find is a
`finding` row that the engine spider converts to a test (§31). Their harness cell carries `red: true` so nothing they
emit is ever briefed to a post as instruction.

Order: this is **V3' = compose/split**, between V3 (capsule out) and V1/V2; it replaces agi-sync's merge and makes U6
(move) trivial (a move = recompose at the new `at`). Done-when: `git log posts/P` is empty after a recompose; every node
edit is visible as one commit on its `refs/grid/<mint>`; `agi-sync` is 0 bytes.

## §26 Q4 — MCP as the one render surface, panes, mixed harnesses

Yes to one surface, no to "MCP in a pane". MCP is a protocol over stdio/HTTP, not a terminal; what goes in a pane is a
**front**. Keep §2's shape: ONE api module (`view`, `walk <word>` (§12), `brief`, `send`, `land`, `check`) and three fronts
over it, nothing else:

| front | who uses it | wake (live updates) |
|---|---|---|
| CLI (`agi …`) | shell harnesses: claude-code, codex, pi, a human | fifo `%t/agi-%i/i` (keep, the fallback) |
| MCP (stdio or HTTP) | claude-code, codex, **pi ≥1.0 (native MCP, Codemode; `.pi/mcp.json`, `--no-mcp`)** | a `wake` tool the post polls; do NOT depend on `notifications/resources/updated` — a 2026-04 issue reports CC drops it silently, closed 05-24 without a stated fix; test on 2.1.295 before any cell relies on it |
| pane (a REPL on the api, in tmux) | shell-less harnesses: grok bot, a chat bot, a browser | the fifo pushes lines into the REPL; the bot reads the pane (tmux `capture-pane`) |

Collaboration across fronts is free because the fronts share no state: the graph, the box and the chain heights are the
state; an MCP post and a fifo post see the same `refs/box/P/TO`. "MCP posts and non-MCP posts collaborate" needs nothing
but the harness cell saying which front a post has. Done-when: `codex`, `claude`, `pi` each land one node through
their front on the same leaf in one lap.

## §27 Q5 — a mint id for every post, kids included

Yes: this is §9 in its final form. A post IS a node: `refs/id/<mint>` is its chain, `posts.md` row = its address
(derived, may change), the Unix uid = the `slot` piece. A rename changes the address and nothing else, exactly the node rule
(CLAUDE.md "Two identifiers"). Parents and kids: **their flow ref IS their chain** — `refs/spawn/<flow>/<i>-<sha12>` already
hashes (flow, i, ARGS, prev); give it the §9 piece tree and every spawn is a graph entry with no second mechanism, updated
live by the flow itself (step i+1 appends). What a kid inherits is a MANIFEST line, not a mechanism:

```
slot:  inherit         → runs in the director's uid, home and worktree (RAM tree under $RUNTIME_DIRECTORY/wt)
scope: ⊆ director's    → the attenuation cert (§Z2) is the proof
cred:  inherit | <capsule-cid>   → the director's login, OR a different capsule = a different subscription
```
`cred` is the "beside the pull setting" cell you asked for: a second Max subscription is a second secret capsule, named
per row. Caveat that stays true: a kid in the director's uid can read the director's credential, so `cred: <other>` with
`slot: inherit` is a contradiction the check refuses — a different login needs its own slot (one DynamicUser). Done-when:
`posts.md` has a `mint` column, the census counts spawns as nodes, a rename is a one-line address change.

## §28 Q6 — the plugin

Do it: U7 is one directory with three manifests over the same files: `.claude-plugin/plugin.json` (skills, hooks, the
MCP server), `.codex-plugin/plugin.json` (Codex plugins since 2026-03: skills + `.mcp.json` at the plugin root, marketplace
at `.agents/plugins/marketplace.json`, cached under `~/.codex/plugins/cache`, no hot reload), `.pi/mcp.json` for pi ≥1.0.
`skills/` stays where it is; the api module is the MCP server for all three. The move tooling's `known_marketplaces`
rewrite dies here (Part I already said build nothing more on it). Done-when: `claude plugin validate`, `codex plugin list
--json` and `pi /mcp` each show the one plugin from the same commit.

## §29 Q7 — directors, parents, kids: who spawns what

Keep the parent, but **as a flow, not a model**. A flow (`refs/spawn/<flow>`) is a script-run chain: step i ends by
appending step i+1, which is exactly "kids automatically launch the next kid until the director's permission is exhausted"
— the stop condition is the scope cert, not a counter. A model-parent spends tokens on decomposition that the director
already did when it sketched leaves (agi-goal §5). So:

```
director  sketches leaves (judgement)           ──▶ mints ONE flow per leaf: steps = nodes to write, scope = leaf
flow      step i = one kid, one node, smallest model that passes the leaf's falsifier; ends by appending i+1
spider    (§31) reviews on red/mismatch only; lands; tells council only on a held merge or a veto
```
A model-parent remains legal as a step kind `plan` inside a flow (for a weak director), never a standing post. Batching:
only `pull: none` steps batch (50 % off, ~1 h); a tool-loop kid cannot. The matrix view: the flow's next step is
`T · e_i` (§12's transition matrix), a spider is a step kind `review`, so "one node calls the next kid" is the same
chain. Done-when: `refs/spawn/*` > 0 (today 0); one leaf lands end-to-end with zero parent-model tokens.

## §30 Q8 — pi back, now, and the A/B you asked for

Move pi up the order: **P1 right after V0**, because it lifts parallelism everywhere else (headless pi ≈ tens of MB; a
kid is one process). Steps: install `@earendil-works/pi-coding-agent` 1.x in a side prefix (`npm --prefix ~/pi1`), point
`agi-kid` at it through the harness cell (`pi1`), keep 0.73.1 for nothing. pi 1.x brings native MCP (§26) and the optchat
extension (§11). Credentials: pi's `anthropic` provider takes the Console key → **the $200/month credits lane**; the same
kid row with `provider: openrouter` is the comparison. Gather, per kid, on the town board (numbers only, one line per lap):
`model · $/landed node · s/landed node · red rate`. Models for the openrouter arm, verified 10-23:

| id | $/M in / out | note |
|---|---|---|
| `deepseek/deepseek-v4.1-flash-1017` | 0.15 / 0.60 | 10-17 snapshot, 1 M context; some routes list 0.30 / 1.20 — check live |
| `z-ai/glm-5.3` | 1.40 / 4.40 (cache read 0.26) | reasoning always on, 1 M context, 32 providers |
| Claude lane via Console key | Haiku 5.5 0.05 / 0.25 batch · Sonnet 5.5 1 / 5 batch | credits, not cash |

The provisioning key (OpenRouter `OPENROUTER_PROVISIONING_KEY`, goal:g1.11) mints a per-kid key with a $ cap → K1 is
the right class for the openrouter arm; no kid ever sees the long-lived key. Done-when: 2 arms × 1 leaf × 10 kids on the
board with the four numbers.

## §31 Q9 — tests: neither "do away" nor "gate"; move them

Keep every test; move WHEN it runs. Today 62 `.t.sh` + 386 pytest files run at gate/land time, i.e. the post waits. Under
spiders: a region's tests run **on chain-height change in that region**, by the region's spider, in the background; the
result is one line on the town board (the coordination surface you named) and a `red` row on the node; the land gate reads
the latest verdict for the touched nodes instead of running anything (a stale verdict = run it then, so correctness holds;
speed is the common case). "No more waiting" = the suite is already green by the time a post lands. The engine's own
pytest suite becomes the `engine` region's tests. Done-when: the gate's wall time < 1 s; the board shows one test line per
region per lap; no `.t.sh` is deleted.

## §32 Q10 — territories: no coordinates needed; a smell walk

The graph has no coordinates (one `temp-coord-board` scaffold hash is all), and it does not need them: **graph distance is
the coordinate**. Two layers:

1. **Territory = scope cert** (region = type × town, e.g. `goal@core`, `experiment@local-maxxing`); overlap is bounded by
   construction (two spiders may share a region; a node is never in two regions). Sizes today: core carries 3,232 of
   3,855 town-tagged nodes — split core by type, or it is one spider's whole world.
2. **Inside a region, a smell walk** (the Boltzmann walk you described):
   ```
   smell(v)  = Σ_sources α^{d(u,v)}        sources: a new node (height rose since the spider's last visit),
                                                     a red, an IOMap mismatch; α≈0.6
   P(next=w | at v) ∝ exp(β · smell(w)) · ρ(w)   over w ∈ N(v) ∩ region, k candidates shown
   ρ(w)      = 1 / (1 + visits by OTHER spiders in the last L steps)      ← repulsion: territories emerge
   ```
   β is the greed (β=0 = uniform random walk, which alone covers a connected region in O(n·m) steps worst case); the
   spider checks every node it stands on, approaching or not. The model only chooses among `k` words (§12 alphabet:
   `up`, `down:3`, `sib:2`, `stay`), never a number. The looped script (`agi-walk <mint>`) prints the k candidates sorted by
   smell with their words; smell is awk over chain heights + red rows, no numerics library. A spider's trail (visited,
   heights seen) is its `mem: goal` store (§11), so a restart continues the walk.

Done-when: a planted red in a region is reached by its spider in < 50 steps with β=1, and two spiders in one region
overlap < 20 % of visits over 1,000 steps (measured from their trails).

## §33 the autonomous run — what the keys need (owner: "provide the claude cloud keys as well as that provisioning key")

Three rules so the team can test on its own without a key ever reaching a prompt or a post env:
- **Where**: each key is a root-owned file under `/etc/credstore/` (mode 600), delivered only by `LoadCredential=` on the
  unit that needs it; never `Environment=`, never a post's env, never the repo (config:secrets forbidden_keys stays).
- **Which unit**: the Console key → the `agi-infer --batch` lane and `claude -p` / pi `anthropic` kids (§13); the OpenRouter
  provisioning key → `provisioning.py`'s successor only (K1 mints per-kid keys with a $ cap; the kid gets the minted key,
  never the provisioning key). A post that asks for a key by name gets the `[root] held … owner-gate` line (§14).
- **Kill**: one cell `credits_live: false` in `.geometry/secrets` empties both lanes at the next tick (the same shape as
  `crons_live`); the owner flips it, nobody else.

Autonomy order (adds to §22): **V0 → P1 (pi 1.x) → U1 → V3 → V3' (compose/split) → V1/V2 → V7 (python out) → U3/U4 → …**.
Season-close picks from §15 still stand.

## §8c sources for Part III
- DeepSeek V4.1 Flash 1017 on OpenRouter: https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017 · https://openrouter.ai/compare/deepseek/deepseek-v4.1-flash-1017 · (conflicting 0.30/1.20: https://computeprices.com/providers/deepseek/models/deepseek-v4-1-flash)
- GLM 5.3 on OpenRouter: https://openrouter.ai/models/z-ai/glm-5.3 · https://openrouter.ai/z-ai/glm-5.3/benchmarks
- pi 1.0 native MCP (Codemode), `.pi/mcp.json`, `--no-mcp`: https://pi.dev/changelog/releases/1.0.1 · https://pi.dev/changelog/releases/1.0.4 · https://www.developersdigest.tech/blog/pi-1-0-release-guide-mcp-codemode-pi-durable
- Codex plugins (`.codex-plugin/plugin.json`, skills + `.mcp.json`, marketplaces, cache, no hot reload): https://codex.danielvaughan.com/2026/03/30/codex-cli-plugin-system · https://codex.danielvaughan.com/2026/04/12/building-codex-plugins-architecture-manifests-distribution/ · https://codex.danielvaughan.com/2026/04/11/codex-marketplace-plugin-distribution/
- Claude Code and `notifications/resources/updated` (dropped silently; issue opened 2026-04-14, closed 05-24): https://claudeissues.com/issue/47823-mcp-notifications-resources-updated-not-handled-per-spec
- age with ssh-ed25519 recipients (`-R`): https://github.com/FiloSottile/age

## §34 round three — the owner's rulings on §23–§33, folded in (10-23)

Checked first: the box's council = {alive, all-is-one, self-perpetuating} (posts.md; personas = vision:alive, vision:all-is-one,
vision:self-perpetuating). **No council post is named anti-fragile**; the word appears once, inside vision:alive's body. Reading: the
owner's "anti-fragile" post = **self-perpetuating** (what perpetuates under stress is antifragile), since the other two posts
were named explicitly. If a fourth council post was meant, it is one row in posts.md and one key in the ring; the design below is the
same either way.

### §34.1 three spider families, one per councilor (Q3 ruling)
All spiders are regular spiders (§18, §32: region, smell walk, act on red/mismatch, council scope certs, lands under the 3/3
height). Each councilor's post owns a family — its flow prefix, its scope cert, its smell sources:

| councilor | family | smell sources (what raises P(approach)) | what a hit becomes |
|---|---|---|---|
| **self-perpetuating** (anti-fragile) | **red** — the council's secret service: pen-test a READ-ONLY compose of the system to make it antifragile ("if we don't, someone else will") | every new piece version, every new front (CLI/MCP/pane), every gate, every cert | a `finding` row → a test (§31) → a fix flow; never a land by the red spider itself |
| **all-is-one** | **unify** — siloed processes and nodes | duplicate nodes (same title/falsifier, two mints), two scripts doing one thing, a non-ff `merge` row (§25), a broken link | a `merge` row with a recommendation, or a fix flow that retires one of two |
| **alive** | **tune** — the system hyper-optimized to itself | cost per landed node, lap time, memory per post, smell-walk overlap, stale `mem:` stores, idle units | a parameter change as one cell edit (β, α, k, budgets), with the before/after numbers on the board |

Red's read-only guarantee, mechanically: a red spider runs under its own uid (`slot: own`, never inherit), `scope =
refs/spider/red/*` only, `reach` = a recompose of the whole grid at a fixed height (`refs/red/<height>`), **no box send to
any post** (its ring lists only its councilor), no land cell. It attacks pieces, fronts and gates in that view; the model may be
abliterated/uncensored (openrouter) because nothing it emits is ever briefed as instruction (`red: true` in the harness
cell, §25). The councilor's own key signs the family's lands cell; an action that crosses families (a red finding that
becomes a fix flow in a Keep director's region) needs the 3/3. Done-when: three flow prefixes `refs/spawn/spider-{red,
unify,tune}/*` exist, each with ≥1 run; a planted vulnerability in a test piece is found by red in one lap and closed by a
fix flow in the next.

### §34.2 Q7 ruling
Parents-as-flows go through the one route: a flow step = `agi-in <capsule>` with `pull: director`, nothing else. The flow
script never spawns by any other verb. (`grep -c 'pi \|claude ' flows/*` = 0 outside agi-in.)

### §34.3 Q8 ruling — the cheap GLM
The owner meant the flash model. On OpenRouter (10-23, aggregator figures, check the live page before the cell is written):

| id | $/M in / out | note |
|---|---|---|
| `z-ai/glm-5.3-flash` | ≈0.075 / 0.25 (one aggregator 0.09 / 0.30; Z.ai direct 0.15 / 0.50) | the cheap arm; OpenRouter's own page did not surface in search |
| `z-ai/glm-4.7-flash` | 0.06 / 0.40 (cache read 0.01) | cheaper on input-heavy work |
| `deepseek/deepseek-v4.1-flash-1017` | 0.15 / 0.60 | §30 |

The §30 A/B becomes three arms: Console-credits (Haiku 5.5 batch 0.05 / 0.25) · glm-5.3-flash · deepseek-flash-1017, one
leaf × 10 kids each, four numbers on the board. The expensive `z-ai/glm-5.3` (1.40 / 4.40) is a `plan` step model, not a kid.

### §34.4 Q9 ruling — two loops, in parallel, never sharing a gate
```
BUILD lane (the Keep)   director → leaf → flow → kids → land        designs and builds; IOMap on the hypothesis (§19)
REPAIR lane (council)   spider → red/gap/mismatch → fix flow → land   closes gaps, fixes tests, unifies, tunes
```
Coupling rules, so neither lane waits on the other:
1. **No shared gate.** A build lands with the latest verdict (§31); a spider never blocks a land, it marks (a `red` row).
2. **Separate budgets.** `spawn_budget` becomes two cells, `build:` and `repair:`; a storm of reds cannot starve a build
   and a big build cannot starve repair. Alive's tune spiders may move the split, with the numbers.
3. **Hand-off only through rows and height.** A red row raises smell (repair picks it up); a fix flow's land raises the
   node's height (the builder sees it at its next `agi-wt pull`, which recomposes).
4. **Claims are the lock.** `refs/claims/<user>` already exists (agi-brief reads it). A spider never fixes a claimed node:
   it leaves the red row and the smell, and moves on; the builder's land then carries the fix or gets the `held` line.
   No priority inversion, no merge war.
5. **Two numbers per lap on the board**: build = landed nodes / lap; repair = reds closed / lap + mean red age.
Done-when: both numbers rise in the same lap on one town, with `build:` and `repair:` budgets both saturated at least once.

### §34.5 the census under the grid inversion (owner: count active/latest only; old versions as deprecated?)
Count **mints by their tip**, never versions. Today's numbers, read on the box:

| what | number |
|---|---|
| live node files (`.agi/nodes/<type>/`) | 5,700 |
| deprecated node files (`deprecated/<type>/`) | 245 |
| grid refs | 9,798 — but all 3,807 `refs/grid/node/<mint>` also exist under `refs/grid/local-maxxing/node/<mint>` |
| unique mints in the grid | 5,991 |
| mints with no file in the view (5,991 − 5,945) | 46 — to be explained before the census cell is trusted |
| deprecated tips, sampled 300 | 14 (≈4.7 %, consistent with the 245 files) |

Rule: **a version is a commit on the mint's ref, not a node** (CLAUDE.md: "never a second node file"). Labeling old versions
deprecated would mint nodes that never existed and would inflate the deprecated count by the version depth. Instead the
census cell carries five numbers, each one git command:
```
mints    = |refs/grid/*|                          (one namespace: refs/grid/<mint>; the town is a cell in node.md)
live     = tips whose status ≠ deprecated          (git cat-file --batch over the tips, grep)
retired  = tips whose status = deprecated          live + retired = mints, never drops
versions = Σ commits over all refs                 only grows; depth per mint = its age in edits
orphans  = mints with no path in the composed view (must be 0; today 46)
```
Consequence worth deciding: under the inversion the `deprecated/<type>/` directory is a **view** derived from the tip's
status by compose, not a place the writer moves a file to; CLAUDE.md's "status and place agree" check becomes a compose
invariant rather than a writer rule. Readers that glob `deprecated/` keep working. The two grid namespaces merge once
(a ref rename, 3,807 duplicates dropped, history kept) as the first step of V3'.

### §34.6 porting the python — the safety rule
Yes, port the rest, one piece per commit, each with the same shape of proof:
1. a `.t.sh` **differential test**: the old python and the new shell run on the same fixtures (≥20 real inputs from the
   grid), output diffed byte-for-byte; the test is the land gate for that commit;
2. **shadow for one lap**: the shell runs beside the python at every call, logs any disagreement, the python still decides;
3. **flip** when the lap shows 0 disagreements (one cell: `impl: sh`); the python stays in git, never deleted.
Order and risk: grow.py (grow-check exists; lowest risk) → the seal (`age` from apt, ssh-ed25519 recipients; test a
round-trip on one capsule, then V3) → brief.py (awk port of the complex power iteration, 2 numbers per node; or skip
straight to the §G walk) → alarm_spool / xai-proxy (root side, with the Prime, under §14).

### §34.7 the order, final for this round
V0 → P1 (pi 1.x) → U1 → V3 (capsule out, age seal) → V3' (namespace merge, compose/split, census cell) → V1/V2 → V7
(grow.py out, differential) → spider families (red · unify · tune) → U3/U4 → V5 → V4 → V6 → V8 → U5–U8 → V9.

## §8d sources for §34
- GLM 5.3 Flash / 4.7 Flash on OpenRouter: https://openrouter.ai/compare/z-ai/glm-5.3-flash/google/gemini-3.6-flash · https://www.getmaxim.ai/bifrost/model-library/compare/openrouter/glm-5.3-flash.md · https://openrouter.ai/z-ai/glm-4.7-flash · https://anotherwrapper.com/llm-pricing/glm-5.3/glm-5.3-flash

## §35 posts, never seats (owner 10-23, verbatim)
> "I want them to always be called posts not seats. We stand guard at our post to make sure the work is quality and the graph
> is always used as the main everything surface like coordination, comms, and chains are grown correctly. So anywhere that is
> called seats or seat.sh or whatever should be called posts. No seat reference anywhere. We stand at our posts, proactively
> monitoring and maintaining the graph. We do not sit around idly waiting for tasks to arrive."

Two rules fall out, one lexical and one behavioural.

**V10 — the rename.** On the trunk today (read 10-23): 2,906 files contain "seat"; `AGI_SEAT` has 830 references in ~190
files (engine-root, engine-wrap, posts.md, tests, nodes); `extensions/agi/bin/seat_status.py` exists; tests are named
`test_rotate_main_seat_rows.py`, `test_session_start_seat_pre_spawn.py`; rotation records end in `.seating.json`. A hypothesis
`l4-a-seat-is-a-post-everywhere` already made this ruling once, and the word came back — so the leaf is not a sweep, it is a
sweep **plus a standing check**:
- `AGI_SEAT` → `AGI_POST` everywhere it is set or read (engine-wrap R6 already records the two-variable mismatch: the unit
  sets one, the box piece needs the other; the rename removes the mismatch instead of bridging it); `seat_status.py` →
  retire (its job is the census cell, §34.5); test files renamed in the same commit; `.seating.json` and every node under
  `deprecated/` are history and are NOT rewritten (git history is the archive).
- Falsifier: `git grep -ilw 'seat\|seats\|seating' -- . ':!.agi/nodes/deprecated' ':!.agi/sessions/rotations' ':!datasets' | wc -l`
  = 0 on the trunk, and the same line is a **unify-spider test** (§34.1) in the engine region, so a regression is a red
  within one lap, not a ruling made twice.
- Wording in this doc is already scrubbed (council **posts**, councilors, "post theft" for the `-c` bug).

**The posture, as mechanism.** "We stand at our posts … we do not sit around idly waiting" is the spider walk (§32) made
the default state of EVERY post, not a spider specialty: a post with no claimed leaf walks its own region (its scope cert),
checks every node it stands on, and acts on red/mismatch, exactly as a spider does; a claimed leaf is a longer step in the
same walk. So there is one idle state in the engine and it is "walking", never "waiting": `agi-walk` is what a post runs
between turns, the fifo/MCP wake interrupts the walk, and the keepalive/CHECK prompts of today become unnecessary (the walk
is the heartbeat). The three spider families (§34.1) are then posts whose region is a *concern* (red, unify, tune) instead of
a town. Done-when: no post unit logs an idle interval > one lap without a walk step; CHECK/keepalive prompts are retired.

## §36 the Console service-account key, prompt caching, and the intake (owner 10-23)

Owner: service account `prime-director`, key `prime-key`, stored in Doppler project `agi` as `CLAUDE_CONSOLE_SP_KEY`; Console
warning: the key is org-wide (not tied to one workspace), works on any Admin API endpoint the account can reach, and every
non-Admin request must carry `anthropic-workspace-id`. Read on the box: `doppler` v3.76.5 is installed here (this box is the
secrets hub the graph calls encryption-town; hostname <host>); the engine calls Doppler nowhere (secrets reach it as
`<source_root>/.env`, mode 600, per config:secrets); `/etc/credstore` exists and is empty; root has no Doppler token yet
(`/root/.doppler` is empty; the owner's user has one). The fork did not read the key or Doppler.

### §36.1 what the key is, verified on the official pages (quotes in §8e)
- **Identity-backed, dual-use.** A service-account key "acts as" the service account and works "in either a single workspace or
  anything the service account has access to, chosen when the key is created". It is accepted on the Messages API and on
  workspace-scoped resources including **Message Batches**; the Admin API accepts it "only if the key isn't scoped to a specific
  workspace". Sent as `Authorization: Bearer` (legacy `x-api-key` still works).
- **The header.** An unscoped key must send `anthropic-workspace-id: wrkspc_…` on every non-Admin request: missing → 400
  `invalid_request_error`; malformed → 400; a workspace the account cannot reach → 404 `not_found_error`. The workspace id is
  in the Console's Workspaces page, in List Workspaces, and in the `anthropic-workspace-id` response header of any call.
- **It does NOT mint keys.** Admin API FAQ, verbatim: "Can I create new API keys through the Admin API? No. You create API keys
  in the Claude Console. The Admin API can only read, rename, and change the status of existing keys." So the OpenRouter
  provisioning analogy fails for API keys. The real analogue is **Workload Identity Federation**: an OIDC JWT is exchanged at
  `POST /v1/oauth/token` for a short-lived `sk-ant-oat01-…` token (60 s–24 h, default 1 h), scoped to one workspace at exchange
  time, "no `sk-ant-api…` string to mint, distribute, or rotate". Prerequisites: a service account, a federation issuer, a
  federation rule — i.e. an identity provider that issues JWTs. **Not needed for batching** (no page links the two; "API keys
  and Workload Identity Federation grant the same access to Claude API endpoints"). Your instinct is right: WIF is the per-kid
  short-lived credential of season 4, when a post has an issuer (the box's own OIDC endpoint, or GitHub Actions' issuer, which
  the seal workflow already uses).
- **Caps live on workspaces, not keys.** "You can set custom spend and rate limits for each workspace" (monthly spend; RPM,
  input/output TPM), lower than the org's, "not on the Default Workspace". A service account reaches the Default Workspace plus
  the workspaces it is added to. Credits per org vs per workspace: **not stated** on any of the four pages.

### §36.2 the design: one key for root, one workspace per lane
```
Console (owner, once)   workspaces  agi-batch · agi-kids · agi-council   each with a monthly spend limit + TPM caps;
                        add prime-director to each; note the three wrkspc_ ids (NOT secrets → cells in config:secrets)
                        OPTION B (fewer moving parts): one workspace-SCOPED service-account key per lane, created in the Console;
                        a scoped key needs no header anywhere (claude -p, pi, curl all just work)
root (this box)         Doppler → /etc/credstore/claude-sp   (0600 root)   by a root timer `agi-cred` running
                        `doppler secrets get CLAUDE_CONSOLE_SP_KEY --plain --project agi --config <cfg>`
                        with a read-only Doppler SERVICE TOKEN held in /etc/credstore/doppler-token (the one manual step: root
                        has no Doppler token today; the owner's user does)
units                   LoadCredential=claude-sp:/etc/credstore/claude-sp on the lane units only; the file appears at
                        $CREDENTIALS_DIRECTORY/claude-sp; never Environment=, never a post's env, never the repo
lanes                   agi-infer --batch (curl: `-H "anthropic-workspace-id: $W"` + `Authorization: Bearer $(cat …)`)
                        pi kids: models.json provider `claude-lane` {api: anthropic-messages, headers: {anthropic-workspace-id},
                          apiKey: "!cat $CREDENTIALS_DIRECTORY/claude-sp"}  ← pi resolves `!cmd` at request time: no env var at all
                        claude -p kids: ANTHROPIC_CUSTOM_HEADERS="anthropic-workspace-id: $W" (format `Name: value`; verify
                          once on 2.1.295 that the header reaches the API and that credits are drawn), key from the credential
                          file via the kid unit's wrapper — a kid unit, not a post (config:secrets forbidden_keys stays for posts)
measurement             the org-wide key's Admin-side read access = the Admin API usage/cost reports grouped by workspace →
                        the board's `$ per lane per lap` comes from the source of truth, not from counting tokens ourselves
                        (verify the report endpoint names on the Admin API page before the cell is written)
kill                    `credits_live: false` in config:secrets → agi-cred removes /etc/credstore/claude-sp and restarts the lane
                        units at the next tick; the owner can also set a workspace's spend limit to 0 or archive the key
```
Least privilege: the org-wide key is **root's only** (it can list every workspace's keys and change their status; its reach
is the service account's org role — check that `prime-director` is `developer`, not `admin`, unless the cost reports need
admin, in which case only root ever holds it). Kids never see it: they get the lane's scoped key (option B) or the credential
file of their own lane unit. The Doppler service token is read-only on the `agi` project's one config.

### §36.3 prompt caching — two modes, where each goes
Official (§8e): **automatic** = one top-level `cache_control` on the request; the breakpoint lands on the last cacheable block
and moves forward as the conversation grows. **Explicit** = `cache_control` on individual blocks, up to 4 breakpoints, 20-block
lookback; both can be mixed (automatic uses one of the 4 slots). TTL 5 min by default, 1 h at 2× write; writes 1.25× (5 min) /
2× (1 h); reads 0.1×, and 0.05× on Opus 5.5 and Sonnet 5.5; a minimum token count applies; a cache entry exists only after
the first response begins, so parallel kids must wait for the first before fanning out. Caching works inside batches (§13).

Where it goes in the engine: only `agi-infer` builds requests by hand (the harnesses cache on their own). Its request order is
tools → system → messages, prefix-matched, so: **system = the piece set + scope cert + brief (stable per flow → one explicit
breakpoint, 1 h TTL for a flow that runs longer than 5 min); messages = the node (varies, after the breakpoint)**. A flow of k
kids over one leaf then pays the piece set once and reads it k−1 times at 0.05–0.1×. For the parallel fan-out: step 1 of a
flow runs alone, steps 2..k fan out — a one-line rule in the flow script. Done-when: `cache_read_input_tokens` > 0 on step 2
of a flow in the board's cost line.

### §36.4 leaves added
- **C1 agi-cred**: root timer, Doppler → credstore, kill cell; done-when the lane unit sees `$CREDENTIALS_DIRECTORY/claude-sp`
  and `grep -r sk-ant /proc/<post pid>/environ` is empty for every post.
- **C2 workspaces + cells**: three workspaces with limits, their ids as cells, `prime-director` a member of each.
- **C3 the three fronts send the header** (or option B scoped keys): agi-infer, pi `claude-lane`, `claude -p` with
  ANTHROPIC_CUSTOM_HEADERS; one request each, the response's `anthropic-workspace-id` header equals the lane's cell.
- **C4 cost line from the Admin API** per workspace per lap on the board.
- **C5 caching breakpoint in agi-infer** (§36.3).
Order: C1 → C2 → C3 fits before P1's A/B (§30/§34.3), since the credits arm needs them; C4/C5 beside V3.

## §8e sources for §36
- Authentication (key types, service-account key, header, errors, WIF overview): https://platform.claude.com/docs/en/manage-claude/authentication
- Admin API (FAQ "Can I create new API keys through the Admin API? No."; list/update only): https://platform.claude.com/docs/en/api/administration-api
- WIF reference (`POST /v1/oauth/token`, `sk-ant-oat01-…`, 60–86,400 s, workspace-scoped at exchange): https://platform.claude.com/docs/en/manage-claude/wif-reference
- Workspaces (spend + rate limits per workspace, not on Default; Batches are workspace-scoped; response header): https://platform.claude.com/docs/en/manage-claude/workspaces
- Prompt caching (automatic vs explicit, TTLs, multipliers, 0.05× on Opus 5.5 / Sonnet 5.5): https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- pi models.json (`headers` per provider, `apiKey` as `$ENV` or `!cmd`): https://cdn.jsdelivr.net/npm/@earendil-works/pi-coding-agent@0.81.1/docs/models.md
- Claude Code `ANTHROPIC_CUSTOM_HEADERS` "Name: value" (third-party gateway doc; verify on the official env-var page): https://docs.opper.ai/integrations/coding-agents/claude-code

## §37 optmem for the Prime = an intake ledger with a closure invariant (owner 10-23)

> "Trajectory holds the momentum data, optmem holds the state/location data." · "if I fire off a stream of ideas … some of
> the smaller points of said brainstorm inevitably slip through the cracks."

**The evidence, from this very doc.** A grep of the doc for ~40 small points in your three long messages (10-23): 0 hits for
"self-improve" (dropped outright); "daisy-chained hashes", "filesystem-like MCP by post identity" and "a location in a matrix
space" are covered only under other words (§10 chain height, §6 visitor, §12/§32); one hit each for "Belam to Fable
permanently", "jev", "assembly/inverse", "import other projects", "auto-start". A careful 1,000-line answer still lost one atom
and thinned five. The brief/recall side (§11) is not where the crack is; **intake** is: nothing today forces every atom of an
owner message into a terminal state.

**The mechanism (graph-native; OptMem's four verbs map onto it 1:1, no second store):**
```
intake node   one per owner message (or long brief): the verbatim, split into numbered ATOMS, one ask per atom
              type intake (or doc kind: intake); parents = town + the thread; part of the Prime's `mem: always` store
atom state    open → leaf:<goal id> | decision:<§21 n> | folded:<atom> | deferred:<season> | declined:<reason> | done:<sha>
              (a closed set; anything but `open` is terminal)
wake          what the Prime's session starts with = the open atoms across its live intake nodes
              (SessionStart hook for claude-code, session_start for pi — the §11 adapters), oldest first
recall        regex over intake nodes (OptMem's recall, no embeddings)       zoom = open the atom's verbatim
note          append an atom (a new throw lands as one more intake node, or one more atom on the open one)
```
- **State vs momentum.** The ledger is position: where each atom is. The town node's TRAJECTORY section + the board's metrics
  line are momentum: Δ per lap. The Prime's brief = seeds ∪ open atoms, with an atom's **age as its α weight** (§11), so the
  oldest open atom is the loudest and nothing starves.
- **The invariant.** An intake node with an `open` atom older than one lap is a red → the unify spider's smell (§34.1) → the
  Prime's wake carries it until it is terminal. No loop close and no season close while a live intake node has an open atom
  (the same shape as "close on the falsifier as written").
- **Independence.** An atom that fits under an existing goal → the Prime mints the leaf itself (agi-goal §5 nesting), no
  round-trip; banked only when it needs a new top-level goal, spend the owner did not name, or an irreversible act
  (CLAUDE.md delegated authority, unchanged). That is "keep throwing things": one throw = one intake node; the Prime closes it.
- **Who splits.** The Prime at receipt (naming, §12 — the thing a model is good at), or a `pull: none` kid flow on Haiku
  batch for a long message; the split is checked by count: atoms ≥ the message's imperative sentences, or the spider marks it.
- **Why not OptMem itself.** Its memory dir is files without parents, signatures or a census; an intake node is the same
  information inside the chain, and `wake`/`recall`/`zoom`/`note` are a hook, a grep, a read and a write. The optchat shape
  (§11) is still right for the *chat*; the ledger is for the *asks*.

**Leaves.** M1 intake node shape + the split flow · M2 the wake hook (open atoms at session start) · M3 the spider test (open
atom > 1 lap = red; close blocked) · M4 age-weighted seeds in the brief · M5 THIS brainstorm's ledger (intake-ledger.md, sent
with the doc) committed by the Prime as the first intake node — its first step on hand-back, before any leaf. Order: M1–M3
right after V0; they protect every other item in the order. Done-when: a 30-atom test message reaches all-terminal within
two laps with zero owner reminders; the grep in the first paragraph of this section returns no zero.

Folded now, so this section does not repeat the crack it describes: **self-improve** = the tune spider family (§34.1) over
the IOMap loop (§19): the system measures itself per lap and changes one cell at a time → `folded: §34.1 tune`.

## §38 do intake nodes pile up? No: one per post, replaced whole, with four typed exits (owner 10-23)

Read on the box first: the `idea` type already exists as the pre-goal type (schema: status `open|active|extended|abandoned|
deprecated`, parents goal/vision/hypothesis; 92 open + 2 active live ideas today), build parent shapes already admit
`[goal, idea]`, spiders "mint ideas, never goals" (§18); owner rulings already have a home per level
(`doc:l4-owner-decisions`, `doc:l5-owner-decisions`, 204 lines); the card already has an outbound queue (§6 BANKED) and is
"replaced whole, every prior version in git"; the board's `metrics_line` is one numbers-only line per lap.

**The three options you floated, weighed:**

| option | live nodes per throw | atom identity | verdict |
|---|---|---|---|
| A. one intake node per post, versioned over itself; atoms added/removed | **0** (one node per post, ever) | none while open (a row), full once placed (the node it moves into) | **recommended** — it is the card's own discipline applied to inbound asks |
| B. atoms on the town board | 0 | none | the board is numbers-only by rule (progress → board, one line per lap); prose atoms would clog the coordination surface. Take ONE number from it: `intake=n` per post |
| C. every atom an idea node (recursively) | +60 per brainstorm | full | ideas have a schema (`scale`, parents) and a census cost; most atoms are rulings or corrections, not proposals. Make the idea an **exit**, not the atom |

**The shape (A, standardized for every post, not only the Prime):**
```
doc:intake-<post>     ONE node per post, replaced whole; versions on its grid ref ARE the history (zoom = git log refs/grid/<mint>)
                      body = the unplaced verbatim only: numbered atoms, each with a TARGET (what it will become) and an age (lap)
exits (closed set of 4)
  → goal:<id>         a leaf; the atom's verbatim moves into the leaf's `## OWNER <date>, verbatim` section (agi-goal §3 already
                      requires it); a big atom = a goal whose leaves are its sub-asks — recursion is goal nesting, nothing new
  → idea:<id>         a proposal not yet a goal (spiders' exit too); deferred-to-season-N = an idea tagged with the season
  → decision          one line in the level's owner-decisions doc (exists)
  → out: <reason>     declined; the reason is the THOUGHT of the removal commit — the only exit that leaves no live node
inbound/outbound      intake = asks coming DOWN (owner → Prime, Prime → director, director → kid); card §6 BANKED = asks going UP.
                      Same discipline, two directions; the card's §0 state line shows `intake=n`
board                 `intake=<n>` joins the metrics line per post per lap; Δn per lap is the momentum you named (trajectory)
invariants            (1) every sentence of an inbound message is verbatim in exactly ONE place: the intake node or a tracker
                      (goal / idea / decisions doc) — a doc node is reference, never placement; (2) intake is EMPTY at rotation,
                      loop close and season close; (3) an atom older than one lap is a red (unify spiders); (4) the node is
                      never deprecated — it empties; its grid versions carry what passed through
```
Pile-up: the live graph grows by zero nodes per throw. Closed atoms land in nodes that would exist anyway (leaves, ideas,
one decisions doc per level). Only the intake node's grid ref grows (one cheap commit per placement), and §AC's rollover
collapse folds those versions like everything else. Renders never see the queue's history unless they zoom.

**What this changes in §37 / M5.** The ledger I sent (intake-ledger.md) is `doc:intake-belam` **version 1**: its `done:§x`
states are **targets** into this doc, not closures — the brainstorm doc is reference, so an atom is placed only when the
leaf / idea / decision node exists. The Prime's hand-back then reads: commit the doc node (reference) + the intake node
(queue, 60 atoms with targets) → each V/U/C/M/P leaf minted removes its atoms → the node empties; the board's `intake=`
number for belam goes 60 → 0 over the laps, which is the one trajectory line that tells you the brainstorm landed. M1
becomes "the intake node shape + the four exits"; M3's red is "an atom older than one lap".

**For council (decision §21 #12):** A vs C is the only real choice; the recommendation is A with C as an exit. If council
prefers a richer atom (its own mint id while open), the compromise is A with atoms as `refs/grid` sub-trees of the intake
node (identity without a live node), but that is machinery §25's compose/split should land first.

## §39 atoms in the card, an atomizer kid, momentum on the board (owner 10-23)

> "each post's atoms hold the position data for that post as it relates to the momentum data in the trajectory. Each agent
> knows where they are, what they should do next, who is around them, and the momentum tells them how the whole graph is
> moving as a whole."

**§38 corrected: the atoms live in the card, not a second node.** CLAUDE.md: "A post's card is its ONE scratch … replaced
whole … a session that dies without a summary must still be resumable." A separate intake node was a second scratch; the card
is where position belongs. So: **card §7 ATOMS**, rows appended and closed line by line (the card is already written during
the work; every version is in the grid). Three things come free: rotation (the successor reads the card, so inbound asks
survive a rotation with no extra step), the brief (the card is already a seed), and history (the card's grid ref). The 100-
line cap stays for §0–§6; §7 is bounded by time, not length: an atom older than one lap is a red (§37), and the count is on
the board, so a long §7 is a load signal the Keep reads, not a rule violation. Kids have no card: their atoms ride in the
flow step's ARGS (already hash-chained), and a kid's one atom closes when its node lands.

**After ingestion, the board.** Atoms do not move to the board; they dissolve into leaves, and what remains of a throw is
momentum, which is exactly what the board holds. The TRAJECTORY section already carries "links → chain nodes", so an
ingested throw becomes ONE line there: `10-23 brainstorm (doc:<mint>) atoms=60 placed=60 → V0 V1 … M5` with the leaf ids.
The metrics line gets, per post per lap: `intake=n placed=k red=r`. Δ per lap is the momentum; the line per throw is where
the brainstorm "becomes part of the town board" once it is fully in the loop — as a record of motion, not as text.

**The atomizer: a small model that cuts, never writes.**
```
trigger    a box piece on receipt (refs/box/P/TO is a signed commit: each commit is atomized ONCE; quoted text `>` excluded)
kid        pull: none, one request on the credits lane (§13/§36): Haiku 5.5 by default (extraction, not judgement);
           Sonnet 5.5 only when Haiku marks a target `?`; the post confirms targets at its next turn
input      the message + the recipient's scope cert + its leaf ids (so targets are real ids, never invented ones)
output     kind: ask | fyi | report      (only `ask` yields atoms; `report` numbers go to the board; `fyi` → nothing)
           rows: `a<n> "<verbatim slice>" → <target: goal:<id> | idea | decision | ?>`
checks     every slice is a substring of the message (grep; a spider test) — the model chooses cuts and labels, it never
           paraphrases (owner words stay verbatim, §12's rule for models: name, don't compute);
           atoms ≤ imperative sentences of the message; 0 atoms for an fyi
cost       ≈ 3k in / 0.5k out per message: Haiku ≈ $0.001, Sonnet ≈ $0.01; a few hundred messages a day < $0.30 on Haiku,
           and it is on credits, so ≈ 0 cash
```
**Routing down the tree.** An atom's target is a leaf id. When a director packs a flow for a leaf (§24), the pack includes
every atom on its card whose target is that leaf or its subtree; the atoms MOVE (not copy) into the flow's ARGS, and the
director's §7 shrinks by the same rows. "Hand a graph slice to someone under you and they get the appropriate atoms" is
then the existing pack → in route with one more MANIFEST section, `atoms:`. Inter-agent comms atomize the same way: a
director's ask to a kid is a box message → an atom on arrival; a kid's report is `kind: report` → board, never an atom.

**The navigation triple, which is §12 and §32 in plain words.** Every post's brief starts with three lines:
```
at:    my claimed leaf + my open atoms, oldest first          = position p (card §7)          "where I am, what next"
near:  my ring (posts.md adjacency) with their intake=n         = neighbourhood N(p)           "who is around me"
flow:  the board's Δ per lap for my town                       = velocity v (TRAJECTORY)      "how the whole is moving"
```
These are the three inputs the smell walk (§32) already needs: it steps from p into N(p), weighted by v and the smell. A
post with an empty §7 and no claim is walking; a post with atoms is placing them; the board shows both as numbers. Done-when:
one owner message to belam and one director→kid ask both appear as §7 rows within one turn with correct targets, the kid's
flow ARGS carry the moved atoms, and the board's `intake=` for the director drops by the same count in the same lap.

**M-leaves, restated.** M1 card §7 shape + `agi-atom add|close` (verbatim-checked) · M2 the atomizer kid on box receipt
(Haiku; Sonnet on `?`) · M3 `atoms:` in the pack, moved not copied · M4 board: `intake/placed/red` per post per lap + one
TRAJECTORY line per ingested throw · M5 the brainstorm: 60 rows into belam's card §7 (no new node), then the board line when
placed=60. Order unchanged: right after V0.
