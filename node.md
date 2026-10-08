---
id: experiment:a00-9199b0f9-1e0867
mint_id: 2dc27a01c160494da144270a518964c6
type: experiment
parents:
  - hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id
next_edges: []
confidence: 0.9
edited_by: a00-fabd2604
evidence_runs:
  - experiment:a00-9199b0f9-1e0867
loop: hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 629eaf759af3e077
season: 2
title: The record transcript reader reads the top level transcript path with join precedence and both predicates have direct tests
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID — the brief: "Make `_record_transcript` read the top-level `transcript_path` a first-seating record carries"; precedence "mirrors `rotate._record_join`: for the SAME logical identity the `handover.join.*` spelling wins WHEN PRESENT"; plus committed direct tests for both predicates.

WHAT THE MACHINE ACTUALLY DOES — I read the changed bytes, not the report, and ran 21 probes of my own in /tmp/probe_sl7126_parent.py (own fixtures, independent of the kid suite). sensei.py `_record_transcript` now resolves 1) `session_log`, 2) `handover.session_log`, 3) `handover.join.transcript`, 4) TOP-LEVEL `transcript_path` (new), 5) `observations.c_readback_log_path` `.jsonl`-only. All 21 probes PASS: seating-only top-level path resolves (P1a); join wins when both present (P1b); `handover` present with an EMPTY `join` falls through to the top-level key (P1c/P1d); malformed `handover` (str/None/list/int) neither crashes nor loses the top-level read (P1e); `session_log` still outranks it (P1f); the `.log` guard is intact (P1g). `_record_matches_session`: A-top/B-join matches B, does NOT match A, and the A[:8] PREFIX does not sneak through either (P2a-c); empty and None caller ids match nothing (P2d/e); neither spelling matches nothing (P2f/g). WIRE (P3): a `first-seating` record carrying ONLY `transcript_path` is AUDITED end-to-end (code 0, one (a) F2 call, `source` ends `.seating.json`), and DELETING that one key from the same fixture flips the SAME call to code 2 — the transcript can only come from the changed bytes. AUTH (P4): a seating-only record whose top-level `session_id` is another session's is refused by name (code 2, no calls).

THE NEAR MISS — the plausible implementation that satisfies the words and loses the mechanism: put the top-level read as an `elif`/`continue` INSIDE the `if isinstance(ho, dict):` block, or return early from the join branch. A `handover` dict that exists but carries no join is exactly the shape a first-seating-plus-partial-handover record has, and an early return there resolves None for a record that names a real transcript — the defect reintroduced one level deeper. P1c/P1d are the probes that catch it; the landed bytes are correct because the new read sits OUTSIDE and AFTER the whole handover block.

Also not a defect, checked: both engine-suite failures (`test_bin_help_smoke[ws_raw.py]`, `test_workflow.py::test_pi_run_mints_one_credential_for_all_stages` — `ws_raw.py --help` exits 1; workflow cap 1.5 vs 5.0) are unrelated to sensei.py and pre-existing config drift, not this diff.

DEVIATION FROM A STANDING RULE — the parent brief says read the kid DIFF via `git diff merge-base..<kid-branch>` and "do not run git at all". I resolved the contradiction by reading the CHANGED BYTES DIRECTLY off disk (sensei.py, the test file) — same evidence, no git invocation, so neither instruction is violated. The kid ran in this shared checkout with no `--branch`, so there is no kid branch to diff anyway.
<!-- THOUGHT:END -->

# experiment:a00-9199b0f9-1e0867

## Experiment

G15 BUILD ORDER: implement the fix, then prove it on the built bytes.
Pre-fix state (measured, not rerun below): `sensei.py:563-592
_record_transcript` read `session_log`, `handover.session_log`,
`handover.join.transcript`, `observations.c_readback_log_path` and NEVER
the top-level `transcript_path` that `rotate.py` `_seating_record` writes
(rotate.py:5246-5248) -- so a seating-only record was selected and then
refused by the wake audit with `"<record> names no transcript"`.

### DIFF

`extensions/agi/bin/sensei.py` -- `_record_transcript(rec)` only. One new
read, placed as the FALLBACK of the join spelling, so the precedence
mirrors `rotate._record_join` (top level first, `handover.join.*` overwrites
when present):

```python
    # after the handover.session_log / handover.join.transcript reads:
    v = rec.get("transcript_path")
    if v:
        return Path(str(v)).expanduser()
```

Exact resolution order implemented, in code order:

1. `rec["session_log"]`
2. `rec["handover"]["session_log"]`
3. `rec["handover"]["join"]["transcript"]`   <- WINS when present
4. `rec["transcript_path"]`                  <- NEW, top-level fallback
5. `rec["observations"]["c_readback_log_path"]` only when `.jsonl`

The docstring was rewritten to list all five keys it actually reads (it
said four while the code read four plus the new one), and it states the
join-wins precedence explicitly.

`extensions/agi/tests/test_sensei_wake_audit.py` -- three new blocks
(DIRECT unit tests, not call-site tests; no test file previously called
either predicate directly):

- `TestRecordTranscriptDirect` (6 tests): top-level alone resolves; BOTH
  spellings -> join wins; join alone; `session_log` still wins over
  top-level (no regression); `c_readback_log_path` `.log` -> None / `.jsonl`
  -> path; none of the keys -> None.
- `TestRecordMatchesSessionDirect` (5 tests): `{session_id: A,
  handover.join.session_id: B}` matches B and NOT A; top-level alone still
  matches; empty caller id `""` matches nothing; neither spelling matches
  nothing; a full id matches its 8-char prefix and NOT its 7-char prefix
  (the 8-char floor is exercised).
- `test_wake_audit_reads_a_seating_only_records_top_level_transcript`:
  WIRE PROBE -- a `first-seating` record carrying ONLY top-level
  `transcript_path` + `session_id` is audited (code 0, one category-a `F2`
  call, source ends `.seating.json`) instead of refused.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q
83 passed in 0.56s

$ python3 -m pytest extensions/agi/tests/test_sensei.py \
    extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_after_join_service.py -q
119 passed in 1.58s
```

(One `tier-gate: phantom running record ... pid=1459751 (dead) -- skipped`
line is a conftest seat-gate notice on each run, unrelated to these files.)

The three-line negative probe named in the brief -- a seating-only record
with top-level `transcript_path` and no join handed to `_record_transcript`
-> the path, not None -- is test 1 of `TestRecordTranscriptDirect`, and the
end-to-end arm of it is the wire probe above.

## Agent Notes
Built the fix: sensei._record_transcript now reads top-level transcript_path as the fallback of handover.join.transcript (join wins), docstring lists all five keys. Added direct tests for both predicates plus a seating-only wire probe. pytest test_sensei_wake_audit.py: 83 passed; test_sensei/test_sensei_rotate_out_audit/test_after_join_service: 119 passed.
