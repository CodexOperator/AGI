---
id: hypothesis:a-rounds-own-path-set-never-fails-open
mint_id: 885ebe132f374f549e04b8e2d15e9b05
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: 4f0c04007360227f
season: 2
testable_claim: an absent agent_id refuses by name; --owns is bound to dispatch-time ids; a test fails on 6c403aeb4b
title: "A round own-path set never fails open and has no unguarded kid route (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-own-path-set-never-fails-open

# hypothesis: A round own-path set never fails open and has no unguarded kid route (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
cli.py:2293 the --node-id seed guard fails OPEN when agent_id is absent; cli.py:2288 --owns is a third kid-supplied route into the own-path set, unguarded (the agent-id-in-basename fix cannot cover it: 689e62f96 carries 4 kid files in one parent commit) (PASS 10 c8)

## Testable claim
an absent agent_id refuses by name; --owns is bound to dispatch-time ids; a test fails on 6c403aeb4b

## CORRECTIVE DH.552 -- closes mur-director-engine-23 DH.514-k1 accept_with_residue + DH.514-k2 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-rounds-own-path-set-a00-792978f9 tip ee2e5823e (branch de-base-552; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. --owns set admits the child's own node_id, a kid-supplied value (cli.py:2207)
2. 3. experiment verdict field contradicts its own THOUGHT (a00-1389258c-50f93f.md:26)
3. MISS 1 (widening is UNCONDITIONAL, not gated on the parent asking — sharpens defect 1): `asked = [node_id, *(owns or []), *(named or [])]` (cli.py:2340) puts every id from `_round_spawned_node_ids` into the sweep whether or not the parent passed `--owns`; `_round_scope_ok` short-circuits True for `p in own_paths` (cli.py:2106) and the commit is `git add -- *in_scope` (cli.py:2529). So a kid-writable `node_id` (cli.py:2207) reaches `git add` with no parent request at all. Neither a00-1389258c-50f93f.md nor a00-ee2d4cb1-6cecb8.md states this; both describe the correction as a --owns fix. The bound that remains is `_round_committable` (cli.py:2389) plus 'the file is dirty in the worktree'.
4. MISS 2 (the un-narrowed glob's real blast radius, and why it is not reachable today): `spawned_by_agent` is `os.environ.get("AGI_AGENT_ID")` (dispatch.py:3000), and for a director seat that value is the SEAT NAME, not a per-round id. Measured live: 494 records carry `spawned_by_agent="director-engine"` spread over ~50 `iter-*` dirs (and 2 over `director-thought`). `_round_spawned_node_ids` has no iteration bound and no id-shape filter, so a seat-named agent that ever ran `done` inside a linked worktree would sweep every node it ever spawned. Unreachable today only because `_auto_commit_worktree` returns before the call outside a worktree (cli.py:2444-2446) and worktrees are minted per a00-<id> — UNVERIFIED in production, and I did not run it. The probe I WOULD run (fixture only, no real done): a tmp graph with `sessions/iter-1/<a>/agent.json` and `sessions/iter-2/<a>/agent.json` both stamped `spawned_by_agent="seat-name"`, then assert `_round_spawned_node_ids(root, "seat-name")` returns only the round's own iter — it currently returns both.
5. MISS 3 (a claim no committed test backs, per the rules I must not take from a report): a00-ee2d4cb1-6cecb8.md:19 asserts 'suite: 290 passed, 0 red across the four named files (parent-measured)'. UNVERIFIED — the two in-scope files hold 78 tests and I measured 77 passed / 1 environmental failure; nothing in the diff pins a 290-test run or names the other two files. Not a defect; recorded so the merge-up does not inherit it as a citation.
6. MISS 4 (checked and CLEAN, stated so the next reviewer does not re-open it): the new test file touches no real resource — it imports only importlib/os/pathlib, builds every graph under tmp_path (test_round_own_path_set_fails_closed.py:30-42) and calls only the three pure helpers; no subprocess, tmux, systemd or crontab, no rotate/heal/send/dispatch symbol. And the diff deletes nothing under .agi/nodes (`git diff --numstat` = 127 and 123 pure insertions for the two nodes), so no demotion-by-deletion. No gate was fixed to pass it: the new file asserts the REFUSAL directions (lines 47, 76, 120, 148) as well as the landed ones, and the auth probe that found kid 1's regression is recorded rather than deleted (a00-1389258c-50f93f.md:112).
7. 1. Kid-writable node_id admitted into the dispatch-time id set (cli.py:2207)
8. 2. Unbounded iter-* glob; spawn authority never expires (cli.py:2200)
9. 3. Union computed unconditionally on every done (cli.py:1756)
10. 4. Kid-1 node frontmatter verdict contradicts its own THOUGHT (a00-1389258c-50f93f.md:26)
11. The union does not only widen the `--owns` route: it also DISARMS the DH.414 `--node-id` SEED guard. cli.py:2345 exempts any seed id present in `named` from the basename/agent-id check, so `done --node-id hypothesis:foreign` now sweeps nodes/hypothesis/foreign.md with EMPTY stderr whenever that id sits in one of this round's child records (reproduced on a tmp fixture). That falsifies the round's own claims `Seed fix left byte-for-byte intact` (a00-ee2d4cb1:49) and `Both seeds refuse by name` (:114). Residue, not demote: pre-diff the same round could reach the same sweep via unguarded `--owns`, so no new authority over base — but the seed fix the node reports as intact is not intact on this route.
12. The new test file's only RED seam is dead where it lives. `AGI_CLI_PY` (test_round_own_path_set_fails_closed.py:22) is deleted before any test body runs by the session-scoped strip in extensions/agi/conftest.py (`strip_dispatch_env` removes every AGI_* key; I confirmed `os.environ.get("AGI_CLI_PY") is None` inside a test body). So `AGI_CLI_PY=<base cli.py> pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py` reports 7 passed while exercising the FIXED bytes; the base RED (4 failed, 3 passed) reproduces only with the file copied outside `tests/` where no conftest loads. `AGI_CLI_PY` appears nowhere else in the engine. The hypothesis's third conjunct (`a test fails on 6c403aeb4b`) is therefore unverifiable as committed — a red-proof seam that cannot go red, on the very file whose docstring advertises it.
13. The production wiring is asserted by NO committed test. Both new spawn tests build the union by hand (test file lines 136-137 and 152-153: `named = _round_named_node_ids(...) + _round_spawned_node_ids(...)`), so nothing pins cli.py:1756; kid-1's own probe already recorded that call site as `inconclusive` (a00-1389258c-50f93f.md:17, `_auto_commit_worktree` returns before the guard on a non-linked tree). UNVERIFIED here — the probe I WOULD run and did not: a tmp linked git worktree with a real `cli.py done --agent-id <parent> --owns <kid node id>` and a spy on the commit, which crosses the round-commit path and writes a verdict. The parent's live probe (a00-ee2d4cb1:114) is the only evidence for that end-to-end claim.
14. Ownership, both checks re-run fresh: (1) scope — the diff touches only cli.py, the one new test file, three test_cli.py call sites, and the two nodes this round's own kids minted; no .agi/config.json, schema, quorum or foreign-node write, no `git add -A`. (2) tree — no deletion or deprecation under .agi/nodes; the only cross-agent write is the parent's sanctioned review write to its own kid's node (edited_by a00-792978f9). The 3 test_cli.py repairs were checked against base cli.py as well (71/71 both ways), so no assertion was weakened to pass. The new tests touch no real resource: tmp_path fixtures, no subprocess, tmux, systemd or crontab. No hand-landed gate: cli.py is named by the hypothesis assignment (`assigned: director-engine`).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli.py test_round_own_path_set_fails_closed.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/tests/test_cli.py · extensions/agi/tests/test_round_own_path_set_fails_closed.py · .agi/nodes/experiment/a00-1389258c-50f93f.md · .agi/nodes/experiment/a00-ee2d4cb1-6cecb8.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (split the numbered items between them, no overlap) · <= 25 production lines net over ee2e5823e · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.557 -- DH.552 left a RED and two kids' items unlanded (harvest 15:0xZ: kid a00-8f39d964 landed; a00-e0e124e8 died, a00-fa7a6d2f failed)
BASE      CUT FROM season2/loops/hypothesis-a-rounds-own-path-set-a00-98233a26 tip e450e5b2e (branch de-base-557). No merge. Never rebase.
1. RED introduced by DH.552: test_round_own_path_set_fails_closed.py::test_owns_reaches_the_nodes_of_the_agents_this_round_spawned asserts ['experiment:a00-kid-1'] and now gets [] (green on the base d2a3abb2f: 7 passed). The DH.552 cli.py change (+27/-9) narrowed the iter-* spawn glob. Make the test green WITHOUT re-widening the glob to every iter-* dir: the spawn authority is bounded to THIS round's iter dir. If the test's fixture places the kid outside the round's own iter dir, fix the fixture and say why on your node.
2. Every item of this node's ## CORRECTIVE DH.552 section that kid a00-8f39d964's node does NOT mark done: do it now (read that node first; list which items you took).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_round_own_path_set_fails_closed.py test_cli.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only. test_help_smoke[suite_guards.py] is red on this old base -- not yours.
FILE SCOPE extensions/agi/bin/cli.py (the round path-set / spawn glob only) · extensions/agi/tests/test_round_own_path_set_fails_closed.py · extensions/agi/tests/test_cli.py · experiment:a00-8f39d964-fc2306 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e450e5b2e · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.557: mur-director-engine-23 DH.552 harvest red residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
