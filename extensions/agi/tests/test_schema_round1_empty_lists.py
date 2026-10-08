"""goal:g1.41 lane I tail, ROUND 1 (DG1 02:13Z + 02:14Z ruling, DG5's exact ids at the live tip d9e0ee099e).

45 LIVE nodes miss a required field that is an EMPTY LIST and nothing else: 24 doc `tags`, 6 vision `tags`, 11 goal
`seeds`, goal g6.51 `seeds` + `tags`, 3 outcome `next_edges` (46 lines). The 2 deprecated docs of the 26 stay out (the
rule is live only). The fill writes ONE front-matter line per field and nothing else; every other node keeps its bytes;
the 10 goals missing `origin`/`confidence` stay unfixed (no bulk fill of a value).

Two kinds of rows:
  * STATE rows (no commit pair): at NEW (ROUND1_NEW, default HEAD) none of the 45 misses its named field(s). They are
    RED on the tip and stay as a standing guard.
  * DIFF rows (a commit pair): BASE -> NEW is exactly the fill. They need ROUND1_BASE=<the build's parent>, e.g.
        ROUND1_BASE=$(git rev-parse HEAD^) python3 -m pytest extensions/agi/tests/test_schema_round1_empty_lists.py
    and SKIP (loudly, by name) without it: a diff row cannot know a moving tip. ROUND1_FULL=1 adds the slow row that
    runs the whole-corpus schema count on both trees (about 2 x 110 s).
Every check reads `git archive` copies of the two revisions (nodes + schemas + config), never the working tree, through
the engine's own node_writer.missing_required: the same function `links.py schema` counts with.
"""
from __future__ import annotations

import difflib
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import node_writer  # noqa: E402
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
BASE_REV = os.environ.get("ROUND1_BASE")
NEW_REV = os.environ.get("ROUND1_NEW") or "HEAD"

DOC = ("card-alive card-all-is-one card-director-general-1 card-director-general-2 card-director-general-3 "
       "card-director-general-6 card-sanctuary-master card-self-perpetuating card-thought-master "
       "draft-skills-first-turn g5-lifecycle-history g716111-stage2-rootplan g716111-stage25-parity "
       "g716111-stage25-rootplan l3-command-ladder-brief l4-owner-decisions lm-progress-2026-09-18 "
       "lm-research-corpus-registry lm-round0-table lm-town-trajectory lm-trove-2026-09-18-owner-links quick-setup "
       "s3-plan season-ladder-and-morals-brief").split()
VISION = "shown-not-told streaming-suite the-owner-sets-the-pace unbroken-signal web-app-suite your-words-our-axes".split()
GOAL_SEEDS = "g1.31 g1.41 g5.23.2 g5.23.3 g5.26.2 g5.30.2 g5.30 g5.31 g7.16.1.11 g7.33 qwen3-np64-noise-band".split()
OUTCOME = "a00-5510b3ee-67fb62 a00-c8365a0c-85a6d1 a00-fd594bfd-ad6af8".split()

#: (type, slug, (fields...)) -- the lane's input, in DG5's order.
ITEMS = ([("doc", s, ("tags",)) for s in DOC] + [("vision", s, ("tags",)) for s in VISION]
         + [("goal", s, ("seeds",)) for s in GOAL_SEEDS] + [("goal", "g6.51", ("seeds", "tags"))]
         + [("outcome", s, ("next_edges",)) for s in OUTCOME])
IDS = [f"{t}-{s}" for t, s, _ in ITEMS]
PATH = {(t, s): f".agi/nodes/{t}/{s}.md" for t, s, _ in ITEMS}
NAMED = {(t, s, f) for t, s, fs in ITEMS for f in fs}
LISTED = set(PATH.values())
needs_base = pytest.mark.skipif(not BASE_REV, reason="a diff row needs ROUND1_BASE=<the build's parent> (see the module doc)")


def _git(*args, text=True):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=text)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr if text else r.stderr.decode(errors='replace')}")
    return r.stdout


def _rev(rev):
    return _git("rev-parse", "--verify", rev + "^{commit}").strip()


def _archive(tmp_root: Path, rev: str) -> Path:
    """A copy of nodes + schemas + config at REV, as a `.agi` root node_writer can read."""
    dest = tmp_root / rev[:12]
    if not dest.exists():
        dest.mkdir(parents=True)
        tar = subprocess.run(["git", "-C", str(REPO), "archive", rev, ".agi/nodes", ".agi/context/schemas", ".agi/config.json"],
                             capture_output=True)
        assert tar.returncode == 0, tar.stderr
        subprocess.run(["tar", "-x", "-C", str(dest)], input=tar.stdout, check=True)
    return dest / ".agi"


@pytest.fixture(scope="module")
def trees(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("round1")
    new = _rev(NEW_REV)
    out = {"new": new, "new_root": _archive(tmp, new)}
    if BASE_REV:
        out["base"] = _rev(BASE_REV)
        out["base_root"] = _archive(tmp, out["base"])
    return out


def _file(root: Path, typ: str, slug: str) -> Path:
    for p in (root / "nodes" / typ / f"{slug}.md", root / "nodes" / "deprecated" / typ / f"{slug}.md"):
        if p.is_file():
            return p      # a node moved to deprecated/ later still carries its front matter
    pytest.fail(f"{typ}:{slug} has no file under nodes/{typ}/ or nodes/deprecated/{typ}/")


def _missing(root: Path, path: Path) -> list:
    typ = node_writer.canonical_node_type(path.parent.name if path.parent.name != "deprecated" else path.parent.parent.name)
    fm = fm_reader.load_node_file(path).frontmatter
    return sorted(node_writer.missing_required(root, typ, fm, str(fm.get("id"))))


# --- STATE rows (NEW only)
@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_r1_state_the_node_no_longer_misses_its_named_field(trees, item):
    typ, slug, fields = item
    root = trees["new_root"]
    miss = _missing(root, _file(root, typ, slug))
    assert not (set(miss) & set(fields)), f"{typ}:{slug} still misses {sorted(set(miss) & set(fields))} at {trees['new'][:10]}"


# --- the list itself (BASE)
@needs_base
@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_r1_before_each_listed_node_misses_exactly_the_named_fields(trees, item):
    typ, slug, fields = item
    root = trees["base_root"]
    assert _missing(root, _file(root, typ, slug)) == sorted(fields), (typ, slug)


# --- DIFF rows (BASE -> NEW)
def _lines(rev: str, path: str):
    return _git("show", f"{rev}:{path}").split("\n")


def _fm_end(lines) -> int:
    """Index of the closing fence of the front matter."""
    assert lines[0] == "---", lines[:2]
    return lines.index("---", 1)


@needs_base
def test_r1_diff_touches_exactly_the_45_listed_files_and_deletes_nothing(trees):
    out = _git("diff", "--name-status", "--no-renames", trees["base"], trees["new"])
    rows = [l.split("\t") for l in out.splitlines() if l]
    assert sorted(r[1] for r in rows) == sorted(LISTED), \
        f"outside the list: {sorted({r[1] for r in rows} - LISTED)}; listed but untouched: {sorted(LISTED - {r[1] for r in rows})}"
    assert {r[0] for r in rows} == {"M"}, [r for r in rows if r[0] != "M"]


@needs_base
@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_r1_diff_each_file_only_gains_the_named_lines_inside_its_front_matter(trees, item):
    typ, slug, fields = item
    path = PATH[(typ, slug)]
    b, n = _lines(trees["base"], path), _lines(trees["new"], path)
    ops = difflib.SequenceMatcher(None, b, n, autojunk=False).get_opcodes()
    kinds = {op[0] for op in ops}
    assert kinds <= {"equal", "insert"}, f"{path}: lines were replaced or deleted: {[o for o in ops if o[0] not in ('equal', 'insert')][:3]}"
    added = [(j, n[j]) for tag, _i1, _i2, j1, j2 in ops if tag == "insert" for j in range(j1, j2)]
    assert sorted(t for _j, t in added) == sorted(f"{f}: []" for f in fields), f"{path} gained {[t for _j, t in added]}"
    end = _fm_end(n)
    assert all(j < end for j, _t in added), f"{path}: a line landed after the front matter's closing fence"


def _mint(lines):
    return [l for l in lines[:_fm_end(lines)] if l.startswith("mint_id:")]


@needs_base
@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_r1_diff_no_mint_id_changes_and_the_body_is_byte_identical(trees, item):
    typ, slug, _fields = item
    path = PATH[(typ, slug)]
    b, n = _lines(trees["base"], path), _lines(trees["new"], path)
    assert _mint(b) == _mint(n) and len(_mint(b)) == 1, path
    assert b[_fm_end(b):] == n[_fm_end(n):], f"{path}: the body or the closing fence changed"


def _expected(base_lines, fields):
    """BASE with each field's line inserted where the file's own key order puts it: `next_edges` directly after the
    parents block, any other key at its alphabetical place among the keys after the parents block (before the first
    key that sorts after it, else at the end of the front matter)."""
    lines = list(base_lines)
    for field in sorted(fields):
        end = _fm_end(lines)
        keys = [(i, l.split(":", 1)[0]) for i, l in enumerate(lines[1:end], 1) if l and not l[0].isspace() and not l.startswith("-") and ":" in l]
        pi = next(i for i, k in keys if k == "parents")
        nxt = next((i for i, _k in keys if i > pi), end)           # the end of the parents block
        if field == "next_edges":
            at = nxt
        else:
            tail = [(i, k) for i, k in keys if i >= nxt and k != "next_edges"]
            at = next((i for i, k in tail if k > field), end)
        lines.insert(at, f"{field}: []")
    return lines


@needs_base
@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_r1_diff_each_new_line_sits_where_the_files_key_order_puts_it(trees, item):
    typ, slug, fields = item
    path = PATH[(typ, slug)]
    b, n = _lines(trees["base"], path), _lines(trees["new"], path)
    assert n == _expected(b, fields), f"{path}: placement differs from the key-order rule (next_edges after parents, else alphabetical)"


# --- CONTROLS
def _blobs(rev, *paths):
    out = _git("ls-tree", "-r", rev, "--", *paths)
    return {l.split("\t", 1)[1]: l.split()[2] for l in out.splitlines() if l}


@needs_base
def test_r1_control_every_other_node_and_schema_keeps_its_bytes(trees):
    b, n = _blobs(trees["base"], ".agi/nodes", ".agi/context/schemas"), _blobs(trees["new"], ".agi/nodes", ".agi/context/schemas")
    changed = {p for p in set(b) | set(n) if b.get(p) != n.get(p)}
    outside = changed - LISTED
    assert not outside, f"{len(outside)} file(s) outside the list changed, e.g. {sorted(outside)[:5]}"
    assert not (set(b) - set(n)), f"a file was deleted: {sorted(set(b) - set(n))[:5]}"


@needs_base
def test_r1_control_the_goals_missing_origin_or_confidence_stay_unfixed_and_nothing_else_is_filled(trees):
    """Every goal node (live and retired): no (node, missing field) pair appears at NEW, and the only pairs that
    disappear are the named seeds/tags ones. A bulk fill of `origin` or `confidence` (or of any field not named) is RED."""
    def pairs(root):
        out = set()
        for p in sorted((root / "nodes").rglob("*.md")):
            if p.parent.name != "goal" or p.name.startswith("."):
                continue
            fm = fm_reader.load_node_file(p).frontmatter
            for f in node_writer.missing_required(root, "goal", fm, str(fm.get("id"))):
                out.add((str(fm.get("id")), f))
        return out
    before, after = pairs(trees["base_root"]), pairs(trees["new_root"])
    named = {(f"goal:{s}", f) for t, s, f in NAMED if t == "goal"}
    assert named <= before, f"named pairs not missing at BASE: {sorted(named - before)}"
    assert not (after - before), f"a goal gained a missing field: {sorted(after - before)}"
    assert (before - after) <= named, f"fields filled beyond the list: {sorted((before - after) - named)}"
    for fld in ("origin", "confidence"):
        n0, n1 = sum(1 for _n, f in before if f == fld), sum(1 for _n, f in after if f == fld)
        assert n0 == n1 >= 1, f"goals missing {fld}: {n0} -> {n1} (want unchanged, >= 1)"


@needs_base
def test_r1_control_the_schema_count_over_the_listed_files_drops_by_exactly_45(trees):
    def count(root):
        return sum(1 for t, s, _f in ITEMS if _missing(root, _file(root, t, s)))
    assert count(trees["base_root"]) - count(trees["new_root"]) == 45


@needs_base
@pytest.mark.skipif(os.environ.get("ROUND1_FULL") != "1", reason="slow (about 2 x 110 s): set ROUND1_FULL=1 for the whole-corpus schema count")
def test_r1_full_corpus_schema_count_drops_by_exactly_45(trees):
    def count(root):
        n = 0
        for p in sorted((root / "nodes").rglob("*.md")):
            if p.name.startswith("."):
                continue
            typ = node_writer.canonical_node_type(p.parent.name)
            if not node_writer.required_fields(root, typ):
                continue
            try:
                fm = fm_reader.load_node_file(p).frontmatter
            except Exception:
                continue
            n += bool(node_writer.missing_required(root, typ, fm, str(fm.get("id") or f"{typ}:{p.stem}")))
        return n
    b, a = count(trees["base_root"]), count(trees["new_root"])
    assert b - a == 45, (b, a)
