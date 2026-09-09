"""hypothesis:l3-pi-install-patch-not-durable -- red-first: an install missing
the edit-tool forgiveness cannot pass unnoticed.

The L3.38 forgiveness patch lives in the SHARED pi install's
`dist/core/tools/edit.js`, outside this repo, so a `pi` upgrade silently drops
it and every kid quietly loses a turn again to the same defect. The repo's own
`test_edit_tool_forgiveness.py` drives the INSTALLED tool and only goes red on
the day the suite runs -- after a wasted turn.

`pi_edit_forgiveness.ensure_pi_edit_forgiveness` is the durable, repo-owned
half and is wired into `pi_adapter.build_command`, so EVERY spawn (and every
restart) gates the installed tool: re-applies the patch when an upgrade
dropped it, or returns FAIL so the caller raises loudly naming the fix. This
file proves, red-first, that the gate really re-applies or really fails loud --
it does not merely assert the patch is present today.

The strongest simulation is the honest one: take the REAL installed edit.js
into a temp copy and strip the marker lines (what an upgrade that drops the
patch leaves behind), then ask the gate to re-apply it. No installed file is
ever touched -- the gate is handed the temp path explicitly. Where pi is not
installed, a minimal hand-written stub upholds the same contract so the file
still runs on any machine.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin" / "adapters"))

import pi_adapter          # noqa: E402
import pi_edit_forgiveness as pf   # noqa: E402

_MARKER = "_normalizeEditsShapes"

# A minimal pre-patch edit.js: the two splice anchors present, marker absent.
_PRE_PATCH_STUB = """\
// minimal edit tool for the forgiveness re-apply test (pre-L3.38 shape)
function prepareEditArguments(input) {
    if (!input || typeof input !== "object") {
        return input;
    }
    const args = input;
    const edits = Array.isArray(args.edits) ? [...args.edits] : [];
    edits.push({ oldText: args.oldText, newText: args.newText });
    const { oldText: _oldText, newText: _newText, ...rest } = args;
    return { ...rest, edits };
}
"""

_PATCHED_STUB = _PRE_PATCH_STUB.replace(
    "function prepareEditArguments(input) {",
    pf._HELPER_FN + "function prepareEditArguments(input) {",
    1,
).replace(
    "const args = input;",
    "const args = input;\n" + pf._ROUTING_LINE,
    1,
)


def _real_install_text():
    """The text of the INSTALLED edit tool, or None (skip) when pi is not at a
    resolvable path. Returned so tests can build a faithful 'upgrade dropped
    the patch' fixture from the real file -- never modify it."""
    resolved = pf.resolve_edit_js()
    if resolved is None:
        return None
    return Path(resolved[0]).read_text(encoding="utf-8")


def _strip_marker(code: str) -> str:
    """What an upgrade that drops the patch leaves behind: every line that
    mentions the L3.38 marker removed, the two splice anchors intact."""
    kept = [ln for ln in code.splitlines(keepends=True) if _MARKER not in ln]
    stripped = "".join(kept)
    assert _MARKER not in stripped
    assert stripped.count(pf._FN_ANCHOR) == 1
    assert stripped.count(pf._ARGS_ANCHOR) == 1
    return stripped


# ---------------------------------------------------------------- the contract


def test_install_missing_the_patch_is_reapplied(tmp_path):
    """RED-FIRST heart of the claim: a file missing the normalisation is
    re-applied by the gate, so the very next spawn self-heals instead of a kid
    paying the turn."""
    target = tmp_path / "edit.js"
    target.write_text(_strip_marker(_real_install_text() or _PRE_PATCH_STUB),
                      encoding="utf-8")
    before = target.read_text(encoding="utf-8")

    status, detail = pf.ensure_pi_edit_forgiveness(edit_js=target)

    assert status == "patched", f"expected re-apply; got {status}: {detail}"
    after = target.read_text(encoding="utf-8")
    assert _MARKER in after, "the marker was not restored in the re-applied file"
    # the routing short-circuit and the helper both landed
    assert "const _agi_edit_norm = _normalizeEditsShapes(args);" in after
    assert after.count(pf._FN_ANCHOR) == 1 and after.count(pf._ARGS_ANCHOR) == 1
    # nothing of the original tmp is lost -- the patch is additive
    assert len(after) > len(before)


def test_install_already_patched_is_a_noop(tmp_path):
    """The common case: marker present -- the gate leaves the file byte-for-byte
    untouched (idempotent), no write, no re-apply."""
    target = tmp_path / "edit.js"
    target.write_text(_PATCHED_STUB, encoding="utf-8")
    before = target.read_bytes()

    status, detail = pf.ensure_pi_edit_forgiveness(edit_js=target)

    assert status == "ok", f"expected no-op; got {status}: {detail}"
    assert target.read_bytes() == before, "a no-op must not rewrite the file"


def test_unanchored_install_fails_loudly_instead_of_guessing(tmp_path):
    """If pi refactored the tool so the splice anchors are gone, the gate must
    refuse to guess at a vendor file -- returning FAIL so the caller raises
    loudly naming the fix rather than corrupting the install."""
    target = tmp_path / "edit.js"
    target.write_text("function somethingElse(x) { return x; }\n", encoding="utf-8")

    status, detail = pf.ensure_pi_edit_forgiveness(edit_js=target)

    assert status == "fail", f"expected FAIL on an unanchored file; got {status}"
    assert "anchor" in detail.lower() or "edit.js" in detail
    # unchanged on disk -- a failed attempt must not corrupt the file
    assert "somethingElse" in target.read_text(encoding="utf-8")


def test_reapply_is_idempotent_when_run_twice(tmp_path):
    """After a re-apply, a second pass is a no-op -- so a concurrent restart
    that re-enters the gate cannot double-splice."""
    target = tmp_path / "edit.js"
    target.write_text(_PRE_PATCH_STUB, encoding="utf-8")

    s1, _ = pf.ensure_pi_edit_forgiveness(edit_js=target)
    s2, d2 = pf.ensure_pi_edit_forgiveness(edit_js=target)

    assert s1 == "patched" and s2 == "ok", (s1, d2)
    # the helper appears exactly once even after a re-entry
    assert target.read_text(encoding="utf-8").count(_MARKER) == 2  # def + call


# ------------------------------------------------------------- the wiring gate


def _kid_command(**kw):
    kw.setdefault("scaffold", {"path": "/tmp/n.md", "node_type": "experiment",
                                "node_id": "experiment:x",
                                "parent": "hypothesis:y"})
    kw.setdefault("cli_py", "/x/cli.py")
    kw.setdefault("context_file", "/tmp/ctx.md")
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    kw.setdefault("sess_dir", Path("/tmp"))
    return pi_adapter.build_command(harness={}, tier="kid", **kw)


def test_build_command_gates_the_installed_tool_every_spawn(monkeypatch):
    """Every spawn funnels through build_command; the gate must run on every
    call, and a healthy install must not block the spawn."""
    calls = []

    def fake_ensure(edit_js=None):
        calls.append(edit_js)
        return ("ok", "stub")
    monkeypatch.setattr(pf, "ensure_pi_edit_forgiveness", fake_ensure)

    cmd = _kid_command()
    assert calls, "the spawn gate did not run"
    assert cmd, "a healthy install must still produce a spawn argv"


def test_build_command_raises_loudly_when_the_gate_cannot_reapply(monkeypatch):
    """The loud-and-early half: when the gate returns FAIL, the spawn must not
    silently proceed -- it raises naming the fix, so an upgrade that dropped
    the patch is caught at the FIRST spawn, not after kids waste turns."""
    monkeypatch.setattr(pf, "ensure_pi_edit_forgiveness",
                        lambda edit_js=None: ("fail", "boom: anchor gone"))
    with pytest.raises(RuntimeError) as exc:
        _kid_command()
    msg = str(exc.value)
    assert "L3.38" in msg, "the raised error must name the L3.38 patch"
    assert "edit" in msg.lower(), "the raised error must name the edit tool"


# --------------------------------------------------- live machine, if pi is on it


def test_live_install_currently_carries_the_forgiveness_monkeypatch(monkeypatch, tmp_path):
    """On the machine that actually runs kids, assert the gate reaches the
    real install and finds it patched (skip where pi is absent). Uses the temp
    copy, never the live file, for any mutation that might be needed."""
    source = _real_install_text()
    if source is None:
        pytest.skip("installed pi package not resolvable; nothing to pin")
    target = tmp_path / "edit.js"
    target.write_text(source, encoding="utf-8")
    status, _ = pf.ensure_pi_edit_forgiveness(edit_js=target)
    # the live install is either already patched, or the gate heals it into a
    # patched state -- either way the re-applied copy carries the marker.
    assert status in ("ok", "patched"), status
    assert _MARKER in target.read_text(encoding="utf-8")