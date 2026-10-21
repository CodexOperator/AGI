"""Proof for `season_report.py facts` (goal:g5.4.1, S1: council design 10-15, falsifiers F1 F3a-c F5 F6).

Every count is PINNED to the commit 5fa654a5f3 (the trunk at the 08:11Z ROLLOVER COMPLETE read), so a later retire cannot move it. The
heads come from a CAPTURED ls-remote (tests/fixtures/season_report/): no row touches the network. Each row has a MUTANT: a copy of
season_report.py with ONE line changed, run the same way, which must go RED.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CLI = HERE.parent / "bin" / "season_report.py"
ROOT = HERE.parents[2]
FIXTURE = HERE / "fixtures" / "season_report" / "heads-20261015T1941Z.txt"
PREV = str(3 - 1)          # the closed season: the old trunk spelling is built, never typed (lane box-move-refs, row trunk-no-live-source-file-spells-the-old-trunk)
PIN = "5fa654a5f3"
NODES = ".agi/nodes"

def _materialize() -> Path:
    """The captured ls-remote with its closed-season spelling filled in (the capture stores @PREV@), in a scratch dir."""
    d = Path(tempfile.mkdtemp(prefix="season-report-"))
    out = d / FIXTURE.name
    out.write_text(FIXTURE.read_text().replace("@PREV@", PREV))
    return out


HEADS = _materialize()

pytestmark = pytest.mark.skipif(
    subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{PIN}^{{commit}}"], capture_output=True).returncode != 0,
    reason=f"{PIN} is not in this clone (a shallow checkout)")


def _git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def _facts_raw(*extra: str, cli: Path = CLI, repo: Path = ROOT, heads: Path = HEADS, season: str = "3", at: str = PIN) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(cli), "--repo", str(repo), "facts", "--season", season, "--at", at,
                           "--heads-file", str(heads), *extra], capture_output=True)


def _facts(**kw) -> dict:
    r = _facts_raw(**kw)
    assert r.returncode == 0, r.stderr.decode()
    return json.loads(r.stdout)


def _mutant(tmp_path: Path, old: str, new: str) -> Path:
    text = CLI.read_text()
    assert text.count(old) == 1, f"mutant anchor not unique ({text.count(old)}): {old!r}"
    p = tmp_path / "season_report_mutant.py"
    p.write_text(text.replace(old, new))
    return p


def _world(repo: Path) -> tuple[str, str]:
    """What `facts` must leave alone: every ref, and the working tree's status."""
    refs = hashlib.sha1(_git(repo, "for-each-ref").encode()).hexdigest()
    return refs, _git(repo, "status", "--porcelain")


@pytest.fixture(scope="module")
def pinned() -> dict:
    return _facts()


# ---- scratch repos: tiny histories built with plain git, never the live repo -----------------------------------------------------------------
_POSTS = '---\nid: config:posts\ntype: config\nposts:\n  - {"name": "a-post", "engine": {"trunk": "core/season3/main"}}\n---\n'


def _ladder(n: int) -> dict:
    return {f"{NODES}/.geometry/ladder.md": f"---\nid: ladder:ladder\ntype: ladder\ncurrent_season: {n}\n---\n"}


class Scratch:
    def __init__(self, path: Path):
        self.path, self.ts = path, 1_760_000_000
        path.mkdir()
        self.git("init", "-q", "-b", "main")

    def git(self, *a: str, inp: str | None = None) -> str:
        self.ts += 60
        env = {"PATH": "/usr/bin:/bin", "HOME": str(self.path), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
               "GIT_AUTHOR_DATE": f"@{self.ts} +0000", "GIT_COMMITTER_DATE": f"@{self.ts} +0000"}
        r = subprocess.run(["git", "-C", str(self.path), "-c", "user.name=t", "-c", "user.email=t@t.invalid", "-c", "commit.gpgsign=false", *a],
                           input=inp, capture_output=True, text=True, env=env)
        assert r.returncode == 0, (a, r.stderr)
        return r.stdout.strip()

    def commit(self, subject: str, files: dict | None = None) -> str:
        for rel, body in (files or {}).items():
            f = self.path / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(body)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", subject)
        return self.git("rev-parse", "HEAD")

    def merge(self, subject: str, side_subject: str) -> str:
        """A --no-ff merge of a one-commit side branch into main: the merge is a FIRST-PARENT merge, the side commit is not."""
        self.git("checkout", "-q", "-b", "side")
        self.git("commit", "-q", "--allow-empty", "-m", side_subject)
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", subject, "side")
        self.git("branch", "-q", "-D", "side")
        return self.git("rev-parse", "HEAD")

    def commit_with_gpgsig_header(self, subject: str, files: dict) -> str:
        """A commit carrying a gpgsig HEADER that no key made: what a header-only reader calls 'signed'."""
        for rel, body in files.items():
            (self.path / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.path / rel).write_text(body)
        self.git("add", "-A")
        tree, parent = self.git("write-tree"), self.git("rev-parse", "HEAD")
        self.ts += 60
        raw = (f"tree {tree}\nparent {parent}\nauthor t <t@t.invalid> {self.ts} +0000\ncommitter t <t@t.invalid> {self.ts} +0000\n"
               f"gpgsig -----BEGIN PGP SIGNATURE-----\n garbage\n -----END PGP SIGNATURE-----\n\n{subject}\n")
        sha = self.git("hash-object", "-t", "commit", "-w", "--stdin", inp=raw)
        self.git("update-ref", "refs/heads/main", sha)
        self.git("reset", "-q", "--hard", sha)
        return sha


@pytest.fixture(scope="module")
def world(tmp_path_factory) -> dict:
    """Season 2 opens at c2; its window holds a LAND merge, a prose merge naming L469, a season-2-form merge and a LAND subject that sits on a
    SIDE branch; season 3 opens at a commit carrying a garbage gpgsig header; a LAND stack 31 lands after the close."""
    s = Scratch(tmp_path_factory.mktemp("world") / "repo")
    c1 = s.commit("c1: season 1", {f"{NODES}/.geometry/posts.md": _POSTS, **_ladder(1)})
    c2 = s.commit("c2: opens season 2", _ladder(2))
    s.merge("sanctuary-master: LAND stack 7 (gate tip abc)", "x: LAND stack 99 (a side-branch subject, never first-parent)")
    s.merge("belam: see L469 for the fix", "y: a side commit")
    s.merge("belam: merge season-2 L21 (8a12fdc239) into season3/main", "z: a side commit")
    c3 = s.commit_with_gpgsig_header("c3: opens season 3", _ladder(3))
    s.merge("sanctuary-master: LAND stack 31 (gate tip def)", "w: a side commit")
    return {"repo": s.path, "c1": c1, "c2": c2, "c3": c3, "later": s.git("rev-parse", "HEAD")}


# ---- F1: byte-equal reruns ---------------------------------------------------------------------------------------------------
def test_f1_two_runs_are_byte_equal_and_a_clock_in_the_json_mutant_is_red(tmp_path: Path):
    a, b = _facts_raw(), _facts_raw()
    assert a.returncode == 0 and a.stdout == b.stdout, "F1: two facts runs differ"
    assert a.stdout.endswith(b"\n") and a.stdout.count(b"\n") > 50
    mut = _mutant(tmp_path, '        "at": sha,\n', '        "at": sha, "now": time.time_ns(),\n')
    m1, m2 = _facts_raw(cli=mut), _facts_raw(cli=mut)
    assert m1.returncode == 0 and m1.stdout != m2.stdout, "MUTANT (a clock in the JSON) must be RED: its two runs must differ"


# ---- F3a: active_by_dir == an independent ls-tree count ----------------------------------------------------------------------------
def _indep_live_paths() -> list[str]:
    names = _git(ROOT, "ls-tree", "-r", "--name-only", PIN, "--", NODES).split("\n")
    return [n for n in names if n.endswith(".md") and not n.startswith(f"{NODES}/deprecated/")]


def test_f3a_active_by_dir_equals_an_independent_ls_tree_count_and_dropping_geometry_is_red(tmp_path: Path, pinned: dict):
    indep = len(_indep_live_paths())
    assert indep == 5706, "the pin moved: 5,706 live node files at 5fa654a5f3"
    assert pinned["counts"]["active_by_dir"] == indep
    assert pinned["counts"]["deprecated_by_dir"] == 239
    mut = _mutant(tmp_path, '        dep = parts[2] == "deprecated"\n',
                  '        dep = parts[2] == "deprecated"\n        if parts[2] == ".geometry":\n            continue\n')
    got = _facts(cli=mut)["counts"]["active_by_dir"]
    assert got == 5682 and got != indep, f"MUTANT (.geometry dropped) must be RED: {got} vs {indep}"


# ---- F3b: active_by_status == an independent git grep -L ---------------------------------------------------------------------------
def test_f3b_active_by_status_equals_an_independent_git_grep_l(pinned: dict):
    out = _git(ROOT, "grep", "-L", "-E", "^status: *\"?deprecated\"?[ \t]*$", PIN, "--", f"{NODES}/*.md", f":(exclude){NODES}/deprecated/*")
    indep = len([ln for ln in out.split("\n") if ln])
    assert indep == 5700
    assert pinned["counts"]["active_by_status"] == indep


# ---- F3c: the mismatch list == |F3a - F3b| == 6 --------------------------------------------------------------------------------------
def test_f3c_the_mismatch_list_has_six_ids_and_dropping_the_list_is_red(tmp_path: Path, pinned: dict):
    c = pinned["counts"]
    assert len(c["status_dir_mismatch"]) == 6 == c["active_by_dir"] - c["active_by_status"]
    assert c["status_dir_mismatch"] == sorted(["doc:lm-town-trajectory", "experiment:a00-3a7d5c8c-46ee39", "experiment:a01-545f623d-6d71d2",
                                               "hypothesis:a00-500a23f5-f8c142", "hypothesis:a00-655e37e2-87cfb0", "hypothesis:a01-98e872ef-bd5f40"])
    mut = _mutant(tmp_path, '"status_dir_mismatch": sorted(mismatch),', '"status_dir_mismatch": [],')
    m = _facts(cli=mut)["counts"]
    assert len(m["status_dir_mismatch"]) == 0 != c["active_by_dir"] - c["active_by_status"], "MUTANT (list dropped) must be RED: 0 vs 6"


# ---- B-a / B-b: the counts reconcile with the engine, and every id and type is the frontmatter's -------------------------------------------
def _node(nid: str, typ: str, status: str) -> str:
    return f"---\nid: {nid}\ntype: {typ}\nstatus: {status}\n---\nbody\n"


def test_b_a_engine_active_equals_the_metrics_rule_and_the_second_mismatch_list_is_read(tmp_path: Path, pinned: dict):
    c = pinned["counts"]
    total = len([n for n in _git(ROOT, "ls-tree", "-r", "--name-only", PIN, "--", NODES).split("\n") if n.endswith(".md")])
    out = _git(ROOT, "grep", "-l", "-E", "^status: *\"?deprecated\"?[ \t]*$", PIN, "--", f"{NODES}/*.md")
    marked = len([ln for ln in out.split("\n") if ln])
    assert (total, marked) == (5945, 245) and c["engine_active"] == total - marked == 5700, "metrics.py's rule: every node .md minus the status-deprecated ones"
    assert c["deprecated_status_mismatch"] == [] and c["ids_from_path"] == []
    s = Scratch(tmp_path / "nodes")
    at = s.commit("nodes", {
        f"{NODES}/.geometry/posts.md": _POSTS, **_ladder(3),
        f"{NODES}/idea/a.md": _node("idea:a", "idea", "active"),
        f"{NODES}/idea/b.md": _node("idea:b", "idea", "deprecated"),                 # a live-dir file marked deprecated
        f"{NODES}/deprecated/idea/c.md": _node("idea:c", "idea", "active"),         # a deprecated/ file NOT marked
        f"{NODES}/deprecated/idea/d.md": _node("idea:d", "idea", "deprecated"),
        f"{NODES}/idea/noid.md": "---\ntype: idea\nstatus: active\n---\nbody\n",    # no id: the path spells it, flagged
        f"{NODES}/.geometry/x.md": _node("config:x", "config", "deprecated")})
    f = json.loads(_facts_raw(repo=s.path, at=at).stdout)["counts"]
    assert f["status_dir_mismatch"] == ["config:x", "idea:b"] and f["deprecated_status_mismatch"] == ["idea:c"]
    assert (f["active_by_dir"], f["active_by_status"], f["deprecated_by_dir"], f["engine_active"]) == (6, 4, 2, 5)
    assert f["ids_from_path"] == ["idea:noid"]
    assert f["by_type"] == {"idea": 3, "config": 2, "ladder": 1} and ".geometry" not in f["by_type"]       # B-b: .geometry stays counted, under its frontmatter type
    assert not any(i.startswith(".geometry") for i in f["status_dir_mismatch"]), "an id was spelled from the path"
    for old, new_, check in (
            ('"deprecated_status_mismatch": sorted(dep_mismatch),', '"deprecated_status_mismatch": [],', lambda c_: c_["deprecated_status_mismatch"] == []),
            ('"engine_active": len(files) - status_deprecated,', '"engine_active": live - status_deprecated,', lambda c_: c_["engine_active"] != 5),
            ('        typ = _fm_scalar(fm, "type") or (nid.split(":", 1)[0] if ":" in nid else tdir)\n', '        typ = tdir\n', lambda c_: ".geometry" in c_["by_type"]),
            ('        nid = _fm_scalar(fm, "id")\n', '        nid = None\n', lambda c_: ".geometry:x" in c_["status_dir_mismatch"])):
        mut = _mutant(tmp_path, old, new_)
        assert check(json.loads(_facts_raw(cli=mut, repo=s.path, at=at).stdout)["counts"]), f"MUTANT {old.strip()[:50]!r} must be RED"


# ---- F5 NEGATIVE: facts changes no ref and no working-tree status ------------------------------------------------------------------------
def test_f5_facts_leaves_every_ref_and_the_status_unchanged_and_a_ref_writing_mutant_is_red(tmp_path: Path):
    # the live repo's refs move under other posts' commits, so the ref digest is proved on a FROZEN throwaway clone (below);
    # the status of THIS checkout is proved in place
    status = _git(ROOT, "status", "--porcelain")
    assert _facts_raw().returncode == 0
    assert _git(ROOT, "status", "--porcelain") == status, "F5: facts changed the working-tree status"
    # the mutant writes a ref: only ever into a THROWAWAY shared clone, never the live repo
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "-n", "--shared", str(ROOT), str(clone)], check=True, capture_output=True)
    mut = _mutant(tmp_path, '    tree = read_tree(repo, sha)\n', '    _git(repo, "update-ref", "refs/mutant/x", sha)\n    tree = read_tree(repo, sha)\n')
    w0 = _world(clone)
    assert _facts_raw(repo=clone).returncode == 0 and _world(clone) == w0, "the unmutated script must leave the clone alone"
    assert _facts_raw(cli=mut, repo=clone).returncode == 0
    assert _world(clone) != w0, "MUTANT (facts writes a ref) must be RED: the refs digest must change"


# ---- F6: the type rows sum to active_by_dir -----------------------------------------------------------------------------------------------
def test_f6_the_type_rows_sum_to_active_by_dir_and_dropping_other_is_red(tmp_path: Path, pinned: dict):
    c = pinned["counts"]
    rows = c["type_rows"]
    assert sum(r["nodes"] for r in rows) == c["active_by_dir"], "F6: the rows must sum to active_by_dir"
    assert rows[-1] == {"type": "other", "label": "other (9 types)", "types": 9, "nodes": 106, "pct": "4.5"}   # .geometry counted under its frontmatter types
    assert len(rows) == 10 and sum(c["by_type"].values()) == c["active_by_dir"]
    mut = _mutant(tmp_path, "    if rest:\n", "    if False:\n")
    m = _facts(cli=mut)["counts"]
    gap = m["active_by_dir"] - sum(r["nodes"] for r in m["type_rows"])
    assert gap == 106 != 0, f"MUTANT (the other row dropped) must be RED: the rows then miss {gap} nodes"


# ---- the other sources, pinned ---------------------------------------------------------------------------------------------------------------
OPEN2, OPEN3 = "80908a5575", "7caa699a07"       # the ladder-cell commits that opened seasons 2 and 3 (committer 06:24:17Z 10-15)


def test_posts_cells_and_close_read_at_the_pin(pinned: dict):
    assert pinned["at"].startswith(PIN) and pinned["season"] == 3
    assert (pinned["posts_named"], pinned["trunk_cells"]) == (33, 14)
    assert pinned["trunks"] == {"core/season3/main": 14}
    assert pinned["cells"]["ladder_current_season"] == "3" and pinned["cells"]["opened"] == "2026-10-15T06:23:30Z"
    assert pinned["close"]["value"] == "2026-10-15T06:24:17Z" and pinned["close"]["sha"].startswith(OPEN3)
    assert pinned["close"]["signed"] == (_git(ROOT, "log", "-1", "--format=%G?", OPEN3).strip() == "G")      # verified by git, never a header read
    assert pinned["close"]["label"].startswith("season 2 closed")
    assert pinned["goals"]["total"] == 699 and pinned["goals"]["by_season_status"]["3:horizon"] == 2


# ---- R1: the ledger is season N-1's window [open(N-1), open(N)), whatever --at is -------------------------------------------------------
def test_r1_the_ledger_window_ends_at_the_close_not_at_the_at_commit_and_a_to_at_mutant_is_red(tmp_path: Path, pinned: dict):
    led = pinned["ledger"]
    assert led["from"].startswith(OPEN2) and led["to"].startswith(OPEN3) and "[open(season 2), open(season 3))" in led["window"]
    assert led["commits"] == int(_git(ROOT, "rev-list", "--count", f"{OPEN2}^..{OPEN3}^")) == 20573 and led["commits"] == led["signed"] + led["unsigned"]
    at_close = json.loads(_facts_raw(at=OPEN3).stdout)["ledger"]
    assert at_close == led, "R1: --at moved the ledger (it must only name the tree the other sources are read at)"
    mut = _mutant(tmp_path, '    rng = [f"{cur[\'sha\']}^"] +', '    rng = [sha] +')
    assert json.loads(_facts_raw(cli=mut).stdout)["ledger"]["commits"] > led["commits"], "MUTANT (window ends at --at) must be RED: it then counts past the close"
    assert json.loads(_facts_raw(cli=mut).stdout)["ledger"] != json.loads(_facts_raw(cli=mut, at=OPEN3).stdout)["ledger"], "MUTANT: the ledger then moves with --at"


# ---- R2: names come from first-parent LAND merges only ---------------------------------------------------------------------------------
def test_r2_names_are_the_first_parent_land_merges_and_the_two_shape_and_prose_mutants_are_red(tmp_path: Path, pinned: dict):
    indep = set()
    for s in _git(ROOT, "log", "--first-parent", "--merges", "--format=%s", f"{OPEN3}^", f"^{OPEN2}^").split("\n"):
        m = re.match(r"^[A-Za-z0-9_.-]+: (?:LAND stack|merge (?:season-\d+ )?L)\s?(\d+)\b", s)
        if m:
            indep.add(int(m.group(1)))
    names = pinned["ledger"]["names"]
    assert names == [f"L{n}" for n in sorted(indep)] and len(names) == 19 and names[0] == "L6" and "L23" not in names
    assert not {"L47", "L159", "L220", "L236", "L469", "S35"} & set(names), "a prose mention leaked into names"
    gone = _mutant(tmp_path, "(_LAND.match(s) or _LFORM.match(s),)", "(_LFORM.match(s),)")
    assert json.loads(_facts_raw(cli=gone).stdout)["ledger"]["names"][0] == "L17", "MUTANT (the LAND shape dropped) must be RED: L6..L16 vanish"


def test_r2_on_a_scratch_history_prose_and_side_branch_subjects_never_name_a_stack(tmp_path: Path, world: dict):
    led = json.loads(_facts_raw(repo=world["repo"], at=world["c3"], heads=HEADS).stdout)["ledger"]
    assert led["names"] == ["L7", "L21"], "LAND stack 7 and the season-2 form count; 'see L469' and the side-branch 'LAND stack 99' do not"
    prose = _mutant(tmp_path, "(_LAND.match(s) or _LFORM.match(s),)", "(re.search(r'\\bL(\\d+)\\b', s),)")
    m = json.loads(_facts_raw(cli=prose, repo=world["repo"], at=world["c3"]).stdout)["ledger"]["names"]
    assert "L469" in m, "MUTANT (any L<n> in a subject) must be RED: the prose mention then names a stack"


def test_r1_on_a_scratch_history_a_later_trunk_commit_leaves_the_ledger_byte_equal(world: dict):
    a = _facts_raw(repo=world["repo"], at=world["c3"]).stdout
    b = _facts_raw(repo=world["repo"], at=world["later"]).stdout
    la, lb = json.loads(a)["ledger"], json.loads(b)["ledger"]
    assert la == lb and la["to"] == world["c3"] and la["from"] == world["c2"] and la["names"] == ["L7", "L21"], "R1: a LAND stack 31 after the close entered the ledger"


# ---- R4: 'signed' is what git VERIFIES ------------------------------------------------------------------------------------------------
def test_r4_a_garbage_gpgsig_header_is_not_signed_and_a_header_reading_mutant_is_red(tmp_path: Path, world: dict):
    c = json.loads(_facts_raw(repo=world["repo"], at=world["c3"]).stdout)
    assert c["close"]["signed"] is False and "UNVERIFIED ladder-cell commit" in c["close"]["label"]
    assert c["ledger"]["signed_label"] == "signature header (not verified)" and c["ledger"]["signed"] == 0     # the close commit is OUT of its own window; the count is labelled a header count
    mut = _mutant(tmp_path, '    verified = _git(repo, "log", "-1", "--format=%G?", c["sha"]).decode().strip() == "G"', '    verified = c["signed"]')
    m = json.loads(_facts_raw(cli=mut, repo=world["repo"], at=world["c3"]).stdout)["close"]
    assert m["signed"] is True, "MUTANT (the header is read, not verified) must be RED: the garbage header then reads 'signed'"


# ---- R5: an empty window is not recorded, never all of history ---------------------------------------------------------------------------
def test_r5_a_ladder_that_never_held_the_previous_season_reads_not_recorded_and_the_guard_mutant_is_red(tmp_path: Path):
    s = Scratch(tmp_path / "gap")
    s.commit("c1", {f"{NODES}/.geometry/posts.md": _POSTS, **_ladder(1)})
    at = s.commit("c2: jumps to season 3", _ladder(3))
    r = _facts_raw(repo=s.path, at=at)
    assert r.returncode == 0 and json.loads(r.stdout)["ledger"] == {"value": "not recorded"}
    mut = _mutant(tmp_path, "    if prev is None or cur is None or _parent", "    if cur is None or _parent")
    m = _facts_raw(cli=mut, repo=s.path, at=at)
    assert not (m.returncode == 0 and json.loads(m.stdout)["ledger"] == {"value": "not recorded"}), "MUTANT (no empty-window guard) must be RED"


def test_heads_and_archives_come_from_the_captured_file_by_the_named_rule(pinned: dict):
    g = pinned["grid"]
    assert g["read_time"] == "2026-10-15T19:41:33Z"
    assert len(g["heads"]) == 20 and g["archives_total"] == 43
    assert [a["name"] for a in g["archives"]] == [
        "core-main-pre-20261015T0809Z", f"local-maxxing/season{PREV}/main", "sanctuary-main-pre-20261015T0809Z", f"sanctuary/season{PREV}/main",
        f"season{PREV}/main", "streaming-suite-main-pre-20261015T0809Z", f"streaming-suite/season{PREV}/main", "web-app-suite-main-pre-20261015T0809Z",
        f"web-app-suite/season{PREV}/main"]
    assert all(h["short"] == h["sha"][:10] for h in g["heads"] + g["archives"])


def test_a_heads_file_without_a_read_time_first_line_is_refused_rc2(tmp_path: Path):
    bad = tmp_path / "heads.txt"
    bad.write_text("dc7ec920bafd2c117a269beb3356988f4f3ec859\trefs/heads/master\n")
    r = _facts_raw(heads=bad)
    assert r.returncode == 2 and r.stdout == b"" and b"read time" in r.stderr


def test_r3_a_malformed_or_empty_heads_file_is_refused_rc2_and_a_skipping_mutant_is_red(tmp_path: Path):
    ok = "dc7ec920bafd2c117a269beb3356988f4f3ec859\trefs/heads/master"
    for body in (f"2026-10-15T19:41:33Z\n{ok}\ngarbage line here\n", "2026-10-15T19:41:33Z\n", f"2026-10-15T19:41:33Z\n{ok}\n\n{ok}\n",
                 f"2026-10-15T19:41:33Z\n{ok[:30]}\trefs/heads/short\n"):
        bad = tmp_path / "heads.txt"
        bad.write_text(body)
        r = _facts_raw(heads=bad)
        assert r.returncode == 2 and r.stdout == b"" and b"--heads-file" in r.stderr, body
    good = tmp_path / "good.txt"
    good.write_text(f"2026-10-15T19:41:33Z\n{ok}\n")
    assert _facts_raw(heads=good).returncode == 0
    bad.write_text(f"2026-10-15T19:41:33Z\n{ok}\ngarbage line here\n")
    mut = _mutant(tmp_path, '        if not _HEADLINE.match(ln):\n            raise Fail(f"--heads-file: line {n} is not <40 hex sha><TAB><ref>")\n',
                  '        if not _HEADLINE.match(ln):\n            continue\n')
    assert _facts_raw(cli=mut, heads=bad).returncode == 0, "MUTANT (a garbage line skipped) must be RED: rc 0 then"


def test_box_facts_absent_reads_not_recorded_and_a_present_value_carries_its_provenance(tmp_path: Path, pinned: dict):
    assert all(v == {"value": "not recorded"} for v in pinned["box"].values()) and len(pinned["box"]) == 7
    ok = tmp_path / "box.json"
    ok.write_text(json.dumps({"run_rc": {"value": 0, "command": "season.py rollover --global --apply", "reader_uid": "a-seat",
                                         "read_time": "2026-10-15T06:24:00Z"}}))
    b = json.loads(_facts_raw("--box-facts", str(ok)).stdout)["box"]
    assert b["run_rc"] == {"value": 0, "command": "season.py rollover --global --apply", "reader_uid": "a-seat", "read_time": "2026-10-15T06:24:00Z"}
    assert b["pin"] == {"value": "not recorded"}
    stale = {"run_rc": {"value": 0, "command": "c", "reader_uid": "a-seat", "read_time": "yesterday"}}
    for bad in (stale, {"run_rc": {"value": 0}}, {"run_rc": 0}, {"not_a_key": {"value": 1, "command": "c", "reader_uid": "u", "read_time": "t"}}):
        p = tmp_path / "bad.json"
        p.write_text(json.dumps(bad))
        r = _facts_raw("--box-facts", str(p))
        assert r.returncode == 2 and r.stdout == b"", bad
    mut = _mutant(tmp_path, '        if not _TIME.match(str(v["read_time"])):\n', '        if False:\n')
    p.write_text(json.dumps(stale))
    assert _facts_raw("--box-facts", str(p), cli=mut).returncode == 0, "MUTANT (read_time unchecked) must be RED"


def test_the_script_and_its_fixture_name_no_host_and_no_home_path():
    for p in (CLI, FIXTURE):
        for needle in ("/ho" + "me/", "/var/" + "lib/agi", "/da" + "ta/work"):    # spelled in parts so this file is not its own hit
            assert needle not in p.read_text(), (p.name, needle)


# ---- P1: the template's slots all resolve against the facts it is rendered from ----------------------------------------------------------
TEMPLATE = HERE.parent / "templates" / "season_report" / "report.html"
_TOKEN = re.compile(r"\{\{(#rows |/rows|#media|/media)?\s*([^}|]*?)\s*(?:\|(\w+))?\}\}")
_ROW_NARRATIVE = {"role"}          # a heads row's role column is written by the narrative, not read from facts


def _resolve(root, path: str):
    cur = root
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return KeyError
        cur = cur[part]
    return cur


def _template_problems(text: str, facts: dict) -> list[str]:
    """The slot grammar legend (an HTML comment) is not part of the page. Every slot is `facts.*` (a scalar that exists), `narr.*`, `media.*` (both inside {{#media}} only for media), or `row.*` inside a loop."""
    out, stack, media = [], [], 0
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in _TOKEN.finditer(text):
        kind, path, flt = m.group(1), m.group(2), m.group(3)
        if kind == "#rows ":
            if path.startswith("facts."):
                lst = _resolve(facts, path[6:])
                if not isinstance(lst, list) or not lst:
                    out.append(f"rows over {path}: not a non-empty list in the facts")
                stack.append(lst[0] if isinstance(lst, list) and lst else {})
            elif path.startswith("narr."):
                stack.append(None)
            else:
                out.append(f"rows over {path}: must be facts.* or narr.*")
                stack.append(None)
        elif kind == "/rows":
            if not stack:
                out.append("{{/rows}} without an open loop")
            else:
                stack.pop()
        elif kind == "#media":
            media += 1
        elif kind == "/media":
            media -= 1
        elif path.startswith("facts."):
            v = _resolve(facts, path[6:])
            if v is KeyError or isinstance(v, (dict, list)):
                out.append(f"{path}: unresolved or not a scalar")
            elif flt == "n" and not isinstance(v, int):
                out.append(f"{path}|n: not an integer")
        elif path.startswith("row."):
            if not stack:
                out.append(f"{path}: outside a loop")
            elif stack[-1] is not None and path[4:] not in stack[-1] and path[4:] not in _ROW_NARRATIVE:
                out.append(f"{path}: the facts row has no such field")
        elif path.startswith("media."):
            if media <= 0:
                out.append(f"{path}: media slot outside {{{{#media}}}}")
        elif not path.startswith("narr."):
            out.append(f"unknown slot {m.group(0)}")
    if stack:
        out.append("a {{#rows}} loop is never closed")
    if media != 0:
        out.append("{{#media}} is unbalanced")
    return out


def test_p1_every_template_slot_resolves_in_the_facts_and_a_typo_mutant_is_red(pinned: dict):
    text = TEMPLATE.read_text()
    assert _template_problems(text, pinned) == []
    assert len(_TOKEN.findall(text)) > 50
    bad = text.replace("{{facts.counts.active_by_dir|n}}", "{{facts.counts.active_by_dr|n}}")
    assert bad != text and _template_problems(bad, pinned) != [], "MUTANT (a typo'd slot) must be RED"
    bad2 = text.replace("{{/rows}}\n  </ol>", "  </ol>", 1)
    assert bad2 != text
    assert _template_problems(bad2, pinned) != [], "MUTANT (an unclosed loop) must be RED"
    bad3 = text.replace("{{#media}}\n  <div", "  <div", 1)
    assert bad3 != text
    assert _template_problems(bad3, pinned) != [], "MUTANT (an unbalanced media block) must be RED"


def test_p1_the_template_carries_no_typed_sha_and_no_seed_number_and_keeps_the_player_inside_the_media_block():
    text = TEMPLATE.read_text()
    standing = re.sub(r"\{\{.*?\}\}", "", text)
    assert not re.search(r"\b[0-9a-f]{7,40}\b", standing), "a typed sha outside a slot"
    for seed in ("2a8056bcb5", "420e00ae9c", "5fa654a5f3", "5,706", "06:24", "08:10Z", "grok", "song-b.mp3", "Lyria"):
        assert seed not in text, f"seed literal {seed!r} left in the template"
    # the player: its <audio>, its button and its <script> exist ONLY between {{#media}} and {{/media}}
    outside = re.sub(r"\{\{#media\}\}.*?\{\{/media\}\}", "", text, flags=re.S)
    for tag in ("<audio", 'id="play"', "<script", "class=\"player\""):
        assert tag not in outside, f"{tag} sits outside the media block"
    assert "<style>" in text and "--accent:#0d6b62" in text, "the seed's style block is kept"
    assert "<title>Season {{facts.season}} Rollover</title>" in text


def test_p1_a_player_outside_the_media_block_mutant_is_red():
    text = TEMPLATE.read_text()
    mut = text.replace("{{#media}}\n  <div class=\"player\"", "  <div class=\"player\"", 1)
    outside = re.sub(r"\{\{#media\}\}.*?\{\{/media\}\}", "", mut, flags=re.S)
    assert 'class="player"' in outside, "MUTANT (player pulled out of the media block) must be RED"
