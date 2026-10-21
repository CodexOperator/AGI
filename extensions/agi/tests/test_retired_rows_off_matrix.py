"""A RETIRED post row (one with a `became` cell) is off the box matrix (goal:g7.16.1.11.45 G3, council 18:54Z 10-21, sp's row for the 4a review).

`box` (engine-post.md `### box`) mails a peer only when `a(sender, peer)` holds: both rows have a harness, a parent chain up to the owner, levels differing by <= 1.
A retired row that kept its parent would stay mailable: a peer's send would re-create refs/box/<peer>/<name> (mail to a dead name) and the CHECKS row refs-left would FAIL in run 2.
So for every retired row of the REAL posts.md: a(peer, name) and a(name, peer) are false for every other row, and the plain old name (the row's name without `-retired`) is off the
matrix too unless a LIVE row has taken it (G5 gives director-general-1 to the ex-DG3). Reads the REAL posts.md and the REAL a() of the box piece of this tree.
"""
import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
POSTS = REPO / ".agi" / "nodes" / ".geometry" / "posts.md"
ENGINE_POST = REPO / ".agi" / "nodes" / ".geometry" / "engine-post.md"
ROW = re.compile(r"^  - (\{.*\})\s*$", re.M)


def _a_function():
    m = re.search(r"^a\(\)\{ .*;\}$", ENGINE_POST.read_text(), re.M)
    assert m, "no a() in the box piece of engine-post.md"
    return m.group(0)


def _repo(tmp_path, posts_text):
    d = tmp_path / "r"
    d.mkdir()
    g = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-C", str(d)]
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    f = d / ".agi/nodes/.geometry/posts.md"
    f.parent.mkdir(parents=True)
    f.write_text(posts_text)
    subprocess.run([*g, "add", "-A"], check=True)
    subprocess.run([*g, "commit", "-qm", "x"], check=True)
    return d


def _adjacent(d, a, b):
    """the box piece's own a(): exit 0 = the two may mail"""
    r = subprocess.run(["sh", "-c", f'{_a_function()}\na "$1" "$2"', "sh", a, b], cwd=d, capture_output=True, text=True, timeout=60,
                       env={"PATH": "/usr/bin:/bin:/usr/local/bin", "AGI_TRUNK": "HEAD", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})
    return r.returncode == 0


def _rows(text):
    return [json.loads(m) for m in ROW.findall(text)]


def _retired(text):
    return [r for r in _rows(text) if "became" in r]


def _off_matrix_problems(d, text):
    """every way a retired row of TEXT is still mailable"""
    rows = _rows(text)
    names = [r["name"] for r in rows]
    problems = []
    for r in _retired(text):
        old = r["name"].removesuffix("-retired")
        live = old in names and "became" not in next(x for x in rows if x["name"] == old)
        for p in names:
            for who in (r["name"],) + (() if live else (old,)):
                if p != who and _adjacent(d, p, who):
                    problems.append(f"a({p}, {who}) holds")
                if p != who and _adjacent(d, who, p):
                    problems.append(f"a({who}, {p}) holds")
    return problems


def test_the_real_posts_md_has_a_retired_row_or_the_test_is_vacuous():
    assert _retired(POSTS.read_text()), "no row with a `became` cell: nothing to prove (the 4a commit adds director-general-1-retired)"


def test_every_retired_row_has_no_parent_no_engine_box_off_and_is_off_the_matrix(tmp_path):
    text = POSTS.read_text()
    for r in _retired(text):
        assert "parent" not in r and "engine" not in r and r.get("box") == "off" and r.get("boot") is None and r.get("recover") is False, r["name"]
    assert _off_matrix_problems(_repo(tmp_path, text), text) == []


@pytest.mark.parametrize("retired", ["director-general-1-retired", "director-general-2-retired"])
def test_MUTANT_a_retired_row_that_keeps_its_parent_is_mailable_and_RED(tmp_path, retired):
    text = POSTS.read_text()
    row = next(r for r in _retired(text) if r["name"] == retired)
    line = next(m for m in re.findall(r"^  - \{.*\}$", text, re.M) if json.loads(m[4:]).get("name") == row["name"])
    kept = {**{"parent": "sanctuary-master"}, **json.loads(line[4:])}      # the retired row keeping its parent
    bad = text.replace(line, "  - " + json.dumps(kept, ensure_ascii=False))
    assert bad != text
    got = _off_matrix_problems(_repo(tmp_path, bad), bad)
    assert got and all(retired in g for g in got), got


def test_the_a_function_itself_says_yes_for_two_live_peers_so_the_no_answers_above_mean_something(tmp_path):
    text = POSTS.read_text()
    assert _adjacent(_repo(tmp_path, text), "director-science-1", "director-review"), "the real a() no longer lets two level-3 posts mail"


@pytest.mark.parametrize("old", ["director-general-1", "director-general-2"])
@pytest.mark.parametrize("peer", ["director-review", "director-goals-1", "director-science-1", "sanctuary-master", "director-general-5"])
def test_a_send_to_the_old_name_is_off_matrix_for_a_peer_while_no_live_row_has_it(tmp_path, peer, old):
    text = POSTS.read_text()
    if old in [r["name"] for r in _rows(text)]:
        pytest.skip(f"a live row took the name {old} (G5/G6)")
    assert not _adjacent(_repo(tmp_path, text), peer, old)
