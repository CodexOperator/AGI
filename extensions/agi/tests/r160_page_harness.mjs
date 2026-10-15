// Node ESM harness for the page FALSIFIER (Prime, merge-up 38): executes
// app.js — the two-layer golden 3D web — against the PINNED three r160 bytes
// with a DOM stub, and asserts the 3D branch COMPLETES and the 5 s poll FIRES.
//
// Node cannot `import()` an https: URL, so `test_graphweb_page_r160.py` swaps
// ONLY the app.js `THREE_URL` constant for a local `file:` URL to the fetched
// pinned bytes and hands us the path as argv[2]. This file installs the DOM /
// window / fetch globals BEFORE dynamically importing app.js, injects a
// renderer stub through the `state.makeRenderer` seam, and asserts:
//   (a) boot() completes with NO `3D failed` / `degraded 2D` line in the log;
//   (b) the stub renderer's render was called >= 1 and the scene holds one
//       node mesh per canned node, at its own layer's z;
//   (c) a captured 5000 ms interval exists; one tick fetches /live.json with
//       cache:no-store and does NOT re-fetch /graph.json; a second tick after
//       the canned graph_version changes re-fetches /graph.json.
//
// Exit 0 + `RESULT {"ok":true,...}` on success; exit 1 + ok:false otherwise.
// The same harness run against the PRE-FIX app.js must fail (ok:false) — that
// is what makes this a falsifier and not a smoke test.
"use strict";

const appUrl = process.argv[2];
if (!appUrl) { console.error("usage: node r160_page_harness.mjs <app.js url>"); process.exit(2); }

// ------------------------------------------------------------------ log buffer
const __log = [];
globalThis.__log = __log;

// ------------------------------------------------------------------ canned data
const LAYER1_Z = 60;
const CANNED_NODES = [
  { id: "goal:g17", type: "goal", title: "Seat system", layer: 1, pos: [0, 0, LAYER1_Z] },
  { id: "goal:g9", type: "goal", title: "Legibility", layer: 0, pos: [100, 0, 0] },
  { id: "experiment:e1", type: "experiment", title: "Edge", layer: 1, pos: [10, 20, LAYER1_Z] },
  { id: "hypothesis:h1", type: "hypothesis", title: "Golden", layer: 0, pos: [-50, 80, 0] },
];
const CANNED_EDGES = [{ from: "goal:g17", to: "goal:g9", kind: "parents" }];
const CANNED_GRAPH = {
  nodes: CANNED_NODES,
  edges: CANNED_EDGES,
  root: "goal:g17",
  layer1_z: LAYER1_Z,
  palette: { ground: "#0f1216", gold: "#a48c5a" },
};

// /live.json is mutable: the poll test bumps graph_version between ticks.
let liveVersion = "gv-0001";
const cannedLive = () => ({
  graph_version: liveVersion,
  seats: [{ seat: "helmsman", active: true, generation: 280, window: "win_a",
            working_on: ["experiment:e1"] }],
  agents: [{ agent: "a00-x", tier: "kid", iter: "L4.252",
             dispatched_by: "helmsman", target: "experiment:e1",
             working_on: ["experiment:e1"],
             new_nodes: [{ id: "experiment:ghost1", type: "experiment",
                           title: "Ghost", parents: ["goal:g17"] }] }],
});

// ------------------------------------------------------------------ fetch stub
const fetchCalls = [];
function jsResponse(obj, status = 200) {
  return { ok: status < 300, status, json: async () => obj };
}
globalThis.fetch = async (url, opts = {}) => {
  const u = String(url);
  fetchCalls.push({ url: u, cache: opts && opts.cache });
  if (u === "/graph.json") return jsResponse(CANNED_GRAPH);
  if (u === "/live.json") return jsResponse(cannedLive());
  return jsResponse({}, 404);
};
const fetchCount = (u) => fetchCalls.filter((c) => c.url === u).length;
const lastCacheFor = (u) => {
  const hit = [...fetchCalls].reverse().find((c) => c.url === u);
  return hit ? hit.cache : undefined;
};

// ------------------------------------------------------------------ DOM stub
function nullSafeCtx() {
  return { fillStyle: "", strokeStyle: "", lineWidth: 1,
           beginPath() {}, moveTo() {}, lineTo() {}, arc() {}, fill() {},
           stroke() {}, fillText() {}, fillRect() {}, clearRect() {} };
}
function makeEl(tag) {
  const el = { tagName: (tag || "div").toUpperCase(), style: {}, clientWidth: 1280,
               clientHeight: 800,
               getContext: (t) => (t === "2d" ? nullSafeCtx() : null),
               appendChild() {}, removeChild() {}, addEventListener() {},
               setAttribute() {}, setAttributeNS() {}, _text: "" };
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
// Injected through the app.js `state.makeRenderer` seam (via the global form
// the seam also honours, since a dynamic import cannot reach `state`).
const stub = {
  domElement: { style: {}, addEventListener() {} },
  _renderCalls: 0, _scene: null, _loop: null,
  setAnimationLoop(cb) { this._loop = cb; },
  render(scene) { this._scene = scene; this._renderCalls += 1; },
  setSize(w, h) { this._w = w; this._h = h; },
  setPixelRatio(d) { this._pixelRatio = d; },
};
globalThis.__rendererStub = stub;
globalThis.__makeRenderer = () => stub;

// ------------------------------------------------------------------ boot + run
(async () => {
  // Give boot() its own chance to finish its async chain even when app.js
  // does not expose __agiBoot (the pre-fix file, which logs "3D failed").
  await new Promise((r) => setTimeout(r, 80));
  const bootP = (globalThis.__agiBoot) || Promise.resolve();
  try {
    await import(appUrl);
  } catch (e) {
    console.log("RESULT " + JSON.stringify({ ok: false, bootError: String(e),
      log: __log.slice(), fetchCalls } ));
    process.exit(1);
  }
  await bootP;
  await new Promise((r) => setTimeout(r, 80));   // flush remaining ticks

  // The injected renderer stub (via the makeRenderer seam inside app.js).
  const renderer = globalThis.__rendererStub;
  const result = {};

  // Drive one animation frame so the stub's render is actually called
  // against the real scene (setAnimationLoop is captured, not auto-run).
  if (renderer && typeof renderer._loop === "function") {
    try { renderer._loop(); } catch (e) { /* render never surfaced */ }
  }

  // (a) 3D branch completed: boot resolved, and no degraded marker.
  const logLine = __log.join("\n");
  result.threeBranchCompleted =
    !/3D failed|degraded 2D|three\.js CDN unreachable/.test(logLine);

  // (b) render called >= 1 and one node mesh per canned node at its own z.
  result.renderCalled = !!(renderer && renderer._renderCalls >= 1);
  const scene = renderer ? renderer._scene : null;
  const meshes = (scene && scene.nodeMeshes) ? scene.nodeMeshes : [];
  result.nodeMeshCount = meshes.length;
  result.oneMeshPerNode = meshes.length === CANNED_NODES.length;
  result.bothPlanes = meshes.some((m) => Math.abs(m.position.z - 0) < 1e-6) &&
                      meshes.some((m) => Math.abs(m.position.z - LAYER1_Z) < 1e-6);
  result.meshesMatchNodeLayers = CANNED_NODES.every((n) =>
    meshes.some((m) => Math.abs(m.position.z - n.pos[2]) < 1e-6));

  // (c) the 5 s poll: a 5000 ms interval exists, one tick fetches /live.json
  // with cache:no-store and does NOT re-fetch /graph.json; a second tick
  // after the graph_version changes re-fetches /graph.json.
  const poll = intervals.find((i) => i.ms === 5000);
  result.pollExists = !!poll;
  result.pollLiveCache = "";
  result.noRefetchOnFirstTick = true;
  result.refetchOnVersionChange = false;
  if (poll) {
    await poll.fn();                                   // first tick
    result.pollLiveCache = lastCacheFor("/live.json");
    result.noRefetchOnFirstTick = fetchCount("/graph.json") === 1;
    liveVersion = "gv-9999";                           // graph_version changed
    await poll.fn();                                   // second tick
    result.refetchOnVersionChange = fetchCount("/graph.json") === 2;
  }

  result.ok = result.threeBranchCompleted && result.renderCalled &&
    result.oneMeshPerNode && result.bothPlanes && result.meshesMatchNodeLayers &&
    result.pollExists && result.pollLiveCache === "no-store" &&
    result.noRefetchOnFirstTick && result.refetchOnVersionChange;

  console.log("RESULT " + JSON.stringify({ ok: result.ok, result, log: __log.slice() }));
  process.exit(result.ok ? 0 : 1);
})();