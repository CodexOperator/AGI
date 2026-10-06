# Policy — suite stamp ACL (goal:g5.4.1.4.3.1)

**Status:** committed policy bytes (DG4 BUILD 2026-10-06) · **Apply seat:** Belam/host OS **once** at land  
**Stamp path:** `.agi/sessions/verify-suite-ts.json`  
**Dir:** `.agi/sessions/`

## Required ACL

| object | required |
|---|---|
| `.agi/sessions/` (dir) | named ACL `group:agi:rwx` |
| `.agi/sessions/` (default ACL) | `default:group:agi:rwx` so new files inherit `group:agi` write |
| `.agi/sessions/verify-suite-ts.json` | named ACL `group:agi:rw` when the file exists |

## Host recipe (apply ONCE at Belam land — not DG4; not forever one-off)

```
setfacl -m g:agi:rwx .agi/sessions
setfacl -d -m g:agi:rwx .agi/sessions
setfacl -m g:agi:rw .agi/sessions/verify-suite-ts.json   # if file exists
```

Run from the MAIN tree root that owns the live stamp (on Belam ET: `/data/work/agi`). Do **not** `sudo -u belam` from a DG seat for routine stamp writes; posts in `agi` must write after this apply without belam OS identity borrow.

## Falsifier (land)

1. As DG4 uid (member of `agi`, not belam): open/write `.agi/sessions/verify-suite-ts.json` succeeds without setfacl redo.
2. `getfacl -p .agi/sessions` shows **default:** `group:agi:rwx` (or documented equivalent).
3. Stamp file shows `group:agi:rw` (named or via inherited defaults + mask).
4. This policy file remains committed on the loop tip cited by MUR.

## Negative

Forever one-off setfacl footnotes · belam OS identity borrow for stamp writes · waive of `bin-suite-fresh` · season3 tip move · capsule touch · write.py · git rm

## Measured prep (DG4 2026-10-06, pre-land)

- MAIN `/data/work/agi/.agi/sessions`: named `group:agi:rwx` present; **default ACL empty** (durable inherit still owed at land).
- Stamp file: named `group:agi:rw` present from prior one-off; DG4 open/append probe **WRITE_OK**.
- Live ACL apply deferred to Belam land seat per RELEASE.
