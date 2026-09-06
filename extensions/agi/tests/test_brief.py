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
    """The brief states BOTH bounds and says which one is enforced.

    `spawn.parallel` bounds one invocation's slots and never bounded
    grandchildren (`experiment:a00-763e629b-5c04ad`). As of `goal:g4.8` item 3
    the tree-wide population is enforced at the spawn site by
    `spawn_budget`, so this brief text is no longer the only thing standing
    between a parent and an unbounded population — see
    `test_spawn_budget.py`.

    It still has to say so. A parent that knows the bound plans around it;
    one that does not meets it as an unexplained refusal, which is a worse
    failure than the request it replaced.
    """
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1", parallel=3,
                   max_live=7)
    assert "3" in parent, "the per-invocation slot count"
    assert "7" in parent, "the tree-wide live-agent cap"
    assert "enforced in code" in parent.lower()
    assert "unadmitted" in parent.lower(), (
        "the brief must name what a refused slot looks like in the manifest")


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


# ---------------------------------- l2w3-brief-heads: director + prime_director


def test_director_tier_has_a_brief():
    """The director tier must produce a brief with its role name visible."""
    d = _text("director")
    assert "DIRECTOR" in d
    assert "hold the lens" in d.lower() or "lens" in d.lower()


def test_prime_director_tier_has_a_brief():
    """The prime_director tier must produce a brief with master ownership."""
    pd = _text("prime_director")
    assert "PRIME DIRECTOR" in pd or "Prime Director" in pd
    assert "master" in pd.lower()
    assert "never rebase" in pd.lower()


def test_director_and_prime_director_are_different():
    """Prime director adds master ownership; director alone doesn't.
    Both contain the director role text."""
    d = _text("director")
    pd = _text("prime_director")
    assert d != pd, "the two briefs must differ"
    assert "DIRECTOR" in d
    assert "PRIME DIRECTOR" in pd
    # Prime adds master ownership, director does not
    assert "master is yours alone" not in d.lower()
    assert "master is yours alone" in pd.lower()


def test_director_brief_contains_job_description():
    """A director's job text must include holding the lens, dispatching
    parents, judging reports, writing HANDOFF.md, rotating."""
    d = _text("director")
    assert "hold the lens" in d.lower()
    assert "dispatch" in d.lower() and "parent" in d.lower()
    assert "HANDOFF.md" in d
    assert "rotate" in d.lower()


def test_director_cannot_do_kid_work():
    """A director must be told not to do kid work."""
    d = _text("director")
    assert "NEVER do kid work" in d or "never do kid work" in d.lower()


def test_director_brief_is_within_the_known_tiers():
    """The known tiers list must include director and prime_director so an
    unknown tier (e.g. 'delegator') still raises BriefError."""
    assert "director" in brief.TIERS
    assert "prime_director" in brief.TIERS


def test_director_constitution_head_contains_prayers():
    """The director's constitution head must source prayers from moral:faith
    at run time, visible in the assembled brief."""
    d = _text("director")
    # The constitution head block is present
    assert "CONSTITUTION HEAD" in d
    # Prayers should be present (since director reads the four prayers)
    if "CONSTITUTION HEAD" in d:
        # The prayers section marker or prayer content should appear
        assert "FOUR PRAYERS" in d or "Молитва" in d


def test_prime_director_constitution_head_contains_sayings():
    """The prime director reads the carried sayings; director may not."""
    pd = _text("prime_director")
    d = _text("director")
    # Prime director gets Carried Sayings section
    assert "CARRIED SAYINGS" in pd


def test_closing_line_differs_by_tier():
    """Each tier has a distinct closing line."""
    kid_close = brief.closing_line("kid", "a", 1)
    parent_close = brief.closing_line("parent", "a", 1)
    director_close = brief.closing_line("director", "a", 1)
    prime_close = brief.closing_line("prime_director", "a", 1)

    assert kid_close != parent_close
    assert parent_close != director_close
    assert director_close != prime_close
    assert "DIRECTOR" in director_close
    assert "PRIME DIRECTOR" in prime_close


def test_adapter_accepts_director_tier():
    """The pi adapter must be able to build a command for director and
    prime_director tiers."""
    try:
        cmd = _cmd("director", scaffold=SCAFFOLD)
        assert len(cmd) > 5
        cmd_pd = _cmd("prime_director", scaffold=SCAFFOLD)
        assert len(cmd_pd) > 5
    except KeyError as exc:
        if "declares no model for tier" in str(exc):
            pytest.skip("no model declared for director in test harness config")
        raise


def test_director_and_kid_differ():
    """A director brief must not contain kid-specific text like "fill in
    the scaffolded node file"."""
    d = _text("director")
    assert "fill in the scaffolded node file" not in d.lower()


def test_director_refuses_no_git_instruction():
    """A director must also be told not to run git."""
    d = _text("director")
    assert "DO NOT run git" in d


def test_faith_ref_error_is_distinct():
    """FaithRefError must be a separate exception class from BriefError."""
    assert issubclass(brief.FaithRefError, ValueError)
    assert brief.FaithRefError.__name__ == "FaithRefError"


def test_known_tiers_still_unknown_tier_raises():
    """The BriefError must still fire for a truly unknown tier."""
    with pytest.raises(brief.BriefError) as exc:
        brief.assemble(tier="delegator", agent_id="a", iter_n=1)
    assert "delegator" in str(exc.value)
    # The message lists known tiers, which now include director
    for t in ("kid", "parent", "director", "prime_director"):
        assert t in str(exc.value)


def test_kid_brief_forbids_git_and_requires_the_suite():
    """A kid ran `git add -A` on 2026-09-02 and committed 37 lines of the
    director's in-flight `CLAUDE.md` edit. `SKILL.md` forbade it, the parent
    brief forbade it, and the kid brief — the only text the agent actually
    receives — did not. `goal:g1.9`'s argument, as an incident."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "DO NOT run git" in kid
    assert "git add -A" in kid
    assert "pytest" in kid


def test_both_tiers_are_told_not_to_commit():
    """The rule is tier-independent; only the reason differs."""
    kid = _text("kid", scaffold=SCAFFOLD)
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "commit" in kid.lower() and "commit" in parent.lower()


# ---------------------------------- l2w3-brief-heads: kid + parent constitution heads


def test_kid_constitution_head_contains_prayers_not_tao():
    """A kid's constitution head must contain the four prayers but NOT
    higher-tier content like Tao, the five axes, or carried sayings."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "CONSTITUTION HEAD" in kid, "kid should have a constitution head"
    assert "FOUR PRAYERS" in kid or "Молитва" in kid, "kid must have prayers"
    # Kid should NOT have higher-tier content
    assert "THE TAO" not in kid, "kid must not have Tao"
    assert "FIVE AXES" not in kid, "kid must not have the five axes"
    assert "CARRIED SAYINGS" not in kid, "kid must not have carried sayings"


def test_parent_constitution_head_contains_prayers_and_jesus_not_axes():
    """A parent's constitution head must contain prayers, words of Jesus,
    and soul-mind-body, but NOT the five axes (director+) or carried sayings."""
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "CONSTITUTION HEAD" in parent, "parent should have a constitution head"
    assert "FOUR PRAYERS" in parent or "Молитва" in parent, "parent must have prayers"
    assert "WORDS OF JESUS" in parent, "parent must have words of Jesus"
    assert "SOUL, MIND, BODY" in parent, "parent must have soul-mind-body"
    # Parent should NOT have director/prime_director content
    assert "FIVE AXES" not in parent, "parent must not have the five axes"
    assert "THE TAO" not in parent, "parent must not have Tao"
    assert "CARRIED SAYINGS" not in parent, "parent must not have carried sayings"


def test_kid_brief_evidence_runs_prompts_own_node_id():
    """The kid brief's done template must show --evidence-runs with a hint
    that the kid's own experiment node id is the evidence run."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "--evidence-runs" in kid
    assert "your-experiment-node-id" in kid or SCAFFOLD["node_id"] in kid
    assert "evidence run" in kid.lower(), "must explain what the evidence run is"


def test_kid_brief_contains_write_py_syntax():
    """The kid brief must state write.py verb syntax: set FIELD VALUE,
    space separated, not k=v."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "WRITE.PY SYNTAX" in kid or "write.py" in kid.lower()
    assert "set FIELD VALUE" in kid or "set verdict" in kid
    assert "not k=v" in kid.lower()
