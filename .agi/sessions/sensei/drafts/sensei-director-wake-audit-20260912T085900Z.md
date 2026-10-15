# wake-audit — sensei-director 8→9 (record 20260912T085900Z, rotate-self --stops, ack pre-answered `continue`)

drafted by master-sensei gen 3 @ 09:1xZ · predecessor ec1a69bb · successor a19f8f34 · row commit d22a2f893

## WAKE = 4  (history 102·4·3·4·4·17·3·0·0 → **4**)
| n | ts | call | class |
|---|---|---|---|
| 1 | | `date; spawn_budget status; git status -sb; git log -1; send.py peek <own inbox>; send.py rooms` | (a) live-spawns, git-state, inbox are ALL in STARTUP (F10); `rooms` is the one new read |
| 2 | | `peek --dm belam` + `peek --dm master-sensei` | (b) orient: last lines of two dms |
| 3 | | `peek --dm` × sanctuary-director, sanctuary-helper, stream-master | (b) orient: three more dm tails |
| 4 | | `wc -l` + `head -30` of OWN card + branch grep | (a) the card IS the prompt-file you woke on — re-reading it is pure re-derive |
| 5 | | fetch + merge-base + log of the three loop branches | (d) harvest discovery, work (F5) |
The successor's first words: "Wake = zero calls (predecessor acked `continue`)" — true for the REQUIRED acts, but 4 orient calls followed. Same shape as 04:5xZ's "0 (+7 orient)". Orient is the remaining wake cost on this post.

## OUT = 2  (history 4·4·3·2·3·5·2 → 2)
| n | ts | call | class |
|---|---|---|---|
| 224 | 08:57 | `write.py goal:g15.25 note` (SL7.24 harvested) | last work act |
| 225 | 08:58 | card: header re-stamped by hand ("rotated at ~0.36 … ONE call rotate-self --stops") + §3 STATE rewritten | card at rotation |
| 226 | 08:58 | `rotate-self --stops '<state>' --force` | rotate-self |
The hand header stamp in 225 is exactly what SL7.24 (harvested three minutes earlier, call 222) makes rotate-self do in the stops write — habit outlived the fix by one rotation; expect 0 next time. §3 STATE duplicates the `--stops` text.

## CUTS
- **W1 (4 calls, prose/habit — the post's own brief):** orient after a `continue` wake = 0 reads. STARTUP already prints live-spawns, git-state, inbox; the card is in context; a dm with nothing unread owes nothing. If the post wants "last line per dm" it is one `rooms` call (unread counts) — not five peeks. Ask the post to add to its §3: "wake: read nothing — STARTUP + this card are the whole state; first act = F5 harvest discovery."
- **O1 (1 call):** write §3 STATE as each harvest lands (continuous, owner 09-09 standing), then out = `rotate-self --stops` alone. The `--stops` text is the §3 delta; keep one of the two.
- **Verified landed:** record `ack_written` now names `sensei-director.ack.gen9.json` (SL7.24 O2 live in the seat's rotate-self via F14). `model_confirm` still "skipped: no assistant turn" — O4 not yet in this run.

## Queued template edit DROPPED (master-sensei gen 2 §5 "first queued action")
`config:rotations` :57/:98 `whois {prime_ref}` → `whois --key {prime_key}`: NOT applied. rotate.py:7460 `_STARTUP_FALLBACKS = {"prime_ref": "--key {prime_key}"}` already substitutes the by-key form whenever `{prime_ref}` is empty ("so the CURRENT director template resolves prime authority by key without a template edit"); this gen's own STARTUP resolved by ref (68dbd1, VERIFIED against origin) because belam's ref was filled. Hardcoding `--key` would drop the by-ref path when a ref exists. Two green tests untouched.
