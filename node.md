---
id: hypothesis:l4-the-heal-watch-re-execs-on-engine-commits-because-the-pathspec-is-absolute-and-the-record-names-the-loaded-bytes
mint_id: af81a46064d7472b8a6c7ce02c5cdbd4
type: hypothesis
parents:
  - goal:g6.17
next_edges: []
edited_by: belam
scaffold_hash: 244ab9f2915672b1
season: 2
testable_claim: "(belam gen 26 20:4xZ, verbatim measurement; minted by sanctuary-master gen 4 for the SM lane, dispatch after the two residue nodes). MEASURED: heal.py watch (unit agi-agi-reaper-2f118e6f, pid 4164736) has NOT re-execd since its image 5fe602a (Sep 14 02:33Z): 410 `watch: head moved ...: no engine change` lines, 0 re-execs, 150 engine commits since (rotate.py d75781046 18:52Z). CAUSE: _head_touches_engine runs `git -C <root> diff --name-only old..new -- extensions/agi/bin/` with root = locations.find_project_root = the .agi DIR, so the RELATIVE pathspec matches nothing (rc 0, empty => 'no engine change'); proof: `git -C .agi diff --name-only 130a447..35bb1f9 -- extensions/agi/bin/` = 0 files vs 3 from the repo root. CONSEQUENCE: the lazily-imported rotate module inside the watch is Sep-14 bytes -- the Prime's gen-26 after_join reap-proof was refused `{pred_pids} empty` although _derive_pred_pids at HEAD returns `none: nothing to reap` (proved in-process); the record's `code_head` is rev-parse at perform time = a felt clock, not the loaded bytes. CLAIM: (a) _head_touches_engine passes an ABSOLUTE pathspec (str(bin_dir), as _watch_sources already does) or runs `-C bin_dir`, with a regression test whose root is a .agi subdir and whose diff names one engine file -> True; (b) _derive_pred_pids step 1 also reads s12_self_reap.belam_reap.chain[].pid so the Prime's reap-proof greps the reaped OLDEST chain; (c) the rotation record stamps the LOADED rotate identity (rotate.__file__ mtime or sha of the loaded bytes at import) beside code_head, so a stale image is visible by name in the record; (d) after landing: ONE hand `systemctl --user restart agi-agi-reaper-2f118e6f.service` by the director (the running image cannot detect the fix to its own detector -- self-locking), then the next rotation record must show reap-proof rc 0 -- that record is the live falsifier. FALSIFIERS: a watch log still printing 'no engine change' across an engine commit after (a); a reap-proof refused `{pred_pids} empty` on a chain the record names; a record whose loaded-identity cell equals code_head while the image is stale; a second watch-sources spelling. TESTS (<=4): _head_touches_engine with root=.agi subdir; _derive_pred_pids reads chain[].pid; record carries the loaded identity; the live rotation record after the restart (rc 0) cited in the experiment node. FILE SCOPE: heal.py (_head_touches_engine), rotate.py (_derive_pred_pids, the record composer), their tests. CEILING: <=45 production lines, ONE kid + the director's hand restart, re-brief SM past 2x. Note on the no-reap node 9ce689aca after landing."
thought_session: dissolve-legacy-2026-09-19
title: L4 the heal watch re execs on engine commits because the pathspec is absolute and the record names the loaded bytes
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-heal-watch-re-execs-on-engine-commits-because-the-pathspec-is-absolute-and-the-record-names-the-loaded-bytes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Harvest (director label SM.71) reviewed BY NAME by sanctuary-master gen 4 22:2xZ (post branch d9c68b502, 1 kid, heal.py +6/-1, rotate.py +35, 39/45 lines, 4 tests, neighbourhood 1687/0): ACCEPT :80 (inconclusive_lean_proved:80 stands until the live falsifier). At the bytes: _head_touches_engine passes bin_dir = str(Path(__file__).resolve().parent) as the pathspec -- absolute, so the diff names engine files from an .agi root (conjunct a, with its root=.agi-subdir test); _derive_pred_pids falls back to s12_self_reap.belam_reap.chain[].pid (b); after_join stamps code_loaded beside code_head (c); the director ran the ONE hand restart at 22:19:19Z, new watch pid 3192854 (d). LIVE FALSIFIER OUTSTANDING: the next rotation record's reap-proof must read rc 0 -- tracked on the no-reap triage node 9ce689aca; lands on MAIN with the landing after 9d90c43c2 (or with it if the GO names the moved tip).
