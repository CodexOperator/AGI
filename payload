## Dungeon Generation & Layout

Procedural or hand-crafted level design: rooms, corridors, spatial topology. Defines the navigable game world. Must respect SPEC.md §V4 (MeshBasicMaterial, no lights). Foundational — all other systems depend on having a dungeon to inhabit.

## Enemy AI & Behavior

NPC decision-making: idle stance, detection, pursuit, retreat, multi-enemy coordination. Gives the dungeon challenge and drama. Couples tightly with damage-logic (AI must model player threat). Plan for incremental complexity: stateless patrol → awareness radius → tactics.

## Combat & Damage System

Hit detection, damage calculation, health state, death handling. Core interaction loop—controls how player overcomes enemy obstacles. Must track invariants: no crashing on zero-health, state consistency during damage events. Couples with inventory (loot drops on death).

## Inventory & Loot Management

Item pickup, storage, equipment slots, stat modifications from gear. Player progression lever—loot incentivizes dungeon exploration and enemy defeat. Couples with quest rewards (milestone loot) and save-load (inventory state persistence).

## Quest System & Goals

Narrative objectives, reward chains, NPC dialogue hooks, milestone tracking. Gives player motivation and pacing. Must reference SPEC.md §T rows and mark completion as quests land. Couples with inventory (quest rewards) and enemy-ai (enemies as quest targets).

## Save/Load & Persistence

Character state serialization, dungeon progress checkpoints, progression retention across sessions. Enables long-play narrative. Couples with inventory, quest state, and enemy state. Leave multiplayer-net as a later phase; focus single-player save first.
