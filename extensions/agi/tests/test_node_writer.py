"""Tests for the one node-writing routine — bin/node_writer.py (GOALS.md S17).

Companion to `test_spawn_gate.py`, which tests the *rule*. This file tests
that the rule is unavoidable: there is exactly one routine that creates a node
file, every writer reaches it the same way, and none of them can write past it.

The three things that matter, in the order they were got wrong:

1. **No writer has its own copy.** `dispatch.py` carried a duplicate of the
   whole scaffold routine — its own type tuple, its own body prompts, its own
   `write_text()`. The duplicate was never gated, so a pi-runtime run wrote
   nodes the gate never saw, and its private tuple kept minting the
   hyphenated spellings `[shape].md` calls non-canonical.
2. **The canonical spelling is written, the hyphen only accepted.**
   `bigger-outcome` in, `bigger_outcome` out — id, `type:` and directory.
3. **A rejection leaves nothing behind.** The gate runs before the filesystem
   is touched, on every path.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


nw = _load("node_writer")


SHAPE = """\
---
name: shape
structural: true
parentless_types:
  - goal:long-term
  - goal:short-term
  - idea
max_parents_ceiling: 2
canonical_type_spelling: underscore
---
shape
"""

SCHEMAS = {
    "[hypothesis].md": "allowed_parents: [idea, hypothesis, experiment]\n  min_parents: 1\n  max_parents: 2",
    "[experiment].md": "allowed_parents: [hypothesis, idea]\n  min_parents: 1\n  max_parents: 2",
    "[verdict].md": "allowed_parents: [experiment, hypothesis, verdict]\n  min_parents: 1\n  max_parents: 2",
    "[mvp].md": "allowed_parents: [verdict, hypothesis, experiment]\n  min_parents: 1\n  max_parents: 2",
    "[outcome].md": "allowed_parents: [mvp, verdict]\n  min_parents: 1\n  max_parents: 2",
    "[bigger_outcome].md": "allowed_parents: [outcome, mvp]\n  min_parents: 1\n  max_parents: 2",
    "[vision].md": "allowed_parents: [overview]\n  min_parents: 1\n  max_parents: 2",
    "[overview].md": "allowed_parents: [bigger_outcome]\n  min_parents: 1\n  max_parents: 2",
    "[idea].md": "allowed_parents: [goal]\n  min_parents: 0\n  max_parents: 1",
    "[task].md": "allowed_parents: [hypothesis]\n  min_parents: 1\n  max_parents: 1",
}


@pytest.fixture
def project(tmp_path):
    """A throwaway graph repo: schemas plus one node of each parent type."""
    (tmp_path / "agi-tree.config.json").write_text("{}")
    sd = tmp_path / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[shape].md").write_text(SHAPE)
    for fname, spawn in SCHEMAS.items():
        name = fname[1:-4]
        (sd / fname).write_text(f"---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n")
    nd = tmp_path / "nodes"
    for ntype, slug in [("idea", "i1"), ("hypothesis", "h1"),
                        ("experiment", "e1"), ("verdict", "v1"),
                        ("mvp", "m1"), ("outcome", "o1"),
                        ("bigger_outcome", "b1"), ("overview", "ov1")]:
        d = nd / ntype
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(
            f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n"
        )
    # Ladder node for season stamping (hypothesis:l2w2-writer-stamps)
    (nd / ".geometry").mkdir(parents=True, exist_ok=True)
    (nd / ".geometry" / "ladder.md").write_text(
        "---\nid: ladder:ladder\ntype: ladder\ncurrent_season: 1\n---")
    return tmp_path


# --------------------------------------------------------------------------
# 1. one routine — no writer keeps a copy
# --------------------------------------------------------------------------

WRITERS = ("cli.py", "dispatch.py", "post_wire.py")


@pytest.mark.parametrize("writer", WRITERS)
def test_every_writer_points_at_the_one_routine_the_same_way(writer):
    """Same method for all four callers: `import node_writer`, then call it.

    Not "each one calls the gate": that is what let dispatch.py drift, since
    a writer that forgets is indistinguishable from one that has no node to
    write.
    """
    text = (BIN / writer).read_text()
    assert "import node_writer" in text, writer
    assert "node_writer.write_node" in text, writer


def test_dispatch_no_longer_touches_the_node_tree_at_all():
    """dispatch.py's only remaining `write_text` calls are session files.

    `cli.py` and `post_wire.py` still rewrite *existing* node files in place
    (`done` and the wiring pass update frontmatter), which is not node
    creation and not this routine's business. dispatch.py only ever created,
    so after the consolidation it should reach `nodes/` for reading and
    nothing else.
    """
    text = (BIN / "dispatch.py").read_text()
    writes = [ln.strip() for ln in text.splitlines() if ".write_text(" in ln]
    assert writes, "expected the manifest/agent.json writes to still be here"
    # `manifest_tmp` is the atomic-write idiom added by goal:s28: the manifest
    # goes to `.manifest.json.tmp` and is renamed, so two dispatches into one
    # iteration cannot leave a partial read. The variable is named for what it
    # holds precisely so this check can still see the target — an earlier bare
    # `tmp` hid it and failed here, which is the assertion working rather than
    # a false positive.
    session_artefacts = ("agent.json", "manifest.json", "manifest_tmp")
    for ln in writes:
        assert any(a in ln for a in session_artefacts), ln


@pytest.mark.parametrize("writer", WRITERS)
def test_no_writer_keeps_its_own_type_table_or_prompts(writer):
    """The two things dispatch.py's copy diverged on."""
    text = (BIN / writer).read_text()
    assert "NODE_TYPES = (" not in text, f"{writer} has a private type tuple"
    assert '"bigger-outcome":' not in text, f"{writer} has private prompts"
    assert '"app-purpose":' not in text, f"{writer} has private prompts"


def test_the_type_table_is_all_underscores():
    for t in nw.CANONICAL_NODE_TYPES:
        assert "-" not in t, t
    # Every alias resolves to a canonical type. Two kinds now live here and
    # the distinction matters: a *spelling* alias (hyphen -> underscore) and a
    # *rename* alias (`app_purpose` -> `vision`, 2026-08-27). The old assertion
    # was `"-" in alias`, which silently encoded "aliases are only ever
    # hyphens" — true until a type was renamed, and it would have rejected the
    # rename rather than the mistake.
    for alias, canonical in nw.TYPE_ALIASES.items():
        assert canonical in nw.CANONICAL_NODE_TYPES, alias
        assert alias not in nw.CANONICAL_NODE_TYPES, f"{alias} is both alias and canonical"
        assert nw.canonical_node_type(alias) == canonical


def test_the_renamed_type_still_resolves_from_its_old_name():
    """`app_purpose` and `app-purpose` both land on `vision`.

    Callers written against the old name keep working — the reader accepts
    both spellings, which is the sequence S11 requires for every rename here.
    """
    for old in ("app_purpose", "app-purpose"):
        assert nw.canonical_node_type(old) == "vision"
    assert "app_purpose" not in nw.CANONICAL_NODE_TYPES


def test_every_canonical_type_has_a_body_prompt():
    # A type in the table with no prompt scaffolds a node with an empty body,
    # which is what `on_exists=reuse-scaffold` then treats as untouched.
    assert set(nw.CANONICAL_NODE_TYPES) <= set(nw.BODY_PROMPTS)


# --------------------------------------------------------------------------
# 2. spelling — canonical out, hyphen accepted in
# --------------------------------------------------------------------------

def test_hyphenated_input_writes_the_canonical_spelling(project):
    res = nw.write_node(project, "bigger-outcome", "bo", ["outcome:o1"])
    assert res.written
    assert res.path == project / "nodes" / "bigger_outcome" / "bo.md"
    text = res.path.read_text()
    assert "id: bigger_outcome:bo" in text
    assert "type: bigger_outcome" in text
    assert "bigger-outcome" not in text


def test_the_scaffold_marks_where_the_body_begins(project):
    """hypothesis:l3-done-broken-frontmatter -- the scaffold writes the one-line
    `BODY:BEGIN` comment right after the closing `---`, so a later `cli.py done`
    can repair a mangled frontmatter block up to that boundary without ever
    swallowing the kid's body."""
    res = nw.write_node(project, "experiment", "fresh", ["hypothesis:h1"])
    assert res.written
    text = res.path.read_text()
    parts = text.split("---\n", 2)
    assert len(parts) == 3
    body = parts[2]
    assert body.startswith(nw.BODY_BEGIN + "\n"), \
        "body must begin with the marker, immediately after the closing `---`"
    # the marker is anchored in the same body the scaffold_hash certifies
    assert "scaffold_hash:" in parts[1]


def test_a_caller_supplied_body_gets_no_marker(project):
    """The marker is a scaffold concept, not a body mandate: a caller that passes
    an explicit body (e.g. `cli.py done`'s verdict-fallback path) keeps its body
    exactly as supplied -- no marker prepended."""
    res = nw.write_node(project, "experiment", "explicit", ["hypothesis:h1"],
                        body="## Verdict\n\nproved\n")
    assert res.written
    text = res.path.read_text()
    assert nw.BODY_BEGIN not in text
    assert "## Verdict" in text


def test_an_unaliased_hyphen_still_lands_canonical():
    # The alias table is the documented surface; the general rule is the
    # backstop, so a type nobody remembered to alias cannot mint a hyphen.
    assert nw.canonical_node_type("some-new-type") == "some_new_type"


# --------------------------------------------------------------------------
# 3. the gate is unavoidable
# --------------------------------------------------------------------------

def test_rejection_writes_nothing(project):
    res = nw.write_node(project, "verdict", "orphan", [])
    assert res.rejected
    assert "min_parents" in res.reason
    assert not (project / "nodes" / "verdict" / "orphan.md").exists()


def test_approval_writes_a_mint_id_and_no_stamp(project):
    res = nw.write_node(project, "verdict", "good", ["experiment:e1"])
    assert res.written
    text = res.path.read_text()
    # goal:s14 — without this the node is skipped by `grid.py commit --all`.
    assert "mint_id:" in text
    # An approval leaves no frontmatter mark; the terminal line is the feedback.
    assert "spawn_gate" not in text
    assert "spawn_check" not in text


def test_bypass_is_stamped(project):
    res = nw.write_node(project, "verdict", "bypassed", [], bypass=True)
    assert res.written
    assert "spawn_gate: bypassed" in res.path.read_text()


def test_unverified_reason_survives_yaml_round_trip(project):
    """An `unverified` reason can contain `: ` and quotes.

    The old writers wrote every stamp as a bare `f"{k}: {v}"`, so a reason
    like `parent id(s) resolve to no node: ['x']` produced frontmatter that
    `yaml.safe_load` then rejected — in the one field whose whole job is
    telling a reviewer why the node was not checked.
    """
    import yaml
    res = nw.write_node(project, "verdict", "dangling", ["experiment:missing"])
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm["spawn_check"] == "unverified"
    assert "experiment:missing" in fm["spawn_check_reason"]


def test_frontmatter_is_valid_yaml_for_every_type(project):
    import yaml
    parent = {"idea": [], "hypothesis": ["idea:i1"], "task": ["hypothesis:h1"],
              "experiment": ["hypothesis:h1"], "verdict": ["experiment:e1"],
              "mvp": ["verdict:v1"], "outcome": ["mvp:m1"],
              "bigger_outcome": ["outcome:o1"], "overview": ["bigger_outcome:b1"],
              "vision": ["overview:ov1"]}
    for ntype, parents in parent.items():
        res = nw.write_node(project, ntype, f"{ntype}-x", parents)
        assert res.status in (nw.WRITTEN,), f"{ntype}: {res.status} {res.reason}"
        fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
        assert fm["id"] == f"{ntype}:{ntype}-x"
        assert fm["type"] == ntype
        assert fm["parents"] == parents


# --------------------------------------------------------------------------
# on_exists — dispatch.py's re-scaffold rule, preserved
# --------------------------------------------------------------------------

def test_skip_never_touches_an_existing_file(project):
    first = nw.write_node(project, "verdict", "keep", ["experiment:e1"])
    (first.path).write_text("---\nid: verdict:keep\n---\n\nREAL WORK\n")
    again = nw.write_node(project, "verdict", "keep", ["experiment:e1"])
    assert again.status == nw.SKIPPED
    assert "REAL WORK" in first.path.read_text()


def test_reuse_scaffold_overwrites_an_untouched_scaffold(project):
    first = nw.write_node(project, "verdict", "fresh", ["experiment:e1"])
    before = first.path.read_text()
    again = nw.write_node(project, "verdict", "fresh", ["experiment:e1"],
                          on_exists=nw.REUSE_SCAFFOLD)
    assert again.written
    # A new mint_id, because this is a new node standing in the same place.
    assert again.path.read_text() != before


def test_reuse_scaffold_preserves_filled_in_work(project):
    first = nw.write_node(project, "verdict", "filled", ["experiment:e1"])
    first.path.write_text(
        first.path.read_text() + "\nAn agent actually wrote this.\n")
    again = nw.write_node(project, "verdict", "filled", ["experiment:e1"],
                          on_exists=nw.REUSE_SCAFFOLD)
    assert again.status == nw.SKIPPED
    assert "An agent actually wrote this." in first.path.read_text()


# --------------------------------------------------------------------------
# find_node_file — the one lookup, beside the one write
# --------------------------------------------------------------------------

def test_direct_path_is_found(project):
    assert nw.find_node_file(project, "hypothesis:h1") == \
        project / "nodes" / "hypothesis" / "h1.md"


def test_descriptive_filename_is_found_by_frontmatter(project):
    """`t-001-some-description.md` holding `id: task:thing`.

    Both old copies handled this in `nodes/task/` only, and only `cli.py`'s
    even tried.
    """
    d = project / "nodes" / "task"
    d.mkdir(parents=True, exist_ok=True)
    (d / "t-001-some-description.md").write_text(
        "---\nid: task:thing\ntype: task\n---\n\nbody\n")
    assert nw.find_node_file(project, "task:thing") == d / "t-001-some-description.md"


def test_abbreviated_prefix_is_found(project):
    """`exp:` and `hyp:` ids live under `experiment/` and `hypothesis/`.

    147 corpus ids are shaped like this, and `cli.py`'s copy resolved none of
    them: every step it had assumed the id prefix names the directory.
    """
    d = project / "nodes" / "experiment"
    (d / "abbrev.md").write_text("---\nid: exp:abbrev\ntype: experiment\n---\n\nb\n")
    assert nw.find_node_file(project, "exp:abbrev") == d / "abbrev.md"


def test_retired_node_is_still_found(project):
    """goal:g2.10 — a node retired into `nodes/deprecated/<type>/` still
    resolves. Deprecation moves an address; it does not remove the node, and an
    edge pointing at one has to keep resolving or the retirement silently
    becomes a broken link.
    """
    d = project / "nodes" / "deprecated" / "hypothesis"
    d.mkdir(parents=True, exist_ok=True)
    (d / "old.md").write_text(
        "---\nid: hypothesis:old\ntype: hypothesis\nstatus: deprecated\n---\n\nb\n")
    assert nw.find_node_file(project, "hypothesis:old") == d / "old.md"


def test_live_node_wins_over_a_retired_namesake(project):
    """The lookup takes the first hit, so directory order is load-bearing: a
    live node must never lose to a retired file of the same name."""
    live = project / "nodes" / "hypothesis"
    live.mkdir(parents=True, exist_ok=True)
    (live / "dup.md").write_text("---\nid: hypothesis:dup\ntype: hypothesis\n---\n\nlive\n")

    dead = project / "nodes" / "deprecated" / "hypothesis"
    dead.mkdir(parents=True, exist_ok=True)
    (dead / "dup.md").write_text(
        "---\nid: hypothesis:dup\ntype: hypothesis\nstatus: deprecated\n---\n\ndead\n")

    assert nw.find_node_file(project, "hypothesis:dup") == live / "dup.md"


def test_unknown_id_is_none_not_a_guess(project):
    # G7.1: a reference that resolves to nothing is reported, never inferred.
    assert nw.find_node_file(project, "verdict:no-such-node") is None
    assert nw.find_node_file(project, "not-an-id") is None


def test_a_runon_frontmatter_opener_is_not_misread(project):
    """l3-corrupt-frontmatter-19 — the lax split loader used to disagree
    with the strict loader on a `---id:` run-on opener: it parsed the id out
    of the glued line and RESOLVED the file, where `load_node_file` raises
    (missing opening `---`). That disagreement hid the corruption from
    every writer. `find_node_file`'s frontmatter scan and the id index now
    delegate to the strict loader, so a run-on file is skipped, not resolved.
    The file must not carry a canonical name, or step 1 (direct path) would
    resolve it by filename and never reach the frontmatter scan.
    """
    from graph_core.persistence import frontmatter as fm_reader
    d = project / "nodes" / "experiment"
    corrupt = d / "not-its-canonical-name.md"
    corrupt.write_text(
        "---id: experiment:ghost\n"
        "mint_id: deadbeef\n"
        "type: experiment\n"
        "parents:\n  - idea:i1\n"
        "---\n\nbody\n",
        encoding="utf-8")
    # the strict reader rejects it — that is the corruption
    with pytest.raises(fm_reader.FrontmatterError):
        fm_reader.load_node_file(corrupt)
    # ...so the lookup must not resolve the id it claims
    assert nw.find_node_file(project, "experiment:ghost") is None
    assert "experiment:ghost" not in nw._build_id_index(project)


def test_the_index_cannot_go_stale_under_its_own_writer(project):
    """Prime the cache with a miss, then write the node and look again."""
    assert nw.find_node_file(project, "verdict:later") is None      # builds index
    res = nw.write_node(project, "verdict", "later", ["experiment:e1"])
    assert res.written
    assert nw.find_node_file(project, "verdict:later") == res.path


def test_both_readers_are_the_same_function():
    cli = _load("cli")
    post_wire = _load("post_wire")
    for name in ("cli.py", "post_wire.py"):
        assert "node_writer.find_node_file" in (BIN / name).read_text(), name
    # And they agree on a case each old copy got differently.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        d = r / "nodes" / "experiment"
        d.mkdir(parents=True)
        (d / "x.md").write_text("---\nid: exp:x\ntype: experiment\n---\n\nb\n")
        assert cli._find_node_file(r, "exp:x") == post_wire._node_file_path(r, "exp:x") == d / "x.md"


# --------------------------------------------------------------------------
# dispatch.py — the writer this whole change is about
# --------------------------------------------------------------------------

dispatch = _load("dispatch")


@pytest.mark.parametrize("level,target,role,expected", [
    ("big", None, None, "idea"),          # parentless-legal; was `hypothesis`
    ("small", "hypothesis:h1", None, "experiment"),
    ("small", "experiment:e1", None, "verdict"),
    ("small", "verdict:v1", None, "mvp"),
    ("small", "mvp:m1", None, "outcome"),
    ("small", "outcome:o1", None, "bigger_outcome"),
    ("small", "idea:i1", None, "hypothesis"),
    ("small", None, "research", "experiment"),
    ("small", None, "implementation", "mvp"),
])
def test_dispatch_picks_a_canonically_spelled_step(level, target, role, expected):
    assert dispatch._node_type_for(level, target, role) == expected


def test_dispatch_scaffold_is_gated_and_canonical(project):
    """The chip: a pi-runtime scaffold now goes through the gate.

    `outcome:o1` is a legal parent for `bigger_outcome`, and the old copy
    would have written `type: bigger-outcome` here.
    """
    info = dispatch._scaffold_node_for_agent(
        project, 1, "a00-dead", "small", "outcome:o1")
    assert info is not None
    assert info["node_type"] == "bigger_outcome"
    text = Path(info["path"]).read_text()
    assert "type: bigger_outcome" in text
    assert "mint_id:" in text


def test_dispatch_scaffold_declines_an_illegal_spawn(project):
    """`task` may only be parented by `hypothesis`, so an outcome parent is
    rejected — and nothing is written. Before the consolidation this path had
    no gate at all, so the node landed."""
    before = list((project / "nodes").rglob("*.md"))
    info = dispatch._scaffold_node_for_agent(
        project, 1, "a00-bad", "small", "verdict:v1", role="nonesuch")
    # role is unknown -> falls through to the step map: verdict -> mvp, legal.
    assert info["node_type"] == "mvp"
    # Now an illegal one: a bigger_outcome cannot be parented by an idea.
    res = nw.write_node(project, "bigger_outcome", "illegal", ["idea:i1"])
    assert res.rejected
    assert len(list((project / "nodes").rglob("*.md"))) == len(before) + 1


def test_big_zoom_scaffold_no_longer_writes_an_illegal_hypothesis(project):
    """Regression for the shape the un-gated copy produced every iteration.

    `_pick_targets` returns `("big", None, ...)`, so slot 0 had no parent and
    `[hypothesis].md` says `min_parents: 1`. The old copy wrote it anyway,
    with a literal empty string as its one parent.
    """
    info = dispatch._scaffold_node_for_agent(project, 1, "a00-big", "big", None)
    assert info is not None
    assert info["node_type"] == "idea"
    text = Path(info["path"]).read_text()
    assert "parents: []" in text
    assert "  - \n" not in text     # the old copy's empty-string parent


# --------------------------------------------------------------------------
# end to end through the real CLI
# --------------------------------------------------------------------------

def test_cli_scaffold_still_writes_through_the_shared_routine(project):
    ad = project / "sessions" / "iter-001" / "a1"
    ad.mkdir(parents=True)
    (ad / "agent.json").write_text(json.dumps({"id": "a1", "status": "run"}))
    r = subprocess.run(
        [sys.executable, str(BIN / "cli.py"), "scaffold", "1", "a1",
         "--type", "app-purpose", "--slug", "ap", "--parent", "overview:ov1"],
        cwd=str(project), capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "SPAWN-GATE APPROVED" in r.stdout
    # Scaffolded under the OLD name and landed under the new one.
    text = (project / "nodes" / "vision" / "ap.md").read_text()
    assert "type: vision" in text
    rec = json.loads((ad / "agent.json").read_text())
    assert rec["scaffolded_node"] == "vision:ap"


# ---------------------------------------------------------------------------
# goal:s31 — a scaffolded node ships schema-invalid.
#
# `[hypothesis].md` requires title + testable_claim; write_node seeded neither;
# the kid holding the content is CORRECTLY forbidden from touching frontmatter.
# The node could not become valid by anyone doing their job as briefed.
#
# The fix must not buy validity with the completion check — `scaffold_hash`
# hashes the BODY, which is what makes seeding frontmatter safe at all, and
# `test_seeding_required_fields_does_not_move_the_scaffold_hash` is the clause
# of s31's falsifier that says so.
# ---------------------------------------------------------------------------

import sys as _sys                                              # noqa: E402
from pathlib import Path as _Path                               # noqa: E402

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "src"))

import node_writer as _nw                                       # noqa: E402


def _schema_project(tmp_path, required):
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[hypothesis].md").write_text(
        "---\nname: hypothesis\nvalidation:\n  required: ["
        + ", ".join(required) + "]\nspawn:\n  allowed_parents: [goal]\n"
        "  min_parents: 1\n  max_parents: 2\n---\n\nbody\n")
    return graph


def test_required_fields_are_read_from_the_registry_not_a_local_table(tmp_path):
    """s31's own objection to a local patch: it would be one more caller
    agreeing with the schema by convention instead of reading it."""
    graph = _schema_project(tmp_path, ["id", "type", "mint_id", "title",
                                       "testable_claim"])
    assert _nw.required_fields(graph, "hypothesis") == [
        "id", "type", "mint_id", "title", "testable_claim"]


def test_a_scaffold_is_born_with_a_real_title_not_a_placeholder(tmp_path):
    """`title` is what every human-facing renderer keys on. A placeholder
    would be the `TODO(model)` shape the [experiment] schema warns about."""
    graph = _schema_project(tmp_path, ["id", "type", "mint_id", "title"])
    res = _nw.write_node(graph, "hypothesis", "shared-lease-bounds-the-tree",
                         parents=["goal:g1"], announce=False)
    assert res.status == _nw.WRITTEN
    text = res.path.read_text()
    assert "title: Shared lease bounds the tree" in text
    assert "TODO" not in text


def test_a_field_that_cannot_be_derived_is_reported_not_invented(tmp_path, capsys):
    graph = _schema_project(tmp_path, ["id", "type", "mint_id", "title",
                                       "testable_claim"])
    res = _nw.write_node(graph, "hypothesis", "some-claim", parents=["goal:g1"],
                         announce=True)
    assert res.missing_required == ["testable_claim"]
    assert "SCHEMA-WARNING" in capsys.readouterr().err
    assert "testable_claim" not in res.path.read_text(), (
        "an underivable field must stay absent, never be invented")


def test_seeding_required_fields_does_not_move_the_scaffold_hash(tmp_path):
    """s31's falsifier, second clause: the fix must not buy validity with the
    completion check. `scaffold_hash` hashes the BODY, so frontmatter cannot
    move it — asserted rather than assumed."""
    bare = _schema_project(tmp_path / "bare", ["id", "type", "mint_id"])
    full = _schema_project(tmp_path / "full", ["id", "type", "mint_id", "title"])

    a = _nw.write_node(bare, "hypothesis", "same-slug", parents=["goal:g1"],
                       announce=False)
    b = _nw.write_node(full, "hypothesis", "same-slug", parents=["goal:g1"],
                       announce=False)

    def _hash_of(path):
        for line in path.read_text().splitlines():
            if line.startswith("scaffold_hash:"):
                return line.split(":", 1)[1].strip()
        return None

    assert "title:" not in a.path.read_text()
    assert "title:" in b.path.read_text()
    assert _hash_of(a.path) == _hash_of(b.path), (
        "seeding frontmatter moved the scaffold hash — completion detection "
        "would break, which is the trade s31 forbids")


def test_the_completion_half_lifts_a_claim_out_of_the_body(tmp_path):
    """The kid writes prose under the heading its brief asked for; the write
    path lifts it into the required field. The kid never touches frontmatter."""
    graph = _schema_project(tmp_path, ["id", "type", "mint_id", "title",
                                       "testable_claim"])
    res = _nw.write_node(graph, "hypothesis", "bounded", parents=["goal:g1"],
                         announce=False)
    res.path.write_text(res.path.read_text().replace(
        "\n# hypothesis:bounded\n",
        "\n# hypothesis:bounded\n\n### Testable claim\n\n"
        "The live population never exceeds the declared bound.\n"))

    filled = _nw.derive_required_from_body(graph, "hypothesis:bounded")
    assert filled.status == _nw.UPDATED
    assert ("testable_claim: The live population never exceeds the declared bound."
            in res.path.read_text())


def test_the_completion_half_invents_nothing_when_the_section_is_absent(tmp_path):
    graph = _schema_project(tmp_path, ["id", "type", "mint_id", "title",
                                       "testable_claim"])
    _nw.write_node(graph, "hypothesis", "empty", parents=["goal:g1"],
                   announce=False)
    filled = _nw.derive_required_from_body(graph, "hypothesis:empty")
    assert filled.status == _nw.UNCHANGED
    assert "testable_claim" not in (graph / "nodes/hypothesis/empty.md").read_text()


# --------------------------------------------------------------------------
# L1.07 — render_frontmatter and nested mappings
# --------------------------------------------------------------------------

def test_a_nested_mapping_round_trips_instead_of_becoming_a_repr():
    """🔴 This destroyed the node the whole command system reads.

    `render_frontmatter` handled list, bool and None, and every other type
    fell through to `str(v)`. `command:commands` carries a nested `commands:`
    mapping, so one `write.py ... 'thought ...'` on it wrote back a **Python
    dict repr inside a quoted string**:

        commands: "{'smoke': {'argv': ['bash', ...

    `commands.load` then raised `'str' object has no attribute 'items'` and
    every `agi <verb>` stopped working. It was committed and pushed, because
    the suite had been run *before* that edit and the edit shared a shell
    command with the commit.

    The bug was old and merely unreachable: nothing had written a node with a
    nested mapping until `[command]` existed. `str(v)` is the branch that
    makes losing data look like working.
    """
    import yaml

    fm = {
        "id": "command:commands",
        "type": "command",
        "commands": {
            "smoke": {"argv": ["bash", "driver.sh", "--smoke"],
                      "about": "no dispatch", "workflow": "verify"},
            "view": {"argv": ["python3", "viewport.py", "--live"],
                     "about": "spiders", "workflow": "see"},
        },
        "workflows": {"verify": ["smoke"], "see": ["view"]},
        "empty_map": {},
    }
    text = "\n".join(nw.render_frontmatter(fm))
    back = yaml.safe_load(text)

    assert isinstance(back["commands"], dict), (
        "a mapping became a scalar — this is the exact regression")
    assert back["commands"]["smoke"]["argv"] == ["bash", "driver.sh", "--smoke"]
    assert back["commands"]["view"]["workflow"] == "see"
    assert back["workflows"] == {"verify": ["smoke"], "see": ["view"]}
    assert back["empty_map"] == {}
    assert "{'" not in text, "a Python repr leaked into the frontmatter"


def test_a_list_of_mappings_round_trips_too():
    """The other container this used to flatten. JSON is valid YAML."""
    import yaml

    fm = {"id": "x:y", "type": "t",
          "rows": [{"k": 1, "v": "a"}, {"k": 2, "v": "b"}]}
    back = yaml.safe_load("\n".join(nw.render_frontmatter(fm)))
    assert back["rows"] == [{"k": 1, "v": "a"}, {"k": 2, "v": "b"}]


def test_scalars_and_empty_containers_are_unchanged_by_the_fix():
    """The fix must not move anything that already worked."""
    import yaml

    fm = {"id": "x:y", "type": "t", "parents": [], "next_edges": ["a:b"],
          "flag": True, "nothing": None, "n": 3, "s": "plain"}
    text = "\n".join(nw.render_frontmatter(fm))
    back = yaml.safe_load(text)
    assert back["parents"] == []
    assert back["next_edges"] == ["a:b"]
    assert back["flag"] is True
    assert back["nothing"] is None
    assert back["n"] == 3 and back["s"] == "plain"
    assert "flag: true" in text, "bools stay lowercase yaml"


# --------------------------------------------------------------------------
# hypothesis:l2w2-writer-stamps — season / loop / model / profile stamping
# --------------------------------------------------------------------------


def test_minted_node_stamps_season_from_ladder_when_no_env(project):
    """Without AGI_SEASON env var, season comes from ladder's current_season.

The ladder.md fixture declares current_season: 1."""
    import yaml
    res = nw.write_node(project, "hypothesis", "seasoned",
                        parents=["idea:i1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("season") == 1


def test_minted_node_stamps_season_from_env_var(project, monkeypatch):
    """AGI_SEASON env var wins over the ladder's current_season."""
    import yaml
    monkeypatch.setenv("AGI_SEASON", "7")
    res = nw.write_node(project, "experiment", "env-season",
                        parents=["hypothesis:h1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("season") == 7


def test_minted_node_stamps_loop_model_profile_from_env(project, monkeypatch):
    """When AGI_LOOP, AGI_MODEL, AGI_PROFILE are set, they are stamped."""
    import yaml
    monkeypatch.setenv("AGI_LOOP", "hypothesis:foo@s2")
    monkeypatch.setenv("AGI_MODEL", "anthropic/claude-sonnet-4")
    monkeypatch.setenv("AGI_PROFILE", "balanced")
    res = nw.write_node(project, "verdict", "stamped",
                        parents=["experiment:e1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("loop") == "hypothesis:foo@s2"
    assert fm.get("model") == "anthropic/claude-sonnet-4"
    assert fm.get("profile") == "balanced"


def test_minted_node_stamps_role_from_env(project, monkeypatch):
    """hypothesis:l3w0-ladder-roles-table — dispatch exports AGI_ROLE and
    node_writer stamps it as `role:` alongside loop/model/profile."""
    import yaml
    monkeypatch.setenv("AGI_ROLE", "parent")
    res = nw.write_node(project, "hypothesis", "roled",
                        parents=["idea:i1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("role") == "parent"


def test_minted_node_omits_role_when_env_absent(project, monkeypatch):
    """No AGI_ROLE -> no `role:` field; never fabricated."""
    import yaml
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.setenv("AGI_SEASON", "1")
    res = nw.write_node(project, "mvp", "norole",
                        parents=["verdict:v1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert "role" not in fm


def test_minted_node_omits_loop_when_env_absent(project, monkeypatch):
    """Absent env vars must NOT fabricate values.

    Controls every AGI_* stamp source: the harness shell (this test suite
    can run under a dispatched session that exports AGI_LOOP/AGI_MODEL/
    AGI_PROFILE) must not leak into an 'absent' assertion. Masked before
    hypothesis:l3w0-ladder-roles-table by the season early-return bug, which
    silently skipped loop/model/profile whenever AGI_SEASON parsed."""
    import yaml
    monkeypatch.setenv("AGI_SEASON", "1")
    for v in ("AGI_LOOP", "AGI_MODEL", "AGI_PROFILE", "AGI_ROLE"):
        monkeypatch.delenv(v, raising=False)
    res = nw.write_node(project, "mvp", "bare",
                        parents=["verdict:v1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("season") == 1
    assert "loop" not in fm
    assert "model" not in fm
    assert "profile" not in fm
    assert "role" not in fm


def test_update_node_does_not_add_stamps(project, monkeypatch):
    """`update_node` must NOT call `_stamp_env_fields`. An existing node
    without season/loop/model/profile keeps them absent after an update."""
    import yaml
    monkeypatch.setenv("AGI_SEASON", "42")
    monkeypatch.setenv("AGI_LOOP", "goal:g1@s42")
    monkeypatch.setenv("AGI_MODEL", "deepseek/deepseek-v4")
    monkeypatch.setenv("AGI_PROFILE", "fast")

    res = nw.update_node(project, "hypothesis:h1",
                         set_fm={"verdict": "proved"},
                         validate=False, announce=False)
    assert res.status == nw.UPDATED
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert "season" not in fm, "update must not add season"
    assert "loop" not in fm, "update must not add loop"
    assert "model" not in fm, "update must not add model"
    assert "profile" not in fm, "update must not add profile"


def test_minted_node_season_defaults_to_1_without_ladder_or_env(
        monkeypatch, tmp_path):
    """When no ladder node exists and no env var is set, season defaults to 1."""
    import yaml
    # Build a project with NO ladder node and a valid config marker
    no_ladder = tmp_path / "no-ladder"
    no_ladder.mkdir(parents=True)
    (no_ladder / "agi-tree.config.json").write_text("{}")
    # Minimal schemas
    sd = no_ladder / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[shape].md").write_text(
        "---\nname: shape\nparentless_types: [idea]\n"
        "max_parents_ceiling: 2\n---\n")
    (sd / "[hypothesis].md").write_text(
        "---\nname: hypothesis\nspawn:\n  allowed_parents: [idea]\n"
        "  min_parents: 1\n  max_parents: 2\n---\n")
    nd = no_ladder / "nodes"
    nd.mkdir(parents=True)
    (nd / "idea").mkdir()
    (nd / "idea/i1.md").write_text(
        "---\nid: idea:i1\ntype: idea\n---\n\nb\n")

    res = nw.write_node(no_ladder, "hypothesis", "default-season",
                        parents=["idea:i1"], announce=False)
    assert res.written, f"{res.status} {res.reason}"
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    assert fm.get("season") == 1


def test_env_season_that_cannot_be_parsed_falls_back_to_ladder(
        project, monkeypatch):
    """A non-integer AGI_SEASON is silently ignored (falls through to ladder)."""
    import yaml
    monkeypatch.setenv("AGI_SEASON", "not-a-number")
    res = nw.write_node(project, "experiment", "bad-season",
                        parents=["hypothesis:h1"], announce=False)
    assert res.written
    fm = yaml.safe_load(res.path.read_text().split("---", 2)[1])
    # Falls back to ladder's current_season: 1
    assert fm.get("season") == 1


# --------------------------------------------------------------------------
# hypothesis:l2-done-doubled-frontmatter — a duplicate leading frontmatter
# block living in the body (a kid that kept the scaffold's frontmatter) is
# absorbed into the real frontmatter, later keys winning, and stripped.
# Reproduces L2.01: experiment:a00-e65beccc-ac5309 arrived with a duplicate
# scaffold FM block left in the body after cli.py done wrote the verdict.
# --------------------------------------------------------------------------

def test_update_node_absorbs_a_duplicate_leading_frontmatter_block(project):
    """A body that opens with a second --- block is merged, dup removed."""
    import yaml
    nf = project / "nodes" / "experiment" / "e1.md"
    dup = ("---\nid: experiment:e1\ntype: experiment\n"
           "title: Kid Kept The Scaffold Frontmatter\n---\n")
    # The kid's rewrite: real scaffold frontmatter, then the scaffold's own
    # frontmatter pasted again at the top of the body.
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\ntitle: Real Title\n---"
        f"\n\n{dup}\n# experiment:e1\n\nkid content\n")

    res = nw.update_node(project, "experiment:e1",
                         set_fm={"verdict": "proved", "confidence": 0.9})
    assert res.status == nw.UPDATED, res.reason

    text = nf.read_text()
    # One real frontmatter block (open + close = exactly two --- lines).
    assert text.count("---") == 2, text
    # The verdict landed in the real frontmatter.
    fm = yaml.safe_load(text.split("---", 2)[1])
    assert fm.get("verdict") == "proved"
    assert fm.get("confidence") == 0.9
    # The duplicate's keys were absorbed into the real block, later keys
    # winning (the body's title is the one that survives).
    assert fm.get("title") == "Kid Kept The Scaffold Frontmatter"
    # And the duplicate text is gone from the body.
    body = text.split("---", 2)[2]
    assert "id: experiment:e1" not in body
    assert "Kid Kept The Scaffold Frontmatter" not in body
    # The kid's real content survived.
    assert "kid content" in body


def test_update_node_leaves_a_body_without_leading_frontmatter_alone(project):
    """No leading dup -> normally equivalent update, verdict still written."""
    import yaml
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\ntitle: Real Title\n---"
        "\n\n# experiment:e1\n\nplain content\n")
    res = nw.update_node(project, "experiment:e1",
                         set_fm={"verdict": "disproved", "confidence": 0.3})
    assert res.status == nw.UPDATED
    text = nf.read_text()
    assert text.count("---") == 2
    fm = yaml.safe_load(text.split("---", 2)[1])
    assert fm.get("verdict") == "disproved"
    assert "plain content" in text.split("---", 2)[2]


# --------------------------------------------------------------------------
# hypothesis:l3-node-without-mint-id — a node written outside node_writer (a
# kid's own file tool) carries no `mint_id`, so grid.py refuses to version it.
# `repair_mint` is the one sanctioned adoption: mint a FIRST mint_id through
# the same identity source as every mint, stamp scaffold_hash so it reads
# complete, and refuse when a `mint_id` already exists.
# --------------------------------------------------------------------------

def _no_mint_node(project, body="the kid wrote this body\n"):
    """A kid-written node: valid frontmatter, real content, no mint_id, no
    scaffold_hash — exactly experiment:a00-230456c1-1abcda's shape."""
    p = project / "nodes" / "experiment" / "e1.md"
    p.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        f"parents:\n- hypothesis:h1\n---\n\n{body}")
    return p


def test_repair_mint_mints_a_first_mint_id_and_preserves_the_body(project):
    import yaml
    nf = _no_mint_node(project)
    res = nw.repair_mint(project, "experiment:e1", announce=False)
    assert res.status == nw.UPDATED, res.reason
    text = nf.read_text()
    assert text.count("---") == 2
    fm = yaml.safe_load(text.split("---", 2)[1])
    # a durable mint_id was minted
    assert isinstance(fm.get("mint_id"), str) and fm["mint_id"].strip()
    # scaffold_hash stamped so the adopted node reads complete
    assert isinstance(fm.get("scaffold_hash"), str) and fm["scaffold_hash"]
    # the kid's content survived untouched
    assert "the kid wrote this body" in text.split("---", 2)[2]


def test_repair_mint_refuses_when_a_mint_id_already_exists(project):
    import yaml
    nf = _no_mint_node(project)
    # give it a mint_id first
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "mint_id: existing-mint-123\nparents:\n- hypothesis:h1\n---\n\nbody\n")
    res = nw.repair_mint(project, "experiment:e1", announce=False)
    assert res.status == nw.SKIPPED
    assert "already" in res.reason
    # the mint_id is untouched
    text = nf.read_text()
    assert "existing-mint-123" in text


def test_repair_mint_reads_complete_after_adoption(project):
    """Stamping scaffold_hash of the placeholder (not of the real body) means
    the adopted node reads COMPLETE under completion.is_complete — a kid node
    already holds real content, so it is not an untouched scaffold."""
    import completion
    _no_mint_node(project)
    # After adoption the node reads COMPLETE by the SAME predicate dispatch
    # uses (the fallback path, without a scaffold_hash, also reads complete
    # here because the kid's real content differs from the prompt -- the
    # stamp pins that answer drift-free).
    res = nw.repair_mint(project, "experiment:e1", announce=False)
    assert res.status == nw.UPDATED
    assert completion.is_complete(project, "experiment:e1") is True


def test_repair_mint_refuses_an_unparseable_node(project):
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text("no frontmatter here\n")
    res = nw.repair_mint(project, "experiment:e1", announce=False)
    assert res.status == nw.REJECTED


def test_repair_mint_refuses_unknown_node(project):
    res = nw.repair_mint(project, "experiment:nope", announce=False)
    assert res.status == nw.REJECTED
    assert "no node file" in res.reason
