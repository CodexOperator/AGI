// agi golden-web page renderer (kid 2).
// Render /graph.json as two layers of golden points with dim golden edges on
// the dark served ground, three.js when the CDN is reachable, plain 2D canvas
// otherwise — never a blank screen, never a thrown error.
"use strict";

const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";

const state = {
  data: null, live: null,
  palette: { ground: "#0f1216", gold: "#a48c5a" },
  nodes: {},         // id -> node record (deduped, layer1 dims to 0 for root)
  seatsById: {},     // seat:<name> -> node record
  layer1z: 60,
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

async function loadData() {
  state.data = await getJSON("/graph.json");
  for (const n of state.data.nodes) {
    if (n.type === "seat") { state.seatsById[n.id] = n; continue; }
    state.nodes[n.id] = n;
  }
  state.layer1z = state.data.layer1_z || 60;
  const p = state.data.palette || {};
  state.palette = { ground: p.ground || "#0f1216", gold: p.gold || "#a48c5a" };
  document.body.style.background = state.palette.ground;
  try { state.live = await getJSON("/live.json"); }
  catch (e) { state.live = { seats: [], agents: [] }; }
}

function showTooltip(text, x, y) {
  if (!text) { tooltipEl.style.display = "none"; return; }
  tooltipEl.style.display = "block";
  tooltipEl.style.left = (x + 14) + "px";
  tooltipEl.style.top = (y + 14) + "px";
  tooltipEl.textContent = text;
}

/* ------------------------- 2D degraded fallback -------------------------- */
function draw2D() {
  const canvas = document.createElement("canvas");
  canvas.id = "degraded";
  canvas.width = stage.clientWidth || window.innerWidth || 800;
  canvas.height = stage.clientHeight || window.innerHeight || 600;
  stage.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = state.palette.ground;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2, cy = canvas.height / 2;
  const scale = 1.4;
  const px = (x, y, z) => [cx + x * scale - z * 0.6, cy + y * scale - z * 0.6];

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

  canvas.addEventListener("mousemove", (ev) => {
    let best = null, bd = 14;
    for (const n of Object.values(state.nodes)) {
      const [sx, sy] = px(n.pos[0], n.pos[1], n.pos[2]);
      const d = Math.hypot(ev.clientX - sx, ev.clientY - sy);
      if (d < bd) { bd = d; best = n; }
    }
    showTooltip(best ? `${best.title}  (${best.id})` : "", ev.clientX, ev.clientY);
  });

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
  log("2D — " + state.data.nodes.length + " nodes, " + state.data.edges.length + " edges");
}

function drawLive2D(ctx, px) {
  ctx.lineWidth = 1.4;
  const seats = (state.live && state.live.seats) ? state.live.seats : [];
  for (const s of seats) {
    const src = state.seatsById["seat:" + s.seat];
    if (!src) continue;
    for (const wid of (s.working_on || [])) {
      const t = state.nodes[wid];
      if (!t) continue;
      const [x1, y1] = px(src.pos[0], src.pos[1], src.pos[2]);
      const [x2, y2] = px(t.pos[0], t.pos[1], t.pos[2]);
      ctx.strokeStyle = s.active ? state.palette.gold : stabColor(state.palette.gold, 0.35);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
  }
}

/* ----------------------- three.js primary renderer ----------------------- */
let THREE = null;
let camera = null;

function fill(hex) {
  hex = String(hex || "").replace("#", "");
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  const n = parseInt(hex.slice(0, 6), 16);
  return new THREE.Color((n >> 16) & 255, (n >> 8) & 255, n & 255);
}

function pointsCloud(positions, colors, size) {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(positions), 3));
  g.setAttribute("color", new THREE.BufferAttribute(new Float32Array(colors), 3));
  g.computeBoundingBox();
  const mat = new THREE.PointsMaterial({ size, vertexColors: true });
  return new THREE.Points(g, mat);
}

function render3D() {
  const nodes = Object.values(state.nodes);
  const layerz = state.layer1z;

  // Node cloud: every node rendered twice — its layer0 copy at z=0 and its
  // layer1 copy at z=layerz. Root's layer1 copy is brightened; layer1 reads
  // as the hovering golden plane above the dim ground.
  const positions = []; const colors = [];
  for (const n of nodes) {
    const gc = fill(state.palette.gold);
    const root = n.id === state.data.root;
    positions.push(n.pos[0], n.pos[1], 0);
    colors.push(gc.r, gc.g, gc.b);
    positions.push(n.pos[0], n.pos[1], layerz);
    const b = Math.min(255, gc.b * (root ? 1.25 : 1.0));
    colors.push(Math.min(255, gc.r * (root ? 1.15 : 1.0)),
                Math.min(255, gc.g * (root ? 1.15 : 1.0)), b);
  }
  const nodeCloud = pointsCloud(positions, colors, 4);

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

  const scene = new THREE.Scene();
  scene.background = fill(state.palette.ground);
  scene.add(nodeCloud);
  scene.add(edgeCloud);

  const rootNode = state.nodes[state.data.root];
  if (rootNode) {
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(6, 24, 16),
      new THREE.Float32ColorMaterial({ baseColor: fill(state.palette.gold) }));
    sphere.position.set(rootNode.pos[0], rootNode.pos[1], layerz);
    scene.add(sphere);
  }

  const W = stage.clientWidth || window.innerWidth || 800;
  const H = stage.clientHeight || window.innerHeight || 600;

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(W, H);
  stage.appendChild(renderer.domElement);

  // camera + manual orbit (drag=orbit, wheel=zoom, right-drag=pan, R=reset)
  const cam = {
    target: new THREE.Vector3(0, 0, layerz / 2),
    az: 0.62, el: 0.55, dist: 1500,
  };
  camera = new THREE.PerspectiveCamera(60, W / H, 1, 50000);
  camera.position.set(cam.dist, cam.dist * 0.6, cam.dist * 0.6);
  camera.lookAt(cam.target);

  const mouse = { ix: 0, iy: 0, over: false, lx: 0, ly: 0 };
  let pick = null;
  let liveEdges = buildLiveCloud();
  let liveCooldown = 0;

  function buildLiveCloud() {
    if (!state.live) return null;
    const seats = Array.isArray(state.live.seats) ? state.live.seats : [];
    const pos = []; const col = [];
    for (const s of seats) {
      const src = state.seatsById["seat:" + s.seat];
      if (!src) continue;
      const bright = s.active ? [1.0, 0.9, 0.5] : [0.5, 0.45, 0.28];
      for (const wid of (s.working_on || [])) {
        const t = state.nodes[wid];
        if (!t) continue;
        pos.push(src.pos[0], src.pos[1], src.pos[2],
                 t.pos[0], t.pos[1], t.pos[2]);
        col.push(bright[0], bright[1], bright[2],
                 bright[0], bright[1], bright[2]);
      }
    }
    if (!pos.length) return null;
    try { return pointsCloud(pos, col, 3); }
    catch (e) { return null; }
  }

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
    if (ev.buttons === 1) {                 // left: orbit
      cam.az += dx * 0.012;
      cam.el = Math.max(0.05, Math.min(1.45, cam.el + dy * 0.010));
    } else if (ev.buttons === 2 || ev.buttons === 4) { // right|middle: pan
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
    const right = new THREE.Vector3().cross(fw, upw).normalize();
    const up = new THREE.Vector3().cross(right, fw);
    const s = cam.dist / 800;
    cam.target.x += -right.x * dx * s + up.x * dy * s;
    cam.target.y += -right.y * dx * s + up.y * dy * s;
    cam.target.z += -right.z * dx * s + up.z * dy * s;
  }

  function updatePick() {
    if (!mouse.over) { if (pick) { pick = null; showTooltip("", 0, 0); } return; }
    let best = null, bd = 20;
    for (const n of nodes) {
      for (const zz of [0, layerz]) {
        const v = new THREE.Vector3(n.pos[0], n.pos[1], zz).project(camera);
        const sx = (v.x + 1) / 2 * W, sy = (1 - v.y) / 2 * H;
        const d = Math.hypot(mouse.ix - sx, mouse.iy - sy);
        if (d < bd) { bd = d; best = n; }
      }
    }
    if (best !== pick) {
      pick = best;
      showTooltip(best ? `${best.title}  (${best.id})` : "", mouse.ix, mouse.iy);
    }
  }

  function frame() {
    setCam();
    if (liveEdges && !liveEdges.parent) scene.add(liveEdges);
    if (++liveCooldown > 150) {
      liveCooldown = 0;
      if (liveEdges) scene.remove(liveEdges);
      liveEdges = buildLiveCloud();
      if (liveEdges && !liveEdges.parent) scene.add(liveEdges);
    }
    updatePick();
    renderer.render(scene, camera);
  }

  if (liveEdges) scene.add(liveEdges);
  renderer.setAnimationLoop(frame);
  log("3D — " + nodes.length + " nodes, " + state.data.edges.length + " edges");
}

/* ----------------------------- entry point ------------------------------- */
async function boot() {
  try { await loadData(); }
  catch (e) { log("could not load /graph.json — " + e.message); return; }
  try { THREE = await import(THREE_URL); }
  catch (e) { THREE = null; log("three.js CDN unreachable"); }
  if (THREE != null) {
    try { render3D(); return; }
    catch (e) { log("3D failed (" + e.message + ") — degraded 2D"); }
  }
  draw2D();
}

boot();