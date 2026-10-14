"""goal:g7.16.1.11.41.1 -- agi-first-start BASE TIP [MSG]: the pieces a post gains or loses at its next start.

agi-post@'s ExecStartPre extracts every fenced `### piece` of engine.md and engine-[pw]*.md into ~/bin at EACH start,
so a landing that changes one reaches every post with no host act. The shipped piece (the bytes in engine-post.md,
extracted here with the same sed `sect` uses) prints `FIRST-START: <pieces>` for a range, computed from the glob the
unit itself carries (engine-root.md at each REV), never a hand list; a landing message over a non-empty set without a
`first-start:` line is refused by name. Rows (a)-(d) are the goal's falsifier 1; MUTANTS run the same rows against a
copy of the piece with one rule broken and must go RED; the last row is falsifier 2, .32's real range.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
GEO = ".agi/nodes/.geometry"
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "t",
       "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def git(repo, *a):
    return subprocess.run(["git", *a], cwd=repo, env=ENV, capture_output=True, text=True, check=True).stdout.strip()


def real_piece() -> str:
    """The shipped agi-first-start, extracted from engine-post.md exactly as the unit / `sect` extracts a piece."""
    src = (ROOT / GEO / "engine-post.md").read_text().splitlines()
    out, inp, fence = [], False, False
    for ln in src:
        if ln.startswith("### agi-first-start "):
            inp = True
            continue
        if inp and ln.startswith("##"):
            break
        if inp and ln.startswith("~~~"):
            fence = not fence
            continue
        if inp and fence:
            out.append(ln)
    assert out, "agi-first-start is not a fenced piece of engine-post.md"
    return "\n".join(out) + "\n"


def extraction_line() -> str:
    for ln in (ROOT / GEO / "engine-root.md").read_text().splitlines():
        if ln.startswith('Environment="AGI_PIECE_GLOB='):
            return ln
    raise AssertionError("the unit's extraction line is not in engine-root.md")


def piece(name, body="echo hi"):
    return f"### {name} (1 B)\n~~~sh\n{body}\n~~~\n\n"


def put(repo, name, text):
    p = repo / GEO / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


HEAD = "---\nid: config:x\n---\n# x\n\n"


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "r"
    r.mkdir()
    git(r, "init", "-q")
    put(r, "engine.md", HEAD + piece("p-zygote"))
    put(r, "engine-post.md", HEAD + piece("p-post") + piece("p-post2"))
    put(r, "engine-wrap.md", HEAD + piece("p-wrap") + piece("p-wrap2"))
    put(r, "engine-grow.md", HEAD + piece("p-grow"))
    put(r, "engine-root.md", HEAD + extraction_line() + "\n\n" + piece("p-root"))
    (r / "boxkit").mkdir()
    (r / "boxkit" / "t.tmpl").write_text("x\n")
    git(r, "add", "-A")
    git(r, "commit", "-qm", "base")
    return r


def commit(repo, msg="c"):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", msg)
    return git(repo, "rev-parse", "HEAD")


def run(script, repo, base, tip, msg=None, cwd=None):
    s = repo.parent / "afs.sh"
    s.write_text(script)
    args = ["sh", str(s), base, tip] + ([str(msg)] if msg else [])
    return subprocess.run(args, cwd=cwd or repo, env=ENV, capture_output=True, text=True)


def msgfile(repo, text):
    m = repo.parent / "msg"
    m.write_text(text)
    return m


def rows(script, repo):
    """Every row (a)-(d) + the glob rows against `script`; returns the names of the rows that FAIL."""
    base = git(repo, "rev-parse", "HEAD")
    bad = []

    def chk(name, cond):
        if not cond:
            bad.append(name)

    # (a) a range touching engine-wrap.md names that piece, and only it
    t = (repo / GEO / "engine-wrap.md")
    t.write_text(t.read_text().replace("echo hi", "echo changed", 1))
    tip = commit(repo)
    r = run(script, repo, base, tip)
    chk("a-a changed piece is named", r.stdout.strip() == "FIRST-START: p-wrap" and r.returncode == 0)
    # (b) a range deleting a fenced piece names it; adding one names it
    base2 = tip
    t.write_text(t.read_text().split("### p-wrap2")[0])
    tip = commit(repo)
    r = run(script, repo, base2, tip)
    chk("b-a deleted piece is named", r.stdout.strip() == "FIRST-START: p-wrap2")
    base3 = tip
    pst = repo / GEO / "engine-post.md"
    pst.write_text(pst.read_text() + piece("p-new"))
    tip = commit(repo)
    r = run(script, repo, base3, tip)
    chk("b-an added piece is named", r.stdout.strip() == "FIRST-START: p-new")
    # (c) only engine-root.md / engine-grow.md / boxkit -> none
    base4 = tip
    for n in ("engine-root.md", "engine-grow.md"):
        f = repo / GEO / n
        f.write_text(f.read_text().replace("echo hi", "echo other"))
    (repo / "boxkit" / "t.tmpl").write_text("y\n")
    tip = commit(repo)
    r = run(script, repo, base4, tip)
    chk("c-root, grow and boxkit only is none", r.stdout.strip() == "FIRST-START: none" and r.returncode == 0)
    # a heading-only (prose) change installs nothing: the FENCED bytes decide
    base5 = tip
    pst.write_text(pst.read_text().replace("# x\n", "# x\nprose only\n", 1))
    tip = commit(repo)
    chk("c-prose outside a fence is none", run(script, repo, base5, tip).stdout.strip() == "FIRST-START: none")
    # the glob, not a list: a NEW engine-p9.md joins [pw]*; engine-z.md does not
    base6 = tip
    put(repo, "engine-p9.md", HEAD + piece("p-nine"))
    put(repo, "engine-z.md", HEAD + piece("p-zed"))
    tip = tip_g = commit(repo)
    chk("g-a file joining the glob is covered, one outside it is not",
        run(script, repo, base6, tip).stdout.strip() == "FIRST-START: p-nine")
    # the glob must not expand against the CWD's files (SM 12:2xZ): from a checkout of BASE, which holds no
    # engine-p9.md, the pattern engine-[pw]*.md would turn into the on-disk list and miss the new file at TIP
    wt = repo.parent / "base-checkout"
    git(repo, "worktree", "add", "-q", "--detach", str(wt), base6)
    r = run(script, repo, base6, tip_g, cwd=wt / ".agi" / "nodes" / ".geometry")
    chk("g-from a checkout of BASE a new file in the glob is still named", r.stdout.strip() == "FIRST-START: p-nine")
    # (d) the landing message: refused by name without first-start:, passes with it, none needs none
    wrap = repo / GEO / "engine-wrap.md"
    base7 = tip
    wrap.write_text(wrap.read_text().replace("echo changed", "echo again", 1))
    tip = commit(repo)
    r = run(script, repo, base7, tip, msgfile(repo, "LAND x\n\nno such line\n"))
    chk("d-a landing without first-start: is refused by name",
        r.returncode == 1 and "REFUSED" in r.stdout and "p-wrap" in r.stdout)
    r = run(script, repo, base7, tip, msgfile(repo, "LAND x\n\nfirst-start: claude posts gain X, lose Y\n"))
    chk("d-with the line it passes", r.returncode == 0 and "REFUSED" not in r.stdout)
    r = run(script, repo, base7, tip, msgfile(repo, "LAND x\n\nfirst-start:\n"))
    chk("d-an empty first-start: line is not enough", r.returncode == 1)
    r = run(script, repo, base6, base6, msgfile(repo, "LAND x\n"))
    chk("d-a range with no piece change needs no line", r.returncode == 0)
    # the extraction line REWORDED (alive's probe: one extra space) -> the glob is empty at that rev. Never 'none' / rc 0:
    # rc 2 + [no-glob] naming the rev, at BASE, at TIP, and at both (a changed piece + NO first-start: line is not accepted)
    er = repo / GEO / "engine-root.md"
    keep = er.read_text()
    good = tip
    er.write_text(keep.replace('Environment="AGI_PIECE_GLOB=', 'Environment="AGI_PIECE_GLOB ='))
    reworded = commit(repo, "reword the extraction line")
    wrap.write_text(wrap.read_text().replace("echo again", "echo third", 1))
    reworded2 = commit(repo, "a box piece changes")
    r = run(script, repo, good, reworded)
    chk("n-a glob empty at TIP exits 2 [no-glob]", r.returncode == 2 and "[no-glob]" in r.stderr and "FIRST-START" not in r.stdout)
    git(repo, "checkout", "-q", reworded2)
    wrap.write_text(wrap.read_text().replace("echo third", "echo fourth", 1))
    t5 = commit(repo, "another change on the reworded line")
    r = run(script, repo, reworded, t5)
    chk("n-a glob empty at BOTH revs exits 2, not none", r.returncode == 2 and "[no-glob]" in r.stderr)
    r = run(script, repo, reworded, t5, msgfile(repo, "LAND x\n\nno such line\n"))
    chk("n-a changed piece with NO first-start: line over a reworded line is not accepted",
        r.returncode == 2 and "REFUSED" not in r.stdout and "[no-glob]" in r.stderr)
    r = run(script, repo, reworded, good)
    chk("n-a glob empty at BASE exits 2", r.returncode == 2 and "[no-glob]" in r.stderr)
    r = run(script, repo, good, good)
    chk("n-control: the unreworded line still reads", r.returncode == 0 and "FIRST-START: none" in r.stdout)
    return bad


def test_the_shipped_piece_passes_every_row(repo):
    assert rows(real_piece(), repo) == []


MUTANTS = {
    # the empty-glob guard dropped: a reworded extraction line reads as 'none', rc 0
    "no-glob-guard-dropped": ("for r in $1 $2;do [ \"$(g $r)\" ]||{ echo \"[no-glob] the extraction line is not in engine-root.md at $r\">&2;exit 2;};done\n", ""),
    # globbing left on: the pattern expands against the cwd's files, not the rev's tree
    "glob-expands-in-the-cwd": ("set -f\n", ""),
    # deletions not counted: only pieces present at TIP can be named
    "deletions-not-counted": ("s=$({ p $1;p $2;}|sort|uniq -u|cut -d' ' -f1|sort -u|tr '\\n' ' ')",
                              "T=$(p $2|cut -d' ' -f1);s=$({ p $1;p $2;}|sort|uniq -u|cut -d' ' -f1|sort -u|grep -xF \"$T\"|tr '\\n' ' ')"),
    # a hand list instead of the unit's glob (a new engine-p9.md is missed)
    "a-hand-list": ("G=$(g $1)",
                    "G='engine.md engine-post.md engine-wrap.md'"),
    # engine-root.md and engine-grow.md counted (engine*.md instead of engine-[pw]*.md)
    "root-counted": ("G=$(g $1)",
                     "G='engine*.md'"),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_a_mutant_with_one_rule_broken_goes_red(repo, name):
    old, new = MUTANTS[name]
    shipped = real_piece()
    assert old in shipped, f"the mutant {name} no longer applies: the piece changed"
    assert rows(shipped.replace(old, new), repo) != [], f"mutant {name} stayed green"


def test_a_message_check_that_never_refuses_goes_red(repo):
    shipped = real_piece()
    old = "||{ echo \"REFUSED:"
    assert old in shipped
    assert any(r.startswith("d-") for r in rows(shipped.replace(old, "||{ :;echo \"REFUSED:").replace("exit 1;}", "exit 0;}"), repo))


def test_32s_real_range_names_agi_run():
    """Falsifier 2: .32's range 6f15c681f4..f94cdee711 deleted agi-run's box-wake loop from engine-wrap.md."""
    for c in ("6f15c681f4", "f94cdee711"):
        if subprocess.run(["git", "cat-file", "-e", c + "^{commit}"], cwd=ROOT, env=ENV).returncode != 0:
            pytest.skip(f"{c} is not in this clone")
    s = Path(os.environ.get("TMPDIR", "/tmp")) / "afs-real.sh"
    s.write_text(real_piece())
    r = subprocess.run(["sh", str(s), "6f15c681f4", "f94cdee711"], cwd=ROOT, env=ENV, capture_output=True, text=True)
    s.unlink()
    assert r.returncode == 0 and r.stdout.startswith("FIRST-START: ") and "agi-run" in r.stdout.split(), r.stdout
