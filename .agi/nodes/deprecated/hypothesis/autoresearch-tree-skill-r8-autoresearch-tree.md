---
id: hyp:autoresearch-tree-skill-r8
mint_id: a909debfc3274ea38bddbc7090ae02ff
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R8
testable_claim: Drop-In Portability
thought_session: season
title: "autoresearch-tree-skill/R8: Drop-In Portability"
---
**Description:** The skill is portable: dropping the project context directory into any repository should be sufficient to run the skill there.

**Acceptance Criteria:**
- [ ] A self-test runs the skill in a fresh empty repository where only the project context directory has been copied in, and the first iteration completes successfully
- [ ] No code path inside the skill assumes the repository name, host path, or any environment beyond an optional model selector
- [ ] Removing the project context directory from a repository removes all skill-managed state from that repository
- [ ] The skill's documentation states the portability contract and the self-test command

**Dependencies:** graph-core (R9 portability)

## Out of Scope

- Ollama-based agent dispatch — deferred to v2
- An in-memory database backend (sqlite or duckdb) for swarm-scale read-write — deferred
- Domain-specific verdict-judging logic beyond emitting taxonomy-conformant values — out of scope
- Modification of the existing autoresearch-create or autoresearch-finalize skills — explicitly forbidden
- Cross-repository or multi-project orchestration — out of scope

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no formal drop-in self-test, though the skill is symlink-portable by construction (`CLAUDE.md`: everything reachable globally by symlink) -- informally true, not testably proven; this THOUGHT is the record.
<!-- THOUGHT:END -->