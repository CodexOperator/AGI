## Seeded RNG Module

Encapsulate deterministic random number generation. A seeded PRNG (e.g., seeded Math.random polyfill or Mulberry32) that takes a seed integer and produces reproducible sequences. Exports functions for random integers, floats, and weighted choices. This is the foundation for all other child tasks — all randomness in the dungeon must come through this module.

## Room Layout Generator

Produce room positions, dimensions, and type (e.g., normal, treasure, boss). Algorithm: grid-based placement with constraints (minimum separation, max dungeons per seed size), then perturb with seeded RNG to add organic variation. Output: array of room objects `{x, y, width, height, type}`. No rendering, no corridors yet — pure spatial logic.

## Corridor Connectivity Algorithm

Connect rooms with corridors (simple orthogonal paths). Algorithm: iterate rooms in seeded order, pick target room, carve corridor from source to target using Manhattan or A* pathfinding seeded by the RNG. Handle intersections (overlap = shared passage). Output: array of corridor objects `{path: [[x, y], ...]}`. Feeds into final dungeon topology.

## Dungeon Mesh Renderer

Convert room and corridor geometry into Three.js floor and wall meshes. Algorithm: iterate rooms and corridors, create plane geometry for each floor tile, extrude/stack for walls at room edges and corridor boundaries. Assign materials (basic material, no lights). Emit a single merged mesh group into the scene. Input: rooms + corridors; output: Three.js Group or Mesh ready for `scene.add()`.

## Determinism Verification

Validate reproducibility: run the generator twice with identical seed, serialize both dungeons to JSON, compare for exact match. Eyeball renders in browser side-by-side or toggle a visual diff (e.g., color code identical vs. diverged tiles). Ensures seeded RNG flows through all three prior steps without state leaks.
