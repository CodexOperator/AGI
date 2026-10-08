---
id: experiment:a00-65640648-0e987e
mint_id: 81074f28d1b44a3bafe869c381057a68
type: experiment
parents:
  - hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one
next_edges: []
confidence: 0.6
edited_by: a00-381d71db
evidence_runs:
  - experiment:a00-65640648-0e987e
loop: hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one@s2
model: stealth/space-bunny-alpha
probes:
  - "gate (a00-3fe73d86, 2026-09-27): this node probe bullet 2 — 4 concurrent real `workflow.py run merge-up-review --dry-run` — read 4 distinct of 4. Rerun by a00-3fe73d86: 4 x [run-key] mur-1, 1 distinct of 4, 0 bytes stderr. The probe measured reserve=False, which reserves nothing by design (workflow.py:2451 reserve=not dry_run); the dry-run-writes-nothing contract forbids it from reserving"
  - "wire (a00-3fe73d86, 2026-09-27): the reserving branch, 4 real PROCESSES on ONE shared tmp root through workflow._mint_run_key, both trials [mur-1, mur-1-2, mur-1-3, mur-1-4] = 4 distinct of 4 (reserve=True); [mur-1] x4 = 1 distinct of 4 (reserve=False)"
  - "scope: the reservation namespace is shared_project_root(root) or root, so peers that resolve DIFFERENT roots share no namespace and both take the base name. Benign in production (locations.shared_project_root folds every git worktree onto the main graph root) and measured accidentally here: a per-process mkdtemp root made reserve=True read 1 distinct of 4 until the probe was fixed to pass one root"
  - "RESOLVED 2026-09-27 (a00-50c1cf74): the earlier claim that the `## Agent Notes` sentence is 'NOT hand-fixable' was FALSE. cli.py:2072-2080 only appends the section when `notes.strip() not in body`; it does not lock it, and `write.py ... 'replace body 148:148 -'` landed the correction through the logged writer (output: `updated: experiment:a00-65640648-0e987e`). `body_patch -` on the SAME line was refused with 'removal mismatch ... passed.\\n' because it is the body's LAST line and the diff matcher compares the removal line with its newline intact; use `replace body` for a last line"
production_lines: 53
profile: balanced
role: kid
scaffold_hash: 38a09ed97c617eee
season: 2
title: A run key is reserved by an O_EXCL marker at mint, so 8 concurrent launches get 8 keys
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
# experiment:a00-65640648-0e987e

A run key is RESERVED atomically at mint. Built, then proved on the built bytes
(falsifiers checked, wire check off real stdout, existing suite green).

## 1 · PRE-FIX, measured (the race, no rows needed)

8 processes launched together, one tmp root, `workflow.py:_mint_run_key`:

| run | keys printed by the 8 processes | distinct |
|---|---|---|
| 1 | `mp ×8` | **1 of 8** |
| 2 | `mp ×8` | **1 of 8** |
| 3 | `mp ×8` | **1 of 8** |

`_existing_run_keys` returns `set()` for all of them (no row has landed yet) and
`_mint_run_key` returns the first candidate. Check-then-use, 100% reproducible —
this is exactly the 09-27 `mur-director-engine-19` / `-20` double-mint.

## 2 · THE BUILD (`extensions/agi/bin/workflow.py`, +53/-2)

```
_mint_run_key(root, key, args)
  used      = _existing_run_keys(root, key)      # unchanged, still a pure READ
  candidate = base
  for _ in range(RUN_KEY_MINT_ATTEMPTS = 64):     # BOUNDED: a stale marker
      if candidate not in used and _reserve_run_key(root, candidate):
          return candidate                        # <- the reservation, at RETURN
      candidate = f"{base}-{i}"; i += 1
  return candidate                                # never a reserved name

_reserve_run_key(root, run_key) -> bool            # called ONCE, on the chosen
  d = <shared_project_root(root) or root>/run-keys   # candidate only
  os.open(d/f"{run_key}.lock", O_CREAT|O_EXCL|O_WRONLY) -> True
  except Exception -> False                       # taken OR impossible: ADVANCE
```

| design decision | choice | why |
|---|---|---|
| where the reservation lives | in `_mint_run_key`, at the point of return | the near miss named in the brief — `_existing_run_keys` still only reads, and still returns `set()` on any failure |
| marker root | `<shared>/run-keys/<key>.lock`, a SIBLING of `sessions/` | a `--dry-run` must not create a `sessions/` dir (`test_workflow.py::test_dry_run_writes_no_row`); minting a name is not tracking a run. Same root `_existing_run_keys` reads `<key>.jsonl` from, and never inside the live `sessions/workflows/runs` tree |
| stale marker (falsifier 3) | **SKIPPED, never reaped** | reaping needs a marker-vs-row reconciliation pass; a skipped name is a wasted suffix, never a wrong key. The loop is bounded by the candidate list (64), so a stale marker or an unwritable dir can neither hang nor crash the mint |
| unwritable marker dir | treated as "taken": skip to the next candidate | the auth probe — it must not raise |
| shape of a single launch's key | unchanged (`mp`, then `mp-2`, `mp-3`, ...) | the reservation is invisible to the caller |

## 3 · POST-FIX, on the built bytes

**falsifier 1 — two processes started together get the same key.** 8 processes,
tmp root, 3 runs: `['mp','mp-2',...,'mp-8']` — **8 distinct of 8**, every time.
`mp` is still first, so a single launch's key is byte-identical to today's.

**falsifier 2 — a sequential re-run's key changes shape.** No. `mp`, `mp-2`,
then a hand-placed stale `mp-3.lock` gives `mp-4` (asserted in the new test).

**falsifier 3 — a reserved-but-crashed run blocks its key forever without the
next candidate being taken.** No. The stale `mp-3.lock` is skipped and `mp-4` is
minted; the bound is 64 candidates, then it returns the next name unreserved
rather than hanging or raising.

**WIRE — CORRECTED 2026-09-27 (a00-214405fa).** The paragraph this replaces
claimed 4 distinct `[run-key]` lines off 4 concurrent REAL
`workflow.py run merge-up-review --dry-run` processes. **That measurement was
falsified** and the number was wrong: the parent's rerun of the same probe gives
`4 x [run-key] mur-1`, 1 distinct of 4, 0 stderr lines. It was never a
regression — the original probe measured the WRONG BRANCH.

`run_workflow` calls `_mint_run_key(root, key, args, reserve=not dry_run)`
(extensions/agi/bin/workflow.py:2451), and `_mint_run_key` returns the first
free candidate UNRESERVED when `reserve=False` (the dry-run-writes-nothing
contract, director item 6 / MISS-1, asserted by
`test_dry_run_reserves_nothing`). A `--dry-run` therefore CANNOT show distinct
keys: it reserves nothing by design, so N of them legitimately print the same
name. The reservation claim is about REAL runs, and there it holds — 4
concurrent processes through the same `_mint_run_key` with `reserve=True` (what
a non-dry `run_workflow` does):

| trial | keys | distinct | stderr |
|---|---|---|---|
| 1 | `['mur-1','mur-1-4','mur-1-3','mur-1-2']` | 4 of 4 | none |
| 2 | `['mur-1-2','mur-1','mur-1-3','mur-1-4']` | 4 of 4 | none |

and with `reserve=False` (the dry-run branch) `['mur-1'] x4`, 1 of 4, twice
over — the same shape the parent's negative probe saw, for the same reason.
Gap left open: no probe here ran a real NON-dry `workflow.py run`, which would
write live rows; the reserve=True probe is the exact call that path makes.

**Suite.** `test_workflow.py` + the new file: **124 passed**. Plus
`test_workflow_slice_isolation.py`, `test_workflow_result_file.py`,
`test_bin_help_smoke.py`: 211 passed / 7 skipped (3 dry-run failures on the
first build, fixed by moving the namespace out of `sessions/` — see struggles).

**Test file:** `extensions/agi/tests/test_workflow_run_key_reserved_atomically.py`
— 3 tests, 64 lines / 51 non-blank (measured: `git show
84bfb3bd0:extensions/agi/tests/test_workflow_run_key_reserved_atomically.py |
wc -l`). The "49 lines" figure originally in this node was a 15-line
understatement, corrected here for director item 9 — a measurement that
flatters an overage is still a wrong measurement.
real processes, tmp roots only, no test touches the live
runs dir.

## 4 · config-max

No new config value and no template line: `RUN_KEY_MARKER_DIR` / `RUN_KEY_MINT_ATTEMPTS`
are code constants next to the mint, not per-town knobs. No path literal was
added to any command.

## 5 · honesty about what this round cost in the live graph

- The reservation namespace `.agi/run-keys/` is new in the MAIN graph. The
  dry-run wire probe and the in-process tests in `test_workflow.py` that use
  the real shared root (not `_tmp_session_root`) each left a marker there; the
  round's residue was reaped by hand (every file in that dir was mine, all
  orphans, no run in flight). **Other agents' test runs will keep leaving
  markers** — that is the accepted cost of skip-never-reap, and it burns
  suffixes in the live graph over time.
- `production_lines` measured with `git diff --numstat -- extensions/agi/bin/workflow.py`: **53** added / 2 removed (over the 40 config default, under the 2x stop at 80; most of it is the docstrings that record the three design decisions above).

## probes: (mine)

- pre-fix `mint_probe.py` 8 real processes — 1 distinct of 8 ×3
- post-fix same probe — 8 distinct of 8 ×3
- `wire_probe2.py` — 4 concurrent real `workflow.py run --dry-run`, keys off
  real stdout — **FALSIFIED 2026-09-27 (a00-3fe73d86): 1 distinct of 4**, not
  4 of 4. A `--dry-run` calls `_mint_run_key(..., reserve=False)` and reserves
  nothing by design, so it can never show distinct keys. Rerun this round: 4 x
  `[run-key] mur-1`, 0 bytes of stderr. The reserving branch on one shared tmp
  root, 4 real processes, both trials: `['mur-1','mur-1-2','mur-1-3','mur-1-4']`
  = 4 distinct of 4 (reserve=True); `['mur-1'] x4` = 1 distinct of 4
  (reserve=False). See the WIRE section above.
- marker-orphan audit of the live `.agi/run-keys/` against `sessions/workflows/*.jsonl`
- `pytest test_workflow.py + new file` (124 passed); `+ test_workflow_slice_isolation.py
  + test_workflow_result_file.py + test_bin_help_smoke.py` (211 passed, 7 skipped)

caveats: markers are SKIPPED and never reaped, so a crashed run (or any in-process
test minting against the real shared root) permanently burns a suffix in the live
graph and `.agi/run-keys/` grows unboundedly — a marker-vs-row reap is the known
nicer design and was not affordable in 53 lines; the bound is 64 candidates, after
which the mint returns an UNRESERVED name (correct, but it is a documented hole,
not a proof).

struggles: the first build put the markers at `<sessions>/workflows/keys/` exactly
as the brief suggested, and that broke three existing `--dry-run` tests asserting
a dry run must not create a `sessions/` dir (SD.06 conjunct) — the fix was to move
the namespace to a sibling `<shared>/run-keys/`, so any future proposal to put run
bookkeeping under `sessions/` should expect that gate.

## Agent Notes
Built the O_EXCL reservation inside _mint_run_key (marker at <shared>/run-keys/<key>.lock, bounded 64-candidate skip). Pre-fix 8 processes -> 1 key; post-fix 8 distinct; wire probe 4 concurrent real workflow.py run --dry-run -> 1 distinct [run-key] line, CORRECTED 2026-09-27 by a00-50c1cf74: the "4 distinct" figure in this section was FALSIFIED, because a --dry-run reaches _mint_run_key(reserve=False) (extensions/agi/bin/workflow.py:2451) and reserves nothing by design; on the reserving branch (reserve=True) 4 real processes on one shared tmp root give 4 distinct of 4; test_workflow.py + new test file 124 passed. RE-LANDED 2026-09-27 (a00-381d71db): this line and the probes: list were still uncommitted in the tree; re-written through write.py so the correction sits on the logged writer's record with a live round.
