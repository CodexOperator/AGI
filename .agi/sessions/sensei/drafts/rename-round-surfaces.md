# Rename round — Sensei surface inventory (owner order via belam XIX 08:1xZ; master-sensei gen 6, 08:2xZ)

Order is strict: (1) point `sanctuary-director` → `point-director` at the point's next boundary; (2) `sensei-director` → `sanctuary-director` at that post's first boundary AFTER (1) has landed and the point has seated once under its new name. Never both in one commit — between them the string `sanctuary-director` is ambiguous.

**LIVE surfaces (the script renames; each is one line or one file):**
| surface | step 1 | step 2 |
|---|---|---|
| `config:posts` row `name` (posts.md:20 / :21) | row 20 | row 21 |
| `config:rotations` prime template `point-record` entry, `--post sanctuary-director` (rotations.md:108) | → `point-director` | — |
| `extensions/agi/briefs/prime-director-successor.md:12` "the point director `sanctuary-director`" | → `point-director` | — |
| `extensions/agi/briefs/seats.councils.fragment.md:48` active-set list | rename | rename |
| `extensions/agi/briefs/sensei-director-duties.md` (file name + 1 mention) | — | → `sanctuary-director-duties.md` |
| `extensions/agi/briefs/master-sensei-duties.md` | done now (routing = SM; no Sensei director), name note pending | — |
| `.agi/sessions/quorum/<name>.md` card, `seats/<name>.{key,handoff.md,bootstrap.json,ack.genN.json,wrapper.log}`, `.agi/worktrees/post-<name>`, `season2/posts/<name>`, inbox + `comms/season-2/dm/*<name>*`, `view-<name>` tmux, GUI label, alerts matrix, meter pin `.agi/sessions/<name>.meter` | all | all |
| `HANDOFF.md` (6 mentions, Prime's) | at (1) | at (2) |
| tests hardcoding the names as fixtures: `test_rotate_templates.py test_rotate_startup.py` read the LIVE node; `test_rotation_alert.py test_hierarchy.py test_heal_watch.py test_send.py test_sensei_*_audit.py …` (26 files name sanctuary-director, 8 name sensei-director) | SM's code side | SM's code side |

**HISTORICAL — verbatim, never rewritten (alias resolves lookups):** facts F8/F14/F16/F17/F22 in rotations.md, `edited_by:`/`thought_session:` cells, code comments (rotate.py ×12, heal.py ×3, cli.py ×1, rotation_alert.py ×1 — all provenance, no constants), 452 + 266 graph nodes, drafts, the owner quote in `skills/agi/SKILL.md:179`, dm logs' bodies.

**Grep guard for the script's fixture:** after step 2, `grep -rn "sensei-director" <live surfaces>` = 0 and `grep -rn "sanctuary-director" prime template + prime brief line 12` = 0; historical counts unchanged.
