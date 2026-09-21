"""hypothesis:l3-pi-install-patch-not-durable -- make the edit-tool forgiveness durable.

`hypothesis:l3-pi-edit-tool-edits-array` (L3.38) fixed a defect where the pi
`edit` tool rejected two mis-shaped `edits` arguments (a single JSON string,
or wrapped one level too deep as `[{ edits: [...] }]`), costing a kid a turn
each. The fix landed as a patch to `prepareEditArguments` in the SHARED pi
install's `dist/core/tools/edit.js` -- a file this repo does NOT track, does
NOT version, and does NOT own. A `pi` upgrade silently reverts it, and the
only symptom is every kid quietly losing a turn again to the same defect. The
repo's own `test_edit_tool_forgiveness.py` drives the INSTALLED tool, so it
only goes red on the day the suite runs -- not before a turn is wasted.

This module is the durable, repo-owned half. It is a spawn-time/adapter-load
gate wired into `pi_adapter.build_command` (`goal:g4.6` -- the adapter is
where every pi spawn funnels, including restarts). At each spawn it checks the
INSTALLED edit tool:

  * marker present          -> no-op, spawn proceeds. (The common case.)
  * marker ABSENT (an upgrade dropped it) -> re-apply the patch in place via
    an idempotent, anchor-backed, atomic rewrite (temp file + os.replace), so
    the very next spawn self-heals instead of a kid paying a wasted turn.
  * marker ABSENT and re-apply cannot be anchored (pi refactored the tool so
    our splice points are gone) -> return a FAIL status; the caller raises
    LOUDLY naming the fix, so the upgrade cannot pass unnoticed in the silent
    direction the hypothesis named.

Why reboot in place and not ship a vendored copy: the patch is an additive,
anchor-backed splice (a self-contained `_normalizeEditsShapes` helper plus one
routing short-circuit at the top of `prepareEditArguments`). Function
declarations hoist in JS, so inserting the helper before `prepareEditArguments`
is safe regardless of where the old empty-branch sat. Both splice anchors
(`function prepareEditArguments(input) {` and `const args = input;`) are
line-start constructs that have been stable across the installed versions this
project has run; if a future pi renames them, the anchor MISSES and we return
FAIL rather than corrupting a vendor file -- the safe degradation. The gate is
idempotent (marker check before any write) and atomic (no partial files under
concurrent spawns). The behavioural guarantee -- that a re-applied tool
actually normalizes the two mis-shapes -- is carried by the existing
`test_edit_tool_forgiveness.py`, which already probes the INSTALLED tool; this
module restores the install so that probe keeps passing.

`AGI_PI_FORGIVENESS_BYPASS=1` turns the gate off entirely, for an unusual
environment that cannot run it.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

#: The one identifier the whole patch pivots on. Its presence in edit.js means
#: the forgiveness is installed (whether by us, by a prior re-apply, or by a
#: manually applied patch) and the gate is a no-op.
_MARKER = "_normalizeEditsShapes"

#: Self-contained helper, verbatim from the L3.38 patch. Function declarations
#: hoist, so splicing it in before `prepareEditArguments` is safe even though
#: the original patch placed it after.
_HELPER_FN = """\
function _normalizeEditsShapes(input) {
    let edits = input.edits;
    if (typeof edits === "string") {
        try {
            edits = JSON.parse(edits);
        }
        catch {
            return input;
        }
    }
    if (Array.isArray(edits) &&
        edits.length > 0 &&
        edits.every((e) => e && typeof e === "object" && Array.isArray(e.edits))) {
        const flattened = [];
        for (const wrap of edits) {
            flattened.push(...wrap.edits);
        }
        edits = flattened;
    }
    if (!Array.isArray(edits)) {
        return input;
    }
    const rest = { ...input };
    rest.edits = edits;
    return rest;
}
"""

#: The splice anchors. Both are line-start constructs that identify the top of
#: `prepareEditArguments` and the line after its input guard. If either is no
#: longer present, the re-apply refused to run (FAIL) rather than guess.
_FN_ANCHOR = "function prepareEditArguments(input) {"
_ARGS_ANCHOR = "const args = input;"

#: The routing short-circuit spliced right after `const args = input;`. It
#: normalizes any normalizable mis-shape and returns the fixed args; on a
#: single-edit call (no `edits` array) `_normalizeEditsShapes` returns the SAME
#: object, so `_pi_norm !== args` is false and the original single-edit path
#: continues untouched. Choosing a temp var name with a long prefix keeps the
#: splice from colliding with pi's own locals.
_ROUTING_LINE = "    const _agi_edit_norm = _normalizeEditsShapes(args);\n" \
                "    if (_agi_edit_norm && _agi_edit_norm !== args) return _agi_edit_norm;"

#: Installed-package search roots, in priority order (same resolution the edit-
#: forgiveness TEST uses). The pi binary on PATH wins; the engine's declared
#: default path is the fallback.
_DEFAULT_BASES = (Path("/home/ubuntu/.npm-global/lib/node_modules"),)


def resolve_edit_js():
    """Locate the INSTALLED pi edit tool's edit.js, or None if pi (or node) is
    not resolvable. Returns (editJs, validationJs) mirroring the repo test's
    resolver, so the gate and the test agree on what "installed" means."""
    if not shutil.which("node"):
        return None
    candidates = []
    pi_bin = shutil.which("pi")
    if pi_bin:
        candidates.append(Path(pi_bin).resolve().parent.parent / "lib" / "node_modules")
    candidates.extend(_DEFAULT_BASES)
    for base in candidates:
        pkg = base / "@mariozechner" / "pi-coding-agent"
        edit_js = pkg / "dist" / "core" / "tools" / "edit.js"
        if not edit_js.exists():
            continue
        validation_js = (
            pkg / "node_modules" / "@mariozechner" / "pi-ai"
            / "dist" / "utils" / "validation.js"
        )
        if validation_js.exists():
            return edit_js, validation_js
    return None


def _reapply(code: str) -> str:
    """Return a patched copy of `code` that carries the forgiveness, or raise
    a ValueError named with the offending anchor when re-apply cannot be
    anchored safely. Raises BEFORE any write so a vendor file is never
    corrupted by a guess."""
    for anchor, what in ((_FN_ANCHOR, "prepareEditArguments"), (_ARGS_ANCHOR, "const args = input;")):
        if code.count(anchor) != 1:
            raise ValueError(
                f"cannot re-apply edit-tool forgiveness: expected exactly one "
                f"{what!r} anchor in edit.js (found {code.count(anchor)}). "
                f"pi refactored the tool; the repo cannot auto-patch it."
            )
    patched = code.replace(_FN_ANCHOR, _HELPER_FN + _FN_ANCHOR, 1)
    patched = patched.replace(
        _ARGS_ANCHOR,
        _ARGS_ANCHOR + "\n" + _ROUTING_LINE,
        1,
    )
    # Structural self-check on the CLOSED string, mirroring the claim the
    # re-application makes: the helper and the routing must both be present,
    # and the anchors must still be intact (no double-splice).
    for needle in (_HELPER_FN.splitlines()[0],
                   _ROUTING_LINE.splitlines()[0],
                   _ARGS_ANCHOR,
                   _FN_ANCHOR):
        if patched.count(needle) != 1:
            raise ValueError(
                f"structural self-check failed after re-apply: {needle!r} "
                f"not exactly once. Refusing to write a broken vendor file."
            )
    return patched


def ensure_pi_edit_forgiveness(edit_js: Path | None = None) -> tuple[str, str]:
    """Gate the installed pi edit tool's forgiveness patch.

    idempotent + atomic + loud. Returns (status, detail):

      ("skip", ...)    pi (or node) is not resolvable; nothing to guard on
                       this machine. Callers should NOT raise.
      ("ok", ...)      the marker is present (an L3.38 patch, ours or a
                       human's, is installed); no write.
      ("patched", ...) the marker was ABSENT (an upgrade dropped it); the
                       patch was re-applied atomically; the next spawn is
                       shielded. Callers should warn, not raise.
      ("fail", ...)    the marker was ABSENT and re-apply could not be done
                       safely. Callers MUST raise loudly, naming the fix so
                       the upgrade cannot pass unnoticed.

    Set AGI_PI_FORGIVENESS_BYPASS=1 to turn the gate off entirely.
    """
    if os.environ.get("AGI_PI_FORGIVENESS_BYPASS") == "1":
        return ("skip", "AGI_PI_FORGIVENESS_BYPASS=1")
    if edit_js is None:
        resolved = resolve_edit_js()
        if resolved is None:
            return ("skip", "pi edit tool (node) not resolvable; nothing to guard")
        edit_js, _validation = resolved
    edit_js = Path(edit_js)
    if not edit_js.is_file():
        return ("fail", f"configured edit tool not found at {edit_js}")
    try:
        code = edit_js.read_text(encoding="utf-8")
    except OSError as exc:
        return ("fail", f"could not read {edit_js}: {exc}")

    if _MARKER in code:
        return ("ok", f"forgiveness present at {edit_js}")

    try:
        patched = _reapply(code)
    except ValueError as exc:
        return ("fail", str(exc))

    # Atomic: write to a temp file in the SAME directory, then swap, so a
    # concurrent spawn reading the file sees either the old or the new bytes,
    # never a half-written splice.
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=str(edit_js.parent),
            prefix=".edit.js.", suffix=".tmp", delete=False,
        ) as fh:
            tmp = Path(fh.name)
            fh.write(patched)
        os.replace(str(tmp), str(edit_js))
        tmp = None
    except OSError as exc:
        if tmp is not None:
            try:
                tmp.unlink()
            except OSError:
                pass
        return ("fail", f"could not atomically re-apply patch to {edit_js}: {exc}")

    return ("patched", f"re-applied edit-tool forgiveness to {edit_js} (was dropped)")


def is_bypassed() -> bool:
    return os.environ.get("AGI_PI_FORGIVENESS_BYPASS") == "1"


def _usage() -> str:
    return (
        "pi_edit_forgiveness.py -- gate the pi install's edit-tool forgiveness.\n"
        "The L3.38 patch (hypothesis:l3-pi-install-patch-not-durable) shields kids "
        "from the pi `edit` tool rejecting mis-shaped `edits`. It lives in the SHARED\n"
        "pi install outside this repo, so a `pi` upgrade silently drops it. Wired\n"
        "into pi_adapter.build_command, this gate re-applies the patch at every\n"
        "spawn when an upgrade removed it -- or fails loudly naming the fix.\n"
        "\n"
        "usage: pi_edit_forgiveness.py [--check] [--edit-js PATH]\n"
        "  (no args)        re-apply when missing (same gate the spawn runs)\n"
        "  --check          print install status; exit 0 only on ok/re-applied\n"
        "  --edit-js PATH   target a specific edit.js (operators/tests)\n"
        "  --help           this message\n"
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--help" in args or "-h" in args:
        print(_usage())
        return 0
    path = None
    if "--edit-js" in args:
        i = args.index("--edit-js")
        if i + 1 >= len(args):
            print("--edit-js needs a path", file=sys.stderr)
            return 2
        path = args[i + 1]
    status, detail = ensure_pi_edit_forgiveness(path)
    print(f"{status}: {detail}")
    if status == "fail":
        print("FIX: repair pi upstream, or re-apply the _normalizeEditsShapes "
              "patch (see extensions/agi/bin/pi_edit_forgiveness.py).",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())