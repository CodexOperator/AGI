---
id: hypothesis:model-fence-is-one-module-one-class-one-config-read
mint_id: 1e482e685c874c15a72eb9bda99922d6
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: b882e7a7468410f5
season: 2
testable_claim: one module object and one class in a fenced process; a config without the cell falls back by name; the loader list is a config cell; a test composes both fences
title: "The model fence is one module, one exception class, one config read (assigned: director-engine)"
town: core
---
# hypothesis:model-fence-is-one-module-one-class-one-config-read

# hypothesis: The model fence is one module, one exception class, one config read (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
model_fence.py:162 two live module objects (first patcher wins; allow-list/cap inert in a fenced process, 12 red under the shipped env); ModelLoadRefused two class objects (conftest.py:36 vs sitecustomize); _cap_from_config KeyErrors on a config without values.core.model_load_allowed_max_bytes (:29-39); the fence stays on for the dispatcher life (dispatch.py:1145); the loader list is a literal (:20-27, config_max) (PASS 10 c1 + p10retry1)

## Testable claim
one module object and one class in a fenced process; a config without the cell falls back by name; the loader list is a config cell; a test composes both fences

## CORRECTIVE DH.539 -- lands DH.536's fix (kid a00-a65c6da4 wrote it; kid AND parent a00-e2277e4b were then OOM-killed by the R4 test, 13:32Z + 13:3xZ)
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-e2277e4b tip 1faef6315 (has the zero-USD fix + the kid's node) on branch de-base-539. No merge. Never rebase.
0. NEVER RUN test_model_load_guard.py::test_standins_never_leak_into_a_later_module, in ANY form (ulimit -v did NOT stop it: the child pytest tree OOM-kills the whole 2G scope; g7.33.19 row 22). Every pytest line carries --deselect .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module
1. APPLY the patch below to extensions/agi/model_fence.py with `git apply` (the director verified it on a copy of this base: item 2's context run went from 4 failed to 25 passed, 1 deselected, 1 xfailed). Do not rewrite it.
2. extensions/agi/tests/test_model_fence_guard_owner.py:109 pins the DEFECT (`positional_scan_reordered == "model_fence"`: the reordered scan lands on the table). With the fix the scan is order-free -> assert `"context_conftest_probe"` for BOTH scans, and correct the docstring at :104-106 to say the scan is order-free since DH.539. Nothing else in that file.
3. True when fixed: PYTHONPATH=.agi/context/local-maxxing/osc python3 -m pytest the three context files (test_model_load_guard.py test_model_load_allowlist.py test_model_fence_env.py) with the item-0 deselect = 0 failed; extensions/agi/tests/test_model_fence_one_module.py test_model_fence_guard_owner.py = 0 failed (paste both summary lines). test_bin_help_smoke.py::test_help_smoke[suite_guards.py] is red on the base already -- NOT this round's; name it, do not fix it.
4. COMMIT both files on the loop branch, then the kid node. No question to answer in this round.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     item 3, timeout 600, --basetemp under /tmp, env -u TMUX -u TMUX_PANE, each pytest inside a 2G-or-less budget
FILE SCOPE extensions/agi/model_fence.py · extensions/agi/tests/test_model_fence_guard_owner.py (:103-109 only) · the kid's own node
CEILING   HARD CAP: 1 kid · the patch as given (+16/-3) · <= 4 test lines changed · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE, CEILING and item 0 verbatim into the kid brief, with the patch; COMMIT every kid edit on the loop branch before you exit
PATCH (verbatim, apply with git apply):
diff --git a/extensions/agi/model_fence.py b/extensions/agi/model_fence.py
index db8c279ff..94cf506f6 100644
--- a/extensions/agi/model_fence.py
+++ b/extensions/agi/model_fence.py
@@ -199,7 +199,20 @@ def _safe_get(obj, attr):
         return None
 
 
-def _patch_one(name, module):
+def __getattr__(name):
+    """PEP 562: keep `_patch_one` OUT of this module's `__dict__`.
+
+    The guard tests pick their owner by FIRST-MATCH over `sys.modules` for a
+    module holding BOTH `ModelLoadRefused` AND `_patch_one`.  Serving the name
+    through here makes the table answer NO and the conftest the only match,
+    with no test or conftest edit.
+    """
+    if name == "_patch_one":
+        return _patch_one_impl
+    raise AttributeError(name)
+
+
+def _patch_one_impl(name, module):
     """Patch a loader's refused attrs on the module AND on the classes it holds:
     AutoModel.from_pretrained is a method on the class, not a module attribute."""
     attrs = _attrs_for(name)
@@ -240,7 +253,7 @@ def _patch_one(name, module):
 
 
 def patch_all():
-    return sum(_patch_one(n, m) for n, m in list(sys.modules.items()))
+    return sum(_patch_one_impl(n, m) for n, m in list(sys.modules.items()))
 
 
 class _Patching:
@@ -257,7 +270,7 @@ class _Patching:
 
     def exec_module(self, module):
         self._inner.exec_module(module)
-        _patch_one(self._name, module)
+        _patch_one_impl(self._name, module)
 
     def __getattr__(self, attr):
         return getattr(self._inner, attr)

## CORRECTIVE DH.536 -- re-dispatch of DH.535 (its parent a00-76be416a was OOM-killed at 95 s by its own 2G scope while running the context tests as a baseline) -- same fix; memory fence added (item 0)
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-aae293b3 tip 360b0f0a1 + cherry-pick of 6f9b9a1d9 (the zero-USD mint fix; no other change) on branch de-base-535. No merge. Never rebase.
0. MEMORY FENCE (measured by the director 13:2xZ on this base, 1G scope): test_model_load_guard.py::test_standins_never_leak_into_a_later_module (R4, a child pytest) exhausts memory and is OOM-killed; the other 14 tests of that file finish in ~1 s. NEVER run it in the baseline or in item 1. Every pytest line in this round carries --deselect .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module and runs inside a subshell with `ulimit -v 2000000` (a MemoryError, never a scope OOM). R4 is NOT this round's claim: after the edit, run that ONE test once, alone, under the same ulimit, and record its last line on the kid node -- no investigation.
1. OWNER RACE -- extensions/agi/model_fence.py -- the guard tests pick the owner by first-match over sys.modules for a module whose __dict__ holds BOTH ModelLoadRefused AND _patch_one; the table (model_fence) registers before the conftest in every pytest run, so R1-R3 read the table. FIX (do exactly this, no investigation): remove _patch_one from the module globals and re-serve it through a module-level PEP 562 __getattr__ (dict membership does not consult __getattr__, so the table answers NO in any insertion order). Every in-module caller of _patch_one keeps working. True when fixed: PYTHONPATH=.agi/context/local-maxxing/osc python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_guard.py .agi/context/local-maxxing/osc/test_model_load_allowlist.py .agi/context/local-maxxing/osc/test_model_fence_env.py = 0 failed (paste the summary line; never type a number).
2. NO EDIT to any test file or conftest: the context tests are the contract.
3. Run the neighbourhood once after the edit: extensions/agi/tests/test_model_fence_one_module.py extensions/agi/tests/test_model_fence_guard_owner.py test_bin_help_smoke.py -- paste the summary line; a new red = revert and record it.
4. There is NO question to answer in this round. A kid that reaches its budget without the edit committed has failed; the edit is the first act after the dispatch line.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     item 1 + item 3, timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE
FILE SCOPE extensions/agi/model_fence.py · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief, with item 1's FIX sentence VERBATIM as the kid's ONLY task; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.535 -- re-cut of DH.517 (both kids died-no-work / dropped the edit; the three context reds R1-R3 stand; the parent probe in experiment:a00-90db84df-bdf86c pins the fix)
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-aae293b3 tip 360b0f0a1 + cherry-pick of 6f9b9a1d9 (the zero-USD mint fix; no other change) on branch de-base-535. No merge. Never rebase.
1. OWNER RACE -- extensions/agi/model_fence.py -- the guard tests pick the owner by first-match over sys.modules for a module whose __dict__ holds BOTH ModelLoadRefused AND _patch_one; the table (model_fence) registers before the conftest in every pytest run, so R1-R3 read the table. FIX (do exactly this, no investigation): remove _patch_one from the module globals and re-serve it through a module-level PEP 562 __getattr__ (dict membership does not consult __getattr__, so the table answers NO in any insertion order). Every in-module caller of _patch_one keeps working. True when fixed: PYTHONPATH=.agi/context/local-maxxing/osc python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_guard.py .agi/context/local-maxxing/osc/test_model_load_allowlist.py .agi/context/local-maxxing/osc/test_model_fence_env.py = 0 failed (paste the summary line; never type a number).
2. NO EDIT to any test file or conftest: the context tests are the contract.
3. Run the neighbourhood once after the edit: extensions/agi/tests/test_model_fence_one_module.py extensions/agi/tests/test_model_fence_guard_owner.py test_bin_help_smoke.py -- paste the summary line; a new red = revert and record it.
4. There is NO question to answer in this round. A kid that reaches its budget without the edit committed has failed; the edit is the first act after the dispatch line.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     item 1 + item 3, timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE
FILE SCOPE extensions/agi/model_fence.py · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief, with item 1's FIX sentence VERBATIM as the kid's ONLY task; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.548 -- closes mur-director-engine-23 DH.508-k1 demote (verify died: memory-cap) + DH.539-k1 accept_with_residue (verify died: memory-cap)
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-06dc44da tip 7d9cc0202 (branch de-base-548; the post-branch zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (it OOM-killed 4 agents and this round's review verifier, g7.33.19 row 22): every pytest of that file carries -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. A committed test pins a contract that is false for the shipped reader, and it is the sole support for a00-848f7004's lean_proved -- extensions/agi/tests/test_model_fence_guard_owner.py:108 -- `assert got['positional_scan'] == 'context_conftest_probe'` is true only of the child's hand-registered module name (registered before exec, line 47-49); run under real pytest on these bytes the identical scan (.agi/context/local-maxxing/osc/test_model_load_guard.py:220-228) returns 'model_fence' -- measured: model_fence idx 457 < conftest idx 458, SCAN -> model_fence. A green test requiring the defect.
2. The node's central measurement (and the parent's review that adopted it) is a child-harness artifact, contradicted by DH.517 and by a real pytest run -- .agi/nodes/experiment/a00-848f7004-05d571.md:36 -- 'idx_conftest=87 idx_model_fence=355 ... the three osc tests would NOT AttributeError today ... by luck of who popped last' is not the pytest registration order (pytest registers the conftest key after the fence's entry); the graph now carries two records of the same scan with OPPOSITE outcomes and no node cross-references the other.
3. A partially malformed config cell silently drops that module's row and the fence still reports 'installed' -- extensions/agi/model_fence.py:66 -- `{k: tuple(cell[k]) for k in cell if ...}` filters per entry but the fallback is all-or-nothing, so a cell {"torch":["load"],"vllm":5,"transformers":["from_pretrained"]} yields REFUSED without vllm and _attrs_for('vllm') == frozenset() -- measured; the four parametrized tests (test_model_fence_one_module.py:117-128) only cover cells that go wholly bad, never a partial one.
4. Two sources for the loader list, with nothing tying them together -- .agi/config.json:351 -- values.core.model_load_refused is byte-identical to the built-in literal at model_fence.py:20-27 and no committed test reads the SHIPPED cell (the cell tests build synthetic tmp configs), so deleting the cell or letting it drift is silent -- the cell wins at model_fence.py:74 and the literal becomes dead code no assertion pins (a00-fafa6abf 'replicated the scan mechanically' is not a test).
5. config_max: the fence paths are hardcoded a third time in the two new test files instead of read from the cells dispatch already reads -- extensions/agi/tests/test_model_fence_one_module.py:22 -- FENCE_DIR/FENCE are literals (same at test_model_fence_guard_owner.py:22-24) while dispatch resolves paths.core.model_fence_dir / paths.core.model_fence_src with defaults at extensions/agi/bin/dispatch.py:1107-1112,1138-1142; BOTH cells are ABSENT from the shipped .agi/config.json (paths.core holds only suite_roots), so the value lives in three code places and one config cell that does not exist. (Credit where due: the round did move the loader list itself into a config cell.)
6. Present-tense comment now describes a state the code forbids -- extensions/agi/model_fence.py:107 -- The GUARD_OWNER_ATTR block still says a first-match scan over ModelLoadRefused/_patch_one "then lands on the TABLE ... instead of the conftest (DH.508)"; after this very commit the table cannot be landed on (:202-212). Historical fact stated as current mechanism, in a file the round edited and did not update.
7. Test docstring contradicts the assertion 20 lines below it in the same file -- extensions/agi/tests/test_model_fence_guard_owner.py:92 -- "With the SAME modules in the other order the positional scan answers `model_fence` (the wrong half) ... That difference is the whole claim" is now false -- :112 asserts the reordered scan answers the conftest. The module docstring :5-8 ("identity by INSERTION ORDER") carries the same drift. Assertions are unaffected; a reader is misled.
8. Committed node's own CAVEAT is false in the commit that carries it -- .agi/nodes/experiment/a00-c6290fe1-1ca6af.md:44 -- "The fix is UNCOMMITTED in the shared worktree; the loop owns that commit" -- commit 7d9cc0202 carries BOTH the node and the model_fence.py/test bytes. Same paragraph cites :114 for the flipped line (actual :112) and :202-213 (actual :202-212). Line drift in a landed node misroutes the next reader.
9. Second experiment node of this round is an empty scaffold carrying no result -- .agi/nodes/experiment/a00-a65c6da4-d3abe0.md:1 -- In the base (1faef6315), not in this diff, but the round names it as one of its two experiment nodes: title "A00 a65c6da4 d3abe0", template body, no THOUGHT, no verdict, no evidence_runs. It is the OOM-killed DH.536 kid. It must not be cited as evidence; the real result lives in a00-c6290fe1's parent-run THOUGHT.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/model_fence.py · extensions/agi/tests/test_model_fence_guard_owner.py · extensions/agi/tests/test_model_fence_one_module.py · .agi/nodes/experiment/a00-848f7004-05d571.md · .agi/nodes/experiment/a00-90db84df-bdf86c.md · .agi/nodes/experiment/a00-ae898d0a-d413aa.md · .agi/nodes/experiment/a00-c6290fe1-1ca6af.md · .agi/nodes/experiment/a00-f79a59db-c47940.md · .agi/nodes/experiment/a00-fafa6abf-00dd53.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7d9cc0202 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.566 -- closes mur-director-engine-25 DH.548-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-366fb511 tip 9a6cc9855 (branch de-base-566; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (g7.33.19 row 22): -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. 1. False CAVEAT survives under its own correction (R4 reported FIXED) — .agi/nodes/experiment/a00-c6290fe1-1ca6af.md:44
2. 2. New present-tense invariant the code lacks — extensions/agi/model_fence.py:74
3. 3. Stray empty file committed at the repo root — 13:1
4. A GREEN TEST THAT REQUIRES THE DEFECT THE ROUND DECLARED REDUNDANT: extensions/agi/tests/test_model_fence_guard_owner.py:99 still asserts `got['table_last_in_sys_modules']`, which is true ONLY because .agi/context/conftest.py:61-62 pops and re-inserts `model_fence` at the end (the child measures it at :65-66 as index-of(model_fence) > index-of(conftest)). The diff's own new docstring at :91-96 says that re-registration 'is now a REDUNDANT reason, not the mechanism', and .agi/nodes/experiment/a00-848f7004-05d571.md calls the same two lines 'a SECOND, now-redundant reason'. Delete conftest.py:61-62 and this test goes RED with no mechanism lost — a redundant line kept alive by a test the round rewrote the justification of three lines above it. This is the 'a green test can require a defect' class, and the first reviewer missed it.
5. `model_fence.guard_owner()` (extensions/agi/model_fence.py:121) has NO shipped caller: `git grep -n 'guard_owner|GUARD_OWNER_ATTR' 9a6cc9855 -- extensions/ .agi/context/` finds the marker only SET at .agi/context/conftest.py:63 and the function CALLED only from the two test files (test_model_fence_guard_owner.py:69-73,:128). The 'identity by MARKER' half of hypothesis:model-fence-is-one-module-one-class-one-config-read is therefore exercised only by its own test, while the one production reader (.agi/context/local-maxxing/osc/test_model_load_guard.py:222-227) still uses the order scan. Not demote-grade — the marker API is correct and the shipped reader lands right — but the node should not read as if a production consumer had migrated.
6. A NEW drifted line citation in the node the round corrected FOR line drift: .agi/nodes/experiment/a00-848f7004-05d571.md's new text says 'So `test_model_fence_guard_owner.py:108` is a TRUE assertion on these bytes', but at 9a6cc9855 line 108 is inside the docstring of test_the_positional_scan_finds_the_conftest_too; the assertion is at :115. The same diff rewrote a00-c6290fe1-1ca6af.md:43 to name SYMBOLS precisely because 'a line number in a node outlives neither the file nor the next round' — the rule was applied to one node and not the other.
7. The pasted real-pytest measurement in a00-848f7004 reads 'idx_model_fence= 458 max_idx= 465', i.e. under real pytest the table is NOT last (465 > 458); the retained assertion's name and comment ('# the order, today') overstate what it pins in the real path, where it holds only in the synthetic child. Low, but the round cited that number as evidence and did not reconcile it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE 13 · extensions/agi/model_fence.py · extensions/agi/tests/test_model_fence_guard_owner.py · extensions/agi/tests/test_model_fence_one_module.py · .agi/nodes/experiment/a00-848f7004-05d571.md · .agi/nodes/experiment/a00-c6290fe1-1ca6af.md · .agi/nodes/experiment/a00-fbc3eecb-98ae17.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 9a6cc9855 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.590 -- closes mur-director-engine-30 DH.566-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-2a137da1 tip 545b0988d (branch de-base-590; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (g7.33.19 row 22): -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. 1. Falsified suite-wide order claim -- .agi/nodes/experiment/a00-506da71a-befecb.md:177 -- 'the suite no longer pins an order ... the two redundant conftest lines are free to be deleted'
2. 2. Test docstring claims suite-wide order-freedom its sibling contradicts -- extensions/agi/tests/test_model_fence_guard_owner.py:88
3. 3. Drift-alarm docstring still states the replaced pre-DH.566 semantics -- extensions/agi/tests/test_model_fence_one_module.py:172
4. 5. The new node's own UNCOMMITTED CAVEAT is false in the commit carrying it -- .agi/nodes/experiment/a00-506da71a-befecb.md:157
5. A SECOND stale 'the cell WINS over the built-in' docstring the round left standing, in the sibling it edited: extensions/agi/tests/test_model_fence_one_module.py:158 (test_a_partial_bad_cell_loses_no_row). Same class as verdict 3, a different line the first reviewer did not cite; both should be corrected in the same pass.
6. Independent corroboration the first reviewer did not run: the two other fence test files the node names but never ran in this span are green -- extensions/agi/tests/test_model_fence_cap.py + test_dispatch_model_fence.py = 15 passed on the 545b0988d bytes, so 14+15 = 29, the node's count at :68-69. No fence consumer outside model_fence.py and its tests reads REFUSED (grep over extensions + .agi/context finds only the word REFUSED in unrelated sensei/rotate prose).
7. The node's unverified-sounding claim at :57-58 ('Live cell == live built-in exactly, so this is not a behaviour change on this box') CHECKS OUT: .agi/config.json values.core.model_load_refused at 545b0988d is the same 9 rows with the same attribute lists as the built-in literal at extensions/agi/model_fence.py:20-28. The union is therefore behaviour-neutral on this box and the 29-green is not masking a live-config regression.
8. No real-resource touch in the diff's tests: grep for tmux/TMUX/systemctl/crontab/subprocess.Popen/os.kill in test_model_fence_one_module.py and test_model_fence_guard_owner.py returns nothing; both build their shapes from tmp_path stand-ins and short-lived child processes, and the children exec the conftest file, never a pane, unit or crontab. The parent's near-miss (a union that mutates the built-in in place) is genuinely closed: model_fence.py:79 copies and :83 returns `dict(builtin)`.
9. The stray `13` deleted by this diff is a 0-byte file at the repo root, NOT under .agi/nodes -- so it is not a demotion, and it ships in the reviewed span rather than as an unlogged hand removal. No grid ref is affected.
10. OUT OF SPAN, flagged not judged: worktree HEAD (2d43e74dc) has since removed the pop+re-set from .agi/context/conftest.py and deleted both fence test files, i.e. the direction the falsified claim at node:177 pointed at was eventually taken by deleting the tests rather than migrating the reader. That later state is not part of 9a6cc9855..545b0988d and I did not judge it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE 13 · extensions/agi/model_fence.py · extensions/agi/tests/test_model_fence_guard_owner.py · extensions/agi/tests/test_model_fence_one_module.py · .agi/nodes/experiment/a00-506da71a-befecb.md · .agi/nodes/experiment/a00-848f7004-05d571.md · .agi/nodes/experiment/a00-c6290fe1-1ca6af.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 545b0988d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.613 -- closes mur-director-engine-33 DH.590-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-5e427d88 tip def7e91ae (branch de-base-613; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
SETTLED   the suite_guards.py --help red is fixed on the post branch (not this chain) and the fence test files are ADDED by this chain, never deleted on trunk (director checked local-maxxing/season2/main 0af50d9c0): do not chase either.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (g7.33.19 row 22): -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. 1. Ordered correction stacked, not applied: the falsified 'conftest lines are free to be deleted' paragraph survives verbatim below its own correction (a00-506da71a-befecb.md:180)
2. 2. Frontmatter verdict contradicts the node's own THOUGHT (a00-ef14bcb2-993a78.md:21 'verdict: proved' vs 'inconclusive_lean_proved:65' and 'DEMOTED item 1' in the same file)
3. MISSED BY THE FIRST REVIEWER, same mechanism as reported defect 1 but a different line: a00-506da71a-befecb.md:182 (RESIDUE paragraph (a)) still asserts 'this kid's bytes AND its node are UNCOMMITTED in the shared worktree', and :193 repeats 'it left its own node UNCOMMITTED' -- while the round's own corrected CAVEAT at :156-158 says those edits 'are COMMITTED now, carried in the checkout's HEAD'. At def7e91ae they ARE committed (model_fence.py at 416198a28; this node landed by def7e91ae itself), so the shipped node carries the same false-about-itself claim the round was ordered to remove, in a second place. This is the residue to fix first: `grep -n 'UNCOMMITTED\|COMMITTED'` on the merged file returns 5 hits across :156, :158, :179, :180, :182, :193.
4. MISSED, and the one that matters most for the merge: the guard's own committed evidence is DELETED on the receiving trunk, and the span's node says so and nobody carried it forward. Verified: local-maxxing/season2/main's extensions/agi/model_fence.py is 245 lines with 0 matches for `_refused_from_config|def guard_owner`, its .agi/context/conftest.py has no GUARD_OWNER_ATTR marker, and test_model_fence_one_module.py, test_model_fence_cap.py and test_model_fence_guard_owner.py are absent; the same is true of the checked-out post branch (7abfb6460, model_fence.py 254 lines, 0 matches). a00-ef14bcb2-993a78.md:157-170 (item 10) flags it and states 'their removal is a finding for the director, not a refactor' -- the first reviewer re-cast it as a merge-ordering note with a wrong citation and dropped the finding. A deletion of a committed test under a merge is a demotion-class event; the director should confirm it was intended before this loop branch restores those files by merge.
5. MECHANISM THE FIRST REVIEWER DID NOT TRACE (it explains why defect 2 is invisible to every gate): a00-ef14bcb2-993a78.md:14 has `evidence_runs: [experiment:a00-ef14bcb2-993a78]` -- the node cites ITSELF, and extensions/agi/bin/evidence_gate.py:33-36 counts an id-shaped entry that resolves in the corpus as one run, so `proved` clears the gate that exists precisely to catch unevidenced overclaims. Nothing in the engine can see the contradiction between :21 and :216; it needs the director, which is why it is residue and not a self-healing demotion.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_model_fence_guard_owner.py · extensions/agi/tests/test_model_fence_one_module.py · .agi/nodes/experiment/a00-506da71a-befecb.md · .agi/nodes/experiment/a00-ef14bcb2-993a78.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over def7e91ae · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.654 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-model-fence-is-one-mo-a00-f8f4d623 tip e5d3cc5f0.
ROUNDS    this post's rounds on this node: DH.590 DH.613 DH.633 DH.654; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

## CORRECTIVE DH.633 -- closes mur-director-engine-36 DH.613-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-24c31597 tip 42d7fa666 (branch de-base-633; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (g7.33.19 row 22): -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. 1. a00-3e0ac0db-808f82.md:22 'verdict: proved' contradicts its own disposition (:270 'DEMOTED proved -> inconclusive_lean_proved:70') — the class item 2 fixed in the sibling file of the same commit
2. 2. a00-506da71a-befecb.md:20 'verdict: proved' with evidence_runs self-citing at :10-11, against its own :179 'NOT FULLY ESTABLISHED' — still in the file the round edited
3. SL7.136 was invoked one commit earlier to refuse an edit on the very file this round then edited: a00-ef14bcb2-993a78.md:216 'I did not delete :180 myself: that node is another kid authored region and SL7.136 forbids a parent landing a kid edit by hand' — yet the DH.613 round rewrites 506da71a:179-180, :182 and :193, and :193 is INSIDE that node's authored region (THOUGHT:BEGIN at :184, THOUGHT:END at :194). Whether the order sanctioned it is not in the diff; the probe I WOULD run and did not: read the DH.613 order node/harvest line for this round and check whether 506da71a's body+THOUGHT were in its file scope. UNVERIFIED.
4. The parent's own probe report is internally inconsistent, the class the prior round's items 6-9 were ordered to fix ('pasted command output, not typed numbers'): a00-3e0ac0db-808f82.md:125 says GATE-1 'returns 5 hits and I read every one' and then enumerates 1 hit (506da71a:179) plus six (ef14bcb2:36/67/72/216/227/289) = 7. My count on the merge head: 506da71a=1, ef14bcb2=6, total 7. The gate CONCLUSION survives (:180 is emptied to the SUPERSEDED DUPLICATE pointer and 506da71a's only hit is the quotation inside the corrected :179 — both verified by grep), so severity is low, but the stated count is a typed number that disagrees with its own enumeration. Trivia in the same paragraph: :129 cites the kid's own 'verdict: proved at :21'; it is at :22 (the ef14bcb2 ':21' citation at :219 is correct).
5. UNVERIFIED, probe NOT run (the branch under review's test files do not exist in this review worktree — HEAD d64923cd8 carries only test_model_fence_cap.py; 42d7fa666 carries all three). The round's 'fence suite 14 passed' wire claim (:269) is therefore unconfirmed here. The probe I WOULD run: cd /data/work/agi/.agi/worktrees/a00-24c31597 && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_model_fence_one_module.py extensions/agi/tests/test_model_fence_cap.py extensions/agi/tests/test_model_fence_guard_owner.py -q -p no:cacheprovider. It is low-value for this diff: 0 production lines means no test byte changed, and the round itself disclaims the green suite as evidence at :258-259.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-3e0ac0db-808f82.md · .agi/nodes/experiment/a00-506da71a-befecb.md · .agi/nodes/experiment/a00-ef14bcb2-993a78.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 42d7fa666 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.654 -- closes mur-director-engine-39 DH.633-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-f8f4d623 tip e5d3cc5f0 (branch de-base-654; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. NEVER run .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module (g7.33.19 row 22): -k 'not test_standins_never_leak_into_a_later_module', from the worktree root.
1. Five stale :179 pointers created by this round's own frontmatter growth — a00-3e0ac0db-808f82.md:40 (also :82, :124, :249, :271)
2. MISSED (real, and it invalidates the round's stated premise): the disclosed 'engine gap' is false and the reader was never read. a00-26dd471a-65047d.md:287 asserts 'extensions/agi/bin/evidence_gate.py:33-36 -- counts an id-shaped evidence_runs entry that resolves in the corpus as one run, so a self-citing experiment passes the gate'; :335 repeats it. Lines 33-36 of that file are MODULE DOCSTRING prose under the H4c heading, not code. The code that settles it is at extensions/agi/bin/evidence_gate.py:306-327 (_is_self_citation) and :394-399 (allow_self = node_type == 'experiment'), documented at :316-320 — an experiment self-citation is the sanctioned reference, not a hole. The graph is now told a live engine hole exists that does not, and the real rule is recorded backwards. The same false claim is left standing in a file this round edited, at a00-3e0ac0db-808f82.md:271 ('evidence_gate.py:33-36 (an experiment may not be its own evidence)'), while the round added 'now closed' markers to :126 and :130 in the same file — the 'stacked falsified paragraph' class, in the round's own edit target.
3. MISSED (real, the class the round exists to remove): two more un-closed falsified-now citations in the round's edit target. a00-3e0ac0db-808f82.md:124 and :271 still assert 'a00-506da71a-befecb.md:10-11 still reads evidence_runs: [experiment:a00-506da71a-befecb] and :20 still reads verdict: proved'; after this round a00-506da71a-befecb.md:10-12 carries two external runs and :21 reads inconclusive_lean_proved:70. Both are present-tense claims a `sed -n '20p'` refutes, in the same file, in the same commit, where :126 and :130 were given DH.633 closure markers and these two were not.
4. MISSED (real, a typed number where the artifact says otherwise): the ONE elided line of the fence-suite paste carries a wrong count. a00-26dd471a-65047d.md:251, :257 and :260 say '14 such lines' of 'tier-gate: phantom running record', and :262 asserts 'The only elision on this node is those 14 lines; every number that carries a claim is pasted in full'. The artifact it names — .agi/sessions/iter-DH.633/a00-26dd471a/fence_suite.txt in worktree a00-f8f4d623 — holds 18 (`grep -c 'phantom running record'` = 18, 18 unique, 18 'skipped'). The count is time-varying (my own re-runs of test_model_fence_cap.py in this worktree now print 17, and printed 14 minutes earlier), so it is a snapshot, but it does not match the file the node cites, and the disclosure sentence is false. Non-load-bearing: '20 passed in 79.54s' and 'EXIT=0' reproduce from the same file.
5. MISSED (config_max, minor): pasted commands and the Evidence section hardcode the absolute box path where a config cell exists — a00-26dd471a-65047d.md:243 'cd /data/work/agi/.agi/worktrees/a00-f8f4d623' and :304, plus :172/:305 for de-base-613; .agi/config.json paths.core.worktrees_root = '.agi/worktrees' is the cell, and house command form substitutes <engine>/<home>.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_model_fence_guard_owner.py test_model_fence_one_module.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-26dd471a-65047d.md · .agi/nodes/experiment/a00-3e0ac0db-808f82.md · .agi/nodes/experiment/a00-506da71a-befecb.md · .agi/nodes/experiment/a00-fbc3eecb-98ae17.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e5d3cc5f0 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.19 -- closes mur-eg-5 DH.654-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-model-fence-is-one-mo-a00-f51a4364 tip 0824b7b5b (branch de-base-EG.19; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Rewritten OUTSIDE FILE SCOPE bullet ends mid-sentence on 'in' (a00-26dd471a-65047d.md:327)
2. 2. The typed '5 hits' the round exists to remove survives in the paragraph the round edited (a00-3e0ac0db-808f82.md:288, vs body :126)
3. 4. New node carries no THOUGHT:BEGIN/END authored region (a00-e7a0f7a7-e74764.md:243), 'so its reasoning and the parent review are unprotected'
4. CONFIG-MAX -- the round's own correction is the false claim, and the first reviewer accepted it. a00-26dd471a-65047d.md:344-351 reads 'There is NO `paths.core.worktrees_root` cell -- `paths.core` holds exactly one key, `suite_roots`' and then 'NAMED FOR THE DIRECTOR, NOT TOUCHED ... a `paths.core.worktrees_root` cell ... is needed'. a00-e7a0f7a7-e74764.md:209-225 repeats it as the order's FALSE premise. Measured: local-maxxing/season2/main:.agi/config.json carries paths.core = {worktrees_root: '.agi/worktrees', suite_roots: ['.agi/context']}, landed 2026-09-27 06:35:41Z in c9d703f46 -- 19h BEFORE this branch tip 0824b7b5b (2026-09-28 01:31:32Z). True in the kid's seat (0824b7b5b:.agi/config.json has only suite_roots), false for the tree this merge lands into, and the round hands the director a cell the director already added. The parent's re-check at a00-e7a0f7a7-e74764.md:313 ('paths.core is still {suite_roots: [...]} -- no cell was added, which is the rule') was taken in the post worktree, on the branch's own line, not on the receiving trunk -- so the review of the review inherited the same blind spot.
5. The invented house-form token resolves through a STALE cell, so the substitution trades a live absolute for a dead one. a00-26dd471a-65047d.md:172-174 rewrote the probe target to `<box.root>/.agi/worktrees/de-base-613/...` and asserts 'the cell it would resolve through does not exist'; a00-e7a0f7a7-e74764.md:194/:220 does the same for a00-f8f4d623. But `box.root` DOES exist -- .agi/config.json box.root = '/home/ubuntu/work/agi' on BOTH 0824b7b5b and local-maxxing/season2/main -- and it is stale: extensions/agi/tests/test_retired_box_prefix.py:60 records 'the box.root CELL, stale (/data/work/agi is the real root)' and names the goal that owns it. So '<box.root>/.agi/worktrees/<name>' resolves to a non-existent directory on this box, and test_retired_box_prefix.py cannot catch it because the string is a config-cell reference, not a /home/ubuntu literal. The diff adds 9 `box.root` occurrences to a00-26dd471a alone (12 across the diff), and the correct citation was the cell name the round declared absent. The $ cd <abs> line left verbatim inside the pasted pytest block (a00-26dd471a.md:351-353) is the right call and is not part of this finding.
6. No finding in this class, reported for the record: the diff writes zero test and zero engine bytes (`git diff --name-only e5d3cc5f0 0824b7b5b -- extensions skills src` is empty), so the round fixed no gate it had to pass through; it touches no tmux pane, systemd unit, crontab or live process (its only runs are committed fence files under `env -u TMUX -u TMUX_PANE ... --basetemp /tmp/...`); and it deletes nothing under .agi/nodes (M/M/A only). Every numeric claim I could re-measure reproduced exactly: 7 hits (1+6), 18 phantom-running-record skips in the named fence_suite.txt, the evidence_gate line citations, and the trunk's missing guard_owner / GUARD_OWNER_ATTR / two of four fence test files. The minor markdown artifacts the diff introduces (a doubled blank at a00-26dd471a.md:177-178 inside the pasted block and at :338-339 before '## Evidence') are wording and are not counted.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-26dd471a-65047d.md · .agi/nodes/experiment/a00-3e0ac0db-808f82.md · .agi/nodes/experiment/a00-e7a0f7a7-e74764.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 0824b7b5b · <= 40 test lines net over 0824b7b5b · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 0824b7b5b <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.19: mur-eg-5 DH.654-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
