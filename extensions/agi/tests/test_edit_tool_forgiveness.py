"""L3.37/L3.38 — the `edit` tool refuses two mis-shaped `edits` arguments.

Two independent kids in one round (L3.37) each spent a turn with the pi
`edit` tool rejecting `edits` passed as a single JSON string, and one wrapped
a level too deep as `[{ edits: [...] }]`. The tool's `prepareArguments` is
now forgiving of both (normalized to the documented array shape *before*
schema validation, so AJV sees a valid array). This test pins that forgiveness
against the *installed* pi tool over the real `prepareArguments` +
`validateToolArguments` path.

It shells out to node because the repo suite is Python and the tool is npm JS.
Where pi (or node) is not installed the whole file skips rather than failing
the suite on unrelated machines; on a machine that actually runs kids it is
live, which is the environment it protects.

DURABILITY (hypothesis:l3-pi-install-patch-not-durable): this probe only
DETECTS a dropped patch once it is run; it does not re-apply it. The spawn-
time gate in `bin/pi_edit_forgiveness.py` (wired into `pi_adapter.build_command`)
re-applies the patch at the first spawn after a `pi` upgrade drops it, or
fails loudly naming the fix -- so the probe keeps passing because the install
is kept patched, not merely checked.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_JS = r"""
import { createEditToolDefinition } from "__EDIT_JS__";
import { validateToolArguments } from "__VALIDATION_JS__";
const def = createEditToolDefinition("/tmp");
const cases = __CASES__;
const out = [];
for (const [name, raw] of Object.entries(cases)) {
    let prepared = raw;
    try {
        if (def.prepareArguments) prepared = def.prepareArguments(raw);
        const validated = validateToolArguments(
            { parameters: def.parameters }, { name: "edit", arguments: prepared });
        const edits = validated.edits;
        out.push({
            name,
            accepted: Array.isArray(edits)
                && edits.every((e) => typeof e === "object"
                    && typeof e.oldText === "string"
                    && typeof e.newText === "string"),
        });
    } catch (e) {
        out.push({ name, accepted: false, error: String(e).split("\n")[0] });
    }
}
console.log(JSON.stringify(out));
"""


def _pi_package_files():
    """Locate the installed pi edit tool + the shared ajv validation module.

    Returns (editJs, validationJs) or None if pi is not installed at a
    resolvable location (the test then skips).
    """
    if not shutil.which("node"):
        return None
    # Resolve the pi package from the pi binary on PATH, falling back to the
    # engine's declared default location.
    candidates = []
    pi_bin = shutil.which("pi")
    if pi_bin:
        candidates.append(Path(pi_bin).resolve().parent.parent / "lib" / "node_modules")
    candidates.append(Path("/home/ubuntu/.npm-global/lib/node_modules"))
    for base in candidates:
        pkg = base / "@mariozechner" / "pi-coding-agent"
        if not (pkg / "dist" / "core" / "tools" / "edit.js").exists():
            continue
        edit_js = pkg / "dist" / "core" / "tools" / "edit.js"
        validation_js = (
            pkg / "node_modules" / "@mariozechner" / "pi-ai"
            / "dist" / "utils" / "validation.js"
        )
        if validation_js.exists():
            return edit_js, validation_js
    return None


pytestmark = pytest.mark.skipif(
    _pi_package_files() is None,
    reason="installed pi package (node) not resolvable; nothing to pin",
)


def test_edit_tool_forgives_stringified_and_nested_edits():
    """The `edit` tool accepts canonical, stringified-`edits`, and
    singly-nested `edits` — the two shapes that cost L3.37 kids a turn each."""
    edit_js, validation_js = _pi_package_files()
    cases = {
        "canonical": {"path": "x.txt", "edits": [{"oldText": "a", "newText": "b"}]},
        "stringified": {
            "path": "x.txt",
            "edits": json.dumps([{"oldText": "a", "newText": "b"}]),
        },
        "nested": {
            "path": "x.txt",
            "edits": [{"edits": [{"oldText": "a", "newText": "b"}]}],
        },
    }
    script = (
        _JS.replace("__EDIT_JS__", str(edit_js))
        .replace("__VALIDATION_JS__", str(validation_js))
        .replace("__CASES__", json.dumps(cases))
    )
    proc = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        pytest.fail(f"node probe failed: {proc.stderr}")
    results = json.loads(proc.stdout.strip())
    by_name = {r["name"]: r for r in results}
    assert set(by_name) == set(cases), f"probe did not cover all cases: {results}"
    for name, r in by_name.items():
        assert r["accepted"], (
            f"edit tool rejected {name!r} edits shape — "
            f"it must be normalized to the canonical array before validation: "
            f"{r.get('error', '')}"
        )