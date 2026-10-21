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


@pytest.mark.parametrize("retired", ["director-general-1-retired", "director-general-2-retired", "director-general-3-retired", "director-general-4-retired"])
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


OLD_NAMES = ["director-general-1", "director-general-2", "director-general-3", "director-general-4"]      # 1, 2 reused (G5, G6); 3 free until G7; 4 free for good


@pytest.mark.parametrize("old", OLD_NAMES)
@pytest.mark.parametrize("peer", ["director-review", "director-goals-1", "director-science-1", "sanctuary-master", "director-general-5"])
def test_a_send_to_an_old_name_is_off_matrix_while_no_live_row_has_it_and_reaches_the_new_holder_once_one_does(tmp_path, peer, old):
    """G3-G6 freed the names director-general-1..4; G5/G6 reuse the first two, G7 the third. Free: off the matrix. Reused (G5, G6): the live row says `was` = the previous
    holder, its `-retired` row of the EARLIER holder stays off the matrix, and a send to the name reaches the new holder. No skip: either leg is asserted."""
    text = POSTS.read_text()
    rows = {r["name"]: r for r in _rows(text)}
    repo = _repo(tmp_path, text)
    if old not in rows:
        assert not _adjacent(repo, peer, old)
        return
    live = rows[old]
    assert live.get("was") and "became" not in live, live
    assert f"{live['was']}-retired" in rows and rows[f"{live['was']}-retired"].get("became") == old, "the previous holder's retired row names the reuse"
    assert not any(k in rows[f"{live['was']}-retired"] for k in ("parent", "engine")), "its retired row stays off the matrix"
    assert _adjacent(repo, peer, old), "mail to the reused name reaches the new holder: it is a live level-3 row like any other peer's"


def test_the_reused_name_director_general_1_is_a_live_row_that_was_director_general_3_once_g5_has_landed(tmp_path):
    rows = {r["name"]: r for r in _rows(POSTS.read_text())}
    assert rows["director-general-1"]["was"] == "director-general-3"
    assert rows["director-general-3-retired"]["became"] == "director-general-1"
    assert rows["director-general-1-retired"]["became"] == "director-goals-1"       # the earlier holder's retired row survives
    assert _adjacent(_repo(tmp_path, POSTS.read_text()), "director-review", "director-general-1")


def _free_names(text):
    """the OLD_NAMES no live row holds: the legs of the send test that take the free-name branch"""
    names = {r["name"] for r in _rows(text)}
    return [o for o in OLD_NAMES if o not in names]


def test_the_free_name_leg_of_the_send_test_is_not_vacuous():
    """aio (council 22:23Z 10-21): with both G5 and G6 names reused, the free branch would never run and pass silently.
    director-general-4 stays free for good (director-general-3 until G7): at least one OLD_NAMES leg must take the free branch."""
    assert "director-general-4" in _free_names(POSTS.read_text()) and _free_names(POSTS.read_text())


def test_MUTANT_the_free_names_given_live_rows_leave_no_free_leg_and_RED(tmp_path):
    text = POSTS.read_text()
    live = next(r for r in _rows(text) if r["name"] == "director-general-2")
    extra = "".join("\n  - " + json.dumps({**live, "name": o}, ensure_ascii=False) for o in _free_names(text))
    anchor = next(m for m in re.findall(r"^  - \{.*\}$", text, re.M) if json.loads(m[4:]).get("name") == "director-general-2")
    bad = text.replace(anchor, anchor + extra)
    assert bad != text and _free_names(bad) == [], "the mutant must leave NO free leg, so the guard above is RED on it"


def test_the_reused_name_director_general_2_is_a_live_row_that_was_director_general_4_once_g6_has_landed(tmp_path):
    rows = {r["name"]: r for r in _rows(POSTS.read_text())}
    assert rows["director-general-2"]["was"] == "director-general-4"
    assert rows["director-general-4-retired"]["became"] == "director-general-2"
    assert rows["director-general-2-retired"]["became"] == "director-science-1"       # the earlier holder's retired row survives
    assert "director-general-4" not in rows                                            # the old name stays free for good
    repo = _repo(tmp_path, POSTS.read_text())
    assert _adjacent(repo, "director-review", "director-general-2")
    assert not _adjacent(repo, "director-review", "director-general-4")
