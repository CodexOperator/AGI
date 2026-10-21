"""goal:g5.4.2 M4: the animated explainer's rules (media_video.py), each with its mutant: a hand-broken input must turn the check RED. No render, no manim, no provider call.
Council 10-21 08:03Z: C1 byte-exact by construction, C2 timing fallback > 25 %, C3 .tmp outside deliver/, C4 the static card kept, C5 the queue is bytes, A2 two SIGTERMs, the start test."""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_video as mv  # noqa: E402
import media_vocab  # noqa: E402,F401  (imports without manim)

REPO = str(HERE.parents[2])
SCRIPT = REPO + "/.agi/context/media/season3-explainer-script.md"


@pytest.fixture(scope="module")
def chaps():
    return mv.load_chapters(SCRIPT, REPO)


# ---- timing: C2
def synth(n=12, rate=17.5, end_pause=0.7, comma=0.3, seed=3):
    """A chapter made by hand: n sentences of known length, a long pause after each, and a short comma pause inside every one. -> lens, duration, pauses, true ends."""
    import random
    rnd = random.Random(seed)
    lens = [rnd.randint(60, 220) for _ in range(n)]
    t, pauses, ends = 0.0, [], []
    for L in lens:
        sp = L / rate
        pauses.append((t + sp * 0.45, t + sp * 0.45 + comma))
        t += sp + comma
        if len(ends) < n - 1:
            pauses.append((t, t + end_pause)); ends.append(t + end_pause / 2); t += end_pause
    return lens, t, pauses, ends


def test_parse_silence_pairs_starts_with_ends_and_drops_an_open_one():
    txt = "[x] silence_start: 0\n[x] silence_end: 0.29 | silence_duration: 0.29\n[x] silence_start: 4.4\n[x] silence_end: 5.2 | d\n[x] silence_start: 9.0\n"
    assert mv.parse_silence(txt) == [(0.0, 0.29), (4.4, 5.2)]


def test_place_finds_every_sentence_end_among_comma_decoys():
    lens, dur, pauses, ends = synth()
    pl = mv.place(lens, dur, pauses)
    assert pl["fallback"] == 0 and pl["kind"][-1] == "end"
    assert all(abs(a - b) < 0.01 for a, b in zip(pl["ends"], ends)) and pl["ends"][-1] == dur
    assert mv.timing_findings(pl) == [] and mv.verify_ends(pl, pauses, dur, lens) == []


def test_mutant_a_shifted_boundary_list_is_red():
    lens, dur, pauses, _ = synth()
    pl = mv.place(lens, dur, pauses)
    bad = dict(pl, ends=[e + 0.5 for e in pl["ends"][:-1]] + [pl["ends"][-1]])
    assert mv.verify_ends(bad, pauses, dur, lens)                     # no longer the middle of any pause


def test_mutant_a_real_pause_in_the_wrong_place_is_red():
    """The end of a long sentence moved to the comma pause inside it: a real pause, in order, but only half the sentence's speech lies before it."""
    lens, dur, pauses, _ = synth()
    pl = mv.place(lens, dur, pauses)
    k = max(range(1, len(lens) - 1), key=lambda i: lens[i])
    inside = [(a + b) / 2 for a, b in pauses if pl["ends"][k - 1] < (a + b) / 2 < pl["ends"][k] - 1.0]
    assert inside and lens[k] / 17.5 > 6
    ends = list(pl["ends"]); ends[k] = inside[0]
    found = mv.verify_ends(dict(pl, ends=ends), pauses, dur, lens)
    assert any(f"end {k} " in f and "speech" in f for f in found)


def test_a_missing_sentence_pause_falls_back_and_is_counted():
    lens, dur, pauses, ends = synth()
    gone = [p for p in pauses if abs((p[0] + p[1]) / 2 - ends[4]) > 0.01]
    pl = mv.place(lens, dur, gone)
    assert pl["fallback"] >= 1 and "prior" in pl["kind"]
    assert mv.verify_ends(pl, gone, dur, lens) == []                  # the fallback is honest, not a finding by itself


def test_mutant_more_than_a_quarter_of_the_boundaries_on_the_prior_is_red_and_the_edge_is_exact():
    base = {"boundaries": 30}
    assert mv.timing_findings(dict(base, fallback=7)) == []           # 23 %
    assert mv.timing_findings(dict(base, fallback=8))                 # 26.7 %
    lens, dur, pauses, _ = synth(20)
    keep = pauses[::6]                                                # most sentence pauses missing
    pl = mv.place(lens, dur, keep)
    assert pl["fallback"] > 0.25 * pl["boundaries"] and mv.timing_findings(pl)


def test_verify_ends_catches_a_lying_report():
    lens, dur, pauses, _ = synth()
    pl = mv.place(lens, dur, pauses)
    assert mv.verify_ends(dict(pl, fallback=3), pauses, dur, lens)                         # count that is not the count
    assert mv.verify_ends(dict(pl, ends=pl["ends"][:-1] + [dur - 5]), pauses, dur, lens)   # last end is not the mp3's length
    e = list(pl["ends"]); e[3], e[4] = e[4], e[3]
    assert mv.verify_ends(dict(pl, ends=e), pauses, dur, lens)                             # out of order
    k = list(pl["kind"]); k[2] = "prior"
    assert mv.verify_ends(dict(pl, kind=k), pauses, dur, lens)                             # claims the prior at a pause


def test_the_real_c2_is_green_and_chains_end_to_start(chaps):
    mp3 = mv.BASE + "/deliver/season3-C2-narration.mp3"
    if not os.path.exists(mp3):
        pytest.skip("no narration file here")
    pl = mv.chapter_plan(chaps[2], mp3)
    assert len(pl["beats"]) == 31 and pl["beats"][0]["t0"] == 0 and abs(pl["beats"][-1]["t1"] - pl["duration"]) < 0.01
    assert all(abs(a["t1"] - b["t0"]) < 0.01 for a, b in zip(pl["beats"], pl["beats"][1:]))
    assert mv.timing_findings(pl) == [] and mv.verify_ends(pl, pl["pauses"], pl["duration"], [len(b["spoken"]) for b in pl["beats"]]) == []


# ---- beats
def test_beats_one_per_tagged_sentence_feed_iff_it_cites(chaps):
    bs = mv.beats(chaps[2], REPO)
    assert len(bs) == 31 and bs[0]["kind"] == "calm" and bs[0]["tag"] == "image" and bs[0]["spoken"].startswith("Now let us watch the ribosome")
    assert all((b["kind"] == "feed") == bool(b["pairs"]) for b in bs)
    two = [b for b in bs if len(b["pairs"]) == 2]
    assert two and all(p["id"].startswith("C2.") for b in bs for p in b["pairs"])
    assert "[" not in "".join(b["spoken"] for b in bs) and "{{" not in "".join(b["spoken"] for b in bs)


def test_every_chapter_has_beats_and_every_pair_needle_is_in_its_range(chaps):
    for n, c in chaps.items():
        for b in mv.beats(c, REPO):
            for p in b["pairs"]:
                mv.strand_window(REPO, p["sha"], p["path"], p["lo"], p["hi"], p["needle"])      # raises if not there


# ---- frames
def test_schedule_adds_up_to_the_beat_exactly_for_any_times():
    import random
    rnd = random.Random(1)
    for _ in range(300):
        t0 = rnd.uniform(0, 100); t1 = t0 + rnd.uniform(0.5, 12)
        want, rest = mv.schedule(t0, t1, [0.5, 0.7, 0.4, 0.7, 0.3])
        assert sum(want) + rest == round(t1 * 25) - round(t0 * 25)
        assert all(w >= 1 for w in want) and rest >= 0


def test_mutant_naive_rounding_drifts_but_schedule_does_not():
    """Each beat rounded to whole frames on its own drifts (4.37 s = 109.25 frames, 200 beats = 2 s late); schedule() re-syncs at every beat, so the running total IS the plan time."""
    t, total, naive = 0.0, 0, 0
    for _ in range(200):
        want, rest = mv.schedule(t, t + 4.37, [0.5, 0.7, 0.4, 0.7, 0.3])
        total += sum(want) + rest
        naive += round(4.37 * 25)
        t += 4.37
        assert total == round(t * 25)
    assert abs(naive - round(t * 25)) > 25            # the mutant is a second late or more: it would have been RED against the mp3 (0.2 s)


def test_schedule_cuts_parts_that_do_not_fit():
    want, rest = mv.schedule(0.0, 1.0, [0.5, 0.7, 0.4, 0.7, 0.3])
    assert sum(want) + rest == 25 and rest >= 0 and all(w >= 1 for w in want)    # cut together; the wait takes what is left


# ---- engine bytes: C1
@pytest.fixture(scope="module")
def pair(chaps):
    return chaps[2]["pairs"]["C2.4"]


def drawn_of(pair_, beat=3, text=None):
    s = media_vocab.Strand(REPO, pair_["sha"], pair_["path"], pair_["lo"], pair_["hi"], pair_["needle"], beat)
    return {"kind": "strand", "beat": beat, "sha": s.sha, "path": s.path, "lo": s.lo, "hi": s.hi, "text": mv.rejoin(s.lines) if text is None else text}, s


def test_strand_window_holds_the_needle_inside_its_line(pair):
    w, i0, i1 = mv.strand_window(REPO, pair["sha"], pair["path"], pair["lo"], pair["hi"], pair["needle"])
    assert w[i0:i1] == pair["needle"] and "\n" not in w and len(w) <= len(pair["needle"]) + 68
    with pytest.raises(ValueError):
        mv.strand_window(REPO, pair["sha"], pair["path"], pair["lo"], pair["hi"], "this is not in the engine at all")


def test_the_window_stops_at_the_ends_of_the_needles_line(monkeypatch):
    monkeypatch.setattr(mv.media_html, "lines_at", lambda repo, sha, path, lo, hi: "first line here\nsecond line there\nthird line")
    assert mv.strand_window("r", "s", "p", 1, 3, "second")[0] == "second line there"          # not the line above it, not the line below
    assert mv.strand_window("r", "s", "p", 1, 3, "line there")[0] == "second line there"
    w, i0, i1 = mv.strand_window("r", "s", "p", 1, 3, "line there", ctx=3)
    assert w == "nd line there" and w[i0:i1] == "line there"


def test_wrap_rejoins_exactly_at_every_width_and_keeps_hard_newlines():
    w = "abc def ghi jkl mno pqr\nstu vwx yz"
    for width in (3, 5, 8, 11, 44, 200):
        assert mv.rejoin(mv.wrap(w, 4, 13, width)) == w
    hot = "".join(t for ln in mv.wrap(w, 4, 13, 8) for t, h in ln if h)
    assert hot == w[4:13]


def test_mutant_wrap_that_drops_a_character_is_caught_by_the_rejoin():
    lines = mv.wrap("abc def ghi jkl", 0, 3, 6)
    lines[1][0] = (lines[1][0][0][1:], lines[1][0][1])
    assert mv.rejoin(lines) != "abc def ghi jkl"


def test_the_real_strands_of_the_whole_script_are_substrings_of_the_engine(chaps):
    drawn = []
    for c in chaps.values():
        for b in mv.beats(c, REPO):
            for p in b["pairs"]:
                d, _ = drawn_of(p, b["i"]); drawn.append(d)
    plan = {"beats": [{"i": i, "kind": "feed", "pairs": [None]} for i in range(0)]}
    assert mv.check_drawn(drawn, plan, REPO) == []


def test_check_drawn_green_then_every_mutant(chaps, pair):
    c = chaps[2]
    bs = [b for b in mv.beats(c, REPO) if b["kind"] == "feed"][:3]
    plan = {"beats": bs}
    good = [drawn_of(p, b["i"])[0] for b in bs for p in b["pairs"]]
    assert mv.check_drawn(good, plan, REPO) == []
    # one byte of the drawn text is not the engine's
    bad = [dict(d) for d in good]; t = bad[0]["text"]; bad[0]["text"] = t[:3] + ("Q" if t[3] != "Q" else "Z") + t[4:]
    assert any("not in" in f for f in mv.check_drawn(bad, plan, REPO))
    # text from another range of the file
    other = [dict(d) for d in good]; other[0]["lo"], other[0]["hi"] = 1, 1
    assert mv.check_drawn(other, plan, REPO)
    # a file that does not exist at the sha
    gone = [dict(d) for d in good]; gone[0]["path"] = "no/such/file.md"
    assert any("unreadable" in f for f in mv.check_drawn(gone, plan, REPO))
    # a feed beat that drew fewer strands than it has pairs
    missing = [d for d in good if d["beat"] != bs[1]["i"]]
    assert any(f"beat {bs[1]['i']}" in f for f in mv.check_drawn(missing, plan, REPO))
    # feed beats and nothing checked at all: RED
    assert any(f.startswith("RED") for f in mv.check_drawn([], plan, REPO))
    # an unknown kind is not silently accepted
    assert mv.check_drawn(good + [{"kind": "mystery", "beat": 0, "sha": pair["sha"], "path": pair["path"], "lo": pair["lo"], "hi": pair["hi"]}], plan, REPO)


def test_a_chapter_with_only_calm_beats_needs_no_strand():
    assert mv.check_drawn([], {"beats": [{"i": 0, "kind": "calm", "pairs": []}]}, REPO) == []


# ---- lint: C1
def test_lint_is_clean_on_the_real_scene_and_vocab():
    assert mv.lint([str(HERE / "media_scene.py"), str(HERE / "media_vocab.py"), str(HERE / "media_video.py")]) == []


@pytest.mark.parametrize("src", ["from manim import *\nt = Text('x')\n", "import manim as m\nt = m.Code('x')\n", "t = MarkupText('<b>x</b>')\n", "t = MathTex('a')\n",
                                 "from manim import Text as T\n", "x = Paragraph('a')\n"])
def test_mutant_raw_text_outside_vocab_is_red(src):
    assert mv.lint_source(src, "scenes.py")


def test_lint_does_not_flag_words_in_strings_or_comments_and_vocab_is_exempt(tmp_path):
    assert mv.lint_source("# Text( is drawn by vocab\ns = 'Code(x)'\nV.caption('Text(')\n") == []
    p = tmp_path / "media_vocab.py"; p.write_text("t = Text('x')\n")
    assert mv.lint([str(p)]) == []
    q = tmp_path / "other.py"; q.write_text("t = Text('x')\n")
    assert mv.lint([str(q)])


# ---- the file checks
def walk_profile():
    src = (HERE / "media_walk.py").read_text()
    line = next(ln for ln in src.split("\n") if ln.startswith("PROFILE = "))
    return ast.literal_eval(line.split("=", 1)[1].strip())


def test_the_profile_is_the_walks_profile():
    assert mv.PROFILE == walk_profile()


def make_mp4(path, size="1280x720", fps=25, pix="yuv420p", ar=44100, ac=1, acodec="aac", secs=1):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x14181f:s={size}:r={fps}", "-f", "lavfi", "-i", f"sine=frequency=300:sample_rate={ar}",
                    "-t", str(secs), "-ac", str(ac), "-pix_fmt", pix, "-c:v", "libx264", "-c:a", acodec, str(path)], check=True)
    return str(path)


def test_probe_green_on_the_profile_and_each_mutant_is_red(tmp_path):
    assert mv.profile_findings(mv.probe(make_mp4(tmp_path / "a.mp4"))) == []
    for kw in ({"size": "1920x1080"}, {"fps": 30}, {"pix": "yuv444p"}, {"ar": 48000}, {"ac": 2}, {"acodec": "mp2"}):
        assert mv.profile_findings(mv.probe(make_mp4(tmp_path / "m.mp4", **kw))), kw


def test_duration_within_two_tenths_of_the_mp3_and_not_beyond():
    assert mv.duration_findings(100.0, 100.19) == [] and mv.duration_findings(100.21, 100.0)


def test_frame_findings_blank_static_and_good():
    flat = bytes([20] * 2304)
    lit = bytes([20] * 2000 + [200] * 304)
    lit2 = bytes([20] * 1500 + [200] * 804)
    assert mv.frame_findings([lit, lit2, lit], ["feed", "feed", "feed"]) == []
    assert any("blank" in f for f in mv.frame_findings([lit, flat], ["calm", "calm"]))                  # mutant: an empty frame
    assert any("does not differ" in f for f in mv.frame_findings([lit, lit], ["calm", "feed"]))         # mutant: a feed beat that changed nothing
    assert mv.frame_findings([lit, lit], ["calm", "calm"]) == []                                         # a calm beat may hold still
    assert any("no frame" in f for f in mv.frame_findings([lit, b""], ["calm", "calm"]))


# ---- the start test (fake files): council 10-21 08:03Z
def box(tmp_path, anon=2500, shmem=0, slab=10, high=5120, avail_gb=4.0, mem_full=0.1, io_some=1.0, gate=False, other=True):
    s = tmp_path / "slice"; s.mkdir(exist_ok=True)
    MiB = 1048576
    (s / "memory.stat").write_text(f"anon {anon * MiB}\nfile 123\nshmem {shmem * MiB}\nslab_unreclaimable {slab * MiB}\n")
    (s / "memory.high").write_text(f"{high * MiB}\n" if isinstance(high, int) else high)
    (tmp_path / "meminfo").write_text(f"MemTotal: 1 kB\nMemAvailable: {int(avail_gb * 1024 * 1024)} kB\n")
    p = tmp_path / "psi"; p.mkdir(exist_ok=True)
    (p / "memory").write_text(f"some avg10=0.0 avg60=0.2 avg300=0.0 total=1\nfull avg10=0.0 avg60={mem_full} avg300=0.0 total=1\n")
    (p / "io").write_text(f"some avg10=0.0 avg60={io_some} avg300=0.0 total=1\nfull avg10=0.0 avg60=0.1 avg300=0.0 total=1\n")
    pr = tmp_path / "proc"; pr.mkdir(exist_ok=True)
    if other:
        d = pr / "11"; d.mkdir(exist_ok=True); (d / "comm").write_text("bash\n")
        (tmp_path / "work").mkdir(exist_ok=True)
        if not (d / "cwd").exists():
            os.symlink(tmp_path / "work", d / "cwd")
    if gate:
        d = pr / "12"; d.mkdir(exist_ok=True); (d / "comm").write_text("pytest\n")
        g = tmp_path / "home" / "gate" / "run"; g.mkdir(parents=True, exist_ok=True)
        if not (d / "cwd").exists():
            os.symlink(g, d / "cwd")
    return dict(slice_dir=str(s), meminfo=str(tmp_path / "meminfo"), psi_dir=str(p), proc=str(pr))


def test_start_test_passes_on_a_quiet_box(tmp_path):
    ok, lines = mv.start_test(1500, **box(tmp_path))
    assert ok and len(lines) == 6 and all(ln.startswith("ok") for ln in lines)


@pytest.mark.parametrize("kw,word", [(dict(anon=3400, shmem=200), "anon+shmem"), (dict(avail_gb=2.9), "MemAvailable"), (dict(mem_full=2.0), "mem PSI"),
                                     (dict(io_some=50.0), "io PSI"), (dict(gate=True), "gate pytest"), (dict(anon=3000, slab=1000, high=5000), "headroom")])
def test_mutant_each_threshold_refuses_at_its_line(tmp_path, kw, word):
    ok, lines = mv.start_test(1500, **box(tmp_path, **kw))
    assert not ok and any(ln.startswith("NO") and word in ln for ln in lines)


def test_the_lines_are_exact_at_the_edges(tmp_path):
    for i, (kw, want) in enumerate([(dict(anon=3499), True), (dict(anon=3500), False), (dict(avail_gb=3.0), True), (dict(mem_full=1.99), True), (dict(io_some=49.9), True)]):
        t = tmp_path / str(i); t.mkdir()
        assert mv.start_test(0, **box(t, high=9000, **kw))[0] is want, kw


def test_headroom_uses_the_render_peak(tmp_path):
    k = box(tmp_path, anon=2500, slab=10, high=5120)          # 2510 + peak < 4820
    assert mv.start_test(2300, **k)[0] and not mv.start_test(2400, **k)[0]


def test_fail_closed_a_missing_or_garbage_read_refuses(tmp_path):
    k = box(tmp_path)
    assert not mv.start_test(1500, **dict(k, slice_dir=str(tmp_path / "no-such-cgroup")))[0]          # mutant: a nonexistent cgroup path
    assert not mv.start_test(1500, **dict(k, meminfo=str(tmp_path / "no-meminfo")))[0]
    assert not mv.start_test(1500, **dict(k, psi_dir=str(tmp_path / "no-psi")))[0]
    assert not mv.start_test(1500, **dict(k, proc=str(tmp_path / "no-proc")))[0]
    t = tmp_path / "g"; t.mkdir()
    assert not mv.start_test(1500, **box(t, high="max\n"))[0]                                         # memory.high = max is not a number
    t = tmp_path / "h"; t.mkdir()
    kk = box(t); Path(kk["meminfo"]).write_text("MemAvailable: lots kB\n")
    assert not mv.start_test(1500, **kk)[0]
    t = tmp_path / "i"; t.mkdir()
    kk = box(t); (Path(kk["psi_dir"]) / "memory").write_text("garbage\n")
    assert not mv.start_test(1500, **kk)[0]


def test_a_nan_anon_does_not_slip_through(tmp_path):
    k = box(tmp_path)
    Path(k["slice_dir"], "memory.stat").write_text("anon nan\nshmem 0\nslab_unreclaimable 0\n")
    assert not mv.start_test(1500, **k)[0]


def test_stop_reason_at_its_lines_and_unreadable_raises(tmp_path):
    k = box(tmp_path)
    assert mv.stop_reason(k["slice_dir"], k["psi_dir"]) is None
    t = tmp_path / "a"; t.mkdir(); k = box(t, anon=4300)
    assert "4200" in mv.stop_reason(k["slice_dir"], k["psi_dir"])
    t = tmp_path / "b"; t.mkdir(); k = box(t, anon=4200)
    assert mv.stop_reason(k["slice_dir"], k["psi_dir"]) is None
    t = tmp_path / "c"; t.mkdir(); k = box(t, mem_full=10.5)
    assert "PSI" in mv.stop_reason(k["slice_dir"], k["psi_dir"])
    with pytest.raises(OSError):
        mv.stop_reason(str(tmp_path / "nowhere"), k["psi_dir"])


# ---- the watcher: A2
class FakeProc:
    def __init__(self, polls, rc=0):
        self.polls, self.rc, self.returncode, self.waited = polls, rc, None, False

    def poll(self):
        if self.polls <= 0:
            self.returncode = self.rc
            return self.rc
        self.polls -= 1
        return None

    def wait(self):
        self.waited = True; self.returncode = -15


def watcher(reads, procs):
    spawned, termed = [], []

    def spawn():
        p = procs.pop(0); spawned.append(p); return p

    def read():
        r = reads.pop(0) if reads else None
        if isinstance(r, Exception):
            raise r
        return r

    return mv.Watcher(spawn, read, lambda s: None, termed.append), spawned, termed


def test_a_clean_run_is_ok_and_no_term():
    w, sp, tm = watcher([None] * 5, [FakeProc(3)])
    assert w.run() == ("ok", 0) and tm == [] and len(sp) == 1


def test_first_stop_requeues_and_the_second_try_can_finish():
    w, sp, tm = watcher(["anon+shmem 4300 MiB > 4200", None, None, None, None], [FakeProc(9), FakeProc(2)])
    assert w.run() == ("ok", 1) and len(tm) == 1 and len(sp) == 2


def test_mutant_two_sigterms_is_stopped_memory_and_no_third_try():
    w, sp, tm = watcher(["a", "b", "c"], [FakeProc(9), FakeProc(9), FakeProc(9)])
    assert w.run() == ("stopped: memory", 2) and len(sp) == 2 and len(tm) == 2 and all(p.waited for p in tm)


def test_three_unreadable_reads_in_a_row_stop_two_do_not():
    w, sp, tm = watcher([OSError(), OSError(), OSError()], [FakeProc(9), FakeProc(0)])
    assert w.run()[1] == 1 and len(tm) == 1
    w, sp, tm = watcher([OSError(), OSError(), None, None], [FakeProc(4)])
    assert w.run() == ("ok", 0) and tm == []


def test_a_failed_render_is_reported_not_requeued():
    w, sp, tm = watcher([None] * 5, [FakeProc(2, rc=1)])
    assert w.run()[0] == "failed: exit 1" and len(sp) == 1


def test_the_watcher_only_terms_it_never_stops_a_process():
    src = Path(mv.__file__).read_text()
    assert "SIGSTOP" not in src.replace('never SIGSTOP', "") and "send_signal(19)" not in src


# ---- publish / undo / queue: C3 C4 C5
@pytest.fixture
def tree(tmp_path):
    d = {k: tmp_path / k for k in ("deliver", "deliver-tmp", "deliver-static", "checks")}
    for v in d.values():
        v.mkdir()
    name = "explainer-ch02-the-ribosome.mp4"
    (d["deliver"] / name).write_bytes(b"STATIC CARD")
    (d["deliver"] / "README-narration.txt").write_text(
        "head\n\n" f"{name}: chapter C2, static-card version; the animated render is pending\n  chunk 0 attempt 1: reused\n"
        "explainer-ch00-cold-open.mp4: chapter C0, static-card version; the animated render is pending\n")
    return d, name


def publish_green(d, name, green=True, body=b"ANIMATED"):
    tmp = d["deliver-tmp"] / name
    tmp.write_bytes(body)
    return mv.publish(str(tmp), name, str(d["deliver"]), str(d["deliver-static"]), str(d["deliver-tmp"]), str(d["checks"] / "ch02.json"), green, {"chapter": "C2"})


def test_publish_swaps_atomically_keeps_the_static_card_and_leaves_no_tmp(tree):
    d, name = tree
    inode_before = os.stat(d["deliver"] / name).st_ino
    sha = publish_green(d, name)
    assert (d["deliver"] / name).read_bytes() == b"ANIMATED" and (d["deliver-static"] / name).read_bytes() == b"STATIC CARD"
    assert os.stat(d["deliver-static"] / name).st_ino == inode_before          # the old file itself, not a copy: nothing was ever missing from deliver/
    assert sorted(os.listdir(d["deliver"])) == sorted([name, "README-narration.txt"]) and os.listdir(d["deliver-tmp"]) == []
    assert json.load(open(d["checks"] / "ch02.json"))["sha256"] == sha and oct(os.stat(d["deliver"] / name).st_mode & 0o777) == "0o644"


def test_mutant_a_tmp_inside_deliver_is_refused(tree):
    d, name = tree
    tmp = d["deliver"] / (name + ".tmp"); tmp.write_bytes(b"x")
    with pytest.raises(ValueError):
        mv.publish(str(tmp), name, str(d["deliver"]), str(d["deliver-static"]), str(d["deliver"]), str(d["checks"] / "c.json"), True, {})
    assert (d["deliver"] / name).read_bytes() == b"STATIC CARD"


def test_mutant_a_tmp_on_another_filesystem_is_refused(tree, monkeypatch):
    d, name = tree
    real = os.stat
    monkeypatch.setattr(mv.os, "stat", lambda p, *a, **k: type("S", (), {"st_dev": 99})() if str(p).endswith("deliver-tmp") else real(p, *a, **k))
    tmp = d["deliver-tmp"] / name; tmp.write_bytes(b"x")
    with pytest.raises(ValueError):
        mv.publish(str(tmp), name, str(d["deliver"]), str(d["deliver-static"]), str(d["deliver-tmp"]), str(d["checks"] / "c.json"), True, {})


def test_a_red_chapter_moves_nothing_but_writes_its_red_checks_file(tree):
    d, name = tree
    assert publish_green(d, name, green=False) is None
    assert (d["deliver"] / name).read_bytes() == b"STATIC CARD" and not (d["deliver-static"] / name).exists()
    assert json.load(open(d["checks"] / "ch02.json"))["green"] is False


def test_undo_is_one_rename_back(tree):
    d, name = tree
    publish_green(d, name)
    mv.undo(name, str(d["deliver"]), str(d["deliver-static"]))
    assert (d["deliver"] / name).read_bytes() == b"STATIC CARD" and not (d["deliver-static"] / name).exists()


def test_a_second_publish_does_not_overwrite_the_kept_static_card(tree):
    d, name = tree
    publish_green(d, name); (d["deliver-tmp"] / name).write_bytes(b"v2")
    publish_green(d, name, body=b"ANIMATED v2")
    assert (d["deliver-static"] / name).read_bytes() == b"STATIC CARD" and (d["deliver"] / name).read_bytes() == b"ANIMATED v2"


def done_readme(d, name, n=2, version="animated version"):
    mv.set_readme_row(str(d["deliver"] / "README-narration.txt"), name, f"C{n}", version)


def test_queue_is_read_from_bytes_and_in_the_pilot_order(tree):
    d, name = tree
    q = mv.pending(str(d["deliver"]), str(d["checks"]))
    assert q[:3] == [2, 0, 1] and q[3:] == list(range(3, 18))
    publish_green(d, name); done_readme(d, name)
    assert mv.pending(str(d["deliver"]), str(d["checks"]))[:2] == [0, 1]          # C2 is done


def test_mutant_the_static_rows_word_animated_does_not_count_as_done(tree):
    d, name = tree
    publish_green(d, name)                                    # checks green, bytes swapped, README still says "the animated render is pending"
    assert 2 in mv.pending(str(d["deliver"]), str(d["checks"]))
    assert mv.animated_rows((d["deliver"] / "README-narration.txt").read_text()) == {}


def test_mutant_readme_says_animated_but_checks_are_missing_red_or_for_other_bytes(tree):
    d, name = tree
    publish_green(d, name); done_readme(d, name)
    assert 2 not in mv.pending(str(d["deliver"]), str(d["checks"]))
    j = json.load(open(d["checks"] / "ch02.json")); j["green"] = False; json.dump(j, open(d["checks"] / "ch02.json", "w"))
    assert 2 in mv.pending(str(d["deliver"]), str(d["checks"]))                                 # red checks
    j["green"] = True; json.dump(j, open(d["checks"] / "ch02.json", "w"))
    (d["deliver"] / name).write_bytes(b"SOMETHING ELSE")
    assert 2 in mv.pending(str(d["deliver"]), str(d["checks"]))                                 # the checks were made for other bytes
    os.remove(d["checks"] / "ch02.json")
    assert 2 in mv.pending(str(d["deliver"]), str(d["checks"]))                                 # no checks file
    os.remove(d["deliver"] / name)
    assert 2 in mv.pending(str(d["deliver"]), str(d["checks"]))                                 # no mp4


def test_no_readme_means_everything_is_pending(tmp_path):
    (tmp_path / "d").mkdir(); (tmp_path / "c").mkdir()
    assert mv.pending(str(tmp_path / "d"), str(tmp_path / "c")) == mv.ORDER


def test_set_readme_row_changes_only_its_row(tree):
    d, name = tree
    p = d["deliver"] / "README-narration.txt"
    before = p.read_text().split("\n")
    done_readme(d, name)
    after = p.read_text().split("\n")
    diff = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
    assert len(before) == len(after) and len(diff) == 1 and after[diff[0]].startswith(name + ": chapter C2, animated version")
    with pytest.raises(ValueError):
        mv.set_readme_row(str(p), "explainer-ch09-nope.mp4", "C9", "animated version")
    p.write_text(p.read_text() + f"{name}: again\n")
    with pytest.raises(ValueError):
        done_readme(d, name)


def test_the_order_is_every_chapter_once_pilot_first():
    assert sorted(mv.ORDER) == list(range(18)) and mv.ORDER[0] == 2
