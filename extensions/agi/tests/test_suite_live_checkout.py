"""hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-to-
the-live-checkout-and-the-runner-basetemp-lives-under-tmp -- a g15 BUILD,
claims (1)+(3): the suite is refused by name when its basetemp resolves to
the live engine checkout, and the shared-state writers refuse under pytest
by name. Unit test per refusal site: the conftest gate predicate, the
verification.py --suite gate, and the three (3) writers.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import locations
import rotate
import send
import spawn_budget
import verification

#: The live engine checkout this conftest ships from -- the tree a suite may
#: never write (a basetemp inside it makes git-escaping writers hit LIVE).
LIVE = locations.git_common_root(Path(locations.__file__).resolve())


def _given_tmp(tmp_path):
    """A non-live given root (under /tmp), as the fixture roots are."""
    return tmp_path / "graph"


# --- claim (1): the conftest gate predicate --------------------------------


def test_conftest_gate_is_live_checkout(tmp_path):
    """The predicate the conftest session gate uses: a basetemp inside the
    engine checkout IS live; a /tmp basetemp under the interim rule is not."""
    assert locations.is_live_checkout(LIVE) is True
    assert locations.is_live_checkout(_given_tmp(tmp_path)) is False


def test_no_git_path_is_never_the_live_checkout(tmp_path):
    """The claim's dedicated no-repo predicate test: a path with NO enclosing
    git repo must read FALSE (never LIVE), while the real engine checkout
    reads True. Covers the regression that could label a gitless /tmp basetemp
    LIVE and trip the H2 refusal."""
    import tempfile
    gitless = Path(tempfile.mkdtemp())  # fresh dir under /tmp, no repo
    assert locations.is_live_checkout(gitless) is False
    assert locations.is_live_checkout(LIVE) is True


def test_no_git_path_is_false_even_when_the_resolver_returns_one_root(
        monkeypatch, tmp_path):
    """The no-repo rule is DECIDED, not coincidental (SM.80 re-open).

    `git_common_root` is annotated `-> Path` and every failure branch returns
    `root` unchanged, so SM.80's `g is not None and e is not None` could never
    be False. Here the resolver is pinned to a single value, so BOTH sides
    resolve equal -- exactly the shape SM.80's tautology read as LIVE. The
    predicate must still answer False for a path in no repository, because
    `_enclosing_repo` is None there. On SM.80's bytes this assertion FAILS
    (the identity fallback happened to differ; nothing decided it)."""
    monkeypatch.setattr(locations, "git_common_root", lambda p: LIVE)
    gitless = tmp_path / "no-repo"
    gitless.mkdir()
    assert locations.is_live_checkout(gitless) is False
    assert locations.is_live_checkout(LIVE) is True


def test_conftest_refusal_line_is_the_named_shared_line():
    """The SAME one-line refusal the conftest gate and verification --suite
    print: names both paths and the /tmp escape."""
    line = locations.live_checkout_refusal("/tmp/bt", LIVE)
    assert "refused: basetemp /tmp/bt resolves to the live checkout" in line
    assert str(LIVE) in line
    assert "pass --basetemp under /tmp" in line


# --- claim (1): the verification.py --suite gate ---------------------------


def test_verification_suite_refusal(capsys, tmp_path):
    """The --suite gate returns exit 3 with the named line on a live basetemp,
    and is silent under the real system-tmp prefix (the interim rule)."""
    assert verification._suite_basetemp_refusal(LIVE, base=LIVE) == 3
    assert "refused: basetemp" in capsys.readouterr().out
    assert verification._suite_basetemp_refusal(LIVE) is None


# --- claim (3): the three writers refuse live resolution by name -----------


def test_rotate_sessions_dir_refuses_live_resolution(tmp_path, monkeypatch):
    monkeypatch.setattr(locations, "shared_sessions_dir", lambda root: LIVE)
    with pytest.raises(RuntimeError, match="resolves to the live checkout"):
        rotate._sessions_dir(_given_tmp(tmp_path))


def test_send_comms_root_refuses_live_resolution(tmp_path, monkeypatch):
    monkeypatch.setattr(send, "_default_comms_root", lambda root: LIVE)
    with pytest.raises(RuntimeError, match="resolves to the live checkout"):
        send.comms_root(_given_tmp(tmp_path))


def test_posts_writer_refuses_live_resolution(tmp_path, monkeypatch):
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda root: LIVE)
    with pytest.raises(RuntimeError, match="resolves to the live checkout"):
        rotate._write_identity_cells(
            _given_tmp(tmp_path), seat="s", actor="a", role="r",
            cells={"pid": 1})


def test_refuse_live_resolution_is_noop_outside_pytest(tmp_path, monkeypatch):
    """Outside a pytest run the shared-room resolution to the main checkout is
    correct production behaviour -- never a refusal."""
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    locations.refuse_live_resolution(_given_tmp(tmp_path), LIVE)


# --- claim (3) ADDENDUM: the budget_dir resolver refuses live too -----------


def test_budget_dir_refuses_live_resolution(tmp_path, monkeypatch):
    """spawn_budget.budget_dir routes through git_common_root like the other
    writers; a given non-live root that resolves LIVE is refused by name."""
    monkeypatch.setattr(locations, "find_project_root",
                        lambda root: LIVE if root else None)
    with pytest.raises(RuntimeError, match="resolves to the live checkout"):
        spawn_budget.budget_dir(_given_tmp(tmp_path))


def test_locations_sibling_resolvers_refuse_live(tmp_path, monkeypatch):
    """The sibling resolvers in locations.py that route through git_common_root
    register behind the SAME is_live_checkout predicate -- one-line additions."""
    for fn in (locations.shared_sessions_dir, locations.shared_project_root):
        monkeypatch.setattr(locations, "find_project_root",
                            lambda root: LIVE)
        with pytest.raises(RuntimeError, match="resolves to the live checkout"):
            fn(_given_tmp(tmp_path))