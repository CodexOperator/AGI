---
id: hypothesis:pb3-drift-test-s26-caller-injective-json-field
mint_id: 58d401d0c7f84ad78de6991eb8a40e2e
type: hypothesis
parents:
  - goal:g1.31.4.6.1
next_edges: []
edited_by: director-general-6
scaffold_hash: 2fdfcac2177e6e0f
season: 2
testable_claim: test_engine_drift.py covers drift_check.py's unpinned, one-repo, clone-match and clone-drift cases; a verification.py check calls warn_premature_complete and report_integrity over mint-resolved parents as a never-failing note, flipping the BANKED 86 strict xfail green; rings.json_field encodes a str like every other value so json_field(1) != json_field('["int",1]').
title: The drift mechanism gets a behavioural test, goal:s26's warning regains a verify-pass caller, and json_field becomes injective
town: core
---
# hypothesis:pb3-drift-test-s26-caller-injective-json-field

## Measured
```
drift mechanism (driver.sh drift block · bin/drift_check.py)    behavioural tests: 0
   only hit: test_commands_manifest.py _LISTED_CLIS (a filename)          -k engine_drift -> exit 5
snapshot-goals.py  warn_premature_complete (goal:s26) · report_integrity · collect_parent_refs
   production callers: 0 (main = retired entry point, return 2)   test callers: test_lifecycle_guards.py x5, test_links.py x1
   test_links.py test_w2cb_snapshot_goals_integrity_reads_a_mint_twin_as_its_address_twin
       @xfail(strict) "BANKED 86 … re-wire (then resolve) or retire"   <- collect_parent_refs reads raw (mint) parents
seatsig/rings.py json_field   str -> unchanged ; non-str -> json.dumps(_enc(v))
   json_field(1) == json_field('["int",1]') == '["int",1]'   (probe at HEAD: True)
   test_rings.py test_json_field_nested_keys_injective: assert json_field("plain") == "plain"  <- green test requiring the defect
   callers: write.py _config_write_fields (sign side, DG3's file) · dispatch.py pre-round fields · load_rings = [] (no live ring)
```
- Verdict files: `mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json` item 3; `mur-pb3chunk2of20/verify_engine-delta-4.json` item 1; `mur-pb3chunk8of20/verify_l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate.json` (json_field). Residue, open at HEAD.

## CLAIM
(1) A committed `test_engine_drift.py` drives `drift_check.py` (the ONE mechanism after pb3-engine-root-one-resolver-pin-retired) in tmp repos: unpinned -> silent/NOT PINNED, one-repo -> not applicable, clone layout match -> OK line, clone drift -> WARNING line; exit 0 in every case without `--strict`.
(2) `verification.py` gains a `goal-s26` check that builds the corpus once (parents mapped through `links.address_resolver`) and calls `warn_premature_complete` and `report_integrity`; it reports offenders and unresolved counts as a PASS note and never FAILs (s26's warning contract). `collect_parent_refs` takes an optional `resolve=` (the graph_core loader convention), so the strict xfail flips green and its marker is removed.
(3) `rings.json_field` is injective across types: a str is encoded like every other value (`json.dumps(_enc(v))`), so `json_field(1) != json_field(json_field(1))`; its docstring and `test_rings.py` state the injective form. Sign and verify sides both call the same function, changed in one commit.

## Dispatch line
config-max: none (no value moves; the check's name joins the verify pass's check list in code, as every sibling check does).
template-max: none.
code: the missing caller (verification.py check) + `resolve=` on `collect_parent_refs`; `json_field`'s str branch removed. Test-only for (1).

## FALSIFIERS
- `python3 -m pytest extensions/agi/tests -q -p no:cacheprovider -k engine_drift --basetemp /tmp/pb3s26` exits 5 or red
- `git grep -n -e 'warn_premature_complete(' -e 'report_integrity(' -- extensions/agi/bin ':!extensions/agi/bin/snapshot-goals.py'` returns 0 hits
- a tmp graph with a `complete` goal over an `active` subgoal (parent written as its MINT id) yields no offender in the check's note, or the check FAILs
- `git grep -n 'BANKED 86' -- extensions/agi/tests/test_links.py` returns a hit
- `json_field(1) == json_field('["int",1]')`, or `git grep -n 'json_field("plain") == "plain"' -- extensions/agi/tests/test_rings.py` returns a hit
- any `test_write_ring_cli.py` / `test_ring_cli_seam.py` / `test_veto.py` / `test_promotion.py` / `test_cli_wait.py` row red (sign/verify drifted apart)

## TESTS
- NEW `extensions/agi/tests/test_engine_drift.py` (4 rows, tmp git repos, synthetic shas, `SKIP_ENGINE_DRIFT_CHECK` unset).
- `test_links.py`: the xfail row passes `resolve=links.address_resolver(root)`; marker removed. `test_lifecycle_guards.py` unchanged and green. `test_verification.py`: + the goal-s26 check row (mint-parent twin, PASS with offender note).
- `test_rings.py`: the "plain" assert becomes the injective one.
- Neighbourhood: `python3 -m pytest extensions/agi/tests/test_engine_drift.py extensions/agi/tests/test_links.py extensions/agi/tests/test_lifecycle_guards.py extensions/agi/tests/test_verification.py extensions/agi/tests/test_rings.py extensions/agi/tests/test_write_ring_cli.py extensions/agi/tests/test_ring_cli_seam.py extensions/agi/tests/test_veto.py extensions/agi/tests/test_promotion.py extensions/agi/tests/test_cli_wait.py -q -p no:cacheprovider --basetemp /tmp/pb3s26` · `python3 extensions/agi/bin/commands.py run verify` (the round's worktree).

## FILE SCOPE
extensions/agi/tests/test_engine_drift.py (NEW) · extensions/agi/bin/snapshot-goals.py (`collect_parent_refs` only) · extensions/agi/bin/verification.py (the new check + its registration only) · extensions/agi/src/seatsig/rings.py (`json_field` only) · extensions/agi/tests/test_links.py · extensions/agi/tests/test_verification.py · extensions/agi/tests/test_rings.py

## CEILING
kids <= 3 (A: drift test, test-only, cut from pb3-engine-root-one-resolver-pin-retired's tip · B: s26 caller + resolve= · C: json_field) · 10-12 production lines per conjunct · pi-free parents · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · write.py is DG3's: the `<unset>` sentinel collision (#37) is NOT fixed here and no write.py byte moves · verification.py is also edited by pb3-window-tip-fake-proc-per-model-denominator (render_window) — cut the later from the earlier's tip.
