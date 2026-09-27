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
1. experiment:a00-cb8fae55-9c5f9e -- DH.513 added a stray fence (:145), a SECOND <!-- THOUGHT:BEGIN --> (:147) and a byte-identical copy of the DH.470 paragraph (:148): old_tip had BEGIN=1/END=1 -> restore exactly one THOUGHT pair and one copy of the paragraph; paste `grep -c 'THOUGHT:BEGIN'` on that one file (= 1).
2. the DH.513 kid applied two edits by scripted exact-string rewrite, so no write-log row attests them -> re-apply the six DH.513 node edits' final bytes through write.py so each node's last write-log sha equals its bytes; paste the per-node check.
3. experiment:a00-212ee37a-73fc13 stays inconclusive_lean_disproved:55 on a premise that no longer reproduces (test_cli.py:2755 reads VISIBLE ONCE; grep -c revisited test_cli.py = 0) -> RE-RUN both, paste, and set the verdict the measurement supports, reason in its THOUGHT.
4. experiment:a00-47615c4e-006a39:155 says the a00-cb8fae55 duplicate is a DH.483 miss; old_tip had BEGIN=1, so DH.513 introduced it -> correct the sentence.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE experiment:a00-cb8fae55-9c5f9e · a00-212ee37a-73fc13 · a00-47615c4e-006a39 · a00-58f9c0e5-af6502 · a00-7087b01c-a4999d · a00-d596cc8b-bea4b5 (write.py only) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.527: mur-18 DH.513-k1 accept_with_residue (verify memory-capped) -- DH.513 itself malformed a00-cb8fae55 (2 BEGIN, stray fence, duplicate paragraph), two edits bypassed write.py so no write-log attests them, a00-212ee37a demoted on a premise that no longer reproduces, a false provenance sentence. Node wording only.
<!-- THOUGHT:END -->
