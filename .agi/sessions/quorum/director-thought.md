# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.

## 0 STATE (2026-09-16)
- Re-stood on claude-sonnet-5/max per owner 06:3xZ resume order (prior dry Copilot window @369 killed).
- Tree-wide 09-14 PAUSE + FULL IDLE lifted by owner 06:5xZ broadcast (belam) — mint/dispatch/audit/merge-up all green again. No PAUSED line was in this card, so nothing to strike.
- TM ORDER 3 received + dispatched: `hypothesis:c2-digital-kuramoto-flip-mode` (chain 2), `dispatch.py . TM.02 --target ... --level small --tier parent --harness pi --branch`. Dry-run clean first. Parent `a00-08515464` (pid 2358398, branch `season2/loops/hypothesis-c2-digital-kuramoto-f-a00-08515464`) spawned and confirmed `status=running` — `inline_reaper=false` here, so dispatch.py returns immediately on spawn regardless of `--detach`; it is NOT a completion signal. Manifest: `.agi/sessions/iter-TM.02/manifest.json`.
- TM also reviewed prior D1 work and DEMOTED it: `hyp lm-round0-box-calibration-and-two-kill-tests` -> inconclusive_lean_disproved:60; `experiment:a00-51318335-e170a9` -> lean_disproved:60. Informational only, no action needed from this seat.

## 1 PLAN
- next: no polling. Wait for a nudge (parent completion, overdue notice, or TM message) before touching TM.02 again.
- when the parent lands: audit its branch bytes (diff vs MERGE-BASE, never a moved tip — F5), confirm it authored NO experiment node itself (only the 3 kid nodes), confirm the 3 probes (gate/wire/sign) ran from the bytes, run the registered merge-up workflow, validate links/schema, push.
- report: one line to thought-master always; belam gets a `[complete]`-tagged dm only per the figure-eight (lap-report rule) — never an untagged ping.
- do not mint/dispatch a second round myself; do not hand-write engine code (owner, 04e5070c9). TM mints every hypothesis node — I only ever dispatch what it already minted.

## 2 LANDED (prior round, closed 09-14)
- `experiment:a00-01a81f78-81defb`: proved; 5% mean loss delta 0.176350, 20% delta 1.024380, all 6/6 positive.
- `experiment:a00-51318335-e170a9`: inconclusive_lean_proved:85.
- Graph validation at close: 3064 resolved links, 0 broken. Merged `04994c52f`.

## 3 STOP
Waiting on thought-master's next order. Nothing else open.

## 4 TRAPS
- `links.py schema` is a dry report, not a clean-suite signal.

## 5 VERIFICATION
`git show --stat --oneline 04994c52f`
