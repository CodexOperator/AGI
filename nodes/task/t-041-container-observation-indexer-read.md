---
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
effort: M
id: "task:t-041"
mint_id: 0007e3f6a4664f5fbd5d0b6b978628bd
origin: build-site
parents:
  - hyp:environment-indexers-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-041: Container observation indexer — read-only nodes with redaction"
type: task
---

**Description:** Use `docker inspect <id>` shelled-out as read-only call. Emit `container` parent + `image`, `port`, `mount`, `env_key` children. Redact env values, secret-like keys (TOKEN/PASSWORD/SECRET/KEY) → `***REDACTED***`. Refuse to call any docker subcommand other than `inspect`/`ps`. Unreachable → `ContainerUnreachableError`.

**Files:** `agi-tree/src/environment_indexers/container_observation.py`, `agi-tree/src/environment_indexers/schemas/[container].md`, `[image].md`, `[port].md`, `[mount].md`, `[env_key].md`, `agi-tree/tests/environment_indexers/test_container_observation.py`

**Test Strategy:** Stub the docker call. Assert subprocess invocations are read-only. Assert env values redacted in frontmatter. Test the unreachable-error branch with a non-existent id.
