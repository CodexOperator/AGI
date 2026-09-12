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
    # A POST's legacy spelling IS seat/<name>@s<n> (hypothesis:
    # l4-branches-follow-the-season-grammar a1) — canonical first, old name
    # kept as the one-season fallback, mirroring the loop branch case.
    assert b.ref_candidates("season2/posts/foo") == [
        "season2/posts/foo", "seat/foo@s2"
    ]


def test_ref_candidates_seat_alias_canonical_first():
    # Real seat branch name on this box (harvest-pinned): canonical first,
    # old `seat/...@s<n>` spelling kept. A reader handed the canonical POST
    # name on a pre-migration tree falls back to the live seat ref.
    name = "seat/sanctuary-director@s2"
    cands = b.ref_candidates(name)
    assert cands == ["season2/posts/sanctuary-director", name]
    # and the canonical-first direction resolves to the same pair
    assert b.ref_candidates("season2/posts/sanctuary-director") == [
        "season2/posts/sanctuary-director", name
    ]


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
