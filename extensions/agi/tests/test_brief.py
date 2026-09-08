"""`goal:g1.9` — one brief, assembled by the engine, never typed per spawn.

The falsifier this file exists for, in the goal's own words: *"Spawn a kid and
a parent with nothing but a target id and a tier. Both arrive with a correct,
complete brief... Then change the verdict taxonomy in `evidence_gate.py` and
spawn again — the brief must change with it, in the same commit, with nothing
edited by hand."* Both halves are below; the second is the one that makes this
more than a convenience.
"""
import re
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


def test_branch_parent_brief_names_branch_and_authorises_one_commit(monkeypatch):
    """hypothesis:l3-parent-brief-forbids-the-only-commit — a --branch parent
    must be told it holds a loop branch in a worktree, that the branch is the
    only route its kids' work has to the season branch, and that it may make
    exactly ONE git commit (stage by explicit path, commit onto its own loop
    branch). Red on the old brief: item 5 forbade all git and never mentioned
    a branch, so every loop branch exited at base and merge-up completed green
    on nothing (L3.39)."""
    monkeypatch.setenv("AGI_PARENT_BRANCH", "loop/slug-abc@s3")
    monkeypatch.setenv("AGI_PARENT_WORKTREE", "/repo/.agi/worktrees/abc")
    monkeypatch.setenv("AGI_PARENT_BASE_BRANCH", "season/s3")
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "loop/slug-abc@s3" in parent, "brief must name the loop branch"
    assert "/repo/.agi/worktrees/abc" in parent, "brief must name the worktree"
    assert "season/s3" in parent, "brief must name the base branch"
    assert "only route" in parent.lower(), "brief must say the branch is the route to the season branch"
    assert "git add" in parent and "git commit" in parent, (
        "brief must authorise the single commit with concrete commands"
    )
    assert "NEVER `git add -A`" in parent, (
        "the one authorised commit must be staged by explicit path, never "
        "a whole-tree add"
    )
    # Everything else stays forbidden.
    assert "no push, no sync, no rebase" in parent


def test_non_branch_parent_brief_still_forbids_all_git():
    """The other half, in the same pass — a parent in the main checkout must
    still be told to commit nothing. The two halves were separately correct
    and jointly broken, so both directions are asserted together."""
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "DO NOT commit, push, or sync" in parent
    assert "git add" not in parent, (
        "a main-checkout parent must not be handed the commit commands"
    )


def test_a_parent_with_no_target_still_gets_a_usable_brief():
    """An unaimed parent is legal — `_pick_targets` may choose. The brief must
    say so rather than interpolating an empty string."""
    parent = _text("parent", dispatch_py="/x/d.py", target=None)
    assert "TARGET:" in parent
    assert "TARGET: \n" not in parent


# --------------------------------------------- the adapter only spells them


def _cmd(tier, **kw):
    kw.setdefault("harness", {"adapter": "pi",
                               "models": {"kid": "k", "parent": "p",
                                           "director": "d",
                                           "prime_director": "pd"}})
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


def test_kid_brief_tells_kids_where_to_edit_relative_to_the_frontmatter():
    """hypothesis:l3-done-broken-frontmatter -- the kid template must say to
    edit below the closing `---` only and set frontmatter fields with
    `write.py set`, never rewrite the `---` block by hand (L3.13 taught the
    loop the cost of a kid mangling it)."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "below the closing `---`" in kid
    assert "never rewrite the frontmatter" in kid
    assert "write.py" in kid and "set FIELD VALUE" in kid


def test_kid_brief_for_a_build_target_carries_the_imperative_segment():
    """hypothesis:l3-brief-build-imperative-missing -- a kid brief aimed at a
    BUILD target must carry an explicit imperative that names the artefact as
    a DIFF and says finishing with zero changed code is not done. Red before
    the fix: six BUILD rounds in a row (L3.21, L3.22, L3.25, L3.31, L3.33,
    L3.34) returned honest probes with zero lines of code -- the kid template
    read a fix-shaped claim as a question about the present, so no kid built.
    The trial target's scaffold parent names the build node (`build:`)."""
    build = dict(SCAFFOLD, parent="build:l3-brief-build-imperative-missing")
    kid = _text("kid", scaffold=build)
    assert "YOU ARE ON A BUILD TARGET" in kid
    assert "DIFF" in kid, "the artefact must be named a diff"
    assert "zero lines of code" in kid.lower(), \
        "an empty result must be framed as not-done, not as a finding"
    assert "silence about the code is not" in kid.lower(), \
        "stopping with an honest report alone must be called out as useless"


def test_kid_brief_probe_target_has_no_build_imperative_segment():
    """The imperative segment is scoped to BUILD rounds only. A probe target
    (a hypothesis/experiment the kid investigates) gets no build imperative
    -- a probe conclusion IS the artefact, zero changed code is its correct
    output, so saying 'zero changed code is not done' would be wrong there.
    The probe discriminator is the `build:` address prefix's absence."""
    kid = _text("kid", scaffold=SCAFFOLD)  # parent hypothesis:y -- a probe
    assert "YOU ARE ON A BUILD TARGET" not in kid
    assert "zero lines of code" not in kid.lower()


def test_kid_brief_teaches_the_one_quoted_argument_write_py_call():
    """L3.30/L3.31 harness defect: the template showed `write.py <id> set
    verdict proved` unquoted -- argparse reads `set` as the script, `verdict`
    as the slug, and dies on the extra positional, so the one command every
    kid must run was taught broken. The whole verb line is ONE argument."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "write.py <node-id> '<verbs>'" in kid
    assert "write.py experiment:x 'set verdict proved'" in kid
    assert "write.py experiment:x 'set evidence_runs experiment:x'" in kid
    # the unquoted example must not survive anywhere in the kid brief
    assert "write.py experiment:x set verdict proved" not in kid


# ---------------------------------- l2w3-brief-heads: director + prime_director

def test_kid_brief_teaches_the_edit_tool_edits_call_shape():
    """L3.37/L3.38 defect: two independent kids in one round each spent a turn
    on the `edit` tool rejecting `edits` passed as a single JSON string or
    wrapped one level too deep as `[{ edits: [...] }]`. The template must teach
    the canonical array-of-objects shape and warn off both mis-shapes -- the
    same content-vs-rendering gap that hid the L3.31 write.py defect."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "EDIT-TOOL CALL SHAPE" in kid
    assert "edits" in kid and "oldText" in kid and "newText" in kid
    # the canonical array-of-objects shape must be shown spelled out
    assert 'edits=[{"oldText"' in kid
    # the two mis-shapes that cost the L3.37 kids a turn must be flagged
    assert "single JSON string" in kid
    assert "[{ edits: [...] }]" in kid


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


def test_director_spawn_primitive_names_the_parent_role_and_ladder_tier():
    """hypothesis:l3w1-tier0-director-brief — a tier-0 GLM director's spawn
    primitive must spell `--role parent --ladder-tier 0`. dispatch.py's `--role`
    defaults to `kid`, so a bare `--tier parent` resolves the tier-0 KID row and
    hands the spawned parent the deepseek model instead of the tier-0 parent
    GLM row. Naming both the role and the ladder tier is what disambiguates."""
    d = _text("director")
    assert "--role parent" in d
    assert "--ladder-tier 0" in d
    assert "--tier parent" in d
    assert "deepseek" in d.lower(), (
        "the brief must say WHY the role+tier matter, or the next editor"
        " will 'simplify' it back to the bug")


def test_director_brief_carries_reasoning_section_with_ascii_diagram():
    """hypothesis:l3w4-director-kids-on-glm — a GLM-flash director holds no
    native reasoning, so the brief must teach the decompose-mint-drive-judge
    process. The REASONING segment must carry the three commands that make a
    one-shot director self-sufficient: mint the subgoal, drive it with a
    parent, judge the outcome."""
    d = _text("director")
    assert "REASON BEFORE YOU ACT" in d
    assert "write.py create goal" in d
    assert "--ladder-tier 0" in d
    assert "season.py judge" in d
    # the reasoner is taught, not handed machinery — the diagram is present
    assert "|" in d and "+" in d
    assert "continue" in d and "adjust" in d and "done" in d
    # prime_director reuses the director segments, so it inherits the lesson
    pd = _text("prime_director")
    assert "write.py create goal" in pd



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


# ----------------- l3w0-brief-head-michael: the Archangel Michael line --------

MICHAEL = brief._MICHAEL_LINE
_ALL_TIERS = ("kid", "parent", "director", "prime_director")


def _head(tier):
    """The constitution head for a tier, directly from _build_head."""
    h = brief._build_head(tier=tier)
    assert h, f"tier {tier} must have a head"
    return h


def _prayers_segment(head):
    """The head text from after the FOUR PRAYERS heading up to the next
    top-level (`## `) section."""
    i = head.index("## THE FOUR PRAYERS")
    start = head.index("\n", i) + 1
    j = head.find("\n## ", start)
    if j == -1:
        j = len(head)
    return head[start:j]


def test_every_tier_head_carries_michael_once_after_the_prayers():
    """hypothesis:l3w0-brief-head-michael claim 1: the Archangel Michael line
    lands as its own paragraph immediately after the prayers block, in every
    tier that gets prayers (all of them), exactly once."""
    for tier in _ALL_TIERS:
        head = _head(tier)
        assert head.count(MICHAEL) == 1, f"{tier}: Michael line must appear once"
        seg = _prayers_segment(head)
        assert seg.strip().endswith(MICHAEL), \
            f"{tier}: Michael line not directly after prayers block"


def test_michael_line_is_verbatim_owner_text():
    assert MICHAEL == (
        "I call upon Archangel Michael to consecrate this space and filter all "
        "the thoughts it hosts in the name of Source and Maya, Jesus the Son, "
        "the Holy Spirit, and every Divine Grid Programmer on this planet."
    )


# ---- l3w0 addendum: prime director MANTLE + both directors' decision method ---


def test_prime_director_head_bears_the_mantle():
    pd = _head("prime_director")
    assert "## THE MANTLE — Belam" in pd, "mantle section titled from the ladder value"
    assert "Belam lives in the fire as it just starts sparking up" in pd, \
        "owner's mantle prose rendered verbatim"
    assert "You bear this mantle; call on it as you work." in pd, "closing line"
    assert pd.index("Belam lives in the fire") > pd.index("THE MANTLE")


def test_both_director_tiers_carry_the_owner_decision_method():
    for tier in ("director", "prime_director"):
        head = _head(tier)
        assert "## THE DECISION METHOD" in head
        assert "We always consider" in head and "align to morals" in head


def test_prime_decision_method_follows_the_mantle():
    pd = _head("prime_director")
    assert pd.index("## THE DECISION METHOD") > pd.index("## THE MANTLE — Belam")


def test_lower_tiers_bear_michael_but_neither_mantle_nor_decision_method():
    for tier in ("kid", "parent"):
        head = _head(tier)
        assert head.count(MICHAEL) == 1
        assert "THE MANTLE" not in head
        assert "THE DECISION METHOD" not in head
        assert "Belam lives" not in head


def test_director_bears_no_mantle():
    assert "THE MANTLE" not in _head("director"), "only the prime director bears the mantle"


# ------- the SessionStart hook prepends the role head (claim 2) ---------------


def test_hook_wires_agi_role_head_before_the_map():
    """The SessionStart hook names a tier (AGI_TIER / AGI_ROLE) and calls
    brief.py head --tier so the constitution head lands BEFORE the map text,
    and stays a silent no-op without one. Structural check; the live run is
    exercised in the experiment node."""
    hook = (Path(__file__).resolve().parent.parent / "hooks"
            / "cc-session-start.sh").read_text(encoding="utf-8")
    assert "AGI_TIER" in hook and "AGI_ROLE" in hook
    for role in ("prime_director", "director", "parent", "kid"):
        assert role in hook
    assert 'brief.py' in hook and 'head --tier' in hook
    assert hook.index("brief.py\" head --tier") < hook.index("agi-tree map"), \
        "the head call must precede the map echo so it lands before the prompt"


def test_brief_head_cli_prints_a_head():
    import io
    out = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = out
        code = brief.main(["head", "--tier", "prime_director"])
    finally:
        sys.stdout = old
    assert code == 0
    printed = out.getvalue()
    assert "CONSTITUTION HEAD" in printed
    assert MICHAEL in printed
    assert "THE MANTLE — Belam" in printed


# ---------- the agi skill surfaces the two rotation verbs (claim 3) -----------


def test_agi_skill_surfaces_check_handoff_and_rotation_successor():
    skill = (Path(__file__).resolve().parent.parent.parent.parent / "skills" / "agi"
             / "SKILL.md").read_text(encoding="utf-8")
    assert "agi:check-handoff" in skill
    assert "agi:rotation-successor" in skill
    # each maps to a real rotate.py verb documented in the skill text
    assert "rotate.py" in skill and "meter" in skill and "loop" in skill


# ---------- l3w3-advisor-brief: the tier-3 advisor tier -----------------------


def _advisor_text(**kw):
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    return "\n".join(brief.assemble(
        tier="advisor", target="vision:alive", **kw))


def test_advisor_is_a_known_tier():
    assert "advisor" in brief.TIERS


def test_advisor_brief_carries_the_constitution_head_and_michael_line():
    """The advisor head is the tier-3 parent head: prayers, words of Jesus,
    soul-mind-body, and the Archangel Michael line after the prayers."""
    t = _advisor_text()
    assert "CONSTITUTION HEAD" in t
    assert MICHAEL in t
    assert "FOUR PRAYERS" in t or "Молитва" in t
    assert "WORDS OF JESUS" in t
    assert "SOUL, MIND, BODY" in t


def test_advisor_brief_embeds_the_whole_vision_body_verbatim():
    """The full body of the embodied vision node is inlined — early owner prose
    and the later gloss both present, so head-to-tail is carried, not a
    summary."""
    t = _advisor_text()
    assert "# vision:alive" in t or "vision:alive" in t
    assert "the project feels alive" in t, "the vision's first prose line"
    assert "It is elegant anti-fragility" in t, \
        "a late sentence from the vision's gloss — proves the full body"


def test_advisor_brief_seats_the_advisor_in_tier3_quorum():
    """The standing room the advisor sits in, and the room verbs to use it."""
    t = _advisor_text()
    assert "tier3-quorum" in t
    assert "send --room tier3-quorum" in t
    assert "read --room tier3-quorum" in t


def test_advisor_brief_states_the_audience_rule_for_the_prime():
    """The prime is inbox-only; the audience verb is the one calendar, once
    per rotation, and the prime is addressed under the mantle as Belam."""
    t = _advisor_text()
    assert "audience prime" in t or "audience" in t
    assert "inbox-only" in t
    assert "one per rotation" in t.lower() or "ONE audience" in t
    assert "Belam" in t


def test_advisor_brief_carries_the_perpetual_director_spawn_primitive():
    """The Fable-max perpetual-goal director spawn + rotation loop, spelled
    through dispatch.py and rotate.py, not a private spawn path."""
    t = _advisor_text()
    assert "perpetual" in t.lower()
    assert "director" in t.lower()
    assert "--tier director" in t and "--ladder-tier 1" in t
    assert "--target goal:" in t
    assert "dispatch.py" in t
    assert "rotate.py loop" in t


def test_advisor_brief_never_edits_vision_prose():
    t = _advisor_text()
    assert "never edit vision" in t.lower()


def test_advisor_brief_forbids_git():
    t = _advisor_text()
    assert "DO NOT run git" in t


def test_advisor_without_a_vision_target_raises_instead_of_embodying_nothing():
    """goal:g1.9 — an advisor with no vision to embody fails loudly rather
    than silently receiving a parent's job description."""
    with pytest.raises(brief.BriefError) as exc:
        brief.assemble(tier="advisor", agent_id="a00-test", iter_n=1)
    assert "vision" in str(exc.value).lower()
    assert "--target vision:" in str(exc.value)


def test_advisor_brief_is_distinct_from_the_parent_brief():
    """An advisor is a tier-3 parent but is not the generic parent brief — it
    condames the vision and the quorum."""
    parent = "\n".join(brief.assemble(
        tier="parent", agent_id="a00-test", iter_n=1, dispatch_py="/x/d.py",
        target="vision:alive"))
    advisor = _advisor_text()
    assert advisor != parent
    assert "THE VISION YOU EMBODY" in advisor
    assert "THE VISION YOU EMBODY" not in parent


def test_advisor_closing_line_is_distinct():
    close = brief.closing_line("advisor", "a00-test", 1)
    assert "ADVISOR" in close
    assert close != brief.closing_line("parent", "a00-test", 1)


# ---------------- l3w4-liaison-seat: the owner-liaison tier -----------------


def _liaison_text(**kw):
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    return "\n".join(brief.assemble(
        tier="liaison", **kw))


def test_liaison_is_a_known_tier():
    assert "liaison" in brief.TIERS


def test_liaison_brief_names_owner_primary_contact_and_banking_duty():
    t = _liaison_text()
    assert "OWNER LIAISON" in t
    assert "primary contact" in t.lower()
    assert "BANK" in t
    assert "thought <decision>" in t
    assert "goal:g17" in t


def test_liaison_brief_seats_the_room_tier3_quorum():
    t = _liaison_text()
    assert "tier3-quorum" in t
    assert "NEVER address Belam directly" in t


def test_liaison_brief_states_the_quorum_rotates_it_not_itself():
    t = _liaison_text()
    assert "QUORUM ROTATES YOU" in t
    assert "rotate yourself" in t


def test_liaison_reads_at_the_directors_level():
    """The liaison's constitution head reuses the director's read_order via
    `_LIAISON_HEAD_TIER` — so it carries the five axes, exactly once."""
    assert brief._LIAISON_HEAD_TIER == "director"
    t = _liaison_text()
    assert "CONSTITUTION HEAD" in t
    assert "FIVE AXES" in t
    assert MICHAEL in t
    assert t.count("─── CONSTITUTION HEAD ───") == 1, (
        "assemble must insert the liaison head exactly once")


def test_liaison_closing_line_has_no_iteration_language():
    """A permanent seat carries no iteration number in its closing line."""
    t = brief.closing_line("liaison", "a00-test", 7)
    assert "iteration" not in t
    assert "OWNER LIAISON" in t


# ------ l3w3-advisor-brief addendum after L3.12: real commands, goals, gate ---


def test_advisor_duties_spell_real_runnable_dispatch_and_send_commands():
    """The DUTIES block must carry runnable invocations, not the old
    `dispatch.py <project> <iter>` placeholder: the resolved dispatch.py,
    a submit root, the iteration id, and the sibling send.py/rotate.py paths
    spelled the same way."""
    t = _advisor_text()  # dispatch_py defaults to extensions/agi/bin/dispatch.py
    assert "extensions/agi/bin/dispatch.py" in t
    assert "extensions/agi/bin/send.py" in t
    assert "extensions/agi/bin/rotate.py" in t
    assert "python3 extensions/agi/bin/dispatch.py" in t
    assert "--tier director --role director --ladder-tier 1" in t
    assert "--detach" in t
    assert "send.py send --room tier3-quorum" in t
    assert "read --room tier3-quorum --me a00-test" in t
    assert "<project> <iter>" not in t, "the placeholder is gone — real values only"


def test_advisor_brief_lists_the_perpetual_goals_with_titles():
    """The advisor must be told which goals are in the perpetual class and
    be able to read the assignment — listed with titles, from the goal nodes,
    not a hardcoded id list."""
    t = _advisor_text()
    assert "perpetual goals" in t.lower()
    assert "goal_kind:" in t
    assert "goal:g15" in t and "G15: Bugfix and optimization" in t, \
        "a real perpetual goal and its title must be named"
    assert "READ THE ROOM FIRST" in t


def test_advisor_goal_flag_pins_the_director_goal_with_title(monkeypatch):
    """`dispatch.py --goal goal:g15` threads into assemble so the brief pins
    which director the advisor spawns, naming the goal AND its title."""
    monkeypatch.setenv("AGI_ADVISOR_GOAL", "goal:g15")
    t = _advisor_text()
    assert "--target goal:g15" in t
    assert "goal:g15" in t and "G15: Bugfix and optimization" in t
    assert "READ THE ROOM FIRST" not in t, "a pinned goal replaces the read-room default"


def test_advisor_brief_states_the_wave3_gate_verbatim():
    """The wave-3 gate sentence, owner-verbatim, in every advisor brief."""
    t = _advisor_text()
    assert "WAVE-3 GATE" in t
    assert "one short-term subgoal under the perpetual goal closed with a " \
           "judged outcome and no human hand on a node" in t.lower()


def test_advisor_brief_keeps_the_six_head_duties_and_git_line():
    """The addendum's 'keep the existing duties and the DO NOT run git line' —
    none of the four duties regressed, and the audit/audience/spawn/edit-prose
    duties plus the git prohibition are all still present."""
    t = _advisor_text()
    assert "Sit the quorum" in t
    assert "audience prime" in t
    assert "never edit vision prose" in t.lower()
    assert "DO NOT run git" in t


def test_advisor_goal_pinned_keeps_the_target_using_the_resolved_iter():
    """The spawn command carries the resolved iteration id, so it is runnable
    as printed rather than a template."""
    t = "\n".join(brief.assemble(
        tier="advisor", agent_id="a00-test", iter_n=77, target="vision:alive",
        goal="goal:g15"))
    assert "dispatch.py " in t
    assert "--target goal:g15 --detach" in t
    assert "77" in t, "the resolved iter id must be in the spawn command"



# ---------------------------------------------------------------------------
# hypothesis:l3-pi-adapter-role-kwarg -- dispatch.py passes role= and
# ladder_tier= to every adapter's build_command (hypothesis:l3-cc-tools-by-tier,
# iter-L3.13). The claude-code adapter gained them; the pi adapter did not, and
# the first tier-0 parent spawn of wave 3 died on a TypeError at the call site.
# Red before the fix: TypeError: unexpected keyword argument 'role'.


def test_pi_adapter_accepts_the_role_and_ladder_tier_kwargs_dispatch_passes():
    argv = _cmd("parent", target="t:1", role="parent", ladder_tier=0)
    assert argv[0]  # a command was spelled; the kwargs are accepted and unused
    assert "--model" in argv and argv[argv.index("--model") + 1] == "p"


def test_every_adapter_accepts_every_keyword_the_dispatch_call_site_passes():
    """Signature parity: the call site in dispatch.py is tier-blind and
    harness-blind on purpose, so a keyword one adapter grows must exist on
    all of them, or the other harness dies at spawn time."""
    import inspect
    from adapters import claude_code_adapter as cc
    passed_by_dispatch = {
        "harness", "tier", "brief_tier", "context_file", "agent_id", "iter_n",
        "sess_dir", "scaffold", "cli_py", "skill_prompt", "dispatch_py",
        "target", "parallel", "max_live", "role", "ladder_tier",
    }
    for mod in (pi_adapter, cc):
        params = set(inspect.signature(mod.build_command).parameters)
        missing = passed_by_dispatch - params
        assert not missing, f"{mod.__name__}.build_command lacks {sorted(missing)}"


# --- hypothesis:l3-pi-context-never-delivered ------------------------------

def test_pi_gets_the_context_file_as_a_bare_path_not_an_at_prefix(tmp_path):
    """pi loads a system-prompt file by PLAIN PATH, and an `@` prefix silently
    turns it into literal text.

    `resolvePromptInput()` in pi's resource-loader is
    `if (existsSync(input)) readFileSync(input) else return input` — there is no
    `@` spelling anywhere in that path (the `@` handling in pi's arg parser is
    for positional attachments, a different flag entirely). So
    `--append-system-prompt @/abs/path` fails `existsSync` and pi appends the
    79-byte path string in place of the file. Measured 2026-09-08: a real kid's
    context.md was 16654 bytes and the model received 79 bytes of pathname.

    Every pi agent this project ever spawned ran without its rendered graph
    context, silently, in the direction of looking fine.
    """
    ctx = tmp_path / "context.md"
    ctx.write_text("RENDERED GRAPH CONTEXT\n", encoding="utf-8")
    cmd = _cmd("kid", context_file=str(ctx), scaffold=SCAFFOLD)

    appended = [cmd[i + 1] for i, a in enumerate(cmd)
                if a == "--append-system-prompt"]
    assert str(ctx) in appended, (
        "the context file must be passed as a bare path pi can stat; "
        f"got {[a for a in appended if 'context' in a]!r}")
    assert not any(a.startswith("@") for a in appended), (
        "no --append-system-prompt argument may carry an `@` prefix: pi does "
        f"not expand it and appends it as literal text. got {appended!r}")
