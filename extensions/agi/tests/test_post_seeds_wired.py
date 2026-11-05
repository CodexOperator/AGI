"""A row's engine.seeds are all WIRED (goal:g7.16.1.11.45, council 3/3 15:25Z 10-21, the BIND on the role templates).

brief.py (engine-post.md `### brief.py`, run by agi-brief) keeps only the seeds it can resolve: `S=[M.get(s,s) for s in S.split(',') if M.get(s,s) in P]`.
A misspelled role seed is dropped WITHOUT a word and the post starts on a brief with no role in it. So for every row that carries an engine cell:
every seed resolves (a node id, or a mint id that maps to one) AND brief.py's own list for that row (K = 20, as agi-brief) names it.
Reads the REAL posts.md, the REAL nodes and the REAL brief.py piece of this tree.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
NODES = REPO / ".agi" / "nodes"
POSTS = NODES / ".geometry" / "posts.md"
ENGINE_POST = NODES / ".geometry" / "engine-post.md"
K = 20                                                           # agi-brief's ${K:-20}


def _rows():
    out = {}
    for line in POSTS.read_text().splitlines():
        m = re.match(r"\s+- (\{.*\})\s*$", line)
        if m:
            r = json.loads(m.group(1))
            out[r["name"]] = r
    return out


def _piece():
    m = re.search(r"### brief\.py[^\n]*\n~~~py\n(.*?)\n~~~", ENGINE_POST.read_text(), re.S)
    assert m, "no `### brief.py` piece in engine-post.md"
    return m.group(1)


@pytest.fixture(scope="module")
def graph(tmp_path_factory):
    """ids and mint ids of every node (what brief.py's walk sees: the first 4000 bytes of every file under the nodes dir), and the piece on disk."""
    ids, mints = set(), {}
    for p in NODES.rglob("*"):
        if p.is_file():
            h = p.read_text(errors="ignore")[:4000]
            i = re.search(r"^id: (\S+)", h, re.M)
            if i:
                ids.add(i[1])
                mi = re.search(r"^mint_id: (\S+)", h, re.M)
                if mi:
                    mints[mi[1]] = i[1]
    piece = tmp_path_factory.mktemp("brief") / "brief.py"
    piece.write_text(_piece())
    return ids, mints, piece


def unwired(row, graph, k=K, seeds=None):
    """The problems of one row: a seed that resolves to no node (brief.py drops it silently), or a resolved seed brief.py's list does not name."""
    ids, mints, piece = graph
    seeds = (row["engine"]["seeds"] if seeds is None else seeds).split(",")
    resolved = {s: mints.get(s, s) for s in seeds}
    problems = [f"{s}: resolves to no node (brief.py drops it silently)" for s, r in resolved.items() if r not in ids]
    out = subprocess.run([sys.executable, str(piece), str(NODES), f"doc:card-{row['name']},{','.join(seeds)}", str(k)],
                         capture_output=True, text=True, timeout=300).stdout
    named = {ln.split()[2] for ln in out.splitlines()}
    problems += [f"{s}: not in brief.py's top {k} for {row['name']}" for s, r in resolved.items() if r in ids and r not in named]
    return problems


WIRED = [n for n, r in _rows().items() if (r.get("engine") or {}).get("seeds")]


@pytest.mark.parametrize("name", WIRED)
def test_every_seed_of_every_engine_row_resolves_and_is_named_by_briefpy(name, graph):
    assert unwired(_rows()[name], graph) == []


def test_director_review_carries_the_role_seed_right_after_the_template():
    seeds = _rows()["director-review"]["engine"]["seeds"].split(",")
    assert seeds[:2] == ["doc:unified-director-brief", "doc:role-director-review"], seeds


def test_MUTANT_a_misspelled_role_seed_is_red_while_brief_py_itself_runs_on_without_a_word(graph):
    row = dict(_rows()["director-review"])
    bad = row["engine"]["seeds"].replace("role-director-review", "role-director-reveiw")
    assert bad != row["engine"]["seeds"]
    got = unwired(row, graph, seeds=bad)
    assert got == ["doc:role-director-reveiw: resolves to no node (brief.py drops it silently)"], got
    ids, mints, piece = graph                                    # the silent half: brief.py exits 0 and lists the other seeds
    r = subprocess.run([sys.executable, str(piece), str(NODES), f"doc:card-{row['name']},{bad}", str(K)], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0 and "doc:unified-director-brief" in r.stdout and "role-director-reveiw" not in r.stdout


def test_a_seed_that_resolves_but_brief_py_does_not_name_is_red_too(graph):
    got = unwired(_rows()["director-review"], graph, k=1)         # one slot for four seeds: the list cannot name them all
    assert got and all("not in brief.py's top 1" in g for g in got), got


def test_a_mint_id_seed_resolves_through_brief_pys_own_mapping(graph):
    ids, mints, piece = graph
    mint = next(m for m, i in mints.items() if i == "doc:role-director-review")
    row = dict(_rows()["director-review"])
    assert unwired(row, graph, seeds=f"doc:unified-director-brief,{mint}") == []
