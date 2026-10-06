# Season drafts g5.4.1.1.2–.6 (DG4 → SM gate → belam write)

**SoT =** `.agi/nodes/.geometry/engine-post.md` `### season` piece → projected `/var/lib/agi/<post>/bin/season`  
**NOT SoT =** `extensions/agi/bin/season` (do not create as the live surface)

## Sequencing

1. **g5.4.1.1.5 first** (or hard-block): ladder `current_season` → `3`. See `g5.4.1.1.5-ladder.STATUS.md`. If still `2`, **do not** land .2.
2. **g5.4.1.1.2** — add `### season` piece (`g5.4.1.1.2-season-piece.draft.sh` + insert note). Same-build: inline `_get_current_season` into write.py; fix test_untrusted_lane.
3. **g5.4.1.1.3** — move season.py + season tests (+ optional import-send set) to `deprecated/` (never git rm).
4. **g5.4.1.1.4** — repoint skills/callers to projected `season` judge; drop alignment; post-doc-sync.
5. **g5.4.1.1.6** — only mandatory if .3 chooses move-all import-send tests; else track as prefer-boxes residue.

## Files

| file | leaf |
|---|---|
| `g5.4.1.1.5-ladder.STATUS.md` | prereq status + exact patch for belam |
| `g5.4.1.1.2-season-piece.draft.sh` | proposed POSIX judge body |
| `g5.4.1.1.2-engine-post.insert.md` | slot after `### box` |
| `g5.4.1.1.3-deprecate.plan.md` | exact mv paths |
| `g5.4.1.1.4-repoint.plan.md` | callers/skills |
| `g5.4.1.1.6-rotate-send.residue.md` | rotate/import-send residue |

## Geometry coupling

Land geometry **C4** (DG boot false) only **after** season .2–.4 builds — DG4 is the live capsule (see `GEOMETRY-README.md`).
