"""goal:g5.4.2 M5: the HTML explainer's checks, each with its mutant (council 11:57Z: audio resolves against the Drive layout; the bare-number check covers prose only;
excerpts and chips keep their digits). The page is built ONCE from the real script at the real sha, in the real repo; every mutant edits a copy of that page."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_html as mh  # noqa: E402

REPO = str(HERE.parents[2])
SCRIPT = REPO + "/.agi/context/media/season3-explainer-script.md"
from media_base import BASE  # noqa: E402

AUDIO = BASE + "/deliver"


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


def test_the_reading_measure_is_capped_at_60ch_but_pre_ex_stays_wide(page):
    """SM 11-12: prose inside the 62rem bytes/details boxes must not run to ~110 chars; excerpts (pre.ex) keep the wide box."""
    css = re.search(r"<style[^>]*>(.*?)</style>", page, re.S).group(1)
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
    def cap(sel):
        return [d for s_, d in rules if sel in [x.strip() for x in s_.split(",")] and "max-width:60ch" in d.replace(" ", "")]
    for sel in (".bytes p", "details>summary", "details>p"):
        assert cap(sel), sel
    assert not any("pre.ex" in s_ and "max-width" in d for s_, d in rules)
    # the wide half, blind-spot closed (aio+sp 11-13): a rule that reaches pre.ex UNNAMED (e.g. details>*) stays out
    capped = {x.strip() for s_, d in rules if "max-width:60ch" in d.replace(" ", "") for x in s_.split(",")}
    assert capped == {"article>*", ".how", ".bytes p", "details>summary", "details>p"}, capped


def _width_decls(html):
    """Every (selector, prop, value) width declaration in every style block; comments stripped, property names case-folded."""
    got = set()
    for css in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I):
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            for prop, val in re.findall(r"(?:^|;)\s*((?:min-|max-)?(?:width|inline-size))\s*:\s*([^;]+)", body, re.I):
                for x in sel.split(","):
                    got.add((x.strip(), prop.lower(), val.strip()))
    return got


WIDTHS = {(".wrap", "max-width", "76rem"), (".how", "max-width", "60ch"), ("article>*", "max-width", "60ch"),
          ("article>.bytes", "max-width", "62rem"), ("article>details", "max-width", "62rem"),
          (".bytes p", "max-width", "60ch"), ("details>summary", "max-width", "60ch"), ("details>p", "max-width", "60ch"),
          ("audio", "width", "100%"), ("audio", "max-width", "34rem"),
          ("h1", "max-width", "15ch"), ("h2", "max-width", "24ch"), (".lede", "max-width", "34ch")}


def test_every_width_declaration_is_known(page):
    """L557 touch (alive+aio 11-13): the exact set of width-bearing declarations (width, min/max-width, inline-size, any value, any selector) on the page.
    NOT covered, named: a rendered-width check (the owner's call); grid/flex/columns/padding; anything but the page's own CSS/markup/script.
    Covers width declarations ONLY, not grid/flex/columns/padding. One style block, no style= attribute, no link tag, one script byte-equal to media_html.JS, every pre exactly class="ex" in a known parent, no @import, so a new one is RED."""
    tags = re.findall(r"<[a-zA-Z](?:[^>\"']|\"[^\"]*\"|'[^']*')*>", page)   # quote-aware: a '>' inside an attribute value does not end the tag            # markup only: excerpt text is escaped, so 'f(x, style=1)' in code is no tag
    assert len(re.findall(r"<style\b", page, re.I)) == 1
    assert not [t for t in tags if re.search(r"\sstyle\s*=", t, re.I)]
    assert not [t for t in tags if re.match(r"<link\b", t, re.I)]            # no stylesheet link
    scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", page, re.S | re.I)  # the page's one handler script; it must never set a width or a style
    assert len(scripts) == 1 and len(re.findall(r"<script\b", page, re.I)) == 1
    assert scripts[0].strip() == mh.JS.strip()   # byte-exact: closes className/classList/style/inline-size/'sty'+'le' in the script, whatever the spelling
    assert "@import" not in page.split("<style", 1)[1].split("</style>", 1)[0].lower()
    got = _width_decls(page)
    assert got == WIDTHS, (got - WIDTHS, WIDTHS - got)


class _Pre(HTMLParser):
    def __init__(self):
        super().__init__(); self.st = []; self.pres = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "pre":
            self.pres.append((a.get("class"), tuple((t, c.get("class")) for t, c in self.st[-3:])))
        if tag not in ("br", "img", "meta", "link", "input", "source", "hr"):
            self.st.append((tag, a))
    def handle_endtag(self, tag):
        for i in range(len(self.st) - 1, -1, -1):
            if self.st[i][0] == tag:
                del self.st[i:]
                break


PRE_PARENTS = {(("article", None), ("section", "bytes"), ("details", "ev")), (("div", "wrap"), ("article", None), ("details", "ev")),
               (("article", None), ("section", "bytes"), ("figure", None))}


def test_every_pre_is_class_ex_in_a_known_parent(page):
    """Pins the class/position routes: class="ex how" / "ex lede" or a pre.ex under any other parent (article>pre) would take a cap or a width the row does not see."""
    h = _Pre(); h.feed(page)
    assert h.pres and all(c == "ex" for c, _ in h.pres)
    assert {path for _, path in h.pres} <= PRE_PARENTS


@pytest.mark.parametrize("pre_edit", [
    lambda p: p.replace('<pre class="ex"', '<pre class="ex how"', 1),
    lambda p: p.replace('<pre class="ex"', '<pre class="ex lede"', 1),
    lambda p: p.replace("</article>", '<pre class="ex">x</pre></article>', 1),
], ids=["ex-how", "ex-lede", "pre-under-article"])
def test_a_pre_class_or_position_change_is_red(page, pre_edit):
    bad = pre_edit(page)
    assert bad != page
    with pytest.raises(AssertionError):
        test_every_pre_is_class_ex_in_a_known_parent(bad)


@pytest.mark.parametrize("edit", [
    lambda p: p.replace("details>p{max-width:60ch}", "details>*{max-width:40rem}"),
    lambda p: p.replace("pre.ex{margin", ".ev pre{width:60ch}pre.ex{margin", 1),
    lambda p: p.replace("pre.ex{margin", ".ev pre{max-inline-size:60ch}pre.ex{margin", 1),
    lambda p: p.replace("pre.ex{margin", ".ev pre{MAX-WIDTH:40rem}pre.ex{margin", 1),
    lambda p: p.replace("pre.ex{margin", "pre.ex{color:red;/*x*/max-width:40rem;margin", 1),
    lambda p: p.replace("pre.ex{margin", "pre.ex{/*x*/max-width:40rem;margin", 1),
    lambda p: p.replace("</head>", "<style>pre.ex{max-width:40rem}</style></head>", 1),
    lambda p: p.replace('<pre class="ex"', '<pre style="max-width:40rem" class="ex"', 1),
    lambda p: p.replace("</head>", '<link rel="stylesheet" href="x.css"></head>', 1),
    lambda p: p.replace("pre.ex{margin", "@import 'x.css';pre.ex{margin", 1),
    lambda p: p.replace("</body>", "<script>document.querySelector('pre').style.maxWidth='40rem'</script></body>", 1),
    lambda p: p.replace("(function(){try{", "(function(){try{document.querySelector('pre').style.maxWidth='40rem';", 1),
    lambda p: p.replace("(function(){try{", "(function(){try{document.querySelector('pre').className='x';", 1),
    lambda p: p.replace("(function(){try{", "(function(){try{document.querySelector('pre')['sty'+'le'].maxWidth='40rem';", 1),
    lambda p: p.replace('<pre class="ex"', '<pre title="a>b" style="max-width:40rem" class="ex"', 1),
], ids=["star", "width", "inline-size", "case", "comment-mid", "comment-first", "second-style", "attr", "link", "import", "script2", "script-in-place", "className", "concat", "quoted-gt"])
def test_a_respelled_width_rule_is_red(page, edit):
    bad = edit(page)
    assert bad != page
    try:
        test_every_width_declaration_is_known(bad)
    except AssertionError:
        return
    raise AssertionError("respelling passed")


def test_a_style_equals_quoted_in_an_excerpt_is_not_a_style_attribute(page):
    bad = page.replace("</code></pre>", " f(x, style=1)</code></pre>", 1)
    assert bad != page
    test_every_width_declaration_is_known(bad)
