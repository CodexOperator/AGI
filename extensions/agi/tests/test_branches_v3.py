import pytest

import branches as b


# --- L4.332 (hypothesis:
# l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-
# reaches-origin) — v3 TOWN-FIRST grammar, ADDED alongside the live season-first
# spellings. The live tree is NOT renamed this round: parse/ref_candidates keep
# resolving season-first, and v3 names are added beside them (test (e)). The
# remote-visibility predicate and the builder share one set of trunk shapes.


# --- (a) the ONE tuple derives EXACTLY the four v3 names ---

def test_derive_names_full_tuple():
    assert b.derive_names("core", 2, "sanctuary-director", "L4.332", "a00-x") == {
        "town_main": "core/main",
        "town_season_main": "core/season2/main",
        "post_main": "core/season2/posts/sanctuary-director/main",
        "loop": "core/season2/posts/sanctuary-director/loops/L4.332/a00-x",
    }


# --- (b) partial inputs: a key is PRESENT only when its inputs are ---

def test_derive_names_partial_inputs():
    two = b.derive_names("core", 2)
    assert set(two) == {"town_main", "town_season_main"}
    assert two["town_main"] == "core/main"
    assert two["town_season_main"] == "core/season2/main"

    three = b.derive_names("core", 2, post="p")
    assert set(three) == {"town_main", "town_season_main", "post_main"}
    assert three["post_main"] == "core/season2/posts/p/main"
    # post given but no round/agent -> NO loop key
    assert "loop" not in three


def test_derive_names_loop_requires_round_and_agent():
    with_r = b.derive_names("core", 2, "p", "L4.332")
    assert "loop" not in with_r
    with_a = b.derive_names("core", 2, "p", None, "a00-x")
    assert "loop" not in with_a
    full = b.derive_names("core", 2, "p", "L4.332", "a00-x")
    assert full["loop"] == "core/season2/posts/p/loops/L4.332/a00-x"


def test_derive_names_reserved_town_raises():
    for leaf in ("main", "posts", "loops"):
        with pytest.raises(ValueError):
            b.derive_names(leaf, 2)


def test_derive_names_town_season_int_ge1():
    with pytest.raises(ValueError):
        b.derive_names("core", 0)
    with pytest.raises(ValueError):
        b.derive_names("core", -1)
    with pytest.raises(ValueError):
        b.derive_names("core", "2")


# --- (c) is_remote_visible: EXACTLY the trunk-pair-per-level shapes ---

REMOTE_VISIBLE = [
    "master",
    "season1/main",
    "season2/main",
    "core/main",
    "core/season2/main",
]

NOT_REMOTE_VISIBLE = [
    "core/season2/posts/x/main",
    "core/season2/posts/x/loops/L4.332/a00-x",
    "season2/posts/x",
    "season2/loops/x-a",
    "core",                        # bare town is NOT a ref (git forbids leaf+dir)
    "posts/main",                  # reserved leaf is never a town
    "main/main",
    "season/s2",                   # one-season alias spelling, not a v3 trunk ref
    "feature/x",
    "",
]


@pytest.mark.parametrize("name", REMOTE_VISIBLE)
def test_is_remote_visible_true(name):
    assert b.is_remote_visible(name) is True


@pytest.mark.parametrize("name", NOT_REMOTE_VISIBLE)
def test_is_remote_visible_false(name):
    assert b.is_remote_visible(name) is False


def test_is_remote_visible_never_raises_on_garbage():
    # Returning False for a name that does not parse is correct and must not
    # raise — including a non-string.
    for name in ("garbage", None, 42, "season2/bogus/x/y"):
        assert b.is_remote_visible(name) is False


# --- (d) assert_remote_visible: refusal by name ---

def test_assert_remote_visible_refuses_and_names_branch():
    with pytest.raises(ValueError) as ei:
        b.assert_remote_visible("core/season2/posts/x/main")
    assert "core/season2/posts/x/main" in str(ei.value)


def test_assert_remote_visible_ok_returns_none():
    assert b.assert_remote_visible("core/season2/main") is None
    assert b.assert_remote_visible("master") is None
    assert b.assert_remote_visible("season2/main") is None


# --- (e) REGRESSION: the existing season-first spellings still resolve, and
# ref_candidates is still current-name-first. v3 ADDS alongside; a reader must
# keep resolving both (copied from the existing suite rather than trusted). ---

def test_regression_season_first_still_parses():
    assert b.parse("season2/main")["kind"] == "main"
    assert b.parse("season2/core/season1/main")["kind"] == "town_main"
    assert b.parse("season2/posts/foo")["kind"] == "post"
    assert b.parse("season2/loops/a-b")["kind"] == "loop"
    assert b.parse("season/s2")["canonical"] == "season2/main"
    assert b.parse("seat/foo@s2")["canonical"] == "season2/posts/foo"


def test_regression_ref_candidates_current_name_first():
    assert b.ref_candidates("season2/main") == ["season2/main", "season/s2"]
    assert b.ref_candidates("season2/posts/foo") == [
        "season2/posts/foo", "post/foo@s2", "seat/foo@s2"]
    assert b.ref_candidates("season/s2") == ["season2/main", "season/s2"]
    # a season-first town main keeps its own candidates (live tree not renamed)
    assert b.ref_candidates("season2/core/season1/main") == [
        "season2/core/season1/main", "town/core/season/s1", "town/core@s2"]


# --- MEASURED CONTRADICTION, documented not papered over. ---
# The live SEASON-FIRST town main `season<n>/<town>/season<k>/main` is a real
# trunk leaf (token set A: a town's Council main — parse() kind == "town_main",
# is_legal_branch's own suite refuses it only because commit-all must run on
# master/season-main). Yet the v3 remote-visibility predicate as specced
# returns False for it: v3 spells the town trunk TOWN-FIRST (<town>/main,
# <town>/season<m>/main). This round ADDS v3 alongside WITHOUT renaming the
# live tree, so a season-first town main still resolves via parse/ref_candidates
# but is_remote_visible refuses it by name. Carrying the live tree onto the v3
# spelling is the rename work of a later slice/round, not this one.

def test_measured_contradiction_season_first_town_main_vs_v3_remote():
    assert b.parse("season2/core/season1/main")["kind"] == "town_main"
    assert b.is_remote_visible("season2/core/season1/main") is False

# --- (f) ref_candidates resolves the v3 TOWN-FIRST names (region D section 1).
# The ONE resolver must not strand a reader handed a v3 name: alongside the
# as-written v3 spelling it must ALSO try the season-first spelling(s) the
# live (not-yet-renamed) tree still carries, then each of THEIR one-season
# aliases. hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-
# the-trunk-pair-per-level-reaches-origin. EVERY existing season-first input
# stays byte-identical (test_regression_ref_candidates_current_name_first
# above pins core rows; the parametrized season-first rows in test_branches.py
# pin the rest). ---

def test_v3_ref_candidates_town_season_main_falls_back_season_first():
    # core/season2/main -> v3 as-written first, then the season-first town
    # main (the tuple's ONE season fills both parent and town season), then
    # that town main's one-season alias.
    assert b.parse("core/season2/main")["kind"] == "v3_town_season_main"
    assert b.ref_candidates("core/season2/main") == [
        "core/season2/main",
        "season2/core/season2/main",
        "town/core/season/s2",
    ]


def test_v3_ref_candidates_post_falls_back_season_first():
    # core/season2/posts/p/main -> v3 as-written, then the season-level post
    # (the v3 town qualifier drops in the season-first old world), then its
    # intermediate and deprecated aliases.
    assert b.parse("core/season2/posts/p/main")["kind"] == "v3_post"
    assert b.ref_candidates("core/season2/posts/p/main") == [
        "core/season2/posts/p/main",
        "season2/posts/p",
        "post/p@s2",
        "seat/p@s2",
    ]


def test_v3_ref_candidates_loop_falls_back_season_first():
    # round and agent travel as separate v3 segments and rejoin with a dash
    # in the season-first loop spelling.
    assert b.parse("core/season2/posts/p/loops/L4.332/a00-x")["kind"] == "v3_loop"
    assert b.ref_candidates("core/season2/posts/p/loops/L4.332/a00-x") == [
        "core/season2/posts/p/loops/L4.332/a00-x",
        "season2/loops/L4.332-a00-x",
        "loop/L4.332-a00-x@s2",
    ]


def test_v3_ref_candidates_bare_town_main_no_season_no_fallback():
    # A bare <town>/main carries NO season number; ref_candidates must NOT
    # invent one. It resolves to the v3 spelling alone (which is_remote_visible
    # honours), and the season-first fallback is empty by design. This is the
    # derived-and-documented answer: guessing a parent/town season would be a
    # guess, and no live season-first branch is implied by a season-less name.
    assert b.parse("core/main")["kind"] == "v3_town_main"
    assert b.ref_candidates("core/main") == ["core/main"]


def test_v3_ref_candidates_as_written_always_first_and_deduped():
    for v3 in ("core/season2/main",
               "core/season2/posts/p/main",
               "core/season2/posts/p/loops/L4.332/a00-x"):
        cands = b.ref_candidates(v3)
        assert cands[0] == v3
        assert len(cands) == len(set(cands))


def test_v3_ref_candidates_cross_checked_by_is_remote_visible():
    # Every candidate a reader would PUSH must be honestly classified: the v3
    # trunk pair (core/main, core/season2/main) and the season-first town main
    # it falls back to are remote-visible TRUE; the post/loop spellings FALSE.
    assert b.is_remote_visible("core/main") is True
    assert b.is_remote_visible("core/season2/main") is True
    # a season-first town main is NOT remote-visible under the v3 ruling — the
    # measured contradiction pinned above — so its candidate row must say so,
    # never paper it over as if it were the v3 trunk.
    assert b.is_remote_visible("season2/core/season2/main") is False
    assert b.is_remote_visible("season2/posts/p") is False
    for cand in b.ref_candidates("core/season2/posts/p/main"):
        assert ("season2/posts/p" in cand) == (b.is_remote_visible(cand) is False) \
            or b.is_remote_visible(cand) is False
