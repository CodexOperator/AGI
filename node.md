---
id: task:t-041
mint_id: 0007e3f6a4664f5fbd5d0b6b978628bd
type: task
parents:
  - hyp:environment-indexers-r6
acceptance_criteria:
  - R6.1 (running against accessible container produces container node + child nodes for image/ports/mounts/env-keys with values redacted)
  - R6.2 (no write operation issued against container or host)
  - R6.3 (unreachable → structured error
  - no nodes)
  - R6.4 (sensitive values redacted before written into frontmatter)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R6
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-041: Container observation indexer — read-only nodes with redaction"
---
**Description:** Use `docker inspect <id>` shelled-out as read-only call. Emit `container` parent + `image`, `port`, `mount`, `env_key` children. Redact env values, secret-like keys (TOKEN/PASSWORD/SECRET/KEY) → `***REDACTED***`. Refuse to call any docker subcommand other than `inspect`/`ps`. Unreachable → `ContainerUnreachableError`.

**Files:** `agi-tree/src/environment_indexers/container_observation.py`, `agi-tree/src/environment_indexers/schemas/[container].md`, `[image].md`, `[port].md`, `[mount].md`, `[env_key].md`, `agi-tree/tests/environment_indexers/test_container_observation.py`

**Test Strategy:** Stub the docker call. Assert subprocess invocations are read-only. Assert env values redacted in frontmatter. Test the unreachable-error branch with a non-existent id.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R6` under `hyp:environment-indexers-r6`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->