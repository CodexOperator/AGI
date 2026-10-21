"""goal:g5.4.2 M5: the HTML explainer's checks, each with its mutant (council 11:57Z: audio resolves against the Drive layout; the bare-number check covers prose only;
excerpts and chips keep their digits). The page is built ONCE from the real script at the real sha, in the real repo; every mutant edits a copy of that page."""
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_html as mh  # noqa: E402

REPO = str(HERE.parents[2])
SCRIPT = REPO + "/.agi/context/media/season3-explainer-script.md"
AUDIO = "/data/work/director-general-3-media/season3/deliver"


@pytest.fixture(scope="module")
def page(tmp_path_factory):
    out = tmp_path_factory.mktemp("m5") / "season3-explainer.html"
    mh.build(SCRIPT, REPO, str(out))
    return out.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def audio(tmp_path_factory):
    d = tmp_path_factory.mktemp("mp3")
    for i in range(18):
        (d / f"season3-C{i}-narration.mp3").write_bytes(b"x")
    return str(d)


def run(tmp_path, text, audio):
    p = tmp_path / "p.html"
    p.write_text(text, encoding="utf-8")
    return [k for k, _ in mh.check(str(p), REPO, audio, echo=False)]


def test_the_real_page_is_green(page, tmp_path, audio):
    assert run(tmp_path, page, audio) == []


def test_the_page_has_no_raw_tags_or_slots_left(page):
    assert "{{" not in page and not re.search(r"\[C\d+\.\d+", page) and "[image]" not in page


def test_excerpts_and_chips_keep_their_digits_and_stay_green(page, tmp_path, audio):
    ex = re.findall(r'<pre class="ex"[^>]*><code>(.*?)</code></pre>', page, re.S)
    assert any(re.search(r"\d", e) for e in ex)                   # a digit inside an excerpt is byte-exact, so GREEN
    assert re.search(r'class="cite"[^>]*>[^<]*line \d+', page)    # chips name a line number
    assert re.search(r'<span class="slot">[\d,]+</span>', page)   # a slot value is a digit span
    assert run(tmp_path, page, audio) == []


# ---- the mutants
def test_mutant_one_byte_changed_in_an_excerpt_is_red(page, tmp_path, audio):
    m = re.search(r'(<pre class="ex"[^>]*><code>)([^<]{20,})', page)
    bad = page[:m.end(1)] + m.group(2)[:5] + ("X" if m.group(2)[5] != "X" else "Y") + m.group(2)[6:] + page[m.end(2):]
    assert "excerpts_bad" in run(tmp_path, bad, audio)


def test_mutant_a_dropped_chapter_is_red(page, tmp_path, audio):
    bad = re.sub(r'<article id="c9">.*?</article>', "", page, flags=re.S)
    assert "chapters" in run(tmp_path, bad, audio)


def test_mutant_a_chapter_out_of_order_is_red(page, tmp_path, audio):
    a = re.search(r'<article id="c3">.*?</article>', page, re.S).group(0)
    b = re.search(r'<article id="c4">.*?</article>', page, re.S).group(0)
    assert "chapters" in run(tmp_path, page.replace(a, "@@A").replace(b, a).replace("@@A", b), audio)


def test_mutant_a_47_typed_into_a_narration_paragraph_is_red(page, tmp_path, audio):
    bad = page.replace('<p class="prose">', '<p class="prose">It has a default of 47 percent. ', 1)
    assert "bare_numbers" in run(tmp_path, bad, audio)


def test_mutant_a_number_word_in_prose_is_red(page, tmp_path, audio):
    bad = page.replace('<p class="prose">', '<p class="prose">Forty seven of them. ', 1)
    assert "bare_numbers" in run(tmp_path, bad, audio)


def test_mutant_a_sentence_without_its_tag_is_red(page, tmp_path, audio):
    bad = page.replace('<span class="s" data-tag="image">', '<span class="s">', 1)
    assert "untagged" in run(tmp_path, bad, audio)


def test_mutant_bare_audio_src_under_html_is_red_on_the_drive_layout(page, tmp_path, audio):
    bad = page.replace('src="../season3-C2-narration.mp3"', 'src="season3-C2-narration.mp3"')
    assert "audio" in run(tmp_path, bad, audio)


def test_mutant_audio_for_a_missing_file_is_red(page, tmp_path, audio):
    bad = page.replace("../season3-C5-narration.mp3", "../season3-C5-narration-final.mp3")
    assert "audio" in run(tmp_path, bad, audio)


@pytest.mark.parametrize("ins", ['<script src="https://cdn.example/x.js"></script>', '<link rel="stylesheet" href="//fonts.example/x.css">',
                                 '<style>@import "x.css";</style>', '<style>a{background:url(x.png)}</style>'])
def test_mutant_any_external_reference_is_red(page, tmp_path, audio, ins):
    assert "external" in run(tmp_path, page.replace("</head>", ins + "</head>"), audio)


def test_mutant_an_unclosed_tag_is_red(page, tmp_path, audio):
    assert "wellformed" in run(tmp_path, page.replace("</article>", "", 1), audio)


def test_mutant_without_the_download_line_is_red(page, tmp_path, audio):
    assert "first_line" in run(tmp_path, page.replace(mh.esc(mh.FIRST_LINE), "Welcome."), audio)


def test_the_audio_names_follow_the_chapter_numbers(page):
    assert [f"../season3-C{i}-narration.mp3" for i in range(18)] == re.findall(r'src="(\.\./season3-C\d+-narration\.mp3)"', page)
