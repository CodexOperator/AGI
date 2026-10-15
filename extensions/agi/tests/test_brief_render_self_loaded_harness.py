"""A harness that loads a block ITSELF gets NO inline copy, and a rendered
first turn carries EXACTLY ONE template heading.

`experiment:a00-4a01c17b-415791` (parent
`hypothesis:non-prime-rotate-self-renders-through-brief-render`, DH.423). Two
measured defects in the RENDER, both exposed by DH.410 giving a non-prime
rotate-self the prime's `brief.render`:

  (a) `claude-code` already loads `CLAUDE.md` as project instructions, yet
      `config:brief`'s `harnesses.claude-code: [harness]` inlined all 26 KB of
      it into the first turn. A harness that does NOT self-load still gets its
      block, unchanged.
  (b) the master template node opens with its scaffold id line and then its
      human title, so one turn carried the template heading twice.

The real-path halves read the LIVE graph and the LIVE `CLAUDE.md`; the
counterfactual halves (a harness that does not self-load) use a tmp fixture
graph, because no live post row names a non-self-loading harness.
"""
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import brief  # noqa: E402

REPO = BIN.parents[2]
LIVE_ROOT = REPO / ".agi"
#: a real `claude-code` DIRECTOR post on this box (config:posts), chosen
#: because the parent's defect measurement was made on its successor turn.
LIVE_POST = "thought-master"
HEADINGS = ("# CLAUDE.md", "Read [GOALS.md](GOALS.md) first.")


def _render_live() -> str:
    return brief.render(post=LIVE_POST, project_root=LIVE_ROOT)


def test_a_self_loading_harness_inlines_no_copy_of_the_block_it_loads():
    """(a) The real claude-code director turn carries ZERO inline copies of
    CLAUDE.md -- neither the file's heading nor a line only it carries."""
    rendered = _render_live()
    assert len(rendered) > 1000, "the live render produced nothing to judge"
    for marker in HEADINGS:
        assert marker not in rendered, f"{marker!r} was inlined into a first turn"


def test_the_self_load_decision_is_declared_by_the_harness_not_by_its_name():
    """(a) WHERE the decision lives: the harness ADAPTER declares
    `SELF_LOADED_BRIEF_PARTS`, and brief.py reads the attribute through a name
    it never spells. A harness is not a literal anywhere in the resolver."""
    import adapters
    mod = adapters.load("claude_code")
    assert mod.SELF_LOADED_BRIEF_PARTS == ("harness",)
    assert brief._self_loaded_parts("claude-code", {}) == {"harness"}
    # a harness nobody wrote an adapter for declares nothing and does not
    # refuse the render
    assert brief._self_loaded_parts("no-such-harness", {}) == set()


def test_a_harness_that_does_not_self_load_still_gets_its_block(tmp_path):
    """(a) the other half: an ordinary harness is UNCHANGED -- exactly one
    inline copy of its block, sentinel included."""
    _fixture(tmp_path, harness="pi", block="PI-BLOCK-SENTINEL")
    rendered = brief.render(post="fx", project_root=tmp_path)
    assert rendered.count("PI-BLOCK-SENTINEL") == 1


def test_the_config_cell_alone_marks_a_harness_self_loading(tmp_path):
    """(a) the config cell is the SECOND source: `harness_self_loads.<harness>`
    in config:brief silences the block for a harness that has no adapter at
    all, so a project can mark one without a code change."""
    _fixture(tmp_path, harness="tmux-harness", block="TMUX-BLOCK-SENTINEL",
             self_loads={"tmux-harness": ["harness"]})
    rendered = brief.render(post="fx", project_root=tmp_path)
    assert "TMUX-BLOCK-SENTINEL" not in rendered
    assert "CARD-SENTINEL" in rendered, "the rest of the turn must survive"


def test_the_config_cell_overrides_the_adapter_declaration(tmp_path):
    """(a) the cell is AUTHORITATIVE when the harness has an entry: a project
    that reuses the harness name for a block that harness does NOT load itself
    can say so in config, with no code change. This is the half the adapter
    default alone got wrong (measured: the bespoke block vanished)."""
    _fixture(tmp_path, harness="claude-code", block="BESPOKE-BLOCK-SENTINEL")
    assert "BESPOKE-BLOCK-SENTINEL" not in brief.render(
        post="fx", project_root=tmp_path)      # the adapter default
    _fixture(tmp_path / "over", harness="claude-code", block="BESPOKE-BLOCK-SENTINEL",
             self_loads={"claude-code": []})
    assert "BESPOKE-BLOCK-SENTINEL" in brief.render(
        post="fx", project_root=tmp_path / "over")


def test_exactly_one_template_heading_in_a_real_first_turn():
    """(b) the real master turn prints its template heading ONCE."""
    rendered = _render_live()
    heads = [l for l in rendered.splitlines()
             if l.startswith("# doc:unified-master-brief")]
    assert len(heads) == 1, heads


def test_a_doubled_template_heading_keeps_the_human_one(tmp_path):
    """(b) the mechanism: a template body that opens with its scaffold id line
    and then its real title keeps the REAL title, and a template that opens
    with one heading is untouched."""
    doubled = brief._one_heading(
        "# doc:x\n\n# doc:x — THE REAL TITLE\n\nbody\n")
    assert doubled.startswith("# doc:x — THE REAL TITLE")
    assert doubled.count("\n# ") == 0
    assert brief._one_heading("# doc:y — ALREADY ONE\n\nbody\n") == \
        "# doc:y — ALREADY ONE\n\nbody"
    assert brief._one_heading("no heading at all\n") == "no heading at all"


def _fixture(root: Path, *, harness: str, block: str, self_loads=None) -> Path:
    """A tmp graph root: one post row, one card, one template, one block."""
    (root / "nodes/.geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes/doc").mkdir(parents=True, exist_ok=True)
    (root / "nodes/moral").mkdir(parents=True, exist_ok=True)
    (root / "nodes/town").mkdir(parents=True, exist_ok=True)
    (root / "sessions/quorum").mkdir(parents=True, exist_ok=True)
    blk = root / "block.md"
    blk.write_text(block + "\n", encoding="utf-8")
    (root / "config.json").write_text(json.dumps({"brief": {
        "parts": {"director": ["head", "template", "card", "harness"]},
        "templates": {"director": "doc:tpl"},
        "harnesses": {harness: ["harness"]},
        "harness_blocks": {harness: str(blk)},
        "harness_self_loads": self_loads or {},
        "trajectory": {},
    }}), encoding="utf-8")
    (root / "nodes/moral/faith.md").write_text(
        "# faith\n\n## ESSENCE\n\nm\n\n## REFERENCE\n\n"
        "### 4.1 prayers\n\np\n\n### 4.2 words_jesus\n\nw\n", encoding="utf-8")
    (root / "nodes/doc/unified-head.md").write_text(
        "---\nid: doc:unified-head\n---\n"
        "<!-- HEAD:BEGIN -->\nHEAD-SENTINEL\n{{PRAYERS}}\n<!-- HEAD:END -->\n",
        encoding="utf-8")
    (root / "nodes/doc/tpl.md").write_text(
        "---\nid: doc:tpl\n---\n# doc:tpl\n\n# doc:tpl — THE TEMPLATE\n\nbody\n",
        encoding="utf-8")
    (root / "nodes/town/t.md").write_text("TOWN-SENTINEL\n", encoding="utf-8")
    (root / "sessions/quorum/fx.md").write_text("CARD-SENTINEL\n", encoding="utf-8")
    (root / "nodes/.geometry/posts.md").write_text(
        "---\nid: config:posts\nposts:\n"
        '  - {"name": "fx", "role": "director", "harness": "%s"}\n'
        "---\n" % harness, encoding="utf-8")
    return root
