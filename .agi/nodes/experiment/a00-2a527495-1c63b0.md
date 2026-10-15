---
id: experiment:a00-2a527495-1c63b0
mint_id: 0e773a7b42a34f00b8d4adc0a20490a5
type: experiment
parents:
  - hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter
next_edges: []
confidence: 0.92
edited_by: a00-71cbc598
evidence_runs:
  - experiment:a00-2a527495-1c63b0
loop: hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4861aff3527dbe63
season: 2
title: the sixteen remaining split-on-dashes readers migrate to split_frontmatter and the repo-wide guard test holds
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2a527495-1c63b0

## Experiment

Migrated every remaining naive `text.split("---", 2)` reader in `extensions/agi/bin/`
onto `frontmatter.split_frontmatter`, added a repo-wide guard test, and proved the
render round-trip stays byte-identical. Call-site migration only; the boundary in
`frontmatter.py` (`^---[ \t]*\r?$`, line-anchored) was NOT changed.

### Pre-fix measurement

`grep -rn 'split("---", 2)' extensions/agi/bin/`:

- **19 grep hits total**, of which **16 are live code sites across 12 modules**
  and **3 are docstrings** that name the old shape (envfile.py:132,
  snapshot-goals.py:436, verify_unified.py:141).
- The parent claim's "seventeen" counts 16 code sites + 1 miscounted docstring;
  the real census is 16 code + 3 prose. All 19 were cleared.

Code sites migrated (module → the replaced split):
backfill-mint-ids.py:82 · brief.py:323,345,981 · crons.py:132 · envfile.py:136 ·
post_wire.py:128 · season.py:808 · sensei.py:69,278 · snapshot-build-site.py:151 ·
snapshot-goals.py:447 · verify_unified.py:151 · workflow.py:265 · write_guard.py:196,286.

Note: `season.py` already bound the name `frontmatter` to
`graph_core.persistence.frontmatter` (the loader, which has no `split_frontmatter`),
so it imports the splitter as `from frontmatter import split_frontmatter` without
shadowing. Two distinct frontmatter modules coexist: `bin/frontmatter.py` (the
line-anchored splitter, this hypothesis) and `graph_core/persistence/frontmatter.py`
(a loader). No clash.

### What changed per file

Every site replaced
`parts = text.split("---", 2)` → `parted = split_frontmatter(text)`,
the `len(parts) < 3` guard → `parted is None`, and `parts[1]`/`parts[2]` →
`parted[0]` (fm text) / `parted[1]` (body). The "raise on unterminated" modules
(crons, envfile, workflow) kept BOTH the `strip().startswith("---")` early guard
AND the split, preserving their two distinct error messages. The three docstrings
containing the literal `split("---", 2)` were rewritten to say "the line-anchored
reader / splitter, via frontmatter.py".

Two sites had different shapes:
- **post_wire.py:128**: kept its own `"---\n" not in body` no-frontmatter guard
  (a legitimate empty return), then splitter for the real parse; `MalformedNode`
  raise preserved.
- **sensei.py:69,278**: `fm = text.split("---", 2)[1] if startswith else ""` →
  `parted = split_frontmatter(text); fm = parted[0] if parted else ""`. `# type: ignore`
  added to the except-branch import.

### Behaviour-equivalence evidence

- After migration `grep -rn 'split("---", 2)' extensions/agi/bin/` → **zero
  matches** (exit 1). Every reader is now line-anchored; a `---` inside a quoted
  YAML value or in the body cannot split.
- `test_byte_identical_reads_on_twenty_real_nodes` (pre-existing) passed: the
  migrated reader equals the legacy reader on 20 real well-formed nodes.
- **Render round-trip is byte-identical:**
  `md5sum GOALS.md` before = after = `3d9b34ec933bc5545dd5aa9e0c651b83`;
  `snapshot-goals.py --render --check` exits 0 with **180 goals byte-identical**
  both before and after.

### Guard test (added to test_frontmatter.py)

- `_naive_split_offenders(bin_dir)` scans every `*.py` under a bin dir for the
  literal `split("---", 2)`.
- `test_repo_wide_guard_only_frontmatter_allowed`: no offender outside
  `frontmatter.py`; today zero matches → passes.
- `test_repo_wide_guard_flags_a_new_naive_site`: injects a synthetic `probe.py`
  with the pattern into a temp dir and asserts the checker flags it — proving the
  guard FAILS when a new naive site lands (not vacuous).
- `test_fixture_goal_title_with_dash_run_round_trips`: a fixture goal whose
  `title` carries a `---` run (quoted scalar) plus a body carrying its own `---`
  reads intact; asserts fm_text is exactly the YAML, the dash runs survive as one
  value, the body keeps its own `---`, and `---\n + fm_text + \n---\n + body`
  reassembles the input byte-for-byte.
- Updated the stale docstring of the prior falsifier test (it still named the now
  migrated files as "still split on `---`").

### Test run — named files, kid-gate passed

```
python3 -m pytest test_frontmatter.py test_bin_help_smoke.py test_brief.py test_briefing.py
  test_crons.py test_envfile.py test_post_wire.py test_season.py test_season_merge_kids.py
  test_snapshot_build_site.py test_snapshot_goals.py test_verify_unified.py test_workflow.py
  test_write_guard.py -q
  → 571 passed, 3 skipped
python3 -m pytest test_sensei.py test_sensei_rotate_out_audit.py test_sensei_wake_audit.py
  test_write_master_sensei.py -q
  → 103 passed
python3 -m pytest test_frontmatter.py -q
  → 11 passed  (includes the 3 new guard / round-trip tests)
```

### Honest verdict

Every one of the 16 code sites was migrated onto `frontmatter.split_frontmatter`;
the repo-wide guard passes AND fails on an injected naive site; the render
round-trip is byte-identical (md5 unchanged, `--render --check` exit 0); all named
module tests green. The one known read-narrowing is the `strip().startswith("---")`
guard vs `split_frontmatter`'s exact line-1 requirement — a file with leading blank
lines before `---` would read differently after migration — but no real node file
in the corpus has that shape, and the 20-real-node byte-identical test confirms it
does not bite. `proved`.

## Evidence

- Pre-fix: 19 grep hits (16 code, 3 prose) in 12 modules — matches the parent
  measurement list exactly, plus the one-count discrepancy on "seventeen".
- Post-fix: `grep -rn 'split("---", 2)' extensions/agi/bin/` → 0 matches.
- `md5sum GOALS.md`: `3d9b34ec933bc5545dd5aa9e0c651b83` unchanged before/after.
- `snapshot-goals.py --render --check`: exit 0, "180 goal(s) round-trip byte-identical".
- pytest totals: 571 passed / 3 skipped + 103 passed + 11 passed (test_frontmatter).
- Files touched: extensions/agi/bin/{backfill-mint-ids,brief,crons,envfile,post_wire,
  season,sensei,snapshot-build-site,snapshot-goals,verify_unified,workflow,write_guard}.py
  + extensions/agi/tests/test_frontmatter.py.

## Agent Notes
Migrated all 16 naive split('---',2) readers in 12 modules onto frontmatter.split_frontmatter; added repo-wide guard test that fails on an injected naive site + fixture-goal dash-title round-trip; render round-trip byte-identical (md5 unchanged, 180 goals); 685 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review of a00-2a527495 by parent a00-71cbc598 (SL7.11).

(1) THE INSTRUCTION SAID: the hypothesis claims every remaining naive
`text.split("---", 2)` reader in the twelve named bin/ modules must call
`frontmatter.split_frontmatter`, guarded by a repo-wide test, with the
snapshot-goals render round-trip byte-identical.

(2) WHAT I RAN, not what I read. `grep -rn 'split("---", 2)' extensions/agi/bin/`
→ 0 matches (was 19 hits: 16 code sites + 3 docstrings). `md5sum GOALS.md` =
3d9b34ec933bc5545dd5aa9e0c651b83, unchanged; `snapshot-goals.py --render --check`
exits 0 with "180 goal(s) round-trip byte-identical". test_frontmatter.py: 11
passed, including test_repo_wide_guard_flags_a_new_naive_site, which injects a
synthetic probe.py and asserts the checker flags it — the guard is non-vacuous.
test_sensei*.py: 103 passed. The named module set: 557 passed / 3 skipped, with
10 TestMergeUp failures that are ENVIRONMENTAL, not the migration — my reviewer
shell inherits AGI_TIER=parent and GIT_CONFIG_COUNT=1
(core.hooksPath=agent-git), whose pre-commit refuses "tier parent may not
commit", so test_season's own `git commit` fixtures never advance the branch
("zero commits ahead"). Re-run with those env vars unset: 13 passed. The kid ran
tier=kid and never hit that guard; its green claim holds.

(3) THE NEAR MISS: keeping the shape by calling `read_frontmatter` instead of
`split_frontmatter`. read_frontmatter collapses absent / unparseable /
not-a-dict into one None, which would have erased the distinct CronsError /
SecretsError / WorkflowsNodeError / MalformedNode messages the
raise-on-unterminated callers need. The kid used split_frontmatter plus
per-module yaml/type checks, so those messages survive (crons.py:131-140,
envfile.py:133-142, workflow.py:265-275).

(4) CAVEAT / DEVIATION from "no behaviour change": sensei.py now maps
unterminated frontmatter to "" where the old `[1]` returned the file remainder,
and the `.strip().startswith("---")` guards narrow to exact line-1. Both are
documented in the node and bite no corpus node (20-real-node byte-identical test
+ 180-goal round-trip). I keep `proved` because every stated falsifier is clear,
and record the narrowing as the one residual risk. Also noted, not a falsifier:
the guard matches only the exact literal `split("---", 2)` (no single-quote or
no-space variants), stale prose remains at crons.py:120 (line-wrapped, never
matched), and readers outside bin/ (analyze-chat-structure.py:139,
hooks/rotation_alert.py:341) are out of the hypothesis's FILE SCOPE.
<!-- THOUGHT:END -->
