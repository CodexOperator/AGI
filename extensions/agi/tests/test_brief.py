"""`goal:g1.9` — one brief, assembled by the engine, never typed per spawn.

The falsifier this file exists for, in the goal's own words: *"Spawn a kid and
a parent with nothing but a target id and a tier. Both arrive with a correct,
complete brief... Then change the verdict taxonomy in `evidence_gate.py` and
spawn again — the brief must change with it, in the same commit, with nothing
edited by hand."* Both halves are below; the second is the one that makes this
more than a convenience.
"""
import json
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


def test_parent_brief_tells_it_to_iterate_continue_adjust_done():
    """hypothesis:l3-parent-never-told-to-iterate — the brief's own defect
    was that it named a loop and described a straight line: every measured
    parent spawned exactly one kid and exited (8/8 then 10/10) because nothing
    told it it could keep going. The ITERATION CONTRACT must hand the parent
    the continue/adjust/done judgement (the SAME words the director block
    already uses, not new ones), a hard per-dispatch kid ceiling, and the
    rule that the next kid's brief carries what the last kid produced. The
    ceiling is the refused-condition defence: an unbounded iterating parent is
    the first thing able to multiply agents without a human in the loop, so
    the number must be visible and small, and "done" must be the default when
    the parent is unsure.
    """
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1",
                   max_live=25, kid_ceiling=3)
    # The three judgements, in the mode's own vocabulary.
    assert "continue" in parent and "adjust" in parent and "done" in parent
    # The ceiling is visible and respected as a bound, not the whole capacity.
    assert "AT MOST 3 KIDS TOTAL" in parent
    assert "25 KIDS" not in parent, ("ceiling must not be silently the whole "
                                      "tree's max_live")
    # The carry-forward rule, so the second kid is not a blind rerun.
    assert "carry what the last kid" in parent.lower() or (
        "carry what the last kid" in parent)
    # Done is the default when unsure — the money-leak guard.
    assert "DONE, not continue" in parent
    # Fan-out and per-kid branches are available but not forced.
    assert "FAN-OUT AND BRANCHES" in parent
    assert "--branch" in parent


def test_parent_brief_defaults_the_kid_ceiling_to_a_small_bound():
    """A caller that does not thread kid_ceiling (e.g. a hand assemble, or a
    restart path) must still get a bounded, visible ceiling — deliberately
    small, never the tree's whole capacity, so an uninstrumented parent plans
    against a number rather than discovering an unbounded loop.
    """
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1",
                   max_live=25)
    assert "AT MOST 4 KIDS TOTAL" in parent
    assert "25 KIDS" not in parent


def test_kid_brief_carries_no_iteration_contract():
    """The ITERATION CONTRACT is parent-tier-only: a kid must not be handed
    continue/adjust/done or a spawn ceiling, or it will copy the loop
    vocabulary into child work it spawns nothing for.
    """
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "HARD CEILING" not in kid
    assert "FAN-OUT AND BRANCHES" not in kid


def test_kid_addendum_lands_as_a_labelled_segment_and_names_the_flag():
    """hypothesis:l3-parent-never-told-to-iterate, carry-forward axis (SD.12)
    -- the per-kid brief channel. THREADING addendum through assemble must
    grow the kid brief by EXACTLY one segment, labelled so a kid can tell
    inherited result from its own assignment, and containing the parent's
    text verbatim. The brief must also be clear this is inherited context,
    not the assignment.
    """
    result = "KID1 disproved hypothesis:x\nsecond line with && and \"quotes\""
    base = brief.assemble(tier="kid", agent_id="a00-t", iter_n=1,
                          scaffold=SCAFFOLD)
    grown = brief.assemble(tier="kid", agent_id="a00-t", iter_n=1,
                           scaffold=SCAFFOLD, addendum=result)
    # Nothing was dropped, nothing retyped -- the channel adds, it does not edit.
    for s in base:
        assert s in grown
    new = [s for s in grown if s not in base]
    assert len(new) == 1, f"expected exactly one added segment, got {len(new)}"
    seg = new[0]
    assert "WHAT THE LAST KID PRODUCED" in seg
    assert "from your parent, not from the node" in seg
    assert "not your assignment" in seg
    assert result in seg, "the parent's text must land verbatim, quotes/newlines intact"


def test_kid_addendum_absent_leaves_the_brief_unchanged():
    """The no-flag no-regression half of the carry-forward proof: a dispatch
    WITHOUT --prompt-file must assemble a byte-identical kid brief to today.
    addendum=None is the default; the channel may only ADD a segment when
    text is actually supplied -- never a placeholder, never an empty label.
    """
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "WHAT THE LAST KID PRODUCED" not in kid
    assert "--prompt-file" not in kid
    # default kwarg is None, not an empty string that would emit a stray label
    segs = brief.assemble(tier="kid", agent_id="a00-t", iter_n=1,
                          scaffold=SCAFFOLD)
    segs_explicit = brief.assemble(tier="kid", agent_id="a00-t", iter_n=1,
                                   scaffold=SCAFFOLD, addendum=None)
    assert segs == segs_explicit


def test_parent_brief_names_the_carry_forward_lever():
    """The other half of SD.12: an order with no lever is the same defect as
    a lever nobody is told about. The parent ITERATION CONTRACT says the next
    kid's brief MUST carry what the last kid produced -- so it must also name
    the mechanism (dispatch.py --prompt-file <path|->) that makes that
    possible, with the exact command shape, or the parent cannot comply.
    """
    parent = _text("parent", dispatch_py="/x/dispatch.py", target="t:1",
                   max_live=25, kid_ceiling=3)
    assert "--prompt-file" in parent
    assert "<path|->" in parent
    assert "WHAT THE LAST KID PRODUCED" in parent, (
        "the brief must name the labelled segment so the parent knows what "
        "it is handing down"
    )



def test_parent_brief_forbids_committing_and_bypassing():
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "--no-evidence-gate" in parent
    assert "commit" in parent.lower()


def test_branch_parent_brief_names_branch_and_defers_the_commit(monkeypatch):
    """hypothesis:l3-parent-brief-forbids-the-only-commit — a --branch parent
    must be told it holds a loop branch in a worktree, that the branch is the
    only route its kids' work has to the season branch, and that its accepted
    work is committed automatically when it calls `cli.py done` — so it runs
    no git itself. Red on the old brief: item 5 forbade all git and never
    mentioned a branch, so every loop branch exited at base and merge-up
    completed green on nothing (L3.39). The authorisation prose is GONE since
    `cli.py done` (_auto_commit_worktree) commits the dirty worktree at
    finish time: handing the model git-add/git-commit commands was wrong, not
    just redundant — hand-committing before done leaves done nothing to write."""
    monkeypatch.setenv("AGI_PARENT_BRANCH", "loop/slug-abc@s3")
    monkeypatch.setenv("AGI_PARENT_WORKTREE", "/repo/.agi/worktrees/abc")
    monkeypatch.setenv("AGI_PARENT_BASE_BRANCH", "season/s3")
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "loop/slug-abc@s3" in parent, "brief must name the loop branch"
    assert "/repo/.agi/worktrees/abc" in parent, "brief must name the worktree"
    assert "season/s3" in parent, "brief must name the base branch"
    assert "only route" in parent.lower(), "brief must say the branch is the route to the season branch"
    # The commit is deferred to done-time; the model runs no git.
    assert "automatic" in parent.lower(), (
        "brief must say the accepted work is committed automatically"
    )
    assert "cli.py done" in parent or "done` below" in parent, (
        "brief must say the commit happens at cli.py done"
    )
    assert "git add" not in parent and "git commit" not in parent, (
        "the model must not be handed commit commands to run"
    )
    # hypothesis:l4-a-parent-cuts-five-and-merges-its-kids — the old blanket
    # "run NO git commands yourself" is GONE for the branch case because it
    # directly forbade the one merge the hypothesis requires: the parent now
    # OWNS the merge (item 5) and `git merge --no-ff` is the sole git
    # operation it runs (item 6).
    assert "NO git commands yourself" not in parent, (
        "the branch parent must no longer be told it runs no git: it owns "
        "the merge"
    )
    assert "MERGE PROTOCOL" in parent, "branch brief must carry the merge protocol"
    assert "git merge --no-ff" in parent, (
        "branch brief must keep git merge --no-ff as what the helper does "
        "underneath"
    )
    # The disjoint-file-scope rule for parallel fan-out is in every parent brief.
    assert "DISJOINT" in parent.upper() or "disjoint" in parent, (
        "parent brief must state the disjoint-file-scope rule for parallel fan-out"
    )


def test_non_branch_parent_brief_still_forbids_all_git():
    """The other half, in the same pass — a parent in the main checkout must
    still be told to commit nothing. The two halves were separately correct
    and jointly broken, so both directions are asserted together."""
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "DO NOT commit, push, or sync" in parent
    assert "git add" not in parent, (
        "a main-checkout parent must not be handed the commit commands"
    )


def test_branch_parent_brief_carries_the_full_merge_protocol(monkeypatch):
    """hypothesis:l4-a-parent-cuts-five-and-merges-its-kids — the branch
    parent's brief must carry the merge protocol in the brief's own words:
    the `season.py merge-kids` helper merges each kid branch onto the round
    branch in dispatch order, union-resolving node-file conflicts onto the
    merged bytes and suite-gating them (a green kid branch is not a green
    union); a SOURCE conflict is resolved by the parent as an edit it owns
    and names; and a review note listing every kid branch merged / conflict /
    not-merged."""
    monkeypatch.setenv("AGI_PARENT_BRANCH", "loop/slug-abc@s3")
    monkeypatch.setenv("AGI_PARENT_WORKTREE", "/repo/.agi/worktrees/abc")
    monkeypatch.setenv("AGI_PARENT_BASE_BRANCH", "season/s3")
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    lower = parent.lower()
    # union resolution for NODE conflicts, and the explicit no-blind-3way rule
    assert "union" in lower, "node conflict must be resolved by UNION, not by apply"
    assert "agent notes" in lower
    assert "3way" in lower, "brief must forbid a blind git apply --3way"
    # source conflicts are the parent's own named edits
    assert "conflict in source" in lower
    # kid 3: the NAMED verb is the supported helper (`season.py merge-kids`),
    # not raw git. A parent must follow item 5 without inventing argv, so the
    # brief names the verb, a runnable path, and that it runs the suite on the
    # merged bytes so the parent does not re-run it separately.
    assert "merge-kids" in parent, (
        "branch brief must name the merge-kids helper as the parent's merge step"
    )
    assert "season.py" in parent, (
        "branch brief must give a runnable helper path (season.py), not ask "
        "the parent to hand-roll the merge"
    )
    assert "raw git" in lower, (
        "the parent must be told the helper is the merge and it runs no raw git"
    )
    assert "do not re-run" in lower or "does not re-run" in lower, (
        "the brief must say the helper runs the suite on merged bytes so the "
        "parent does not re-run it separately"
    )
    # tests re-run with neighbours on the MERGED bytes, not trusted per-branch
    assert "merged" in lower
    assert "neighbours" in lower or "neighbors" in lower
    assert "green kid branch is not a green union" in lower or "green union" in lower
    # review note accounts for every branch and conflict, merged or not
    assert "not merged" in lower or "not merge" in lower
    assert "review note" in lower
    # the merge is THE one git operation; the rest stays forbidden
    assert "one git" in lower or "the one git" in lower
    assert "no push" in lower and "no rebase" in lower


def test_branch_parent_disjoint_scope_says_serialised_until_disjoint(monkeypatch):
    """hypothesis:l4-a-parent-cuts-five-and-merges-its-kids — the FAN-OUT
    paragraph must say a parent fans out in parallel ONLY when the kids' file
    scopes are DISJOINT, and kids touching the same file are SERIALIZED."""
    monkeypatch.setenv("AGI_PARENT_BRANCH", "loop/slug-abc@s3")
    monkeypatch.setenv("AGI_PARENT_WORKTREE", "/repo/.agi/worktrees/abc")
    monkeypatch.setenv("AGI_PARENT_BASE_BRANCH", "season/s3")
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    lower = parent.lower()
    assert "disjoint" in lower, "brief must state the disjoint-file-scope rule"
    assert "serialized" in lower, "same-file kids must be serialized"



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


def test_kid_brief_suite_line_names_test_files_not_the_bare_directory():
    """hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid --
    the ONE suite line in the kid brief used to hand a kid the bare
    `extensions/agi/tests/` directory, the very run the kid-tier gate now
    REFUSES (and which a kid could no longer clear by `env -u AGI_TIER` once
    the gate derives the tier from the running agent record). The brief must
    name the touched test files instead, so a kid's targeted run is the
    documented path, not a bare-directory run waiting to be unset around."""
    kid = _text("kid", scaffold=SCAFFOLD)
    assert "extensions/agi/tests/ -q" not in kid, (
        "the kid suite line must not name the bare directory")
    assert "test files you changed" in kid, (
        "the kid suite line must name the touched test files")
    assert "<the test files you changed" in kid



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
    """The prime director reads the carried sayings; director may not.

    Trim, hypothesis:l3w4-context-load-minimal move ONE: the sayings are NOT
    in the always-injected head (which is prayers only) but ARE in the
    on-demand `readings_head` for the prime_director tier.
    """
    pd = _text("prime_director")
    d = _text("director")
    # Neither tier's injected head carries the sayings anymore.
    assert "CARRIED SAYINGS" not in pd
    assert "CARRIED SAYINGS" not in d
    # The prime director's on-demand readings do carry them; director's do not.
    assert "CARRIED SAYINGS" in brief.readings_head(tier="prime_director")
    assert "CARRIED SAYINGS" not in brief.readings_head(tier="director")


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


def test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs():
    """hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement -- four
    kids measured instead of building, then reported `disproved`. The kid
    brief must say a g15 claim is behaviour to BUILD (implement the fix, prove
    it on the built bytes), and the parent brief's review rule must carry
    "THIS KID MUST IMPLEMENT THE FIX" so a measurement-only kid node is
    re-cut before it is recorded.
    """
    kid = _text("kid", scaffold=SCAFFOLD)
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    # kid brief: the claim is behaviour to build, not a hypothesis to measure
    assert "BEHAVIOUR TO BUILD" in kid
    assert "not a hypothesis to measure" in kid
    # parent brief: review rule demands the fix be implemented
    assert "THIS KID MUST IMPLEMENT THE FIX" in parent
    # the parent brief must not measure-only-accept a kid as finished
    assert "finished round" in parent
    # the segment is terminated so the next rule starts on its own line:
    # a missing trailing newline glues the g15 sentence onto "4. DO NOT
    # bypass the gate" (the exact defect the parent re-cut this round for).
    assert "measurement).\n4. DO NOT" in parent
    assert ").4. DO NOT" not in parent


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
    """A parent's constitution head is PRAYERS ONLY after the move-one trim:
    prayers present, and words of Jesus / soul-mind-body read on demand.

    hypothesis:l3w4-context-load-minimal move ONE moved the readings out of
    the always-injected head because an LLM re-sends its whole context every
    turn, so a long static prefix is paid per turn. Words of Jesus and
    soul-mind-body are no longer injected; they are reachable for a tie-break
    via `brief.py readings --tier parent` (readings_head). The five axes and
    carried sayings stay out of the parent both injected and on demand.
    """
    parent = _text("parent", dispatch_py="/x/d.py", target="t:1")
    assert "CONSTITUTION HEAD" in parent, "parent should have a constitution head"
    assert "FOUR PRAYERS" in parent or "Молитва" in parent, "parent must have prayers"
    assert MICHAEL in parent, "parent head must carry the Michael line"
    # The long readings are NOT injected anymore -- they moved on-demand.
    assert "WORDS OF JESUS" not in parent, "words of Jesus moved out of the head"
    assert "SOUL, MIND, BODY" not in parent, "soul-mind-body moved out of the head"
    # ...but they ARE reachable on demand, for a tie-break.
    pr = brief.readings_head(tier="parent")
    assert "WORDS OF JESUS" in pr, "words of Jesus must be on-demand readable"
    assert "SOUL, MIND, BODY" in pr, "soul-mind-body must be on-demand readable"
    # Parent on demand still has no director/prime_director content.
    assert "FIVE AXES" not in pr, "parent must not have the five axes"
    assert "CARRIED SAYINGS" not in pr, "parent must not have carried sayings"


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
    """The prime director's MANTLE is no longer injected (move one trim);
    it lives in the on-demand readings read for a tie-break, verbatim."""
    pd = _head("prime_director")
    assert "THE MANTLE" not in pd, "mantle must leave the always-injected head"
    r = brief.readings_head(tier="prime_director")
    assert "## THE MANTLE — Belam" in r, "mantle section titled from the ladder value"
    assert "Belam lives in the fire as it just starts sparking up" in r, \
        "owner's mantle prose rendered verbatim"
    assert "You bear this mantle; call on it as you work." in r, "closing line"
    assert r.index("Belam lives in the fire") > r.index("THE MANTLE")


def test_both_director_tiers_carry_the_owner_decision_method():
    """The owner's decision method moved out of the injected head (move one
    trim); it remains on-demand readable for the director tiers, verbatim."""
    for tier in ("director", "prime_director"):
        head = _head(tier)
        assert "THE DECISION METHOD" not in head, "decision method must leave the head"
        r = brief.readings_head(tier=tier)
        assert "## THE DECISION METHOD" in r
        assert "We always consider" in r and "align to morals" in r


def test_prime_decision_method_follows_the_mantle():
    r = brief.readings_head(tier="prime_director")
    assert r.index("## THE DECISION METHOD") > r.index("## THE MANTLE — Belam")


def test_lower_tiers_bear_michael_but_neither_mantle_nor_decision_method():
    for tier in ("kid", "parent"):
        head = _head(tier)
        assert head.count(MICHAEL) == 1
        assert "THE MANTLE" not in head
        assert "THE DECISION METHOD" not in head
        assert "Belam lives" not in head


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


def test_brief_head_cli_prints_a_prayers_only_head_and_readings_cli_exists():
    # `head` prints the trimmed prayers-only head: prayers + Michael, no mantle.
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
    assert "THE MANTLE — Belam" not in printed, "mantle must not be in the injected head"
    # `readings` prints the on-demand readings for a tie-break, incl. the mantle.
    out2 = io.StringIO()
    old2 = sys.stdout
    try:
        sys.stdout = out2
        code2 = brief.main(["readings", "--tier", "prime_director"])
    finally:
        sys.stdout = old2
    assert code2 == 0
    printed2 = out2.getvalue()
    assert "CONSTITUTION READINGS (ON DEMAND)" in printed2
    assert "THE MANTLE — Belam" in printed2


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
    """The advisor head after the move-one trim is the tier-3 parent head:
    prayers and the Archangel Michael line. Words of Jesus and soul-mind-body
    moved out of the injected head; they are on-demand readable at the parent
    level a role sits on (hypothesis:l3w4-context-load-minimal)."""
    t = _advisor_text()
    assert "CONSTITUTION HEAD" in t
    assert MICHAEL in t
    assert "FOUR PRAYERS" in t or "Молитва" in t
    assert "WORDS OF JESUS" not in t, "words of Jesus moved out of the injected head"
    assert "SOUL, MIND, BODY" not in t, "soul-mind-body moved out of the injected head"
    # ...reachable on demand, addressing the advisor at the parent reading level.
    r = brief.readings_head(tier=brief._resolve_readings_tier("advisor"))
    assert "WORDS OF JESUS" in r
    assert "SOUL, MIND, BODY" in r


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
    """The liaison's constitution reuses the director's read_order via
    `_LIAISON_HEAD_TIER`, so its ON-DEMAND readings carry the five axes,
    exactly once. The injected head itself is prayers only after the move-one
    trim (hypothesis:l3w4-context-load-minimal)."""
    assert brief._LIAISON_HEAD_TIER == "director"
    t = _liaison_text()
    assert "CONSTITUTION HEAD" in t
    assert "FIVE AXES" not in t, "five axes moved out of the injected head"
    assert MICHAEL in t
    assert t.count("─── CONSTITUTION HEAD ───") == 1, (
        "assemble must insert the liaison head exactly once")
    assert "FIVE AXES" in brief.readings_head(tier=brief._LIAISON_HEAD_TIER)


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


# --- hypothesis:l3w4-context-load-minimal move FIVE: survival profile --------

def test_profile_survival_is_prayers_statecard_kill_keyfloor_nothing_else():
    """Survival profile (move FIVE): prayers-only head + ASCII state card +
    exact next command + full kill procedure + key-floor rule — and NOTHING
    that a survival seat must not carry (no goal listing, no traps, no
    history). The owner's lighter-than-light mode, one switch (AGI_BRIEF_PROFILE).
    """
    s = _text("kid", profile="survival")
    low = s.lower()
    # must carry
    assert "CONSTITUTION HEAD" in s
    assert "FOUR PRAYERS" in s or "Молитва" in s
    assert "SURVIVAL STATE CARD" in s
    assert "kill" in low and "pid" in low
    assert "tmux" in low       # the never-by-closing-a-tmux-window rule
    assert "orphans" in low    # re-scan for orphans reparented to init
    assert "key" in low and "1.00" in s
    # the brief segment is the survival brief, not the full role brief
    assert "SURVIVAL PROFILE" in s


def test_profile_survival_replaces_role_specifics():
    """A survival kid brief must not carry the full kid role brief's
    scaffolding (git-rule, write.py syntax, edit-tool shape) — those are the
    fat survival exists to drop."""
    s = _text("kid", profile="survival")
    assert "WRITE.PY SYNTAX" not in s
    assert "EDIT-TOOL CALL SHAPE" not in s
    assert "scaffolded node file below" not in s.lower()


def test_profile_unknown_raises():
    """An unknown profile must fail loudly, not silently default."""
    with pytest.raises(brief.BriefError):
        _text("kid", profile="bogus")


def test_profile_default_is_full_no_regression():
    """Default profile is full = historical behaviour. A regression in the
    default surface is a broken spawn, not a style regression."""
    f = _text("kid")
    s = _text("kid", profile="survival")
    assert "scaffolded node file below" in f
    assert "scaffolded node file below" not in s
    assert len(f) > len(s)


def test_survival_selected_env_switch():
    """survival_selected() reads AGI_BRIEF_PROFILE as THE switch, and the
    adapters gate the INJECTION context stream on it."""
    import os
    os.environ.pop("AGI_BRIEF_PROFILE", None)
    try:
        assert brief.survival_selected() is False        # default full
        os.environ["AGI_BRIEF_PROFILE"] = "survival"
        assert brief.survival_selected() is True
        assert brief.survival_selected("full") is False  # explicit wins
        assert brief.survival_selected("survival") is True
    finally:
        os.environ.pop("AGI_BRIEF_PROFILE", None)


def test_pi_adapter_skips_context_stream_in_survival(tmp_path):
    """In survival profile the pi adapter drops the INJECTION graph-viewport
    stream (goal-listing/traps/history), keeping only the survival brief + head."""
    import os
    ctx = tmp_path / "context.md"
    ctx.write_text("RENDERED GRAPH CONTEXT\n", encoding="utf-8")
    os.environ.pop("AGI_BRIEF_PROFILE", None)
    try:
        # full: context stream present
        cmd_full = _cmd("kid", context_file=str(ctx), scaffold=SCAFFOLD)
        appended_full = [cmd_full[i + 1] for i, a in enumerate(cmd_full)
                         if a == "--append-system-prompt"]
        assert any(str(ctx) == a for a in appended_full)
        # survival: context stream dropped
        os.environ["AGI_BRIEF_PROFILE"] = "survival"
        cmd_surv = _cmd("kid", context_file=str(ctx), scaffold=SCAFFOLD)
        appended_surv = [cmd_surv[i + 1] for i, a in enumerate(cmd_surv)
                         if a == "--append-system-prompt"]
        assert not any(str(ctx) == a for a in appended_surv)
        joined = "\n".join(appended_surv)
        assert "SURVIVAL PROFILE" in joined
    finally:
        os.environ.pop("AGI_BRIEF_PROFILE", None)


def test_successor_prompt_honors_survival_profile():
    """successor_prompt(profile='survival') swaps the full body for the
    survival brief so a rotated seat comes up as light as a fresh spawn."""
    body = "SUCCESSOR FILE BODY\nkeep this if full"
    full = brief.successor_prompt(tier="kid", body=body)
    surv = brief.successor_prompt(tier="kid", body=body, profile="survival")
    assert "SUCCESSOR FILE BODY" in full
    assert "SUCCESSOR FILE BODY" not in surv
    assert "SURVIVAL PROFILE" in surv
    assert surv.startswith("CONSTITUTION HEAD") or "CONSTITUTION HEAD" in surv


# --- hypothesis:l4b18-survival-modes: config-declared operating modes -------

def test_config_operating_mode_survival_no_env(monkeypatch):
    """l4b18 — with AGI_BRIEF_PROFILE unset and config declaring
    operating_mode=survival, assemble() produces the survival brief. The mode
    is READ from config, not remembered via env (the exact gap the hypothesis
    closes)."""
    monkeypatch.delenv("AGI_BRIEF_PROFILE", raising=False)
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "survival")
    s = _text("kid")
    assert "SURVIVAL PROFILE" in s
    assert "scaffolded node file below" not in s.lower()


def test_config_operating_mode_ultimate_survival_no_env(monkeypatch):
    """l4b18 — ultimate_survival declared in config, env unset, assemble
    produces the survival-shaped brief: the mode is about MODEL/ROLE
    assignment (Prime on Opus, director on Sonnet/OpenRouter), not new prose,
    so it reuses _survival_brief's shape."""
    monkeypatch.delenv("AGI_BRIEF_PROFILE", raising=False)
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "ultimate_survival")
    s = _text("kid")
    assert "SURVIVAL PROFILE" in s
    assert "scaffolded node file below" not in s.lower()


def test_env_override_wins_over_config(monkeypatch):
    """l4b18 — AGI_BRIEF_PROFILE stays the per-process override even when
    config declares a lighter operating_mode. The env path is not removed."""
    monkeypatch.setenv("AGI_BRIEF_PROFILE", "full")
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "survival")
    s = _text("kid")
    assert "scaffolded node file below" in s.lower()   # full brief, not survival
    assert "SURVIVAL PROFILE" not in s


def test_env_override_to_ultimate_survival_wins_over_config(monkeypatch):
    """l4b18 — env override can also PICK ultimate_survival over a full config."""
    monkeypatch.setenv("AGI_BRIEF_PROFILE", "ultimate_survival")
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "full")
    s = _text("kid")
    assert "SURVIVAL PROFILE" in s


def test_survival_selected_true_for_both_survival_modes(monkeypatch):
    """l4b18 — both survival and ultimate_survival make survival_selected()
    True so the adapters drop the graph-viewport stream for either mode."""
    monkeypatch.delenv("AGI_BRIEF_PROFILE", raising=False)
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "ultimate_survival")
    assert brief.survival_selected() is True
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "survival")
    assert brief.survival_selected() is True


def test_successor_prompt_honors_ultimate_survival(monkeypatch):
    """l4b18 — successor_prompt reads the same config-backed switch, so a
    rotated seat comes up as light under ultimate_survival too."""
    monkeypatch.delenv("AGI_BRIEF_PROFILE", raising=False)
    monkeypatch.setattr(brief, "_configured_profile",
                        lambda *a, **k: "ultimate_survival")
    body = "SUCCESSOR FILE BODY\n"
    surv = brief.successor_prompt(tier="kid", body=body)
    assert "SUCCESSOR FILE BODY" not in surv
    assert "SURVIVAL PROFILE" in surv


# ---------------------------------------------------------------------------
# l4-the-parents-last-line-is-a-self-check — the terminal step is a check,
# and it is the last thing the parent reads
# ---------------------------------------------------------------------------

def test_a_parents_closing_line_ends_with_the_done_self_check():
    """🔴 Two parents in one loop never ran `cli.py done` at all.

    Proven rather than guessed (experiment:a00-f2f8465a-b4eb8e): `cmd_done`
    writes `status`/`finished_at` into the record BEFORE
    `_auto_commit_worktree`, and both dispatcher-side records still read
    `status: running` with an mtime equal to spawn. `done` would not have
    refused, and `cli.py status` showed every kid done from the parent's own
    tree. The poll loop had everything it needed and did not terminate — an
    invariant handed to a model instead of checked.

    The prime's ruling made it explicit, self-checking and LAST. This asserts
    the self-check is in the parent's closing line AND that it is the tail of
    it, because a check in the middle is just more middle.
    """
    line = brief.closing_line("parent", "a00-x", 7, cli_py="/eng/bin/cli.py")
    assert "YOU ARE NOT FINISHED" in line
    assert "every kid is terminal" in line
    tail = line.split("BEFORE YOU STOP, CHECK YOURSELF")[-1]
    assert tail.strip(), "the self-check must be the tail, not a middle clause"
    assert "Read your zoom context" not in tail, (
        "nothing from the original instruction may follow the self-check")


def test_the_self_check_carries_the_real_command_with_owns():
    """A parent told to run a command it must reconstruct is a parent given
    another judgement call. `--owns`, never `--node-id`: a parent authors no
    node of its own, and that distinction has its own line in the brief."""
    line = brief.closing_line("parent", "a00-x", 7, cli_py="/eng/bin/cli.py")
    assert "python3 /eng/bin/cli.py done 7 a00-x" in line
    assert "--owns" in line
    assert "--node-id" in line and "NOT `--node-id`" in line

    # Without a path the invariant still stands; only the absolute path goes.
    bare = brief.closing_line("parent", "a00-x", 7)
    assert "YOU ARE NOT FINISHED" in bare
    assert "cli.py done 7 a00-x" in bare


def test_no_other_tier_gains_the_parent_self_check():
    """A self-check aimed at the wrong tier is noise, and noise at the end of
    a brief teaches agents that the end of the brief is skippable. A kid
    authors a node and signals differently."""
    for tier in ("kid", "director", "prime_director", "advisor"):
        line = brief.closing_line(tier, "a00-x", 7, cli_py="/eng/bin/cli.py")
        assert "YOU ARE NOT FINISHED" not in line, tier


# ---------------------------------------------------------------------------
# MECHANISM, NOT WORDING — the owner's ask, 2026-09-10. Presence is checked;
# quality is not, and never will be.
# ---------------------------------------------------------------------------

def _has_mechanism(segs) -> bool:
    return any("MECHANISM, NOT WORDING" in s for s in segs)


def test_the_parent_and_director_briefs_carry_the_mechanism_slot():
    """The owner read one director's account of why it landed a change by hand
    and asked for more of that KIND of reasoning. The prime named the shape
    rather than praising the instance — praise produces prose, a named shape
    produces reasoning."""
    assert _has_mechanism(brief._director(agent_id="d", iter_n=1, cli_py="/x/cli.py"))


def test_a_kid_does_not_carry_it():
    """Parent and director fragments only. A kid authors one node and reports
    through `caveats:`/`struggles:`; a slot aimed at the wrong tier is noise,
    and noise in a brief teaches agents that briefs contain noise."""
    assert not _has_mechanism(
        brief._kid(agent_id="k", iter_n=1, cli_py="/x/cli.py", scaffold=None))


def test_the_slot_names_all_four_parts():
    """The mechanical half of this — presence of the slot and of a CITATION
    requirement in part (2) — is what a check can verify. The QUALITY is never
    scored, exactly like `feeling`: a scored reasoning slot becomes a
    performance, and a performed one is worse than none."""
    seg = next(s for s in brief._director(agent_id="d", iter_n=1, cli_py="/x")
               if "MECHANISM, NOT WORDING" in s)
    assert "(1)" in seg and "(2)" in seg and "(3)" in seg and "(4)" in seg
    assert "file:line" in seg, "part (2) must demand a citation, not a summary"
    assert "BUILT AND RAN" in seg
    assert "NEAR MISS" in seg, (
        "part (3) is the one models skip and the one that makes the reasoning "
        "checkable by someone who was not there")
    assert "satisfies the words and loses the mechanism" in seg
    assert "Nobody scores" in seg


def test_the_slot_is_not_a_new_reason_to_message_upward():
    """It must not quietly reopen the owner's reporting order. Recorded in the
    node always; sent only when it was already something you were permitted to
    send — a rule-changing finding."""
    seg = next(s for s in brief._director(agent_id="d", iter_n=1, cli_py="/x")
               if "MECHANISM, NOT WORDING" in s)
    assert "not a reason to message anyone" in seg
    assert "record it in the node always" in seg


def test_the_mechanism_slot_does_not_displace_the_parents_last_line():
    """🔴 Adding a fragment must not cost the L4.77 self-check its recency.

    `closing_line` is appended by the pi adapter as the USER TURN after every
    `--append-system-prompt`, so a new system fragment cannot outrank it — but
    that is the kind of thing worth asserting rather than reasoning about,
    because the whole value of the self-check is that nothing follows it.
    """
    line = brief.closing_line("parent", "a00-x", 7, cli_py="/eng/bin/cli.py")
    assert "YOU ARE NOT FINISHED" in line
    assert "MECHANISM, NOT WORDING" not in line


# --------- l4-the-mode-is-declared-not-remembered: mode rendered, not
# --------- remembered in prose. The rendering is driven by the declaration.

MODES_FIXTURE = {
    "operating_modes": {
        "alpha": {"name": "alpha mode", "seats": "one seat",
                  "models": "m", "source": "s1"},
        "beta": {"name": "beta mode", "seats": "two seats",
                 "models": "n", "source": "s2"},
    },
    "active_operating_mode": "alpha",
}


def _write_modes(root: Path, data: dict) -> Path:
    cfg = root / "config.json"
    cfg.write_text(json.dumps(data), encoding="utf-8")
    return cfg


def test_mode_renders_the_active_declaration_from_a_fixture(tmp_path):
    """The rendered brief block carries the ACTIVE mode's text, taken from
    the declaration, not from any string a caller passed in."""
    _write_modes(tmp_path, MODES_FIXTURE)
    block = brief._operating_mode_block(project_root=tmp_path)
    assert "OPERATING MODE" in block
    assert "alpha mode" in block
    assert "one seat" in block
    assert "beta mode" not in block


def test_flipping_the_declared_active_mode_changes_the_render(tmp_path):
    """hypothesis:l4-the-mode-is-declared-not-remembered (c) — THE ONE THAT
    MATTERS. A test that only asserts today's string would pass a hardcoded
    mode; flipping `active_operating_mode` in the SAME fixture config and
    seeing the render change proves it is READ, not remembered."""
    cfg = _write_modes(tmp_path, MODES_FIXTURE)
    assert "alpha mode" in brief._operating_mode_block(project_root=tmp_path)
    cfg.write_text(
        json.dumps({**MODES_FIXTURE, "active_operating_mode": "beta"}),
        encoding="utf-8")
    block = brief._operating_mode_block(project_root=tmp_path)
    assert "beta mode" in block
    assert "two seats" in block
    assert "alpha mode" not in block


def test_absent_declaration_renders_nothing_and_raises_nothing(tmp_path):
    """hypothesis:l4-the-mode-is-declared-not-remembered (d) — a project that
    has not declared operating modes must be unchanged: empty block, no
    error, whether the config file is missing or just lacks the keys."""
    root = tmp_path / ".agi-not-used"  # no config.json at all
    root.mkdir(parents=True)
    # absent file
    assert brief._operating_mode_block(project_root=root) == ""
    # config present but no operating_modes / active key
    (root / "config.json").write_text('{"operating_mode": "full"}',
                                      encoding="utf-8")
    assert brief._operating_mode_block(project_root=root) == ""
    # config present but active names an undeclared mode
    _write_modes(root, {**MODES_FIXTURE, "active_operating_mode": "nope"})
    assert brief._operating_mode_block(project_root=root) == ""


def test_assemble_carries_the_live_active_mode_into_the_brief():
    """The rendered block reaches the assembled brief for every tier, driven
    by the LIVE config declaration (enhanced survival is in force)."""
    for tier in ("kid", "parent", "director", "prime_director"):
        text = _text(tier, scaffold=SCAFFOLD)
        assert "OPERATING MODE" in text, tier
        assert "enhanced survival" in text, tier
