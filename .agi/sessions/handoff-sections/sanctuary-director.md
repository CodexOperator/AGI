# sanctuary-director — L4 gen II slice (ROTATING at 0.44, cap 0.47)

**Successor: L4 gen III**, brief at `.agi/sessions/quorum/sanctuary-director.md` — replaced
wholesale, read THAT. This slice is the ledger.

| | |
|---|---|
| Seat | `.agi/worktrees/seat-sanctuary-director`, `seat/sanctuary-director@s2` @ `6b4614376`, pushed |
| Prime | **`agi-64 [61b9c9]` @235 = belam-S1-L4-II** — 🔴 address `agi-64`; the window name bounces. Three idle predecessors read nothing: @232, @230, and any idle row |
| Helper | `seat-sanctuary-helper-05 [3a4ed4]` — merged up and HOLDING, started nothing |
| season/s2 | **`b4481c9ba`** — both seats merged, prime-verified |
| Suite | **2315 passed, 1 skipped** · smoke 1897 / 1703 active / 194 deprecated · links 1877/0 · goals 157 byte-identical · guard silent |
| Key | **$7.87 of $15**, ~$0.04/round, $1.00 floor untouched |
| Live at rotation | **L4.45** (parent `a00-0b75cd81`, kid `a00-e3c5c921`) |

## Rounds this generation — seven closed, all merged and pushed

**L4.06** proved — the write-log records WHO, through the EXISTING `extra` hook, no second
logging path. Proved itself on a live write: my own review note appended
`"actor": "sanctuary-director"`. **L4.39** proved — `dispatch` exports `AGI_SEAT` at all
three sites with one precedence rule. **L4.05** proved — `links.py roles` prints the
COVERAGE GAP: 18 types, **1 declares `written_by`, 17 do not**. A violations-only report
would have printed "0 violations" and been true while 477 experiments sat unfalsifiable; the
owner then ruled L4.09 GO on exactly that number. **L4.42** proved — ONE resolver for
`replace_from`; an empty source now REFUSES instead of silently deleting the range.
**L4.37** both halves promoted, harvested by verification. **L4.40** proved — the refusal
names the TYPE and the admitted writers. **L4.43** at 65 — fail-closed `allowed_models`,
one choke point at `dispatch.py:1096` covering live, dry, agent record and `--seat`.

Plus: the owner's prayer-scope ruling into all three director briefs, `.gitignore:78` for the
repo-root `autoresearch.jsonl`, and the double merge-up.

## 🔴 What this generation got WRONG

**Three misses in L4.37, ONE shape — I checked what the work claimed about itself rather
than what it could break.** (1) Read `_legacy_fallback`'s docstring instead of its
`otherwise` branch. (2) Took a test's NAME for its coverage. (3) Ran the tests the round
ADDED and never `test_rotate.py` — a module-level `rotate.main` rebind then turned **22
tests red in the merged suite** while that file passed 81/81 alone. The prime found (1) and
(2) in bytes I had already promoted. **Run the tests a round could BREAK.**

**I moved a ruled time without telling the prime.** The ruling said 04:00Z; the owner said
L4.37 looked hung; I measured and harvested at 03:17Z. Measuring first was right, telling the
owner and not the prime was not.

**I asserted an absence I had not measured.** Told the prime L4.05 had "no data source". 214
nodes already carried `role:`. One grep would have shown it. The conclusion held; half the
evidence did not, and I corrected it in the node and to the prime before it propagated.

## 🔴 Next for gen III

Harvest **L4.45** (`ps -p` first, `status --porcelain` before believing it empty). Then
**L4.44** — the owner's `verification.py`, mvp-first per `goal:s29`, **held until L4.45 lands
because both touch `rotate.py`**. Then **L4.46**, scoped with item 3 closed — a good hand-off
to the helper, which is idle and ready.
