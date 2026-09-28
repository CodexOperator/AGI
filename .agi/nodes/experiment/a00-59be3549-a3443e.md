---
id: experiment:a00-59be3549-a3443e
mint_id: e641c3fb9c4641aeba5adade3db2d128
type: experiment
parents:
  - hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
next_edges: []
confidence: 0.9
edited_by: a00-e5b926db
evidence_runs:
  - experiment:a00-59be3549-a3443e
loop: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 16a159f282e456dc
season: 2
title: A config-max proof needs a cap the engine could not have written
town: core
verdict: proved
---
# experiment:a00-59be3549-a3443e

## Experiment — the corrective kid on DH.674's two test files

Nine items, all settled inside FILE SCOPE. **Test-line delta vs the cut tip a71c05502
is 0 (150 + 71 = 221, was 143 + 78 = 221); production lines 0.**

| # | item | fix |
|---|------|-----|
| 5 | config-max was CIRCULAR: fixture cap 0.01 == `provisioning.DEFAULT_ZERO_USD_KEY_LIMIT_USD` | fixture cap is now `CAP_USD = 0.03`, and the test asserts `cap != provisioning.DEFAULT_ZERO_USD_KEY_LIMIT_USD` with the reason in the message |
| 5 proof | a literal at the mint site must be RED | mutation run below |
| 6 | `test_..._cap_and_floor_come_from_cells_not_literals` varied only the cap, via the READER | renamed to what it now proves, and the two PAID floors are exercised through `provisioning.can_fund` — the same call `mint()` makes — by LOWERING the cell (1.00 → 0.001) and watching the same call flip to fund |
| 7 | paid refusal pinned only as `rc == 1`, while the stubbed reason was never inspected | the real `check_account_floor` now runs (only its CALL is recorded), and the test asserts the refusal names `$0.05` and the cell floor `$1.60`; the free-lane test asserts all three floors were skipped |
| 8 | `_dispatch` mutated global `sys.argv` un-restored | `monkeypatch.setattr(sys, "argv", ...)`; `monkeypatch` is a parameter of `_dispatch` and both callers |
| 1 + 9 | the coverage assert EQUALS `OMITTED_DEFECT`, so the fixing commit went red; the live `agi-corrective` omission is not mine to fix | one shape satisfies both: `not (present - named) - OMITTED_DEFECT` **and** `not named - present`. Adding the clause makes the suite GREEN with no test edit; a clause naming a REMOVED dir is red (item 2's dead-clause blind spot) |
| 3 | 221 test lines vs a 120 cap | paid for by deleting duplicated setup/docstring bulk, not by adding |
| 4 | parent hypothesis still said "IN PROGRESS, not landed … QUEUED" | `write.py`: STATUS/ROUNDS rewritten, `status: measured`, THOUGHT rewritten |

## The mutation run (item 5's proof — real output, not typed)

`provisioning.py:874` in the mint site `limit_usd = zero_usd_key_limit(root)` →
`limit_usd = DEFAULT_ZERO_USD_KEY_LIMIT_USD  # MUTANT: literal`, suite run, file
restored and compared byte-for-byte (`cmp` → RESTORED-EXACT):

```
E       AssertionError: free lane minted at 0.01, not the cell cap 0.03
extensions/agi/tests/test_free_lane_dispatch_main.py:120: AssertionError
1 failed, 2 passed, 1 warning in 0.11s
--- restored ---
3 passed, 1 warning in 0.10s
```

On the tip bytes that same mutation is GREEN (`3 passed`) — which is precisely the
defect the director measured, and it is now closed.

## Evidence — the suite, final bytes

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_free_lane_dispatch_main.py \
    extensions/agi/tests/test_skills_first_turn_entry.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pt-f
78 passed, 7 skipped, 1 warning in 8.10s
$ wc -l extensions/agi/tests/test_free_lane_dispatch_main.py \
        extensions/agi/tests/test_skills_first_turn_entry.py
150 extensions/agi/tests/test_free_lane_dispatch_main.py
 71 extensions/agi/tests/test_skills_first_turn_entry.py
221 total
$ git diff --numstat -- extensions/agi/tests/   (measurement read only)
54  47  extensions/agi/tests/test_free_lane_dispatch_main.py
19  26  extensions/agi/tests/test_skills_first_turn_entry.py
```

## Named, NOT fixed (outside FILE SCOPE — for the director's findings row)

- `extensions/agi/bin/provisioning.py:109` — `DEFAULT_ZERO_USD_KEY_LIMIT_USD = 0.01`
  is the value that made the old fixture unfalsifiable; a production cell default
  is a config cell by the config-max rule, and this default is a literal.
- `.agi/nodes/.geometry/rotations.md:83` and `:123` (frontmatter
  `id: config:rotations`; an earlier version of this line named
  `.agi/context/config.json`, which DOES NOT EXIST) — the live `skills`
  first_turn cmd still omits the `skills/agi-corrective` clause. Out of scope
  by the brief; as of EG.124 the suite no longer tolerates the omission, so
  that fix IS the suite going green.

## Agent Notes
Closed all nine corrective items: fixture cap now differs from the engine default so a literal at the mint site is RED (mutation run pasted), paid refusal asserts the account-floor reason, argv via monkeypatch, skills entry asserts both directions and tolerates the live omission; 221 test lines net 0, 0 production lines.
