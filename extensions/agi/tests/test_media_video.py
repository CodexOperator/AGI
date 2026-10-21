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
    assert w == "line there" and w[i0:i1] == "line there"          # a cut inside "second" is moved in to the space


def test_a_window_never_opens_or_ends_inside_a_word(monkeypatch):
    line = "aaaaaaaa bbbbbbbb cccccccc NEEDLE dddddddd eeeeeeee ffffffff"
    monkeypatch.setattr(mv.media_html, "lines_at", lambda repo, sha, path, lo, hi: line)
    for ctx in (3, 7, 10, 13, 20, 25):
        w, i0, i1 = mv.strand_window("r", "s", "p", 1, 1, "NEEDLE", ctx=ctx)
        a = line.index(w)
        assert w[i0:i1] == "NEEDLE" and w in line
        assert a == 0 or line[a - 1] == " "                      # starts at a word start (or the line's)
        assert a + len(w) == len(line) or line[a + len(w)] == " "  # ends at a word end (or the line's)


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


def test_frame_diff_line_sits_between_the_measured_populations():
    """C2 pilot, 10-21: the same picture twice = mean diff 0.17-0.18; a new caption and one more graph node = 1.49-1.79. The line (0.8) is between them."""
    base = bytes([20] * 2000 + [200] * 304)
    same = bytes(base[:-1] + bytes([base[-1] - 1]))                      # one count off in one pixel: ~0.0004
    small = bytes([20 + (9 if k % 6 == 0 else 0) for k in range(2000)]) + bytes([200] * 304)    # 1.5 mean diff
    assert any("does not differ" in f for f in mv.frame_findings([base, same], ["feed", "feed"]))
    d_small = sum(abs(a - b) for a, b in zip(base, small)) / len(base)
    assert 1.3 < d_small < 1.7 and mv.frame_findings([base, small], ["feed", "feed"]) == []
    assert any("does not differ" in f for f in mv.frame_findings([base, same], ["calm", "feed"]))


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


# ---- one chapter end to end, with a stub in place of manim (the real render is the pilot)
STUB = r'''
import json, os, subprocess, sys
sys.path.insert(0, os.environ["STUB_TESTS"])
import media_vocab
if os.environ.get("STUB_MODE") == "exit1":
    sys.exit(1)
if os.environ.get("STUB_MODE") == "sleep":
    import time; time.sleep(60)
open(os.environ["STUB_MARK"], "w").write("rendered")
plan = json.load(open(os.environ["M4_PLAN"]))
drawn = []
for b in plan["beats"]:
    for p in b["pairs"]:
        s = media_vocab.Strand(os.environ["M4_REPO"], p["sha"], p["path"], p["lo"], p["hi"], p["needle"], b["i"])
        text = "".join(t for ln in s.lines for t, _ in ln)
        if os.environ.get("STUB_MODE") == "badbyte":
            text = text[:2] + ("Q" if text[2] != "Q" else "Z") + text[3:]
        drawn.append({"kind": "strand", "beat": b["i"], "sha": s.sha, "path": s.path, "lo": s.lo, "hi": s.hi, "text": text})
json.dump(drawn, open(os.environ["M4_DRAWN"], "w"))
out = os.path.join(os.environ["M4_MEDIA"], "videos", os.environ["M4_OUT"] + ".mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1280x720:r=25", "-t", str(plan["duration"] + 0.2), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "ultrafast", out], check=True)
'''


@pytest.fixture
def job(tmp_path, chaps, monkeypatch):
    """A 9 s chapter of three sentences with real pairs, a narration with pauses where the sentences end, and the Drive-like dirs."""
    real = chaps[2]["pairs"]
    chap = {"id": "C2", "n": 2, "title": "The ribosome: the unit turns pieces into tools", "sha": chaps[2]["sha"],
            "pairs": {"C2.2": real["C2.2"], "C2.3": real["C2.3"]},
            "narration": ["Hello there friend. [image] The unit makes a worktree. [C2.2] It refuses a trunk. [C2.3]"]}
    mp3 = tmp_path / "season3-C2-narration.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=300:sample_rate=44100:duration=9", "-af", "volume='if(between(t,2.3,2.9)+between(t,6.1,6.7),0,1)':eval=frame", str(mp3)], check=True)
    d = {k: str(tmp_path / k) for k in ("video", "deliver", "tmp", "static", "checks")}
    for k in ("deliver", "tmp"):
        os.makedirs(d[k])
    name = mv.video_name(chap)
    Path(d["deliver"], name).write_bytes(b"STATIC")
    Path(d["deliver"], "README-narration.txt").write_text(f"head\n{name}: chapter C2, static-card version; the animated render is pending\n")
    stub = tmp_path / "stub.py"; stub.write_text(STUB)
    monkeypatch.setenv("STUB_TESTS", str(HERE)); monkeypatch.setenv("STUB_MARK", str(tmp_path / "mark"))
    return dict(chap=chap, mp3=str(mp3), d=d, name=name, cmd=[sys.executable, str(stub)], mark=tmp_path / "mark")


GO = lambda peak: (True, ["ok"])


def go(job, **kw):
    kw.setdefault("gate", GO); kw.setdefault("poll", 0.05); kw.setdefault("read", lambda: None)
    return mv.run_chapter(2, job["chap"], job["mp3"], job["d"], job["cmd"], REPO, **kw)


def test_e2e_green_publishes_swaps_keeps_the_card_and_marks_the_readme(job):
    r = go(job, publish_it=True)
    d = job["d"]
    assert r["status"] == "green" and r["findings"] == [] and r["published"] and r["vmpeak_kb"] >= 0
    assert Path(d["deliver"], job["name"]).read_bytes() != b"STATIC" and Path(d["static"], job["name"]).read_bytes() == b"STATIC"
    assert mv.pending(d["deliver"], d["checks"]) .count(2) == 0 and len(r["keyframes"]) == 3 and all(os.path.getsize(k) > 1000 for k in r["keyframes"])
    assert mv.profile_findings(mv.probe(str(Path(d["deliver"], job["name"])))) == []


def test_e2e_without_publish_leaves_deliver_alone(job):
    r = go(job, publish_it=False)
    assert r["status"] == "green" and "unpublished" in r and Path(job["d"]["deliver"], job["name"]).read_bytes() == b"STATIC"


def test_e2e_mutant_a_drawn_byte_that_is_not_the_engines_is_red_and_nothing_moves(job, monkeypatch):
    monkeypatch.setenv("STUB_MODE", "badbyte")
    r = go(job, publish_it=True)
    assert r["status"] == "red: checks" and any("not in" in f for f in r["findings"])
    assert Path(job["d"]["deliver"], job["name"]).read_bytes() == b"STATIC" and mv.pending(job["d"]["deliver"], job["d"]["checks"]).count(2) == 1
    assert json.load(open(Path(job["d"]["checks"], "ch02.json")))["green"] is False


def test_e2e_mutant_a_refused_start_test_renders_nothing(job):
    r = go(job, gate=lambda peak: (False, ["NO MemAvailable 2.0 GB"]))
    assert r["status"] == "refused: start test" and not job["mark"].exists()


def test_e2e_mutant_red_timing_renders_nothing(job):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=300:sample_rate=44100:duration=9", job["mp3"] + ".x.mp3"], check=True)
    r = mv.run_chapter(2, job["chap"], job["mp3"] + ".x.mp3", job["d"], job["cmd"], REPO, gate=GO, poll=0.05, read=lambda: None)
    assert r["status"] == "red: timing" and not job["mark"].exists()


def test_e2e_a_render_that_exits_1_is_failed_not_published(job, monkeypatch):
    monkeypatch.setenv("STUB_MODE", "exit1")
    r = go(job, publish_it=True)
    assert r["status"] == "failed: exit 1" and Path(job["d"]["deliver"], job["name"]).read_bytes() == b"STATIC"


def test_e2e_mutant_memory_stop_twice_is_stopped_memory_with_the_process_group_gone(job, monkeypatch):
    monkeypatch.setenv("STUB_MODE", "sleep")
    pids, real = [], mv.subprocess.Popen

    def spy(*a, **k):
        p = real(*a, **k)
        if k.get("start_new_session"):
            pids.append(p.pid)
        return p

    monkeypatch.setattr(mv.subprocess, "Popen", spy)
    r = go(job, publish_it=True, read=lambda: "anon+shmem 4300 MiB > 4200")
    assert r["status"] == "stopped: memory" and r["stops"] == 2 and len(pids) == 2          # two tries, no third
    for pid in pids:
        with pytest.raises(ProcessLookupError):
            os.killpg(pid, 0)                                                              # the whole process group is gone


def test_the_render_runs_under_the_address_space_limit(job, monkeypatch, tmp_path):
    probe_py = tmp_path / "lim.py"
    probe_py.write_text("import resource,os;open(os.environ['STUB_MARK'],'w').write(str(resource.getrlimit(resource.RLIMIT_AS)[0]))\n")
    mv.run_chapter(2, job["chap"], job["mp3"], job["d"], [sys.executable, str(probe_py)], REPO, gate=GO, poll=0.05, read=lambda: None, vmlimit_kb=3000000)
    assert job["mark"].read_text() == str(3000000 * 1024)


def test_video_name_is_the_walks_name(chaps):
    assert mv.video_name(chaps[2]) == "explainer-ch02-the-ribosome-the-unit-turns-pieces-into-tools.mp4"
    assert mv.video_name(chaps[0]).startswith("explainer-ch00-")


# ---- council 10-21 09:52Z: the token-wrap rule
COUNCIL_LINE = 'Environment="AGI_PIECE_GLOB=engine.md engine-[pw]*.md"'


def rows_of(lines):
    return ["".join(t for t, _ in ln if t != "\n") for ln in lines]


def naive_wrap(window, width):
    """The mutant: the old cut, at a space in the last 10 columns, else mid-token."""
    out, s = [], 0
    while len(window) - s > width:
        end = s + width
        sp = window.rfind(" ", s + width - 10, s + width)
        if sp > s:
            end = sp + 1
        out.append(window[s:end]); s = end
    return out + [window[s:]]


def test_the_councils_example_wraps_at_legal_breaks_and_the_old_cut_is_what_the_row_catches():
    rows = rows_of(mv.wrap(COUNCIL_LINE, 0, len(COUNCIL_LINE), 26))
    assert mv.token_findings(rows) == [] and "".join(rows) == COUNCIL_LINE
    assert mv.token_findings(naive_wrap(COUNCIL_LINE, 26))                    # 'AGI_PIECE_GLO' | 'B=engine.md ...': the row fires on the old rule


def test_no_drawn_line_of_any_pair_of_the_script_ends_inside_a_word(chaps):
    n = 0
    for c in chaps.values():
        for b in mv.beats(c, REPO):
            for p in b["pairs"]:
                w, i0, i1 = mv.strand_window(REPO, p["sha"], p["path"], p["lo"], p["hi"], p["needle"])
                lines = mv.wrap(w, i0, i1, 26)
                assert mv.rejoin(lines) == w and mv.token_findings(rows_of(lines)) == [], (c["id"], p["id"])
                assert max(len(r) for r in rows_of(lines)) <= 40        # none needs more than ~65 % shrinking (see MIN_SCALE)
                n += 1
    assert n > 300


def test_a_token_longer_than_the_line_runs_long_instead_of_being_cut():
    w = "x " + "a" * 60 + " y"
    rows = rows_of(mv.wrap(w, 0, len(w), 26))
    assert mv.token_findings(rows) == [] and "a" * 60 in "".join(rows) and any(len(r) > 26 for r in rows) and "".join(rows) == w


def test_every_cut_is_a_legal_one_at_every_width():
    for width in (6, 9, 14, 26, 44):
        rows = rows_of(mv.wrap(COUNCIL_LINE + " " + COUNCIL_LINE, 0, 10, width))
        assert mv.token_findings(rows) == []


def test_check_drawn_reds_a_cut_word_a_lost_line_and_a_font_too_small(chaps, pair):
    bs = [b for b in mv.beats(chaps[2], REPO) if b["kind"] == "feed"][:1]
    plan = {"beats": bs}
    d = drawn_of(bs[0]["pairs"][0], bs[0]["i"])[0]
    real = [dict(d, rows=[d["text"]], scale=1.0)]
    assert mv.check_drawn(real, plan, REPO) == []
    k = next(i for i in range(1, len(d["text"])) if d["text"][i - 1].isalnum() and d["text"][i].isalnum())
    cut = dict(d, rows=[d["text"][:k], d["text"][k:]], scale=1.0)
    assert any("ends inside a word" in f for f in mv.check_drawn([cut], plan, REPO))
    assert any("do not re-join" in f for f in mv.check_drawn([dict(d, rows=[d["text"][:-3]], scale=1.0)], plan, REPO))
    assert any("of its font" in f for f in mv.check_drawn([dict(d, rows=[d["text"]], scale=0.4)], plan, REPO))
    assert mv.check_drawn([dict(d, rows=[d["text"]], scale=0.55)], plan, REPO) == []       # the line is exact: 0.55 passes, 0.54 does not
    assert mv.check_drawn([dict(d, rows=[d["text"]], scale=0.54)], plan, REPO)


# ---- timing counts, falsifiers, the named C6 exception
def test_counts_carry_the_dp_the_08_alone_and_the_greedy_rule():
    lens, dur, pauses, _ = synth()
    c = mv.timing_counts(lens, dur, pauses)
    assert set(c) == {"dp_rel", "dp_tol_only", "greedy"} and c["dp_rel"] <= c["dp_tol_only"]


def test_the_real_c6_counts_are_the_numbers_in_the_readme(chaps):
    mp3 = mv.BASE + "/deliver/season3-C6-narration.mp3"
    if not os.path.exists(mp3):
        pytest.skip("no narration file here")
    pl = mv.chapter_plan(chaps[6], mp3)
    assert pl["counts"] == {"dp_rel": 10, "dp_tol_only": 12, "greedy": 15} and pl["fallback"] == 10
    offs = mv.prior_offsets(pl)
    assert len(offs) == 10 and all(x["ok"] for x in offs)


def test_falsifier_pauses_filled_with_noise_is_red(job):
    noisy = Path(job["mp3"]).with_name("noisy.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=300:sample_rate=44100:duration=9", "-f", "lavfi", "-i", "anoisesrc=amplitude=0.3:sample_rate=44100:duration=9",
                    "-filter_complex", "[0:a]volume='if(between(t,2.3,2.9)+between(t,6.1,6.7),0,1)':eval=frame[a];[a][1:a]amix=inputs=2:duration=first", str(noisy)], check=True)
    pl = mv.chapter_plan(job["chap"], str(noisy))
    assert mv.timing_findings(pl)                                          # no pause is found: every end on the prior


def test_falsifier_another_chapters_sentences_against_this_audio_is_red(chaps):
    mp3 = mv.BASE + "/deliver/season3-C2-narration.mp3"
    if not os.path.exists(mp3):
        pytest.skip("no narration file here")
    pauses, dur = mv.silences(mp3), mv.mp3_seconds(mp3)
    right = mv.place([len(b["spoken"]) for b in mv.beats(chaps[2], REPO)], dur, pauses)
    wrong = mv.place([len(b["spoken"]) for b in mv.beats(chaps[3], REPO)], dur, pauses)
    assert mv.timing_findings(right) == [] and (mv.timing_findings(wrong) or wrong["fallback"] > right["fallback"] + 4)


def plan_of(job, kinds, ends, rate=None):
    pl = mv.chapter_plan(job["chap"], job["mp3"])
    ends = ends[:-1] + [pl["duration"]]
    pl["kind"], pl["ends"], pl["prior"] = kinds, ends, list(ends)
    pl["fallback"] = kinds.count("prior")
    for b, e0, e1 in zip(pl["beats"], [0.0] + ends[:-1], ends):
        b["t0"], b["t1"] = e0, e1
    if rate:
        pl["rate"] = rate
    return pl


def test_prior_offsets_ok_and_fail_rows():
    pl = {"beats": [{"spoken": "a" * 100}, {"spoken": "b" * 20}, {"spoken": "c" * 100}], "rate": 10.0, "kind": ["prior", "prior", "end"], "ends": [10.2, 13.0, 30.0], "pauses": [(10.0, 10.4)]}
    r = mv.prior_offsets(pl)
    assert [x["ok"] for x in r] == [True, False] and r[0]["offset"] == 0.0 and r[1]["offset"] == 2.6 and r[1]["shorter_s"] == 2.0     # 2.6 s from the nearest pause > 2.0 s neighbour


def test_c6_exception_is_accepted_on_a_number_and_refused_when_an_offset_fails(job, tmp_path):
    ok = plan_of(job, ["prior", "prior", "end"], [2.6, 6.4, 9.0])
    assert mv.timing_findings(ok)                                                        # 100 % on the prior is RED for any chapter
    r = mv.run_chapter(6, job["chap"], job["mp3"], job["d"], job["cmd"], REPO, gate=GO, poll=0.05, read=lambda: None, plan=ok)
    assert r["status"] == "green" and "C6: timing approximate, 2 of 2 boundaries on the prior" in r["exception"] and "council ruling" in r["exception"]
    bad = plan_of(job, ["prior", "prior", "end"], [2.6, 6.4, 9.0], rate=40.0)            # the neighbours are then 0.5 s long: 0.0 offsets still pass, so move one end off its pause
    bad["ends"][0] = bad["prior"][0] = 4.6
    r2 = mv.run_chapter(6, job["chap"], job["mp3"], job["d"], job["cmd"], REPO, gate=GO, poll=0.05, read=lambda: None, plan=bad)
    assert r2["status"] == "red: timing" and any("named exception C6 refused" in f for f in r2["findings"])
    other = mv.run_chapter(2, job["chap"], job["mp3"], job["d"], job["cmd"], REPO, gate=GO, poll=0.05, read=lambda: None, plan=ok)
    assert other["status"] == "red: timing"                                              # the line stays 25 % for every other chapter


def test_the_readme_row_carries_the_three_counts_and_the_exception(job):
    ok = plan_of(job, ["prior", "prior", "end"], [2.6, 6.4, 9.0])
    r = mv.run_chapter(6, job["chap"], job["mp3"], job["d"], job["cmd"], REPO, gate=GO, poll=0.05, read=lambda: None, plan=ok, publish_it=True)
    row = [ln for ln in Path(job["d"]["deliver"], "README-narration.txt").read_text().split("\n") if ln.startswith(job["name"])][0]
    assert "animated version" in row and "2 of 2 boundaries on the prior (DP with 12 % REL; the approved 0.7 s alone" in row and "the approved greedy rule" in row and "council ruling" in row and r["status"] == "green"


def test_rel_is_named_as_a_deviation_and_the_ulimit_and_exceptions_are_the_rulings():
    src = Path(mv.__file__).read_text()
    assert "DEVIATION 5" in src and mv.REL == 0.12 and mv.TOL == 0.7 and mv.FALLBACK_MAX == 0.25
    assert mv.VMLIMIT_KB == 2500000 and set(mv.EXCEPTIONS) == {6}
    assert "CONSISTENCY re-check" in src


# ---- the publish checks after, the joined-duration check
def test_mutant_publish_that_writes_into_the_kept_cards_inode_is_red_and_restores(tree, monkeypatch):
    d, name = tree
    real = os.replace
    calls = []

    def evil(src, dst):
        if not calls and str(dst).endswith(name):
            calls.append(1)
            import shutil
            shutil.copyfile(src, dst); os.remove(src)             # in place: the kept hard link now holds the NEW bytes too
        else:
            real(src, dst)

    monkeypatch.setattr(mv.os, "replace", evil)
    with pytest.raises(ValueError, match="publish check failed"):
        publish_green(d, name)
    assert (d["deliver"] / name).exists()                            # the file is there (put back by os.replace of the kept link); the check named the fault


def test_publish_check_passes_on_the_real_swap_twice(tree):
    d, name = tree
    publish_green(d, name)
    publish_green(d, name, body=b"ANIMATED v2")
    assert os.stat(d["deliver-static"] / name).st_ino != os.stat(d["deliver"] / name).st_ino and (d["deliver-static"] / name).read_bytes() == b"STATIC CARD"


def test_joined_duration_is_the_sum_of_the_18_files_not_the_old_c2_and_not_both(tmp_path):
    dd = tmp_path / "deliver"; dd.mkdir()
    for i in range(3):
        make_mp4(dd / f"explainer-ch{i:02d}-x.mp4", secs=2)
    (dd / "README-narration.txt").write_text("x")
    tot = mv.deliver_total(str(dd))
    assert 5.9 < tot < 6.3 and mv.joined_findings(tot + 0.4, str(dd)) == [] and mv.joined_findings(tot - 0.4, str(dd)) == []
    assert mv.joined_findings(tot + 2.0, str(dd))                                 # the old C2 AND the new one in the join
    assert mv.joined_findings(tot - 2.0, str(dd))                                 # a chapter missing from the join


# ---- the queue files
def test_wait_start_touches_rendering_first_and_hold_only_after_an_hour(tmp_path):
    q, h = tmp_path / "RENDERING", tmp_path / "HOLD-GATES"
    clock, log = [0.0], []
    answers = iter([(False, ["NO gate"])] * 4 + [(True, ["ok"])])

    def start(peak):
        assert q.exists()                                                       # RENDERING exists before the start test is even read
        return next(answers)

    def sleep(s):
        clock[0] += 1500                                                        # 25 min per poll: the 4th read, at 4500 s, fails after the hour: the hold is touched there and not at 3000 s
        assert not h.exists() or clock[0] > 3600

    ok, _ = mv.wait_start(1500, poll=1, queue=str(q), hold=str(h), start=start, sleep=sleep, now=lambda: clock[0], log=log.append)
    assert ok and q.exists() and h.exists() and len(log) == 1 and "HOLD-GATES touched" in log[0]


def test_wait_start_does_not_hold_at_59_minutes_and_does_at_60(tmp_path):
    for waited, held in ((3599, False), (3600, True)):
        q, h = tmp_path / f"q{waited}", tmp_path / f"h{waited}"
        clock = [0.0]
        seq = iter([(False, []), (False, []), (True, [])])

        def start(peak, clock=clock):
            r = next(seq)
            if len(clock) == 1 and r[0] is False and clock[0] == 0.0:
                pass
            return r

        def sleep(s, clock=clock, waited=waited):
            clock[0] = waited if clock[0] == 0.0 else clock[0] + 1

        mv.wait_start(1500, poll=1, queue=str(q), hold=str(h), start=start, sleep=sleep, now=lambda clock=clock: clock[0], log=lambda m: None)
        assert h.exists() is held, waited


def test_wait_start_with_a_ready_box_never_touches_hold(tmp_path):
    q, h = tmp_path / "RENDERING", tmp_path / "HOLD-GATES"
    ok, _ = mv.wait_start(1500, queue=str(q), hold=str(h), start=lambda p: (True, ["ok"]), sleep=lambda s: None)
    assert ok and q.exists() and not h.exists()


def test_the_render_command_removes_rendering_even_when_the_job_fails(tmp_path, monkeypatch):
    q = tmp_path / "RENDERING"
    monkeypatch.setattr(mv, "QUEUE", str(q))

    def boom(*a, **k):
        q.touch(); raise RuntimeError("render blew up")

    monkeypatch.setattr(mv, "run_chapter", boom)
    with pytest.raises(RuntimeError):
        mv.main(["render", "2"])
    assert not q.exists()


def test_the_row_as_the_council_wrote_it_independent_of_the_codes_own_regex(chaps):
    """'no drawn line ends inside an [A-Za-z0-9_.] run that continues on the next line', with its OWN regex here (a change to media_video.WORD must not move this row)."""
    import re as _re
    word = _re.compile(r"[A-Za-z0-9_.]")
    seen = 0
    for c in chaps.values():
        for b in mv.beats(c, REPO):
            for p in b["pairs"]:
                w, i0, i1 = mv.strand_window(REPO, p["sha"], p["path"], p["lo"], p["hi"], p["needle"])
                rows = rows_of(mv.wrap(w, i0, i1, 26))
                for a, nx in zip(rows, rows[1:]):
                    assert not (a and nx and word.match(a[-1]) and word.match(nx[0])), (c["id"], p["id"], a[-14:], nx[:14])
                    seen += 1
    assert seen > 200
    rows = rows_of(mv.wrap(COUNCIL_LINE, 0, len(COUNCIL_LINE), 26))
    assert not any(word.match(a[-1]) and word.match(b[0]) for a, b in zip(rows, rows[1:]))


def test_render_then_publish_as_two_steps_keyframes_between(job):
    r = go(job, publish_it=False)
    d = job["d"]
    assert r["status"] == "green" and Path(d["deliver"], job["name"]).read_bytes() == b"STATIC" and Path(r["unpublished"]).exists()
    plan = json.load(open(Path(d["video"], "ch02-plan.json")))
    sha = mv.publish_chapter(2, d, json.load(open(Path(d["checks"], "ch02.report.json"))), plan)
    assert Path(d["deliver"], job["name"]).read_bytes() != b"STATIC" and Path(d["static"], job["name"]).read_bytes() == b"STATIC" and mv.pending(d["deliver"], d["checks"]).count(2) == 0
    assert json.load(open(Path(d["checks"], "ch02.report.json")))["published"] == sha


def test_a_red_chapter_cannot_be_published_later(job, monkeypatch):
    monkeypatch.setenv("STUB_MODE", "badbyte")
    r = go(job, publish_it=False)
    assert r["status"] == "red: checks"
    with pytest.raises(ValueError, match="not a green rendered chapter"):
        mv.publish_chapter(2, job["d"], json.load(open(Path(job["d"]["checks"], "ch02.report.json"))), json.load(open(Path(job["d"]["video"], "ch02-plan.json"))))
    assert Path(job["d"]["deliver"], job["name"]).read_bytes() == b"STATIC"
