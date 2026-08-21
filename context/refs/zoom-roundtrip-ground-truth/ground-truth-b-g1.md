# Ground truth claim list — Subject B: idea:goal-playable-dungeon-crawler

Source: `nodes/idea/goal-playable-dungeon-crawler.md` (full file, frontmatter + body).
Built by the opus orchestrator BEFORE any decomposition ran. Not shown to any haiku agent.

Categories: DESC = description, INV = invariant citation, DEP = dependency,
PATH = file path, ACC = acceptance criterion.

| id | cat | atomic claim |
|----|-----|--------------|
| B-D1 | DESC | This is the root goal node for GOALS.md §G1 |
| B-D2 | DESC | The aim is to upgrade the dungeon-crawler scene |
| B-D3 | DESC | The scene is built with Three.js |
| B-D4 | DESC | Upgrades proceed one node at a time |
| B-D5 | DESC | Title is "Goal G1: playable dungeon crawler" |
| B-D6 | DESC | Confidence is 1.0 / status open |
| B-P1 | DEP | Candidate child node: town-scene |
| B-P2 | DEP | Candidate child node: dungeon-generation |
| B-P3 | DEP | Candidate child node: damage-logic |
| B-P4 | DEP | Candidate child node: enemy-ai |
| B-P5 | DEP | Candidate child node: inventory |
| B-P6 | DEP | Candidate child node: quests |
| B-P7 | DEP | Candidate child node: save-load |
| B-P8 | DEP | Candidate child node: multiplayer-net |
| B-I1 | INV | Every chain landing code must respect SPEC.md §V invariants |
| B-I2 | INV | §V4 is cited by identifier |
| B-I3 | INV | V4 content: the scene has no lights |
| B-I4 | INV | V4 content: MeshBasicMaterial only |
| B-I5 | INV | §T rows must be marked as work lands |
| B-F1 | PATH | GOALS.md is referenced by name |
| B-F2 | PATH | SPEC.md is referenced by name |
| B-A1 | ACC | Verify that it renders in a real browser |
| B-A2 | ACC | An HTTP 200 proves nothing about WebGL output |

Totals: DESC 6, INV 5, DEP 8, PATH 2, ACC 2. n = 23.

## Scoring rule (identical to subject A, fixed before seeing any output)

A claim counts as RECOVERED if the reconstruction asserts it explicitly or in an
unambiguous paraphrase. Partial/vague gestures do NOT count. A path counts only if
the actual filename string is present. An invariant citation counts only if the
identifier (§V4, §V, §T) is present; restating the rule without the id counts as
"content-without-citation" and is tracked separately.

Pooled totals across both subjects: DESC 16, INV 5, DEP 9, PATH 3, ACC 4. n = 37.
