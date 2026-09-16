"""SL7.128 parent probes — one negative probe per claim conjunct.

Probe A (gate class, conjunct 1): the fixture's `seating_merged` must equal
the LITERAL product of `rotate._seating_record_merge_handover` run end-to-end
on disk. If a hand-written dict drifted from the producer/merger, this fails.

Probe B (wire class, conjunct 2): the e2e audit must compose through the live
`sensei._resolve_predecessor_transcript` call site (sensei.py:1702-1705), not
read a fixture value. A spy wrapper proves the call happens; a pre-fix
join-only `_record_transcript` mutation proves the shapes fail without the
fallback (i.e. the coverage is real, not vacuous).
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/ubuntu/work/agi/.agi/worktrees/a00-a0f3395e")
sys.path.insert(0, str(ROOT / "extensions/agi/bin"))
sys.path.insert(0, str(ROOT / "extensions/agi/tests"))

import sensei  # noqa: E402
import rotate  # noqa: E402
import test_sensei_rotate_out_audit as T  # noqa: E402

failures = []


def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        failures.append(name)


# ── PROBE A (gate): fixture == literal on-disk merge product ────────────────
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    graph = tmp / ".agi"
    (graph / "sessions" / "rotations").mkdir(parents=True)
    tr = tmp / "tr.jsonl"
    tr.write_text("{}\n", encoding="utf-8")

    # the producer's record, written to disk exactly as rotate writes it
    rec = rotate._seating_record(
        seat=T.SEAT, role="prime_director", source="rotate",
        window_id=None, ref="", pid=None, session_id="",
        transcript_path=str(tr), first_turn=None, generation=T.GEN)
    rotate._write_seating_record(graph, rec)
    # the merger's OWN handover payload, then the real function
    merge_in = {"seat": rec["seat"], "recorded_at": rec["recorded_at"],
                "handover": {"seating_row_commit": "abc123"}}
    written = rotate._seating_record_merge_handover(graph, merge_in)
    literal = json.loads(Path(written).read_text(encoding="utf-8"))

    # the fixture's dict for the same shape
    graph2, tr2, prev_path = T._write_root_join_absent(
        Path(td) / "fixture", "seating_merged")
    fixture = json.loads(prev_path.read_text(encoding="utf-8"))

    def norm(d):
        d = dict(d)
        d.pop("recorded_at", None)
        d.pop("box", None)          # machine-local fact, not shape
        # each lives in its own tempdir; compare presence, not the path value
        d.pop("transcript_path", None)
        return d

    check("A0 both carry a top-level transcript_path",
          "transcript_path" in fixture and "transcript_path" in literal)

    check("A1 no observations.b_generation in literal merge product",
          "observations" not in literal)
    check("A2 no handover.join in literal merge product",
          "join" not in (literal.get("handover") or {}))
    check("A3 top-level gen_after present on literal merge product",
          literal.get("gen_after") == T.GEN, f"gen_after={literal.get('gen_after')}")
    check("A4 fixture shape == literal on-disk merge product (minus local cells)",
          norm(fixture) == norm(literal),
          f"\n  fixture-only={sorted(set(norm(fixture))-set(norm(literal)))}"
          f"\n  literal-only={sorted(set(norm(literal))-set(norm(fixture)))}"
          f"\n  differing={[k for k in set(norm(fixture))&set(norm(literal)) if norm(fixture)[k]!=norm(literal)[k]]}")

# ── PROBE B (wire): the audit composes through the live resolver ────────────
for shape in ("near_miss", "first_seating", "seating_merged"):
    with tempfile.TemporaryDirectory() as td:
        graph, tr, _ = T._write_root_join_absent(Path(td), shape)
        seen = []
        orig = sensei._resolve_predecessor_transcript

        def spy(*a, **k):
            seen.append(a)
            return orig(*a, **k)

        sensei._resolve_predecessor_transcript = spy
        try:
            code, calls, counts, win = sensei.rotate_out_audit(
                graph, T.SEAT, T.GEN, None)
        finally:
            sensei._resolve_predecessor_transcript = orig

        check(f"B[{shape}] audit calls the live resolver exactly once",
              len(seen) == 1, f"calls={len(seen)}")
        check(f"B[{shape}] audit exits 0 with the fixture path",
              code == 0 and str(win.get("log_path")) == str(tr),
              f"code={code}")

    # pre-fix mutation: join-only `_record_transcript` must make the shape FAIL
    with tempfile.TemporaryDirectory() as td:
        graph, tr, _ = T._write_root_join_absent(Path(td), shape)
        orig_rt = sensei._record_transcript

        def join_only(rec):
            return ((rec.get("handover") or {}).get("join") or {}).get("transcript")

        sensei._record_transcript = join_only
        try:
            code, _, _, _ = sensei.rotate_out_audit(graph, T.SEAT, T.GEN, None)
        finally:
            sensei._record_transcript = orig_rt
        check(f"B[{shape}] pre-fix join-only resolver makes the audit exit 2 "
              f"(coverage is non-vacuous)", code == 2, f"code={code}")

print()
if failures:
    print(f"PROBE FAILURES: {failures}")
    sys.exit(1)
print("ALL PROBES PASS")
