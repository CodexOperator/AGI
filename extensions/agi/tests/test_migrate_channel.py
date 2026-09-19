# test_migrate_channel.py -- SM.123 QUICK-MIGRATE, source-side slice.
#
# The ONE cross-box `migrate` record kind plus `rotate.py migrate`'s plan:
# one record dict, one signed file under the season comms root, refusals by
# name, and a --dry-run that touches nothing. The carryover commit, the ref
# push, the target receive and the seated line are named steps, not this
# round's bytes.
import argparse
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import migrate_channel, rotate  # noqa: E402
import send  # noqa: E402 -- the module rotate's lazy `import send` resolves


def _rec(**kw):
    base = dict(post="p", mode="rotate", source_box="boxA", target_box="boxB",
                branch="refs/agi/posts/p", tip="abc123",
                session_id=None, ts="2026-09-18T12:00:00+00:00")
    base.update(kw)
    return migrate_channel.record(**base)


def _ns(**kw):
    base = dict(post=None, to=None, mode="rotate", session_id=None, tip=None,
                dry_run=False, root=None)
    base.update(kw)
    return argparse.Namespace(**base)


def test_record_refuses_unknown_mode_by_name():
    with pytest.raises(ValueError, match="unknown migrate mode"):
        _rec(mode="teleport")


def test_record_name_is_aliases_only():
    name = migrate_channel.record_name(_rec())
    assert name.endswith("-p--boxB.md")
    assert "/" not in name and ":" not in name


def test_format_parse_roundtrips_all_fields_and_rejects_other_kinds():
    rec = _rec(session_id="sess-1")
    parsed = migrate_channel.parse_record(migrate_channel.format_record(rec))
    assert parsed == rec
    assert migrate_channel.parse_record("---\nkind: dm\nmode: rotate\n---\n") is None
    assert migrate_channel.parse_record("no frontmatter") is None


def test_signed_record_verifies_and_a_tampered_byte_does_not(tmp_path):
    minted = send._mint_seat_key(tmp_path, "p", "ed25519")
    assert minted is not None
    _path, pub = minted
    text = migrate_channel.format_record(_rec(), sign_root=tmp_path, signer="p")
    assert "sig: ed25519:" in text
    assert migrate_channel.verify_record(text, pub.hex()) is True
    assert migrate_channel.verify_record(text.replace("rotate", "fork", 1),
                                         pub.hex()) is False
    assert migrate_channel.verify_record(
        migrate_channel.format_record(_rec()), pub.hex()) is False


def test_dry_run_prints_every_step_and_touches_nothing(tmp_path, monkeypatch,
                                                       capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB", "--dry-run",
                      "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "step 1:" in out and "step 6:" in out
    assert "dry-run: nothing touched" in out
    assert not (tmp_path / "comms").exists()


def test_same_box_refused_by_name(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxA", "--dry-run",
                      "--root", str(tmp_path)])
    assert rc == 1
    assert "REFUSED" in capsys.readouterr().out


def test_unknown_mode_refused_by_name(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.cmd_migrate(_ns(post="p", to="boxB", mode="teleport"), tmp_path)
    assert rc == 1
    assert "unknown mode" in capsys.readouterr().out


def test_apply_writes_one_signed_record(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    assert send._mint_seat_key(tmp_path, "p", "ed25519") is not None
    fake_comms = tmp_path / "comms"
    monkeypatch.setattr(send, "comms_root",
                        lambda root, override=None: fake_comms)
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB",
                      "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    files = sorted((fake_comms / "migrate").glob("*.md"))
    assert len(files) == 1
    parsed = migrate_channel.parse_record(files[0].read_text())
    assert parsed["mode"] == "rotate"
    assert parsed["source_box"] == "boxA" and parsed["target_box"] == "boxB"
    assert "signed with the p key" in out
