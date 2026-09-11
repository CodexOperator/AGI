// agi golden-web page renderer (kid 2) + LIVE OVERLAY (kid A) + GHOST NODES (kid C).
// Render /graph.json as two layers of golden points with dim golden edges on
// the dark served ground, three.js when the CDN is reachable, plain 2D canvas
// otherwise — never a blank screen, never a thrown error.
//
// Live overlay (the claim's original item 3, now really in the bytes):
//   * polls /live.json every 5 s (cache: no-store), replaces state.live.
//   * when live.graph_version differs from the last seen one, re-fetches
//     /graph.json and rebuilds the node/edge geometry IN PLACE (both
//     renderers), so a new node appears without a page reload.
//   * live seat->node AND agent(dispatched_by seat)->node edges draw as
//     THREE.LineSegments — bright gold when the seat is active, dim otherwise
//     (kid A).
//   * an active seat's point PULSES (a sin on its sphere's size in frame()).
// Ghost nodes (owner 2026-09-11 15:5xZ):
//   * every live agent whose node is not yet in the served graph floats as a
//     blank semi-transparent circle near its TARGET node (a seeded 8-15 unit
//     offset + a slow bob), breathing via a sin on scale.
//   * when the agent's /live.json `new_nodes` carries the record, the ghost
//     SNAPS: real id/type/title (tooltip on hover), solid gold, an edge to
//     its first parent.
//   * once /graph.json contains that id the ghost retires and the real node
//     stands at its layout position.
"use strict";

const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";

const state = {
  data: null, live: null,
  graphVersion: null,
  palette: { ground: "#0f1216", gold: "#a48c5a" },
  nodes: {},         // id -> node record (deduped, layer1 dims to 0 for root)
  seatsById: {},     // seat:<name> -> node record
  layer1z: 60,
  t: 0,              // animation clock (seconds-ish, for pulse / bob)
};

const statusEl = document.getElementById("status");
const tooltipEl = document.getElementById("tooltip");
const stage = document.getElementById("stage");

const log = (...a) => { statusEl.textContent = a.join(" "); };

function stabColor(hex, alpha) {
  hex = String(hex || "").replace("#", "");
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  const n = parseInt(hex.slice(0, 6), 16);
  const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  return alpha == null ? `rgb(${r},${g},${b})` : `rgba(${r},${g},${b},${alpha})`;
}

async function getJSON(p) {
  const r = await fetch(p, { cache: "no-store" });
  if (!r.ok) throw new Error(p + " -> " + r.status);
  return r.json();
}

// Apply a fresh /graph.json into state (id records, layer1_z, palette).
function applyGraph(data) {
  state.data = data;
  state.nodes = {};
  state.seatsById = {};
  for (const n of data.nodes) {
    if (n.type === "seat") { state.seatsById[n.id] = n; continue; }
    state.nodes[n.id] = n;
  }
  state.layer1z = data.layer1_z || 60;
  const p = data.palette || {};
  state.palette = { ground: p.ground || "#0f1216", gold: p.gold || "#a48c5a" };
  document.body.style.background = state.palette.ground;
}

async function loadData() {
  applyGraph(await getJSON("/graph.json"));
  try { state.live = await getJSON("/live.json"); }
  catch (e) { state.live = { seats: [], agents: [] }; }
  state.graphVersion = (state.live && state.live.graph_version) || null;
}

// The 5 s poll (kid A): replace state.live; when the graph version changes,
// re-fetch /graph.json and rebuild geometry IN PLACE (no page reload).
function startPoll() {
  const tick = async () => {
    let live;
    try { live = await getJSON("/live.json"); }
    catch (e) { return; }              // keep the last known live frame
    const next = (live && live.graph_version) || state.graphVersion;
    const versionChanged = state.graphVersion != null && next != null
      && next !== state.graphVersion;
    const firstFrame = state.graphVersion == null;
    state.graphVersion = next;
    state.live = live;
    if (versionChanged || firstFrame) {
      try {
        applyGraph(await getJSON("/graph.json"));
        state.graphVersion = next;
        rebootRenderer();
      } catch (e) { /* keep current geometry on a failed re-fetch */ }
    }
  };
  window.setInterval(tick, 5000);
}

function showTooltip(text, x, y) {
  if (!text) { tooltipEl.style.display = "none"; return; }
  tooltipEl.style.display = "block";
  tooltipEl.style.left = (x + 14) + "px";
  tooltipEl.style.top = (y + 14) + "px";
  tooltipEl.textContent = text;
}

/* --------------------------- ghost model -------------------------------- */
function hashStr(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h *= 16777619; }
  return (Math.abs(h) % 1000) / 1000;   // deterministic 0..1
}

// A live agent's ghost: the future node it is building, floating near the
// TARGET node it works toward. Returns null when there is nothing to ghost.
function ghostFor(agent) {
  if (!agent || !agent.target) return null;
  const snaps = (agent.new_nodes || []).filter(r => r && r.id);
  let snap = null;
  for (const r of snaps) { if (r.id.includes(agent.agent)) { snap = r; break; } }
  if (!snap && snaps.length) snap = snaps[0];
  // retired: the real node is now in the served graph.
  if (snap && state.nodes[snap.id]) return null;
  const target = state.nodes[agent.target] || state.seatsById[agent.target];
  if (!target) return null;
  const seed = hashStr(agent.agent || agent.iter || "ghost");
  const ang = seed * Math.PI * 2;
  const rad = 8 + seed * 7;             // seeded 8-15 unit float
  const off = [Math.cos(ang) * rad, Math.sin(ang) * rad];
  return { agent, snap, target, off, phase: seed * Math.PI * 2 };
}

function liveGhosts() {
  if (!state.live || !Array.isArray(state.live.agents)) return [];
  const out = [];
  for (const a of state.live.agents) {
    const g = ghostFor(a);
    if (g) out.push(g);
  }
  return out;
}

// bob offset for a ghost: ~3 s sine walk on the z (out-of-plane) axis.
function ghostBob(g, t) {
  return Math.sin(t * 2.1 + g.phase) * 2.5;
}

/* ------------------------- 2D degraded fallback -------------------------- */
function draw2D() {
  const canvas = document.createElement("canvas");
  canvas.id = "degraded";
  canvas.width = stage.clientWidth || window.innerWidth || 800;
  canvas.height = stage.clientHeight || window.innerHeight || 600;
  stage.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  const cx = canvas.width / 2, cy = canvas.height / 2;
  const scale = 1.4;
  const px = (x, y, z) => [cx + x * scale - z * 0.6, cy + y * scale - z * 0.6];

  canvas.addEventListener("mousemove", (ev) => {
    let best = null, bd = 18;
    for (const n of Object.values(state.nodes)) {
      const [sx, sy] = px(n.pos[0], n.pos[1], n.pos[2]);
      const d = Math.hypot(ev.clientX - sx, ev.clientY - sy);
      if (d < bd) { bd = d; best = n; }
    }
    let tip = best ? `${best.title}  (${best.id})` : "";
    if (!tip) {
      for (const g of liveGhosts()) {
        const [gx, gy] = ghostPt2D(g, state.t, px);
        if (Math.hypot(ev.clientX - gx, ev.clientY - gy) < 14) {
          tip = `${g.agent.tier || ""} ${g.agent.agent} -> ${g.agent.target}`;
          break;
        }
      }
    }
    showTooltip(tip, ev.clientX, ev.clientY);
  });

  function paint() {
    state.t += 0.12;
    ctx.fillStyle = state.palette.ground;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = stabColor(state.palette.gold, 0.16);
    ctx.lineWidth = 0.6;
    for (const e of state.data.edges) {
      const a = state.nodes[e.from] || state.seatsById[e.from];
      const b = state.nodes[e.to] || state.seatsById[e.to];
      if (!a || !b) continue;
      const [x1, y1] = px(a.pos[0], a.pos[1], a.pos[2]);
      const [x2, y2] = px(b.pos[0], b.pos[1], b.pos[2]);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }

    for (const n of Object.values(state.nodes)) {
      const [sx, sy] = px(n.pos[0], n.pos[1], n.pos[2]);
      const isRoot = n.id === state.data.root;
      ctx.fillStyle = isRoot ? stabColor(state.palette.gold, 1)
        : stabColor(state.palette.gold, n.pos[2] > 0 ? 0.92 : 0.7);
      ctx.beginPath();
      ctx.arc(sx, sy, isRoot ? 3.4 : 1.8, 0, Math.PI * 2);
      ctx.fill();
      if (isRoot) { ctx.strokeStyle = state.palette.gold; ctx.lineWidth = 1; ctx.stroke(); }
    }
    drawLive2D(ctx, px);
    drawGhosts2D(ctx, px);
  }

  paint();
  window.setInterval(paint, 120);   // breathe the ghosts / pulse seats in 2D
  log("2D — " + state.data.nodes.length + " nodes, " + state.data.edges.length + " edges");
}

function ghostPt2D(g, t, px) {
  const [tx, ty, tz] = g.target.pos;
  const [nx, ny] = px(tx + g.off[0], ty + g.off[1], tz + ghostBob(g, t));
  return [nx, ny];
}

function liveSeatPairs() {
  const seats = Array.isArray(state.live && state.live.seats)
    ? state.live.seats : [];
  const out = [];
  for (const s of seats) {
    const src = state.seatsById["seat:" + s.seat];
    if (!src) continue;
    for (const wid of (s.working_on || [])) {
      const t = state.nodes[wid];
      if (t) out.push({ src, t, active: !!s.active });
    }
  }
  // agent live edges: dispatched_by seat -> working_on node (kid A).
  const agents = (state.live && Array.isArray(state.live.agents))
    ? state.live.agents : [];
  for (const a of agents) {
    const src = a.dispatched_by ? state.seatsById["seat:" + a.dispatched_by] : null;
    if (!src) continue;
    for (const wid of (a.working_on || [])) {
      const t = state.nodes[wid];
      if (t) out.push({ src, t, active: false });
    }
  }
  return out;
}

function drawLive2D(ctx, px) {
  ctx.lineWidth = 1.4;
  for (const { src, t, active } of liveSeatPairs()) {
    const [x1, y1] = px(src.pos[0], src.pos[1], src.pos[2]);
    const [x2, y2] = px(t.pos[0], t.pos[1], t.pos[2]);
    ctx.strokeStyle = active ? state.palette.gold
      : stabColor(state.palette.gold, 0.35);
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  }
}

function drawGhosts2D(ctx, px) {
  for (const g of liveGhosts()) {
    const [gx, gy] = ghostPt2D(g, state.t, px);
    const breath = 0.5 + 0.18 * Math.sin(state.t * 2.1 + g.phase);
    if (!g.snap) {
      // blank semi-transparent circle — breathing, no text
      ctx.fillStyle = stabColor(state.palette.gold, 0.35 * breath);
      ctx.strokeStyle = stabColor(state.palette.gold, 0.25);
    } else {
      // snapped: solid gold, real label
      ctx.fillStyle = stabColor(state.palette.gold, 1);
      ctx.strokeStyle = state.palette.gold;
      ctx.fillText(`${g.snap.type} ${g.snap.title}`, gx + 6, gy - 6);
    }
    ctx.beginPath();
    ctx.arc(gx, gy, 2.2 + breath, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    if (g.snap && g.snap.parents && g.snap.parents.length) {
      const par = state.nodes[g.snap.parents[0]];
      if (par) {
        const [sx, sy] = px(par.pos[0], par.pos[1], par.pos[2]);
        ctx.strokeStyle = state.palette.gold;
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(sx, sy); ctx.stroke();
      }
    }
  }
}

/* ----------------------- three.js primary renderer ----------------------- */
let THREE = null;
let camera = null;

function fill(hex) {
  // THREE.Color(r, g, b) takes 0-1 FLOATS; the hex int form new THREE.Color(n)
  // is the one correct call for a `#rgb` string (Prime, merge-up 38).
  hex = String(hex || "").replace("#", "");
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  const n = parseInt(hex.slice(0, 6), 16);
  return new THREE.Color(n);
}

function pointsCloud(positions, colors, size) {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(positions), 3));
  g.setAttribute("color", new THREE.BufferAttribute(new Float32Array(colors), 3));
  g.computeBoundingBox();
  const mat = new THREE.PointsMaterial({ size, vertexColors: true });
  return new THREE.Points(g, mat);
}

// LineSegments of (x1,y1,z1, x2,y2,z2) per edge; colors 3 floats per vertex.
function makeLines(segments, colors) {
  if (!segments.length) return null;
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(segments), 3));
  g.setAttribute("color", new THREE.BufferAttribute(new Float32Array(colors), 3));
  g.computeBoundingBox();
  const mat = new THREE.LineBasicMaterial({ vertexColors: true, linewidth: 1.6 });
  return new THREE.LineSegments(g, mat);
}

const BRIGHT = [1.0, 0.9, 0.5];
const DIM = [0.5, 0.45, 0.28];

function render3D() {
  const nodes = Object.values(state.nodes);
  const layerz = state.layer1z;
  const gold = state.palette.gold;

  // ONE mesh per node, at its OWN layer's z — layer-1 nodes only on the
  // sanctuary plane (z=layerz) and layer-0 only on the outer plane (z=0),
  // never a copy on both planes (Prime, merge-up 38). `pos[2]` already
  // carries the layer's z, so placing each node at its own pos is exact.
  const scene = new THREE.Scene();
  scene.background = fill(state.palette.ground);
  scene.nodeMeshes = [];
  const gc = fill(gold);
  for (const n of nodes) {
    // geometry holds an origin point; the OBJECT carries the node's layer z
    // (a Points' .position, not its geometry, is what carries the location).
    const mesh = pointsCloud([0, 0, 0], [gc.r, gc.g, gc.b], 4);
    mesh.position.set(n.pos[0], n.pos[1], n.pos[2]);
    scene.nodeMeshes.push(mesh);
    scene.add(mesh);
  }

  // Edges: sample each as a short run of dim-gold beads between endpoints.
  const epos = []; const ecol = [];
  const per = 7;
  for (const e of state.data.edges) {
    const a = state.nodes[e.from] || state.seatsById[e.from];
    const b = state.nodes[e.to] || state.seatsById[e.to];
    if (!a || !b) continue;
    const za = a.pos[2], zb = b.pos[2];
    for (let i = 1; i < per; i++) {
      const t = i / per;
      epos.push(a.pos[0] + (b.pos[0] - a.pos[0]) * t,
                a.pos[1] + (b.pos[1] - a.pos[1]) * t,
                za + (zb - za) * t);
      ecol.push(0.30, 0.28, 0.22);
    }
  }
  const edgeCloud = pointsCloud(epos, ecol, 2);
  scene.add(edgeCloud);

  const rootNode = state.nodes[state.data.root];
  if (rootNode) {
    // MeshBasicMaterial: the r160 spelling of a plain solid-color surface
    // (Float32ColorMaterial does not exist in three r160).
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(6, 24, 16),
      new THREE.MeshBasicMaterial({ color: fill(state.palette.gold) }));
    sphere.position.set(rootNode.pos[0], rootNode.pos[1], rootNode.pos[2]);
    scene.add(sphere);
  }

  const W = stage.clientWidth || window.innerWidth || 800;
  const H = stage.clientHeight || window.innerHeight || 600;

  // ONE injectable seam for the renderer (Prime's falsifier): the harness
  // grants a stub (via globalThis.__makeRenderer, since a cross-module
  // dynamic import cannot reach `state`); a browser takes the default
  // WebGLRenderer (or an explicit state.makeRenderer if one is ever set).
  // The stub records render/setSize/setPixelRatio and captures the animation
  // loop.
  const buildRenderer = globalThis.__makeRenderer || state.makeRenderer ||
    (() => new THREE.WebGLRenderer({ antialias: true }));
  const renderer = buildRenderer();
  renderer.setSize(W, H);
  if (renderer.setPixelRatio) renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.domElement = renderer.domElement || {};
  stage.appendChild(renderer.domElement);

  const cam = {
    target: new THREE.Vector3(0, 0, layerz / 2),
    az: 0.62, el: 0.55, dist: 1500,
  };
  camera = new THREE.PerspectiveCamera(60, W / H, 1, 50000);
  camera.position.set(cam.dist, cam.dist * 0.6, cam.dist * 0.6);
  camera.lookAt(cam.target);

  const mouse = { ix: 0, iy: 0, over: false, lx: 0, ly: 0 };
  let pick = null;

  // ---- live overlay objects rebuilt here on a cadence ----
  let liveEdges = null;   // THREE.LineSegments (seat + agent work edges)
  let seatMeshes = [];    // {mesh, active} — pulsing active seat spheres
  let ghostMeshes = [];   // {mesh, g, snapped} — ghost circles + snap edges

  function dim(active, mult) {
    const [r, g, b] = active ? BRIGHT : DIM;
    return [r * mult, g * mult, b * mult];
  }

  function buildLive() {
    // --- work edges: seat->node AND agent(dispatched seat)->node ---
    const segs = []; const c = [];
    for (const { src, t, active } of liveSeatPairs()) {
      const [br, bg, bb] = dim(active, 1);
      segs.push(src.pos[0], src.pos[1], src.pos[2],
                t.pos[0], t.pos[1], t.pos[2]);
      c.push(br, bg, bb, br, bg, bb);
    }
    if (liveEdges && liveEdges.parent) scene.remove(liveEdges);
    liveEdges = makeLines(segs, c);
    if (liveEdges) scene.add(liveEdges);

    // --- seat spheres (pulse when active) ---
    for (const m of seatMeshes) if (m.mesh.parent) scene.remove(m.mesh);
    seatMeshes = [];
    const seats = Array.isArray(state.live && state.live.seats)
      ? state.live.seats : [];
    for (const s of seats) {
      const src = state.seatsById["seat:" + s.seat];
      if (!src) continue;
      const mat = new THREE.MeshBasicMaterial({
        color: fill(s.active ? "#f5d962" : gold) });
      const mesh = new THREE.Mesh(new THREE.SphereGeometry(2.6, 16, 12), mat);
      mesh.position.set(src.pos[0], src.pos[1], src.pos[2]);
      mesh.scale.set(1, 1, 1);
      mesh.updateMatrix();
      scene.add(mesh);
      seatMeshes.push({ mesh, active: !!s.active });
    }

    // --- ghost circles ---
    for (const m of ghostMeshes) if (m.mesh.parent) scene.remove(m.mesh);
    ghostMeshes = [];
    for (const g of liveGhosts()) {
      const [tx, ty, tz] = g.target.pos;
      const breath = 0.5 + 0.18 * Math.sin(state.t * 2.1 + g.phase);
      const snapped = !!g.snap;
      const mat = new THREE.MeshBasicMaterial({
        color: fill(snapped ? "#f5d962" : gold),
        transparent: true,
        opacity: snapped ? 1 : 0.45 });
      const mesh = new THREE.Mesh(new THREE.SphereGeometry(2.4, 16, 12), mat);
      mesh.position.set(tx + g.off[0], ty + g.off[1], tz + ghostBob(g, state.t));
      mesh.scale.set(snapped ? 1 : 1, 1, 1);
      mesh.updateMatrix();
      scene.add(mesh);
      ghostMeshes.push({ mesh, g, snapped });
    }

    // --- snapped ghosts also draw an edge to their first parent ---
    const gsegs = []; const gc = [];
    for (const gm of ghostMeshes) {
      if (!gm.snapped || !gm.g.snap.parents || !gm.g.snap.parents.length) continue;
      const par = state.nodes[gm.g.snap.parents[0]];
      if (!par) continue;
      const [tx, ty, tz] = gm.g.target.pos;
      gsegs.push(tx + gm.g.off[0], ty + gm.g.off[1],
                 tz + ghostBob(gm.g, state.t),
                 par.pos[0], par.pos[1], par.pos[2]);
      gc.push(1.0, 0.85, 0.5, 1.0, 0.85, 0.5);
    }
    const gEdge = makeLines(gsegs, gc);
    if (gEdge) scene.add(gEdge);
    return gEdge;   // caller removes it next rebuild
  }

  function refreshLive() {
    const extra = buildLive();
    if (existingGhostEdge && existingGhostEdge.parent) scene.remove(existingGhostEdge);
    existingGhostEdge = extra;
  }
  let existingGhostEdge = null;

  function setCam() {
    const s = Math.sin(cam.el), c = Math.cos(cam.el);
    camera.position.set(cam.target.x + cam.dist * s * Math.sin(cam.az),
                        cam.target.y + cam.dist * c,
                        cam.target.z + cam.dist * s * Math.cos(cam.az));
    camera.lookAt(cam.target);
    camera.updateMatrixWorld();
  }
  function resetCam() {
    cam.target.set(0, 0, layerz / 2); cam.az = 0.62; cam.el = 0.55; cam.dist = 1500;
    setCam();
  }

  renderer.domElement.addEventListener("pointermove", (ev) => {
    mouse.ix = ev.clientX; mouse.iy = ev.clientY; mouse.over = true;
    if (ev.buttons === 0) return;
    const dx = ev.clientX - mouse.lx, dy = ev.clientY - mouse.ly;
    mouse.lx = ev.clientX; mouse.ly = ev.clientY;
    if (ev.buttons === 1) {
      cam.az += dx * 0.012;
      cam.el = Math.max(0.05, Math.min(1.45, cam.el + dy * 0.010));
    } else if (ev.buttons === 2 || ev.buttons === 4) {
      pan(dx, dy);
    }
  });
  renderer.domElement.addEventListener("pointerdown", (ev) => {
    mouse.lx = ev.clientX; mouse.ly = ev.clientY;
  });
  renderer.domElement.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    cam.dist = Math.max(200, Math.min(9000, cam.dist * (ev.deltaY > 0 ? 0.88 : 1.13)));
  }, { passive: false });
  document.addEventListener("keydown", (ev) => {
    if (String(ev.key || "").toUpperCase() === "R") resetCam();
  });

  function pan(dx, dy) {
    const fw = new THREE.Vector3(
      cam.target.x - camera.position.x, cam.target.y - camera.position.y,
      cam.target.z - camera.position.z).normalize();
    const upw = new THREE.Vector3(0, 0, 1);
    // crossVectors(a, b) is the two-argument form. In three r160
    // Vector3.cross(v) takes ONE argument (the two-argument cross(a, b) was
    // removed), so `new Vector3().cross(fw, upw)` was (0,0,0) x fw = the zero
    // vector and right-drag pan was a live no-op (sanctuary-helper L4.259).
    const right = new THREE.Vector3().crossVectors(fw, upw).normalize();
    const up = new THREE.Vector3().crossVectors(right, fw);
    const s = cam.dist / 800;
    cam.target.x += -right.x * dx * s + up.x * dy * s;
    cam.target.y += -right.y * dx * s + up.y * dy * s;
    cam.target.z += -right.z * dx * s + up.z * dy * s;
  }

  function updatePick() {
    if (!mouse.over) { if (pick) { pick = null; showTooltip("", 0, 0); } return; }
    let best = null, bd = 20;
    // ONE projection per node, at its OWN layer's z — render3D places one
    // mesh per node at pos[2], so a pick over a phantom z=0 projection of a
    // layer-1 node (or vice versa) must hit nothing (sanctuary-helper L4.259).
    for (const n of nodes) {
      const v = new THREE.Vector3(n.pos[0], n.pos[1], n.pos[2]).project(camera);
      const sx = (v.x + 1) / 2 * W, sy = (1 - v.y) / 2 * H;
      const d = Math.hypot(mouse.ix - sx, mouse.iy - sy);
      if (d < bd) { bd = d; best = n; }
    }
    let tip = best ? `${best.title}  (${best.id})` : "";
    if (!tip) {
      for (const gm of ghostMeshes) {
        const v = new THREE.Vector3(gm.mesh.position.x, gm.mesh.position.y,
                                    gm.mesh.position.z).project(camera);
        const sx = (v.x + 1) / 2 * W, sy = (1 - v.y) / 2 * H;
        if (Math.hypot(mouse.ix - sx, mouse.iy - sy) < 18) {
          tip = `${gm.g.agent.tier || ""} ${gm.g.agent.agent} -> ${gm.g.agent.target}`;
          break;
        }
      }
    }
    if (tip !== pick) { pick = tip; showTooltip(tip, mouse.ix, mouse.iy); }
  }

  let liveCooldown = 0;
  function frame() {
    setCam();
    state.t += 1 / 60;

    // pulse active seats / breathe ghosts (a sin on size each frame).
    for (const { mesh, active } of seatMeshes) {
      const s = active ? 1 + 0.2 * Math.sin(state.t * 3 + mesh.position.x)
                       : 1;
      mesh.scale.set(s, s, s);
      mesh.updateMatrix();
    }
    for (const gm of ghostMeshes) {
      if (gm.snapped) { gm.mesh.scale.set(1, 1, 1); gm.mesh.updateMatrix(); continue; }
      const s = 1 + 0.22 * Math.sin(state.t * 2.1 + gm.g.phase);
      gm.mesh.scale.set(s, s, s);
      // bob toward target
      const [tx, ty, tz] = gm.g.target.pos;
      gm.mesh.position.set(tx + gm.g.off[0], ty + gm.g.off[1],
                           tz + ghostBob(gm.g, state.t));
      gm.mesh.updateMatrix();
    }

    if (++liveCooldown > 120) {       // ~2 s cadence of live-edge refresh
      liveCooldown = 0;
      refreshLive();
    }
    updatePick();
    renderer.render(scene, camera);
  }

  refreshLive();
  renderer.setAnimationLoop(frame);
  log("3D — " + nodes.length + " nodes, " + state.data.edges.length + " edges");
}

/* --------------------------- entry point --------------------------------- */
// Rebuild the live geometry for the current renderer after a graph_version
// change — tear down the stage and re-run whichever renderer is active.
function rebootRenderer() {
  const had3D = THREE != null;
  while (stage.firstChild) stage.removeChild(stage.firstChild);
  if (had3D) {
    try { render3D(); return; }
    catch (e) { log("3D rebuild failed (" + e.message + ") — degraded 2D"); }
    draw2D();
  } else {
    draw2D();
  }
}

async function boot() {
  try { await loadData(); }
  catch (e) { log("could not load /graph.json — " + e.message); return; }
  try { THREE = await import(THREE_URL); }
  catch (e) { THREE = null; log("three.js CDN unreachable"); }
  if (THREE != null) {
    try { render3D(); }
    catch (e) { log("3D failed (" + e.message + ") — degraded 2D"); draw2D(); }
  } else {
    draw2D();
  }
  startPoll();
}

// Page-falsifier seam: expose the boot lifecycle for the node harness that
// runs this file against the pinned CDN bytes with a DOM stub. Harmless in a
// browser, where nothing reads it.
globalThis.__agiBoot = boot();