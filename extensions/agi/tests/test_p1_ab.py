"""goal:g7.16.1.11.46.9 (P1) -- the pi1 cell, the pin, the capped mint, the spawn gate, the board line.

No test mints for real: `provisioning._call` and `_read_provisioning_key` are mocked (the project-wide guard).
"""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import p1_ab  # noqa: E402
import provisioning  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CFG = json.loads((ROOT / ".agi" / "config.json").read_text())
PIN = CFG["p1"]["pin"]


# --- the cell ----------------------------------------------------------------

def test_the_p1_cell_carries_the_council_numbers():
    p = CFG["p1"]
    assert (p["leaves"], p["key_cap_usd"], p["cash_total_usd"], p["max_live"], p["slice_gb_max"]) == (10, 0.5, 10.0, 2, 5.0)
    assert p["arm_cap_usd"] == {"glm": 5.0, "deepseek": 5.0, "credits": 5.0}
    assert PIN["package"] == "@earendil-works/pi-coding-agent" and PIN["version"] == "1.4.0"
    assert PIN["integrity"].startswith("sha512-")


def test_pi1_is_a_harness_whose_bin_is_the_side_prefix_and_not_the_old_pi(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("PI_BIN", raising=False)
    fake = tmp_path / "pi1" / "node_modules" / ".bin" / "pi"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    for name, model in (("pi1", "z-ai/glm-5.3-flash"), ("pi1:glm", "z-ai/glm-5.3-flash"),
                        ("pi1:deepseek", "deepseek/deepseek-v4.1-flash-1017"), ("pi1:credits", "claude-haiku-5-5")):
        h = adapters.harness_block(CFG, name)
        assert h and h["models"]["kid"] == model, name
        assert h["bin"] == "~/pi1/node_modules/.bin/pi"
        assert adapters.resolve_bin(h, "PI_BIN", "pi") == str(fake)
    assert adapters.harness_block(CFG, "pi1:credits")["provider"] == "anthropic"
    # the old cell is not the new one
    assert adapters.harness_block(CFG, "pi")["bin"] != adapters.harness_block(CFG, "pi1")["bin"]


# --- the pin -----------------------------------------------------------------

def _prefix(tmp_path, *, version=PIN["version"], integrity=PIN["integrity"], installed=PIN["version"]):
    pre = tmp_path / "pi1"
    pkg = pre / "node_modules" / PIN["package"]
    pkg.mkdir(parents=True)
    (pkg / "package.json").write_text(json.dumps({"version": installed}))
    (pre / "package-lock.json").write_text(json.dumps({"packages": {
        f"node_modules/{PIN['package']}": {"version": version, "integrity": integrity}}}))
    return pre


def test_the_pin_holds_for_the_pinned_version_and_integrity(tmp_path):
    assert p1_ab.check_pin(_prefix(tmp_path), CFG) == []


@pytest.mark.parametrize("kw", [{"integrity": "sha512-AAAA"}, {"version": "1.4.1"}, {"installed": "1.3.0"}])
def test_the_pin_is_red_for_a_swapped_tarball_or_version(tmp_path, kw):
    assert p1_ab.check_pin(_prefix(tmp_path, **kw), CFG)


def test_the_pin_is_red_for_an_absent_prefix(tmp_path):
    assert p1_ab.check_pin(tmp_path / "nope", CFG)


@pytest.mark.skipif(not (Path.home() / "pi1" / "package-lock.json").exists(), reason="no side prefix in this home")
def test_this_homes_side_prefix_holds_the_pin():
    assert p1_ab.check_pin("~/pi1", CFG) == []


@pytest.mark.skipif(not os.path.exists("/usr/local/bin/pi"), reason="no old pi on this box")
def test_the_old_pi_is_untouched():
    """Falsifier 3, negative: /usr/local/bin/pi still resolves into 0.73.1 and prints it."""
    assert p1_ab.old_pi_untouched() == []


def test_old_pi_check_is_red_for_a_pi_that_is_not_0_73_1(tmp_path):
    fake = tmp_path / "pi"
    fake.write_text("#!/bin/sh\necho 1.4.0\n")
    fake.chmod(0o755)
    problems = p1_ab.old_pi_untouched(str(fake))
    assert len(problems) == 2 and any("1.4.0" in x for x in problems)


# --- the capped mint ---------------------------------------------------------

class Api:
    """A mocked provisioning API: records what was sent, lists what it 'stored'."""

    def __init__(self, monkeypatch, *, stored_limit="echo"):
        self.sent, self.revoked, self.rows = [], [], []
        self.stored_limit = stored_limit
        monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda root=None: "sk-prov")
        monkeypatch.setattr(provisioning, "_call", self.call)
        monkeypatch.setattr(provisioning, "can_fund", lambda root=None, **k: (True, None))
        monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: list(self.rows))

    def call(self, method, url, key, payload=None, timeout=30):
        if method == "DELETE":
            self.revoked.append(url.rsplit("/", 1)[-1])
            return 200, {}
        self.sent.append(payload)
        h = f"h{len(self.sent)}"
        lim = payload["limit"] if self.stored_limit == "echo" else self.stored_limit
        self.rows.append({"hash": h, "limit": lim, "usage": 0})
        return 201, {"key": f"sk-{h}", "data": {"hash": h, "expires_at": "2099-01-01T00:00:00Z"}}


def test_a_mint_sends_the_cap_reads_it_back_and_writes_the_ledger(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "led.json"
    k = p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=led)
    assert api.sent[0]["limit"] == 0.5 and k.secret == "sk-h1"
    assert json.loads(led.read_text()) == [{"arm": "glm", "leaf": 1, "hash": "h1", "cap": 0.5}]


@pytest.mark.parametrize("bad", [0, -1, float("inf"), float("nan"), 0.51, 5, True, "0.5"])
def test_a_key_without_a_finite_cap_in_range_is_refused_before_any_call(monkeypatch, tmp_path, bad):
    api = Api(monkeypatch)
    with pytest.raises(p1_ab.P1Refused, match="refused at mint"):
        p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=tmp_path / "l.json", limit_usd=bad)
    assert api.sent == []


@pytest.mark.parametrize("stored", [None, 5.0, 0.51])
def test_an_uncapped_or_over_cap_key_on_read_back_is_revoked_and_refused(monkeypatch, tmp_path, stored):
    """The API ignoring the cap is the failure the read-back exists for (a 201 that lied)."""
    api = Api(monkeypatch, stored_limit=stored)
    led = tmp_path / "l.json"
    with pytest.raises(p1_ab.P1Refused, match="read back"):
        p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=led)
    assert api.revoked == ["h1"] and not led.exists()


def test_a_key_that_is_missing_from_the_listing_is_refused_too(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: [])
    with pytest.raises(p1_ab.P1Refused, match="read back"):
        p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=tmp_path / "l.json")
    assert api.revoked == ["h1"]


def test_a_leaf_never_mints_twice_a_capped_kid_is_a_red_not_a_retry(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    p1_ab.mint_capped(arm="glm", leaf=3, cfg=CFG, ledger=led)
    with pytest.raises(p1_ab.P1Refused, match="never retried"):
        p1_ab.mint_capped(arm="glm", leaf=3, cfg=CFG, ledger=led)
    assert len(api.sent) == 1
    p1_ab.mint_capped(arm="deepseek", leaf=3, cfg=CFG, ledger=led)     # another arm, same leaf: the pair
    assert len(api.sent) == 2


def test_ten_leaves_fill_an_arm_to_exactly_its_cap_and_no_key_passes_it(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    for leaf in range(1, 11):
        p1_ab.mint_capped(arm="glm", leaf=leaf, cfg=CFG, ledger=led)
    assert p1_ab.exposure(json.loads(led.read_text()), "glm") == 5.0
    with pytest.raises(p1_ab.P1Refused, match="leaf"):
        p1_ab.mint_capped(arm="glm", leaf=11, cfg=CFG, ledger=led)
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["arm_cap_usd"]["glm"] = 4.9
    led2 = tmp_path / "l2.json"
    for leaf in range(1, 10):
        p1_ab.mint_capped(arm="glm", leaf=leaf, cfg=cfg, ledger=led2)
    with pytest.raises(p1_ab.P1Refused, match="arm cap"):
        p1_ab.mint_capped(arm="glm", leaf=10, cfg=cfg, ledger=led2)


def test_the_cash_total_binds_across_the_two_openrouter_arms(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["cash_total_usd"] = 1.0
    led = tmp_path / "l.json"
    p1_ab.mint_capped(arm="glm", leaf=1, cfg=cfg, ledger=led)
    p1_ab.mint_capped(arm="deepseek", leaf=1, cfg=cfg, ledger=led)
    with pytest.raises(p1_ab.P1Refused, match="cash"):
        p1_ab.mint_capped(arm="glm", leaf=2, cfg=cfg, ledger=led)
    assert len(api.sent) == 2


def test_the_credits_arm_mints_no_openrouter_key(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    with pytest.raises(p1_ab.P1Refused, match="org link"):
        p1_ab.mint_capped(arm="credits", leaf=1, cfg=CFG, ledger=tmp_path / "l.json")
    assert api.sent == []


def test_no_provisioning_key_mints_nothing_and_does_not_fall_back(monkeypatch, tmp_path):
    monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda root=None: None)
    with pytest.raises(p1_ab.P1Refused, match="no provisioning key"):
        p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=tmp_path / "l.json")


def test_an_unreadable_ledger_stops_minting(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    led.write_text("{not json")
    with pytest.raises(p1_ab.P1Refused, match="unreadable"):
        p1_ab.mint_capped(arm="glm", leaf=1, cfg=CFG, ledger=led)
    assert api.sent == []


# --- the spawn gate and the board --------------------------------------------

@pytest.mark.parametrize("live,gb,ok", [(0, 4.99, True), (1, 5.0, True), (2, 1.0, False), (0, 5.01, False), (0, None, False)])
def test_may_start(live, gb, ok):
    assert p1_ab.may_start(live, gb, CFG)[0] is ok


def test_slice_gb_reads_bytes_and_fails_closed(tmp_path):
    f = tmp_path / "m"
    f.write_text("5340000000\n")
    assert p1_ab.slice_gb(str(f)) == pytest.approx(5.34)
    assert p1_ab.slice_gb(str(tmp_path / "gone")) is None
    f.write_text("max\n")
    assert p1_ab.slice_gb(str(f)) is None


def test_board_line_four_numbers_and_the_zero_landed_case():
    kids = [{"landed": True, "usd": 0.10, "secs": 100, "red": False}] * 4 + \
           [{"landed": False, "usd": 0.20, "secs": 60, "red": True}] * 2 + \
           [{"landed": True, "usd": 0.0, "secs": 0, "red": False}] * 4
    assert p1_ab.board_line("z-ai/glm-5.3-flash", kids) == "p1 z-ai/glm-5.3-flash $/landed=0.1000 s/landed=65 red=2/10"
    none = [{"landed": False, "usd": 0.3, "secs": 9, "red": True}] * 10
    assert p1_ab.board_line("m", none) == "p1 m $/landed=n/a s/landed=n/a red=10/10"
    assert p1_ab.board_line("m", none).startswith("p1 ")
