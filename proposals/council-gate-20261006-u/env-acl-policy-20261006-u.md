# Policy — MAIN `.env` durable ACL (gate-u U2 / g5.4.1.4.7)

**Leaf:** `goal:g5.4.1.4.7` · mint `433ab7c8a8b54af48d024af9e4f94db4`  
**Lean:** A — durable named ACL (default). Soft-skip B only on explicit SM/Owner flip (labeled U2 residue).  
**Apply seat:** **Belam/host OS once** after SM PASS — never DG invent; never forever one-off footnote; SM does not apply.  
**Date:** 2026-10-06-u · Package: `council-gate-20261006-u`

## Required ACL

| path | required |
|---|---|
| MAIN `/data/work/agi/.env` (envfile-resolved) | named ACL `group:agi:r--` (read); write stays owner/belam |

## Host recipe (Belam ONE ACL window with U3)

```bash
# from MAIN root /data/work/agi — READ for agi posts; write stays belam-only
setfacl -m g:agi:r-- .env
getfacl -p .env   # expect group:agi:r--
```

## Falsifier

1. As DG4 uid (`agi` member, not belam): `test -r /data/work/agi/.env` succeeds **or** labeled U2 skip contract active (no unnamed PermissionError).
2. `getfacl -p .env` shows `group:agi:r--` (lean A).
3. This policy file PRESENT on cited tip.
4. Negative: world-readable `.env`; belam-borrow chmod from DG; reopen `.4.3.*` / `.4.2`; write.py; git rm; strip pytest.

## Out of scope

suite-stamp ACL `g5.4.1.4.3.*` · reopen `.4.2` · gate-t · write-path g5.4.1.6 · season3/capsule/Master
