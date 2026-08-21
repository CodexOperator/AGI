## Seeded PRNG & Determinism

Foundation for reproducible generation. Implement a seeded random number generator (Seeded XorShift, Mulberry32, or similar) that takes the seed value and produces a deterministic stream of random numbers. This layer ensures that calling the generator twice with the same seed produces identical sequences, which cascades determinism through the entire pipeline.

## Room Generation & Placement

Create individual room entities with configurable dimensions (width, height within ranges), and implement 2D spatial placement logic that adds rooms to the dungeon without overlap. This includes deciding room count per dungeon, selecting random sizes from a defined range, and using collision detection or sweep-to-fit logic to position each new room in available space.

## Corridor Generation & Pathfinding

Connect rooms by generating corridors between them. Choose connection strategy (e.g., nearest-neighbor links, spanning tree, or layered connectivity) and implement pathfinding or tunnel-carving (L-shaped corridors, straight lines, or stairs) to join disconnected rooms. This ensures the dungeon is fully connected.

## Dungeon Layout Validation & Diagnostics

Validate the generated structure: verify no room-to-room overlaps, confirm all rooms are reachable (flood fill or BFS), check corridor continuity, and detect invalid states (e.g., isolated rooms, degenerate geometry). Provide diagnostic output for debugging seed-driven generation issues.

## Mesh Rendering (Floor & Walls)

Convert the abstract dungeon layout (room and corridor positions) into Three.js geometry. Generate floor meshes (quads) for traversable regions and wall meshes (quads or boxes) for room perimeters and corridor edges. Apply basic materials (MeshBasicMaterial per SPEC convention) and add the meshes to the scene graph so the layout is visible in the browser.
