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

    def __init__(self, monkeypatch, *, stored_limit="echo", stored_expiry="echo", sent_expiry="echo"):
        self.sent, self.revoked, self.rows, self.patched = [], [], [], []
        self.stored_limit, self.stored_expiry, self.sent_expiry = stored_limit, stored_expiry, sent_expiry
        monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda root=None: "sk-prov")
        monkeypatch.setattr(provisioning, "_call", self.call)
        monkeypatch.setattr(provisioning, "can_fund", lambda root=None, **k: (True, None))
        monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: list(self.rows))

    def call(self, method, url, key, payload=None, timeout=30):
        if method == "DELETE":
            self.revoked.append(url.rsplit("/", 1)[-1])
            return 200, {}
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
        return 201, {"key": f"sk-{h}", "data": {"hash": h, "expires_at": got}}


def test_a_mint_sends_the_cap_reads_it_back_and_writes_the_ledger(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    led = tmp_path / "led.json"
    k = p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=led)
    assert api.sent[0]["limit"] == 0.5 and k.secret == "sk-h1"
    assert json.loads(led.read_text()) == [{"arm": "glm", "leaf": LEAVES[0], "hash": "h1", "cap": 0.5}]


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
def arm(tmp_path):
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
    return dict(prefix=pre, keydir=keydir, wt=wt, cfg=cfg, env=env)


def _pre(a, **over):
    kw = dict(arm="deepseek", leaf=LEAVES[0], prefix=a["prefix"], cfg=a["cfg"], kid_uid=KID,
              keydir=a["keydir"], worktree=a["wt"])
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
    with pytest.raises(p1_ab.P1Refused, match="frozen base"):
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


def test_a_missed_disable_is_a_red_and_the_file_is_still_removed(monkeypatch, tmp_path):
    api = Api(monkeypatch, stored_limit="ignore-disable")
    k = p1_ab.mint_capped(arm="glm", leaf=LEAVES[0], cfg=CFG, ledger=tmp_path / "l.json")
    f = tmp_path / "k"
    f.write_text(k.secret)
    problems = p1_ab.end_arm([{"hash": k.key_hash, "file": str(f)}])
    assert any("not disabled" in x for x in problems) and not f.exists()


def test_a_key_that_vanished_from_the_listing_is_a_red(monkeypatch, tmp_path):
    api = Api(monkeypatch)
    monkeypatch.setattr(provisioning, "list_keys", lambda root=None, workspace_id=None: [])
    problems = p1_ab.end_arm([{"hash": "gone", "file": str(tmp_path / "none")}])
    assert any("absent" in x for x in problems)


def test_a_scratch_land_that_creates_a_shadow_bin_file_reads_red():
    assert p1_ab.scratch_land_problems(["extensions/x.py", ".agi/nodes/goal/g.md"], CFG) == []
    for bad in (".agi/bin/render-context.py", ".agi/bin/snapshot-build-site.py"):
        assert p1_ab.scratch_land_problems(["a.py", bad], CFG) == [f"scratch land creates {bad}: forbidden"]


# --- the spawn gate ------------------------------------------------------------------

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
    assert any("not disabled" in x for x in out["problems"]) and not Path(k["file"]).exists()
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
def test_the_cli_prints_json_without_the_secret_and_exits_nonzero_on_a_refusal(monkeypatch, tmp_path, capsys):
    api = Api(monkeypatch)
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
