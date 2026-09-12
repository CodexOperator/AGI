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
    ("seat/streaming-suite@s2", "season2/streaming-suite"),
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
    # season2/streaming-suite is a town node, not a leaf; alias still resolves.
    d = b.parse("seat/streaming-suite@s2")
    assert d["kind"] == "alias"
    assert d["canonical"] == "season2/streaming-suite"


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


def test_ref_candidates_post_no_legacy():
    # posts had no legacy spelling -> canonical alone
    assert b.ref_candidates("season2/posts/foo") == ["season2/posts/foo"]


class _Sink:
    def __init__(self, target):
        self.target = target

    def write(self, s):
        self.target.append(s)
