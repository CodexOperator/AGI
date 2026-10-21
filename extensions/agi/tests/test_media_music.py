"""goal:g5.4.2 M6: the music sample runner and its mutants. No request is sent: urlopen is a stub that returns a canned SSE stream."""
import base64
import importlib
import json
import subprocess
import sys
import urllib.error
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


@pytest.fixture
def m(tmp_path, monkeypatch):
    monkeypatch.setenv('MUSIC_DIR', str(tmp_path / 'music')); monkeypatch.setenv('MUSIC_DELIVER', str(tmp_path / 'deliver'))
    sys.modules.pop('media_music', None)
    mm = importlib.import_module('media_music')
    mm.STOP.clear(); mm.SENT.clear()
    return mm


def mp3(tmp_path, secs):
    p = tmp_path / f't{secs}.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=300', '-t', str(secs), '-b:a', '64k', str(p)], check=True)
    return p.read_bytes()


def sse(data):
    b64 = base64.b64encode(data).decode()
    cut = len(b64) // 3
    ch = lambda d: ('data: ' + json.dumps({'choices': [{'delta': d}]}) + '\n').encode()
    return [ch({'content': '[0.0:4.0] la'}), ch({'audio': {'data': b64[:cut]}}), ch({'audio': {'data': b64[cut:]}}), b'data: [DONE]\n']


def stub(mm, monkeypatch, outcomes):
    calls = []
    def fake(req, timeout=0):
        calls.append(json.loads(req.data))
        o = outcomes[len(calls) - 1]
        if isinstance(o, Exception):
            raise o
        return iter(o)
    monkeypatch.setattr(mm.urllib.request, 'urlopen', fake)
    return calls


def test_a_valid_30_s_stream_is_written_644_to_deliver(m, monkeypatch, tmp_path):
    calls = stub(m, monkeypatch, [sse(mp3(tmp_path, 30))])
    st, note = m.sample('k', 'a', 'swing-flamenco', m.PROMPTS[0][2])
    assert st == 'ok', note
    out = Path(m.DELIVER, 'music-sample-a-swing-flamenco.mp3')
    assert out.exists() and oct(out.stat().st_mode & 0o777) == '0o644'
    b = calls[0]
    assert b['stream'] is True and b['model'] == 'google/lyria-3-clip-preview' and b['modalities'] == ['text', 'audio']


def test_the_real_prompts_pass_their_own_guard_and_name_no_artist(m):
    assert len(m.PROMPTS) == 3
    for _, _, p in m.PROMPTS:
        assert m.guard(p) == [] and 'bpm' in p and 'Instrumental' in p


@pytest.mark.parametrize('name', ['Delinquent Habits', 'Balkan Beat Box', 'Return of the Tres', 'Hermetico', 'in the style of a famous band', 'SOUNDS LIKE the radio'])
def test_mutant_a_named_reference_is_refused_before_any_send(m, monkeypatch, name):
    calls = stub(m, monkeypatch, [sse(b'x')])
    st, note = m.sample('k', 'a', 's', f'Instrumental swing, {name}, 150 bpm')
    assert st == 'refused' and calls == [] and m.SENT == []
    assert not Path(m.M, 'walk-requests-music.log').exists()


def test_mutant_a_503_stops_after_one_request_with_no_retry(m, monkeypatch):
    calls = stub(m, monkeypatch, [urllib.error.HTTPError('u', 503, 'x', {}, __import__('io').BytesIO(b'e')), [b'never']])
    st, _ = m.sample('k', 'a', 's', m.PROMPTS[0][2])
    assert st == 'stopped' and len(calls) == 1 and m.STOP == ['http']


def test_mutant_a_timeout_stops_clean_too(m, monkeypatch):
    stub(m, monkeypatch, [TimeoutError('t')])
    assert m.sample('k', 'a', 's', m.PROMPTS[0][2])[0] == 'stopped' and m.STOP == ['http']


def test_mutant_a_fourth_request_is_refused(m, monkeypatch, tmp_path):
    data = mp3(tmp_path, 30)
    calls = stub(m, monkeypatch, [sse(data)] * 4)
    assert [m.sample('k', c, 's' + c, m.PROMPTS[0][2])[0] for c in 'abc'] == ['ok'] * 3
    st, note = m.sample('k', 'd', 'sd', m.PROMPTS[0][2])
    assert st == 'refused' and len(calls) == 3 and 'hard limit' in note


def test_mutant_a_12_s_stream_is_red_and_kept_out_of_deliver(m, monkeypatch, tmp_path):
    stub(m, monkeypatch, [sse(mp3(tmp_path, 12))])
    st, _ = m.sample('k', 'a', 's', m.PROMPTS[0][2])
    assert st == 'red'
    assert not list(Path(m.DELIVER).glob('music-sample-*'))


def test_mutant_an_empty_or_junk_stream_is_red(m, monkeypatch):
    stub(m, monkeypatch, [[b'data: [DONE]\n']])
    assert m.sample('k', 'a', 's', m.PROMPTS[0][2])[0] == 'red'


def test_the_request_is_logged_before_it_is_sent(m, monkeypatch, tmp_path):
    seen = []
    log = Path(m.M, 'walk-requests-music.log')
    data = mp3(tmp_path, 30)
    def fake(req, timeout=0):
        seen.append(log.read_text().count('\n'))
        return iter(sse(data))
    monkeypatch.setattr(m.urllib.request, 'urlopen', fake)
    m.sample('k', 'a', 's', m.PROMPTS[0][2])
    assert seen == [1]
    rec = json.loads(log.read_text().splitlines()[0])
    assert rec['n'] == 1 and len(rec['prompt_sha256']) == 64 and 'key' not in json.dumps(rec).lower().replace('keyfile', '')


def test_main_writes_a_readme_with_every_prompt_and_stops_clean_on_http(m, monkeypatch, tmp_path):
    data = mp3(tmp_path, 30)
    keydir = tmp_path / 'home' / 'keys'; keydir.mkdir(parents=True); (keydir / 'k.key').write_text('secret\n')
    monkeypatch.setenv('HOME', str(tmp_path / 'home'))
    stub(m, monkeypatch, [sse(data), urllib.error.HTTPError('u', 500, 'x', {}, __import__('io').BytesIO(b'e'))])
    m.main('k.key')
    txt = Path(m.DELIVER, 'README-music.txt').read_text()
    assert 'music-sample-a-swing-flamenco.mp3: ready' in txt and 'stopped: http' in txt and 'c2pa' in txt and 'secret' not in txt
    assert not Path(m.DELIVER, 'music-sample-c-trombone-flamenco-jazz.mp3').exists()


# ---- council 12:06Z edits
GOAL = HERE.parents[2] / '.agi/nodes/goal/g5.4.2.md'


def direction_names():
    """The song titles and artists in the goal's music direction line, FOUND BY MATCH (never a line number)."""
    import re
    line = next(l for l in GOAL.read_text(encoding='utf-8').split('\n') if re.search(r'music video\. Direction:', l))
    titles = re.findall(r'"([^"]+)"', line)
    artists = re.findall(r'by ([A-Z][A-Za-z ]+?)(?: and |\.|,|$)', line)
    return [x.lower() for x in titles + artists]


def test_the_four_names_are_pinned_in_the_code_guard(m):
    for n in ('return of the tres', 'delinquent habits', 'hermetico', 'balkan beat box', 'in the style of'):
        assert n in m.GUARD


def test_every_name_in_the_goals_direction_line_is_in_the_guard(m):
    names = direction_names()
    assert len(names) == 4, names                                 # two titles, two artists: the match found them all
    assert [n for n in names if n not in m.GUARD] == []


def test_mutant_a_name_missing_from_the_guard_is_red(m):
    m.GUARD.remove('balkan beat box')
    assert [n for n in direction_names() if n not in m.GUARD] == ['balkan beat box']


def test_prompt_b_balkan_brass_swing_passes_but_the_band_name_is_refused(m, monkeypatch):
    assert m.guard(m.PROMPTS[1][2]) == []
    calls = stub(m, monkeypatch, [sse(b'x')])
    assert m.sample('k', 'b', 's', 'Instrumental, Balkan Beat Box brass, 160 bpm')[0] == 'refused' and calls == []


def test_readme_says_sample_c_is_instrumental_with_a_wordless_crowd_shout_and_why(m, monkeypatch, tmp_path):
    data = mp3(tmp_path, 30)
    keydir = tmp_path / 'home' / 'keys'; keydir.mkdir(parents=True); (keydir / 'k.key').write_text('secret\n')
    monkeypatch.setenv('HOME', str(tmp_path / 'home'))
    stub(m, monkeypatch, [sse(data)] * 3)
    m.main('k.key')
    txt = Path(m.DELIVER, 'README-music.txt').read_text()
    assert 'instrumental with a wordless crowd shout' in txt
    assert 'music VIDEO is its own piece' in txt and 'Three of Three' in txt and "owner's pick" in txt and '$0.08' in txt
    assert 'a bed under the narration' in txt and 'is the real reason' not in txt
