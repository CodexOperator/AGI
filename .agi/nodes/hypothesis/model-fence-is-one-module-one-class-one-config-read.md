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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.536: DH.535 parent OOM-killed (its 2G scope) running the context tests as a baseline; the director measured the culprit in a 1G scope = R4 test_standins_never_leak_into_a_later_module (child pytest); item 0 fences it (deselect + ulimit -v) and keeps R4 out of the claim. Fix order unchanged.
<!-- THOUGHT:END -->
