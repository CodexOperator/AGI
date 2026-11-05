#!/usr/bin/env python3
"""goal:g5.4.2 M5, the HTML explainer. 0 provider spend, no render.
  media_html.py build SCRIPT.md REPO OUT.html     one self-contained page from the M2 script (same sha, same 18 chapters)
  media_html.py check PAGE.html REPO AUDIO_DIR    the page checks below, against the Drive layout (page in html/, the mp3s one level up)
The page: per chapter the narration as readable paragraphs; each [Cn.k] tag becomes a cite chip that opens the pair's claim, its file and line at the sha
and the BYTE-EXACT excerpt with the needle marked; the chapter's `### html` text and its @@excerpt blocks follow; an <audio> names the chapter's mp3.
No CDN, no web font, no external request: everything is inline. Council 11:57Z amendments: (1) audio src resolves against the DRIVE layout
(the watcher sorts *.html -> html/ and the mp3s stay at the top: src='../season3-CNN-narration.mp3'), the page's first line says to download the folder
and open it locally; (2) the bare-number check covers prose only (slot values, chips and excerpts keep their digits); the excerpts are bound by check 1.
check prints one line per finding and `findings=N`; exit = N.
  1 excerpts_bad    every pre.ex equals `git show SHA:PATH` lines Lx-Ly, byte for byte
  2 chapters        exactly C0..C17, each once, in order
  3 bare_numbers    prose (outside slot values, chips, excerpts) has no digit and no number word
  4 untagged        every sentence span carries data-tag (a pair id list or `image`)
  5 audio           every <audio src> resolves to an existing file in the Drive layout
  6 external        no http(s):// or protocol-relative reference, no @import, no url() to anything but data:
  7 wellformed      tags nest and close
  8 first_line      the first paragraph says to download the folder and open the page locally
"""
import html as H
import os
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_fm1  # noqa: E402
import media_fm2  # noqa: E402

PAGE_NAME = "season3-explainer.html"
FIRST_LINE = "Download the folder and open season3-explainer.html on your own computer: Drive's viewer does not run a page. The audio plays from the narration files in the folder above this one."
TAG, SLOT = media_fm2.TAG, media_fm2.SLOT
SKIP = re.compile(r"^(@@excerpt|fn:|live:|uncalled:|sha:|pair )")
NUMWORDS = media_fm2.NUMWORDS


# ---- parse the script
def parse(path):
    """-> [{id, n, title, sha, fn, live, pairs{id: dict}, narration [paragraph], html [item]}]; a paragraph is the joined text, an html item is ('p', text) or ('ex', sha, path, lo, hi, body)."""
    lines = open(path, encoding="utf-8").read().split("\n")
    chaps, c, sec, fence, blk, ex = [], None, None, False, [], None

    def flush():
        if blk and c is not None and sec in ("narration", "html"):
            t = " ".join(blk)
            (c["narration"].append(t) if sec == "narration" else c["html"].append(("p", t)))
        blk.clear()

    for ln in lines:
        m = re.match(r"^## (C(\d+))\s*[·:\-]\s*(.+?)\s*$", ln)
        if m and not fence:
            flush(); sec = None
            c = {"id": m.group(1), "n": int(m.group(2)), "title": m.group(3), "sha": None, "fn": [], "live": [], "pairs": {}, "narration": [], "html": []}
            chaps.append(c); continue
        if c is None:
            continue
        if ln.startswith("~~~~"):
            if not fence:
                fence, body = True, []
            else:
                fence = False
                if ex:
                    c["html"].append(("ex", *ex, "\n".join(body))); ex = None
            continue
        if fence:
            body.append(ln); continue
        m = re.match(r"^### (narration|html)\b", ln)
        if m:
            flush(); sec = m.group(1); continue
        if re.match(r"^##+ ", ln):
            flush(); sec = None; continue
        m = re.match(r"^@@excerpt ([0-9a-f]{7,40}):(.+):L(\d+)-L(\d+)\s*$", ln)
        if m:
            flush(); ex = (m.group(1), m.group(2), int(m.group(3)), int(m.group(4))); continue
        m = re.match(r"^pair (C\d+\.\d+): (.+?) => ([0-9a-f]{7,40}):(.+):L(\d+)-L(\d+) ~ (.+)$", ln)
        if m:
            c["pairs"][m.group(1)] = {"claim": m.group(2), "sha": m.group(3), "path": m.group(4), "lo": int(m.group(5)), "hi": int(m.group(6)), "needle": m.group(7)}; continue
        m = re.match(r"^sha: ([0-9a-f]{7,40})\s*$", ln)
        if m and c["sha"] is None:
            c["sha"] = m.group(1); continue
        if ln.startswith("fn:"):
            c["fn"].append(ln[3:].strip()); continue
        if ln.startswith("live:"):
            c["live"].append(ln[5:].strip()); continue
        if sec is None or SKIP.match(ln):
            continue
        if not ln.strip():
            flush()
        else:
            blk.append(ln.strip())
    flush()
    return chaps


def lines_at(repo, sha, path, lo, hi):
    raw = media_fm1.show(repo, sha, path)
    if raw is None:
        raise ValueError(f"{sha}:{path} does not exist")
    ls = raw.decode("utf-8", "surrogateescape").split("\n")
    return "\n".join(ls[lo - 1:hi])


# ---- build
def esc(s):
    return H.escape(s, quote=True)


def prose(text, repo, sha, chap, shown):
    """One paragraph -> html: one <span class=s data-tag> per tagged sentence, slot values in <span class=slot>, a cite chip per pair."""
    parts = TAG.split(text)
    out = []
    for k in range(0, len(parts), 2):
        seg = parts[k].strip()
        tag = parts[k + 1] if k + 1 < len(parts) else "image"
        if not seg:
            continue
        body, pos = [], 0
        for m in SLOT.finditer(seg):
            body.append(esc(seg[pos:m.start()]))
            v = media_fm2.slot_value(m.group(1), m.group(2), repo, sha)
            if v is None:
                raise ValueError("unresolved slot " + m.group(0))
            body.append(f'<span class="slot">{v:,}</span>')
            pos = m.end()
        body.append(esc(seg[pos:]))
        chips = ""
        if tag != "image":
            for pid in tag.split(","):
                p = chap["pairs"][pid]
                chips += f' <a class="cite" href="#ev-{pid.replace(".", "-")}">{esc(os.path.basename(p["path"]))}, line {p["lo"]}' + (f"-{p['hi']}" if p["hi"] != p["lo"] else "") + "</a>"
        out.append(f'<span class="s" data-tag="{esc(tag)}">{"".join(body)}{chips}</span>')
    return "<p class=\"prose\">" + " ".join(out) + "</p>"


def evidence(pid, p, repo):
    txt = lines_at(repo, p["sha"], p["path"], p["lo"], p["hi"])
    i = txt.find(p["needle"])
    code = esc(txt) if i < 0 else esc(txt[:i]) + "<mark>" + esc(p["needle"]) + "</mark>" + esc(txt[i + len(p["needle"]):])
    src = f'{p["sha"]}:{p["path"]}:L{p["lo"]}-L{p["hi"]}'
    return (f'<details class="ev" id="ev-{pid.replace(".", "-")}"><summary>{esc(p["claim"])}</summary>'
            f'<p class="where">{esc(p["path"])}, line {p["lo"]}' + (f'-{p["hi"]}' if p["hi"] != p["lo"] else "") + f' at {esc(p["sha"])}</p>'
            f'<pre class="ex" data-src="{esc(src)}"><code>{code}</code></pre></details>')


def chapter_html(c, repo):
    cid = c["id"].lower()
    shown, out = set(), [f'<article id="{cid}"><h2>{esc(c["title"])}</h2>',
                         f'<audio controls preload="none" src="../season3-{c["id"]}-narration.mp3"></audio>']
    if c["fn"] or c["live"]:
        out.append('<p class="facts">' + " ".join(esc(x) + "." for x in (["The piece: " + f for f in c["fn"]] + ["Called from: " + l for l in c["live"]])) + "</p>")
    for t in c["narration"]:
        out.append(prose(t, repo, c["sha"], c, shown))
        for pid in dict.fromkeys(x for tag in TAG.findall(t) for x in tag.split(",") if x != "image"):
            if pid not in shown:
                shown.add(pid); out.append(evidence(pid, c["pairs"][pid], repo))
    if c["html"]:
        out.append("<section class=\"bytes\"><h3>At the bytes</h3>")
        for it in c["html"]:
            if it[0] == "p":
                out.append(prose(it[1], repo, c["sha"], c, shown))
                for pid in dict.fromkeys(x for tag in TAG.findall(it[1]) for x in tag.split(",") if x != "image"):
                    if pid not in shown:
                        shown.add(pid); out.append(evidence(pid, c["pairs"][pid], repo))
            else:
                _, sha, path, lo, hi, body = it
                out.append(f'<figure><pre class="ex" data-src="{esc(f"{sha}:{path}:L{lo}-L{hi}")}"><code>{esc(body)}</code></pre>'
                           f'<figcaption>{esc(os.path.basename(path))}, line {lo}' + (f'-{hi}' if hi != lo else '') + f' at {esc(sha)}</figcaption></figure>')
        out.append("</section>")
    out.append("</article>")
    return "\n".join(out)


CSS = """
:root{--ground:#eef1ef;--ground2:#e2e8e5;--ink:#14201c;--soft:#33433d;--accent:#1d4f91;--mark:#cfe3ff;color-scheme:light dark}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ground:#101614;--ground2:#18211e;--ink:#e9efec;--soft:#b7c4be;--accent:#8db8ff;--mark:#27466f}}
:root[data-theme=dark]{--ground:#101614;--ground2:#18211e;--ink:#e9efec;--soft:#b7c4be;--accent:#8db8ff;--mark:#27466f}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);font:1.125rem/1.6 Georgia,"Iowan Old Style","Times New Roman",serif}
.wrap{padding:0 16px;max-width:76rem;margin:0 auto}
@media (min-width:700px){.wrap{padding:0 32px}}
.top{padding:40px 0 64px}
.how{margin:0 0 48px;padding:16px;background:var(--ground2);max-width:46rem}
h1{font-size:clamp(2.4rem,8vw,6.5rem);line-height:.98;letter-spacing:-.03em;margin:0 0 24px;max-width:15ch}
.lede{font-size:1.4rem;line-height:1.4;max-width:34ch;margin:0 0 40px}
nav ol{columns:2 16rem;column-gap:32px;margin:0;padding-left:1.6em}
nav a{color:var(--ink);text-underline-offset:.2em}nav li{margin:0 0 .35em}
article{padding:96px 0 40px}article:nth-of-type(even){background:var(--ground2)}
article>*{max-width:46rem}article>.bytes,article>details,article>.facts{max-width:62rem}
h2{font-size:clamp(1.9rem,5vw,3.4rem);line-height:1.05;letter-spacing:-.02em;margin:0 0 24px;max-width:24ch}
h3{font-size:1.6rem;line-height:1.2;margin:48px 0 16px}
audio{display:block;width:100%;max-width:34rem;margin:0 0 24px}
.facts{color:var(--soft)}
.prose{margin:0 0 20px}
.cite{font-size:1rem;color:var(--accent);text-decoration:none;white-space:nowrap;background:var(--ground2);padding:0 .4em;border-radius:0}
article:nth-of-type(even) .cite{background:var(--ground)}
.cite:hover,.cite:focus-visible{text-decoration:underline;outline:2px solid var(--accent);outline-offset:2px}
.ev{margin:0 0 24px;padding:12px 16px;background:var(--ground2)}
article:nth-of-type(even) .ev{background:var(--ground)}
.ev summary{cursor:pointer;font-weight:700}.ev:target{outline:3px solid var(--accent)}
.where{margin:12px 0 8px;color:var(--soft)}
pre.ex{margin:0 0 8px;padding:16px;overflow:auto;background:var(--ground2);font:1rem/1.5 ui-monospace,Menlo,Consolas,monospace;white-space:pre}
.ev pre.ex{background:var(--ground2)}article:nth-of-type(even) pre.ex{background:var(--ground)}
.wrapx pre.ex{white-space:pre-wrap;word-break:break-all}
mark{background:var(--mark);color:inherit}
figure{margin:0 0 24px}figcaption{color:var(--soft)}
footer{padding:64px 0 96px;color:var(--soft)}
@media (prefers-reduced-motion:no-preference){.cite,nav a{transition:background-color .15s}}
"""

JS = """
(function(){try{
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.cite');if(!a)return;
var d=document.getElementById(a.getAttribute('href').slice(1));if(d){d.open=true;}});
var b=document.getElementById('wraptoggle');if(b){b.addEventListener('click',function(){document.body.classList.toggle('wrapx');b.setAttribute('aria-pressed',document.body.classList.contains('wrapx'));});}
if(location.hash){var d=document.getElementById(location.hash.slice(1));if(d&&d.tagName==='DETAILS')d.open=true;}
}catch(e){}})();
"""


def build(script, repo, out):
    chaps = parse(script)
    sha = chaps[0]["sha"] if chaps else "?"
    nav = "".join(f'<li><a href="#{c["id"].lower()}">{esc(c["title"])}</a></li>' for c in chaps)
    body = "\n".join(chapter_html(c, repo) for c in chaps)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The life of one node edit</title>
<meta name="description" content="One node edit followed through the engine, eighteen chapters, every sentence cited to the bytes it is about.">
<style>{CSS}</style></head>
<body><header class="top"><div class="wrap">
<p class="how">{esc(FIRST_LINE)}</p>
<h1>The life of one node edit</h1>
<p class="lede">Follow one small change through the engine, and open the exact bytes behind every sentence.</p>
<p><button id="wraptoggle" type="button" aria-pressed="false">Wrap long lines of code</button></p>
<nav aria-label="Chapters"><ol start="0">{nav}</ol></nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap"><p>Every excerpt is read from the engine at {esc(sha)} and compared with it byte for byte before this page is delivered.</p></div></footer>
<script>{JS}</script>
</body></html>
"""
    open(out, "w", encoding="utf-8").write(page)
    return page


# ---- check
class P(HTMLParser):
    VOID = {"meta", "br", "img", "input", "link", "hr", "source"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.bad, self.articles, self.audio, self.ex, self.refs = [], [], [], [], [], []
        self.prose_text, self.first_p, self.untagged, self.cur_ex, self.skip_depth = [], None, [], None, []
        self.in_p, self.in_s, self.ctx = False, False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ("src", "href"):
            if a.get(k) and (re.match(r"^(https?:)?//", a[k]) or a[k].startswith("ftp:")):
                self.refs.append(a[k])
        if tag not in self.VOID:
            self.stack.append(tag)
        cls = (a.get("class") or "").split()
        if tag == "article":
            self.articles.append(a.get("id"))
        elif tag == "audio":
            self.audio.append(a.get("src"))
        elif tag == "pre" and "ex" in cls:
            self.cur_ex = {"src": a.get("data-src"), "text": []}
        elif tag == "p":
            self.in_p = True
            if "prose" in cls:
                self.ctx.append("prose")
            elif self.first_p is None:
                self.first_p = []
        elif tag == "span" and "s" in cls:
            self.in_s = True
            if a.get("data-tag") is None:
                self.untagged.append(a.get("class"))
        if tag == "span" and "slot" in cls or tag == "a" and "cite" in cls or tag == "style" or tag == "script":
            self.skip_depth.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.bad.append(f"</{tag}> closes {self.stack[-1] if self.stack else 'nothing'}")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()
        if self.skip_depth and tag in ("span", "a", "style", "script") and self.skip_depth[-1] == tag:
            self.skip_depth.pop()
        if tag == "pre" and self.cur_ex is not None:
            self.ex.append(self.cur_ex); self.cur_ex = None
        if tag == "p":
            self.in_p = False
            if self.ctx and self.ctx[-1] == "prose":
                self.ctx.pop(); self.prose_text.append("\n")
            elif self.first_p is not None and not isinstance(self.first_p, str):
                self.first_p = " ".join(self.first_p)
        if tag == "span":
            self.in_s = False

    def handle_data(self, d):
        if self.cur_ex is not None:
            self.cur_ex["text"].append(d)
        elif self.ctx and self.ctx[-1] == "prose" and not self.skip_depth:
            self.prose_text.append(d)
        elif self.first_p is not None and not isinstance(self.first_p, str) and self.in_p:
            self.first_p.append(d)


def check(page, repo, audio_dir, echo=True):
    """-> list of findings (empty = GREEN). audio_dir holds the mp3s; the page is placed in <layout>/html/ and each src resolved there."""
    p = P(); p.feed(open(page, encoding="utf-8").read()); p.close()
    raw = open(page, encoding="utf-8").read()
    f = []
    bad = []
    for e in p.ex:
        m = re.match(r"^([0-9a-f]{7,40}):(.+):L(\d+)-L(\d+)$", e["src"] or "")
        if not m:
            bad.append(f"excerpt without a source: {e['src']!r}"); continue
        try:
            want = lines_at(repo, m.group(1), m.group(2), int(m.group(3)), int(m.group(4)))
        except ValueError as x:
            bad.append(str(x)); continue
        if "".join(e["text"]) != want:
            bad.append(f"excerpt {e['src']} differs from the engine at that sha")
    f += [("excerpts_bad", x) for x in bad]
    want_ids = [f"c{i}" for i in range(18)]
    if p.articles != want_ids:
        f.append(("chapters", f"found {p.articles}, want c0..c17 in order"))
    text = "".join(p.prose_text)
    hits = re.findall(r"\d+", text) + [t for t in re.findall(r"[a-z]+", text.lower()) if t in NUMWORDS]
    if hits:
        f.append(("bare_numbers", " ".join(hits[:8])))
    if p.untagged:
        f.append(("untagged", f"{len(p.untagged)} sentence spans without data-tag"))
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(f"{t}/html")
        for src in p.audio:
            if not src or re.match(r"^[a-z]+:", src):
                f.append(("audio", f"unusable src {src!r}")); continue
            # the Drive layout: page in html/, the mp3s at the top; the file must exist in AUDIO_DIR under the name the src points at
            target = os.path.normpath(os.path.join(f"{t}/html", src))
            if os.path.dirname(target) != t or not os.path.exists(os.path.join(audio_dir, os.path.basename(target))):
                f.append(("audio", f"{src} does not resolve in the Drive layout (html/ beside the mp3s one level up)"))
    ext = p.refs + re.findall(r"@import|url\((?!['\"]?data:)", raw)
    if ext:
        f.append(("external", ", ".join(ext[:4])))
    if p.bad or p.stack:
        f.append(("wellformed", "; ".join(p.bad[:3]) or f"unclosed {p.stack[-3:]}"))
    if (p.first_p if isinstance(p.first_p, str) else "") != FIRST_LINE:
        f.append(("first_line", f"first paragraph is {p.first_p!r}"))
    if echo:
        print(f"excerpts={len(p.ex)} chapters={len(p.articles)} audio={len(p.audio)}")
        for k, v in f:
            print(f"  {k}: {v}")
        print(f"findings={len(f)}")
    return f


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 4 and a[0] == "build":
        build(a[1], a[2], a[3]); print("wrote", a[3])
    elif len(a) == 4 and a[0] == "check":
        sys.exit(len(check(a[1], a[2], a[3])))
    else:
        sys.exit(__doc__)
