"""`goal:g1.9` — one brief, assembled by the engine, never typed per spawn.

The falsifier this file exists for, in the goal's own words: *"Spawn a kid and
a parent with nothing but a target id and a tier. Both arrive with a correct,
complete brief... Then change the verdict taxonomy in `evidence_gate.py` and
spawn again — the brief must change with it, in the same commit, with nothing
edited by hand."* Both halves are below; the second is the one that makes this
more than a convenience.
"""
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN / "adapters"))

import brief            # noqa: E402
import evidence_gate    # noqa: E402
import pi_adapter       # noqa: E402

SCAFFOLD = {
    "path": "/tmp/n.md",
    "node_type": "experiment",
    "node_id": "experiment:x",
    "parent": "hypothesis:y",
}


def _text(tier, **kw):
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    kw.setdefault("cli_py", "/x/cli.py")
    return "\n".join(brief.assemble(tier=tier, **kw))


def test_parent_and_kid_get_different_briefs():
    """The defect this module was written for: `dispatch.py --tier parent`
    selected the parent model correctly and then handed it the kid brief, so a
    parent wrote one node and stopped while looking like it ran a loop."""
    kid = _text("kid", scaffold=SCAFFOLD)
    parent = _text("parent", dispatch_py="/x/dispatch.py", target="hypothesis:y")

    assert "fill in the scaffolded node file" in kid.lower()
    assert "fill in the scaffolded node file" not in parent.lower()
    assert "--tier kid" in parent, "a parent must be told how to spawn"
    assert "--tier kid" not in kid


def test_an_unknown_tier_raises_instead_of_defaulting():
    """Defaulting is the bug. A tier with no brief must fail loudly rather
    than silently receive another tier's job description."""
    with pytest.raises(brief.BriefError) as exc:
        brief.assemble(tier="delegator", agent_id="a", iter_n=1)
    assert "delegator" in str(exc.value)
    assert "kid" in str(exc.value) and "parent" in str(exc.value)


def test_verdict_taxonomy_is_derived_not_retyped(monkeypatch):
    """g1.9's falsifier, second half. Change the taxonomy where the gate
    defines it; every brief must change in the same commit.

    A brief that restates a rule enforced elsewhere is a hand-maintained copy
    of a contract. This project lost a kid's verdict to exactly that drift —
    `goal:s8` shipped kids a completion contract belonging to the other
    runtime, and a bare `:N` was read as `0.6`.
    """
    sentinel = "TAXONOMY-SENTINEL-9f3a"
    monkeypatch.setattr(evidence_gate, "VERDICT_HELP", sentinel)

    assert sentinel in _text("kid", scaffold=SCAFFOLD)
    assert sentinel in _text("kid", scaffold=None)
    assert sentinel in _text("parent", dispatch_py="/x/d.py", target="t:1")


def test_parent_brief_carries_the_grandchild_bound():
    """`spawn.parallel` does NOT bound grandchildren
    (`experiment:a00-763e629b-5c04ad`), so a parent's own spawns are an
    unbounded population unless the parent applies the limit again.

    Asserted here because the brief is where it is currently stated. It is
    NOT sufficient — `goal:g4.8` owns enforcing it at the spawn site, since a
    bound that lives only in a brief is one a parent can ignore.
    """
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1", parallel=3)
    assert "3" in parent
    assert "does not bound" in parent.lower()


def test_parent_brief_forbids_committing_and_bypassing():
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "--no-evidence-gate" in parent
    assert "commit" in parent.lower()


def test_a_parent_with_no_target_still_gets_a_usable_brief():
    """An unaimed parent is legal — `_pick_targets` may choose. The brief must
    say so rather than interpolating an empty string."""
    parent = _text("parent", dispatch_py="/x/d.py", target=None)
    assert "TARGET:" in parent
    assert "TARGET: \n" not in parent


# --------------------------------------------- the adapter only spells them


def _cmd(tier, **kw):
    kw.setdefault("harness", {"adapter": "pi", "models": {"kid": "k", "parent": "p"}})
    kw.setdefault("context_file", "/tmp/ctx.md")
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    kw.setdefault("sess_dir", Path("/tmp"))
    kw.setdefault("cli_py", "/x/cli.py")
    return pi_adapter.build_command(tier=tier, **kw)


def test_adapter_selects_the_tier_model_and_the_tier_brief():
    """Both halves of the tiering, in one assertion, because they were
    separately correct and jointly broken: the model was already per-tier and
    the brief was not."""
    kid, parent = _cmd("kid", scaffold=SCAFFOLD), _cmd("parent", target="t:1")
    assert kid[kid.index("--model") + 1] == "k"
    assert parent[parent.index("--model") + 1] == "p"
    assert "signal done" in kid[-1]
    assert "spawn and review kids" in parent[-1]


def test_the_adapter_holds_no_brief_text_of_its_own():
    """`goal:g4.6` — an adapter owns the argv and the environment, nothing
    else. If brief prose reappears in an adapter, the seam has moved back and
    a second harness will grow its own copy of it."""
    src = (BIN / "adapters" / "pi_adapter.py").read_text()
    for phrase in ("fill in the scaffolded", "Your job:", "--tier kid",
                   "Begin iteration"):
        assert phrase not in src, f"brief content leaked back into the adapter: {phrase!r}"


# ---------------------------------- goal:s27 — a parent's artefact is its kids


def test_parent_signals_done_with_owns_not_node_id():
    """The owner's reframing: a parent is not nodeless, it is responsible for
    its children's nodes. So its completion is theirs, propagated."""
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "--owns" in parent
    assert "--node-id" not in parent.replace("`--owns`, NOT `--node-id`", "")


def test_parent_brief_sends_review_prose_to_the_kids_thought_block():
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "THOUGHT:BEGIN" in parent
    assert "never append" in parent.lower()
    assert "absent means empty" in parent.lower()


def test_parent_brief_names_the_thought_stopgap_as_temporary():
    """Recorded in the brief on purpose, so the compression is not mistaken
    for the design: session linking is where a full review belongs."""
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "goal:g2.7" in parent and "goal:g10.1" in parent
    assert "stopgap" in parent.lower()


def test_kid_brief_is_untouched_by_the_parent_artefact_change():
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "--owns" not in kid
    assert "--node-id experiment:x" in kid
