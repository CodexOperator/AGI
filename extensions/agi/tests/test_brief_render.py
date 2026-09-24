"""`hypothesis:brief-py-assembles-every-first-turn-from-config` — phase 1.

The claim: `brief.py render` returns the WHOLE first user turn for any role
(Prime, master, director, parent, kid) assembled from ONE config cell — the
head (byte-identical across roles), the post's card (data, never expanded),
the harness block and the town trajectory — and writes NO injection file.

Each test is a falsifier from the hypothesis node, pinned red-first.
"""
import json
import subprocess
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


def test_every_pi_role_brief_names_the_paid_for_path_guard(monkeypatch,
                                                            tmp_path):
    """Pi skips repository context files, so its role briefs must carry the
    one context rule agents still need, sourced from the module constant."""
    sentinel = "PAID-FOR-PATH-GUARD-SENTINEL"
    monkeypatch.setattr(brief, "PAID_FOR_PATH_GUARD", sentinel)
    kid = "\n".join(brief.assemble(
        tier="kid", agent_id="a", iter_n=1, cli_py="cli.py", scaffold=None))
    parent = "\n".join(brief.assemble(
        tier="parent", agent_id="a", iter_n=1, cli_py="cli.py",
        dispatch_py="dispatch.py", target="hypothesis:x"))
    assert sentinel in kid
    assert sentinel in parent
    for tier in ("director", "prime_director", "liaison"):
        rendered = "\n".join(brief.assemble(
            tier=tier, agent_id="a", iter_n=1, cli_py="cli.py",
            dispatch_py="dispatch.py", target=None))
        assert sentinel in rendered
    advisor = "\n".join(brief.assemble(
        tier="advisor", agent_id="a", iter_n=1, cli_py="cli.py",
        dispatch_py="dispatch.py", target="vision:alive"))
    assert sentinel in advisor
    for profile in ("survival", "ultimate_survival"):
        # project_root=tmp_path keeps the survival state card off the LIVE
        # repo: with no root, brief.assemble -> _survival_state_card runs a
        # real `git status` against this checkout (brief.py:753-760).
        rendered = "\n".join(brief.assemble(
            tier="kid", agent_id="a", iter_n=1, cli_py="cli.py",
            scaffold=None, profile=profile, project_root=tmp_path))
        assert sentinel in rendered


def test_survival_state_card_uses_the_passed_project_root(tmp_path):
    """The survival card's TREE row follows each passed repository root."""
    roots = []
    for name, count in (("two", 2), ("five", 5)):
        root = tmp_path / name
        root.mkdir()
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for index in range(count):
            (root / f"untracked-{name}-{index}.txt").write_text(
                "untracked\n", encoding="utf-8")
        roots.append((root, count))

    for profile in ("survival", "ultimate_survival"):
        rendered = [
            "\n".join(brief.assemble(
                tier="kid", agent_id="a", iter_n=1, cli_py="cli.py",
                scaffold=None, profile=profile, project_root=root))
            for root, _ in roots
        ]
        assert "TREE  2 dirty/unreviewed" in rendered[0]
        assert "TREE  2 dirty/unreviewed" not in rendered[1]
        assert "TREE  5 dirty/unreviewed" in rendered[1]
        assert "TREE  5 dirty/unreviewed" not in rendered[0]


def test_default_profile_resolution_follows_project_root(monkeypatch, tmp_path):
    """The full sentinel must re-resolve the supplied root's own mode."""
    monkeypatch.delenv("AGI_BRIEF_PROFILE", raising=False)
    renders = {}
    for name, mode in (("survival", "survival"), ("full", "full")):
        root = _root(tmp_path / name, parts={"kid": []})
        cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
        cfg["operating_mode"] = mode
        (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
        renders[name] = "\n".join(brief.assemble(
            tier="kid", agent_id="a", iter_n=1, cli_py="cli.py",
            scaffold=None, project_root=root))
    assert "SURVIVAL PROFILE" in renders["survival"]
    assert "SURVIVAL PROFILE" not in renders["full"]


def test_paid_for_path_guard_follows_project_config(tmp_path):
    root = _root(tmp_path, parts={"kid": ["head"]})
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    cfg["brief"]["paid_for_path_guard"] = "CONFIG-GUARD-SENTINEL"
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    rendered = "\n".join(brief.assemble(
        tier="kid", agent_id="a", iter_n=1, cli_py="cli.py",
        project_root=root))
    assert "CONFIG-GUARD-SENTINEL" in rendered


def test_survival_brief_paid_for_path_guard_follows_project_config(tmp_path):
    """The survival SUCCESSOR path (successor_prompt), not assemble() —
    assemble(profile="survival") already goes through _finish()'s
    substitution and would pass even without _survival_brief's own fix;
    successor_prompt does not call _finish() at all (mur-9-5)."""
    root = _root(tmp_path, parts={"kid": ["head"]})
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    cfg["brief"]["paid_for_path_guard"] = "SURVIVAL-CONFIG-GUARD-SENTINEL"
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    rendered = brief.successor_prompt(tier="kid", body="UNUSED-BODY",
                                      profile="survival", project_root=root)
    assert "SURVIVAL-CONFIG-GUARD-SENTINEL" in rendered
    assert brief.PAID_FOR_PATH_GUARD not in rendered


def test_paid_for_path_guard_follows_config_brief_node(tmp_path):
    root = _root(tmp_path, parts={"kid": ["head"]})
    _write(root, "nodes/config/brief.md",
           "---\nid: config:brief\nbrief:\n"
           "  paid_for_path_guard: NODE-GUARD-SENTINEL\n---\n")
    rendered = "\n".join(brief.assemble(
        tier="kid", agent_id="a", iter_n=1, cli_py="cli.py",
        project_root=root))
    assert "NODE-GUARD-SENTINEL" in rendered


def test_render_carries_paid_for_path_guard_for_pi_free_and_pi(monkeypatch, tmp_path):
    sentinel = "RENDER-PAID-FOR-PATH-GUARD-SENTINEL"
    monkeypatch.setattr(brief, "PAID_FOR_PATH_GUARD", sentinel)
    for role, harness in (("kid", "pi-free"), ("parent", "pi-free"),
                          ("director", "pi")):
        root = _root(tmp_path / f"{role}-{harness}",
                     parts={role: ["head"]})
        rendered = brief.render(role=role, harness=harness, project_root=root)
        assert rendered.count(sentinel) == 1, (role, harness)


def test_render_paid_for_path_guard_override_is_exactly_once(tmp_path):
    root = _root(tmp_path, parts={"kid": ["head"]})
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    cfg["brief"]["paid_for_path_guard"] = "RENDER-OVERRIDE-SENTINEL"
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    rendered = brief.render(role="kid", harness="pi-free", project_root=root)
    assert rendered.count("RENDER-OVERRIDE-SENTINEL") == 1
    assert brief.PAID_FOR_PATH_GUARD not in rendered


def test_render_does_not_duplicate_paid_for_path_guard_in_a_part(tmp_path):
    """render() must not duplicate a guard already present in a part
    (extras_text, not card+post — see the sibling override test's
    docstring for why card+post silently renders the wrong role)."""
    root = _root(tmp_path, parts={"kid": ["extras"]})
    rendered = brief.render(role="kid", harness="pi-free",
                            extras_text=brief.PAID_FOR_PATH_GUARD + "\nEXTRAS-SENTINEL",
                            project_root=root)
    assert rendered.count(brief.PAID_FOR_PATH_GUARD) == 1


def test_render_override_replaces_guard_already_present_in_a_part(tmp_path):
    """A configured guard replaces historical prose already in a part,
    rather than joining it (mur-9-4). Uses extras_text, not card+post: the
    _root() fixture's posts.md row hardcodes role="director", so post=
    silently overrides any role=/harness= kwarg and a card-based fixture
    never actually renders the content it thinks it does."""
    root = _root(tmp_path, parts={"kid": ["extras"]})
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    override = "HISTORICAL-GUARD-REPLACEMENT-SENTINEL"
    cfg["brief"]["paid_for_path_guard"] = override
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")

    rendered = brief.render(role="kid", harness="pi-free",
                            extras_text=brief.PAID_FOR_PATH_GUARD + "\nEXTRAS-SENTINEL",
                            project_root=root)

    assert rendered.count(override) == 1
    assert brief.PAID_FOR_PATH_GUARD not in rendered


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


def test_config_schema_declares_the_template_post_row_cell():
    """Conjunct: the `template` post-row cell is declared in
    `.agi/context/schemas/[config].md` under `fields.seats`, as the role
    template node ref that beats `brief.templates[<role>]`."""
    repo = BIN.parents[2]
    schema = (repo / ".agi" / "context" / "schemas" / "[config].md").read_text(
        encoding="utf-8")
    row = schema[schema.index("seats: {type: list}"):]
    row = row[:row.index("posts: {type: list}")]
    assert "template" in row, "the post row's `template` cell is declared"
    assert "brief.templates" in row, \
        "the clause names what `template` beats (brief.templates[<role>])"


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


def test_the_template_macro_is_gone_and_renders_literal(tmp_path):
    """The `{{template:}}` mechanism is REMOVED (hypothesis:brief-render-
    hygiene-after-the-batch-mur): a macro line in an `extras` node or a card
    is DATA, never an expansion directive. Pre-fix the `extras` ref expanded
    the referenced node's body one level."""
    root = _root(tmp_path, parts={"director": ["extras", "card"]},
                 extras={"director": ["doc:wrapper"]})
    _write(root, "nodes/doc/wrapper.md",
           "WRAPPER-SENTINEL\n\n{{template:doc:deeper}}\n")
    out = brief.render(post="some-post", project_root=root)
    assert "WRAPPER-SENTINEL" in out, "the extras node itself still renders"
    assert "{{template:doc:deeper}}" in out, "an extras macro stays literal"
    assert "DEEPER-SENTINEL" not in out, "the macro never expands"
    assert "{{template:doc:inner}}" in out, "a card macro stays literal"


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


def test_successor_command_honours_explicit_project_root(tmp_path, monkeypatch):
    """An explicit prompt-file successor must render from the caller-supplied
    graph root, not the live checkout discovered by brief.py's default."""
    import rotate

    root = _root(tmp_path, parts={"kid": ["head"]})
    prompt_file = _write(root, "successor.md", "SUCCESSOR-BODY-SENTINEL\n")
    seen = {}
    monkeypatch.setattr(
        rotate, "_build_harness_command",
        lambda harness, **kw: (seen.setdefault("prompt", kw["prompt_text"]),
                               ["x"])[1])

    rotate._successor_command(
        name="kid-seat", tier="kid", prompt_file=str(prompt_file),
        model=None, effort=None, settings=None, debug_file="/dev/null",
        harness="pi", project_root=root)

    assert "SUCCESSOR-BODY-SENTINEL" in seen["prompt"]
    assert HEAD_SENTINEL in seen["prompt"]
    assert HEAD_SENTINEL not in brief.successor_prompt(
        tier="kid", body="LIVE-DEFAULT-SENTINEL")


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


# ---- phase 4: the extras override + the doc-card node wins ----------------


def test_extras_text_override_lands_last_and_order_is_the_config_cell(tmp_path):
    """dispatch.py hands `render` the dynamic dispatch brief; the PARTS and
    their ORDER still come from the config cell, never from the caller."""
    root = _root(tmp_path, parts={"kid": ["head", "card", "extras"]})
    out = brief.render(role="kid", extras_text="EXTRAS-SENTINEL",
                       project_root=root)
    assert out.index("EXTRAS-SENTINEL") < out.index("Paid-for path guard")
    assert out.count("Paid-for path guard") == 1
    assert HEAD_SENTINEL in out
    assert out.index(HEAD_SENTINEL) < out.index("EXTRAS-SENTINEL")


def test_a_doc_card_node_wins_over_the_quorum_file(tmp_path):
    """`doc:card-<post>`'s file must win; the quorum file is the fallback."""
    root = _root(tmp_path, parts={"director": ["head", "card"]},
                 card="QUORUM-CARD-SENTINEL\n")
    _write(root, "nodes/doc/card-some-post.md",
           "---\nid: doc:card-some-post\n---\n"
           "# doc:card-some-post\n\nDOC-CARD-SENTINEL\n")
    out = brief.render(post="some-post", project_root=root)
    assert "DOC-CARD-SENTINEL" in out
    assert "QUORUM-CARD-SENTINEL" not in out


def test_assemble_without_head_returns_the_body_only(tmp_path):
    """The `include_head=False` seam dispatch.py uses: the body carries no
    head, so a caller can render head + card itself and pass this as extras."""
    root = _root(tmp_path, parts={})
    segs = brief.assemble(tier="kid", agent_id="a", iter_n=1,
                          include_head=False, project_root=root)
    text = "\n\n".join(segs)
    assert HEAD_SENTINEL not in text
    assert "DO NOT run git" in text


def test_rotate_fallback_reason_reaches_stderr(tmp_path, monkeypatch, capsys):
    """The fallback from `brief.render` to `brief.assemble` is never silent."""
    sys.path.insert(0, str(BIN))
    import rotate

    root = _root(tmp_path, parts={"director": ["head", "card"]})
    _write(root, "nodes/doc/director-brief.md", "D\n")
    # remove the head source so the render refuses by name
    (root / "nodes" / "doc" / "unified-head.md").unlink()
    monkeypatch.setattr(rotate, "_build_harness_command",
                        lambda harness, **kw: ["x"])
    # the fallback body is stubbed: this test is about the STDOUT/STDERR
    # contract, not about assembling against a minimal tmp graph.
    monkeypatch.setattr(brief, "assemble", lambda **kw: ["BODY"])
    rotate._assembled_successor_command(
        name="some-post", tier="director", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi",
        project_root=root)
    err = capsys.readouterr().err
    assert "brief.render" in err and "falling back to brief.assemble" in err


def test_rotate_assemble_fallback_forwards_project_root(tmp_path,
                                                        monkeypatch):
    """The legacy fallback must render the same caller-supplied graph root."""
    import rotate

    def refuse(**kwargs):
        raise brief.RenderError("forced primary-path refusal")

    captured = {}
    monkeypatch.setattr(brief, "render", refuse)
    monkeypatch.setattr(
        brief, "assemble",
        lambda **kwargs: captured.update(kwargs) or ["FALLBACK-BODY-SENTINEL"])
    monkeypatch.setattr(rotate, "_build_harness_command",
                        lambda harness, **kwargs: ["x"])
    root = _root(tmp_path, parts={"kid": []})
    rotate._assembled_successor_command(
        name="kid-seat", tier="kid", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi", project_root=root)
    assert captured["project_root"] == root


# ---- phase 4, items 2+3: the Prime spawn path renders and the card lands once


def _prime_root(tmp_path):
    """A tmp graph root with a prime_director post, its template, its card and
    the town trajectory, so the Prime spawn render can be exercised."""
    root = _root(
        tmp_path,
        parts={"prime_director": ["head", "template", "card", "trajectory"]},
        templates={"prime_director": "doc:director-brief"})
    _write(root, "nodes/doc/director-brief.md", "PRIME-TEMPLATE-SENTINEL\n")
    _write(root, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           '  - {"name": "prime-post", "role": "prime_director", '
           '"harness": "pi"}\n---\n')
    _write(root, "sessions/quorum/prime-post.md", "PRIME-CARD-SENTINEL\n")
    return root


def _capture_prime_body(monkeypatch, root, prompt_file=None, **over):
    sys.path.insert(0, str(BIN))
    import rotate

    seen = {}
    monkeypatch.setattr(
        rotate, "_build_harness_command",
        lambda harness, **kw: (seen.setdefault("prompt", kw["prompt_text"]),
                               ["x"])[1])
    rc, _ = rotate.spawn_window(
        name="prime-post", tier="prime_director", prompt_file=prompt_file,
        dry_run=True, root=root, **over)
    assert rc == 0
    return seen["prompt"]


def test_prime_successor_with_no_prompt_file_renders_once(tmp_path,
                                                         monkeypatch):
    """A Prime successor with NO `--prompt-file` is the SAME assembled render
    every other seat gets: head + the role template + the post's card + the
    town trajectory -- and the card appears EXACTLY ONCE, never once from the
    render and again from a `[handoff-head]` first_turn read."""
    root = _prime_root(tmp_path)
    body = _capture_prime_body(monkeypatch, root)
    # `ultracode` is the keyword first line the prime's ladder row sets; the
    # constitution head follows it and precedes the template, card, trajectory.
    assert brief.render_head(project_root=root) in body
    assert body.index("PRIME-TEMPLATE-SENTINEL") < body.index("PRIME-CARD-SENTINEL")
    assert body.index("PRIME-CARD-SENTINEL") < body.index("TOWN-TRAJECTORY-SENTINEL")
    assert body.count("PRIME-CARD-SENTINEL") == 1


def test_prime_explicit_prompt_file_still_wins(tmp_path, monkeypatch):
    """An EXPLICIT `--prompt-file` beats the render byte-for-byte: the card is
    NOT smuggled in, and the file's body is the one shipped."""
    root = _prime_root(tmp_path)
    pf = _write(root, "explicit-prime.md",
                "EXPLICIT-PRIME-BODY-SENTINEL {name}\n")
    body = _capture_prime_body(monkeypatch, root, prompt_file=str(pf))
    assert "EXPLICIT-PRIME-BODY-SENTINEL prime-post" in body
    assert "PRIME-CARD-SENTINEL" not in body
    assert "PRIME-TEMPLATE-SENTINEL" not in body


def test_config_rotations_first_turn_no_longer_reads_the_card():
    """The Prime's card reaches its first turn through the render alone; no
    `config:rotations` first_turn entry may read `build:HANDOFF.md` (which is a
    symlink to `doc:card-belam`) or the card would land twice. Other first_turn
    entries stay."""
    repo = BIN.parents[2]
    rot = (repo / ".agi" / "nodes" / ".geometry" / "rotations.md").read_text(
        encoding="utf-8")
    assert "build:HANDOFF.md" not in rot
    assert '"label": "rotation-record"' in rot
    assert '"label": "verify"' in rot


# ---- render hygiene (hypothesis:brief-render-hygiene-after-the-batch-mur) --

THOUGHT_BLOCK = (
    "<!-- THOUGHT:BEGIN — authored, not derived. -->\n"
    "THIS-VERSION-REASONING-SENTINEL\n"
    "<!-- THOUGHT:END -->\n")


def test_node_sourced_parts_strip_the_thought_block(tmp_path):
    """Falsifier: a render hands a successor a node's THOUGHT changelog.
    The template, the card node and the trajectory carry only current words."""
    root = _root(tmp_path, parts={"director": ["template", "card", "trajectory"]},
                 templates={"director": "doc:director-brief"})
    _write(root, "nodes/doc/director-brief.md",
           "DIRECTOR-BRIEF-SENTINEL\n\n" + THOUGHT_BLOCK)
    _write(root, "nodes/doc/card-some-post.md", "CARD-SENTINEL\n\n" + THOUGHT_BLOCK)
    _write(root, "nodes/town/t.md", "TOWN-TRAJECTORY-SENTINEL\n\n" + THOUGHT_BLOCK)
    out = brief.render(post="some-post", project_root=root)
    assert "DIRECTOR-BRIEF-SENTINEL" in out
    assert "CARD-SENTINEL" in out
    assert "TOWN-TRAJECTORY-SENTINEL" in out
    assert "THIS-VERSION-REASONING-SENTINEL" not in out
    assert "<!-- THOUGHT:BEGIN" not in out


def test_template_payload_strips_the_thought_block(tmp_path):
    """A build node's template is its PAYLOAD file; the strip follows it."""
    payload = _write(tmp_path, "payload-brief.md",
                     "PAYLOAD-BRIEF-SENTINEL\n\n" + THOUGHT_BLOCK)
    _write(tmp_path, "nodes/build/the-prime-brief.md",
           "---\nid: build:the-prime-brief\npayload_ref: " + str(payload)
           + "\n---\n<!-- BODY:BEGIN -->\n# build:the-prime-brief\n")
    root = _root(tmp_path, parts={"prime_director": ["template"]},
                 templates={"prime_director": "build:the-prime-brief"})
    out = brief.render(role="prime_director", project_root=root)
    assert "PAYLOAD-BRIEF-SENTINEL" in out
    assert "THIS-VERSION-REASONING-SENTINEL" not in out


def test_a_thought_mention_in_prose_is_not_stripped(tmp_path):
    """The strip is the authored REGION, not the bare word: a node line that
    merely names THOUGHT:BEGIN survives (measured live: the director template's
    harvest diagram carries `THOUGHT:BEGIN <= 1 per new node`)."""
    root = _root(tmp_path, parts={"director": ["trajectory"]})
    _write(root, "nodes/town/t.md",
           "TOWN-TRAJECTORY-SENTINEL\n\nTHOUGHT:BEGIN <= 1 per new node\n")
    out = brief.render(post="some-post", project_root=root)
    assert "THOUGHT:BEGIN <= 1 per new node" in out


def test_operating_mode_is_a_config_part_and_off_by_default(tmp_path):
    """Falsifier: render drops the declared operating mode with no way to ask
    for it. It is a `operating_mode` part now; the default lists are unchanged,
    so nothing renders until the config cell names it."""
    root = _root(tmp_path, parts={"director": ["head"]})
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    cfg["operating_modes"] = {"enhanced_survival": {
        "name": "enhanced survival", "seats": "three seats",
        "models": "opus", "source": "goal:g17.1"}}
    cfg["active_operating_mode"] = "enhanced_survival"
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    assert "OPERATING MODE" not in brief.render(post="some-post", project_root=root)
    cfg["brief"]["parts"] = {"director": ["head", "operating_mode"]}
    (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    out = brief.render(post="some-post", project_root=root)
    assert "─── OPERATING MODE (declared in .agi/config.json) ───" in out
    assert "ACTIVE: enhanced survival" in out
    assert "SOURCE: goal:g17.1" in out
