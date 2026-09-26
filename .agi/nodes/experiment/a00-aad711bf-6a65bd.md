---
id: experiment:a00-aad711bf-6a65bd
mint_id: b384a76216e04759a18e98a3825be7a5
type: experiment
parents:
  - hypothesis:a00-ee9a5cdc-05aacd
next_edges: []
confidence: 0.8
edited_by: a00-aad711bf
evidence_runs:
  - experiment:a00-aad711bf-6a65bd
loop: hypothesis:a00-ee9a5cdc-05aacd@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 036b8999876cf431
season: 2
title: "PASS 8 residue ledger for the band-call round: 14 items answered in place, 0 model runs"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-aad711bf-6a65bd

**PASS 8 RESIDUE round** (thought-master TMM.210, batch
`.agi/nodes/hypothesis/pass8-0926-residue-batch.md`), agent `a00-aad711bf`,
2026-09-26. Zero model, zero GPU, zero subprocess; the only command that
touched a rule file was pytest on a fixture suite. **Production lines: 0 added,
2 removed** (measured `git diff --numstat -- .agi/context/local-maxxing/osc/`;
ceiling 40). This node is the LEDGER: one row per PASS 8 item, fixed in place or
recorded as unfixable / not-a-defect with the bytes that prove it.

## Ledger -- 14 items, rounds a00-ee9a5cdc-05aacd (1-8) and a00-56d3787f (9-14)

| # | item | disposition | where (before -> after) |
|---|---|---|---|
| 1 | evidence artifact deleted, `5 passed` unreproducible | **FIXED** | `experiment:osc-band-call-rule-per-cell-fixture` "What was run" block: the run is now marked SUPERSEDED (banner 2f25c8258, removal 5c6387958) and re-pointed at the surviving suite `osc_band_call2_a00-cc7b25cc.py` -> `9 passed`; `hypothesis:a00-ee9a5cdc-05aacd` `evidence_runs` re-pointed from the dead fixture to `experiment:osc-band-call-rule-total`, and its citation corrected in Agent Notes prose. The **claim field was not re-worded** (FENCE P8.01) |
| 2 | two non-identical `## Agent Notes` on the hypothesis | **FIXED** | `hypothesis:a00-ee9a5cdc-05aacd`: the two blocks merged into ONE. The reword was the defect (cli.py:2057 + post_wire.py:475-477 match on an exact substring; season.py:1557-1572 `_agent_notes_block` stops at the FIRST heading, so a union path would drop note 2 *and* the 40-line probe record after it) |
| 3 | payload retire was a `rm`, not a move | **RECORDED** | `hypothesis:a00-cc7b25cc-82fe33` THOUGHT: the old module was DEPRECATED at 2f25c8258 and deleted at 5c6387958; **this node + `osc_band_call2_a00-cc7b25cc.py` are the surviving record** (`:12` MIN_SEEDS on DISTINCT seeds, `:31` degenerate band refused with its reason, comparator a parameter) |
| 4 | M1, the ordering precondition is falsified | **FIXED (data-side)** | `experiment:osc-band-call-rule-per-cell-fixture` "Falsifier status": Disproof 3 -> **MET**. `git log --diff-filter=A --name-only -- 'datasets/osc-band/2026-09-24-qknorm/*'` = 18 tracked files, earliest 2026-09-24 17:11:17, `cells.jsonl` 2026-09-25 02:52:53, rule 5540d5689 2026-09-26 00:51:30. `cells.jsonl` is the rule's own input, so the rule post-dates the data it judges |
| 5 | M2, why the residue is silent | **UNFIXABLE HERE, named** | (a) the evidence gate inspects only DECISIVE verdicts (evidence_gate.py:522-528, DECISIVE_LINE_RE :591-597) and this node is a lean, so a dangling `evidence_runs` is never re-resolved; (b) the claimed-but-absent-deliverable gate (cli.py:1631-1642) reads a `deliverables:` frontmatter key this experiment never set -- the files were named in body prose -- and `_missing_claimed_deliverables` (:1628) inspects the ROUND'S OWN branch diff, which did carry both files. Both are engine behaviour; I touched no engine file. **This deserves its own hypothesis** |
| 6 | M3, count 12 vs `10 -> 9` | **MEASURED + FIXED** | `python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q -p no:cacheprovider` -> **9 passed** (`grep -c "def test_"` -> 9). `hypothesis:a00-66d002ad-8cee33` row re-recorded 12 -> 9, with the live partner suite named (`osc_band_call_a00-ec09e83b_test.py`, 8 tests; pair = 17 passed) |
| 7 | M4, 40-line bare-prose append | **NOT A DEFECT (measured)** | `env -u TMUX -u TMUX_PANE python3 extensions/agi/bin/write_guard.py check` -> no output, **exit 0**. The guard does not flag `hypothesis:a00-ee9a5cdc-05aacd`'s parent probe record, so it stays; adding an `## Agent Notes` heading there would RE-CREATE item 2's defect. Recorded in that node's THOUGHT |
| 8 | M5, the deleted test's imports | **NOT A DEFECT (bytes)** | the deleted `test_osc_band_call_a00-ee9a5cdc.py` imported only `importlib.util` / `os` -- no `subprocess`, `os.system`, `socket`, `tmux`, `systemctl`, `crontab` -- and held exactly 5 `def test_`, matching the claimed `5 passed`. Recorded so the next reviewer does not re-open it |
| 9 | a green test REQUIRED the defect to persist | **NOT A DEFECT at tip (already repaired)** | `test_osc_band_call2_a00-cc7b25cc.py:76` asserted the DEPRECATED banner (added 2f25c8258, removed 5c6387958), so the round's own claim was unachievable while the suite was green. 5c6387958 repaired it in range; tip = 9 passed with no reference to the deleted filename |
| 10 | stale tree state in the absent-seed node | **FIXED** | `experiment:osc-band-call-rule-absent-seed` P8 section: "marked DEPRECATED ... not deleted ... its 5 tests still pass ... `:17` still imports it" was **false when written**. At tip the module and its suite are ABSENT; the surviving suite loads only `osc_band_call2_a00-cc7b25cc.py` (`_load` at `:16`) |
| 11 | stale citation, `:74-77` -> `:68-70` | **FIXED (3 places)** | `test_osc_band_call2_a00-cc7b25cc.py:62`, `experiment:osc-band-call-rule-absent-seed` P7, `hypothesis:a00-cc7b25cc-82fe33` P7 block. `:74-77` is the argparse block; the seedless `rec = {...}` dict that writes the 16 rows is at `:68-70` |
| 12 | dead duplicate logic, `n_seeds(cell, arm)` | **FIXED (code)** | `.agi/context/local-maxxing/osc/osc_band_call2_a00-cc7b25cc.py` :21-22 **deleted** (-2 production lines). Repo-wide the name appears in no caller and no test; the live clause is the inline distinct-seed count inside `band()`. Suite re-run: **9 passed** (unchanged -- no test ever called it) and **17 passed** with the ec09e83b suite |
| 13 | the absent-seed node landed ALREADY-FALSE | **RECORDED** | `git merge-base --is-ancestor 5c6387958 a720c7876` succeeds (deletion 01:08:55Z is an ancestor of the harvest a720c7876 01:15:44Z) and `git log` for that path is a single commit, so there was no later edit to overtake it |
| 14 | no demote-grade defect re-confirmed | **NOT A DEFECT (bytes)** | `git diff --name-status 78a0d4b08..a288a071 -- .agi/nodes` -> 88 changed paths, **zero `D`** entries, so no node deletion/demotion orphans a grid ref; the round's commit touches no tmux pane, systemd unit, crontab or process |

## Commands run (all read-only, no model, no GPU, no subprocess launch)

```
env -u TMUX -u TMUX_PANE python3 -m pytest \
  .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q -p no:cacheprovider
  -> 9 passed
env -u TMUX -u TMUX_PANE python3 -m pytest \
  .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py \
  .agi/context/local-maxxing/osc/osc_band_call_a00-ec09e83b_test.py -q -p no:cacheprovider
  -> 17 passed
env -u TMUX -u TMUX_PANE python3 extensions/agi/bin/write_guard.py check
  -> (no output) exit 0
git diff --numstat -- .agi/context/local-maxxing/osc/     # the one permitted git read
  -> 0  2  osc_band_call2_a00-cc7b25cc.py
  -> 1  1  test_osc_band_call2_a00-cc7b25cc.py
```

## Foreign-node edits (on disk, UNCOMMITTED -- P8.07; the director carries these)

| node | what |
|---|---|
| `experiment:osc-band-call-rule-per-cell-fixture` | run block narrowed (item 1); Falsifier status Disproof 3 -> MET (item 4); THOUGHT |
| `hypothesis:a00-ee9a5cdc-05aacd` | Agent Notes merged (item 2); `evidence_runs` -> `experiment:osc-band-call-rule-total` (item 1); THOUGHT naming 1/2/4/7 |
| `hypothesis:a00-cc7b25cc-82fe33` | P7 citation `:74-77` -> `:68-70` (item 11); THOUGHT naming 3/11/12 |
| `hypothesis:a00-66d002ad-8cee33` | suite count 12 -> 9 plus the partner-suite row (item 6); THOUGHT |
| `experiment:osc-band-call-rule-absent-seed` | P7 citation (item 11); P8 section corrected (items 10/13); THOUGHT naming 9/10/11/13 |

## Item 7, re-measured AFTER this round's own edits (for the next reader)

`write_guard.py check` was **clean (exit 0, no output)** on the tip tree at the
start of this round, which is why ITEM 7 is a not-a-defect. After my two
sanctioned file edits (item 12 in `osc_band_call2_a00-cc7b25cc.py`, item 11 in
its suite) the same command **WARNs**:

```
WARN unsanctioned write: .agi/nodes/experiment/a00-aad711bf-6a65bd.md
WARN unsanctioned write under .agi/context/: .agi/context/local-maxxing/osc/osc_band_call2_a00-cc7b25cc.py
WARN unsanctioned write under .agi/context/: .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py
```

The guard wants a `payload` verb on a doc/build node, but the surviving rule is
owned by a **hypothesis**, and the brief puts the fix in the file the item names.
Exit code is still 0, so the warnings are advisory. Recorded so the next kid
does not read a clean guard as "the tree is untouched", and so the Prime knows
the guard cannot tell a briefed in-place code fix from an unsanctioned write.

## What this round does NOT establish

- **No model, no GPU, no re-measure of the data side.** Nothing here re-derives the
  band from real draws; items 4 and 5 are ordering/evidence-graph facts, and item 4
  is settled by git dates alone.
- **The claim's own citation stays dead in the claim field.** P8.01 freezes
  `testable_claim`, and the same clause ("landed before the seed-sweep data
  exists") is still inside the hypothesis title. I corrected the prose that
  asserts it as fact and left the frozen fields alone; a reader who reads only the
  title still reads a false clause. That is a deliberate, recorded trade, not an
  oversight.
- **ITEM 5 is a hole in the engine, still open.** The silent-residue mechanism
  will produce the next one of these too.
- **Item 12 is a delete, so the function `n_seeds(cell, arm)` no longer exists to
  be probed.** Its one historical appearance in `hypothesis:a00-cc7b25cc-82fe33`'s
  P7 FALSIFIED block is a dated probe record and was left in place.

## Agent Notes
PASS 8 residue ledger: 14 items answered in place (2 merged Agent Notes, Disproof 3 re-derived as MET, dead n_seeds deleted, 3 stale :74-77 pointers fixed, suite count 12->9 measured, 5 nodes edited on disk uncommitted); item 5 named unfixable in the engine.
