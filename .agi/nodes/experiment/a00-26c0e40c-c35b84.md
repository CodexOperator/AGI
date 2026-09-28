---
id: experiment:a00-26c0e40c-c35b84
mint_id: 9db03e7e895644f3b519abd9dbee2201
type: experiment
parents:
  - hypothesis:provisioning-reads-its-cells-through-one-import-route
next_edges: []
confidence: 0.9
edited_by: a00-cd9ce068
evidence_runs:
  - experiment:a00-26c0e40c-c35b84
loop: hypothesis:provisioning-reads-its-cells-through-one-import-route@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9a6a6726afcd73e1
season: 2
title: the can_fund loop now reaches _prov_cell and goes red on pre-fix bytes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-26c0e40c-c35b84

## What I built

DH.673 landed the production fix but shipped a VACUOUS guard: its 100-call loop ran
`provisioning.can_fund(tmp_path)` on a keyless fixture, so `credit_balance` returned
`None` and `can_fund` returned `(True, None)` at provisioning.py:227-229 — BEFORE
`_prov_cell`. `assert len(sys.path) == before` therefore passed on the PRE-fix bytes.
One thing changed this round: the committed test now drives a `can_fund` input that
REACHES `_prov_cell` (provisioning.py:234).

| cell | value | why |
|---|---|---|
| `monkeypatch.setattr(provisioning, "credit_balance", lambda root=None: (2.0, 1.50, 0.50))` | non-None | the old path short-circuited on None |
| config `provisioning.min_mint_remaining_usd` | `0.75` | differs from the code default `MIN_REMAINING_CREDITS = 1.0` |
| `remaining` | `0.50` | BELOW the floor → the call refuses, so the floor it read is printed |

**Choice (recorded, as asked):** `remaining` BELOW the floor, so `can_fund` refuses and
the refusal string NAMES the cell. The test asserts `ok is False` AND
`"$0.50" in reason and "$0.75" in reason`. That is stronger than the "proceeds" option:
if `_prov_cell` silently fell back to its default the message would say `($1.00)`, so the
test cannot stop reaching the cell without going red. 8 added / 1 removed test lines.

## Measurement 1 — RED on the PRE-FIX bytes (a4fe034f0)

```
$ git show a4fe034f0:extensions/agi/bin/provisioning.py > <scratch>/prefix_provisioning.py
$ grep -n "sys.path.insert" <scratch>/prefix_provisioning.py
67:sys.path.insert(0, str(Path(__file__).resolve().parent))     <- module scope
205:sys.path.insert(0, ...)   834: ...   1187: ...   1248: ...   1525: ...   <- 5 per-call pairs
$ env -u TMUX -u TMUX_PANE python3 <scratch>/prefix_red_driver.py <scratch>/prefix_provisioning.py
len(sys.path): 10 -> 110   outcome=(False, 'remaining credits ($0.50) below minimum ($0.75, provisioning.min_mint_remaining_usd) — minting a new key risks making the loop unfundable')
Traceback (most recent call last):
  File "<scratch>/prefix_red_driver.py", line 27, in <module>
    assert len(sys.path) == before, "a config cell read must not touch sys.path"
AssertionError: a config cell read must not touch sys.path
```
10 -> 110 entries, exactly the 5 per-call inserts x 2 (bin dir + `locations` parent) x
100 calls. The driver is the same loop/assertions as the committed test, loaded against
the pre-fix module via importlib.

## Measurement 2 — GREEN at my tip

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_bin_help_smoke.py \
    -q --basetemp=/tmp/eg81-a00-26c0e40c
1 failed, 161 passed, 12 skipped in 7.28s
FAILED test_provisioning.py::test_a_swept_lease_surrenders_its_credential_hash
```
The one failure is PRE-EXISTING and outside my edit (a `spawn_budget` lease-sweep
assertion: `['the-hash-not-the-secret', 'h-orphan'] == ['h-orphan']` — a leaked lease
hash from another test in the shared tree). My test, run alone:
`1 passed, 94 deselected in 0.10s`.

## Measurement 3 — CEILING vs the CUT tip a5478e026

```
$ git diff --numstat a5478e026 -- extensions/agi/bin/ extensions/agi/tests/test_provisioning.py
8       1       extensions/agi/tests/test_provisioning.py
```
Production paths (`extensions/agi/bin/`): empty → 0 added / 0 removed.
`provisioning.py` was NOT touched (its fix landed in DH.673).

## Outside file scope

- `extensions/agi/bin/spawn_budget.py` — `test_a_swept_lease_surrenders_its_credential_hash`
  fails on the base tree (sweep revokes a hash leaked by another test's lease file);
  a `_revoke_all` that filters the leases it actually swept would fix it. Not touched.

## Caveats

The RED was produced by a driver script replicating the loop against the pre-fix module,
not by running the committed test file itself against pre-fix bytes (pytest cannot be
pointed at a historical module without a conftest shim). The loop, stub and assertions
are character-identical to the committed test; a reviewer wanting the pytest-native RED
should copy the pre-fix file into the bin dir once and run `pytest -k one_import_route`.

## Agent Notes
de-vacuumed the sys.path guard: credit_balance stubbed non-None, remaining 0.50 below the 0.75 cell floor, RED on pre-fix (10->110) and GREEN at tip; 0 production lines

PARENT REVIEW (a00-cd9ce068, iter EG.81) — ACCEPTED, verdict proved, confidence 0.9.

THE BYTES (read, not the report): git diff --numstat a5478e026 HEAD = 8 added / 1 removed on extensions/agi/tests/test_provisioning.py, 0 on every production path. The 8 added lines stub provisioning.credit_balance to (2.0, 1.50, 0.50) and replace the old (ok, reason) == (True, None) assertion with ok is False plus a check that the refusal string carries $0.50 and $0.75. provisioning.py is untouched (still exactly one sys.path.insert at line 67, one import locations at line 69). Ceiling honoured: 1 kid, 0 production lines, <= 20 test lines.

PROBES (run by me, offline, no mint, tmp dirs under /tmp only):
  - GATE (the falsifier this round exists to kill): I staged the PRE-FIX module with git show a4fe034f0:extensions/agi/bin/provisioning.py into a tmp copy of the tree and ran THE COMMITTED TEST FILE ITSELF against it, not the kid driver script. Result: test_a_cell_read_reaches_config_by_one_import_route FAILS at line 297 with AssertionError: a config cell read must not touch sys.path / assert 127 == 27. The kid recorded a caveat that its RED came from a replicating driver rather than from the committed file; this probe CLOSES that caveat — the committed test is red on the pre-fix bytes and green at the tip (1 passed, 94 deselected).
  - WIRE: with a counting spy substituted for provisioning._prov_cell and credit_balance stubbed, 100 can_fund(root) calls fired the spy 100/100 times, all for min_mint_remaining_usd, with len(sys.path) 10 -> 10 and outcome (False, remaining credits ($0.50) below minimum ($0.75, provisioning.min_mint_remaining_usd)). The changed bytes are live on the path the test drives.
  - AUTH: can_fund(None) with no project still reads the DEFAULT floor and refuses by name at $1.00 (the code default, not a config value), and the zero-USD lane still reads its own cell (zero_usd_key_limit -> 0.01). Two distinct cells, one import route, both live.
  - CLAIM CHECK: the kid statement that the one failure is PRE-EXISTING holds. I ran the base tree at a5478e026 (base bin/provisioning.py AND base test file) and test_a_swept_lease_surrenders_its_credential_hash fails there identically (1 failed, 89 passed, 5 skipped). The kid named it as an outside-scope finding on spawn_budget.py instead of touching it, which is what the OUTSIDE rule asks.

MECHANISM, NOT WORDING. (1) The brief said the 100-call loop must reach _prov_cell and the test must go RED on the pre-fix bytes. (2) The machine does: the non-None credit_balance stub carries can_fund past the None short-circuit at provisioning.py:227-229 to the floor read at :234, and the refusal string carries the CONFIGURED $0.75, so the assertion cannot pass if the cell ever stops being read. (3) THE NEAR MISS: a stub returning a non-None tuple with remaining ABOVE the floor and the old (ok, reason) == (True, None) assertion kept would still be green on both pre-fix and post-fix bytes for the wrong reason — it would pass even if _prov_cell were deleted outright, because the floor it read is never printed. Asserting the REFUSAL TEXT is what makes the guard a guard; asserting only the tuple is not. (4) No standing rule was deviated from: the kid stayed inside FILE SCOPE and reported the pre-existing spawn_budget.py failure instead of fixing it.

STILL OPEN for the director, not fixed here: extensions/agi/bin/spawn_budget.py — test_a_swept_lease_surrenders_its_credential_hash fails on the untouched base tree because the lease sweep revokes a credential hash leaked by another test lease file (live_count 1 vs 0 at extensions/agi/tests/test_provisioning.py:251); a _revoke_all that filters the leases it actually swept would fix it. Outside this round FILE SCOPE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW PASS, EG.81 (a00-26c0e068) — the parent who judged this node, not the kid who wrote it.

WHAT THE INSTRUCTION SAID (the corrective, quoted): "1. Vacuous sys.path guard in the committed test (test_provisioning.py:290): the 100-call can_fund loop short-circuits at provisioning.py:227-229 before _prov_cell, so the guard passes on pre-fix bytes -> FIX: drive the path that REACHES _prov_cell ..., and paste the test RED on the pre-fix bytes ... then GREEN at your tip."

WHAT THE MACHINE ACTUALLY DOES (measured by the parent, on the bytes): the committed test now monkeypatches provisioning.credit_balance to the non-None triple (2.0, 1.50, 0.50) before the 100-call loop, so can_fund cannot return at the None short-circuit (provisioning.py:227-229) and must evaluate the floor read at :234; the loop's assertion is the REFUSAL TEXT ($0.50 and $0.75) rather than a truthy tuple. Staged against the pre-fix module the SAME committed test file fails: assert 127 == 27, AssertionError "a config cell read must not touch sys.path". At the tip it passes, with a _prov_cell spy firing 100/100 times and len(sys.path) 10 -> 10. Production bytes are identical to the cut tip a5478e026.

THE NEAR MISS: the shape that satisfies the instruction's words ("drive the path that reaches _prov_cell", "the test goes green") while guarding nothing is a stub whose remaining is ABOVE the floor with the old (ok, reason) == (True, None) assertion kept — the cell read then happens but nothing observable depends on it, and the test would pass identically against a provisioning.py with _prov_cell deleted. The guard becomes real only when the assertion names the value the cell returned. Symmetrically, the kid's own RED came from a driver script replicating the loop rather than from the committed file; a reviewer running only the kid's evidence would not have proven the committed artifact goes red, so the parent re-ran the committed file against the pre-fix module.

WHY THIS VERSION DIFFERS FROM THE PREVIOUS ONE: the kid's body is unchanged; this version adds the parent's review — the byte diff against the cut tip, four parent-run probes (gate on the committed file, wire via a _prov_cell spy, auth on the None-root and zero-USD lanes, and a base-tree re-run confirming the unrelated spawn_budget failure is pre-existing), the mechanism/near-miss reading, and the one finding left for the director. The DH.673 caveat on this same chain — that the committed guard passed on pre-fix bytes — is now CLOSED by measurement, not by assertion.
<!-- THOUGHT:END -->
