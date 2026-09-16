---
id: experiment:a00-a467a5c2-a935a8
mint_id: 2b7ebb06b1f7402593506fe557eca725
type: experiment
parents:
  - hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote
next_edges: []
confidence: 0.85
edited_by: a00-ba912100
evidence_runs:
  - experiment:a00-a467a5c2-a935a8
loop: hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b03cdafcb412df68
season: 2
title: SL7.134 audit-preserve + STARTED refusal + floors from config + commit-by-path + one window shape
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a467a5c2-a935a8

## Experiment — SL7.134 built the parent's (a)-(f) residue

Target: hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote — a g15 BUILD ORDER, not a measurement. Pre-fix state measured by reading the code (`_write_rotation_record`/`_write_rotate_self_started` rebuild the dict from arguments and re-merge a FIXED key list; `audit` is outside it). The claim was then IMPLEMENTED and proven on the built bytes.

### what moved

**rotate.py** — preserve list ONLY
- NEW `_preserve_audit(rec, existing_path)` :4542 — mechanism (A), the same shape as `_preserve_swept_latches`/`_preserve_closeout`: a fresh `audit` THIS run always wins, else the on-disk block is merged back. Best-effort, never raises.
- called from `_write_rotation_record` :4596 (the in-place OUTCOME rewrite) and `_write_rotate_self_started` :4695 (the progress rewrite). This is the (a) rotate.py side.

**sensei.py**
- (a) verb side: `STARTED_REFUSAL = "record still STARTED; audit after the outcome"` :1524; `write_audit_into_record` :1580 raises `AuditRefusal` :1615 BEFORE any write when `rec["result"] == "started"`; `cmd_wake_audit` :1754 and `cmd_rotate_out_audit` :2159 catch it, print `ERR: <the string>` on stderr and return 3.
- (b) `AUDIT_FLOOR` (:1487) and `AUDIT_SIDES` (:1489) DELETED. `_audit_floors(fm)` :1499 reads `floor_wake`/`floor_out` off the config:rotations frontmatter that `_read_rotations` already hands both verbs; `FALLBACK_AUDIT_FLOOR` :1496 is the ONLY fallback. `audit_payload(..., floor=)` :1539 writes the CELL value into the record; wake carries it on `counts["_floor"]` :1441, out on `window["floor"]` :2117.
- (c) `_commit_audit_record` :1618 — ONE `git commit -q -o -m "audit record: <seat> <side> <stamp> — <green/FINDING line>" -- <record>`, never `-A`, never bundled, never a grid commit. Refuses BY NAME (no commit) when MERGE_HEAD is present or when `git ls-files --error-unmatch` fails; SKIPPED on a gitless root. Called from `finish_audit` :1685 immediately after the write.
- (d) `audit_window_point(call_index=None, line=None, ts=None)` :1527 — ONE dict shape, all three named keys present-or-null, for both bounds on both sides: wake :1438-1439, out :2159.
- (e) `write_audit_into_record` refuses by name when `json.dumps(json.loads(raw), indent=2) + "\n" != raw`.

**tests**
- test_sensei_audit_record_writeback.py: window assertions moved to the ONE shape; the soft `len` assertion (:197) made EXACT (`len(second) == len(first)`); `test_floors_...` now reads the config cell (and asserts a CHANGED cell moves the recorded floor); the live-corpus test's docstring corrected to say it is the ONE conjunct that reads the real corpus; 11 NEW tests.
- test_sensei_audit_record_window.py: three records canonicalised (`json.dumps(r, indent=2) + "\n"`). They claim to copy the LIVE record shapes and live records are canonical, so the compact form was the fixture's defect, surfaced by (e).

### which item each hunk satisfies
- (a) `_preserve_audit` + both call sites + `STARTED_REFUSAL`/`AuditRefusal` + test_started_record_audit_refuses_by_name_and_writes_nothing + test_started_record_rotate_out_audit_refuses_by_name_too + test_outcome_rewrite_preserves_the_audit_block + test_started_rewrite_preserves_the_audit_block
- (b) `_audit_floors`/`FALLBACK_AUDIT_FLOOR`/deleted constants + test_floors_are_the_owners_numbers_and_have_one_reader + the floor assertion in test_rotate_out_green_at_verb_level
- (c) `_commit_audit_record` + test_audited_record_is_committed_by_exact_path + test_merge_in_progress_refuses_the_commit_by_name + test_untracked_record_refuses_the_commit_by_name + test_gitless_root_skips_the_commit_without_failing
- (d) `audit_window_point` + both call sites + test_wake_and_out_coexist_in_one_record
- (e) canonical precondition + test_non_canonical_record_refuses_by_name
- (f) the test-file edits above + test_rotate_out_green_at_verb_level (green asserted at VERB level)

## Evidence

Verb file:
    python3 -m pytest extensions/agi/tests/test_sensei_audit_record_writeback.py -q
    -> 25 passed, 1 warning in 0.55s

Focused set (every sensei audit test):
    python3 -m pytest extensions/agi/tests/test_sensei.py test_sensei_wake_audit.py test_sensei_rotate_out_audit.py test_sensei_audit_record_window.py test_sensei_audit_record_writeback.py -q
    -> 173 passed

rotate writers:
    python3 -m pytest test_rotate.py test_rotate_latch_sweep.py test_rotate_closeout.py test_rotate_autopsy.py test_rotate_verb.py test_rotate_selfreap.py -q
    -> 375 passed

FULL SUITE (every `extensions/agi/tests/test_*.py` named explicitly; the bare dir is refused at AGI_TIER=kid):
    -> 4791 passed, 15 skipped, 1 xfailed in 510.28s

Live floor cells read from this tree (`_read_rotations` + `_audit_floors`):
    {'wake': 0, 'out': 1}

## Falsifier (re-runnable by the parent)
- a fixture STARTED record handed to either verb: exit 3, `record still STARTED; audit after the outcome` on stderr, zero bytes changed;
- an `audit` on disk before `rotate._write_rotation_record(path=...)` / `rotate._write_rotate_self_started(...)`: still present and equal afterwards;
- `audit[side].floor` != the config:rotations cell (a changed cell moves the recorded floor);
- a green run on a TRACKED record leaves the record dirty (the commit is `-o -- <record>`, and the path is clean after it).

## Weak
- The commit's FAILED branch (git commit exits non-zero for a reason other than nothing-to-commit) is code, not a test.
- `_preserve_audit` is exercised through the two writer functions, not through a full live rotate-self.
- The out side's `call_index` bound is always null (that window is bounded by a transcript line and the record ts, and no call index is resolved there); the key is still present so no reader has to guess.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL7.134 (a00-ba912100): accepted, verdict kept proved. INSTRUCTION (parent brief, verbatim): run one negative probe per claim conjunct yourself and record them; a kid that passes its own suite but fails your probe is lean_disproved with the probe named. MECHANISM (built and run, 11/11 PASS, probes.py in .agi/sessions/iter-SL7.134/a00-ba912100/): (a) gate: a canonical STARTED record handed to sensei.write_audit_into_record raises AuditRefusal carrying sensei.STARTED_REFUSAL with zero bytes changed; wire: an audit on disk survives BOTH rotate.py writers (_write_rotation_record path= and _write_rotate_self_started), and a fresh audit this run wins. (b) wire: changing the config cell from floor_wake:0 to floor_wake:5 moved the RECORDED floor to 5 and the printed line to (floor 5); AUDIT_FLOOR and AUDIT_SIDES are gone from the module. (c) gate: a tracked record is committed by exact path -- git show --name-only HEAD listed ONLY the record while an unrelated OTHER.txt stayed modified, so nothing is bundled; an untracked record and a MERGE_HEAD tree each REFUSED by name with no commit. (d) wire: both verbs emitted window_start/window_end as dicts with exactly {call_index,line,ts}, with different per-side values. (e) gate: a compact-JSON record raised AuditRefusal naming the canonical byte form, bytes unchanged. (f) gate: two consecutive verb runs produced byte-identical length 662. NEAR MISS: reading the report and the test names would have certified (c) while _commit_audit_record silently returned SKIPPED for every call -- the exact-path commit is only proven by inspecting what git actually committed, which is what P5 does. LIVE CORPUS: one non-canonical live record exists (sequence.json, {"sequence":127}) but it carries no seat field, so _seat_rotation_records never selects it; 177/178 canonical. REGRESSION: 490 passed across the sensei and rotate suites; no collateral from the new (e) precondition. DEVIATION: none.
<!-- THOUGHT:END -->

## Agent Notes
Built (a)-(f): rotate.py _preserve_audit on both writers; sensei.py refuses by name on result:started and on non-canonical bytes; floors read from config:rotations cells (AUDIT_FLOOR/AUDIT_SIDES deleted); finish_audit commits the record git commit -o -- <path> with named MERGE_HEAD/untracked refusals; one window shape {call_index,line,ts}. Full suite 4791 passed / 15 skipped / 1 xfailed.

PARENT VERDICT SL7.134: ACCEPTED as proved. All six claim items (a)-(f) implemented in the diff this parent read (rotate.py _preserve_audit on both writers; sensei.py STARTED refusal + AuditRefusal + _audit_floors cells + AUDIT_FLOOR/AUDIT_SIDES deleted + _commit_audit_record exact-path commit with MERGE_HEAD/untracked refusals + audit_window_point one shape + canonical byte precondition). 11/11 parent-run negative probes pass, 490 regression tests pass. One wire finding below threshold for a demotion but worth the next run: _commit_audit_record resolves the repo through rotate._shared_graph_root and returns SKIPPED when the record lies outside that toplevel, so a caller whose geometry resolution fails would silently not commit -- the FAILED branch is also untested.
