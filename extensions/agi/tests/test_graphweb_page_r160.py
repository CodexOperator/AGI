"""FALSIFIER for the PRIME merge-up 38: the golden 3D branch must ACTUALLY
render. A node test that executes app.js against the PINNED three r160 CDN
bytes with a DOM stub and asserts the 3D branch COMPLETES and the 5 s poll
FIRES. Nothing here touches a browser, a live pane, or the real .agi.

Mechanics (measured on node v22.22.2 — node cannot import() https: URLs, so
we rewrite):
  * fetch THREE_URL once into a cache dir (SKIP-not-fail when unreachable),
    write the pinned bytes to <tmp>/three.module.js;
  * load app.js text, swap ONLY the THREE_URL constant for the file URL (and
    leave the rest byte-identical);
  * run `node` on the ESM harness `r160_page_harness.mjs`, which installs a
    DOM / window / fetch / rAF / performance stub BEFORE dynamically importing
    app.js, injects a renderer stub through the makeRenderer seam, and asserts
    (a) boot completes with no `3D failed` / `degraded 2D`, (b) render called
    >= 1 and one node mesh per canned node at its own layer's z, (c) a captured
    5000 ms interval fetches /live.json with cache:no-store and re-fetches
    /graph.json when the graph_version changes.

A parameterised variant runs the EXACT SAME harness against a PRE-FIX copy of
app.js (the Float32ColorMaterial build that always degrades to 2D) and demands
it FAIL — that is what makes this a falsifier, not a smoke test.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

import graphweb  # noqa: F401  (import graph already; pytest module needs the path)

TESTS = Path(__file__).resolve().parent
GRAPH_WEB = TESTS.parent / "web" / "graph"
APP_JS = GRAPH_WEB / "app.js"
HARNESS = TESTS / "r160_page_harness.mjs"

# The pinned three r160 ES-module bytes the page claims to use.
THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js"
THREE_CACHE = Path.home() / ".cache" / "agi-graphweb"
THREE_PINNED = THREE_CACHE / "three-0.160.0.module.js"


def _pinned_three_bytes() -> bytes | None:
    """The pinned three r160 bytes, from a cache dir; None when unreachable
    (the test SKIPs rather than fails — a real page is not a test dep)."""
    if THREE_PINNED.is_file():
        return THREE_PINNED.read_bytes()
    try:
        with urllib.request.urlopen(  # noqa: S310  pinned-unpkg, fetch-once
                THREE_URL, timeout=45) as r:
            body = r.read()
    except Exception:  # noqa: BLE001  no network in CI -> skip, not fail
        return None
    THREE_CACHE.mkdir(parents=True, exist_ok=True)
    THREE_PINNED.write_bytes(body)
    return body


FIX_TOKEN = "__THREE_URL_FILE__"


def _rewritten_app(tmp_path: Path, kind: str) -> Path:
    """Write app.js with only the THREE_URL constant swapped for the local
    pinned bytes and no other change. `kind` == 'prefix' restores the two
    known-dead lines (Float32ColorMaterial x3 + top-level `boot();`) so the
    SAME harness must fail. Returns the out file path (a file:// URL)."""
    src = APP_JS.read_text(encoding="utf-8")
    pinned = _pinned_three_bytes()
    if not pinned:
        pytest.skip("three r160 CDN bytes unreachable; cannot build falsifier")
    three = tmp_path / "three.module.js"
    three.write_bytes(pinned)

    three_url = three.as_uri()
    swapped = src.replace(
        'const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";',
        f'const THREE_URL = {three_url!r};')

    if kind == "prefix":
        # Re-introduce the dead 3D branch: Float32ColorMaterial (not in r160)
        # at the root-seat / seat / ghost constructions, plus plain `boot();`
        # so the boot lifecycle is not exposed. This is the pre-fix shape on
        # which the falsifier must fail.
        swapped = swapped.replace(
            "new THREE.MeshBasicMaterial({ color: fill(state.palette.gold) }))",
            "new THREE.Float32ColorMaterial({ baseColor: fill(state.palette.gold) }))")
        swapped = swapped.replace(
            "color: fill(s.active ? \"#f5d962\" : gold) });",
            "baseColor: fill(s.active ? \"#f5d962\" : gold) });")
        swapped = swapped.replace(
            "color: fill(snapped ? \"#f5d962\" : gold),\n        transparent: true,",
            "baseColor: fill(snapped ? \"#f5d962\" : gold),")
        swapped = swapped.replace(
            "globalThis.__agiBoot = boot();", "boot();")

    out = tmp_path / f"app_{kind}.mjs"
    out.write_text(swapped, encoding="utf-8")
    return out


def _run_harness(app_file: Path) -> dict:
    res = subprocess.run(
        [sys.executable and "node", str(HARNESS), app_file.as_uri()],
        capture_output=True, text=True, timeout=120)
    payload = {}
    for line in (res.stdout or "").splitlines():
        if line.startswith("RESULT "):
            payload = json.loads(line[len("RESULT "):])
    payload.setdefault("rc", res.returncode)
    if not payload:
        payload["raw_stderr"] = res.stderr
    return payload


# --------------------------------------------------------------------------- #
# GREEN: the fixed page must complete the 3D branch and fire the 5 s poll.     #
# --------------------------------------------------------------------------- #
def test_r160_3d_branch_completes_and_poll_fires(tmp_path) -> None:
    app = _rewritten_app(tmp_path, "fixed")
    p = _run_harness(app)
    r = p.get("result", {})
    assert p.get("ok") is True, \
        f"3D page falsifier failed: {json.dumps(p, indent=2)}"
    assert r.get("threeBranchCompleted") is True
    assert r.get("renderCalled") is True
    assert r.get("oneMeshPerNode") is True, f"node meshes: {r.get('nodeMeshCount')}"
    assert r.get("bothPlanes") is True
    assert r.get("meshesMatchNodeLayers") is True
    assert r.get("pollExists") is True
    assert r.get("pollLiveCache") == "no-store"
    assert r.get("noRefetchOnFirstTick") is True
    assert r.get("refetchOnVersionChange") is True


# --------------------------------------------------------------------------- #
# RED: the EXACT SAME harness must fail on the pre-fix Float32ColorMaterial    #
# build — that is what makes the round a falsifier, not a smoke test.          #
# --------------------------------------------------------------------------- #
def test_same_harness_fails_on_prefix_app(tmp_path) -> None:
    app = _rewritten_app(tmp_path, "prefix")
    p = _run_harness(app)
    r = p.get("result", {})
    assert p.get("ok") is False, \
        f"predicted to FAIL on pre-fix but passed: {json.dumps(p, indent=2)}"
    assert r.get("threeBranchCompleted") is False, \
        "pre-fix degrades to 2D, so the 3D-branch log marker must be absent"
    assert r.get("renderCalled") is False


# --------------------------------------------------------------------------- #
# The pinned-bytes cache actually IS three r160 (guard against a wildcard that #
# silently reverts to a 2D-only world).                                        #
# --------------------------------------------------------------------------- #
def test_pinned_bytes_are_r160_and_use_real_materials() -> None:
    body = _pinned_three_bytes()
    if not body:
        pytest.skip("pinned three r160 unreachable")
    text = body.decode("utf-8", "replace")
    assert "Float32ColorMaterial" not in text
    for cls in ("MeshBasicMaterial", "PointsMaterial",
                "LineBasicMaterial", "WebGLRenderer", "Color"):
        assert f"class {cls}" in text