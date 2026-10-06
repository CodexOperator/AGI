# Policy — spawn-budget lock durable ACL (gate-u U3 / g5.4.1.4.8)

**Leaf:** `goal:g5.4.1.4.8` · mint `82d355870dbb45c5a9155b1af5c120fe`  
**Lean:** A — durable named+default ACL (default). Soft-skip B only on explicit SM/Owner flip (labeled U3 residue).  
**Apply seat:** **Belam/host OS once** after SM PASS — same ONE ACL window as U2. SM does not apply.  
**Date:** 2026-10-06-u · Package: `council-gate-20261006-u`

## Required ACL

| path | required |
|---|---|
| `.agi/sessions/.spawn-budget` (dir) | named `group:agi:rwx` + default `group:agi:rwx` |
| `.agi/sessions/.spawn-budget/.lock` | named `group:agi:rw` when file exists |

Note: sessions parent may already have defaults from gate-q / `.4.3.1`; existing `.spawn-budget` objects may predate inherit — **apply named ACL even if defaults exist**.

## Host recipe (Belam ONE ACL window with U2)

```bash
# from MAIN /data/work/agi
setfacl -m g:agi:rwx .agi/sessions/.spawn-budget
setfacl -d -m g:agi:rwx .agi/sessions/.spawn-budget
setfacl -m g:agi:rw .agi/sessions/.spawn-budget/.lock   # if exists
getfacl -p .agi/sessions/.spawn-budget
getfacl -p .agi/sessions/.spawn-budget/.lock
```

## Falsifier

1. As DG4: open/append `.agi/sessions/.spawn-budget/.lock` succeeds without setfacl redo **or** labeled U3 skip active.
2. `getfacl` shows named + default `group:agi:rwx` on budget dir; lock shows `group:agi:rw`.
3. This policy file PRESENT on cited tip.
4. Negative: belam-borrow from DG; reopen `.4.3.*` / `.4.2`; write.py; git rm; strip pytest.

## Out of scope

suite-stamp ACL `g5.4.1.4.3.*` · reopen `.4.2` · gate-t · write-path g5.4.1.6 · season3/capsule/Master
