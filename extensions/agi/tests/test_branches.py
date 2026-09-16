import subprocess
from pathlib import Path

import pytest

import branches as b


def test_season_main_exact():
    assert b.season_main(1) == "season1/main"
    assert b.season_main(2) == "season2/main"


def test_town_main_exact():
    assert b.town_main(2, "streaming-suite", 1) == "season2/streaming-suite/season1/main"
    assert b.town_main(2, "web-app-suite", 1) == "season2/web-app-suite/season1/main"


def test_post_branch_exact():
    assert b.post_branch(2, "foo") == "season2/posts/foo"


def test_loop_branch_exact():
    assert b.loop_branch(2, "opt-auth", "a1") == "season2/loops/opt-auth-a1"


def test_reserved_town_refused():
    for leaf in ("main", "posts", "loops"):
        with pytest.raises(ValueError):
            b.town_main(2, leaf, 1)


def test_parse_main():
    d = b.parse("season2/main")
    assert d["kind"] == "main"
    assert d["season"] == 2


def test_parse_town_main():
    d = b.parse("season2/streaming-suite/season1/main")
    assert d["kind"] == "town_main"
    assert d["season"] == 2
    assert d["town"] == "streaming-suite"
    assert d["town_season"] == 1


def test_parse_post():
    d = b.parse("season2/posts/foo")
    assert d["kind"] == "post"
    assert d["season"] == 2
    assert d["name"] == "foo"


def test_parse_loop():
    d = b.parse("season2/loops/opt-auth-a1")
    assert d["kind"] == "loop"
    assert d["season"] == 2
    assert d["name"] == "opt-auth-a1"


def test_parse_town_post():
    d = b.parse("season2/streaming-suite/season1/posts/bar")
    assert d["kind"] == "post"
    assert d["town"] == "streaming-suite"
    assert d["town_season"] == 1
    assert d["name"] == "bar"


def test_parse_round_trip_build_fns():
    for name in (
        b.season_main(2),
        b.town_main(2, "web-app-suite", 1),
        b.post_branch(2, "foo"),
        b.loop_branch(2, "opt-auth", "a1"),
    ):
        assert b.parse(name) is not None  # parses without raising


def test_parse_garbage_raises():
    for name in ("garbage", "season2/bogus/x/y", "season/main/posts/loops"):
        with pytest.raises(ValueError):
            b.parse(name)


# --- deprecated aliases ---


@pytest.mark.parametrize("old,canonical", [
    ("master", "season1/main"),
    ("season/s2", "season2/main"),
    ("seat/streaming-suite@s2", "season2/posts/streaming-suite"),
    ("town/streaming-suite/season/s1", "season2/streaming-suite/season1/main"),
    ("town/web-app-suite@s2", "season2/web-app-suite/season1/main"),
])
def test_alias_forms(old, canonical):
    d = b.parse(old)
    assert d["kind"] == "alias"
    assert d["canonical"] == canonical


def test_alias_warns_once_per_process(monkeypatch):
    b._warned = False
    err = []
    monkeypatch.setattr(b.sys, "stderr", _Sink(err))
    b.parse("master")
    b.parse("master")
    b.parse("season/s2")
    assert "".join(err).count("deprecated alias used") == 1
    b._warned = False


def test_alias_seat_never_raises():
    # A `seat/<name>@s<N>` resolves to a POST branch; it never refuses.
    d = b.parse("seat/streaming-suite@s2")
    assert d["kind"] == "alias"
    assert d["canonical"] == "season2/posts/streaming-suite"


# --- merge_target ---


def test_merge_target_season_post_loop():
    assert b.merge_target("season2/posts/foo") == "season2/main"
    assert b.merge_target("season2/loops/xx-yy") == "season2/main"
    assert b.merge_target(b.post_branch(2, "foo")) == "season2/main"
    assert b.merge_target(b.loop_branch(2, "xx", "yy")) == "season2/main"


def test_merge_target_town_main():
    assert b.merge_target("season2/web-app-suite/season1/posts/foo") == \
        "season2/web-app-suite/season1/main"
    assert b.merge_target("season2/web-app-suite/season1/loops/xx-yy") == \
        "season2/web-app-suite/season1/main"


def test_merge_target_legacy_loop_alias_to_season_main():
    # The one-season deprecated `loop/<slug>@s<N>` spelling resolves through
    # its canonical to the season main it sits under.
    assert b.merge_target("loop/xx-yy@s2") == "season2/main"


def test_merge_target_leaf_is_its_own_target():
    # Sitting ON a main leaf returns that leaf unchanged -- a core main and a
    # town main are each their own merge target.
    assert b.merge_target("season2/main") == "season2/main"
    assert b.merge_target("season2/web-app-suite/season1/main") == \
        "season2/web-app-suite/season1/main"


# --- ref_candidates (the season-grammar reader resolver) ---


def test_ref_candidates_season_trunk():
    assert b.ref_candidates("season2/main") == ["season2/main", "season/s2"]


def test_ref_candidates_town_trunk():
    assert b.ref_candidates("season2/web-app-suite/season1/main") == [
        "season2/web-app-suite/season1/main",
        "town/web-app-suite/season/s1",
        "town/web-app-suite@s2",
    ]


def test_ref_candidates_loop():
    # a loop branch falls back to its legacy @s<N> spelling too
    assert b.ref_candidates("season2/loops/opt-auth-a1") == [
        "season2/loops/opt-auth-a1",
        "loop/opt-auth-a1@s2",
    ]


def test_ref_candidates_accepts_old_input_canonical_first():
    # an OLD name is accepted and still resolves canonical-first (never refused)
    assert b.ref_candidates("season/s2") == ["season2/main", "season/s2"]


def test_ref_candidates_post_keeps_legacy_seat_alias():
    # A POST's candidates are canonical, INTERMEDIATE `post/<n>@s<n>`, and the
    # legacy `seat/<name>@s<n>` spelling — in that order, deduped
    # (hypothesis:l4-branches-follow-the-season-grammar a1 + the L4.319
    # intermediate rule). Canonical first, the as-written canonical input is
    # present in the list, legacy last, mirroring the loop branch case.
    assert b.ref_candidates("season2/posts/foo") == [
        "season2/posts/foo", "post/foo@s2", "seat/foo@s2"
    ]


def test_ref_candidates_seat_alias_canonical_first():
    # Real seat branch name on this box (harvest-pinned): canonical first,
    # the INTERMEDIATE `post/...@s<n>` spelling, old `seat/...@s<n>` spelled
    # input kept last. A reader handed the canonical POST name on a
    # pre-migration tree falls back through the intermediate to the live seat
    # ref; a reader handed the live seat ref still finds all three.
    name = "seat/sanctuary-director@s2"
    cands = b.ref_candidates(name)
    assert cands == [
        "season2/posts/sanctuary-director",
        "post/sanctuary-director@s2",
        name,
    ]
    # and the canonical-first direction resolves to the same triple
    assert b.ref_candidates("season2/posts/sanctuary-director") == [
        "season2/posts/sanctuary-director",
        "post/sanctuary-director@s2",
        name,
    ]


# --- L4.322 (hypothesis:
# l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling)
# The as-written input spelling must ALWAYS appear in its own returned
# candidate list for ALL THREE input spellings of a post. Order is exactly
# [canonical, intermediate, legacy]; dedupe keeps the list unique.


@pytest.mark.parametrize("name", [
    "season2/posts/foo",
    "post/foo@s2",
    "seat/foo@s2",
])
def test_ref_candidates_post_input_keeps_as_written_spelling(name):
    cands = b.ref_candidates(name)
    # the as-written input is never dropped from its own candidate list
    assert name in cands
    # exactly [canonical, intermediate, legacy]
    assert cands == ["season2/posts/foo", "post/foo@s2", "seat/foo@s2"]
    # canonical first, legacy last
    assert cands[0] == "season2/posts/foo"
    assert cands[-1] == "seat/foo@s2"
    # dedupe keeps the list unique
    assert len(cands) == len(set(cands))


# --- L4.331 (hypothesis:
# l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-
# is-in-its-own-ref-candidates) — every input spelling appears in its own
# candidate list, not just the post/loop ones. `master` and the town
# one-season alias `town/<t>@s<N>` were absent from their own lists; the
# docstring claim "as-written input always appears in the result" is now
# true. Add the missing REVERSE rows to _canonical_to_old, canonical first,
# deduped, post/loop order untouched.


@pytest.mark.parametrize("name,expected", [
    # core season-1 main bears BOTH old spellings; `master` is legal
    # (is_legal_branch) and must be its own list.
    ("season1/main", ["season1/main", "season/s1", "master"]),
    ("master", ["season1/main", "season/s1", "master"]),
    ("season/s1", ["season1/main", "season/s1", "master"]),
    # a town main with town_season==1 bears town/<t>/season/s<1> AND the
    # one-season alias town/<t>@s<n>.
    ("town/core@s2", ["season2/core/season1/main", "town/core/season/s1", "town/core@s2"]),
    ("town/core/season/s1", ["season2/core/season1/main", "town/core/season/s1", "town/core@s2"]),
    ("season2/core/season1/main", ["season2/core/season1/main", "town/core/season/s1", "town/core@s2"]),
    # the already-true post/loop/season lists stay byte-identical
    ("season/s2", ["season2/main", "season/s2"]),
    ("loop/y-a00@s2", ["season2/loops/y-a00", "loop/y-a00@s2"]),
    ("post/foo@s2", ["season2/posts/foo", "post/foo@s2", "seat/foo@s2"]),
    ("seat/foo@s2", ["season2/posts/foo", "post/foo@s2", "seat/foo@s2"]),
])
def test_ref_candidates_every_input_kind_in_own_list(name, expected):
    cands = b.ref_candidates(name)
    # the as-written input spelling is never dropped from its own list
    assert name in cands
    # canonical first, deduped, exact expected row
    assert cands == expected
    assert cands[0] == expected[0]
    assert len(cands) == len(set(cands))


def test_ref_candidates_master_is_legal_branch():
    # `master` is accepted by the grammar (is_legal_branch -> True) and now
    # appears in its own candidate list.
    assert b.is_legal_branch("master") is True
    assert "master" in b.ref_candidates("master")


def test_town_alias_reverse_row_derives_back():
    # The one-season town alias round-trips: town/<t>@s<N> parses to
    # season<N>/<t>/season1/main, and a town main with town_season==1 now
    # derives BOTH old spellings back (town/<t>/season/s<k> and town/<t>@s<n>).
    assert b.parse("town/core@s2")["canonical"] == "season2/core/season1/main"
    assert b._canonical_to_old("season2/core/season1/main") == [
        "town/core/season/s1", "town/core@s2"]
    # a town main whose town_season is NOT 1 has no town@ reverse (town/<t>@s<n>
    # only means season<n>/<t>/season1/main).
    assert b._canonical_to_old("season2/core/season3/main") == [
        "town/core/season/s3"]


def test_master_reverse_only_for_season1_main():
    # `master` is the pre-rename spelling of ONLY the core season-1 main;
    # a later season main carries only its season/s<n> alias.
    assert b._canonical_to_old("season1/main") == ["season/s1", "master"]
    assert b._canonical_to_old("season2/main") == ["season/s2"]


class _Sink:
    def __init__(self, target):
        self.target = target

    def write(self, s):
        self.target.append(s)


# --- g15 round I residue (a1): real old names pinned on this box ---
# A `seat/<name>@s<N>` is a POST under that season's main; a
# `loop/<slug>-<agent>@s<N>` is a LOOP under it. Both are accepted as a
# DEPRECATED alias and canonicalise to the two-season spelling.

def test_seat_alias_canonicalises_to_post():
    d = b.parse("seat/post-name@s2")
    assert d["kind"] == "alias"
    assert d["season"] == 2
    assert d["canonical"] == "season2/posts/post-name"


def test_real_loop_alias_parses():
    # Real loop branch name on this box (harvest-pinned).
    name = "loop/hypothesis-harvest-table-subcomm-a00-26e81f42@s2"
    d = b.parse(name)
    assert d["kind"] == "alias"
    assert d["season"] == 2
    assert d["canonical"] == "season2/loops/hypothesis-harvest-table-subcomm-a00-26e81f42"


def test_loop_alias_ref_candidates_canonical_first():
    name = "loop/hypothesis-l4-branches-follow-th-a00-0b43f895@s2"
    cands = b.ref_candidates(name)
    assert cands[0] == "season2/loops/hypothesis-l4-branches-follow-th-a00-0b43f895"
    assert name in cands  # old name kept as the one-season fallback


def test_seat_merge_target_is_season_main():
    assert b.merge_target("seat/post-name@s2") == "season2/main"


def test_loop_alias_merge_target_is_season_main():
    assert b.merge_target("loop/opt-auth-a1@s2") == "season2/main"


# --- grid legal-branch predicate (hypothesis:l4-commit-all-is-legal-on-the-season-main-only) ---
# The predicate the 5-min grid cron's commit --all gate uses. commit --all runs
# unattended and writes the same ref namespace from any worktree, so it may only
# run on master or the season MAIN (canonical season<N>/main or its one-season
# alias season/s<N>). A post, loop or town name in EITHER spelling is refused.


def test_legal_branch_accepts_canonical_season_main():
    assert b.is_legal_branch("season2/main")


def test_legal_branch_refuses_canonical_post():
    assert not b.is_legal_branch("season2/posts/x")


def test_legal_branch_refuses_canonical_loop():
    assert not b.is_legal_branch("season2/loops/a-b")


def test_legal_branch_refuses_canonical_town_main():
    assert not b.is_legal_branch("season2/web-app-suite/season1/main")


def test_legal_branch_accepts_season_aliases():
    # season/s<N> and master must stay accepted for one season.
    assert b.is_legal_branch("season/s2")
    assert b.is_legal_branch("master")


def test_legal_branch_refuses_legacy_post_spelling():
    assert not b.is_legal_branch("seat/x@s2")


def test_legal_branch_refuses_legacy_loop_spelling():
    assert not b.is_legal_branch("loop/a-b@s2")


def test_legal_branch_refuses_legacy_town_spellings():
    assert not b.is_legal_branch("town/web-app-suite/season/s1")
    assert not b.is_legal_branch("town/x@s2")


def test_legal_branch_refuses_feature_branch():
    assert not b.is_legal_branch("feature/x")


def test_legal_branch_refuses_malformed_season_name():
    assert not b.is_legal_branch("season2/weird")


def test_legal_branch_refuses_detached_head():
    assert not b.is_legal_branch("")
    assert not b.is_legal_branch(None)


# --- L4.319: the post/<n>@sN INTERMEDIATE alias (hypothesis:
# l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts)
# The seat->post rename moves through `post/<name>@s<N>` before re-pointing
# onto the canonical `season<N>/posts/<name>`. parse() must resolve it like the
# seat alias (never raises); the reverse of a canonical post returns the
# INTERMEDIATE spelling by default, with the DEPRECATED seat/ spelling still
# reachable via legacy_seat for a reader of a pre-migration tree.

def test_post_at_alias_canonicalises_to_post():
    d = b.parse("post/foo@s2")
    assert d["kind"] == "alias"
    assert d["season"] == 2
    assert d["canonical"] == "season2/posts/foo"


def test_post_at_round_trips_through_canonical():
    # parse(post/<n>@s2) -> canonical season2/posts/<n>; the reverse of that
    # canonical yields the INTERMEDIATE spelling back.
    d = b.parse("post/foo@s2")
    assert b._canonical_to_old(d["canonical"]) == ["post/foo@s2"]
    assert b.ref_candidates(d["canonical"])[0] == "season2/posts/foo"


def test_post_at_reverse_keeps_legacy_seat_under_flag():
    # The DEPRECATED seat/<name>@s<N> spelling stays reachable for a reader of
    # a pre-migration tree (ref_candidates pins it); the intermediate post/
    # spelling is the new default.
    assert b._canonical_to_old("season2/posts/foo") == ["post/foo@s2"]
    assert b._canonical_to_old("season2/posts/foo", legacy_seat=True) == ["seat/foo@s2"]


def test_seat_alias_still_resolves_after_post_at_rule():
    # The adjacent seat/<name>@s<N> deprecated alias must keep resolving.
    d = b.parse("seat/foo@s2")
    assert d["kind"] == "alias"
    assert d["canonical"] == "season2/posts/foo"


def test_post_at_malformed_without_season_raises():
    # A `post/<n>` with no @s<N> is not claimed by the alias table — it must
    # still be refused (raise / not parse).
    with pytest.raises(ValueError):
        b.parse("post/foo")
    with pytest.raises(ValueError):
        b.parse("post/foo@s")


# --- goal:g15.25 lines (1)+(2) (SM.250): the mirror ref -------------------
def _mirror_fixture(tmp_path, branch="season2/posts/adv"):
    """A work repo ON `branch` with one commit and a bare origin. Returns
    (repo, bare)."""
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", "-b", branch, str(repo)], check=True)
    for k, v in (("user.email", "t@t"), ("user.name", "t")):
        subprocess.run(["git", "-C", str(repo), "config", k, v], check=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "i"],
                   check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                    str(bare)], check=True)
    return repo, bare


def _ls_remote(bare, pattern):
    """The sha list `git ls-remote <bare> <pattern>` reports."""
    out = subprocess.run(["git", "ls-remote", str(bare), pattern],
                         capture_output=True, text=True).stdout
    return [ln.split("\t")[0] for ln in out.splitlines() if ln.strip()]


def test_mirror_ref_shapes_and_branch_lookup():
    """`mirror_ref` returns `refs/agi/posts/<name>` and `refs/agi/loops/<name>`
    (goal:g15.25 (a)); `mirror_ref_for_branch` maps a post/loop branch to its
    mirror ref and every trunk to None; a bad kind refuses by name."""
    assert b.mirror_ref(2, "posts", "sanctuary-director") == \
        "refs/agi/posts/sanctuary-director"
    assert b.mirror_ref(2, "loops", "slug-a00") == "refs/agi/loops/slug-a00"
    assert b.mirror_ref_for_branch("season2/posts/adv") == \
        "refs/agi/posts/adv"
    assert b.mirror_ref_for_branch("season2/loops/l4-round-a00") == \
        "refs/agi/loops/l4-round-a00"
    assert b.mirror_ref_for_branch("season2/main") is None
    assert b.mirror_ref_for_branch("master") is None
    assert b.mirror_ref_for_branch("not a branch!!") is None
    with pytest.raises(ValueError):
        b.mirror_ref(2, "heads", "adv")


def test_mirror_ref_for_branch_resolves_v3_town_first_post_and_loop():
    """SM.25b defect (1): the TOWN-FIRST spellings every live seat carries
    parse to `v3_post`/`v3_loop`, which the helper must recognise exactly as
    it recognises the season-first arms. Pre-fix both returned None, so the
    mirror never resolved on the branches that matter and `merge-up --post`
    refused for every real seat. FALSIFIER: None for any live seat spelling."""
    assert b.parse("core/season2/posts/sanctuary-director/main")["kind"] \
        == "v3_post"
    assert b.parse(
        "core/season2/posts/sanctuary-director/loops/L4.332/a00-x")[
            "kind"] == "v3_loop"
    assert b.mirror_ref_for_branch(
        "core/season2/posts/sanctuary-director/main") == \
        "refs/agi/posts/sanctuary-director"
    assert b.mirror_ref_for_branch(
        "core/season2/posts/sanctuary-director/loops/L4.332/a00-x") == \
        "refs/agi/loops/L4.332-a00-x"
    # a v3 trunk still maps to no mirror (unchanged)
    assert b.mirror_ref_for_branch("core/season2/main") is None


def test_mirror_and_prove_is_additive_and_proves_by_ls_remote(tmp_path):
    """goal:g15.25 (c)+(f): the tip lands at `refs/agi/posts/<name>` on the
    bare origin, ls-remote proves the sha, and NO head is created. The helper
    is ADDITIVE -- its source never deletes and never forces."""
    import inspect
    repo, bare = _mirror_fixture(tmp_path)
    ref = b.mirror_ref_for_branch("season2/posts/adv")
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    ok, detail, info = b.mirror_and_prove(repo, ref)
    assert ok, detail
    assert info["ref"] == ref and info["sha"] == head
    assert info["proved_by"] == "ls-remote"
    assert _ls_remote(bare, ref) == [head]
    assert _ls_remote(bare, "refs/heads/season2/posts/*") == []
    src = inspect.getsource(b.mirror_and_prove)
    assert "--delete" not in src and "--force" not in src


def test_mirror_and_prove_refuses_by_name_on_failed_push(tmp_path):
    """goal:g15.25 (d): a receive that fails is a REFUSAL BY NAME (rc-gated),
    the ok flag is False, and nothing landed on origin."""
    repo, bare = _mirror_fixture(tmp_path)
    hook = bare / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    ref = b.mirror_ref_for_branch("season2/posts/adv")
    ok, detail, _info = b.mirror_and_prove(repo, ref)
    assert ok is False
    assert "refused" in detail and ref in detail
    assert _ls_remote(bare, ref) == []
    assert _ls_remote(bare, "refs/heads/season2/posts/*") == []


def test_no_engine_path_pushes_a_post_head():
    """goal:g15.25 (e): no engine source names a post branch as a pushed
    HEAD ref (`refs/heads/season<n>/posts/...`)."""
    bin_dir = Path(b.__file__).parent
    offenders = []
    for p in sorted(bin_dir.glob("*.py")):
        for i, line in enumerate(
                p.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue                      # a comment names it to refuse it
            if "refs/heads/season" in line and "posts" in line:
                offenders.append(f"{p.name}:{i}")
    assert not offenders, offenders
