"""goal:g7.16.1.1.5 · hypothesis:one-cell-activates-one-formation-and-reads-back-one.

verification.check_formation: 0 active -> FAIL · 1 -> PASS · 2 -> FAIL; no cell
-> SKIP. The wake list reads the park TAG `parked:<goal>` (goal:g7.16.1.2.6): a
node that merely MENTIONS it in its body never wakes; a THOUGHT still carrying
the retired `parked: formation` mark FAILs the check.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import verification  # noqa: E402

_T = "<!-- THOUGHT:BEGIN -->\n{}\n<!-- THOUGHT:END -->\n"


def _node(root: Path, rel: str, nid: str, body: str = "", tags: str = "") -> None:
    f = root / "nodes" / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    fm = f"tags: [{tags}]\n" if tags else ""
    f.write_text(f"---\nid: {nid}\ntype: {nid.split(':')[0]}\n{fm}---\n{body}", "utf-8")


@pytest.fixture
def groot(tmp_path):
    root = tmp_path / ".agi"
    _node(root, "doc/council-loop.md", "doc:council-loop")
    _node(root, "doc/two-step.md", "doc:two-step")
    _node(root, "goal/g1.md", "goal:g1", _T.format("parked: why"), "keep, parked:g7.16.2")
    _node(root, "goal/g2.md", "goal:g2", "a body naming `parked:g7.16.2`\n")
    _node(root, "goal/g3.md", "goal:g3", tags="parked:g7.16.20")
    _node(root, "deprecated/goal/g4.md", "goal:g4", tags="parked:g7.16.2")
    return root


def _cell(root: Path, active: str) -> None:
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / ".geometry" / "formations.md").write_text(
        "---\nid: config:formations\ntype: config\n"
        f"active: {active}\n"
        "templates: {doc:council-loop: g7.16.1, doc:two-step: g7.16.2}\n---\n", "utf-8")


def test_no_cell_is_a_skip(groot):
    assert verification.check_formation(groot).status == "SKIP"


@pytest.mark.parametrize("active", ["''", "[doc:council-loop, doc:two-step]",
                                    "doc:not-registered"])
def test_zero_or_two_active_fails(groot, active):
    _cell(groot, active)
    assert verification.check_formation(groot).status == "FAIL"


def test_one_active_passes_and_wakes_only_the_tag(groot):
    _cell(groot, "doc:two-step")
    r = verification.check_formation(groot)
    assert (r.status, r.note, r.message) == ("PASS", "active doc:two-step g7.16.2",
                                             "wake goal:g1")


def test_switching_is_one_cell_and_changes_the_wake_list(groot):
    _cell(groot, "doc:two-step")
    assert verification.check_formation(groot).number == {"wake": 1}
    _cell(groot, "doc:council-loop")
    r = verification.check_formation(groot)
    assert (r.status, r.number) == ("PASS", {"wake": 0})


# --- goal:g7.16.1.2.5 · hypothesis:formation-check-refuses-a-deprecated-template
# (council bundle 2, director-general-2)
def _cell_with(root: Path, active: str, templates: str) -> None:
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / ".geometry" / "formations.md").write_text(
        f"---\nid: config:formations\ntype: config\nactive: {active}\n"
        f"templates: {templates}\n---\n", "utf-8")


# RED on the trunk at 82d64ffe7 -- find_node_file resolves nodes/deprecated/,
# so a retired template passed; green since director-general-3's build.
def test_a_retired_template_fails_the_check(groot):
    _node(groot, "deprecated/doc/retired.md", "doc:retired")
    _cell_with(groot, "doc:retired", "{doc:council-loop: g7.16.1, doc:retired: g7.16.9}")
    assert verification.check_formation(groot).status == "FAIL"


def test_the_switch_runs_through_write_py(groot):
    """The ONE act that switches a formation is `write.py config:formations
    'set active <doc>'` -- driven here in the tmp project, then read back."""
    import subprocess
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    wp = Path(__file__).resolve().parents[1] / "bin" / "write.py"
    r = subprocess.run([sys.executable, str(wp), "config:formations", "set active doc:two-step",
                        "--actor", "test", "--role", "director"],
                       cwd=groot.parent, capture_output=True, text=True, timeout=120,
                       env={k: v for k, v in __import__("os").environ.items() if not k.startswith(("TMUX", "AGI_"))})
    assert r.returncode == 0, r.stderr[-400:]
    res = verification.check_formation(groot)
    assert res.status == "PASS" and "doc:two-step" in (res.note or "")


# --- goal:g7.16.1.2.6 · hypothesis:park-is-a-tag-that-set-active-drops
# (council bundle 2, director-general-2). RED on the trunk at 82d64ffe7 -- the
# park was THOUGHT text and `set active` dropped nothing; green since
# director-general-3's build.
def test_set_active_drops_that_formations_park_tag(groot):
    import os, subprocess
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    f = groot / "nodes" / "hypothesis" / "h.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("---\nid: hypothesis:h\ntype: hypothesis\ntitle: h\ntestable_claim: c\n"
                 "tags:\n  - parked:g7.16.2\n  - keep-me\n---\nbody\n", "utf-8")
    wp = Path(__file__).resolve().parents[1] / "bin" / "write.py"
    r = subprocess.run([sys.executable, str(wp), "config:formations", "set active doc:two-step",
                        "--actor", "test", "--role", "director"], cwd=groot.parent,
                       capture_output=True, text=True, timeout=120,
                       env={k: v for k, v in os.environ.items() if not k.startswith(("TMUX", "AGI_"))})
    assert r.returncode == 0, r.stderr[-400:]
    text = f.read_text("utf-8")
    assert "parked:g7.16.2" not in text and "keep-me" in text


def test_a_thought_park_mark_fails_the_check(groot):
    """The retired mark never parks quietly: the read-back names its carrier."""
    _node(groot, "goal/g5.md", "goal:g5", _T.format("triage (parked: formation g7.16.2)"))
    _cell(groot, "doc:two-step")
    r = verification.check_formation(groot)
    assert (r.status, r.message) == ("FAIL", "mark goal:g5")


@pytest.mark.parametrize("tags,ok", [("[parked:g7.16.2, keep-me, parked]", True),
                                     ("[parked: formation g7.16.2]", False),
                                     ("[parked:g7.]", False)])
def test_the_schema_holds_the_park_tag_form(groot, tags, ok):
    import os, shutil, subprocess
    (groot / "config.json").write_text("{}\n", "utf-8")
    src = Path(__file__).resolve().parents[3] / ".agi" / "context" / "schemas"
    (groot / "context").mkdir()
    shutil.copytree(src, groot / "context" / "schemas")
    wp = Path(__file__).resolve().parents[1] / "bin" / "write.py"
    r = subprocess.run([sys.executable, str(wp), "goal:g3", f"set tags {tags}",
                        "--actor", "test", "--role", "director"], cwd=groot.parent,
                       capture_output=True, text=True, timeout=120,
                       env={k: v for k, v in os.environ.items() if not k.startswith(("TMUX", "AGI_"))})
    assert (r.returncode == 0) is ok, r.stderr[-400:]
    assert ("item_regex" in r.stderr) is (not ok)


# --- goal:g7.16.1.2.8 · hypothesis:formations-are-one-registry-with-one-home
# The LIVE registry (a corpus row, like the thought-hygiene corpus test): every
# registered template maps to a goal and lives in the one formations home.
# RED on the trunk at 82d64ffe7 -- 4 of 6 map to "", and doc:council-loop sat
# under nodes/doc/ (council bundle 2, director-general-2); green since the
# home move (e12ca48c7) and the Prime's templates cell (fee990795).
def test_the_live_registry_maps_every_template_to_a_goal_in_one_home():
    import locations, node_writer, yaml
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        pytest.skip("not running inside an agi project checkout")
    cell = node_writer.find_node_file(root, "config:formations")
    fm = yaml.safe_load(cell.read_text("utf-8").split("---", 2)[1])
    table = fm.get("templates") or {}
    assert table and all(str(g).startswith("g") for g in table.values()), table
    home = root / "nodes" / ".geometry" / "formations"
    for doc in table:
        path = node_writer.find_node_file(root, doc)
        assert path is not None and path.parent == home, doc


# --- goal:g7.16.1.2.8 conjuncts (2)+(3) · goal:g7.16.1.2.5 Falsifier 2 (re-scoped onto T)
def test_the_live_formation_home_holds_pointers_not_copies():
    """LIVE: the active formation sits in the one home, and no live template
    carries the stand-up steps inline or a goal:g7.16 L<n> citation."""
    import re, locations, node_writer
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        pytest.skip("not running inside an agi project checkout")
    home = root / "nodes" / ".geometry" / "formations"
    assert node_writer.find_node_file(root, "doc:council-loop").parent == home
    for f in sorted(home.glob("*.md")):
        text = f.read_text("utf-8")
        assert "rotate.py spawn --seat" not in text and "skill agi-post" in text, f.name
        assert not re.search(r"goal:g7\.16 L\d", text), f.name


@pytest.mark.parametrize("rel,nid,thought,status", [
    ("goal/g6.md", "goal:g6", "why\nparked: formation g7.16.2 -- x", "FAIL"),  # 52: line 2 (re.M only)
    ("goal/g6.md", "goal:g6", "parked: formation g7.16.2 -- why", "FAIL"),           # the ^ branch
    ("build/b.md", "build:b", "triage (parked: formation g7.16.2)", "PASS"),         # not a carrier type
    ("goal/g6.md", "goal:g6", "11 parked: formation g7.16.2 -- rows 2 4", "PASS"),   # a tally
    ("build/b.md", "build:b", "FAILs on the retired parked: formation mark", "PASS"),  # prose
    ("goal/g6.md", "goal:g6", "prose names the parked: formation g7.16.2 mark", "PASS"),  # prose on a goal
])
def test_only_the_mark_shape_on_a_carrier_trips_the_check(groot, rel, nid, thought, status):
    """Residues 49 + 52: the MARK shape, on any THOUGHT line, on goal/hypothesis only."""
    _node(groot, rel, nid, _T.format(thought))
    _cell(groot, "doc:two-step")
    assert verification.check_formation(groot).status == status


@pytest.mark.parametrize("how", ["rejected", "oserror"])
def test_a_rejected_carrier_is_named_on_stderr(groot, monkeypatch, capsys, how):
    """Residue 54: the set-active hook names a carrier update_node REJECTS or
    whose write raises OSError, and goes on (the loop is never aborted)."""
    import node_writer, write
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    real = node_writer.update_node

    def refuse_g1(root, nid, **kw):
        if nid != "goal:g1":
            return real(root, nid, **kw)
        if how == "oserror":
            raise OSError("probe")
        return node_writer.NodeWrite(status=node_writer.REJECTED, node_id=nid, reason="probe")
    monkeypatch.setattr(node_writer, "update_node", refuse_g1)
    _node(groot, "goal/g9.md", "goal:g9", tags="parked:g7.16.2")  # sorts AFTER goal:g1 (residue 56)
    write.submit(groot, write.Edit(node_id="config:formations", set_fm={"active": "doc:two-step"}),
                 actor="test", role="director")
    err = capsys.readouterr().err
    assert "unpark REJECTED goal:g1 (parked:g7.16.2): probe" in err
    assert "unparked goal:g9 (parked:g7.16.2)" in err  # the loop went on
    assert "parked:g7.16.2" not in (groot / "nodes" / "goal" / "g9.md").read_text("utf-8")


# council C1 on bundle 3 (alive, all-is-one's lens): a carrier grep that cannot
# look REFUSES `set active` with nothing written -- never rc 0 with every carrier
# still parked (check_formation's fail-closed stance, on the write side).
def test_set_active_refuses_when_the_carrier_grep_fails(groot, monkeypatch, capsys):
    import rotation_record, write
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    _node(groot, "goal/g9.md", "goal:g9", tags="parked:g7.16.2")
    cell = groot / "nodes" / ".geometry" / "formations.md"
    before = cell.read_bytes()

    def blind(root, goal):
        raise rotation_record.GrepError("git grep exit 128: fatal: probe")
    monkeypatch.setattr(rotation_record, "parked_carriers", blind)
    rc = write.main(["config:formations", "set active doc:two-step", "--root", str(groot),
                     "--actor", "test", "--role", "director"])
    assert rc == 2 and "set active refused" in capsys.readouterr().err
    assert cell.read_bytes() == before  # nothing written
    assert "parked:g7.16.2" in (groot / "nodes" / "goal" / "g9.md").read_text("utf-8")


# --- goal:g7.16.1.3.1 · hypothesis:row-parks-carry-a-carrier-tag (bundle 3 H3,
# director-general-2): a row ending `· triage: parked: formation g<N> |` needs its
# carrier's parked:<goal> tag; a node that only QUOTES the string never trips it.
_ROW = "| 2 | x | OWED · triage: parked: formation g7.16.2 |\n"
_QUOTE = "| a bare `triage: parked: formation` grep | `· triage: parked: formation g[0-9.]+ \\|$` |\n"


@pytest.mark.parametrize("body,tags,status", [
    (_ROW, "", "FAIL"),                 # the untagged carrier
    (_ROW, "parked:g7.16.2", "PASS"),   # the tagged carrier
    (_QUOTE, "", "PASS"),               # quotes only: the rule is anchored
], ids=["untagged-row", "tagged-row", "quote-only"])
def test_a_row_park_needs_its_carrier_tag(groot, body, tags, status):
    _node(groot, "goal/g8.md", "goal:g8", body, tags)
    _cell(groot, "doc:council-loop")    # the row waits for g7.16.2, a formation NOT active
    r = verification.check_formation(groot)
    assert r.status == status and (status == "PASS" or "goal:g8" in r.message)


# council mur CM7: the ROW rule claims "a live node", so a row-park on a doc
# (not a MARK carrier type) needs its tag too; the MARK rule stays goal/hypothesis.
@pytest.mark.parametrize("tags,status", [("", "FAIL"), ("parked:g7.16.2", "PASS")])
def test_a_row_park_on_any_live_node_needs_its_tag(groot, tags, status):
    _node(groot, "doc/d.md", "doc:d", _ROW, tags)
    _cell(groot, "doc:council-loop")
    r = verification.check_formation(groot)
    assert r.status == status and (status == "PASS" or r.message == "untagged doc:d (parked:g7.16.2)")


# sanctuary-master mur wf_a3b15e54-c65 residue 61: `set active` on the formation a
# row waits for drops the carrier's tag while the row stays -- the gate PASSes then.
def test_rows_parked_for_the_active_formation_pass_untagged(groot):
    _node(groot, "goal/g8.md", "goal:g8", _ROW, "")
    _cell(groot, "doc:two-step")        # g7.16.2 is now the active formation's goal
    assert verification.check_formation(groot).status == "PASS"


# residue 62: a hit with NO frontmatter block is a named FAIL, never a TypeError.
def test_a_frontmatter_less_hit_is_a_named_fail(groot):
    (groot / "nodes" / "goal").mkdir(parents=True, exist_ok=True)
    (groot / "nodes" / "goal" / "loose.md").write_text("parked: formation g7.16.2\n", "utf-8")
    _cell(groot, "doc:council-loop")
    r = verification.check_formation(groot)
    assert r.status == "FAIL" and "loose.md" in r.message


# --- goal:g7.16.1.3.2.3.2 · hypothesis:the-formation-gate-fails-closed-on-a-grep-error
# (bundle 3 H4 f, director-general-2): git grep exit >= 2 is a FAIL carrying
# git's stderr (exit 1 = no hits stays PASS: test_switching_... wake 0).
@pytest.mark.parametrize("how", ["bad-pathspec", "git-config"])
def test_a_grep_error_fails_closed(groot, monkeypatch, how):
    import subprocess
    real = subprocess.run
    if how == "git-config":
        monkeypatch.setenv("GIT_CONFIG_PARAMETERS", "bogus")    # real git, exit 128
    else:                                                       # real git, exit 128
        monkeypatch.setattr(subprocess, "run", lambda a, **kw: real(
            [":(badmagic)." if x in (".", "*.md") else x for x in a], **kw))   # *.md: SM 103
    _cell(groot, "doc:two-step")
    r = verification.check_formation(groot)
    assert r.status == "FAIL" and ("fatal" in r.note + r.message
                                   or "bogus" in r.note + r.message)


def test_a_malformed_hit_is_a_named_fail_not_a_crash(groot):
    f = groot / "nodes" / "goal" / "bad.md"
    f.write_text("---\nid: goal:bad\ntags: [unclosed\n---\nparked: formation g7.16.2\n", "utf-8")
    _cell(groot, "doc:two-step")
    r = verification.check_formation(groot)
    assert r.status == "FAIL" and "bad.md" in r.message
