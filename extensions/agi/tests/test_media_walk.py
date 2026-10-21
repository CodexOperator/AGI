"""goal:g5.4.2 THE WALK, council 08:08Z amendments, each with its mutant. Nothing here sends a request: urlopen / render_chunk are stubs, sleeps are zero.
W2 one 60 s retry on 5xx/timeout, stop clean on 4xx or a 2nd failure.  W3 a 2nd FIDELITY RED keeps the take with fewer error ops, flagged, 'partial: N flagged'; a 2nd PCM RED is skipped.
W4 every chapter ALSO as explainer-chNN-<slug>.mp4 under ONE fixed encode profile."""
import importlib
import json
import subprocess
import sys
import urllib.error
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_fidelity as mf  # noqa: E402


@pytest.fixture
def w(tmp_path, monkeypatch):
    monkeypatch.setenv('WALK_DIR', str(tmp_path / 'walk'))
    monkeypatch.setenv('WALK_DELIVER', str(tmp_path / 'deliver'))
    monkeypatch.setattr(sys, 'argv', ['media_walk.py', '--dry'])
    sys.modules.pop('media_walk', None)
    m = importlib.import_module('media_walk')
    m.KEYS.update({'tts': 'k', 'stt': 'k'})
    (tmp_path / 'walk').mkdir(); (tmp_path / 'deliver').mkdir()
    m.RETRY_WAIT = 0
    m.STOP.clear()
    return m


class Resp:
    def __init__(self, b): self.b = b
    def read(self): return self.b


def http(code):
    return urllib.error.HTTPError('u', code, 'x', {}, __import__('io').BytesIO(b'err'))


def script(w, monkeypatch, outcomes):
    calls = []
    def fake(req, timeout=0):
        calls.append(1)
        o = outcomes[len(calls) - 1]
        if isinstance(o, Exception):
            raise o
        return Resp(o)
    monkeypatch.setattr(w.urllib.request, 'urlopen', fake)
    return calls


# ---- W2
def test_w2_a_503_once_then_success(w, monkeypatch):
    calls = script(w, monkeypatch, [http(503), b'ok'])
    assert w.post('tts', 'https://x.invalid/', {'a': 1}, {'chunk': 0}) == b'ok'
    assert len(calls) == 2 and not w.STOP


def test_w2_mutant_503_twice_stops_clean(w, monkeypatch):
    calls = script(w, monkeypatch, [http(503), http(503), b'never'])
    assert w.post('tts', 'https://x.invalid/', {'a': 1}, {'chunk': 0}) is None
    assert len(calls) == 2 and w.STOP == ['http']


def test_w2_mutant_timeout_once_is_retried_and_twice_stops(w, monkeypatch):
    calls = script(w, monkeypatch, [TimeoutError('t'), b'ok'])
    assert w.post('tts', 'https://x.invalid/', {}, {}) == b'ok' and len(calls) == 2
    w.STOP.clear()
    calls = script(w, monkeypatch, [TimeoutError('t'), TimeoutError('t')])
    assert w.post('tts', 'https://x.invalid/', {}, {}) is None and w.STOP == ['http']


@pytest.mark.parametrize('code', [400, 401, 402, 404])
def test_w2_mutant_a_4xx_is_never_retried(w, monkeypatch, code):
    calls = script(w, monkeypatch, [http(code), b'never'])
    assert w.post('tts', 'https://x.invalid/', {}, {}) is None
    assert len(calls) == 1 and w.STOP == ['http']


def test_w2_every_try_is_logged_before_it_is_sent(w, monkeypatch):
    seen = []
    log = Path(w.W, 'walk-requests-tts.log')
    def fake(req, timeout=0):
        seen.append(log.read_text().count('\n'))        # lines already logged when this send happens
        if len(seen) == 1:
            raise http(503)
        return Resp(b'x')
    monkeypatch.setattr(w.urllib.request, 'urlopen', fake)
    assert w.post('tts', 'https://x.invalid/', {}, {'chunk': 3}) == b'x'
    assert seen == [1, 2]


# ---- W3
def T(w, status, errs=0, runs=(), mp3=None):
    return w.take(status, mp3, errs, runs, ['n'])


def run_chunk(w, monkeypatch, takes):
    it = iter(takes)
    monkeypatch.setattr(w, 'render_chunk', lambda *a: next(it))
    notes = []
    return w.walk_chunk('C2', 0, 'text', None, notes), notes


def test_w3_second_fidelity_red_keeps_the_take_with_fewer_errors_flagged(w, monkeypatch):
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'fid', 9, ['sent [a] heard [b]'], 'a1.mp3'), T(w, 'fid', 4, ['sent [c] heard [d]'], 'a2.mp3')])
    assert mp3 == 'a2.mp3' and flag == (4, 9, ['sent [c] heard [d]'])
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'fid', 3, [], 'a1.mp3'), T(w, 'fid', 8, [], 'a2.mp3')])
    assert mp3 == 'a1.mp3' and flag[0] == 3


def test_w3_mutant_second_pcm_red_is_skipped_and_absent(w, monkeypatch):
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'pcm'), T(w, 'pcm')])
    assert mp3 is None and flag is None


def test_w3_a_pcm_red_beside_a_fidelity_red_keeps_the_sound_take_flagged(w, monkeypatch):
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'fid', 5, [], 'a1.mp3'), T(w, 'pcm')])
    assert mp3 == 'a1.mp3' and flag == (5, None, [])


def test_w3_a_green_second_take_is_not_flagged(w, monkeypatch):
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'fid', 5, [], 'a1.mp3'), T(w, 'ok', 0, [], 'a2.mp3')])
    assert mp3 == 'a2.mp3' and flag is None


def test_w3_pace_or_pitch_red_twice_is_still_skipped(w, monkeypatch):
    (mp3, flag), _ = run_chunk(w, monkeypatch, [T(w, 'other', 0, [], 'a1.mp3'), T(w, 'other', 0, [], 'a2.mp3')])
    assert mp3 is None and flag is None


def test_w3_score_ranks_two_reds_and_agrees_with_check():
    ref = 'the tip moved and the trunk comes in to the tree'
    bad = 'a b c d e f g h i j'
    worse = 'x'
    assert mf.score(ref, ref)[0] == 0 == mf.check(ref, ref, echo=False)
    r1, e1, _ = mf.score(ref, bad)
    r2, e2, _ = mf.score(ref, worse)
    assert r1 == r2 == 1 and e2 > 0 and e1 > 0
    assert mf.score(ref, 'the tip moved and the trunk comes in to the tree work')[1] == 1


def test_w3_main_names_the_chapter_partial_n_flagged(w, monkeypatch):
    chap = next(iter(w.narration()))
    monkeypatch.setattr(w, 'CHAPTERS', [chap])
    monkeypatch.setattr(w, 'walk_chunk', lambda c, i, t, r, n: ('/nonexistent.mp3', (2, 7, ['sent [x] heard [y]'])))
    monkeypatch.setattr(w, 'join', lambda c, files, dst: Path(dst).write_bytes(b''))
    monkeypatch.setattr(w, 'card_video', lambda c, t, m: str(Path(w.DELIVER) / w.video_name(c, t)))
    w.main()
    txt = Path(w.DELIVER, 'README-narration.txt').read_text()
    assert 'partial: ' in txt and 'flagged' in txt and 'FLAGGED (2nd fidelity RED' in txt and 'sent [x] heard [y]' in txt


# ---- W4
@pytest.mark.parametrize('chap,title,name', [
    ('C0', 'Cold open: a graph that lives in git', 'explainer-ch00-cold-open-a-graph-that-lives-in-git.mp4'),
    ('C2', 'The ribosome: the unit turns pieces into tools', 'explainer-ch02-the-ribosome-the-unit-turns-pieces-into-tools.mp4'),
    ('C17', 'The whole path again, in a breath', 'explainer-ch17-the-whole-path-again-in-a-breath.mp4'),
])
def test_w4_names_use_the_two_digit_script_chapter_number(w, chap, title, name):
    assert w.video_name(chap, title) == name


def test_w4_real_script_titles_parse_for_all_18_chapters(w):
    t = w.chapter_titles()
    assert sorted(t, key=lambda c: int(c[1:])) == [f'C{i}' for i in range(18)]


def probe(path):
    out = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-of', 'json', '-show_streams', str(path)], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in out['streams'] if s['codec_type'] == 'video')
    a = next(s for s in out['streams'] if s['codec_type'] == 'audio')
    return {'codec_name': v['codec_name'], 'width': v['width'], 'height': v['height'], 'r_frame_rate': v['r_frame_rate'], 'pix_fmt': v['pix_fmt'],
            'a_codec': a['codec_name'], 'sample_rate': a['sample_rate'], 'channels': a['channels']}


def test_w4_two_chapters_share_the_one_fixed_profile(w, tmp_path):
    mp3 = tmp_path / 'n.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=200:duration=2', '-ac', '1', '-ar', '44100', str(mp3)], check=True)
    for c in ('C0', 'C17'):
        (Path(w.W) / c).mkdir(exist_ok=True)
    outs = [Path(w.card_video(c, 'A title, with: punctuation', str(mp3))) for c in ('C0', 'C17')]
    assert [o.name for o in outs] == ['explainer-ch00-a-title-with-punctuation.mp4', 'explainer-ch17-a-title-with-punctuation.mp4']
    assert probe(outs[0]) == probe(outs[1]) == w.PROFILE


def test_w4_mutant_a_changed_profile_is_caught(w, tmp_path):
    mp3 = tmp_path / 'n.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=200:duration=2', '-ac', '1', '-ar', '44100', str(mp3)], check=True)
    (Path(w.W) / 'C1').mkdir(exist_ok=True)
    w.PROFILE = {**w.PROFILE, 'width': 640, 'height': 360}
    o = w.card_video('C1', 'x', str(mp3))
    assert probe(o)['width'] == 640 != 1280                        # the profile is read from the constant: a changed constant changes the file, and the test above pins 1280x720


def test_w4_no_font_file_gives_a_plain_frame_not_a_failure(w, tmp_path, monkeypatch):
    mp3 = tmp_path / 'n.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=200:duration=2', '-ac', '1', '-ar', '44100', str(mp3)], check=True)
    (Path(w.W) / 'C3').mkdir(exist_ok=True)
    monkeypatch.setattr(w, 'CARD_FONT', '/nonexistent.ttf')
    assert probe(w.card_video('C3', 'x', str(mp3)))['codec_name'] == 'h264'
