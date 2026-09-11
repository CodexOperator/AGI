"""FALSIFIER for the L4.259 fix-only round (sanctuary-helper 3baf36): the
golden-web page is broken a SECOND time. Proves, against the PINNED three r160
bytes with a DOM stub:

  * right-drag / middle-drag PAN actually moves the camera (the pre-fix pan()
    used the ONE-argument THREE cross — removed in r160 — returning the zero
    vector, so pan was a live no-op);
  * the node PICKER ignores a node's phantom z=0 projection (pre-fix
    updatePick() projected every node at BOTH planes, showing a tooltip for a
    mesh that is not there) and picks at its OWN layer's z.

Nothing here touches a browser, a live pane, or the real .agi.

Mechanics (same shape as test_graphweb_page_r160.py):
  * fetch THREE_URL once into a cache dir (SKIP-not-fail when unreachable);
  * load app.js, swap ONLY the THREE_URL constant for the local file URL;
  * run `node` on pan_pick_harness.mjs, which imports the same pinned three,
    records the renderer domElement listeners, dispatches a right-drag pan and
    pointer-hovers over a layer-1 node's phantom and own-plane projections,
    and asserts: panMovesTarget, pickIgnoresPhantomPlane, pickOwnPlane.

A parameterised variant runs the EXACT SAME harness against a PRE-FIX copy of
app.js (the two dead hunks restored) and demands it FAIL the two falsifier
keys and PASS the own-plane key — that separation is what makes it a falsifier.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

import graphweb  # noqa: F401

TESTS = Path(__file__).resolve().parent
GRAPH_WEB = TESTS.parent / "web" / "graph"
APP_JS = GRAPH_WEB / "app.js"
HARNESS = TESTS / "pan_pick_harness.mjs"

THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js"
THREE_CACHE = Path.home() / ".cache" / "agi-graphweb"
THREE_PINNED = THREE_CACHE / "three-0.160.0.module.js"


def _pinned_three_bytes() -> bytes | None:
    if THREE_PINNED.is_file():
        return THREE_PINNED.read_bytes()
    try:
        with urllib.request.urlopen(THREE_URL, timeout=45) as r:  # noqa: S310
            body = r.read()
    except Exception:  # noqa: BLE001  no network -> skip, not fail
        return None
    THREE_CACHE.mkdir(parents=True, exist_ok=True)
    THREE_PINNED.write_bytes(body)
    return body


def _rewritten_app(tmp_path: Path, kind: str) -> Path:
    """app.js with only THREE_URL swapped for the local pinned bytes. `kind`
    == 'prefix' restores the two pre-fix hunks so the SAME harness must fail."""
    src = APP_JS.read_text(encoding="utf-8")
    pinned = _pinned_three_bytes()
    if not pinned:
        pytest.skip("three r160 CDN bytes unreachable; cannot build falsifier")
    three = tmp_path / "three.module.js"
    three.write_bytes(pinned)

    swapped = src.replace(
        'const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";',
        f'const THREE_URL = {three.as_uri()!r};')

    if kind == "prefix":
        # Restore the two L4.259 defects.
        # (1) one-argument cross (zero vector) instead of crossVectors.
        swapped = swapped.replace(
            "const right = new THREE.Vector3().crossVectors(fw, upw).normalize();\n"
            "    const up = new THREE.Vector3().crossVectors(right, fw);",
            "const right = new THREE.Vector3().cross(fw, upw).normalize();\n"
            "    const up = new THREE.Vector3().cross(right, fw);")
        # (2) project every node at BOTH planes.
        swapped = swapped.replace(
            "    for (const n of nodes) {\n"
            "      const v = new THREE.Vector3(n.pos[0], n.pos[1], n.pos[2]).project(camera);",
            "    for (const n of nodes) {\n"
            "      for (const zz of [0, layerz]) {\n"
            "        const v = new THREE.Vector3(n.pos[0], n.pos[1], zz).project(camera);")
        # (the replaced block had one less `}` level after dropping the loop)
        swapped = swapped.replace(
            "      const d = Math.hypot(mouse.ix - sx, mouse.iy - sy);\n"
            "      if (d < bd) { bd = d; best = n; }\n"
            "    }",
            "        const d = Math.hypot(mouse.ix - sx, mouse.iy - sy);\n"
            "        if (d < bd) { bd = d; best = n; }\n"
            "      }\n"
            "    }")

    out = tmp_path / f"app_{kind}.mjs"
    out.write_text(swapped, encoding="utf-8")
    return out


def _run_harness(app_file: Path, three_file: Path) -> dict:
    res = subprocess.run(
        [sys.executable and "node", str(HARNESS), app_file.as_uri(),
         three_file.as_uri()],
        capture_output=True, text=True, timeout=120)
    payload = {}
    for line in (res.stdout or "").splitlines():
        if line.startswith("RESULT "):
            payload = json.loads(line[len("RESULT "):])
    payload.setdefault("rc", res.returncode)
    if not payload:
        payload["raw_stderr"] = res.stderr
    return payload


@pytest.fixture()
def three_bytes(tmp_path):
    pinned = _pinned_three_bytes()
    if not pinned:
        pytest.skip("three r160 CDN bytes unreachable")
    three = tmp_path / "three.module.js"
    three.write_bytes(pinned)
    return three


# --------------------------------------------------------------------------- #
# GREEN: the fixed page pans and picks correctly.                              #
# --------------------------------------------------------------------------- #
def test_pan_moves_target_and_picker_uses_own_plane(three_bytes, tmp_path) -> None:
    app = _rewritten_app(tmp_path, "fixed")
    p = _run_harness(app, three_bytes)
    r = p.get("result", {})
    assert p.get("ok") is True, \
        f"pan/pick falsifier failed: {json.dumps(p, indent=2)}"
    assert r.get("panMovesTarget") is True, f"pan delta: {r.get('panDelta')}"
    assert r.get("pickIgnoresPhantomPlane") is True, \
        f"pixels: {r.get('pickPixels')}"
    assert r.get("pickOwnPlane") is True
    assert r.get("pickPixelsSeparated") is True


# --------------------------------------------------------------------------- #
# RED: the EXACT SAME harness must fail the two falsifier keys on the pre-fix  #
# build but PASS the own-plane key — that separation is the falsifier.         #
# --------------------------------------------------------------------------- #
def test_same_harness_fails_on_prefix_app(three_bytes, tmp_path) -> None:
    app = _rewritten_app(tmp_path, "prefix")
    p = _run_harness(app, three_bytes)
    r = p.get("result", {})
    assert p.get("ok") is False, \
        f"predicted FAIL on pre-fix but passed: {json.dumps(p, indent=2)}"
    # Pre-fix pan is a dead no-op (one-argument cross -> zero vector).
    assert r.get("panMovesTarget") is False, f"pan delta: {r.get('panDelta')}"
    # Pre-fix picker projects at BOTH planes, so the phantom z=0 projection of
    # the layer-1 node matches -> a tooltip appears for a mesh that is not there.
    assert r.get("pickIgnoresPhantomPlane") is False
    # Own-plane pick must still succeed even on the broken build.
    assert r.get("pickOwnPlane") is True
