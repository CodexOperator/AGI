"""Conjuncts (1) and (2) of hypothesis:cron-layer-keeps-its-disk-footprint-bounded,
and the quiet half of (3).

(1) a DECLARED maintenance job holds `.git/objects` within 1.5x of a fresh full
    repack — measured here on a fixture repo that actually carries duplicate
    entries, by running the command the crons NODE declares, not a command
    this test invents;
(2) every file in the logs dir — the cron log AND the reaper log — stays under
    `logs.cap_mb` with `logs.rotations` copies kept;
(3) a no-op apply writes at most one line.

No test here touches the real crontab, the real logs dir or the real
user manager: `HOME` is redirected into tmp, every apply goes through
`--crontab-file`.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

CADENCES = {
    "grid_sync": {"every_mins": 5, "enabled": True},
    "branch_push": {"schedule": "7 * * * *", "enabled": True},
    "maint_gc": {
        "schedule": "41 4 * * *", "enabled": True,
        "cmd": "git -C {repo_root} gc --quiet",
    },
}


BOX_SCHEMA = """---
name: box
structural: true
fields:
  root: {type: str}
  logs_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  logs: logs_dir
  tmux: tmux_session
  user: user
  repo_root: repo_root
  box: box
---
"""


@pytest.fixture(autouse=True)
def redirected_home(tmp_path, monkeypatch):
    """NEVER let a test in this file see the real `~/logs`.

    `enforce_log_caps` deliberately has no `--logs-dir` seam — it works on the
    same directory the rendered lines write to — so `HOME` is the seam. Without
    this, a test that declares `logs` cells rotates the REAL reaper log. (A
    first draft of this file did exactly that, on this box, at 02:39Z.)
    """
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return home


def _git(path: Path, *args: str) -> str:
    res = subprocess.run(["git", *args], cwd=path, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args}: {res.stderr}")
    return res.stdout.strip()


def make_project(tmp_path, cells=None) -> Path:
    """A project root that IS the graph repo, with a crons node and a config.

    `cells` becomes the top-level `logs` namespace of `.agi/config.json`
    (None = the namespace is ABSENT, which must be a no-op, not a crash).
    """
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    fm = {"id": "cron:crons", "type": "cron", "crons_live": True,
          "cadences": CADENCES}
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")
    cfg = {} if cells is None else {"logs": cells}
    (root / "agi-tree.config.json").write_text(json.dumps(cfg))
    sch = root / "context" / "schemas"
    sch.mkdir(parents=True)
    (sch / "[box].md").write_text(BOX_SCHEMA)
    _git(root, "init", "-q", "-b", "master")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    (root / "keep").write_text("x")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "init")
    return root


def pack_bytes(repo: Path) -> int:
    """Bytes the repo's PACKS occupy -- the number the object-store claim is
    about. `.idx`/`.rev` sidecars are excluded: they are a fixed per-object
    index, not duplicated content, and counting them makes a SMALL fixture
    look like a duplicate-heavy one for the wrong reason."""
    packdir = repo / ".git" / "objects" / "pack"
    return sum(p.stat().st_size for p in packdir.glob("*.pack")) if packdir.is_dir() else 0


def repack_size(repo: Path) -> int:
    """Bytes a FRESH full repack would produce — the falsifier's denominator."""
    listing = _git(repo, "rev-list", "--objects", "--all")
    res = subprocess.run(["git", "-C", str(repo), "pack-objects", "--stdout"],
                         input=listing.encode(), capture_output=True, cwd=repo)
    return len(res.stdout)


def declared_cmd_lines(root: Path) -> list[str]:
    root_, _, repo_root, engine_root, node = crons._resolve(root)
    return crons.render_managed_lines(root_, repo_root, engine_root, node)


# --- (1) the declared maintenance job holds objects near a fresh repack ----


def test_declared_maintenance_job_lands_the_gc_line(tmp_path):
    root = make_project(tmp_path)
    lines = [l for l in declared_cmd_lines(root) if " gc " in l or l.endswith("gc")]
    assert len(lines) == 1, lines
    assert lines[0].startswith("41 4 * * * cd ")
    assert f"git -C {root} gc" in lines[0]


def test_maintenance_job_keeps_objects_within_1_5x_of_a_fresh_repack(tmp_path):
    """The claim, measured: after the DECLARED job runs, the object store is
    within 1.5x of what a full repack would cost.

    The fixture is built to have the defect the box had: 60 commits whose
    trees carry the same payload blob over and over, so the incremental packs
    hold 60x the entries for 1 unique blob.
    """
    root = make_project(tmp_path)
    payload = random.Random(0).randbytes(40000)  # incompressible: a dup is a real cost
    for i in range(60):
        (root / "n.txt").write_text(str(i))
        (root / "f.txt").write_bytes(payload)  # SAME payload, 60 times over
        _git(root, "add", "n.txt", "f.txt")
        _git(root, "commit", "-q", "-m", f"c{i}")
    # Pre-shape: pack what is there, then add more so a pack holds duplicates.
    _git(root, "gc", "-q")
    for i in range(60, 90):
        (root / "m.txt").write_text(str(i))
        (root / "g.txt").write_bytes(payload + str(i).encode())
        _git(root, "add", "m.txt", "g.txt")
        _git(root, "commit", "-q", "-m", f"d{i}")
    # The box's shape: SEVERAL packs, none of them a full repack (the grid
    # writes with plumbing, so nothing ever merged them). `repack` without
    # `-d` adds a second pack and keeps the first.
    _git(root, "repack", "-q")
    packs = lambda: len(list((root / ".git/objects/pack").glob("*.pack")))  # noqa: E731
    before = pack_bytes(root) / repack_size(root)
    assert packs() == 2, f"fixture should hold two packs, holds {packs()}"

    line = [l for l in declared_cmd_lines(root) if " gc" in l][0]
    body = line.split(" && ", 1)[1]
    subprocess.run(body, shell=True, cwd=root, check=True)

    after = pack_bytes(root) / repack_size(root)
    assert packs() == 1, f"the declared job must leave ONE pack, left {packs()}"
    assert after <= 1.5, (f"packs/repack before {before:.2f}, after {after:.2f}")


# --- (2) every logs file under a declared cap, with declared rotations ----


def test_over_cap_log_is_rotated_and_older_copies_leave(tmp_path,
                                                         redirected_home):
    home = redirected_home
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 2})
    logs = home / "logs"
    big = logs / "agi-crons-proj-aaaaaaaa.log"
    big.write_bytes(b"a" * (2 * 1024 * 1024))
    # The reaper log lives in the SAME dir and is NOT this project's cron log:
    # it must be covered by the same cap.
    reap = logs / "agi-reaper-agi-2f118e6f.log"
    reap.write_bytes(b"b" * (2 * 1024 * 1024))
    small = logs / "quiet.log"
    small.write_text("one line\n")

    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert len(out) == 2, out
    for name in (big.name, reap.name):
        assert (logs / name).stat().st_size == 0
        assert (logs / f"{name}.1").stat().st_size == 2 * 1024 * 1024
    assert small.read_text() == "one line\n"
    assert not (logs / f"{small.name}.1").exists()

    # A second breach rotates again, and the OLDEST copy leaves: with
    # rotations=2 there are never more than 2 archives.
    big.write_bytes(b"c" * (2 * 1024 * 1024))
    crons.enforce_log_caps(root, root, dry_run=False)
    crons.enforce_log_caps(root, root, dry_run=False)
    assert not (logs / f"{big.name}.3").exists()
    assert (logs / f"{big.name}.1").is_file()
    assert (logs / f"{big.name}.2").is_file()


def test_dry_run_reports_the_breach_and_touches_nothing(tmp_path,
                                                         redirected_home):
    home = redirected_home
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 1})
    big = home / "logs" / "agi-reaper-agi-2f118e6f.log"
    big.write_bytes(b"a" * (2 * 1024 * 1024))
    out = crons.enforce_log_caps(root, root, dry_run=True)
    assert len(out) == 1 and "dry-run" in out[0]
    assert big.stat().st_size == 2 * 1024 * 1024
    assert not (home / "logs" / f"{big.name}.1").exists()


def test_absent_cells_are_a_noop_and_malformed_cells_raise_by_name(
        tmp_path, monkeypatch, redirected_home):
    home = redirected_home
    big = home / "logs" / "agi-reaper-agi-2f118e6f.log"
    big.write_bytes(b"a" * (2 * 1024 * 1024))

    undeclared = make_project(tmp_path / "a", cells=None)
    assert crons.enforce_log_caps(undeclared, undeclared) == []
    assert big.stat().st_size == 2 * 1024 * 1024

    bad = make_project(tmp_path / "b", {"cap_mb": 0, "rotations": 2})
    try:
        crons.enforce_log_caps(bad, bad)
    except crons.CronsError as exc:
        assert "logs.cap_mb" in str(exc)
    else:
        raise AssertionError("a cap of 0 MB must be refused by name")


def test_apply_enforces_the_cap_through_its_own_command(tmp_path, monkeypatch,
                                                        capsys,
                                                        redirected_home):
    home = redirected_home
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 1})
    big = home / "logs" / "agi-reaper-agi-2f118e6f.log"
    big.write_bytes(b"a" * (2 * 1024 * 1024))
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    rc = crons.main(["apply", "--root", str(root), "--crontab-file", str(fixture)])
    assert rc == 0
    assert big.stat().st_size == 0
    assert "rotated" in capsys.readouterr().out


# --- (3) a no-op cycle writes at most one line -----------------------------


def test_a_noop_apply_writes_exactly_one_line(tmp_path, capsys,
                                              redirected_home):
    root = make_project(tmp_path, cells={"cap_mb": 1, "rotations": 1})
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    argv = ["apply", "--root", str(root), "--crontab-file", str(fixture)]
    assert crons.main(argv) == 0
    installed = len(capsys.readouterr().out.strip().splitlines())
    assert crons.main(argv) == 0
    out = capsys.readouterr().out
    assert out.strip().splitlines() == [
        f"crons: no-op — the crontab already matches the node "
        f"({installed - 1} line(s))"], out
    assert os.path.isfile(fixture)


# --- (2) the cap enforcement is ITSELF bounded ---------------------------
#
# A ROTATED ARCHIVE lives in the same dir and is the same size as the log it
# came from, so an enforcement that globs `*` and rotates whatever is over the
# cap rotates its own archives too: `x.log` -> `x.log.1` -> `x.log.1.1` -> ...
# One more nesting level per apply, forever. The cap then GROWS the footprint
# it was declared to bound.


def _names(logs: Path) -> list[str]:
    return sorted(p.name for p in logs.iterdir())


def test_n_applies_leave_exactly_one_base_plus_n_rotations(tmp_path,
                                                           redirected_home):
    """The claim: N applies over one over-cap log leave `1 + rotations` paths.

    The shipped code leaves seven (with rotations=3) and adds a nesting level
    every apply. This cannot have passed before the repair: the assertion is on
    the PATH SET, not on any one file's size.
    """
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 3})
    big = logs / "x.log"
    big.write_bytes(b"a" * (2 * 1024 * 1024))
    for _ in range(3):
        big.write_bytes(b"a" * (2 * 1024 * 1024))
        crons.enforce_log_caps(root, root, dry_run=False)
    assert _names(logs) == ["x.log", "x.log.1", "x.log.2", "x.log.3"]
    assert big.stat().st_size == 0  # the LAST apply rotated it, once
    assert (logs / "x.log.3").stat().st_size == 2 * 1024 * 1024
    assert not list(logs.glob("*.1.*")), "a rotation rotated a rotation"


def test_a_base_exactly_at_the_cap_is_left_alone(tmp_path, redirected_home):
    """Boundary DECLARED: over-cap is strictly `>`; at the cap is kept."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 2})
    at = logs / "at.log"
    at.write_bytes(b"a" * (1024 * 1024))
    assert crons.enforce_log_caps(root, root, dry_run=False) == []
    assert _names(logs) == ["at.log"]


def test_rotations_zero_truncates_in_place_and_keeps_one_path(tmp_path,
                                                              redirected_home):
    """Boundary DECLARED: `rotations: 0` means no archive is kept -- the log
    is emptied in place, so the dir holds ONE path, forever."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 0})
    big = logs / "x.log"
    for _ in range(3):
        big.write_bytes(b"a" * (2 * 1024 * 1024))
        crons.enforce_log_caps(root, root, dry_run=False)
    assert _names(logs) == ["x.log"]
    assert big.stat().st_size == 0


def test_an_archive_named_like_one_from_outside_is_never_rotated_as_a_base(
        tmp_path, redirected_home):
    """Boundary DECLARED: `<x>.1` is an ARCHIVE by shape wherever it came
    from. It is pruned by its own base's rotation shift (or deleted as the
    oldest slot), never rotated into `<x>.1.1`."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 2})
    orphan = logs / "external.log.1"
    orphan.write_bytes(b"a" * (2 * 1024 * 1024))
    for _ in range(3):
        crons.enforce_log_caps(root, root, dry_run=False)
    assert not list(logs.glob("*.1.*"))


def test_a_legacy_nested_residue_is_pruned_not_rotated(tmp_path,
                                                        redirected_home):
    """Boundary DECLARED: `x.log.1.1` can only be residue of the pre-fix
    unbounded enforcement. It is DELETED, not rotated deeper -- the footprint
    it left shrinks, monotonically, on the next apply."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 3})
    (logs / "old.log.1.1.1").write_bytes(b"a" * (2 * 1024 * 1024))
    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert not (logs / "old.log.1.1.1").exists()
    assert any("residue" in line for line in out), out
    assert crons.enforce_log_caps(root, root, dry_run=True) == []


def test_a_directory_and_a_symlink_in_the_logs_dir_are_left_alone(
        tmp_path, redirected_home):
    """Boundary DECLARED: a subdirectory is not a log; a symlink is an
    operator's link to somewhere else, and rotating it would sever it (and
    truncating it would empty the target). Neither is touched."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 2})
    elsewhere = tmp_path / "elsewhere.log"
    elsewhere.write_bytes(b"a" * (2 * 1024 * 1024))
    (logs / "sub").mkdir()
    (logs / "sub" / "x.log").write_bytes(b"a" * (2 * 1024 * 1024))
    link = logs / "linked.log"
    link.symlink_to(elsewhere)
    assert crons.enforce_log_caps(root, root, dry_run=False) == []
    assert link.is_symlink() and elsewhere.stat().st_size == 2 * 1024 * 1024
    assert (logs / "sub" / "x.log").stat().st_size == 2 * 1024 * 1024


def test_a_legitimately_named_log_with_a_digit_suffix_is_still_a_base(
        tmp_path, redirected_home):
    """The NEAR MISS, pinned: an archive is `<stem>.<digits>` AT THE END. A
    log legitimately named `agi-crons-x.1.log` does not match, and stays a
    base -- capped, rotated, with its own `rotations` archives."""
    home = redirected_home
    logs = home / "logs"
    root = make_project(tmp_path, {"cap_mb": 1, "rotations": 2})
    base = logs / "agi-crons-x.1.log"
    base.write_bytes(b"a" * (2 * 1024 * 1024))
    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert [o for o in out if base.name in o], out
    assert base.stat().st_size == 0
    assert (logs / f"{base.name}.1").stat().st_size == 2 * 1024 * 1024
