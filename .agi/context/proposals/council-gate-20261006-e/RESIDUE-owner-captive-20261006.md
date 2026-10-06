# Owner design residue — captive ping-wake + orient `ok` (Shael 10:29 via plan-master)

**Status:** RESIDUE for SM mid-gate on g5.34.6 / g5.34.7 / g5.34.8 v6 LOCK. Pen self-perpetuating.  
**Owner (via PM):** riff the existing **capsule box-mail loop** as an **instant captive ping-wake** (not a minute poll); **orientation dump also captive** — wait for typed **`ok`** before continuing.

## Intent (plain)

| piece | today / v6 lean | owner add |
|---|---|---|
| Mail / ping | tip-sha detect + exit wake; interim often **polls** (60s) | **Instant** detect (block on refs/fs event or tight wait — **not** minute-class poll). **Captive:** hold a single-line gate until the driver answers; don’t just print-and-continue. |
| Orient dump | clear+reprint+header; driver reads and proceeds | After dump (and end mark), **captive prompt** — session **does not continue** until typed **`ok`** (exact token; other input held/rejected per DG). |

“Captive” = same family as engine `agi-captive` / fill window: **blocks the pane path** until closed, not a FYI line that scrolls away.

## Binding cuts (fold into open leaves)

### C-mail — instant captive ping (g5.34.6.2 + g5.34.8.1)

1. **Instant:** `monitor wait` / mail-wake must not default to ≥60s sleep as the happy path. Prefer: block on tip-sha change (poll ≤2s only as fallback if no inotify; packed-refs → short poll OK, **not** minute). Falsifier: new tip → wake/captive gate in **<5s** wall time when manned.  
2. **Captive gate:** on ping, present one captive line (riff capsule box-mail UX), e.g. `box: mail from <F> — read now? (y/N)` or owner-preferred wording; **block** until a full line. Keep W4: `(y/N)`, Enter=HOLD. Bot path (K7): bot may answer `y` via ssh/`i` as the driver.  
3. **Not a minute poll:** any interim shell that `sleep 60` between checks is **non-compliant** with this residue once landed; heartbeat 6h stays for re-arm only.

### C-orient — captive `ok` (g5.34.7.2 + shared bash arm)

1. After successful orient dump + `===== end startup =====`, print captive prompt: `orient ready — type ok to continue`.  
2. **Block** until a line that is exactly `ok` (case: DG picks; lean **exact `ok`**). No other command runs until then (history/eval deferred — same spirit as W3 “anything else” only **after** captive closes, or reject until ok).  
3. Falsifier: attach/`orient` → dump visible → **no** prompt/`i` activity accepted until `ok`; then normal shell.  
4. Re-arm with F1: each fresh driver attach gets the captive again.

### Cross-leaf

- One bash arm still shared (.6/.7/.8).  
- Captive must not write spurious bytes that break orient-dump sha check (print **after** end mark).  
- Monitor process-exit wake (g5.34.8) still wakes the Grok Bot; captive gate is **on the pane** for the driver (human or bot typing `ok`/`y`).

## Leaf sketch delta

| leaf | add |
|---|---|
| **g5.34.6.2** | captive mail gate + instant (<5s) |
| **g5.34.7.2** | post-dump captive `ok` |
| **g5.34.8.1** | monitor wait: no minute poll; exit feeds captive path |

## Non-goals

Auto-continue past orient · minute-class poll as SoT · captive that injects via watcher into `i` without driver (W2)

## Ask SM

Absorb into v6 PASS-with-amend (or stamp as must-carry residue on .6.2/.7.2/.8.1) without reopening Belam A+B scope.
