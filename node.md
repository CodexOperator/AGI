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

## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.665 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-round-commit-schema-g-a00-3ef778da tip 630d1f8ff.
ROUNDS    this post's rounds on this node: DH.597 DH.644 DH.665; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

## CORRECTIVE DH.527 -- closes mur-director-engine-18 DH.513-k1 (review accept_with_residue; verify killed by memory-cap rc=-9, review residues stand)
BASE      CUT FROM season2/loops/hypothesis-round-commit-schema-g-a00-5a917eb9 tip 73a3d5003 (worktree a00-5a917eb9). No merge. Never rebase. NEVER DH.442.
0 production lines, 0 test lines: node wording only, EVERY edit through write.py (never a scripted rewrite: the write-log must attest each one).
1. experiment:a00-cb8fae55-9c5f9e -- DH.513 added a stray fence (:145), a SECOND <!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.65: mur-eg-14 EG.46-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->

## CORRECTIVE DH.665 -- closes mur-director-engine-41 DH.644-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-round-commit-schema-g-a00-3ef778da tip 630d1f8ff (branch de-base-665; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Pasted sha for the parent review's own node is stale (6e689196fb69 vs f37872e3 at tip) — a00-790ef013-40bf20.md:148.
2. MISREAD PROBE — the parent's own auth probe is stated about the wrong node. a00-790ef013-40bf20.md:148 (THOUGHT, PROBE B) claims 'the frontmatter `evidence_runs` parsed as a real YAML LIST of three ids, each of which EXISTS on disk and is NOT this node' and that '`verdict` reads `inconclusive_lean_disproved:70`'. This node's own frontmatter says four entries with the first being the node itself (:10-14, `- experiment:a00-790ef013-40bf20` — already in the kid's commit b9fbb68ce) and `verdict: disproved` (:23). The three-id list and the `:70` verdict belong to a00-f69f0880-e5a133.md:10-13/:23, and PARENT PROBES at :151 repeats the same wrong list. Substance is true of a00-f69f0880 (I re-verified all three ids resolve and its verdict/title); the referent is one clause from true. This is the round's own defect class — a claim about a reader, written into the file the reader describes, 137 lines from the claim.
3. CONTRADICTED RATIONALE + a wrong before-cell. The demotion of a00-f69f0880 is justified in the bytes partly by '`evidence_runs: [/, itself]` so `>= 1` was satisfied with zero independent runs' (a00-790ef013-40bf20.md:40, repeated in the correction table at a00-f69f0880-e5a133.md:144) — but self-citation by an `experiment` is the engine's SANCTIONED form (evidence_gate.py:394-398, cli.py:1473-1478), so that half of the rationale names a non-defect. And the `- /` cell does not exist at 9bf67143e: the base frontmatter was a single self entry (`git show 9bf67143e:…a00-f69f0880-e5a133.md`, lines 10-11), so the BEFORE column mis-describes the base it claims to have read. The demotion survives on its other reason (landed no bytes, which I confirmed).
4. OWNERSHIP / MECHANISM re-check by the first reviewer cited the wrong reader. cli.py:2242-2257 is inert for this round; the live gate is cli.py:2125-2126 with 2448-2453, and `done` did not refuse — it committed the round's own node (b9fbb68ce 145 lines, c8e0082d2 151) and left three foreign paths. Any director reading the first review will go looking at the schema round_commit cell for a node type that has none.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-66a47ae7-588fa2.md · .agi/nodes/experiment/a00-790ef013-40bf20.md · .agi/nodes/experiment/a00-e429a125-580d12.md · .agi/nodes/experiment/a00-f69f0880-e5a133.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 630d1f8ff · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE EG.65 -- closes mur-eg-14 EG.46-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-round-commit-schema-g-a00-03658de5 tip 29962ec4f (branch de-base-EG.65; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. New false referent: the fourth sha is NOT the review's PROBE D figure -- .agi/nodes/experiment/a00-7b6cb4e2-3639f2.md:62 -- The new comment says 'the fourth (d63213aa54f7) IS the review's own PROBE D figure'; the review's only PROBE D figure is 6e689196fb69 for a00-790ef013 (a00-790ef013-40bf20.md:148) and it printed none for a00-f69f0880 — 'git grep -n d63213aa 5d149fc56 -- .agi/nodes/experiment/*.md' hits exactly one line, the kid's own paste at :61. Correct form: PROBE D asserted only 'The other three are unchanged and still reproduce', an assertion that is itself false at 5d149fc56 for the fourth. A false claim about a reader replaces the false label it cured.
2. 'this node' at two correction sites names no node and is false of the file it sits in -- .agi/nodes/experiment/a00-7b6cb4e2-3639f2.md:40 -- :40 'this node's own frontmatter is THREE entries, first = itself, verdict: disproved' and :137 'this node is 3 entries self-first, disproved' read inside a00-7b6cb4e2, whose own frontmatter (:10-11) has ONE evidence_runs entry and whose verdict is inconclusive_lean_proved:70 (:25); both are true only of the reviewed node a00-790ef013-40bf20, which neither site names — the same 'claim about a reader' class the round exists to fix, at the two sites the order named without a referent.
3. Present-tense stale fact plus a mis-cited probe in the new hypothesis Agent Note -- .agi/nodes/hypothesis/round-commit-schema-gate-reads-its-cell-names-its-refusal-and-binds-the-parent-tier.md:61 -- 'its node edits never reached a commit, per a00-790ef013 PROBE B and PARENT PROBES' is false in the present tense at this tip: those edits are in commits 630d1f8ff ('land DH.644's logged node edits') and 5d149fc56 ('land DH.665's logged node edits'), and the bytes at 29962ec4f carry the re-lands ('GIT ATTESTATION (DH.644)' = 1 hit in a00-e429a125). PROBE B is the referent correction, not the uncommitted-state evidence; that is the THOUGHT's section (3) THE NEAR MISS at :148 and PARENT PROBES 'CONDITION ON THE ROUND' at :151. The instant label this round applied everywhere else is missing here.
4. The CEILING measurement the orders required was never pasted -- .agi/nodes/experiment/a00-7b6cb4e2-3639f2.md:141 -- ordersEG.46.md CEILING: 'MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 5d149fc56 <your final tip>` on your node (an empty range is not a measurement)'. No such paste exists in any of the three nodes; my measurement is 3/3, 12/10, 9/1 (all .md, 0 production, 0 test), i.e. the round is inside the ceiling but the reader has no pasted proof.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_bin_help_smoke.py once (timeout 900, TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT (TMM.322)); TEXT-ONLY round: node text only
FILE SCOPE .agi/nodes/experiment/a00-790ef013-40bf20.md · .agi/nodes/experiment/a00-7b6cb4e2-3639f2.md · .agi/nodes/hypothesis/round-commit-schema-gate-reads-its-cell-names-its-refusal-and-binds-the-parent-tier.md (write.py) · the kid's own node
CEILING   HARD CAP: this kid only (claude-code text-fix, skill agi-corrective §3a) · 0 production lines · 0 test lines · node text only · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 29962ec4f <your final tip>` on your node (an empty range is not a measurement)
KID       you ARE the round: commit every edit on your loop branch (cli.py done) before you exit; a version delta goes in the node THOUGHT (write.py), never the body
