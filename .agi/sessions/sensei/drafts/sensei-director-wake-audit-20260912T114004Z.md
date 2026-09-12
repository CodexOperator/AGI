# wake-audit — sensei-director 10→11 (record 20260912T114004Z, rotate-self --stops, ack pre-answered `continue`)

drafted by master-sensei gen 3 @ 12:0xZ · predecessor aee3a4bc · successor 5187498e · row commit cfcc809

## WAKE 0 / OUT 1 — **the floor (owner 03:2xZ), first post to reach it on both sides**
history wake 102·4·3·4·4·17·3·0·0·4·0 → **0** · out 4·4·3·2·3·5·2·2·6 → **1**

### wake
Call 1 (11:40:56) = `git fetch` + branch lookup of the three gone parents + behind count = F5 harvest discovery = work. First words named the gone parents from STARTUP live-spawns. No orient reads.

### out
| n | ts | call | class |
|---|---|---|---|
| 84 | 11:29:57 | card §3 STATE rewrite — DURING the suite wait (83→85) | card, continuous (owner 09-09 standing) |
| 87 | 11:39:40 | SL2#19 numbers line to belam | last work act |
| 88 | 11:39:57 | `rotate-self --stops '<state>' --force` | rotate-self — the only call after the last work act |
All three 103731Z cuts took on the very next rotation: no hand merge (O2 — rotate-self merged inside), no Monitor teardown (O3), header now `# SESSION HANDOFF — sensei-director: … LIVE SCRATCHPAD (rotating at 0.2223 of the line, 11:39Z)` written by `_stamp_rotating_header` (O1).

## CUTS
None on this post. Re-measure next rotation for regression only. The shape to copy to every other post: card written as the work lands; `--stops` carries the delta; one call out.

## Side finding (write.py, routed): `replace body N:M` re-serializes the whole node
Applying the F14 re-word (one body line) via `write.py config:rotations "replace body 56:56 <file>"` also rewrote two unrelated `ack` first_turn entries (`—` → `—`: the JSON-in-YAML template strings are re-dumped with ensure_ascii) and added the EOF newline HEAD lacked. Round trip is not byte-identical on this node; a one-line edit should touch one line. Restored the two `—` lines by hand before committing; kept the canonical EOF newline (SL7.04's serializer).
