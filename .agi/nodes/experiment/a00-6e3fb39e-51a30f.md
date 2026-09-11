---
id: experiment:a00-6e3fb39e-51a30f
mint_id: 072a35b69fd1428294aa7ff266283414
type: experiment
parents:
  - hypothesis:l4-the-sb-status-wrapper-resolves-like-the-engine
next_edges: []
confidence: 0.9
edited_by: a00-ceaed4ce
evidence_runs:
  - experiment:a00-6e3fb39e-51a30f
loop: hypothesis:l4-the-sb-status-wrapper-resolves-like-the-engine@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2635731ec4a99543
season: 2
title: A00 6e3fb39e 51a30f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6e3fb39e-51a30f

## Experiment

Parent `hypothesis:l4-the-sb-status-wrapper-resolves-like-the-engine` is a
g15 claim being built across rounds. L4.229 already DONE (per the fix-only
claim on the parent's Agent Notes): the template (streamer-stub 8b50fe3) and
the deployed wrapper resolve a declared relative stub against its project
root, stop the walk at `.git`, keep the install-time fallback $HOME-relative
when a config has no cell, and the guard reads the executing line. THIS round
is the FIX-ONLY re-dispatch: `test_commands.py` gains the missing shape — the
config-without-a-cell fallback, the shape the L4.229 kid's tests never built
(and which was what broke the owner's `sb-status` from inside the agi seat).

FILE CHANGED: `extensions/agi/tests/test_commands.py` ONLY (the stub template
is done; a kid finding it wrong reports, does not edit). No git anywhere, no
touch of the foreign streamer-stub tree beyond a read.

Added `test_sb_status_wrapper_config_without_cell_falls_back_to_home(tmp_path,
monkeypatch)` (new @stub_only test, immediately after the existing configured-
stub test). It installs the wrapper into a scratch $HOME from the LIVE
template (`locations.streamer_stub(REAL_ROOT)/bin/install-cli.sh`) with the
install-time stub under home (so the fallback is spelled $HOME-relative), then:

 (1) CONFIG WITHOUT A CELL -> INSTALL-TIME FALLBACK. A project whose
     `.agi/config.json` is `{"locations": {}}` (config present, `streamer_stub`
     cell absent — the agi-seat shape). Run the generated wrapper from inside
     it; assert the INSTALL-TIME stub answers (`str(inst_stub) in out`) AND
     that the direct re-root-under-project spelling is absent
     (`str(proj / "work" / "streamer-stub") not in out`). The latter is the
     falsifier: the L4.229 bug re-rooted the fallback under the project, so
     this assertion is RED on the old template.
 (2) SAME RUN, DECLARED-RELATIVE STILL RESOLVES PROJECT-RELATIVE. A project
     whose config declares `"streamer_stub": "rel/stub"`. Run from inside it;
     assert the project-root-relative stub answers and the install-time one
     does not — guarding that the fix did not break the other half of the
     claim.

## Evidence

    cd <checkout> && python3 -m pytest extensions/agi/tests/test_commands.py -q
    37 passed in 2.37s

37 = 36 prior + 1 new. The @stub_only guard is satisfied (stub present on this
box), so the new test genuinely ran the generated wrapper from the LIVE
template. conftest-derived tier is kid-appropriate.

Manual reasoning on the falsifier (not run — the suite assertion IS the
falsifier probe): on the OLD template, `_base="$_root"` unconditionally when
a config resolved, so `{"locations": {}}` would set `_base=<noproj>` and
resolve `stub=<noproj>/work/streamer-stub` (fb stayed $HOME-relative) —
assertion (1)'s `str(noproj / "work" / "streamer-stub") not in out` fires.
On the shipped template (8b50fe3), `_decl` is empty so `_base="$HOME"`, the
install-time stub answers, and the falsifier is silent. Both directions green.

## Agent Notes
test_commands.py gains the missing config-without-a-cell shape on the generated sb-status wrapper (install into scratch HOME from LIVE template; config {'locations':{}} -> install-time $HOME fallback, not re-rooted under project; declared-relative still project-relative in same run); 37 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.231 (a00-ceaed4ce). VERDICT KEPT: proved, confidence 0.9.

(1) WHAT THE INSTRUCTION SAID. The FIX-ONLY CLAIM on the parent node: "test_commands.py gains the missing shape -- install into a scratch $HOME from the LIVE template, create a project whose .agi/config.json has NO streamer_stub cell, run the generated wrapper from inside it, assert the INSTALL-TIME stub answers (and not <project>/<fallback>)". FALSIFIER: "the config-without-a-cell shape resolving under the project."

(2) WHAT THE MACHINE ACTUALLY DOES. Read the added test at extensions/agi/tests/test_commands.py:948-1010: fixture {"locations": {}}, runs the generated wrapper, asserts str(inst_stub) in out AND str(noproj/"work"/"streamer-stub") not in out, then a same-run declared-relative project-relative half. Ran the suite: 37 passed. Independently materialized the PRE-FIX template (streamer-stub 6bb09b8 -> /tmp/oldstub) and ran it against the SAME fixture: it resolved <project>/work/streamer-stub and exited 127 with hold.sh: No such file or directory, so the test assertion is RED on the old bytes; shipped 8b50fe3 prints STUB:<home>/work/streamer-stub. The regression guard is real, not documentary.

(3) NEAR MISS. A test that asserted only str(inst_stub) in out on the new template would satisfy the sentence and be vacuous: _fb is $HOME-relative on BOTH templates, so the install-time stub answers either way. Only the negative assertion (plus rc==0) discriminates, and it is present.

(4) DEVIATION. None. Kid scope was test_commands.py only, no git anywhere, foreign stub tree read-only.
<!-- THOUGHT:END -->