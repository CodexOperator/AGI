"""`hypothesis:brief-py-assembles-every-first-turn-from-config` — phase 1.

The claim: `brief.py render` returns the WHOLE first user turn for any role
(Prime, master, director, parent, kid) assembled from ONE config cell — the
head (byte-identical across roles), the post's card with its
`{{template:<node id>}}` lines expanded one level, the harness block and the
town trajectory — and writes NO injection file.

Each test is a falsifier from the hypothesis node, pinned red-first.
"""
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN / "adapters"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import brief  # noqa: E402

HEAD_SENTINEL = "HEAD-BYTES-SENTINEL-7f2c"
PRAYERS_SENTINEL = "PRAYERS-SENTINEL-2b91"
FAITH = (
    "# faith\n\n## ESSENCE\n\nmoral region\n\n## REFERENCE\n\n"
    "### 4.1 prayers\n\n" + PRAYERS_SENTINEL + "\n\n"
    "### 4.2 words_jesus\n\nwords\n"
)
ROLES = ("kid", "parent", "director", "prime_director", "master")


def _write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _root(tmp_path: Path, *, parts, harnesses=None, harness_blocks=None,
          trajectory=None, extras=None, card=None, harness="claude-code",
          templates=None) -> Path:
    """A minimal tmp graph root with the parts the claim needs."""
    block = _write(tmp_path, "harness-block.md", "HARNESS-BLOCK-SENTINEL\n")
    if harness_blocks is None:
        harness_blocks = {"claude-code": str(block)}
    _write(tmp_path, "config.json", json.dumps({"brief": {
        "parts": parts,
        "templates": templates or {},
        "harnesses": harnesses if harnesses is not None else {"claude-code": ["harness"]},
        "harness_blocks": harness_blocks,
        "trajectory": trajectory if trajectory is not None else {"town": "t"},
        "extras": extras or {},
    }}))
    _write(tmp_path, "nodes/moral/faith.md", FAITH)
    _write(tmp_path, "nodes/doc/unified-head.md",
           "---\nid: doc:unified-head\n---\n"
           "<!-- HEAD:BEGIN -->\n" + HEAD_SENTINEL + "\n{{PRAYERS}}\n<!-- HEAD:END -->\n")
    _write(tmp_path, "nodes/doc/inner.md", "INNER-BODY-SENTINEL\n\n{{template:doc/deeper}}\n")
    _write(tmp_path, "nodes/doc/deeper.md", "DEEPER-SENTINEL\n")
    _write(tmp_path, "nodes/town/t.md", "TOWN-TRAJECTORY-SENTINEL\n")
    _write(tmp_path, "sessions/quorum/some-post.md",
           card if card is not None else "CARD-SENTINEL\n\n{{template:doc:inner}}\n")
    _write(tmp_path, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           '  - {"name": "some-post", "role": "director", "harness": "' + harness + '"}\n'
           "---\n")
    return tmp_path


def _files(root: Path):
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


def test_head_bytes_are_identical_across_all_five_roles(tmp_path):
    """Falsifier 1: the head bytes differ between any two roles. The head is
    one doc region and takes no role, so all five renders agree byte for byte."""
    root = _root(tmp_path, parts={role: ["head"] for role in ROLES})
    heads = {role: brief.render(role=role, project_root=root) for role in ROLES}
    assert len(set(heads.values())) == 1, {k: v[:80] for k, v in heads.items()}
    assert HEAD_SENTINEL in heads["kid"]
    assert PRAYERS_SENTINEL in heads["kid"], "{{PRAYERS}} must be filled from moral:faith"


def test_one_config_line_adds_or_removes_a_part(tmp_path):
    """Falsifier 2: adding or removing a part needs a code change. Flip the
    config cell alone and the rendered turn changes with it."""
    root = _root(tmp_path, parts={"director": ["head"]})
    assert "CARD-SENTINEL" not in brief.render(post="some-post", project_root=root)
    _write(root, "config.json", json.dumps({"brief": {"parts": {"director": ["head", "card"]}}}))
    assert "CARD-SENTINEL" in brief.render(post="some-post", project_root=root)


def test_card_is_data_and_is_never_expanded(tmp_path):
    """The amendment (owner 08:5xZ): a card is DATA. A `{{template:}}`
    line in a card is NOT an expansion directive -- the ROLE template comes
    from the config cell/row, never from a line in the card."""
    root = _root(tmp_path, parts={"director": ["card"]})
    out = brief.render(post="some-post", project_root=root)
    assert "{{template:doc:inner}}" in out, "the card's template line stays literal"
    assert "INNER-BODY-SENTINEL" not in out


def test_missing_template_node_is_refused_by_name(tmp_path):
    """A named ROLE template that does not resolve must refuse BY NAME, not
    render an empty string."""
    root = _root(tmp_path, parts={"director": ["head", "template", "card"]},
                 templates={"director": "doc:nope"})
    with pytest.raises(brief.RenderError) as exc:
        brief.render(post="some-post", project_root=root)
    assert "doc:nope" in str(exc.value)


def test_template_part_is_chosen_by_role_and_row_overrides(tmp_path):
    """The template is CONFIG: the formation default for the role, beaten by
    a `template` cell on the post's own `config:posts` row."""
    _write(tmp_path, "nodes/doc/director-brief.md", "DIRECTOR-BRIEF-SENTINEL\n")
    _write(tmp_path, "nodes/doc/row-brief.md", "ROW-BRIEF-SENTINEL\n")
    root = _root(tmp_path, parts={"director": ["head", "template", "card"]},
                 templates={"director": "doc:director-brief"})
    out = brief.render(post="some-post", project_root=root)
    assert "DIRECTOR-BRIEF-SENTINEL" in out
    assert "ROW-BRIEF-SENTINEL" not in out
    _write(root, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           '  - {"name": "some-post", "role": "director", "template": "doc:row-brief"}\n'
           "---\n")
    over = brief.render(post="some-post", project_root=root)
    assert "ROW-BRIEF-SENTINEL" in over
    assert "DIRECTOR-BRIEF-SENTINEL" not in over


def test_build_template_reads_its_payload(tmp_path):
    """A build node's template is its PAYLOAD file, not the contract body."""
    payload = _write(tmp_path, "payload-brief.md", "PAYLOAD-BRIEF-SENTINEL\n")
    _write(tmp_path, "nodes/build/the-prime-brief.md",
           "---\nid: build:the-prime-brief\npayload_ref: " + str(payload) + "\n---\n"
           "<!-- BODY:BEGIN -->\n# build:the-prime-brief\n\nCONTRACT-WORDS\n")
    root = _root(tmp_path, parts={"prime_director": ["template"]},
                 templates={"prime_director": "build:the-prime-brief"})
    out = brief.render(role="prime_director", project_root=root)
    assert "PAYLOAD-BRIEF-SENTINEL" in out
    assert "CONTRACT-WORDS" not in out


def test_render_writes_no_file(tmp_path):
    """Falsifier 3: a render writes INJECTION.md or another cache file."""
    root = _root(tmp_path, parts={"director": ["head", "card", "harness", "trajectory"]})
    before = _files(root)
    out = brief.render(post="some-post", project_root=root)
    assert out
    assert _files(root) == before, "a render must create or modify nothing"
    assert not (root / "INJECTION.md").exists()
    assert not (root / "context" / "INJECTION.md").exists()


def test_post_row_resolves_role_and_harness_and_pi_adds_nothing(tmp_path):
    """`--post` resolves role + harness from the row; the claude-code harness
    adds its block, a pi post (unconfigured) adds nothing."""
    parts = {"director": ["head", "card"]}
    root = _root(tmp_path, parts=parts, harness="claude-code")
    assert "HARNESS-BLOCK-SENTINEL" in brief.render(post="some-post", project_root=root)
    root_pi = _root(tmp_path / "pi", parts=parts, harness="pi")
    assert "HARNESS-BLOCK-SENTINEL" not in brief.render(post="some-post", project_root=root_pi)


def test_render_fails_loudly_on_an_unknown_post_or_part(tmp_path):
    root = _root(tmp_path, parts={"director": ["head"]})
    with pytest.raises(brief.RenderError):
        brief.render(post="no-such-post", project_root=root)
    _write(root, "config.json", json.dumps({"brief": {"parts": {"director": ["head", "typo"]}}}))
    with pytest.raises(brief.RenderError) as exc:
        brief.render(post="some-post", project_root=root)
    assert "typo" in str(exc.value)


# ---- phase 2: the cell is COMMITTABLE, and rotate/the hook share ONE head ----


def test_render_reads_the_committed_config_brief_node(tmp_path):
    """The cell must live where a round's own `done` commit can carry it.

    `cli.py:_round_scope_ok` refuses `.agi/config.json`, so the phase-1 cell
    there was absent from the landed branch and a fresh checkout could not
    render (`experiment:a00-15fc3737-5e48d5`). A `config:brief` NODE named in
    `done --owns` is committed -- here config.json carries NO brief cell and
    the node alone drives the render.
    """
    root = _root(tmp_path, parts={"director": ["head", "card"]})
    _write(root, "config.json", json.dumps({}))
    _write(root, "nodes/.geometry/brief.md",
           "---\nid: config:brief\nbrief:\n"
           "  parts: {director: [head, card]}\n  harness_blocks: {}\n---\n"
           "# config:brief\n")
    out = brief.render(post="some-post", project_root=root)
    assert HEAD_SENTINEL in out
    assert "CARD-SENTINEL" in out


def test_rotated_successor_is_head_plus_template_plus_card(tmp_path, monkeypatch):
    """Falsifier: a rotated successor's first turn lacks the head, its role
    template, or its card. A DIRECTOR successor built by rotate.py's
    non-prime path is the SAME render the SessionStart hook prints: head,
    then the config-chosen role template, then the post's card. Fixtures: a
    director post and a prime_director post."""
    sys.path.insert(0, str(BIN))
    import rotate

    root = _root(tmp_path, parts={"director": ["head", "template", "card"],
                                  "prime_director": ["head", "template", "card"]},
                 templates={"director": "doc:director-brief",
                            "prime_director": "doc:director-brief"})
    _write(root, "nodes/doc/director-brief.md", "DIRECTOR-TEMPLATE-SENTINEL\n")
    _write(root, "sessions/quorum/prime-post.md", "PRIME-CARD-SENTINEL\n")
    _write(root, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           '  - {"name": "some-post", "role": "director", "harness": "pi"}\n'
           '  - {"name": "prime-post", "role": "prime_director", "harness": "pi"}\n'
           "---\n")

    seen = {}
    monkeypatch.setattr(
        rotate, "_build_harness_command",
        lambda harness, **kw: (seen.setdefault("prompt", kw["prompt_text"]), ["x"])[1])
    rotate._assembled_successor_command(
        name="some-post", tier="director", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi", project_root=root)
    body = seen["prompt"]
    assert body.startswith(brief.render_head(project_root=root))
    assert "DIRECTOR-TEMPLATE-SENTINEL" in body
    assert "CARD-SENTINEL" in body
    assert body.index("DIRECTOR-TEMPLATE-SENTINEL") < body.index("CARD-SENTINEL")

    # the Prime fixture: render's prime_director parts carry the card too.
    prime = brief.render(post="prime-post", project_root=root)
    assert prime.count("PRIME-CARD-SENTINEL") == 1
    assert "DIRECTOR-TEMPLATE-SENTINEL" in prime


def test_hook_head_equals_rotate_head_at_one_sha():
    """Falsifier: the head bytes differ between two roles, or between the
    SessionStart hook and a rotated successor. `brief.py head` and
    `successor_prompt` both read `render`'s ONE head part."""
    import io
    out = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = out
        code = brief.main(["head", "--tier", "director"])
    finally:
        sys.stdout = old
    assert code == 0
    hook = out.getvalue().strip()
    prompt = brief.successor_prompt(tier="director", body="THE-CARD-BODY")
    assert prompt[:prompt.index("THE-CARD-BODY")].strip() == hook
    assert hook == brief.render_head()
