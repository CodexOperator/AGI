"""goal:g7.16.1.11.46.9 (P1) -- the pi1 cell, the pin and the sealed tree, the capped mint, the key files, the arm's
refusals, the spawn gate, the results segment.

No test mints for real: `provisioning._call` and `_read_provisioning_key` are mocked (the project-wide guard).
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import p1_ab  # noqa: E402
import provisioning  # noqa: E402
import success_metrics  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CFG = json.loads((ROOT / ".agi" / "config.json").read_text())
PIN = CFG["p1"]["pin"]
LEAVES = CFG["p1"]["leaves"]
NODE = ROOT / ".agi" / "nodes" / "goal" / "g7.16.1.11.46.9.md"
needs_acl = pytest.mark.skipif(shutil.which("setfacl") is None or shutil.which("getfacl") is None,
                               reason="no setfacl/getfacl on this box")


# --- the cell: ONE source for the leaves --------------------------------------

def test_the_p1_cell_carries_the_council_numbers():
    p = CFG["p1"]
    assert (p["key_cap_usd"], p["cash_total_usd"], p["max_live"], p["slice_gb_max"]) == (0.5, 10.0, 2, 5.0)
    assert p["arm_cap_usd"] == {"glm": 5.0, "deepseek": 5.0, "credits": 5.0}
    assert p["arm_order"] == ["deepseek", "glm", "credits"]
    assert PIN["package"] == "@earendil-works/pi-coding-agent" and PIN["version"] == "1.4.0"
    assert PIN["integrity"].startswith("sha512-")
    assert len(LEAVES) == 5 and len(set(LEAVES)) == 5 and len(p["base"]) == 40


def test_the_cell_equals_the_nodes_frozen_list_and_base():
    """A test reads .46.9 itself: the cell and the node agree, or the trunk is red."""
    assert p1_ab.frozen_problems(CFG, NODE.read_text()) == []


def test_a_cell_that_differs_from_the_node_reads_red():
    text = NODE.read_text()
    swapped = copy.deepcopy(CFG)
    swapped["p1"]["leaves"] = LEAVES[:-1] + ["goal:g1.1"]
    assert any("frozen list" in x for x in p1_ab.frozen_problems(swapped, text))
    reordered = copy.deepcopy(CFG)
    reordered["p1"]["leaves"] = list(reversed(LEAVES))
    assert p1_ab.frozen_problems(reordered, text)
    rebased = copy.deepcopy(CFG)
    rebased["p1"]["base"] = "0" * 40
    assert any("frozen base" in x for x in p1_ab.frozen_problems(rebased, text))
    assert any("no `FROZEN BASE" in x for x in p1_ab.frozen_problems(CFG, text.replace("FROZEN BASE", "OTHER BASE")))
    assert any("no `FROZEN LIST" in x for x in p1_ab.frozen_problems(CFG, text.replace("FROZEN LIST", "OTHER LIST")))


def test_leaves_refuses_a_count_or_a_bad_list():
    for bad in (10, [], ["g4.21"], "goal:g4.21"):
        cfg = copy.deepcopy(CFG)
        cfg["p1"]["leaves"] = bad
        with pytest.raises(p1_ab.P1Refused, match="leaves"):
            p1_ab.leaves(cfg)


# --- the harness cell: no implicit paid row -------------------------------------

def test_pi1_names_no_default_row_so_a_bare_pi1_resolves_to_nothing():
    """P2-b: a spawn naming pi1 without a row must not land on a paid OpenRouter arm outside the caps."""
    assert not any(r.get("default") for r in CFG["harnesses"]["pi1"]["rows"])
    assert adapters.harness_block(CFG, "pi1") == {}
    with pytest.raises(adapters.AdapterError):
        adapters.resolve(CFG, "pi1")


def test_the_default_row_mutant_would_land_on_a_paid_arm():
    """The mutant (a default row restored) resolves bare pi1 to a paid model: the test above is what goes red."""
    mutant = copy.deepcopy(CFG)
    mutant["harnesses"]["pi1"]["rows"][0]["default"] = True
    assert adapters.harness_block(mutant, "pi1")["models"]["kid"] == "z-ai/glm-5.3-flash"


def test_pi1_rows_resolve_by_name_to_the_side_prefix_and_not_the_old_pi(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("PI_BIN", raising=False)
    fake = tmp_path / "pi1" / "node_modules" / ".bin" / "pi"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    for name, model in (("pi1:glm", "z-ai/glm-5.3-flash"), ("pi1:deepseek", "deepseek/deepseek-v4.1-flash-1017"),
                        ("pi1:credits", "claude-haiku-5-5")):
        h = adapters.harness_block(CFG, name)
        assert h and h["models"]["kid"] == model, name
        assert h["bin"] == "~/pi1/node_modules/.bin/pi"
        assert adapters.resolve_bin(h, "PI_BIN", "pi") == str(fake)
    assert adapters.harness_block(CFG, "pi1:credits")["provider"] == "anthropic"
    assert adapters.harness_block(CFG, "pi")["bin"] != adapters.harness_block(CFG, "pi1:glm")["bin"]


# --- the pin and the sealed tree ----------------------------------------------------

def _prefix(tmp_path, *, version=PIN["version"], integrity=PIN["integrity"], installed=PIN["version"]):
    pre = tmp_path / "pi1"
    pkg = pre / "node_modules" / PIN["package"]
    pkg.mkdir(parents=True)
    (pkg / "package.json").write_text(json.dumps({"version": installed}))
    (pkg / "cli.js").write_text("console.log('pi')\n")
    (pre / "node_modules" / ".bin").mkdir()
    os.symlink("../" + PIN["package"] + "/cli.js", pre / "node_modules" / ".bin" / "pi")
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


def test_a_sealed_tree_holds_and_one_changed_byte_makes_it_red(tmp_path):
    pre = _prefix(tmp_path)
    p1_ab.seal(pre, CFG)
    assert p1_ab.check_tree(pre) == []
    js = pre / "node_modules" / PIN["package"] / "cli.js"
    js.write_text("console.log('pi')\n ")            # one byte appended
    assert any("install changed" in x for x in p1_ab.check_tree(pre))
    js.write_text("console.log('pi')\n")
    assert p1_ab.check_tree(pre) == []                # restored bytes read green again
    (pre / "node_modules" / "extra.js").write_text("x")  # a planted file
    assert p1_ab.check_tree(pre)


def test_a_retargeted_link_changes_the_tree(tmp_path):
    pre = _prefix(tmp_path)
    p1_ab.seal(pre, CFG)
    link = pre / "node_modules" / ".bin" / "pi"
    link.unlink()
    os.symlink("../elsewhere.js", link)
    assert p1_ab.check_tree(pre)


def test_an_unsealed_prefix_is_a_problem_and_seal_refuses_a_prefix_without_the_pin(tmp_path):
    pre = _prefix(tmp_path)
    assert any("not sealed" in x for x in p1_ab.check_tree(pre))
    bad = _prefix(tmp_path / "bad", integrity="sha512-AAAA")
    with pytest.raises(p1_ab.P1Refused, match="does not hold the pin"):
        p1_ab.seal(bad, CFG)


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


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads everything")
def test_main_env_denied_is_green_for_an_unreadable_file_and_red_for_a_readable_one(tmp_path):
    env = tmp_path / ".env"
    env.write_text("OPENROUTER_PROVISIONING_KEY=x\n")
    env.chmod(0o000)
    assert p1_ab.main_env_denied(env) == []
    env.chmod(0o600)
    assert any("READABLE" in x for x in p1_ab.main_env_denied(env))
    assert any("not the EACCES" in x for x in p1_ab.main_env_denied(tmp_path / "gone"))


# --- the capped mint ---------------------------------------------------------------

class Api:
    """A mocked provisioning API: records what was sent, lists what it 'stored'."""

    def __init__(self, monkeypatch, *, stored_limit="echo", stored_expiry="echo", sent_expiry="echo", secret=None):
        self.sent, self.revoked, self.rows, self.patched = [], [], [], []
        self.gets, self.keys_status, self.workspaces = [], 200, None      # workspaces: None = a 403 on the listing
        self.secret = secret
        self.stored_limit, self.stored_expiry, self.sent_expiry = stored_limit, stored_expiry, sent_expiry
        monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda root=None: "sk-prov")
        monkeypatch.setattr(provisioning, "_call", self.call)
        monkeypatch.setattr(provisioning, "can_fund", lambda root=None, **k: (True, None))
        monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: list(self.rows))

    def call(self, method, url, key, payload=None, timeout=30):
        if method == "DELETE":
            self.revoked.append(url.rsplit("/", 1)[-1])
            return 200, {}
        if method == "GET" and "/keys/" in url:                       # GET /keys/<hash>: the key by hash, any workspace
            h = url.rsplit("/", 1)[-1]
            row = next((r for r in self.rows if r["hash"] == h), None)
            return (200, {"data": dict(row)}) if row is not None else (404, {"error": "no such key"})
        if method == "GET":
            self.gets.append(url)
            if url.endswith("/workspaces"):
                return (200, {"data": [{"id": w} for w in self.workspaces]}) if self.workspaces is not None else (403, {})
            return self.keys_status, {}
        if method == "PATCH":
            h = url.rsplit("/", 1)[-1]
            self.patched.append(h)
            for r in self.rows:
                if r["hash"] == h and payload.get("disabled") is True and self.stored_limit != "ignore-disable":
                    r["disabled"] = True
            return 200, {}
        self.sent.append(payload)
        h = f"h{len(self.sent)}"
        lim = payload["limit"] if self.stored_limit in ("echo", "ignore-disable") else self.stored_limit
        exp = payload["expires_at"] if self.stored_expiry == "echo" else self.stored_expiry
        got = payload["expires_at"] if self.sent_expiry == "echo" else self.sent_expiry
        self.rows.append({"hash": h, "limit": lim, "usage": 0, "expires_at": exp, "disabled": False})
        return 201, {"key": self.secret or f"sk-{h}", "data": {"hash": h, "expires_at": got}}


def test_a_mint_sends_the_cap_reads_it_back_and_writes_the_ledger(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "led.json"
    k = p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led)
    assert api.sent[0]["limit"] == 0.5 and k.secret == "sk-h1"
    assert json.loads(led.read_text()) == [{"arm": "glm", "leaf": LEAVES[0], "hash": "h1", "cap": 0.5}]


def test_p0g_a_workspace_of_another_account_is_red_and_nothing_is_minted(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    api.workspaces = ["ws-mine"]                                   # the key's account owns ONLY ws-mine
    with pytest.raises(p1_ab.P1Refused, match="workspace preflight RED.*not one of"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "led.json", workspace_id="ws-other-account")
    assert api.sent == [] and not (tmp_path / "led.json").exists()
    assert "ws-other-account" not in " ".join(api.gets)             # the id is checked by listing, never echoed in a url
    assert p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "led.json", workspace_id="ws-mine")
    assert api.sent[0]["workspace_id"] == "ws-mine"


def test_p0g_a_key_without_management_rights_is_red_and_nothing_is_minted(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    api.keys_status = 403
    for ws in (None, "ws-mine"):
        api.workspaces = ["ws-mine"]
        with pytest.raises(p1_ab.P1Refused, match="cannot manage keys"):
            p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "led.json", workspace_id=ws)
    assert api.sent == [] and not (tmp_path / "led.json").exists()


def test_p0g_an_unlistable_workspace_set_is_red_and_an_absent_cell_needs_no_listing(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    api.workspaces = None                                          # GET /workspaces -> 403
    with pytest.raises(p1_ab.P1Refused, match="GET /workspaces answered HTTP 403"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "led.json", workspace_id="ws-mine")
    assert api.sent == []
    assert p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "led.json", workspace_id=None)
    assert api.sent and "workspace_id" not in api.sent[0]          # absent means absent: the field is omitted


def test_a_leaf_id_off_the_frozen_list_is_refused_before_any_call(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    for bad in ("goal:g6.50", 1, "g4.21", None, ""):
        with pytest.raises(p1_ab.P1Refused, match="frozen list"):
            p1_ab.mint_capped(arm="glm", leaf=bad, cfg=CFG, ledger=tmp_path / "l.json")
    assert api.sent == []


@pytest.mark.parametrize("bad", [0, -1, float("inf"), float("nan"), 0.51, 5, True, "0.5"])
def test_a_key_without_a_finite_cap_in_range_is_refused_before_any_call(monkeypatch, tmp_path, bad):
    api = Api(monkeypatch)
    with pytest.raises(p1_ab.P1Refused, match="refused at mint"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json", limit_usd=bad)
    assert api.sent == []


@pytest.mark.parametrize("stored", [None, 5.0, 0.51])
def test_an_uncapped_or_over_cap_key_on_read_back_is_revoked_and_refused(monkeypatch, tmp_path, stored):
    """The API ignoring the cap is the failure the read-back exists for (a 201 that lied)."""
    api = Api(monkeypatch, stored_limit=stored)
    led = tmp_path / "l.json"
    with pytest.raises(p1_ab.P1Refused, match="cap read back"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led)
    assert api.revoked == ["h1"] and not led.exists()


def _later(minutes):
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


@pytest.mark.parametrize("stored", [None, "", "not-a-time", "2020-01-01T00:00:00Z", _later(600), "2099-01-01T00:00:00"])
def test_an_expiry_that_reads_back_null_past_or_outside_the_window_is_revoked_and_refused(monkeypatch, tmp_path, stored):
    """provisioning.py's own note: expires_in_seconds can be silently ignored; the listing is the proof."""
    api = Api(monkeypatch, stored_expiry=stored)
    led = tmp_path / "l.json"
    with pytest.raises(p1_ab.P1Refused, match="expires_at"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led, ttl_minutes=90)
    assert api.revoked == ["h1"] and not led.exists()


def test_a_stub_that_answers_expires_at_null_at_creation_is_revoked_by_the_mint_itself(monkeypatch, tmp_path):
    api = Api(monkeypatch, sent_expiry=None)
    with pytest.raises(provisioning.ProvisioningError, match="no TTL"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")
    assert api.revoked == ["h1"]


def test_a_key_that_is_missing_from_the_listing_is_refused_too(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: [])
    with pytest.raises(p1_ab.P1Refused, match="cap read back"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")
    assert api.revoked == ["h1"]


def test_a_leaf_never_mints_twice_a_capped_kid_is_a_red_not_a_retry(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    p1_ab.mint_capped(arm="glm", leaf=LEAVES[2], cfg=CFG, ledger=led)
    with pytest.raises(p1_ab.P1Refused, match="never retried"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[2], cfg=CFG, ledger=led)
    assert len(api.sent) == 1
    p1_ab.mint_capped(arm="deepseek", leaf=LEAVES[2], cfg=CFG, ledger=led)     # another arm, same leaf: the pair
    assert len(api.sent) == 2


def test_five_leaves_by_two_arms_is_at_most_ten_keys_and_never_more(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    for arm in ("deepseek", "glm"):
        for leaf in LEAVES:
            p1_ab.mint_capped(arm=arm, leaf=leaf, cfg=CFG, ledger=led)
    rows = json.loads(led.read_text())
    assert len(rows) == 10 and len(api.sent) == 10
    assert p1_ab.exposure(rows, "glm") == 2.5 and p1_ab.exposure(rows) == 5.0
    for arm in ("deepseek", "glm"):                   # every (arm, leaf) is spent: nothing more can mint
        for leaf in LEAVES:
            with pytest.raises(p1_ab.P1Refused):
                p1_ab.mint_capped(arm=arm, leaf=leaf, cfg=CFG, ledger=led)
    assert len(api.sent) == 10


def test_the_arm_cap_and_the_cash_total_bind(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["arm_cap_usd"]["glm"] = 0.9
    led = tmp_path / "l.json"
    p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=cfg, ledger=led)
    with pytest.raises(p1_ab.P1Refused, match="arm cap"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[1], cfg=cfg, ledger=led)
    cfg2 = copy.deepcopy(CFG)
    cfg2["p1"]["cash_total_usd"] = 1.0
    led2 = tmp_path / "l2.json"
    p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=cfg2, ledger=led2)
    p1_ab.mint_capped(arm="deepseek", leaf=LEAVES[0], cfg=cfg2, ledger=led2)
    with pytest.raises(p1_ab.P1Refused, match="cash"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[1], cfg=cfg2, ledger=led2)


def test_the_credits_arm_mints_no_openrouter_key(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    with pytest.raises(p1_ab.P1Refused, match="org link"):
        p1_ab.mint_capped(arm="credits", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")
    assert api.sent == []


def test_no_provisioning_key_mints_nothing_and_does_not_fall_back(monkeypatch, tmp_path):
    monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda root=None: None)
    with pytest.raises(p1_ab.P1Refused, match="no provisioning key"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")


def test_an_unreadable_ledger_stops_minting(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    led.write_text("{not json")
    with pytest.raises(p1_ab.P1Refused, match="unreadable"):
        p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led)
    assert api.sent == []


# --- the key files: two ACL entries --------------------------------------------------

KID = 54321


@needs_acl
def test_a_key_file_gets_file_r_and_dir_x_for_exactly_the_kid_uid(tmp_path):
    d = tmp_path / "keys"
    f = p1_ab.write_key_file(d, "deepseek-1.key", "sk-secret", KID)
    assert f.read_text() == "sk-secret"
    # with an ACL the group bits of stat() show the MASK (the kid's r / x); the real group and other entries are ---
    assert (f.stat().st_mode & 0o707) == 0o600 and (d.stat().st_mode & 0o707) == 0o700
    assert p1_ab.acl_problems(f, d, KID) == []
    facl = subprocess.run(["getfacl", "-n", "-p", str(f)], capture_output=True, text=True).stdout
    assert f"user:{KID}:r--" in facl
    dacl = subprocess.run(["getfacl", "-n", "-p", str(d)], capture_output=True, text=True).stdout
    assert f"user:{KID}:--x" in dacl and f"user:{KID}:r" not in dacl


@needs_acl
def test_a_dir_without_x_or_with_r_or_with_a_second_reader_reads_red(tmp_path):
    d = tmp_path / "keys"
    f = p1_ab.write_key_file(d, "k", "sk-secret", KID)
    subprocess.run(["setfacl", "-x", f"u:{KID}", str(d)], check=True)           # the dir's x is gone
    assert any("dir" in x for x in p1_ab.acl_problems(f, d, KID))
    subprocess.run(["setfacl", "-m", f"u:{KID}:rx", str(d)], check=True)        # r on the dir lets it LIST
    assert any("dir" in x for x in p1_ab.acl_problems(f, d, KID))
    subprocess.run(["setfacl", "-m", f"u:{KID}:x", str(d)], check=True)
    assert p1_ab.acl_problems(f, d, KID) == []
    subprocess.run(["setfacl", "-m", f"u:{KID + 1}:r", str(f)], check=True)     # a second reader on the file
    assert any("file" in x for x in p1_ab.acl_problems(f, d, KID))
    subprocess.run(["setfacl", "-x", f"u:{KID + 1}", str(f)], check=True)
    subprocess.run(["setfacl", "-m", "g::r", str(f)], check=True)               # the owning group may read
    assert any("group::" in x for x in p1_ab.acl_problems(f, d, KID))
    subprocess.run(["setfacl", "-m", "g::-", "-m", "o::r", str(f)], check=True)  # everyone may read
    assert any("other::" in x for x in p1_ab.acl_problems(f, d, KID))


@needs_acl
def test_a_key_file_refuses_the_holder_a_bad_uid_a_bad_name_and_an_overwrite(tmp_path):
    d = tmp_path / "keys"
    for uid in (os.geteuid(), 0, -1, True, "1000", None):
        with pytest.raises(p1_ab.P1Refused, match="kid uid"):
            p1_ab.write_key_file(d, "k", "s", uid)
    for name in ("../k", "a/b", "", ".", "..", "k k"):
        with pytest.raises(p1_ab.P1Refused, match="plain file name"):
            p1_ab.write_key_file(d, name, "s", KID)
    p1_ab.write_key_file(d, "k", "s", KID)
    with pytest.raises(FileExistsError):
        p1_ab.write_key_file(d, "k", "s2", KID)
    assert (d / "k").read_text() == "s"


@needs_acl
def test_a_key_file_is_removed_when_its_acl_does_not_verify(tmp_path, monkeypatch):
    d = tmp_path / "keys"
    monkeypatch.setattr(p1_ab, "acl_problems", lambda *a: ["forced"])
    with pytest.raises(p1_ab.P1Refused, match="forced"):
        p1_ab.write_key_file(d, "k", "sk-secret", KID)
    assert not (d / "k").exists()


# --- the arm's refusals -------------------------------------------------------------

@pytest.fixture
def arm(tmp_path, monkeypatch):
    """A sealed pi1 prefix, a key dir, and a kid worktree sitting exactly on the frozen base."""
    pre = _prefix(tmp_path)
    p1_ab.seal(pre, CFG)
    keydir = tmp_path / "keys"
    keydir.mkdir(mode=0o700)
    wt = tmp_path / "wt"
    wt.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": "/dev/null"}
    for argv in (["init", "-q"], ["commit", "-q", "--allow-empty", "-m", "base"]):
        subprocess.run(["git", "-C", str(wt), *argv], check=True, env=env, capture_output=True)
    base = subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["base"] = base
    home = tmp_path / "home"
    (home / "k").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    return dict(prefix=pre, keydir=keydir, wt=wt, cfg=cfg, env=env, home=home, kid_home=home / "k" / "kid1")


def _pre(a, **over):
    kw = dict(arm="deepseek", leaf=LEAVES[0], prefix=a["prefix"], cfg=a["cfg"], kid_uid=KID,
              keydir=a["keydir"], worktree=a["wt"], kid_home=a["kid_home"])
    kw.update(over)
    p1_ab.arm_preflight(**kw)


def test_an_arm_that_meets_every_rule_starts(arm):
    _pre(arm)


def test_a_leaf_off_the_list_refuses_the_arm(arm):
    with pytest.raises(p1_ab.P1Refused, match="frozen list"):
        _pre(arm, leaf="goal:g6.50")


def test_one_changed_byte_in_pi1_refuses_the_arm(arm):
    (arm["prefix"] / "node_modules" / PIN["package"] / "cli.js").write_text("console.log('PI')\n")
    with pytest.raises(p1_ab.P1Refused, match="pi1 prefix refused"):
        _pre(arm)


def test_an_unsealed_or_unpinned_pi1_refuses_the_arm(arm):
    (arm["prefix"] / p1_ab.TREE_FILE).unlink()
    with pytest.raises(p1_ab.P1Refused, match="not sealed"):
        _pre(arm)


def test_a_kid_launched_as_the_key_holder_or_root_refuses_the_arm(arm):
    holder = os.stat(arm["keydir"]).st_uid
    for uid in (holder, 0):
        with pytest.raises(p1_ab.P1Refused, match="key holder"):
            _pre(arm, kid_uid=uid)


def test_a_worktree_not_on_the_frozen_base_refuses_the_arm(arm):
    subprocess.run(["git", "-C", str(arm["wt"]), "commit", "-q", "--allow-empty", "-m", "drift"],
                   check=True, env=arm["env"], capture_output=True)
    with pytest.raises(p1_ab.P1Refused, match="frozen base"):
        _pre(arm)
    with pytest.raises(p1_ab.P1Refused, match="not the top of a git worktree"):
        _pre(arm, worktree=arm["wt"].parent / "not-a-repo")


def test_the_credits_or_an_unknown_arm_is_not_started_as_an_openrouter_arm(arm):
    with pytest.raises(p1_ab.P1Refused, match="not a P1 arm"):
        _pre(arm, arm="mystery")


# --- end of arm ---------------------------------------------------------------------

def test_end_arm_disables_reads_back_disabled_and_removes_the_files(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    rows = []
    for i, leaf in enumerate(LEAVES[:2]):
        k = p1_ab.mint_capped(arm="glm", leaf=leaf, cfg=CFG, ledger=tmp_path / "l.json")
        f = tmp_path / f"k{i}"
        f.write_text(k.secret)
        rows.append({"hash": k.key_hash, "file": str(f)})
    assert p1_ab.end_arm(rows) == []
    assert api.patched == ["h1", "h2"] and all(not Path(r["file"]).exists() for r in rows)
    assert all(r["disabled"] for r in api.rows)


def test_a_key_in_another_workspace_reads_disabled_by_hash_though_the_listing_is_blind(monkeypatch, tmp_path):
    """The live red (10-24): GET /keys lists only the default workspace and omits disabled keys, so a key minted into
    agi-local-town read back 'absent' after a correct disable. The read-back is GET /keys/<hash>, never the listing."""
    api = Api(monkeypatch)
    api.workspaces = ["ws-town"]
    led = tmp_path / "l.json"
    k = p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led, workspace_id="ws-town")
    monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: [])     # blind, whatever is asked
    f = tmp_path / "k"
    f.write_text(k.secret)
    assert p1_ab.end_arm([{"hash": k.key_hash, "file": str(f)}], workspace_id="ws-town") == [] and not f.exists()
    api.rows[0]["usage"] = 0.0249
    done = p1_ab.kid_done(key_hash=k.key_hash, keyfile=f, ledger=led, workspace_id="ws-town")     # second call: idempotent
    assert done["problems"] == [] and done["usd"] == 0.0249
    row = json.loads(led.read_text())[0]
    assert row["done"] is True and row["usd"] == 0.0249                                              # so `record` can read it


def test_a_missed_disable_is_a_red_and_the_file_is_still_removed(monkeypatch, tmp_path):
    api = Api(monkeypatch, stored_limit="ignore-disable")
    k = p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")
    f = tmp_path / "k"
    f.write_text(k.secret)
    problems = p1_ab.end_arm([{"hash": k.key_hash, "file": str(f)}])
    assert any("LIVE" in x for x in problems) and not f.exists()                              # a 200 with disabled false is LIVE


def test_a_key_the_api_does_not_know_by_hash_is_a_red(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: [])
    problems = p1_ab.end_arm([{"hash": "gone", "file": str(tmp_path / "none")}])
    assert len(problems) == 1 and "unread: 404" in problems[0] and "disabled" not in problems[0].replace("unread", "")     # a 404 never reads disabled


def test_a_scratch_land_that_creates_a_shadow_bin_file_reads_red():
    assert p1_ab.scratch_land_problems(["extensions/x.py", ".agi/nodes/goal/g.md"], CFG) == []
    for bad in (".agi/bin/render-context.py", ".agi/bin/snapshot-build-site.py"):
        assert p1_ab.scratch_land_problems(["a.py", bad], CFG) == [f"scratch land creates {bad}: forbidden"]


# --- the spawn gate ------------------------------------------------------------------

@pytest.mark.parametrize("live,gb,ok", [(0, 4.99, True), (1, 5.0, True), (2, 1.0, False), (0, 5.01, False), (0, None, False)])
def test_may_start(live, gb, ok):
    assert p1_ab.may_start(live, gb, CFG)[0] is ok


def _slice_files(tmp_path, *, anon=3.1, shmem=0.0, dirty=0.0, writeback=0.0, file=1.4, kernel=0.6, slab_reclaimable=0.5,
                 psi=0.0, avail=3.6, stat=True, pressure=True, meminfo=True):
    g = lambda x: int(x * 1e9)
    (tmp_path / "stat").write_text("\n".join(f"{k} {g(v)}" for k, v in dict(
        anon=anon, file=file, kernel=kernel, shmem=shmem, file_dirty=dirty, file_writeback=writeback,
        slab_reclaimable=slab_reclaimable).items()) + "\npgscan 15034070\n")
    (tmp_path / "pressure").write_text(f"some avg10={psi:.2f} avg60=0.00 avg300=0.04 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n")
    (tmp_path / "meminfo").write_text(f"MemTotal:        8042504 kB\nMemAvailable:    {int(avail * 1e9 / 1024)} kB\n")
    files = [str(tmp_path / n) for n in ("stat", "pressure", "meminfo")]
    for flag, i in ((stat, 0), (pressure, 1), (meminfo, 2)):
        if not flag:
            files[i] = str(tmp_path / "gone")
    return tuple(files)


def _may(tmp_path, **kw):
    return p1_ab.may_start(0, p1_ab.slice_reading(*_slice_files(tmp_path, **kw)), CFG)[0]


def test_p0c_the_measure_ignores_page_cache_counts_dirty_pages_and_keeps_the_5_0_bound(tmp_path):
    """alive's rows: file 1.4 + anon 3.1 ~ 3.2 ok; file_dirty 1.0 + anon 3.1 ~ 4.1; anon 5.1 RED; PSI 35 RED; PSI 2 ok."""
    r = p1_ab.slice_reading(*_slice_files(tmp_path, anon=3.1, file=1.4))
    assert r["gb"] == pytest.approx(3.2) and r["psi"] == 0.0 and r["avail_gb"] == pytest.approx(3.6, abs=0.01)
    assert p1_ab.slice_reading(*_slice_files(tmp_path, anon=3.1, dirty=1.0))["gb"] == pytest.approx(4.2)
    assert p1_ab.slice_reading(*_slice_files(tmp_path, anon=3.1, writeback=0.5, shmem=0.2))["gb"] == pytest.approx(3.9)
    assert _may(tmp_path) is True
    assert _may(tmp_path, anon=5.1) is False
    assert _may(tmp_path, anon=4.4, dirty=1.0) is False               # 4.4 + 1.0 + 0.1 > 5.0
    assert _may(tmp_path, psi=35) is False and _may(tmp_path, psi=20) is True and _may(tmp_path, psi=2) is True
    assert _may(tmp_path, avail=1.4) is False and _may(tmp_path, avail=1.51) is True
    assert CFG["p1"]["slice_gb_max"] == 5.0 and CFG["p1"]["psi_max"] == 20 and CFG["p1"]["mem_avail_min_gb"] == 1.5


def test_p0c_any_of_the_three_readings_unreadable_fails_closed(tmp_path):
    for kw in (dict(stat=False), dict(pressure=False), dict(meminfo=False)):
        assert p1_ab.slice_reading(*_slice_files(tmp_path, **kw)) is None
        assert _may(tmp_path, **kw) is False
    (tmp_path / "stat").write_text("anon 1\n")                       # a stat without the keys
    assert p1_ab.slice_reading(str(tmp_path / "stat"), str(tmp_path / "pressure"), str(tmp_path / "meminfo")) is None


def test_p0c_the_real_files_of_this_box_read_when_they_exist():
    if not Path(p1_ab.SLICE_STAT).exists():
        pytest.skip("no agi.slice here")
    r = p1_ab.slice_reading()
    assert r is not None and 0 < r["gb"] < 64 and r["psi"] >= 0 and r["avail_gb"] > 0


# --- the results file -> the metrics_line segment -------------------------------------

def _kids(spec):
    return [{"leaf": LEAVES[i], "landed": l, "usd": u, "secs": s, "red": r} for i, (l, u, s, r) in enumerate(spec)]


RESULTS = {"base": CFG["p1"]["base"], "arms": [
    {"arm": "deepseek", "model": "deepseek/deepseek-v4.1-flash-1017",
     "kids": _kids([(True, 0.10, 100, False), (True, 0.10, 120, False), (False, 0.20, 60, True), (True, 0.0, 20, False), (False, 0.10, 40, True)])},
    {"arm": "glm", "model": "z-ai/glm-5.3-flash", "kids": _kids([(False, 0.3, 9, True)] * 5)},
]}


def test_the_segment_has_the_four_numbers_per_arm_and_n_is_the_leaf_count():
    seg = p1_ab.render_segment(RESULTS, CFG)
    assert seg == ("| p1: deepseek/deepseek-v4.1-flash-1017 $/landed=0.1667 s/landed=113 red=2/5 "
                   "| p1: z-ai/glm-5.3-flash $/landed=n/a landed=0 red=5/5")
    assert seg.count("| p1: ") == 2
    assert p1_ab.render_segment({"arms": []}, CFG) == ""


def test_merge_pick_takes_the_first_green_run_in_the_fixed_arm_order():
    res = {"arms": [
        {"arm": "glm", "model": "m", "kids": _kids([(True, 0, 0, False)] * 5)},
        {"arm": "deepseek", "model": "m", "kids": _kids([(False, 0, 0, True), (True, 0, 0, False), (False, 0, 0, True),
                                                         (False, 0, 0, True), (True, 0, 0, False)])},
    ]}
    pick = p1_ab.merge_pick(res, CFG)
    assert pick == {LEAVES[0]: "glm", LEAVES[1]: "deepseek", LEAVES[2]: "glm", LEAVES[3]: "glm", LEAVES[4]: "deepseek"}
    none = p1_ab.merge_pick({"arms": [{"arm": "glm", "model": "m", "kids": _kids([(False, 0, 0, True)] * 5)}]}, CFG)
    assert set(none.values()) == {None}


def test_the_one_metrics_writer_renders_the_segment_and_names_a_bad_file(tmp_path):
    root = tmp_path
    (root / ".agi").mkdir()
    (root / ".agi" / "config.json").write_text(json.dumps(CFG))
    assert success_metrics.p1_segment(root) == ""                       # no results file, no segment
    res = root / CFG["p1"]["results"]
    res.parent.mkdir(parents=True)
    res.write_text(json.dumps(RESULTS))
    seg = success_metrics.p1_segment(root)
    assert seg.count("| p1: ") == 2 and "red=2/5" in seg
    res.write_text("{broken")
    assert success_metrics.p1_segment(root).startswith("| p1: UNMEASURED(results unreadable")


# --- belam's thin driver: kid-key before a kid, kid-done after ------------------------

@needs_acl
def test_kid_key_mints_and_writes_one_acld_file_and_returns_no_secret(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    d = tmp_path / "keys"
    out = p1_ab.kid_key(arm="deepseek", leaf=LEAVES[1], cfg=CFG, keydir=d, ledger=tmp_path / "l.json", kid_uid=KID)
    assert out == {"arm": "deepseek", "leaf": LEAVES[1], "hash": "h1", "file": str(d / "deepseek-l2.key")}
    assert "sk-h1" not in json.dumps(out) and (d / "deepseek-l2.key").read_text() == "sk-h1"
    assert p1_ab.acl_problems(d / "deepseek-l2.key", d, KID) == []
    assert api.sent[0]["limit"] == 0.5


@needs_acl
def test_at_most_max_live_key_files_exist_and_a_third_waits(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    d = tmp_path / "keys"
    led = tmp_path / "l.json"
    p1_ab.kid_key(arm="deepseek", leaf=LEAVES[0], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)
    p1_ab.kid_key(arm="deepseek", leaf=LEAVES[1], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)
    with pytest.raises(p1_ab.P1Refused, match="at most 2 at once"):
        p1_ab.kid_key(arm="deepseek", leaf=LEAVES[2], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)
    assert len(api.sent) == 2                       # the third never reached the API
    p1_ab.kid_done(key_hash="h1", keyfile=d / "deepseek-l1.key", ledger=led)
    p1_ab.kid_key(arm="deepseek", leaf=LEAVES[2], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)   # a slot freed


def test_kid_key_refuses_a_leaf_off_the_list_before_anything(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    with pytest.raises(p1_ab.P1Refused, match="frozen list"):
        p1_ab.kid_key(arm="glm", leaf="goal:g6.50", cfg=CFG, keydir=tmp_path / "k", ledger=tmp_path / "l.json", kid_uid=KID)
    assert api.sent == [] and not (tmp_path / "k").exists()


@needs_acl
def test_a_key_file_that_cannot_be_written_revokes_the_key_and_the_leaf_stays_spent(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "l.json"
    with pytest.raises(p1_ab.P1Refused, match="kid uid"):
        p1_ab.kid_key(arm="glm", leaf=LEAVES[0], cfg=CFG, keydir=tmp_path / "k", ledger=led, kid_uid=os.geteuid())
    assert api.revoked == ["h1"] and not list((tmp_path / "k").glob("*.key"))
    with pytest.raises(p1_ab.P1Refused, match="never retried"):
        p1_ab.kid_key(arm="glm", leaf=LEAVES[0], cfg=CFG, keydir=tmp_path / "k", ledger=led, kid_uid=KID)


@needs_acl
def test_kid_done_reads_spend_disables_reads_back_removes_the_file_and_records(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    d = tmp_path / "keys"
    led = tmp_path / "l.json"
    k = p1_ab.kid_key(arm="glm", leaf=LEAVES[0], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)
    api.rows[0]["usage"] = 0.1234
    out = p1_ab.kid_done(key_hash=k["hash"], keyfile=k["file"], ledger=led)
    assert out == {"arm": "glm", "leaf": LEAVES[0], "hash": "h1", "usd": 0.1234, "problems": []}
    assert api.rows[0]["disabled"] is True and not Path(k["file"]).exists()
    row = json.loads(led.read_text())[0]
    assert row["usd"] == 0.1234 and row["done"] is True


@needs_acl
def test_kid_done_with_a_key_that_stays_enabled_is_a_red_and_still_removes_the_file(monkeypatch, tmp_path):
    api = Api(monkeypatch, stored_limit="ignore-disable")
    d = tmp_path / "keys"
    led = tmp_path / "l.json"
    k = p1_ab.kid_key(arm="glm", leaf=LEAVES[0], cfg=CFG, keydir=d, ledger=led, kid_uid=KID)
    out = p1_ab.kid_done(key_hash=k["hash"], keyfile=k["file"], ledger=led)
    assert any("LIVE" in x for x in out["problems"]) and not Path(k["file"]).exists()
    assert json.loads(led.read_text())[0]["done"] is False


def test_kid_done_will_not_touch_a_key_the_ledger_never_minted(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    api.rows.append({"hash": "owners-key", "limit": None, "usage": 1.0, "disabled": False})
    led = tmp_path / "l.json"
    led.write_text("[]")
    with pytest.raises(p1_ab.P1Refused, match="not in the ledger"):
        p1_ab.kid_done(key_hash="owners-key", keyfile=tmp_path / "x", ledger=led)
    assert api.patched == []


@needs_acl
def _town_workspaces(api):
    """The CLI reads the repo's own config: the workspace it will send is owned, as the live key's account would own it."""
    town = json.loads((Path(p1_ab.__file__).resolve().parents[3] / ".agi" / "config.json").read_text())
    api.workspaces = [provisioning.workspace(town)]


def test_the_cli_prints_json_without_the_secret_and_exits_nonzero_on_a_refusal(monkeypatch, tmp_path, capsys):
    api = Api(monkeypatch)
    _town_workspaces(api)
    d, led = tmp_path / "keys", tmp_path / "l.json"
    rc = p1_ab.main(["p1_ab.py", "kid-key", "deepseek", LEAVES[0], "--kid-uid", str(KID), "--keydir", str(d), "--ledger", str(led)])
    out = capsys.readouterr().out
    assert rc == 0 and "sk-h1" not in out and json.loads(out)["hash"] == "h1"
    rc = p1_ab.main(["p1_ab.py", "kid-key", "deepseek", LEAVES[0], "--kid-uid", str(KID), "--keydir", str(d), "--ledger", str(led)])
    out = capsys.readouterr().out
    assert rc == 1 and "never retried" in out and out.rstrip().endswith("RED") and "sk-" not in out
    rc = p1_ab.main(["p1_ab.py", "kid-done", "--hash", "h1", "--file", str(d / "deepseek-l1.key"), "--ledger", str(led)])
    done = json.loads(capsys.readouterr().out)
    assert rc == 0 and done["problems"] == [] and "sk-" not in json.dumps(done)


# --- the kid launch (my side): F1, F2, the bounds that hold, node, models.json, env, results -------------

MARK = "sk-or-MARKER-7f3a9c"


def test_f2_a_minted_key_repr_never_carries_the_secret():
    k = provisioning.MintedKey(secret=MARK, key_hash="h", name="n", limit_usd=0.5, expires_at="x")
    assert MARK not in repr(k) and MARK not in str(k) and k.secret == MARK


@needs_acl
def test_f1_kid_key_stdout_and_its_red_path_hold_zero_bytes_of_the_secret(monkeypatch, tmp_path, capsys):
    """A stub mint whose secret is a marker: the JSON line, the refusal text and the ledger never contain it; only
    the key file does. (Mutant: a return dict carrying the secret reads RED in the D3 row above and here.)"""
    api = Api(monkeypatch, secret=MARK)
    _town_workspaces(api)
    d, led = tmp_path / "keys", tmp_path / "l.json"
    argv = ["p1_ab.py", "kid-key", "glm", LEAVES[0], "--kid-uid", str(KID), "--keydir", str(d), "--ledger", str(led)]
    assert p1_ab.main(argv) == 0
    out = capsys.readouterr()
    assert MARK not in out.out + out.err and (d / "glm-l1.key").read_text() == MARK
    assert p1_ab.main(argv) == 1                                      # the RED path: already minted
    out = capsys.readouterr()
    assert "RED" in out.out and MARK not in out.out + out.err
    assert MARK not in led.read_text()
    bad = ["p1_ab.py", "kid-key", "deepseek", LEAVES[0], "--kid-uid", str(os.geteuid()), "--keydir", str(d), "--ledger", str(led)]
    assert p1_ab.main(bad) == 1                                       # the RED path: the file write refused after the mint
    out = capsys.readouterr()
    assert "RED" in out.out and MARK not in out.out + out.err
    assert not (d / "deepseek-l1.key").exists()


def test_the_bounds_that_hold_are_named_by_rows():
    """alive's [withdraw]: the record names the REAL protections, not an isolation the one-uid model cannot give.
    max_live 2 key files (test_at_most_max_live_key_files...), the $0.50 cap with the expires_at window read back
    (test_an_uncapped..., test_an_expiry...), kid-done disables + reads back + removes (test_kid_done_...). Here:
    the cell values those rows run against."""
    p = CFG["p1"]
    assert p["max_live"] == 2 and p["key_cap_usd"] == 0.5
    assert "isolation" not in json.dumps(p).lower()


def _fake_node(tmp_path, version="v22.30.0", body=""):
    f = tmp_path / f"node-{version}"
    f.write_text(f'#!/bin/sh\nif [ "$1" = "--version" ]; then echo {version}; exit 0; fi\n{body}\n')
    f.chmod(0o755)
    return str(f)


def _cfg_node(*nodes):
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["node_candidates"] = list(nodes)
    return cfg


def test_node_for_pi_takes_the_first_candidate_at_or_above_node_min(tmp_path):
    old, new = _fake_node(tmp_path, "v20.20.2"), _fake_node(tmp_path, "v22.19.0")
    assert p1_ab.node_for_pi(_cfg_node(old, new)) == new
    assert p1_ab.node_for_pi(_cfg_node(new, old)) == new


def test_node_for_pi_refuses_when_no_node_is_new_enough(tmp_path, monkeypatch):
    old = _fake_node(tmp_path, "v20.20.2")
    monkeypatch.setattr(shutil, "which", lambda name: old)
    with pytest.raises(p1_ab.P1Refused, match="no node >= 22.19.0"):
        p1_ab.node_for_pi(_cfg_node(old, str(tmp_path / "missing"), _fake_node(tmp_path, "v22.18.9")))


def test_pi_cli_must_sit_inside_the_pinned_package(tmp_path):
    pre = _prefix(tmp_path)
    assert p1_ab.pi_cli(pre, CFG).endswith("/cli.js")
    link = pre / "node_modules" / ".bin" / "pi"
    link.unlink()
    outside = tmp_path / "evil.js"
    outside.write_text("x")
    os.symlink(outside, link)
    with pytest.raises(p1_ab.P1Refused, match="outside the pinned package"):
        p1_ab.pi_cli(pre, CFG)


def test_models_json_holds_a_path_never_a_key_and_is_0600(tmp_path):
    kf = tmp_path / "keys" / "glm-l1.key"
    m = p1_ab.write_models_json(tmp_path / "agent", "openrouter", kf)
    assert json.loads(m.read_text()) == {"providers": {"openrouter": {"apiKey": f"!cat {kf}"}}}
    assert (m.stat().st_mode & 0o777) == 0o600
    for bad in ("rel/key", "/a b/key", '/a"b', "/a;rm", "/a$(x)", "/a\nb", ""):
        with pytest.raises(p1_ab.P1Refused, match="plain path"):
            p1_ab.write_models_json(tmp_path / "agent2", "openrouter", bad)


def test_leaf_brief_carries_the_falsifier_verbatim_and_the_standing_rule_only_where_the_cell_says():
    b = p1_ab.leaf_brief("goal:g4.18.2.1", ROOT, CFG)
    node = (ROOT / ".agi/nodes/goal/g4.18.2.1.md").read_text()
    assert "goal:g4.18.2.1" in b and "## Falsifier" in b
    fal = node.split("## Falsifier", 1)[1].split("\n## ", 1)[0].strip().splitlines()[0]
    assert fal in b
    assert "never create .agi/bin/render-context.py or .agi/bin/snapshot-build-site.py" in b
    assert "Standing rule" not in p1_ab.leaf_brief("goal:g7.31.3.1", ROOT, CFG)
    with pytest.raises(p1_ab.P1Refused, match="frozen list"):
        p1_ab.leaf_brief("goal:g6.50", ROOT, CFG)


def _plan(tmp_path, node, arm="deepseek", **kw):
    pre = _prefix(tmp_path)
    cfg = _cfg_node(node)
    cfg["p1"]["kid_timeout_s"] = kw.pop("timeout", 30)
    return cfg, p1_ab.kid_plan(arm=arm, leaf=LEAVES[0], cfg=cfg, keyfile=tmp_path / "keys" / "k.key",
                               worktree=tmp_path, kid_home=tmp_path / "kidhome", prompt="do it", prefix=pre, **kw)


def test_kid_plan_has_the_pinned_command_and_an_environment_with_no_key(tmp_path):
    node = _fake_node(tmp_path)
    cfg, plan = _plan(tmp_path, node)
    assert plan["argv"][0] == node and plan["argv"][1].endswith("/cli.js")
    i = plan["argv"].index("--model")
    assert plan["argv"][i + 1] == "deepseek/deepseek-v4.1-flash-1017" and plan["argv"][plan["argv"].index("--provider") + 1] == "openrouter"
    assert set(plan["env"]) == set(p1_ab.KID_ENV_KEYS) and plan["env"]["PATH"].startswith(os.path.dirname(node))
    assert "OPENROUTER_API_KEY" not in plan["env"] and "sk-" not in json.dumps(plan)
    assert plan["env"]["HOME"] == str(tmp_path / "kidhome")


def test_kid_plan_refuses_the_credits_arm_an_unknown_arm_and_an_off_list_leaf(tmp_path):
    node = _fake_node(tmp_path)
    pre = _prefix(tmp_path)
    cfg = _cfg_node(node)
    for arm in ("credits", "mystery"):
        with pytest.raises(p1_ab.P1Refused, match="cannot launch"):
            p1_ab.kid_plan(arm=arm, leaf=LEAVES[0], cfg=cfg, keyfile="/k", worktree=tmp_path, kid_home=tmp_path, prompt="p", prefix=pre)
    with pytest.raises(p1_ab.P1Refused, match="frozen list"):
        p1_ab.kid_plan(arm="glm", leaf="goal:g6.50", cfg=cfg, keyfile="/k", worktree=tmp_path, kid_home=tmp_path, prompt="p", prefix=pre)


def test_run_kid_runs_once_with_the_whitelisted_env_a_models_json_that_is_gone_afterwards(tmp_path):
    out = tmp_path / "seen"
    out.mkdir()
    node = _fake_node(tmp_path, body=f'env > {out}/env\ncat "$PI_CODING_AGENT_DIR/models.json" > {out}/models\nexit 3')
    cfg, plan = _plan(tmp_path, node)
    (tmp_path / "kidhome").mkdir()
    res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert res["rc"] == 3 and res["timed_out"] is False and res["secs"] >= 0
    env_keys = {ln.split("=", 1)[0] for ln in (out / "env").read_text().splitlines()}
    assert env_keys <= set(p1_ab.KID_ENV_KEYS) | {"PWD", "SHLVL", "_", "OLDPWD"}
    assert "!cat" in (out / "models").read_text()
    assert not (tmp_path / "kidhome" / ".p1-agent" / "models.json").exists()
    assert (tmp_path / "kidhome" / "p1-deepseek-1.log").exists()


def test_run_kid_refuses_at_the_live_bound_an_unreadable_slice_and_a_foreign_env(tmp_path):
    node = _fake_node(tmp_path, body="exit 0")
    cfg, plan = _plan(tmp_path, node)
    (tmp_path / "kidhome").mkdir()
    for live, gb in ((2, 1.0), (0, None), (0, 5.5)):
        with pytest.raises(p1_ab.P1Refused, match="not started"):
            p1_ab.run_kid(plan, cfg, live=live, gb=gb)
    plan["env"]["OPENROUTER_API_KEY"] = "x"
    with pytest.raises(p1_ab.P1Refused, match="only"):
        p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert not (tmp_path / "kidhome" / ".p1-agent" / "models.json").exists()


def test_a_kid_at_the_timeout_is_a_counted_red_not_a_retry(tmp_path):
    node = _fake_node(tmp_path, body="sleep 30")
    cfg, plan = _plan(tmp_path, node, timeout=1)
    (tmp_path / "kidhome").mkdir()
    res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert res["timed_out"] is True and res["rc"] is None
    assert not (tmp_path / "kidhome" / ".p1-agent" / "models.json").exists()


def test_record_result_adds_one_row_per_pair_in_arm_order_and_renders(tmp_path):
    f = tmp_path / "res.json"
    p1_ab.record_result(f, CFG, arm="glm", leaf=LEAVES[0], landed=True, usd=0.1, secs=100, red=False)
    p1_ab.record_result(f, CFG, arm="deepseek", leaf=LEAVES[0], landed=False, usd=0.2, secs=50, red=True)
    p1_ab.record_result(f, CFG, arm="deepseek", leaf=LEAVES[1], landed=True, usd=0.3, secs=70, red=False)
    res = json.loads(f.read_text())
    assert [a["arm"] for a in res["arms"]] == ["deepseek", "glm"] and res["base"] == CFG["p1"]["base"]
    assert res["arms"][0]["model"] == "deepseek/deepseek-v4.1-flash-1017" and len(res["arms"][0]["kids"]) == 2
    seg = p1_ab.render_segment(res, CFG)
    assert "| p1: deepseek/deepseek-v4.1-flash-1017 $/landed=0.5000 s/landed=120 red=1/5" in seg
    assert "| p1: z-ai/glm-5.3-flash $/landed=0.1000 s/landed=100 red=0/5" in seg
    for kw, why in ((dict(arm="glm", leaf=LEAVES[0], usd=0.1), "already has"), (dict(arm="glm", leaf="goal:g6.50", usd=0.1), "frozen list"),
                    (dict(arm="glm", leaf=LEAVES[2], usd=-1), "finite"), (dict(arm="glm", leaf=LEAVES[2], usd=float("nan")), "finite"),
                    (dict(arm="nope", leaf=LEAVES[2], usd=0.1), "no harness row")):
        with pytest.raises(p1_ab.P1Refused, match=why):
            p1_ab.record_result(f, CFG, landed=True, secs=1, red=False, **kw)
    res["base"] = "0" * 40
    f.write_text(json.dumps(res))
    with pytest.raises(p1_ab.P1Refused, match="frozen base"):
        p1_ab.record_result(f, CFG, arm="glm", leaf=LEAVES[2], landed=True, usd=0.1, secs=1, red=False)


def _node22():
    try:
        return p1_ab.node_for_pi(CFG)
    except p1_ab.P1Refused:
        return None


@pytest.mark.skipif(_node22() is None or not (Path.home() / "pi1" / p1_ab.TREE_FILE).exists(),
                    reason="needs node >= 22.19 and this home's sealed pi1")
def test_the_real_pi1_reads_its_key_from_the_file_through_models_json_offline(tmp_path):
    """The smoke turn at $0: a local stub speaks the OpenAI streaming shape; pi1 sends the key it cats from the file."""
    import http.server
    import threading
    seen = []

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            self.rfile.read(int(self.headers.get("content-length") or 0))
            seen.append(self.headers.get("authorization"))
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            for d in ({"id": "c", "object": "chat.completion.chunk", "created": 1, "model": "s",
                       "choices": [{"index": 0, "delta": {"role": "assistant", "content": "hi from stub"}, "finish_reason": None}]},
                      {"id": "c", "object": "chat.completion.chunk", "created": 1, "model": "s",
                       "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                       "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}, "[DONE]"):
                self.wfile.write(("data: " + (d if isinstance(d, str) else json.dumps(d)) + "\n\n").encode())

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    keyfile = tmp_path / "keys" / "k.key"
    keyfile.parent.mkdir()
    keyfile.write_text(MARK)
    home = tmp_path / "kidhome"
    home.mkdir()
    plan = p1_ab.kid_plan(arm="glm", leaf=LEAVES[0], cfg=CFG, keyfile=keyfile, worktree=tmp_path, kid_home=home,
                          prompt="say hi", prefix="~/pi1", base_url=f"http://127.0.0.1:{srv.server_port}/v1")
    plan["argv"] += ["--no-tools", "--no-context-files"]
    assert MARK not in json.dumps(plan)
    res = p1_ab.run_kid(plan, CFG, live=0, gb=1.0)
    srv.shutdown()
    assert res["rc"] == 0 and seen and seen[0] == f"Bearer {MARK}"
    assert "hi from stub" in (home / "p1-glm-1.log").read_text()
    assert not (home / ".p1-agent" / "models.json").exists()


# --- R1-R4 (council 3/3, 03:05Z 10-24) -------------------------------------------------------------------

LEAF = LEAVES[3]          # goal:g4.21
NODE_TEXT = """---
id: goal:g4.21
---
# goal:g4.21

## Why this exists
because.

## Target end-state
- ONE project marker.

## Invariants
- no legacy marker.

## Falsifier
1. A test creates a scratch directory holding only a legacy marker.

## Out of scope
- the rest.

<!-- THOUGHT:BEGIN -->
secret thought
<!-- THOUGHT:END -->
"""
RULES_TEXT = ("## Target end-state\n- (Q2) leaves. The kid brief for g4.21 carries the standing rule: leave the "
              "marker list alone. (Q3) p1_ab.py writes numbers to a file.\n")


def _git(repo, *argv):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": "/dev/null"}
    return subprocess.run(["git", "-C", str(repo), *argv], check=True, capture_output=True, text=True, env=env).stdout.strip()


@pytest.fixture
def brief_repo(tmp_path):
    repo = tmp_path / "briefrepo"
    (repo / ".agi" / "nodes" / "goal").mkdir(parents=True)
    _git(repo, "init", "-q")
    (repo / ".agi/nodes/goal/g4.21.md").write_text(NODE_TEXT)
    (repo / ".agi/nodes/goal/g7.16.1.11.46.9.md").write_text(RULES_TEXT)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    cfg = copy.deepcopy(CFG)
    cfg["p1"]["base"] = _git(repo, "rev-parse", "HEAD")
    return repo, cfg


def test_r3_the_brief_is_the_leaf_node_at_the_base_with_four_sections_and_the_preregistered_rule(brief_repo):
    repo, cfg = brief_repo
    b = p1_ab.leaf_brief(LEAF, repo, cfg)
    for head in ("Target end-state", "Invariants", "Falsifier", "Out of scope"):
        assert f"## {head}" in b, head
    assert "ONE project marker" in b and "no legacy marker" in b and "the rest" in b
    assert "secret thought" not in b and "because" not in b
    assert "Standing rule: leave the marker list alone" in b
    (repo / ".agi/nodes/goal/g7.31.3.1.md").write_text(NODE_TEXT.replace("goal:g4.21", "goal:g7.31.3.1"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "a second leaf, no preregistered rule")
    cfg2 = copy.deepcopy(cfg)
    cfg2["p1"]["base"] = _git(repo, "rev-parse", "HEAD")
    assert "Standing rule" not in p1_ab.leaf_brief("goal:g7.31.3.1", repo, cfg2)


def test_r3_a_trunk_edit_to_the_falsifier_the_rule_text_or_a_cell_leaves_the_sha_unchanged(brief_repo):
    repo, cfg = brief_repo
    before = p1_ab.leaf_brief(LEAF, repo, cfg)
    sha = p1_ab.brief_digest(before)
    (repo / ".agi/nodes/goal/g4.21.md").write_text(NODE_TEXT.replace("legacy marker.", "a DIFFERENT falsifier."))
    (repo / ".agi/nodes/goal/g7.16.1.11.46.9.md").write_text(RULES_TEXT.replace("leave the marker list alone", "do something else"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "trunk moves on")
    cfg2 = copy.deepcopy(cfg)
    cfg2["p1"]["kid_rules"] = {LEAF: "an injected cell rule"}
    for c in (cfg, cfg2):
        after = p1_ab.leaf_brief(LEAF, repo, c)
        assert after == before and p1_ab.brief_digest(after) == sha
    assert "DIFFERENT" not in before and "injected" not in before


def test_r3_a_base_that_cannot_be_read_refuses_the_brief(brief_repo):
    repo, cfg = brief_repo
    cfg["p1"]["base"] = "0" * 40
    with pytest.raises(p1_ab.P1Refused, match="frozen base cannot be read"):
        p1_ab.leaf_brief(LEAF, repo, cfg)


def test_r3_both_arms_rows_for_a_leaf_carry_the_same_sha_or_the_second_is_refused(tmp_path):
    f = tmp_path / "res.json"
    p1_ab.record_result(f, CFG, arm="deepseek", leaf=LEAF, landed=True, usd=0.1, secs=5, red=False, brief_sha256="a" * 64)
    with pytest.raises(p1_ab.P1Refused, match="one frozen brief per leaf"):
        p1_ab.record_result(f, CFG, arm="glm", leaf=LEAF, landed=True, usd=0.1, secs=5, red=False, brief_sha256="b" * 64)
    p1_ab.record_result(f, CFG, arm="glm", leaf=LEAF, landed=True, usd=0.1, secs=5, red=False, brief_sha256="a" * 64)
    rows = [k for arm in json.loads(f.read_text())["arms"] for k in arm["kids"]]
    assert [k["brief_sha256"] for k in rows] == ["a" * 64, "a" * 64]


def _ledgers(tmp_path, *, done=True, usd=0.12, rc=0, timed_out=False, sweep=(), secs=33.0, with_run=True, arm="deepseek"):
    led, runs = tmp_path / "ledger.json", tmp_path / "runs.json"
    mint = {"arm": arm, "leaf": LEAF, "hash": "h1", "cap": 0.5}
    if done is not None:
        mint.update(usd=usd, done=done)
    led.write_text(json.dumps([mint]))
    runs.write_text(json.dumps([{"arm": arm, "leaf": LEAF, "rc": rc, "secs": secs, "timed_out": timed_out,
                                 "sweep": list(sweep), "brief_sha256": "e" * 64}] if with_run else []))
    return led, runs


def _rec(tmp_path, landed, red, **kw):
    led, runs = _ledgers(tmp_path, **kw)
    return p1_ab.record_from_ledgers(tmp_path / "res.json", CFG, arm="deepseek", leaf=LEAF, ledger=led, runs=runs,
                                     landed=landed, red=red)


def test_r1_record_reads_usd_from_the_kid_done_row_and_secs_from_the_run_row(tmp_path):
    res = _rec(tmp_path, True, False, usd=0.1234, secs=41.5)
    k = res["arms"][0]["kids"][0]
    assert (k["usd"], k["secs"], k["landed"], k["red"], k["brief_sha256"]) == (0.1234, 41.5, True, False, "e" * 64)


@pytest.mark.parametrize("kw", [dict(done=None), dict(done=False), dict(usd=None), dict(with_run=False)],
                         ids=["no-done-key", "done-false", "usd-null", "no-run-row"])
def test_r1_no_kid_done_row_or_no_run_row_is_refused(tmp_path, kw):
    with pytest.raises(p1_ab.P1Refused, match="no kid-done row|no run row"):
        _rec(tmp_path, True, False, **kw)
    assert not (tmp_path / "res.json").exists()


@pytest.mark.parametrize("kw", [dict(timed_out=True, rc=None), dict(rc=3), dict(sweep=[4242])])
def test_r1_a_red_run_cannot_be_recorded_as_landed_or_not_red(tmp_path, kw):
    for i, (landed, red) in enumerate(((False, False), (True, False), (True, True))):
        d = tmp_path / f"c{i}"
        d.mkdir()
        with pytest.raises(p1_ab.P1Refused, match="ran red"):
            _rec(d, landed, red, **kw)
    d = tmp_path / "ok"
    d.mkdir()
    k = _rec(d, False, True, **kw)["arms"][0]["kids"][0]
    assert (k["landed"], k["red"]) == (False, True)


def test_r1_a_clean_run_can_still_be_judged_red_by_the_gate(tmp_path):
    k = _rec(tmp_path, False, True)["arms"][0]["kids"][0]
    assert (k["landed"], k["red"]) == (False, True)


def test_r1_the_cli_has_no_typed_usd_or_secs(tmp_path, capsys):
    led, runs = _ledgers(tmp_path)
    for flag in ("--usd", "--secs"):
        with pytest.raises(SystemExit):
            p1_ab._mine("record", ["deepseek", LEAF, "--ledger", str(led), "--runs", str(runs), "--landed", "1", "--red", "0", flag, "9"],
                        CFG, tmp_path)
    capsys.readouterr()


def test_r2_live_kids_counts_minted_without_a_kid_done_other_than_this_pair():
    rows = [{"arm": "deepseek", "leaf": LEAVES[0], "done": True}, {"arm": "deepseek", "leaf": LEAVES[1]},
            {"arm": "deepseek", "leaf": LEAVES[2], "done": False}, {"arm": "deepseek", "leaf": LEAF}]
    assert p1_ab.live_kids(rows, "deepseek", LEAF) == 2
    assert p1_ab.live_kids(rows, "glm", LEAF) == 3          # a different pair: this deepseek row counts too


def _run_env(tmp_path, body="exit 0", **cfgkw):
    node = _fake_node(tmp_path, body=body)
    cfg, plan = _plan(tmp_path, node, **cfgkw)
    (tmp_path / "kidhome").mkdir(exist_ok=True)
    return cfg, plan


def _ledger_with(tmp_path, rows):
    led = tmp_path / "ledger.json"
    led.write_text(json.dumps(rows))
    return led


def test_r2_two_open_rows_refuse_the_run_and_one_open_row_allows_it(tmp_path):
    cfg, plan = _run_env(tmp_path)
    mine = {"arm": "deepseek", "leaf": LEAVES[0], "hash": "h0", "cap": 0.5}
    other = lambda n: {"arm": "deepseek", "leaf": LEAVES[n], "hash": f"h{n}", "cap": 0.5}
    runs = tmp_path / "runs.json"
    kw = dict(arm="deepseek", leaf=LEAVES[0], cfg=cfg, runs=runs, repo=tmp_path, plan=plan, gb=1.0)
    with pytest.raises(p1_ab.P1Refused, match="not started: 2 kids live"):
        p1_ab.run_logged(ledger=_ledger_with(tmp_path, [mine, other(1), other(2)]), **kw)
    assert not runs.exists()
    row = p1_ab.run_logged(ledger=_ledger_with(tmp_path, [mine, other(1), {**other(2), "done": True}]), **kw)
    assert row["rc"] == 0 and row["timed_out"] is False and row["sweep"] == [] and len(row["brief_sha256"]) == 64


def test_r2_a_pair_without_a_mint_row_or_already_run_is_refused_and_there_is_no_live_flag(tmp_path):
    cfg, plan = _run_env(tmp_path)
    runs = tmp_path / "runs.json"
    kw = dict(arm="deepseek", leaf=LEAVES[0], cfg=cfg, runs=runs, repo=tmp_path, plan=plan, gb=1.0)
    with pytest.raises(p1_ab.P1Refused, match="no mint row"):
        p1_ab.run_logged(ledger=_ledger_with(tmp_path, []), **kw)
    led = _ledger_with(tmp_path, [{"arm": "deepseek", "leaf": LEAVES[0], "hash": "h0", "cap": 0.5}])
    p1_ab.run_logged(ledger=led, **kw)
    with pytest.raises(p1_ab.P1Refused, match="a kid runs once"):
        p1_ab.run_logged(ledger=led, **kw)
    with pytest.raises(SystemExit):
        p1_ab._mine("run-kid", ["deepseek", LEAVES[0], "--ledger", str(led), "--runs", str(runs), "--key-file", "/k", "--worktree", "/w",
                                "--kid-home", "/h", "--live", "0"], CFG, tmp_path)


def _wait_gone(path, secs):
    import time
    end = time.time() + secs
    while time.time() < end:
        if path.exists():
            return False
        time.sleep(0.2)
    return True


def test_r4_a_background_job_of_a_kid_that_exits_zero_is_killed_at_exit(tmp_path):
    marker = tmp_path / "M"
    cfg, plan = _run_env(tmp_path, body=f"(sleep 2; touch {marker}) &\nexit 0")
    res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert res["rc"] == 0 and res["timed_out"] is False
    assert _wait_gone(marker, 3.5), "the background job outlived the kid"


def test_r4_the_group_kill_alone_catches_a_job_that_left_the_worktree_and_holds_no_fd(tmp_path):
    """The sweep matches by cwd and fd; a job that cd'd away and closed its fds is only reachable through the
    process group, so the kill at a normal exit has its own row."""
    marker = tmp_path / "M"
    cfg, plan = _run_env(tmp_path, body=f"( cd /; sleep 2; touch {marker} ) >/dev/null 2>&1 </dev/null &\nexit 0")
    res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert res["rc"] == 0 and res["sweep"] == [], res
    assert _wait_gone(marker, 3.5), "the job that left the worktree outlived the kid"


@pytest.mark.skipif(shutil.which("setsid") is None, reason="no setsid")
def test_r4_a_kid_that_escapes_its_session_and_hangs_is_swept_and_the_run_is_red(tmp_path):
    marker = tmp_path / "M"
    cfg, plan = _run_env(tmp_path, body=f"setsid sh -c 'sleep 2; touch {marker}' &\nsleep 30", timeout=1)
    res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
    assert res["timed_out"] is True and res["sweep"], res
    assert _wait_gone(marker, 3.5), "the escaped job was not killed"
    led, runs = tmp_path / "ledger.json", tmp_path / "runs.json"
    led.write_text(json.dumps([{"arm": "deepseek", "leaf": LEAF, "hash": "h1", "cap": 0.5, "usd": 0.1, "done": True}]))
    runs.write_text(json.dumps([{"arm": "deepseek", "leaf": LEAF, **{k: res[k] for k in ("rc", "secs", "timed_out", "sweep")}, "brief_sha256": "e" * 64}]))
    with pytest.raises(p1_ab.P1Refused, match="ran red"):
        p1_ab.record_from_ledgers(tmp_path / "r.json", CFG, arm="deepseek", leaf=LEAF, ledger=led, runs=runs, landed=True, red=False)


def test_r4_the_sweep_matches_by_cwd_and_by_open_fd_and_leaves_everything_else_alone(tmp_path):
    import time
    inside, outside = tmp_path / "kid", tmp_path / "elsewhere"
    inside.mkdir()
    outside.mkdir()
    held = inside / "held.txt"
    held.write_text("x")
    a = subprocess.Popen(["sleep", "30"], cwd=inside)                                          # cwd under the path
    b = subprocess.Popen(["sh", "-c", f"exec 3<{held}; sleep 30"], cwd=outside)                 # an open fd under it
    c = subprocess.Popen(["sleep", "30"], cwd=outside)                                          # unrelated
    try:
        time.sleep(0.5)
        hit, older = p1_ab.proc_sweep([inside])
        assert older == []
        a.wait(timeout=5)
        b.wait(timeout=5)
        assert a.pid in hit and b.pid in hit and c.pid not in hit and c.poll() is None
        assert os.getpid() not in hit
    finally:
        c.kill()
        a.kill()
        b.kill()


def test_p0_reads_a_to_f_and_goes_red_on_each_failure(brief_repo, tmp_path, monkeypatch):
    repo, cfg = brief_repo
    cfg["p1"]["prices"] = copy.deepcopy(CFG["p1"]["prices"])
    data = [{"id": m, "pricing": {"prompt": str(v["in_per_m"] / 1e6), "completion": str(v["out_per_m"] / 1e6)}}
            for m, v in cfg["p1"]["prices"]["models"].items()]
    mem = _slice_files(tmp_path / "ok") if (tmp_path / "ok").mkdir() is None else None
    modfile = repo / "extensions/agi/bin/p1_ab.py"
    modfile.parent.mkdir(parents=True)
    modfile.write_text(Path(p1_ab.__file__).read_text())
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "trunk carries p1_ab")
    cfg["p1"]["base"] = _git(repo, "rev-parse", "HEAD")           # the worktree under test sits on the frozen base
    env = tmp_path / ".env"
    env.write_text("x")
    wt = repo
    monkeypatch.setattr(success_metrics, "p1_segment", lambda root: "")
    run = lambda **kw: {n[0]: (ok, d) for n, ok, d in [(r[0].split()[0], r[1], r[2]) for r in p1_ab.p0_readings(
        cfg=cfg, repo=repo, worktree=kw.get("wt", wt), main_env=kw.get("env", env), fetch=lambda: kw.get("data", data), slice_files=kw.get("mem", mem), trunk="HEAD", module_file=kw.get("module", modfile))]}
    if os.geteuid() != 0:
        env.chmod(0o000)
    good = run()
    assert all(ok for ok, _ in good.values()), good
    assert good["g"][0] and "NOT EVALUATED" in good["g"][1]          # this uid cannot read the provisioning key
    assert good["b"][1].count("per M") == 2
    monkeypatch.setattr(success_metrics, "p1_segment", lambda root: "| p1: UNMEASURED(x)")
    assert run()["a"][0] is False
    monkeypatch.setattr(success_metrics, "p1_segment", lambda root: "")
    moved = [{**d, "pricing": {"prompt": "0.00001", "completion": "0.00001"}} for d in data]
    assert run(data=moved)["b"][0] is False and run(data=[])["b"][0] is False
    (tmp_path / "big").mkdir()
    assert run(mem=_slice_files(tmp_path / "big", anon=5.5))["c"][0] is False
    (tmp_path / "unr").mkdir()
    assert run(mem=_slice_files(tmp_path / "unr", stat=False))["c"][0] is False
    if os.geteuid() != 0:
        env.chmod(0o600)
        assert run()["d"][0] is False
    other = tmp_path / "other"
    other.mkdir()
    _git(other, "init", "-q")
    _git(other, "commit", "-q", "--allow-empty", "-m", "x")
    assert run(wt=other)["e"][0] is False
    off = tmp_path / "off.py"
    off.write_text(modfile.read_text() + " ")                         # one byte off the trunk's blob
    assert run(module=off)["f"][0] is False
    assert run(module=tmp_path / "nofile.py")["f"][0] is False
    api = Api(monkeypatch)                                           # the holder's side: g is evaluated, not deferred
    api.workspaces = ["ws-mine"]
    cfg.setdefault("spawn", {}).setdefault("credential", {})["workspace_id"] = "ws-mine"
    assert run()["g"][0] is True and "NOT EVALUATED" not in run()["g"][1]
    cfg["spawn"]["credential"]["workspace_id"] = "ws-stale-from-the-old-account"
    assert run()["g"][0] is False
    cfg["spawn"]["credential"]["workspace_id"] = "ws-mine"
    api.keys_status = 403
    assert run()["g"][0] is False


# --- the kill-path guard (SM's finding on GATE193): the sweep must never be pointed at HOME or the caller's own tree --

def test_guard_a_kid_home_that_is_home_or_outside_k_is_refused_before_any_spawn(arm):
    for bad in (arm["home"], arm["home"] / "k", arm["home"] / "elsewhere", Path("/tmp") / "kid", Path("/")):
        with pytest.raises(p1_ab.P1Refused, match="kid home|kill path"):
            _pre(arm, kid_home=bad)


def test_guard_a_kid_home_under_k_that_is_fresh_runs_and_one_that_is_not_fresh_does_not(arm):
    _pre(arm)                                                    # absent: fine
    arm["kid_home"].mkdir()
    _pre(arm)                                                    # present and empty: fine
    (arm["kid_home"] / "leftover").write_text("x")
    with pytest.raises(p1_ab.P1Refused, match="not a fresh"):
        _pre(arm)


def test_guard_a_symlinked_kid_home_that_escapes_k_is_refused(arm, tmp_path):
    (tmp_path / "away").mkdir()
    os.symlink(tmp_path / "away", arm["home"] / "k" / "ln")
    with pytest.raises(p1_ab.P1Refused, match="not a plain path|not under"):
        _pre(arm, kid_home=arm["home"] / "k" / "ln")


def test_guard_a_worktree_that_is_home_root_the_callers_repo_or_an_ancestor_of_cwd_is_refused(arm, monkeypatch, tmp_path):
    repo = Path(p1_ab.__file__).resolve().parents[3]
    for bad in (arm["home"], Path("/"), repo, repo.parent, Path.cwd(), Path.cwd().parent):
        with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
            _pre(arm, worktree=bad)
    inner = tmp_path / "cwdhere" / "deep"
    inner.mkdir(parents=True)
    monkeypatch.chdir(inner)
    with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
        _pre(arm, worktree=tmp_path / "cwdhere")


def test_guard_a_worktree_must_be_the_top_of_a_git_worktree_not_a_subdirectory_of_one(arm):
    sub = arm["wt"] / "sub"
    sub.mkdir()
    with pytest.raises(p1_ab.P1Refused, match="not the top of a git worktree"):
        _pre(arm, worktree=sub)


def test_guard_run_kid_and_proc_sweep_refuse_home_before_killing_anything(tmp_path, monkeypatch):
    """The typo case: `--kid-home $HOME`. A process of this uid sitting in HOME must survive."""
    import time
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    bystander = subprocess.Popen(["sleep", "30"], cwd=home)
    try:
        time.sleep(0.3)
        for bad in ([home], [tmp_path], [Path("/")]):
            with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
                p1_ab.proc_sweep(bad)
        node = _fake_node(tmp_path, body="exit 0")
        cfg = _cfg_node(node)
        plan = p1_ab.kid_plan(arm="deepseek", leaf=LEAVES[0], cfg=cfg, keyfile=tmp_path / "k.key", worktree=tmp_path / "wt",
                              kid_home=home, prompt="p", prefix=_prefix(tmp_path))
        with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
            p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
        assert bystander.poll() is None, "the sweep killed a bystander in HOME"
        assert not (home / ".p1-agent").exists() and not (home / "p1-deepseek-1.log").exists(), "it spawned before it refused"
    finally:
        bystander.kill()


def test_guard_the_pure_rule():
    u = p1_ab.unsafe_kill_path
    kw = dict(home="/h/me", cwd="/h/me/repo/sub", repos=("/h/me/repo",))
    for bad in ("/", "/h", "/h/me", "/h/me/repo", "/h/me/repo/sub"):
        assert u(bad, **kw), bad
    for ok in ("/h/me/k/kid1", "/h/me/wt", "/tmp/x"):
        assert u(ok, **kw) is None, ok


def test_guard_the_callers_repo_is_refused_even_when_the_cwd_is_elsewhere(arm, monkeypatch, tmp_path):
    """The repos check on its own: cwd moved away, the repo the caller runs from is still never a kill target."""
    monkeypatch.chdir(tmp_path)
    repo = Path(p1_ab.__file__).resolve().parents[3]
    with pytest.raises(p1_ab.P1Refused, match="repo the caller runs from"):
        _pre(arm, worktree=repo)
    with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
        _pre(arm, worktree=repo.parent)


def test_guard_a_worktree_that_is_or_contains_k_is_refused(arm):
    for bad in (arm["home"] / "k", arm["home"]):
        with pytest.raises(p1_ab.P1Refused, match="kill path refused"):
            _pre(arm, worktree=bad)


# --- S2: the sweep only kills what started after the kid; R1b: the run ledger append is under flock ----------------

def test_s2_an_older_process_under_the_kid_home_survives_is_named_and_the_run_reads_red(tmp_path):
    import time
    node = _fake_node(tmp_path, body="exit 0")
    cfg, plan = _plan(tmp_path, node)
    kid_home = Path(plan["env"]["HOME"])
    kid_home.mkdir(exist_ok=True)
    old = subprocess.Popen(["sleep", "30"], cwd=kid_home)             # exists BEFORE the kid starts
    try:
        time.sleep(0.3)
        res = p1_ab.run_kid(plan, cfg, live=0, gb=1.0)
        assert res["sweep"] == [] and res["older"] == [old.pid], res
        assert old.poll() is None, "an older process was killed"
        led, runs = tmp_path / "ledger.json", tmp_path / "runs.json"
        led.write_text(json.dumps([{"arm": "deepseek", "leaf": LEAF, "hash": "h1", "cap": 0.5, "usd": 0.1, "done": True}]))
        runs.write_text(json.dumps([{"arm": "deepseek", "leaf": LEAF, **{k: res[k] for k in ("rc", "secs", "timed_out", "sweep", "older")},
                                     "brief_sha256": "e" * 64}]))
        with pytest.raises(p1_ab.P1Refused, match=f"older=\\[{old.pid}\\]"):
            p1_ab.record_from_ledgers(tmp_path / "r.json", CFG, arm="deepseek", leaf=LEAF, ledger=led, runs=runs, landed=True, red=False)
    finally:
        old.kill()


def test_s2_a_process_started_after_the_kid_is_still_swept(tmp_path):
    import time
    inside = tmp_path / "kid"
    inside.mkdir()
    since = p1_ab.boot_ticks()
    time.sleep(0.1)
    late = subprocess.Popen(["sleep", "30"], cwd=inside)
    try:
        time.sleep(0.3)
        hit, older = p1_ab.proc_sweep([inside], since=since)
        assert hit == [late.pid] and older == []
        late.wait(timeout=5)
    finally:
        late.kill()


def test_r1b_two_overlapping_kids_each_keep_their_run_row(tmp_path):
    """An overlap under max_live 2: with a read at start and a write at the end, B's row erased A's (or the reverse)."""
    from concurrent.futures import ThreadPoolExecutor
    runs, led = tmp_path / "runs.json", tmp_path / "ledger.json"
    led.write_text(json.dumps([{"arm": "deepseek", "leaf": LEAVES[0], "hash": "h0", "cap": 0.5},
                               {"arm": "deepseek", "leaf": LEAVES[1], "hash": "h1", "cap": 0.5}]))
    jobs = []
    for i in (0, 1):
        d = tmp_path / f"kid{i}"
        d.mkdir()
        node = _fake_node(d, body="sleep 1")
        cfg, plan = _plan(d, node)
        (d / "kidhome").mkdir(exist_ok=True)
        jobs.append((LEAVES[i], cfg, plan))
    with ThreadPoolExecutor(2) as ex:
        futs = [ex.submit(p1_ab.run_logged, arm="deepseek", leaf=leaf, cfg=cfg, ledger=led, runs=runs, repo=tmp_path, plan=plan, gb=1.0)
                for leaf, cfg, plan in jobs]
        rows = [f.result(timeout=60) for f in futs]
    assert {r["leaf"] for r in rows} == {LEAVES[0], LEAVES[1]}
    assert sorted(r["leaf"] for r in json.loads(runs.read_text())) == sorted([LEAVES[0], LEAVES[1]])


def test_r1b_a_pair_that_got_a_run_row_while_it_ran_is_refused_not_overwritten(tmp_path):
    runs = tmp_path / "runs.json"
    row = {"arm": "deepseek", "leaf": LEAVES[0], "rc": 0, "secs": 1, "timed_out": False, "sweep": [], "older": [], "brief_sha256": "e" * 64}
    p1_ab._append_run(runs, row)
    with pytest.raises(p1_ab.P1Refused, match="got a run row while it ran"):
        p1_ab._append_run(runs, {**row, "rc": 9})
    assert json.loads(runs.read_text()) == [row]


def test_r1b_eight_simultaneous_appends_all_land_even_with_the_read_to_write_window_widened(tmp_path, monkeypatch):
    """Deterministic: each append sleeps between its read and its write. Without the flock the later writers
    overwrite the earlier ones with a list that never saw them; with it they take turns and every row survives."""
    import time
    from concurrent.futures import ThreadPoolExecutor
    real_runs = p1_ab._runs

    def slow_runs(path):
        rows = real_runs(path)
        time.sleep(0.05)
        return rows

    monkeypatch.setattr(p1_ab, "_runs", slow_runs)
    runs = tmp_path / "runs.json"
    rows = [{"arm": "deepseek", "leaf": f"goal:x{i}", "rc": 0, "secs": 1, "timed_out": False, "sweep": [], "older": [],
             "brief_sha256": "e" * 64} for i in range(8)]
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda r: p1_ab._append_run(runs, r), rows))
    assert sorted(r["leaf"] for r in real_runs(runs)) == sorted(r["leaf"] for r in rows)
