---
id: hypothesis:round-commit-schema-gate-reads-its-cell-names-its-refusal-and-binds-the-parent-tier
mint_id: 2aab2305dede4883974a4eebbe79615f
type: hypothesis
parents:
  - hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses
next_edges: []
edited_by: director-engine
scaffold_hash: 4b03199d8bc67cc6
season: 2
testable_claim: "_round_scope_ok reads the schemas prefix from cell locations.schemas_root (no literal), a schema-gate exception refuses by name with a non-zero outcome, test_cli carries bracketed + broken-neighbour rows, and the parent-tier pre-commit runs the scope check before its loop-branch exit (TMM.262 residues 4-7, assigned: director-engine)"
title: Round commit schema gate reads its cell names its refusal and binds the parent tier
town: core
---
# hypothesis:round-commit-schema-gate-reads-its-cell-names-its-refusal-and-binds-the-parent-tier

## Measured
- TMM.262 (4) CONFIG-MAX: extensions/agi/bin/cli.py:2123 hard-codes `.agi/context/schemas/`, duplicating the declared cell `locations.schemas_root` (spawn_gate's SCHEMAS_SUBDIR mirrors it); layout-blind where the read at cli.py:2217 is not.
- (5) cli.py:2249-2252: a schema-block exception is a SILENT no-commit with exit 0.
- (6) the error branch's only committed test uses bare `hypothesis.md` (test_cli.py:2039-2049) while 21 of 22 live schemas are bracketed `[<type>].md`.
- (7) hooks/agent-git/pre-commit:98 exits 0 for season*/loops/* at tier parent before any scope check: a parent may commit a schema.

## CLAIM
(a) _round_scope_ok derives the schemas prefix from the `locations.schemas_root` cell (one source), no literal; (b) a schema-gate exception refuses with a named line AND a non-zero outcome the caller reports (never a silent exit 0); (c) test_cli.py carries a bracketed-schema error row plus a broken-neighbour row (one unreadable schema does not open the gate for a different, readable type); (d) the parent tier's pre-commit runs the same scope check before its loop-branch exit, or the node's THOUGHT states measured why a parent may commit a schema.

## Dispatch line
config-max: the prefix = cell locations.schemas_root (already declared; READ it) / template-max: none / code: the read of the cell, the named refusal, the hook binding.

## FALSIFIERS
- `grep -n "context/schemas/" extensions/agi/bin/cli.py` still hits a literal inside _round_scope_ok;
- a monkeypatched schema read raising -> exit 0 with nothing printed;
- a parent-tier commit of `.agi/context/schemas/[x].md` on a season2/loops/* branch succeeds.

## TESTS
extensions/agi/tests/test_cli.py (+ neighbourhood test_heal_watch.py test_dispatch.py). Every hook test under `timeout`, in a tmp git repo under /tmp, never this tree.

## FILE SCOPE
extensions/agi/bin/cli.py · extensions/agi/hooks/agent-git/pre-commit · extensions/agi/tests/test_cli.py · a new extensions/agi/tests/test_agent_git_precommit_scope.py if needed. Never .agi/config.json (the director commits cells).

## CEILING
<= 3 kids · <= 12 production lines per conjunct · pi parents (tier-0) · 0 USD. Every test that spawns python/pytest/git runs under `timeout` + a process cap; never a pytest that re-collects its own dir; kids never launch real claude.

## CORRECTIVE DH.527 -- closes mur-director-engine-18 DH.513-k1 (review accept_with_residue; verify killed by memory-cap rc=-9, review residues stand)
BASE      CUT FROM season2/loops/hypothesis-round-commit-schema-g-a00-5a917eb9 tip 73a3d5003 (worktree a00-5a917eb9). No merge. Never rebase. NEVER DH.442.
0 production lines, 0 test lines: node wording only, EVERY edit through write.py (never a scripted rewrite: the write-log must attest each one).
1. experiment:a00-cb8fae55-9c5f9e -- DH.513 added a stray fence (:145), a SECOND <!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.644: mur-director-engine-38 DH.597-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
