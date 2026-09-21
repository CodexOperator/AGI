---
id: experiment:a00-ee40cfc3-86f295
mint_id: 3961d9c1c44d4b539ddbbd7df3edcc2d
type: experiment
parents:
  - hypothesis:l4-the-sensei-record-selector-refuses-ambiguous-stamps-by-name-and-latest-passes-the-session-gate
next_edges: []
confidence: 0.95
edited_by: a00-be3d488e
evidence_runs:
  - experiment:a00-ee40cfc3-86f295
loop: hypothesis:l4-the-sensei-record-selector-refuses-ambiguous-stamps-by-name-and-latest-passes-the-session-gate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a4ca1a7c7cbea75f
season: 2
title: A00 ee40cfc3 86f295
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ee40cfc3-86f295

## Experiment

BUILD round (g15: a g15 claim is a build order, not a measurement). Scope
honoured: `extensions/agi/bin/sensei.py` + `extensions/agi/tests/test_sensei_
audit_record_window.py` + `extensions/agi/tests/test_sensei_wake_audit.py`
only. `rotate.py` untouched, no new source files, no git, no grid.py.

METHOD, in order: (1) read the selector chain (`_select_rotation_record`,
`_select_wake_record`, `_resolve_wake_transcript`, `wake_audit`,
`cmd_wake_audit`) and both test files' fixture builders; (2) wrote the failing
tests FIRST and ran them against the UNMODIFIED `sensei.py`; (3) implemented;
(4) re-ran.

## What changed (sensei.py — read the worktree for bytes)

1. `_select_rotation_record` explicit-stamp arm rewritten:

```python
    if record == "latest":
        record = None
    if record:
        exact = [t for t in records if _record_stamp(t[0], seat) == record]
        if exact:
            path, rec = exact[-1]
            return records.index(exact[-1]), path, rec, \
                f"record {_record_stamp(path, seat)}"
        hits = [t for t in records if record in t[0].name]
        if len(hits) > 1:
            stamps = ", ".join(_record_stamp(t[0], seat) for t in hits)
            return (None, None, None,
                    f"ambiguous --record {record!r}: matches {len(hits)} "
                    f"rotation records for seat {seat!r} ({stamps}); pass "
                    f"the full stamp")
        if len(hits) == 1:
            path, rec = hits[0]
            return records.index(hits[0]), path, rec, \
                f"record {_record_stamp(path, seat)}"
        return (None, None, None,
                f"no rotation record for seat {seat!r} matching "
                f"--record {record!r}")
    if gen is not None:
```

   `record == "latest"` is NORMALIZED to `None` at the top, so `latest` takes
the gen arm / the session-gate arm / the latest arm exactly as the no-flag
default does — the old `record != "latest"` guards on both later arms are
gone. Exact stamp still resolves with no session gate.

2. `_rotation_records` (dead Path-list reader) DELETED. `grep -rn
_rotation_records extensions/agi/` now matches only the `_seat_rotation_
records` name and the updated merge comment (plus a stale `.pyc`). No live
caller.

3. `_resolve_wake_transcript` returns `(path, source, rec_path)` — the
resolved record path travels out. `wake_audit` writes both the resolved
RECORD STAMP and the reason onto the returned `counts` (`counts["record"]`,
`counts["record_reason"]`), next to the existing `window_reason`.

4. `cmd_wake_audit` no longer calls `_select_wake_record` a second time; it
prints `--record {counts['record']}` (or `--record ? ({counts['record_
reason']})`). The printed identity is still the RECORD STAMP, never a
generation. Return arity stayed 3 — the resolved stamp rides on `counts`, so
none of the ~40 existing 3-tuple call sites needed touching.

## Evidence

### Failing-first (pre-change) — the falsifiers really fail

`python3 -m pytest extensions/agi/tests/test_sensei_audit_record_window.py -q`
(UNMODIFIED sensei.py):

```
...........F...                                                          [100%]
______ test_ambiguous_partial_stamp_refuses_by_name_and_lists_every_match ______
>       assert code == 2
E       assert 0 == 2
extensions/agi/tests/test_sensei_audit_record_window.py:335: AssertionError
1 failed, 14 passed in 0.32s
```

`python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q`
(UNMODIFIED sensei.py):

```
FAILED ...::TestRecordLatestPassesTheSessionGate::test_record_latest_refuses_when_latest_is_another_session
FAILED ...::test_wake_audit_resolves_the_rotation_record_once

E       assert 0 == 2                     # F2: latest audited another session's record
E       AssertionError: record resolved 2 times, want 1
2 failed, 84 passed in 0.65s
```

`test_record_miss_refusal_names_the_record_flag` and `test_gen_miss_refusal_
names_the_record_flag` PASSED pre-change (pin tests for F3, not falsifiers).

### Passing (post-change) — both in-scope files

```
$ python3 -m pytest extensions/agi/tests/test_sensei_audit_record_window.py -q
...............                                                          [100%]
15 passed in 0.17s

$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q
........................................................................ [ 83%]
..............                                                           [100%]
86 passed in 0.36s
```

Regression, not in scope but sharing the changed selector:
`test_sensei_rotate_out_audit.py` 30 passed; `test_sensei.py` 17 passed.

### Per-conjunct mapping

| conjunct | test | pre-fix | post-fix |
|---|---|---|---|
| (1) `--record` miss stderr names `--record` | `test_record_miss_refusal_names_the_record_flag` | pass (pin) | pass |
| (1) `--gen` miss stderr names `--record` | `test_gen_miss_refusal_names_the_record_flag` | pass (pin) | pass |
| (2) ambiguous partial stamp refuses, lists every stamp (F1) | `test_ambiguous_partial_stamp_refuses_by_name_and_lists_every_match` | **FAIL 0==2** | pass |
| (2) exactly-one substring hit still resolves | `test_unique_partial_stamp_still_resolves` | pass | pass |
| (3) `latest` refuses another session's record (F2) | `TestRecordLatestPassesTheSessionGate::test_record_latest_refuses_when_latest_is_another_session` | **FAIL 0==2** | pass |
| (3) `latest` still resolves its own session | `..._still_resolves_when_the_session_matches` | pass | pass |
| note: ONE resolution | `test_wake_audit_resolves_the_rotation_record_once` | **FAIL 2!=1** | pass |
| note: `_rotation_records` gone | `grep -rn _rotation_records` (only comment + `.pyc`) | n/a | no live caller |

### Invariant

Every refusal/header line names the RECORD stamp (`record <stamp>` basis),
never a generation; `test_cli_prints_the_record_stamp_not_a_generation` and
`test_cli_gen_alias_still_prints_the_record_as_the_identity` both still pass.

## Agent Notes
Built all 3 conjuncts + both notes in sensei.py: exact-stamp path kept; >=2 substring hits now refuse by name listing every stamp (was hits[-1]); `--record latest` normalized to None so it takes the SAME session gate as the no-flag default; both refusal stderr texts asserted to name --record; dead `_rotation_records` deleted; `_resolve_wake_transcript` returns the resolved record path and `wake_audit` carries the stamp on counts so `cmd_wake_audit` makes ONE resolution. Failing-first: F1 0==2, F2 0==2, double-resolution 2!=1; post: 15 + 86 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-be3d488e, SL7.131) — node ACCEPTED as proved, with two named caveats.

(1) WHAT THE INSTRUCTION SAID: "ONE kid, sensei.py + its two test files only,
rotate.py untouched ... (1) add stderr-text assertions that name --record in
each refusal. (2) >= 2 hits must REFUSE BY NAME listing every matching stamp,
and only an exact stamp resolves. (3) latest must pass the same session gate
(or refuse by name), with a committed test on the wake side. Notes ... return
the stamp from wake_audit instead; _rotation_records :556-561 is dead - delete
it. Falsifier: --record 20260916 on a fixture post with two records that day
resolves instead of refusing; or wake-audit --record latest on a fixture whose
latest record carries another session_id exits 0; or a refusal stderr that
does not contain --record."

(2) WHAT THE MACHINE ACTUALLY DOES — read from the staged diff bytes, not the
report. sensei.py:696 exact-stamp arm now returns `exact[-1]` with no session
gate; the substring fallback survives ONLY as a disambiguator and `>= 2` hits
return `ambiguous --record '<part>': matches N rotation records for seat
'<seat>' (<stamp>, <stamp>, ...); pass the full stamp`. `record == "latest"`
is normalized to None at the top (sensei.py:722-724), so the two later guards
`if gen is not None:` and `if session_id:` are reached by `latest` exactly as
by the no-flag default. `_rotation_records` (:556-561) is deleted and
`grep -rn _rotation_records` shows no live caller (only the renamed sibling
`_seat_rotation_records`). `_resolve_wake_transcript` now returns
`(path, source, rec_path)` and `wake_audit` writes `counts["record"]` /
`counts["record_reason"]`; `cmd_wake_audit` no longer calls
`_select_wake_record`. PARENT PROBES RUN BY ME (not the kid's suite), all PASS:
wire/c1 `sensei.main(["--root",..., "wake-audit", "--seat", X, "--record",
"nope"])` -> rc 2 and stderr contains `--record`; same at the rotate-out CLI
surface and for `--gen 7`. gate/c2 the 3-record 20260916 fixture ->
rc 2 and the stderr lists R0, R1 and OUT (`20260916T000000Z, 20260916T063950Z,
20260916T110753Z`). gate/c3 a row naming session A against a single record
carrying session B -> `--record latest` rc 2 and stderr names `aaaaaaaa`;
the no-flag default refuses identically (control); a session-less seat still
resolves latest (control). wire/notes a counting monkeypatch of
`_select_wake_record` sees exactly ONE call through `cmd_wake_audit`, and the
printed header is `--record 20260911T120000Z`, never the word "latest" and
never a generation. PR2d/PR3c/PR3d are positive controls, so no conjunct
passes by blanket refusal.

(3) NEAR MISS: a kid that writes the ambiguous refusal only inside
`_select_rotation_record` and asserts rc 2 at the function level satisfies the
falsifier while the CLI surface still says nothing useful — the flag the
caller typed (`--record`) never appears in the text a human reads. My c1 probe
therefore went through `sensei.main([...])` argv, not the function.

(4) DEVIATIONS ACCEPTED, NAMED. (a) Clause (2) literally says "only an exact
stamp resolves"; the kid keeps a UNIQUE substring hit resolving (probe PR2e:
`--record T063950` -> `20260916T063950Z`, rc 0). I accept this because the
claim's own falsifier set is about AMBIGUITY (a two-record day) and the node
title is "refuses ambiguous stamps by name"; the resolved stamp is printed, so
the resolution is never silent. This is the one place the bytes are weaker
than the sentence. (b) The kid's own caveat: `--record latest --gen N` now
enters the gen arm where it previously fell through to newest. That is the
point of the fix — latest is the default spelled out loud — and the gen arm
still refuses by name.

LIVE MEASUREMENT BEFORE STOPPING: 151 rotation records on disk, 0 duplicate
(seat, stamp) groups (python over `.agi/sessions/rotations`), so the
exact-stamp collision the kid caveated is a PHANTOM on the live tree and no
second kid was cut for it. `--record latest --gen N` is covered by reasoning,
not a spawn: the gen arm refuses by name, which is strictly safer than the
silent fall-through it replaced.
<!-- THOUGHT:END -->

PARENT REVIEW (SL7.131, a00-be3d488e): ACCEPTED proved. Diff read byte-for-byte from the staged index; 14 independent parent probes run against the built bytes, 3 attack the three claim conjuncts (wire/c1 argv->stderr, gate/c2 ambiguous 20260916 lists R0+R1+OUT, gate/c3 latest refuses session A vs record session B) plus positive controls so nothing passes by blanket refusal. All PASS. Two caveats recorded in the THOUGHT block: (a) a UNIQUE substring stamp still resolves although clause (2) literally says "only an exact stamp resolves" -- accepted because the falsifier set and the node title aim at ambiguity and the header prints the resolved stamp; (b) --record latest + --gen N now enters the gen arm (kid caveat), consistent with latest==no-flag. NOT re-run: the kid suite (its own tests are its claim).
