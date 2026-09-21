---
id: hypothesis:l4-level3-no-flag-default-refuses-a-rootless-cwd-and-the-sl7-25-body-names-its-missing-and-orphan-counts
mint_id: df0b5c78220b4afaaec1851ee9c47a9d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count
next_edges: []
edited_by: sensei-director
scaffold_hash: bb972cd8750b1127
season: 2
testable_claim: "goal:g15 FIX-ONLY node, mur-SL2.18 (Prime XV 11:09Z, by name, wf_ba6f364a-870; g17.1 note 793b21281) line (3) — SL7.25 ACCEPT with residue. Cite at cd959870d; re-measure on your base (HEAD 7f0ede08f). MEASURED: (i) extensions/agi/bin/level3.py:173 `PROJECT_ROOT = locations.project_root_from_env() or Path(os.getcwd()).resolve()` — with no --project flag the default falls back to the RAW cwd without going through `resolve_project_root` (176), so a no-flag run from a rootless directory still writes/reads a `<cwd>/nodes/...` tree — exactly the stray-tree hazard the docstring above 173 records, now closed only for the --project spelling (1169 `resolved = resolve_project_root(args.project)`; 1176 `project_root = PROJECT_ROOT`); (ii) the SL7.25 kid node experiment:a00-1cf94a6c-67305c calls the real-graph re-run 'clean' (line 45 'rc=0 non-strict = clean') while the same run reports 18 missing_payload + 108 orphan_files — the wording, not the code, is wrong. CLAIM: (a) the no-flag default resolves through the SAME `resolve_project_root` (env value first, then cwd) and refuses by name (`ERR ... no graph root at <path>`, non-zero) when neither resolves, matching the --project refusal byte-for-byte in shape; (b) the kid node body says what the run measured — rc 0 non-strict with 18 missing_payload and 108 orphan_files named — and drops the word clean (edit the body prose in place, one sentence; verdict and confidence untouched). FALSIFIERS: `cd /tmp/<rootless> && python3 level3.py --verify` still exits 0 with `level-3 nodes: 0`; the env spelling (AGI project root env) stops resolving; the body still reads clean. TESTS: a no-flag rootless run refuses by name; a no-flag run from inside a worktree resolves its nearest .agi; --project behaviour unchanged (existing tests). FILE SCOPE: extensions/agi/bin/level3.py (the default at 173 and main's resolve, only), extensions/agi/tests/test_level3*.py, the one kid node body sentence. EXCLUDED: stitch.py (already resolves), locations.py. CEILING: one resolver, no new flag."
thought_session: sensei-director-genXI-L11
title: level3.py's no-flag default resolves the graph root or refuses by name like --project does, and the SL7.25 kid body names its 18 missing_payload and 108 orphan_files instead of calling the re-run clean
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-level3-no-flag-default-refuses-a-rootless-cwd-and-the-sl7-25-body-names-its-missing-and-orphan-counts

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
