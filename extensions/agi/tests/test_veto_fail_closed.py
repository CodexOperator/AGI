"""G-FRZ FAILS CLOSED (goal:g7.16.1.11.13.2, DG1 18:21Z + goals v3 ebbbc40be8 + the writer list's F3; DG2 writes the rows FIRST, DG4 builds).

The frozen-prime veto guards seven gated acts. Today five of them read the veto cell NON-strict (a MISSING or MALFORMED cell reads as a FREE tree with no exception) and swallow every other error under an `except Exception: pass`; the config-row gate of write.py does the same; the publish check of rotate.py lets an ImportError through. After the build EVERY site reads strict and EVERY failure to read or judge the veto is HELD BY NAME carrying the cause, and nothing is pushed / merged / written:

  S1 `_make_closeout_seams()["merge_up"]` (rotate.py:9520)      S2 `_make_closeout_seams()["push"]` (:9644)       S3 `_push_season_branch` (:10832)
  S4 `_stops_push` when the branch is a TRUNK (:19208)           S5 `_rotate_human_gate` for ANOTHER post (:19616)  S6 `_publish_row_to_authority` ImportError arm (:10979)
  S7 write.py's config-row edit gate OUTSIDE self_row (:1921-1927).

Causes, each a row per site: the cell MISSING · MALFORMED (unparsable) · `active_gates` not a list · `seatsig.veto.read` raising ValueError · `seatsig.veto.is_frozen` raising ValueError (a healthy cell) · `from seatsig import veto` raising ImportError. A well-formed FREE cell proceeds exactly as today (the side effect happens); a FROZEN cell holds with the HELD text as today. Rows w/ a raising cause also require the exception TEXT in the held line. F3: `_grid_commit` (:9616) and `_button_down` (:12557) report the retired no-op honestly and a real failure as a failure, never `grid committed`. Negative: the lying comment is gone and no veto read lacks `strict=True` (rotate.py:19601's best-effort active_gate lookup is exempt BY NAME).

Env VETO_ROOT=<tree> runs the rows against a scratch tree (extensions/agi/{bin,src}); default: the repo that holds this file. Hermetic: git, subprocess and MAIN resolution are faked; the veto cell is a REAL file in a tmp graph root.
"""
from __future__ import annotations

import os
import re
import sys
import types
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("VETO_ROOT") or HERE.parents[3])
EXT = ROOT / "extensions"
BIN = EXT / "agi" / "bin"
sys.path.insert(0, str(EXT))
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(EXT / "agi" / "src"))

from agi.bin import rotate  # noqa: E402
import write  # noqa: E402
import node_writer  # noqa: E402
from seatsig import veto  # noqa: E402

CELL = Path("nodes") / ".geometry" / "vetoes.md"
FREE = "---\nid: config:vetoes\nmint_id: 5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a\ntype: config\nparents: []\nactive_gates: []\nvetoes: []\n---\n\n# config:vetoes\n"
CAUSES = ["missing", "malformed", "notlist", "read_raises", "frozen_check_raises", "import_error"]
EXC = {"read_raises": "boom-read-7", "frozen_check_raises": "boom-frozen-7", "import_error": "boom-import-7"}


class Proc:
    def __init__(self, rc=0, out="", err=""):
        self.returncode, self.stdout, self.stderr = rc, out, err


def make_graph(tmp_path: Path, state: str) -> Path:
    """A graph root whose veto cell is in `state`: free | frozen | missing | malformed | notlist (the patch causes use a FREE cell)."""
    g = tmp_path / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    cell = g / CELL
    if state == "missing":
        return g
    if state == "malformed":
        cell.write_text("---\nactive_gates: [unclosed\n  - {\n---\nbody\n")
    elif state == "notlist":
        cell.write_text("---\nid: config:vetoes\ntype: config\nactive_gates: oops\nvetoes: []\n---\nbody\n")
    elif state == "frozen":
        cell.write_text(FREE)
        geom = veto.read(g, CELL)
        geom["active_gates"] = [{"scope": "prime", "since": "2026-09-12T00:00:00Z", "reason": "council veto", "veto_ref": "veto:001", "answered": ""}]
        geom["vetoes"] = [{"veto_ref": "veto:001", "scope": "prime", "filed_at": "2026-09-12T00:00:00Z", "expires_at": "2026-09-12T00:00:00Z", "answer": ""}]
        veto.save(g, geom, CELL)
    else:
        cell.write_text(FREE)
    return g


def arm(monkeypatch, cause: str) -> str:
    """Install the CAUSE: returns the cell state to build. Patch causes use a FREE cell."""
    if cause in ("missing", "malformed", "notlist", "free", "frozen"):
        return cause
    if cause == "read_raises":
        def boom(*a, **k):
            raise ValueError(EXC[cause])
        monkeypatch.setattr(veto, "read", boom)
    elif cause == "frozen_check_raises":
        def boom2(*a, **k):
            raise ValueError(EXC[cause])
        monkeypatch.setattr(veto, "is_frozen", boom2)
    elif cause == "import_error":
        class Stub(types.ModuleType):
            def __getattr__(self, name):
                raise ImportError(EXC["import_error"])
        monkeypatch.setitem(sys.modules, "seatsig", Stub("seatsig"))
    return "free"


# ---- the seven sites: each runner returns (held: bool, text: str, effects: list of argv-tuples that pushed / merged) ----

def _fake_closeout(monkeypatch, g, calls):
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda r: g)
    monkeypatch.setattr(rotate, "_closeout_main", lambda r: g)
    monkeypatch.setattr(rotate, "_closeout_branch", lambda cwd: "season2/main")
    monkeypatch.setattr(rotate, "_fd_seat_branch", lambda r, main, seat: "season2/posts/adv")
    monkeypatch.setattr(rotate, "_closeout_main_clean", lambda main, sb: (True, [], 0))
    monkeypatch.setattr(rotate, "_git_proc", lambda cwd, *a: calls.append(a) or Proc(0))
    monkeypatch.setattr(rotate, "_git_maybe", lambda cwd, *a: ["abc1234"] if a[:1] == ("rev-parse",) else None)


def site_merge_up(monkeypatch, g):
    calls = []
    _fake_closeout(monkeypatch, g, calls)
    ok, res, detail = rotate._make_closeout_seams(g, {}, seat="adv")["merge_up"]()
    return (not ok and "HELD" in detail), detail, [c for c in calls if c[:1] == ("merge",)]


def site_push(monkeypatch, g):
    calls = []
    _fake_closeout(monkeypatch, g, calls)
    ok, res, detail = rotate._make_closeout_seams(g, {}, seat="adv")["push"]()
    return (not ok and "HELD" in detail), detail, [c for c in calls if c[:1] == ("push",)]


def _fake_run(monkeypatch, branch, calls):
    def run(argv, **kw):
        calls.append(tuple(argv))
        if "rev-parse" in argv:
            return Proc(0, branch + "\n")
        if "ls-remote" in argv:
            return Proc(0, f"{branch}\trefs/agi/posts/adv")
        return Proc(0)
    monkeypatch.setattr(rotate.subprocess, "run", run)


def site_push_season_branch(monkeypatch, g):
    calls = []
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda r: g)
    monkeypatch.setattr(rotate, "_git_toplevel", lambda r: g)
    _fake_run(monkeypatch, "season2/main", calls)
    line = rotate._push_season_branch(g)
    return "HELD" in line, line, [c for c in calls if "push" in c]


def site_stops_push_trunk(monkeypatch, g):
    calls = []
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda r: g)
    monkeypatch.setattr(rotate, "_git_toplevel", lambda r: g)
    _fake_run(monkeypatch, "season2/main", calls)
    out = rotate._stops_push(g, "stops")
    return (out is not None and "HELD" in out), out or "", [c for c in calls if "push" in c]


def site_rotate_other(monkeypatch, g):
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda r: g)
    held, freeze = rotate._rotate_human_gate(g, "some-other-post", actor="me")
    return (held is not None and "HELD" in held), held or "", ([] if held else [("rotated",)])


def site_publish(monkeypatch, g):
    import send as _send
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda r: g)
    monkeypatch.setattr(_send, "authority_ref", lambda r: (_ for _ in ()).throw(RuntimeError("no authority in the fixture")))
    out = rotate._publish_row_to_authority(g, "adv", "")
    return "HELD" in out, out, ([] if "HELD" in out else [("past-the-gate",)])


def site_write(monkeypatch, g):
    """write.py's gate: a config:seats edit by the OWNER (not a seated self_row writer) in a project whose graph root is `g`."""
    import json
    rows = [{"name": "belam", "role": "prime_director", "model": "claude-opus-5", "session_ref": "aca130", "generation": 0, "window": ""}]
    g.mkdir(parents=True, exist_ok=True)
    sd = g / "context" / "schemas"
    sd.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text("{}")
    live = ROOT / ".agi" / "context" / "schemas" / "[config].md"
    (sd / "[config].md").write_text(live.read_text(encoding="utf-8") if live.exists() else "---\nname: config\nwritten_by: [owner, prime_director]\nself_row: {list_key: seats, match_key: name, fields: [session_ref, generation, window]}\n---\n")
    body = "\n".join(f"  - {r!r}" for r in rows)
    seats = g / "nodes" / ".geometry" / "seats.md"
    seats.write_text("---\nid: config:seats\nmint_id: 3e88873e3c204c5088f6ab81322a26de\ntype: config\nparents:\n  - goal:g17\nseats:\n" + body + "\n---\n\n# config:seats\n\nfixture body\n")
    before = seats.read_bytes()
    new = [dict(rows[0], role="director")]
    e = write.Edit("config:seats")
    write.verb_set(e, "seats", json.dumps(new))
    try:
        write.submit(g, e, actor="owner", role="owner")
    except write.EditError as exc:
        return True, str(exc), ([("wrote",)] if seats.read_bytes() != before else [])
    return False, "", ([("wrote",)] if seats.read_bytes() != before else [])


SITES = {"merge_up": site_merge_up, "push": site_push, "push_season_branch": site_push_season_branch, "stops_push_trunk": site_stops_push_trunk,
         "rotate_other": site_rotate_other, "publish": site_publish, "write_config_row": site_write}


def has_cause_text(cause: str, text: str) -> bool:
    if cause in EXC:
        return EXC[cause] in text
    return "veto" in text.lower()      # missing / malformed / notlist: the VetoCellUnreadable text names the cell


@pytest.mark.parametrize("site", sorted(SITES))
@pytest.mark.parametrize("cause", CAUSES)
def test_a_veto_that_cannot_be_read_or_judged_holds_by_name_and_does_nothing(tmp_path, monkeypatch, site, cause):
    """EVERY cause x EVERY site: HELD, the held line carries the cause, and no merge / push / write happened."""
    g = make_graph(tmp_path, arm(monkeypatch, cause))
    held, text, effects = SITES[site](monkeypatch, g)
    assert held, f"{site} with {cause}: not HELD (fail-OPEN): {text!r}"
    assert has_cause_text(cause, text), f"{site} with {cause}: the held line does not carry the cause: {text!r}"
    assert effects == [], f"{site} with {cause}: HELD but it still acted: {effects}"


@pytest.mark.parametrize("site", sorted(SITES))
def test_a_well_formed_free_cell_proceeds_as_today(tmp_path, monkeypatch, site):
    """The control (and the build's no-blanket-refusal row): a well-formed FREE cell is NOT held, and the act happens."""
    g = make_graph(tmp_path, "free")
    held, text, effects = SITES[site](monkeypatch, g)
    assert not held, f"{site}: a free cell was HELD: {text!r}"
    assert effects != [], f"{site}: free but nothing happened ({text!r})"


@pytest.mark.parametrize("site", sorted(SITES))
def test_a_frozen_prime_holds_with_the_human_gate_text_and_does_nothing(tmp_path, monkeypatch, site):
    """A FROZEN cell holds exactly as today (HELD, FROZEN named, nothing done)."""
    g = make_graph(tmp_path, "frozen")
    held, text, effects = SITES[site](monkeypatch, g)
    assert held and "FROZEN" in text, f"{site}: {text!r}"
    assert effects == []


# ====
# F3: the callers of the gated verbs report a retired no-op honestly
# ====

RETIRED_LINE = "grid: retired (cron:crons grid_sync.enabled false); nothing written"


def _grid_commit_result(monkeypatch, tmp_path, rc, out):
    monkeypatch.setattr(rotate, "_closeout_main", lambda r: tmp_path)
    monkeypatch.setattr(rotate.subprocess, "run", lambda argv, **kw: Proc(rc, out, ""))
    return rotate._make_closeout_seams(tmp_path, {}, seat="adv")["grid_commit"]()


def test_f3_grid_commit_seam_reports_the_retired_no_op(tmp_path, monkeypatch):
    ok, res, detail = _grid_commit_result(monkeypatch, tmp_path, 0, RETIRED_LINE + "\n")
    assert "retired" in (res + " " + detail).lower(), (ok, res, detail)


def test_f3_grid_commit_seam_reports_a_real_failure_as_a_failure(tmp_path, monkeypatch):
    ok, res, detail = _grid_commit_result(monkeypatch, tmp_path, 1, "ERR: boom\n")
    assert ok is False and "committed" not in detail.lower(), (ok, res, detail)


def test_f3_grid_commit_seam_normal_success_is_as_today(tmp_path, monkeypatch):
    ok, res, detail = _grid_commit_result(monkeypatch, tmp_path, 0, "grid: 3 new version(s)\n")
    assert ok is True and res == "ok" and "retired" not in detail.lower(), (ok, res, detail)


def _button_down_line(monkeypatch, tmp_path, rc, out):
    def run(argv, **kw):
        if "rev-parse" in argv:
            return Proc(0, "season2/main\n")
        return Proc(rc, out, "")
    monkeypatch.setattr(rotate.subprocess, "run", run)
    return rotate._button_down(root=tmp_path, branch_allow=True, legal_branch="season2/main")


def test_f3_button_down_reports_the_retired_no_op(tmp_path, monkeypatch):
    line = _button_down_line(monkeypatch, tmp_path, 0, RETIRED_LINE + "\n")
    assert "retired" in line.lower() and "grid committed" not in line, line


def test_f3_button_down_reports_a_failure_not_grid_committed(tmp_path, monkeypatch):
    line = _button_down_line(monkeypatch, tmp_path, 3, "ERR: refused\n")
    assert "grid committed" not in line and ("fail" in line.lower() or "refus" in line.lower() or "rc" in line.lower()), line


def test_f3_button_down_normal_success_is_as_today(tmp_path, monkeypatch):
    line = _button_down_line(monkeypatch, tmp_path, 0, "grid: 2 new version(s)\n")
    assert line.startswith("grid committed") and "season2/main" in line, line


# ====
# negative: the lying comments are gone; no veto read is non-strict
# ====

def _src(name: str) -> str:
    return (BIN / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["rotate.py", "write.py"])
def test_the_lying_comment_is_gone(name):
    assert "a broken veto cell never" not in _src(name), f"{name} still says a broken veto cell never un-gates / gates silently / frees-silent"


@pytest.mark.parametrize("name", ["rotate.py", "write.py"])
def test_every_veto_read_and_judgement_is_strict(name):
    """Every `_veto.read(` / `is_frozen(` call carries `strict=True` or a `geom=` taken from a strict read; the ONE exemption BY NAME is rotate.py's best-effort `active_gate(_veto.read(_groot), "prime")` lookup inside the frozen branch."""
    text = _src(name)
    bad = []
    aliases = {"veto", "_veto"} | {m.group(1) or "veto" for m in re.finditer(r"from seatsig import veto(?: as (\w+))?", text)}
    for m in re.finditer(r"\b(?:" + "|".join(sorted(aliases)) + r")\.(read|is_frozen)\(", text):
        call = text[m.start(): m.start() + 200]
        line = text[:m.start()].count("\n") + 1
        if "strict=True" in call.split(")\n")[0] or "geom=" in call.split(")\n")[0]:
            continue
        if name == "rotate.py" and 'active_gate(_veto.read(_groot), "prime")' in text[max(0, m.start() - 40): m.start() + 80]:
            continue
        bad.append((name, line, call.splitlines()[0][:100]))
    assert bad == [], f"non-strict veto call sites: {bad}"
