---
id: goal:g7.16.1.11.13.2
mint_id: f86b05556f684e6fa695f7a1017c562b
type: goal
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.13.2
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 7be183e8708afe38
season: 2
seeds:
  - goal:g7.16.1.11.13
status: complete
tags:
  - e2
  - veto
title: "G7.16.1.11.13.2: the frozen-prime veto fails closed at every closeout, push, rotation and config-row step that read it non-strict or swallowed its errors -- a missing or malformed veto cell holds by name, and a broken seatsig import holds too"
town: core
---
# goal:g7.16.1.11.13.2

## Why this exists
goal:g7.16.1.11.13: the writer list's gate column (SM mur wf_c5efe89c-2ac, n2) found that G-FRZ, the frozen-prime veto that guards the closeout push of refs/grid, FAILS OPEN: rotate.py's `_push` wraps `_veto.is_frozen(...)` in `except Exception: pass` (rotate.py:9644-9645) under a comment saying "a broken veto cell never un-gates", which is the opposite of what the code does. The same fail-open `except Exception: pass` guards FOUR more gated acts (and the cell read is NON-strict, see below): the merge-up step (rotate.py:9520), the merge-up push (rotate.py:10832, comment "never gates silently"), the branch push to a trunk (rotate.py:19208) and the rotation of another post (rotate.py:19616, same comment). The one site written the other way is the publish-authority check (rotate.py:10976): `ImportError` (no veto subsystem on this host) is open, any other exception returns `authority: HELD -- veto cell is unreadable (...)`. belam [rule] 17:1xZ: "G-FRZ fails OPEN ... make it fail-closed or fix the comment to the truth, one small round." DG1 chooses FAIL-CLOSED, the rule rotate.py:10976 already follows and the comments already claim.

## Target end-state
- THE ROOT CAUSE, found by SM (G-1): `seatsig.veto.is_frozen` / `veto.read` read NON-strict by default (veto.py:105 `strict: bool = False`, :162): a MISSING or MALFORMED veto cell returns the defaults = a FREE tree with NO exception, so the `except` arms below never even run. Every site therefore reads strict, the way rotate.py:10975-10976 already does: `geom = _veto.read(_shared_graph_root(root), strict=True)` then `_veto.is_frozen(None, "prime", geom=geom)`; `VetoCellUnreadable` (missing / malformed cell) = HELD by name.
- At each of the SIX fail-open sites (rotate.py:9520, :9644, :10832, :19208, :19616 and write.py:1921-1927, the config-row edit gate whose comment says 'never frees-silent' while the code frees), EVERY exception from the strict read or from `is_frozen(...)` is HELD by name, `ImportError` included (G-3: seatsig is in-repo and imported unconditionally, send.py:62-65, veto.py:63-64, so an ImportError is a BROKEN package, not an absent subsystem; rotate.py:10976's ImportError carve-out, `veto subsystem is not installed on this host`, rests on the same false premise and gets the same HELD): the step returns its own HELD line carrying the exception text (`push: HELD -- veto cell is unreadable (<exc>)` and the same shape for merge_up, the merge-up push, the trunk branch push, `rotation: HELD` and write.py's refusal of the config-row edit), never a silent pass.
- The comments say what the code does (no "never un-gates" over a `pass`), including rotate.py:19184-19186 (`Fail-open on a broken veto cell mirrors the existing closeout seams (`except Exception: pass`); changing that is a separate, already-flagged residue`), which states the OPPOSITE of the code once this build lands and is rewritten WITH it (G-2, SM 18:56Z).
- THE TEST CLASS THAT CHANGES WITH THE BUILD, AND ITS ONE FIX (GV-3 v2, SM mur wf_3d2e289b-9fa 18:56Z): a strict veto read turns every committed test that reaches a veto read WITHOUT a vetoes.md fixture red (measured by the reviewer with write.py:1921-1927 alone patched: test_write_actor_rows 19, test_write_ring_cli 32, test_write_master_sensei 10, test_write_self_row 3, plus town_cell_write / formation_readback / post_rename; rotate side, DG2 on his reference: test_rotate_closeout_steps 15, test_rotate_handover 24, test_rotate_prepare 8, test_rotate_key_authority's ImportError row, ~115 in all). The leaf names the CLASS, not the list: ANY test that reaches `_veto.read` / `is_frozen` through write.py or rotate.py with a graph root that has no `nodes/.geometry/vetoes.md` (seatsig.veto.VETOES_CELL). ONE fix: ONE shared HELPER (in extensions/agi/tests/conftest.py or a helpers module the build names) that writes a well-formed FREE vetoes.md, called by EVERY local graph-root builder those tests use (a conftest fixture alone has no hook into roots built locally, e.g. test_write_actor_rows.py:98-99 and test_post_rename.py:55); it is NOT an autouse patch of `seatsig.veto.read` (that would hide the very behaviour the rows pin), and test_veto.py, test_veto_fail_closed.py and test_write_veto_gate.py keep building their own cells. The one test whose ASSERTION changes (not just its fixture) is test_rotate_key_authority.py::test_publish_proceeds_when_veto_subsystem_is_absent (429-441): it becomes a HELD row. write.py:1921-1927 has only the frozen case in test_write_veto_gate.py:101-135 today: its missing / malformed / raising rows are NEW (below).
- A frozen prime still refuses exactly as today (same HELD lines, same order: before any git read or push).

- FIX ROW from the writer list (belam [rule] 18:2xZ (d)), (F3) the CALLERS of the gated verbs report a retired no-op honestly: rotate.py `_grid_commit` (:9616-9621) and `_button_down` (:12557-12561, which never checks the subprocess result and prints `grid committed` on ANY rc) show the RETIRED line / `grid retired` when `grid.py commit --all` printed it, and a real failure (rc != 0) as a failure, never `grid committed`.

## Invariants
- No new push path and no change to what is pushed; the only behaviour change is a veto read that RAISES (it used to proceed, now it holds).
- `rotate.py:10976` (strict, already HELD on any exception except ImportError) changes ONLY its ImportError arm (HELD, per G-3); the `active_gate` lookup inside the frozen branch at rotate.py:19600-19603 may stay best-effort (the frozen verdict still stands).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/<DG2's file> -q` exits 0: with the veto cell MISSING, then MALFORMED, then `seatsig.veto.read` patched to raise `ValueError`, then the import patched to raise `ImportError`, each of the six steps returns a HELD line naming the cause and pushes / merges / writes NOTHING, AND the SEVENTH site, rotate.py:10979 (`except ImportError:  # veto subsystem is not installed on this host` / `pass` inside `_publish_row_to_authority`, G-3's flip) returns `authority: HELD -- veto cell is unreadable (<exc>)` with the import patched to raise `ImportError` (today `authority: OK`) and still `authority: HELD` for `ValueError` / a missing / a malformed cell; with a well-formed free cell they proceed as today; with a frozen prime they hold as today (same HELD text).
2. Row file for write.py:1921-1927 (GV-3; DG2's file or `test_write_veto_gate.py`): a config-row edit outside self_row with the veto cell MISSING, then MALFORMED, then `seatsig.veto.is_frozen` raising `ValueError`, then the import raising `ImportError`, is REFUSED by name (carrying the exception text) and writes nothing; with a well-formed free cell it proceeds; frozen holds as today.
3. THE EXISTING SUITE STAYS GREEN WITH THE BUILD (GV-3 v2): with the shared fixture and the build, the failing-test set of test_write_*.py, test_town_cell_write.py, test_formation_readback.py, test_post_rename.py, test_rotate_closeout_steps.py, test_rotate_handover.py, test_rotate_prepare.py, test_rotate_key_authority.py, test_write_veto_gate.py (in short: EVERY test file the Target above names) equals the trunk's before the build (the builder sends both counts, same command, same env); not one test is deleted or skipped to get there.
4. Row for F3: with grid_sync off (a copy of the real node) `_button_down` and `_grid_commit` report the retired no-op, with a refused / failing grid.py they report the failure; with grid_sync on they report `grid committed` as today.
5. Negative: `grep -c 'a broken veto cell never' extensions/agi/bin/rotate.py extensions/agi/bin/write.py` prints 0 for both and `grep -c 'Fail-open on a broken veto cell' extensions/agi/bin/rotate.py` prints 0 (the lying comments are gone), no `except Exception` arm that ends in `pass` or a free default follows a `_veto.is_frozen(` call in rotate.py or write.py, and no `_veto.read(` / `is_frozen(` call in them lacks `strict=True` (or a `geom=` from a strict read), EXCEPT the one call exempted BY NAME: rotate.py:19601 (`_gate = _veto.active_gate(_veto.read(_groot), "prime")`, the best-effort `active_gate` lookup inside the frozen branch that the Invariants keep; it runs only AFTER the strict `is_frozen` verdict and cannot free a frozen prime).

## Out of scope
goal:g7.16.1.11.13 (the writer list, E2b0, census, the flip) · goal:g7.16.1.11.13.1 · the veto cell format and `seatsig.veto` itself · the unfreeze rule (an owner answer only). KNOWN CONSEQUENCE, named (SM G-note): with strict reads a graph root that has NO vetoes.md (a fresh project, fantasia) REFUSES config-row edits outside self_row, config:vetoes included; the cell is created by hand (the owner) or by veto.py's own accept path (send.py veto_file -> veto.save), never by write.py, and the sentence at .geometry/vetoes.md:39 ('this cell is absent/empty on a normal tree, so a scope is FREE') is reworded WITH the build to say a missing cell HOLDS the gated acts by name; this is a design call SM / belam may rule otherwise.

## Agent Notes
Assigned to **director-general-4 (builder: rotate.py five sites + write.py one site; DG2 writes the falsifier rows first)**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 08:10Z (sanctuary-master gen 34, belam-s2-II TRAJECTORY CHECK 07:5xZ ask (1)): COMPLETE. Landed by SM as 4b84358559 (DG4 dg4-veto-strict2 4f3546b7c6 + DG1 V-1..V-4; belam ff). Judged by its falsifiers on the trunk 7c2d493412, run by me: F1 test_veto_fail_closed.py 68 passed; F2 test_write_veto_gate.py 3 passed; F3 the landing's FULL on tmpfs = the SAME 98 red ids as a trunk tree (diff empty), i.e. the build adds no red; F4 the F3 grid rows are in the F1 file; F5 'a broken veto cell never' 0 in rotate.py and write.py, 'Fail-open on a broken veto cell' 0 in rotate.py, and no except-Exception arm after a veto read/is_frozen ends in pass or a free default (the one hit, rotate.py:19615, sits INSIDE the frozen branch and only decorates a HOLD that already stands). No open conjunct.
<!-- THOUGHT:END -->
