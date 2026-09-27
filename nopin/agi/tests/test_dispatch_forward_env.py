"""hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ

The gap: `harnesses.<h>.env` is LITERALS ONLY and `dispatch.scrubbed_env` is
the DISPATCHER's environ. A post-session director round (a shell that never
`source`d the MAIN `.env`) therefore hands no `.env` key to a kid, even though
`TYPESAFE_KEY` sits in the MAIN root's `.env`.

`harnesses.<h>.forward_env: [NAMES]` closes it: names only, each read from the
MAIN-root `.env` at spawn by the ONE seam every adapter's `child_env` calls
(`adapters.forward_named_env`), so main dispatch AND adapter `restart` reach it.

What these guard:

  1. two listed names present in `.env` -> both reach the child env, from
     `.env`, through all three shipped adapters (one seam, not three);
  2. a listed name absent from `.env` -> spawn proceeds, exactly ONE notice
     names it -- never an exception, never a partial env;
  3. `forward_env` never REMOVES a key the dispatcher environ already passes
     (driver.sh-dispatched kids keep every key they get today);
  4. `harnesses.<h>.env` literals keep today's behaviour -- and win over a
     forwarded name, exactly as a literal already wins over `base`;
  5. a forwarded VALUE is redacted in `spawn.json` even when the NAME carries
     none of the KEY/TOKEN/SECRET/PASSWORD substrings -- the far half of the
     claim: registration with the scrubber, not the name shape;
  6. with the dispatcher shell never sourced (the named key absent from `base`)
     the listed name still reaches the child FROM `.env`.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import dispatch  # noqa: E402

#: Every shipped adapter funnels through the same `child_env` -> forwarding
#: seam, so the rule is proven for all three and not just pi.
ADAPTERS = ("pi", "claude_code", "copilot_cli")


@pytest.fixture(autouse=True)
def _clean_registry():
    """The scrubber registry is process-global; a test must not inherit one."""
    adapters._FORWARDED_NAMES.clear()
    yield
    adapters._FORWARDED_NAMES.clear()


def _env_file(tmp_path: Path, text: str) -> Path:
    p = tmp_path / ".env"
    p.write_text(text, encoding="utf-8")
    return p


@pytest.fixture
def main_env(tmp_path, monkeypatch):
    """The MAIN-root `.env` the forwarded names are read from."""
    p = _env_file(
        tmp_path,
        "# the two TypeSafe spellings the contract names\n"
        "TYPESAFE_KEY=ts-secret-value-1\n"
        "TYPESAFE_API_KEY=ts-secret-value-2\n",
    )
    monkeypatch.setattr(adapters, "_FORWARD_ENV_FILE", p)
    return p


@pytest.mark.parametrize("harness_name", ADAPTERS)
def test_two_listed_names_reach_the_child_and_values_are_redacted(
        harness_name, main_env, capsys):
    harness = {"adapter": harness_name,
               "forward_env": ["TYPESAFE_KEY", "TYPESAFE_API_KEY"]}
    env = adapters.load(harness_name).child_env(
        harness=harness, base={"PATH": "/bin"}, tier="kid")

    assert env["TYPESAFE_KEY"] == "ts-secret-value-1"
    assert env["TYPESAFE_API_KEY"] == "ts-secret-value-2"
    recorded = json.dumps(dispatch._redact_env_map(env))
    assert "ts-secret-value-1" not in recorded
    assert "ts-secret-value-2" not in recorded
    assert capsys.readouterr().err == ""  # both present: no notice


def test_absent_name_is_skipped_with_exactly_one_named_notice(
        tmp_path, monkeypatch, capsys):
    p = _env_file(tmp_path, "PRESENT_KEY=present-value\n")
    monkeypatch.setattr(adapters, "_FORWARD_ENV_FILE", p)
    harness = {"adapter": "pi",
               "forward_env": ["MISSING_KEY", "PRESENT_KEY"]}

    env = adapters.load("pi").child_env(harness=harness, base={}, tier="kid")

    assert env["PRESENT_KEY"] == "present-value"
    assert "MISSING_KEY" not in env
    err = capsys.readouterr().err
    assert err.count("MISSING_KEY") == 1 and "PRESENT_KEY" not in err


def test_forward_env_never_removes_a_key_the_environ_already_passes(main_env):
    base = {"TYPESAFE_KEY": "from-the-dispatcher-environ", "UNRELATED": "kept"}
    harness = {"adapter": "pi", "forward_env": ["TYPESAFE_KEY"]}

    env = adapters.load("pi").child_env(harness=harness, base=base, tier="kid")

    assert env["TYPESAFE_KEY"] == "from-the-dispatcher-environ"
    assert env["UNRELATED"] == "kept"


def test_harness_env_literal_still_merges_and_wins(main_env):
    harness = {"adapter": "pi",
               "env": {"LITERAL": "literal-value",
                       "TYPESAFE_KEY": "literal-wins"},
               "forward_env": ["TYPESAFE_KEY"]}

    env = adapters.load("pi").child_env(harness=harness, base={}, tier="kid")

    assert env["LITERAL"] == "literal-value"
    assert env["TYPESAFE_KEY"] == "literal-wins"


def test_no_forward_env_is_byte_identical_to_today(main_env):
    harness = {"adapter": "pi", "env": {"LITERAL": "literal-value"}}

    env = adapters.load("pi").child_env(harness=harness, base={"A": "b"}, tier="kid")

    assert env == {"A": "b", "LITERAL": "literal-value"}


def test_forwarded_value_redacted_even_when_the_name_is_not_secret_shaped(
        tmp_path, monkeypatch):
    p = _env_file(tmp_path, "PLAIN_SETTING=plain-value-abc\n")
    monkeypatch.setattr(adapters, "_FORWARD_ENV_FILE", p)
    harness = {"adapter": "pi", "forward_env": ["PLAIN_SETTING"]}

    env = adapters.load("pi").child_env(harness=harness, base={}, tier="kid")

    # The name/shape halves alone would NOT catch this one -- which is why the
    # value is registered with the scrubber by NAME at forward time.
    assert "PLAIN_SETTING" in adapters._FORWARDED_NAMES
    adapters._FORWARDED_NAMES.clear()
    try:
        assert dispatch._looks_like_secret(
            "PLAIN_SETTING", "plain-value-abc") is False
    finally:
        adapters._FORWARDED_NAMES.add("PLAIN_SETTING")
    assert "plain-value-abc" not in json.dumps(dispatch._redact_env_map(env))


def test_listed_name_reaches_the_child_when_the_shell_never_sourced_env(
        main_env):
    assert "TYPESAFE_KEY" not in os.environ  # the post-session shell
    harness = {"adapter": "pi", "forward_env": ["TYPESAFE_KEY"]}

    env = adapters.load("pi").child_env(harness=harness, base={}, tier="kid")

    assert env["TYPESAFE_KEY"] == "ts-secret-value-1"