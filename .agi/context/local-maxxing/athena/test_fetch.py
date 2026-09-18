#!/usr/bin/env python3
"""Tests for fetch_parallel.py (TM.33).

Covers the byte-range/resume math the supervisor relies on, and the TM.33
rate SCHEDULE: aggregate cap 1.5 MB/s inside [02:00, 06:00) America/New_York,
else 0.5 MB/s, selected with stdlib zoneinfo (never a fixed UTC offset).

Run: python3 -m pytest .agi/context/local-maxxing/athena/test_fetch.py -q
"""
import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_parallel as fp  # noqa: E402

NY = ZoneInfo("America/New_York")


def at(y, mo, d, h, mi):
    return datetime(y, mo, d, h, mi, tzinfo=NY)


def _seed_sizes():
    # deterministic non-divisible sizes so the divmod remainder is exercised
    fp.FILES["athena"]["size"] = 2405   # 24 segs -> q=100, r=5
    fp.FILES["base"]["size"] = 802      # 16 segs -> q=50,  r=2


# ---------------------------------------------------------------- range math

def test_seg_size_divmod_remainder_first():
    _seed_sizes()
    sizes = [fp.seg_size("athena", i) for i in range(24)]
    assert sizes[:5] == [101] * 5
    assert sizes[5:] == [100] * 19
    assert sum(sizes) == 2405
    # base: remainder 2
    bsizes = [fp.seg_size("base", i) for i in range(16)]
    assert bsizes[:2] == [51, 51]
    assert sum(bsizes) == 802


def test_seg_lo_offsets_match_seg_size():
    _seed_sizes()
    for i in range(24):
        assert fp.seg_lo("athena", i) == sum(fp.seg_size("athena", j) for j in range(i))
    # half-open contiguity: no gaps, no overlap
    assert fp.seg_lo("athena", 23) + fp.seg_size("athena", 23) == 2405


def test_resume_range():
    lo, hi = 100, 199  # 100 bytes
    assert fp.resume_range(lo, hi, 100) is None      # complete
    assert fp.resume_range(lo, hi, 40) == (140, 199)  # partial resumes at have
    assert fp.resume_range(lo, hi, 0) == (100, 199)
    assert fp.resume_range(lo, hi, 101) is None       # over-complete is done


def test_commit_rem_appends_partial_prefix(tmp_path):
    sp = str(tmp_path / "seg000")
    rem = sp + ".rem"
    with open(sp, "wb") as f:
        f.write(b"A" * 10)
    with open(rem, "wb") as f:
        f.write(b"B" * 5)          # a SHORT rem is a valid contiguous prefix
    fp.commit_rem(sp, rem, 0, 19)  # range [0,19] length 20, have=10
    assert open(sp, "rb").read() == b"A" * 10 + b"B" * 5
    assert not os.path.exists(rem)  # nothing downloaded is discarded


def test_commit_rem_truncates_to_range_length(tmp_path):
    sp = str(tmp_path / "seg001")
    rem = sp + ".rem"
    open(sp, "wb").write(b"A" * 10)
    open(rem, "wb").write(b"B" * 20)  # overlong rem
    fp.commit_rem(sp, rem, 10, 24)     # start already = lo + have; range len 15
    assert os.path.getsize(sp) == 25   # appended exactly end-start+1 = 15


# ----------------------------------------------------------------- schedule

def test_schedule_boundaries_frozen():
    # inclusive-exclusive [02:00, 06:00): 01:59 and 06:00 are the outer side.
    cases = {
        (1, 59): fp.DEFAULT_AGG,
        (2, 0): fp.PEAK_AGG,
        (5, 59): fp.PEAK_AGG,
        (6, 0): fp.DEFAULT_AGG,
        (14, 0): fp.DEFAULT_AGG,
    }
    for (h, mi), want in cases.items():
        assert fp.aggregate_limit(at(2026, 9, 18, h, mi)) == want, (h, mi)
        assert fp.per_segment_rate(at(2026, 9, 18, h, mi)) == int(want // 40)


def test_schedule_uses_zone_not_utc_offset():
    # 06:00Z in summer is 02:00 EDT -> PEAK; 10:00Z is 06:00 EDT -> DEFAULT.
    summer = timezone.utc
    assert fp.aggregate_limit(datetime(2026, 7, 15, 6, 0, tzinfo=summer)) == fp.PEAK_AGG
    assert fp.aggregate_limit(datetime(2026, 7, 15, 10, 0, tzinfo=summer)) == fp.DEFAULT_AGG
    # winter: 07:00Z is 02:00 EST -> PEAK; 11:00Z is 06:00 EST -> DEFAULT
    assert fp.aggregate_limit(datetime(2026, 1, 15, 7, 0, tzinfo=summer)) == fp.PEAK_AGG
    assert fp.aggregate_limit(datetime(2026, 1, 15, 11, 0, tzinfo=summer)) == fp.DEFAULT_AGG


def test_dst_offsets_differ_window_holds():
    jan = at(2026, 1, 15, 2, 30)
    jul = at(2026, 7, 15, 2, 30)
    assert jan.utcoffset() != jul.utcoffset()  # EST vs EDT, not a fixed offset
    assert jan.utcoffset().total_seconds() == -5 * 3600
    assert jul.utcoffset().total_seconds() == -4 * 3600
    assert fp.aggregate_limit(jan) == fp.aggregate_limit(jul) == fp.PEAK_AGG


def test_per_segment_rate_is_aggregate_over_segments():
    _seed_sizes()  # sizes do not change the segment COUNT
    assert fp.total_segments() == 40
    assert fp.per_segment_rate(at(2026, 9, 18, 3, 0)) * 40 <= fp.PEAK_AGG
    assert fp.per_segment_rate(at(2026, 9, 18, 14, 0)) * 40 <= fp.DEFAULT_AGG
