// Node ESM harness for the L4.259 fix-only round (sanctuary-helper 3baf36):
// proves right-drag PAN moves the camera and the node PICKER ignores phantom
// planes, against the PINNED three r160 bytes with a DOM stub.
//
// Two defects fixed in app.js, verified here:
//   (1) pan() used `new THREE.Vector3().cross(fw, upw)` — the ONE-argument
//       cross, removed in r160 (which exported only crossVectors). It returned
//       the zero vector, so every right-drag/middle-drag added 0 to cam.target:
//       RIGHT-DRAG PAN WAS A LIVE NO-OP.
//   (2) updatePick() projected EVERY node at BOTH planes `for (zz of [0,
//       layerz])` while render3D places ONE mesh per node at its OWN layer's
//       z — hovering a node's phantom z=0 projection showed a tooltip for a
//       mesh that is not there.
//
// The renderer stub here RECORDS its domElement listeners (the r160 harness's
// stub swallows them) and lets us dispatch, then captures the camera the real
// render() was handed so we can project with the SAME camera updatePick uses.
//
// argv: [2] app.js url  [3] three.module.js url (pinned r160, local file).
// Exit 0 + RESULT {ok:true} on success, else exit 1 + ok:false. The SAME
// harness run on the PRE-FIX app.js must FAIL (ok:false) — the falsifier.
"use strict";

const appUrl = process.argv[2];
const threeUrl = process.argv[3];
if (!appUrl || !threeUrl) {
  console.error("usage: node pan_pick_harness.mjs <app.js url> <three url>");
  process.exit(2);
}

const __log = [];
globalThis.__log = __log;

// ------------------------------------------------------------------ canned data
const LAYER1_Z = 200;
// A layer-1 node FAR off axis so its z=0 phantom projection and its own
// (z=LAYER1_Z) projection land at clearly separated screen pixels (parallax).
const LAYER1_NODE = { id: "experiment:e1", type: "experiment",
                      title: "EdgeCase", layer: 1, pos: [700, 350, LAYER1_Z] };
const LAYER0_NODE = { id: "hypothesis:h1", type: "hypothesis",
                      title: "Golden", layer: 0, pos: [-400, -250, 0] };
const CANNED_NODES = [
  { id: "goal:g17", type: "goal", title: "Seat system", layer: 1,
    pos: [0, 0, LAYER1_Z] },
  LAYER1_NODE,
  LAYER0_NODE,
];
const CANNED_EDGES = [{ from: "goal:g17", to: "experiment:e1", kind: "parents" }];
const CANNED_GRAPH = {
  nodes: CANNED_NODES,
  edges: CANNED_EDGES,
  root: "goal:g17",
  layer1_z: LAYER1_Z,
  palette: { ground: "#0f1216", gold: "#a48c5a" },
};
const cannedLive = () => ({ graph_version: "gv-pp1",
                            seats: [], agents: [] });

// ------------------------------------------------------------------ fetch stub
const fetchCalls = [];
const jsResponse = (obj, status = 200) =>
  ({ ok: status < 300, status, json: async () => obj });
globalThis.fetch = async (url, opts = {}) => {
  const u = String(url);
  fetchCalls.push({ url: u, cache: opts && opts.cache });
  if (u === "/graph.json") return jsResponse(CANNED_GRAPH);
  if (u === "/live.json") return jsResponse(cannedLive());
  return jsResponse({}, 404);
};

// ------------------------------------------------------------------ DOM stub
function nullSafeCtx() {
  return { fillStyle: "", strokeStyle: "", lineWidth: 1,
           beginPath() {}, moveTo() {}, lineTo() {}, arc() {}, fill() {},
           stroke() {}, fillText() {}, fillRect() {}, clearRect() {} };
}
function makeEl(tag) {
  const el = { tagName: (tag || "div").toUpperCase(), style: {},
               clientWidth: 1280, clientHeight: 800,
               getContext: (t) => (t === "2d" ? nullSafeCtx() : null),
               appendChild() {}, removeChild() {}, setAttribute() {},
               setAttributeNS() {}, _text: "",
               _listeners: {} };
  el.addEventListener = (type, fn) => { el._listeners[type] = fn; };
  Object.defineProperty(el, "textContent", {
    get() { return this._text; },
    set(v) { this._text = String(v); globalThis.__log.push(String(v)); },
  });
  return el;
}
const els = {};
globalThis.document = {
  getElementById: (id) => (els[id] = els[id] || makeEl(id)),
  createElement: (tag) => (els[tag] = els[tag] || makeEl(tag)),
  addEventListener() {},
  body: { style: {} },
};

// ------------------------------------------------------------------ window stub
const intervals = [];
globalThis.window = {
  innerWidth: 1280, innerHeight: 800, devicePixelRatio: 1,
  addEventListener() {},
  setInterval(fn, ms) { intervals.push({ fn, ms }); return intervals.length; },
};
globalThis.requestAnimationFrame = () => 0;
globalThis.performance = { now: () => 0 };

// ------------------------------------------------------------------ renderer stub
// domElement RECORDS its listeners (unlike the r160 stub, which swallows
// them) so we can dispatch pointerdown / pointermove; render() captures the
// camera it is handed so we can project with the same one updatePick uses.
const stub = {
  domElement: { style: {}, _listeners: {} },
  _renderCalls: 0, _scene: null, _loop: null, _cam: null, _w: 1280, _h: 800,
  setAnimationLoop(cb) { this._loop = cb; },
  render(scene, camera) { this._scene = scene; this._cam = camera; this._renderCalls += 1; },
  setSize(w, h) { this._w = w; this._h = h; },
  setPixelRatio(d) { this._pixelRatio = d; },
};
stub.domElement.addEventListener = (type, fn) => { stub.domElement._listeners[type] = fn; };
globalThis.__rendererStub = stub;
globalThis.__makeRenderer = () => stub;

const dispatch = (type, ev) => {
  const fn = stub.domElement._listeners[type];
  if (!fn) throw new Error("no " + type + " listener registered on domElement");
  fn(ev);
};

// ------------------------------------------------------------------ boot + run
(async () => {
  const THREE = await import(threeUrl);
  await new Promise((r) => setTimeout(r, 80));
  const bootP = (globalThis.__agiBoot) || Promise.resolve();
  try { await import(appUrl); }
  catch (e) {
    console.log("RESULT " + JSON.stringify({ ok: false, bootError: String(e),
      log: __log.slice() }));
    process.exit(1);
  }
  await bootP;
  await new Promise((r) => setTimeout(r, 80));

  let result = {};
  try {
    const renderer = globalThis.__rendererStub;
    const W = renderer._w, H = renderer._h;
    const tick = () => { if (typeof renderer._loop === "function") renderer._loop(); };

    // One frame so the render stub captures the camera (set from the default
    // orbit) before we touch it.
    tick();
    const cam = renderer._cam;
    if (!cam) throw new Error("render stub never captured a camera");

    // Give the camera a REAL projection matrix (the stub renderer never calls
    // updateProjectionMatrix, so the default is identity and z would be
    // ignored). updatePick reads the same matrices, so both agree.
    cam.updateProjectionMatrix();
    cam.updateMatrixWorld(true);

    // ------------------------------------------------------------- (a) PAN
    const c0 = { ...cam.position };
    dispatch("pointerdown", { clientX: 100, clientY: 100, buttons: 1 });
    // right-drag (buttons:2) by (40, 25)
    dispatch("pointermove", { clientX: 140, clientY: 125, buttons: 2 });
    tick();
    const c1 = { ...cam.position };
    const dx = c1.x - c0.x, dy = c1.y - c0.y, dz = c1.z - c0.z;
    const finiteMove = [dx, dy, dz].every((v) => Number.isFinite(v));
    const moved = Math.hypot(dx, dy, dz);
    result.panMovesTarget = finiteMove && moved > 1e-6;
    result.panDelta = { dx, dy, dz, moved };

    // A projection helper on the REAL camera (identical to updatePick's math).
    const toPixel = (x, y, z) => {
      const v = new THREE.Vector3(x, y, z).project(cam);
      return { x: (v.x + 1) / 2 * W, y: (1 - v.y) / 2 * H };
    };

    // ------------------------------------------------------ (b) PICK phantom
    const L1 = LAYER1_NODE;
    // The phantom z=0 projection of the layer-1 node — a mesh is NOT there.
    const ph = toPixel(L1.pos[0], L1.pos[1], 0);
    dispatch("pointermove", { clientX: ph.x, clientY: ph.y, buttons: 0 });
    tick();
    const phantomTip = (els["tooltip"] || {}).textContent || "";
    const phantomShown = els["tooltip"] && els["tooltip"].style.display === "block";
    result.pickIgnoresPhantomPlane = !phantomShown
      && !phantomTip.includes(L1.title);

    // --------------------------------------------------- (c) PICK own plane
    const own = toPixel(L1.pos[0], L1.pos[1], L1.pos[2]);
    dispatch("pointermove", { clientX: own.x, clientY: own.y, buttons: 0 });
    tick();
    const ownTip = (els["tooltip"] || {}).textContent || "";
    const ownShown = els["tooltip"] && els["tooltip"].style.display === "block";
    result.pickOwnPlane = ownShown && ownTip.includes(L1.title)
      && ownTip.includes(L1.id);

    // The two pick pixels must actually separate (> 40 px) or the phantom vs
    // own-plane distinction is meaningless.
    const sep = Math.hypot(own.x - ph.x, own.y - ph.y);
    result.pickPixelsSeparated = sep > 40;
    result.pickPixels = { phantom: ph, own, sep };

    result.ok = result.panMovesTarget && result.pickIgnoresPhantomPlane
      && result.pickOwnPlane && result.pickPixelsSeparated;
  } catch (e) {
    result.ok = false;
    result.harnessError = String(e);
  }

  console.log("RESULT " + JSON.stringify({ ok: result.ok, result, log: __log.slice() }));
  process.exit(result.ok ? 0 : 1);
})();
