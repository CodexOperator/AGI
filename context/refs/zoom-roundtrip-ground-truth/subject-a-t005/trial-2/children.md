## Room Generation Algorithm

Core generator for discrete rooms: placement, sizing, and dimensional constraints. Produces axis-aligned rectangles with configurable min/max dimensions. Handles random placement within bounds and prevents overlap via collision detection. Output: array of room objects with position and dimensions. No corridor logic, no meshing—pure spatial layout.

## Corridor Routing & Connection

Algorithm to connect generated rooms with corridors. Selects room pairs for connection, routes corridors (straight, L-shaped, or orthogonal pathfinding), and ensures walkable paths between all rooms. Validates that corridors don't clip through walls or create topological issues. Output: list of corridor segments (start, end, width). Decoupled from room generation and meshing.

## Seeding & Deterministic PRNG

Establishes a seeded random number generator that controls all procedural decisions (room position, size, corridor routing). Same seed input guarantees identical output on every call. Integrates PRNG into room and corridor modules so they pull randomness from the seeded instance. Provides interface for setting seed externally.

## Mesh Generation (Geometry Factory)

Converts abstract room and corridor layout into Three.js geometry. Builds floor and wall meshes from room/corridor data. Handles z-fighting offsets, normal orientation, and vertex/face construction. Output: array of BufferGeometry objects (one per room floor, one per wall section, one per corridor floor/walls). No materials or scene integration—pure geometry.

## Layout Validation & Constraints

Validates generated dungeons against invariants: no overlapping rooms, all rooms within bounds, corridors don't intersect incorrectly, no unreachable spaces. Runs post-generation to flag invalid layouts before meshing. Returns validation report (pass/fail + violation list). Ensures consistent, playable output.

## Scene Integration & Rendering

Assembles validated geometry into the Three.js scene. Applies materials (floors, walls), positions meshes in world space, sets up lighting/shading if needed. Handles cleanup (dispose old meshes before regenerating). Provides interface to swap out entire dungeon by seed. Bridges the generation pipeline to the existing scene graph.
