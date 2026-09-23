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
          trajectory=None, extras=None, card=None, harness="claude-code") -> Path:
    """A minimal tmp graph root with the parts the claim needs."""
    block = _write(tmp_path, "harness-block.md", "HARNESS-BLOCK-SENTINEL\n")
    if harness_blocks is None:
        harness_blocks = {"claude-code": str(block)}
    _write(tmp_path, "config.json", json.dumps({"brief": {
        "parts": parts,
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


def test_template_expands_one_level_only(tmp_path):
    """The card's `{{template:doc:inner}}` expands; the template line the
    expansion itself carries is NOT re-expanded (one level)."""
    root = _root(tmp_path, parts={"director": ["card"]})
    out = brief.render(post="some-post", project_root=root)
    assert "INNER-BODY-SENTINEL" in out
    assert "DEEPER-SENTINEL" not in out
    assert "{{template:doc/deeper}}" in out, "one level means the inner line stays literal"


def test_a_missing_template_node_refuses(tmp_path):
    """Falsifier: a `{{template:}}` over a missing node renders an empty
    string. It must refuse by name instead."""
    root = _root(tmp_path, parts={"director": ["card"]},
                 card="{{template:doc:nope}}\n")
    with pytest.raises(brief.RenderError) as exc:
        brief.render(post="some-post", project_root=root)
    assert "doc:nope" in str(exc.value)


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


def test_rotated_successor_is_head_plus_card(tmp_path, monkeypatch):
    """Falsifier: a rotated successor's first turn lacks the head or its card.

    A DIRECTOR successor built by rotate.py's non-prime path is the SAME
    render the SessionStart hook prints: render's head part, then the post's
    card. Fixtures: a director post and a prime_director post.
    """
    sys.path.insert(0, str(BIN))
    import rotate

    root = _root(tmp_path, parts={"director": ["head", "card"],
                                  "prime_director": ["head", "card"]})
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
    assert "CARD-SENTINEL" in body

    # the Prime fixture: rotate-self hands the card as the body through
    # successor_prompt, which prepends the SAME head bytes.
    prime = brief.successor_prompt(
        tier="prime_director", body="PRIME-CARD-SENTINEL", project_root=root)
    assert prime.startswith(brief.render_head(project_root=root))
    assert "PRIME-CARD-SENTINEL" in prime


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
