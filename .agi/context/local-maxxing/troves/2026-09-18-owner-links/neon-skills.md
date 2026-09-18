# NEON SKILLS — reading digest (2026-09-18, read-only, no key, no install)

Owner command DOCUMENTED, never run: `npx neon@latest skills -s neon -s neon-postgres -y`
MEASURED = quoted from a page/file read now; ESTIMATE = my inference.

## 1. WHAT THE COMMAND DOES — a DOCS install, not a database
- MEASURED (neon.com/docs/cli/skills): "The `skills` command installs Neon agent
  skills into your coding agents, so tools like Cursor and Claude Code know how
  to work with Neon's Postgres, AI Gateway, Object Storage, and Functions."
  Runs via npx → "needs Node.js 22.20.0+".
- MEASURED (registry.npmjs.org/neon/latest): npm pkg `neon` = the **Neon CLI**,
  v**5.0.0**, Apache-2.0, bin `neon`, 241 files, repo `neondatabase/neon-pkgs`,
  deps incl. `add-mcp`, `@neon/sdk`, `execa`, `undici`. (formerly `neonctl`.)
- MEASURED (neon-pkgs `packages/cli/src/skills/catalog.ts`): the CLI ships no
  skill text — it shells out to the **agentskills.io `skills` CLI** with source
  `neondatabase/agent-skills`. So the command = download Neon CLI (241 files)
  → download skills CLI → download SKILL.md files from GitHub.
- MEASURED (neon.com/docs/ai/agent-skills): "Each skill is a `SKILL.md` entry
  point … the skill fetches the relevant documentation from online" — skills are
  **pointers, not bundled docs**. Install is **project-level by default**
  (current dir); `--global` = user-level.
- MEASURED (docs/cli/skills): agents = antigravity, cline, cline-cli,
  claude-code, claude-desktop, codex, cursor, gemini-cli, goose,
  github-copilot-cli, grok-build, opencode, vscode, windsurf, zed. "Claude
  Desktop and Claude Code both write to `claude-code`." `-s` + `-y` skips every
  prompt, so the owner's command is well-formed.
- Version skew MEASURED: docs list 7 default skills (neon, neon-ai-gateway,
  neon-functions, neon-object-storage, neon-postgres, neon-postgres-branches,
  neon-postgres-egress-optimizer); `catalog.ts` on main = same 7 **plus
  `neon-auth` default-true**. Docs are per-release; catalog drifts.

## 2. WHAT THE TWO REQUESTED SKILLS CONTAIN (source read)
- MEASURED (agent-skills `skills/neon/SKILL.md`, 474 lines): Neon is "a complete
  set of cloud backend primitives around **Lakebase Postgres, from Databricks**
  — Auth (managed Better Auth), long-running Functions, Object Storage, and an
  AI Gateway, all instant, branchable, and serverless." "Call the database
  Lakebase Postgres, and use 'Neon' for the brand."
- MEASURED (same): a branch is an "isolated, copy-on-write clone … shares data
  with its parent until writes cause it to diverge." Region gate: Storage/
  Functions/AI Gateway only in `aws-us-east-2`, `aws-us-east-1`,
  `aws-eu-central-1`, `aws-ap-southeast-1`.
- MEASURED (`skills/neon-postgres/SKILL.md`, 279 lines): index of Neon Postgres
  docs — pooled vs direct connections, migrations, branching, autoscaling,
  scale-to-zero, instant restore, read replicas, IP allow lists, logical
  replication, Lakebase Search (vector/full-text/BM25/hybrid).
- Town read: these teach an agent *how* to use Neon; they create and store
  nothing. The data plane is the **MCP server** (`neon mcp`) or `neon init` /
  `neon plugins` — none of which is in the owner's command.

## 3. WHAT LEAVES THE BOX (three channels)
- **Install-time (MEASURED, `skills/run.ts`)**: `skillsChildEnv` **deletes
  `NEON_API_KEY`** from the child env (good), but **removes
  `DISABLE_TELEMETRY` / `DO_NOT_TRACK`** so the skills CLI's install ping still
  fires, passing `{origin:"neon-cli", command, version}`. Neon CLI itself
  telemeters (docs/cli: "anonymous data … never user-defined data"; opt out
  `--no-analytics`).
- **Run-time (MEASURED, agent-skills docs)**: the agent fetches neon.com docs
  when a topic comes up. Queries *about* Neon leave; the graph does not.
- **Data-plane (MEASURED, docs/ai/neon-mcp-server)**: hosted `mcp.neon.tech`
  connects from static IPs two static egress IPs (published in the Neon docs page cited; literals removed here by town rule); docs say
  "MCP for development and testing only", "never connect MCP agents to
  production databases", "avoid exposing production or PII data".
  `?readonly=true` restricts to SELECT/schema; `?projectId=` scopes. Auth =
  OAuth or API-key `Authorization` header. Data then sits in Neon's cloud.

## 4. WHAT A NEON PROJECT GIVES (docs/introduction/plans)
- Serverless Postgres, storage decoupled from compute → autoscaling, branching,
  instant restore, scale-to-zero.
- MEASURED Free ($0, no card): **100 projects**, **10 branches/project**,
  **100 CU-hours/project/month**, autoscale to **2 CU (8 GB RAM)**, **0.5 GB
  storage/project**, **5 GB egress/project/month**, 6 h instant-restore history
  (≤1 GB), 1 manual snapshot, 60k Auth MAU, 5 GB object storage, Functions 10
  active + 400 waiting capacity-hrs + 1M invocations, 1-day metrics.
- MEASURED: scale-to-zero "After 5 min" on Free and **cannot be disabled**;
  "Computes that are suspended do not accrue CU-hours." 1 CU ≈ 4 GB RAM;
  `size × hours = CU-hours`; 100 CU-hr = 0.25 CU for 400 h/mo.
- MEASURED Free overage: out of CU-hours/egress → **compute suspended until next
  period**; over 0.5 GB storage → writes fail; branch 11 fails. "None of these
  limits delete your data."
- MEASURED paid: Launch $0.106/CU-hr, $0.35/GB-month storage, $0.10/GB egress
  past 500 GB, $1.50/extra-branch-month; Scale $0.222/CU-hr. Snapshots $0.09/GB-mo.
- Every plan: multi-AZ HA, read replicas, pgBouncer pooling to 10,000 conns,
  extension library incl. **pgvector**, PostGIS, TimescaleDB.
- Auth order MEASURED (docs/cli): `--api-key` → `NEON_API_KEY` env →
  `~/.config/neonctl/credentials.json` from `neon login` (browser OAuth) →
  interactive web auth.

## 5. TOWN QUESTION — Neon as graph mirror / typed-decision replay store
- Graph size MEASURED (viewport, 2026-09-18): **3475 nodes, 3780 edges**; 1403
  experiment, 996 hypothesis, 300 build, 184 goal, 171 verdict, 130 idea,
  91 task, 64 mvp.
- ESTIMATE: markdown bodies ≲2 KB → whole graph ≈ 7 MB; 10× headroom ≈ 70 MB.
  **The full mirror fits the Free 0.5 GB cap with ~7× margin**; the typed-
  decision replay corpus (171 verdicts + their experiments) is kilobytes.
- ESTIMATE cost: with scale-to-zero, a sync is minutes of 0.25 CU ≈ 0.02 CU-hr;
  50 syncs/mo ≈ 1 of 100 free CU-hr. **Dollar cost of the mirror on Free = $0**;
  binding limits are egress (5 GB) and storage (0.5 GB), neither near.
- What Neon adds over grep on `.agi/nodes/`: SQL + JSONB + **pgvector** +
  full-text/BM25 — "which verdicts lean disproved against goal g11.4" becomes a
  query. That is a reader feature; git stays source of truth.
- MEASURED risk shape: the mirror is derived, so it must rebuild from
  `.agi/nodes` in ONE pass and never be authoritative. Failure mode = a stale
  mirror answering confidently. Mitigation the graph already knows: content hash
  per node, whole rebuild not incremental (cheap at 7 MB), fail loudly on drift.
- Real cost is not $: (a) a network dependency in a $0-CPU-first town, (b) graph
  content leaving the box to a Databricks-run cloud, (c) a second copy that can
  disagree. A $0 local SQLite/pg on this box buys the same query surface with
  none of those three.

## 6. HYPOTHESIS SEEDS (smallest experiment; THIS box unless noted)
- **h-neon-mirror-is-unnecessary**: build a **local SQLite mirror** of
  `.agi/nodes` (3475 rows: id, type, status, tags, body, hash); measure build
  time, DB size, 5 queries (verdicts leaning disproved per goal; hypotheses with
  0 experiments; nodes untouched >30 d). Falsifier: mirror ≥0.5 GB or build
  >60 s, or a needed query needs pgvector. est_cost **$0**, **~15 min**.
- **h-free-tier-headroom**: from the mirror's real byte size, compute the
  Free-plan CU-hours + egress for a 50-sync month against 100 CU-hr / 5 GB /
  0.5 GB. Falsifier: any limit exceeded → local pg, not Neon. est_cost **$0**,
  **~5 min** (arithmetic on MEASURED plan numbers).
- **h-typed-decisions-replay-local**: dump the 171 verdict + 1403 experiment
  nodes into a table, replay typed acts (verdict class, accept/demote) against
  `hypothesis:lm-jev-typed-acts-replay`'s bars (top-1 ≥0.75, ECE ≤0.10) with a
  local classifier — no Neon, no API. Falsifier: cannot clear the bars.
  est_cost **$0**, **~30 min**.
- **h-neon-only-if-multi-writer**: the mirror earns a remote Postgres only if
  ≥2 boxes write concurrently. On local-town (ssh alias): two writers, local file
  mirror vs one Neon branch each. Falsifier: a local git+file lock suffices.
  est_cost **$0**, **~30 min**; no Camber hours (3/month is spend).

## SOURCES (all read 2026-09-18)
neon.com/docs/cli/skills · neon.com/docs/cli · neon.com/docs/cli/init ·
neon.com/docs/ai/agent-skills · neon.com/docs/ai/neon-mcp-server ·
neon.com/docs/introduction/plans · neon.com/pricing ·
registry.npmjs.org/neon/latest · github.com/neondatabase/neon-pkgs
(packages/cli/src/skills/{catalog,targets,run}.ts) ·
github.com/neondatabase/agent-skills (skills/{neon,neon-postgres}/SKILL.md)
