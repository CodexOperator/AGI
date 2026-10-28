"""goal:g1.43.2 -- conftest's ONE autouse throwaway git identity.

Under a hermetic line (GIT_CONFIG_GLOBAL=/dev/null, no GIT_AUTHOR_*) a fixture
that commits without user.name/user.email commits as the throwaway identity;
with the four vars removed -- the fixture dropped, or a test of the
missing-identity path, which must delenv them itself -- the same commit is
refused by git ('no email was given and auto-detection is disabled'). Council [decision] alive
07:42:34Z 10-28 (676f5d177e).
"""
import os
import subprocess

#: the four vars tests/conftest.py's _throwaway_git_identity sets (its
#: THROWAWAY_GIT_IDENTITY; the module name `conftest` resolves to extensions/agi/conftest.py here)
IDENTITY_VARS = ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL")


def _commit(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.delenv("EMAIL", raising=False)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return subprocess.run(["git", "-C", str(tmp_path), "-c", "commit.gpgsign=false",
                           "-c", "user.useConfigOnly=true",   # no guess from the host name: env or nothing
                           "commit", "-q", "--allow-empty", "-m", "x"],
                          capture_output=True, text=True)


def test_a_fixture_commit_with_no_identity_anywhere_lands_as_the_throwaway(tmp_path, monkeypatch):
    r = _commit(tmp_path, monkeypatch)
    assert r.returncode == 0, r.stderr
    who = subprocess.run(["git", "-C", str(tmp_path), "log", "-1", "--format=%an <%ae> %cn <%ce>"],
                         capture_output=True, text=True).stdout.strip()
    i = os.environ
    assert i["GIT_AUTHOR_NAME"] == "agi-test", "the autouse fixture is not in effect"
    assert who == (f"{i['GIT_AUTHOR_NAME']} <{i['GIT_AUTHOR_EMAIL']}> "
                   f"{i['GIT_COMMITTER_NAME']} <{i['GIT_COMMITTER_EMAIL']}>")


def test_mutant_the_fixture_dropped_the_commit_is_refused_RED(tmp_path, monkeypatch):
    """The drop-it mutant, and the shape a missing-identity test must take:
    delenv the four, and git refuses the commit by name."""
    for k in IDENTITY_VARS:
        monkeypatch.delenv(k, raising=False)
    r = _commit(tmp_path, monkeypatch)
    assert r.returncode != 0
    assert "auto-detection is disabled" in r.stderr, r.stderr
