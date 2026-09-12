"""g15 round I-3b — the REAL town mint through `write.py create`
(hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names).

The first kid's proof hand-wrote the three town node FILES (`_three_towns`) and
backed the round with a `--dry-run`. Both miss the gate. This file closes the
gap with a REAL FIXTURE MINT on the mint path, and it MEASURES each of the four
gate behaviours as the gate actually behaves — not as the schema file's prose
claims.

Measured, and asserted here:
  * `--dry-run` bypasses the gate wholesale (write.py:2062-2070 — the create
    branch `return 0`s before `create()` is ever called), so a dry-run
    "proof" is parse-only. Dry-running an ILLEGAL parent or a `branches:`
    cell both print happily and exit 0.
  * the three DELIVERABLE create lines (core season 2 / streaming-suite season
    1 / web-app-suite season 1, the councils the schema body names) MINT three
    town nodes through the real create path as the prime actor, and
    `towns.load_towns` / `towns.town_tuples` read all three back with the
    ruling's exact cells and table.
  * the town's OWN `season` counter is NOT settable via `--set season=N`
    alone: `node_writer._stamp_env_fields` overwrites it at mint time from
    AGI_SEASON > ladder current_season (node_writer.py:770-777). The ruling's
    core-2 / apps-1 split requires the mint to run under AGI_SEASON=2 / =1.
  * ILLEGAL PARENT: a parent that RESOLVES to a non-ladder type is hard
    REJECTED (rc=2) with the allowed shape named ("allowed: ['ladder']"). A
    PHANTOM parent id (a node that doesn't exist) is UNVERIFIED — the node is
    written, because the gate cannot resolve the id's type.
  * VISIONS OMITTED: the schema now opts that field into `validation.
    required_nonempty` (a schema-DECLARED rule, the town deliberately opting
    out of goal:s31's warn-and-write on `validation.required` alone), so the
    CREATE GATE refuses it BY NAME at mint (rc=2) and NOTHING is written — a
    town with no `visions` is no longer born only for `towns.load_towns` to
    refuse it at READ time ("town with no visions"). `visions=[]` (explicitly
    empty) refuses too. A schema declaring NO `required_nonempty` keeps the
    warn-and-write rule for its own missing-required (goal:s31 unbroken).
  * NON-PRIME ACTOR: hard REFUSED by `_enforce_written_by` naming the
    admitted roles — "may be hand-edited only by admitted roles owner,
    prime_director".
  * `branches:` CELL: the CREATE GATE now enforces the schema's field-level
    `refuse:` annotation GENERICALLY (hypothesis:l4-the-town-create-gate-
    refuses-what-the-loader-refuses-...): a `--set branches=…` refuses BY
    NAME at mint (rc=2) with the schema's own ground quoted, and nothing is
    written — the loader's `DERIVED, never a cell` refusal moves INTO the
    gate, so the write no longer admits a cell only for a later reader to
    reject it. The same gate also refuses a non-`int` under a declared
    `int` type (`season=abc`, `season=true`) by name, never a traceback.

Every assertion runs against a FRESH fixture project under tmp_path and never
touches the live tree.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

import towns
import write


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch):
    """The mint path reads AGI_ROLE / AGI_SEASON from os.environ. Running as a
    kid under a dispatch shell sets both; hermetic tests must clear them (and
    set AGI_SEASON only where a test intends it)."""
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_SEASON", raising=False)


def _real_schema() -> str:
    """The LIVE `[town].md` schema bytes, copied byte-for-byte — never
    paraphrased (the round's rule). Resolved like test_town_schema.py."""
    from graph_core.persistence import load_node_file  # noqa: F401
    import locations
    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no project root for the live [town].md"
    p = Path(root) / "context" / "schemas" / "[town].md"
    assert p.is_file(), f"missing live schema: {p}"
    return p.read_text(encoding="utf-8")


def _write(g: Path, rel: str, content: str):
    p = g / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def _fixture(tmp_path: Path) -> Path:
    """Build a fresh fixture PROJECT under tmp_path; returns the project root.
    Layout (the G11 shape):
        <proj>/.agi/config.json
        <proj>/.agi/context/schemas/[town].md      (unwieldy - the LIVE schema)
        <proj>/.agi/context/schemas/[notown].md    (a fixture schema with a required field but NO required_nonempty — goal:s31 control)
        <proj>/.agi/nodes/.geometry/ladder.md      (current_season 2 + towns)
        <proj>/.agi/nodes/.geometry/posts.md       (prime_director + 3 councils)
        <proj>/.agi/nodes/ladder/ladder.md         (so the gate resolves ladder:ladder)
        <proj>/.agi/nodes/vision/*.md              (vision:a/b/c)
    """
    proj = tmp_path / "proj"
    g = proj / ".agi"
    _write(g, "config.json", "{}\n")
    _write(g, "context/schemas/[town].md", _real_schema())
    _write(g, "context/schemas/[notown].md",
           "---\nname: notown\nfields:\n  thing: {type: str}\n"
           "validation:\n  required: [thing]\n"
           "spawn:\n  allowed_parents: [ladder]\n  min_parents: 1\n  max_parents: 1\n---\n")
    _write(g, "nodes/.geometry/ladder.md",
           "---\nid: ladder:ladder\ncurrent_season: 2\n"
           "towns: [core, streaming-suite, web-app-suite]\n---\nbody\n")
    posts = [
        {"name": "prime_director", "role": "prime_director", "town": "all"},
        {"name": "council-core", "role": "council", "town": "core"},
        {"name": "council-streaming-suite", "role": "council",
         "town": "streaming-suite"},
        {"name": "council-web-app-suite", "role": "council",
         "town": "web-app-suite"},
    ]
    _write(g, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           + "\n".join(f"  - {json.dumps(r)}" for r in posts) + "\n---\n")
    _write(g, "nodes/ladder/ladder.md",
           "---\nid: ladder:ladder\ntype: ladder\n---\nbody\n")
    for v in ("vision:a", "vision:b", "vision:c",
              "vision:streaming-suite", "vision:web-app-suite"):
        _write(g, f"nodes/vision/{v.split(':')[-1]}.md",
               f"---\nid: {v}\ntype: vision\ntitle: x\n---\nbody\n")
    return proj


def _mint(monkeypatch, proj: Path, slug: str, *, visions,
          council: str, season: int, agi_season: str | None,
          parent: str = "ladder:ladder", extra_sets: dict | None = None,
          actor: str = "prime_director", dry_run: bool = False) -> int:
    """One real `write.py create town …` as the target actor; returns rc.
    `agi_season` None => AGI_SEASON cleared (ladder current_season decides)."""
    if agi_season is None:
        monkeypatch.delenv("AGI_SEASON", raising=False)
    else:
        monkeypatch.setenv("AGI_SEASON", str(agi_season))
    argv = ["create", "town", slug,
            "--parent", parent,
            "--root", str(proj),
            "--actor", actor,
            "--set", f"visions={json.dumps(visions)}",
            "--set", f"council={council}",
            "--set", f"season={season}"]
    for k, v in (extra_sets or {}).items():
        argv += ["--set", f"{k}={v}"]
    if dry_run:
        argv.append("--dry-run")
    return write.main(argv)


def test_dry_run_bypasses_spawn_gate_but_not_the_schema_refuse_gate(tmp_path, monkeypatch):
    """`--dry-run` returns 0 BEFORE create() runs (write.py:2062-2070), so it
    exercises no spawn gate — an illegal parent still dry-runs happily. But the
    schema field-level `refuse:` gate now sits BEFORE the dry-run short-circuit,
    because a dry run is a simulation of the mint and refuses what the real
    mint would refuse: a `branches:` cell refuses by name even under --dry-run."""
    proj = _fixture(tmp_path)
    # Illegal parent that WOULD hard-refuse for real (vision:a resolves):
    rc = _mint(monkeypatch, proj, "dryrun-bad", visions=["vision:a"],
               council="council-core", season=2, agi_season="2",
               parent="vision:a", dry_run=True)
    assert rc == 0, "dry-run must not run the spawn gate (write.py:2062-2070)"
    # A branches cell IS refused even under a dry run (schema gate pre-dry-run):
    rc2 = _mint(monkeypatch, proj, "dryrun-branches", visions=["vision:a"],
                council="council-core", season=2, agi_season="2",
                extra_sets={"branches": "[core/main]"}, dry_run=True)
    assert rc2 == 2, "the schema refuse: gate must fire before the dry-run return"
    # Nothing was minted by a dry run:
    assert not (proj / ".agi" / "nodes" / "town" / "dryrun-bad.md").exists()
    assert not (proj / ".agi" / "nodes" / "town" / "dryrun-branches.md").exists()


def test_three_create_lines_mint_and_readback_equal_ruling(tmp_path, monkeypatch):
    """The three DELIVERABLE create lines MINT three town nodes through the
    REAL create path, and load_towns / town_tuples read back the ruling's
    cells. The season split (core 2 / apps 1) needs AGI_SEASON because
    `_stamp_env_fields` overwrites `--set season` at mint time
    (node_writer.py:770-777)."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    lines = {
        "core": (["vision:a", "vision:b", "vision:c"], "council-core", 2, "2"),
        "streaming-suite": (["vision:streaming-suite"],
                            "council-streaming-suite", 1, "1"),
        "web-app-suite": (["vision:web-app-suite"],
                          "council-web-app-suite", 1, "1"),
    }
    for slug, (visions, council, season, agi_season) in lines.items():
        rc = _mint(monkeypatch, proj, slug, visions=visions, council=council,
                   season=season, agi_season=agi_season)
        assert rc == 0, f"{slug} create must succeed on the real mint path"
        assert (g / "nodes" / "town" / f"{slug}.md").is_file(), slug

    by = {t.slug: t for t in towns.load_towns(g)}
    assert set(by) == {"core", "streaming-suite", "web-app-suite"}
    assert by["core"].season == 2
    assert sorted(by["core"].visions) == ["vision:a", "vision:b", "vision:c"]
    assert by["streaming-suite"].season == 1
    assert by["streaming-suite"].council == "council-streaming-suite"
    assert by["web-app-suite"].season == 1
    assert by["web-app-suite"].council == "council-web-app-suite"

    assert towns.town_tuples(g) == [
        {"town": "core", "season": 2, "global_season": 2, "council": "council-core"},
        {"town": "streaming-suite", "season": 1, "global_season": 2,
         "council": "council-streaming-suite"},
        {"town": "web-app-suite", "season": 1, "global_season": 2,
         "council": "council-web-app-suite"},
    ]


def test_season_set_is_overridden_at_mint_time(tmp_path, monkeypatch):
    """`--set season=1` does NOT land as 1 under a ladder current_season of 2 —
    `_stamp_env_fields` stamps season from AGI_SEASON > ladder current_season
    at mint time (node_writer.py:770-777). This is the measured reason the
    ruling's apps-are-season-1 needs AGI_SEASON=1, and it is a corner the
    first kid's hand-written fixture could not expose."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    rc = _mint(monkeypatch, proj, "wants-1", visions=["vision:a"],
               council="council-core", season=1, agi_season=None)
    assert rc == 0
    nf = towns._load_one(g / "nodes" / "town" / "wants-1.md")
    assert nf is not None and nf.season == 2, \
        "ladder current_season (2) must stamp season over --set season=1"


def test_illegal_parent_real_vision_refused_by_name(tmp_path, monkeypatch):
    """A parent that RESOLVES to a non-ladder type is hard-REJECTED with the
    allowed parent shape named. `vision:a` is the honest illegal parent — the
    schema body says a vision is a town's CELL, never its ancestor."""
    proj = _fixture(tmp_path)
    rc = _mint(monkeypatch, proj, "kid-of-vision", visions=["vision:a"],
               council="council-core", season=2, agi_season="2",
               parent="vision:a")
    assert rc == 2, "a vision parent must be rejected on the mint path"
    assert not (proj / ".agi" / "nodes" / "town" / "kid-of-vision.md").exists(), \
        "a rejected spawn must leave no node behind"


def test_phantom_parent_is_unverified_not_refused(tmp_path, monkeypatch):
    """`--parent vision:alive` when NO such node exists does NOT hard-refuse —
    the gate cannot resolve the phantom id's type, so it is UNVERIFIED and the
    node IS written (the same corner the first kid's dry-run hid). The gate
    refuses by RESOLVED type; a phantom resolves to nothing."""
    proj = _fixture(tmp_path)  # vision:alive does NOT exist here
    rc = _mint(monkeypatch, proj, "phantom-parent", visions=["vision:a"],
               council="council-core", season=2, agi_season="2",
               parent="vision:alive")
    assert rc == 0, "an unresolvable parent id is UNVERIFIED, not rejected"


def test_visions_omitted_refused_by_create_gate_by_name(tmp_path, monkeypatch, capsys):
    """A town whose schema declares `visions` on `validation.required_nonempty`
    and whose create leaves `visions` ABSENT is REFUSED BY NAME at mint (rc=2),
    and NOTHING is written. This is the schema-DECLARED own of goal:s31's
    missing-required warn-and-write: `validation.required` alone stays a
    SCHEMA-WARNING and the node is written (other types), but a field a type
    opts into `required_nonempty` refuses at MINT — so the write no longer
    admits a town only for `towns.load_towns` to refuse it at read."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    import os as _os
    monkeypatch.delenv("AGI_SEASON", raising=False)
    rc = write.main(["create", "town", "novisions",
                     "--parent", "ladder:ladder",
                     "--root", str(proj),
                     "--actor", "prime_director",
                     "--set", "council=council-core",
                     "--set", "season=2"])
    assert rc == 2, "the mint gate must refuse a town with no visions (absent)"
    err = capsys.readouterr().err
    assert "refused by name" in err
    assert "'visions'" in err
    assert "required_nonempty" in err
    assert not (g / "nodes" / "town" / "novisions.md").exists(), \
        "a refused mint must leave no node behind"


def test_visions_explicitly_empty_refused_by_create_gate_by_name(tmp_path, monkeypatch, capsys):
    """`--set visions=[]` — an EXPLICITLY EMPTY visions cell — refuses BY NAME
    at mint (rc=2) under the same `required_nonempty` rule, and nothing is
    written. An empty list is as un-owning as an absent one."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    rc = _mint(monkeypatch, proj, "empty-visms", visions=[],
               council="council-core", season=2, agi_season="2")
    assert rc == 2, "visions=[] must refuse at mint"
    err = capsys.readouterr().err
    assert "refused by name" in err
    assert "'visions'" in err
    assert "empty" in err
    assert not (g / "nodes" / "town" / "empty-visms.md").exists(), \
        "an empty-visions mint must leave no node behind"


def test_no_required_nonempty_schema_still_warns_and_writes(tmp_path, monkeypatch, capsys):
    """goal:s31 is NOT broken: a schema declaring `validation.required` but NO
    `required_nonempty` keeps the standing warn-and-write for a MISSING required
    field — the node is ALIVE with a SCHEMA-WARNING and rc=0, never refused.
    The new refusal is a schema-OPT-IN, not a blanket flip of missing-required
    into rc=2."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    monkeypatch.delenv("AGI_SEASON", raising=False)
    rc = write.main(["create", "notown", "missing-thing",
                     "--parent", "ladder:ladder",
                     "--root", str(proj),
                     "--actor", "prime_director"])
    assert rc == 0, ("a required-missing field on a schema without "
                     "required_nonempty must warn-and-write (goal:s31)")
    assert (g / "nodes" / "notown" / "missing-thing.md").is_file(), \
        "the warned node must be written"


def test_non_prime_actor_refused_naming_admitted_roles(tmp_path, monkeypatch):
    """A kid actor is REFUSED by `_enforce_written_by` naming the admitted
    roles — 'may be hand-edited only by admitted roles owner, prime_director'
    — and nothing is written."""
    proj = _fixture(tmp_path)
    with pytest.raises(write.EditError) as e:
        _mint(monkeypatch, proj, "kidtown", visions=["vision:a"],
              council="council-core", season=2, agi_season="2",
              actor="a00-someone")
    msg = str(e.value)
    assert "only by admitted roles owner, prime_director" in msg
    assert not (proj / ".agi" / "nodes" / "town" / "kidtown.md").exists()


def test_branches_cell_refused_by_create_gate_by_name(tmp_path, monkeypatch, capsys):
    """The schema's field-level `refuse:` annotation is now a GENERIC gate
    rule on the create path: a `--set branches=...` refuses BY NAME at mint
    (rc=2) naming the key and quoting the schema's own ground, and NO node is
    born. What the loader used to catch at read time the gate now refuses at
    write time — for any schema declaring a `refuse:`, not a town special
    case."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"
    rc = _mint(monkeypatch, proj, "with-branches", visions=["vision:a"],
               council="council-core", season=2, agi_season="2",
               extra_sets={"branches": "[core/main]"})
    assert rc == 2, "a branches: cell must be refused at mint, not admitted"
    err = capsys.readouterr().err
    assert "refused by name" in err
    assert "'branches'" in err
    assert "DERIVED, never a cell" in err
    assert not (g / "nodes" / "town" / "with-branches.md").exists(), \
        "a refused spawn must leave no node behind"


def test_non_int_season_refused_by_name_at_mint(tmp_path, monkeypatch, capsys):
    """A non-`int` under the schema's declared `season: int` refuses BY NAME at
    mint (rc=2), never a traceback. `season=abc` (a bare string) and
    `season=true` (a bool, a subclass of int that is not a season) both
    refuse; `season=2` passes. Generic across every schema that declares an
    `int` type."""
    proj = _fixture(tmp_path)
    g = proj / ".agi"

    for bad in ("abc", "true", "2.5"):
        rc = _mint(monkeypatch, proj, "bad-season", visions=["vision:a"],
                   council="council-core", season=bad, agi_season="2")
        assert rc == 2, f"season={bad!r} must refuse at mint"
        err = capsys.readouterr().err
        assert "refused by name" in err, bad
        assert "'season'" in err, bad
        assert "must be an integer" in err, bad
        assert not (g / "nodes" / "town" / "bad-season.md").exists(), bad

    # The positive corner: a real int season still mints.
    rc = _mint(monkeypatch, proj, "good-season", visions=["vision:a"],
               council="council-core", season=2, agi_season="2")
    assert rc == 0
    assert (g / "nodes" / "town" / "good-season.md").is_file()