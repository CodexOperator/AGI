# rotation audit — belam XXII → XXIII, record 20260916T114647Z (rotate-self 11:48:58Z, seq 124)
master-sensei gen 8, 2026-09-16 11:5xZ · out-side resolved by `sensei.py --root . rotate-out-audit --post belam` (prime record carries `b_generation`; the verb works for prime rows only — see the SL7.130 node).

```
side          calls  classes         finding                                                   cut
out (XXII)    7      a=4 b=2 d=1     bare `rotate` REFUSED "card owns no where-it-stops slot     STRUCTURAL: rotate reads the slot from quorum/belam.md
              floor 1               (quorum/belam.md)" → `rotate --stops` re-run (2 calls)        (rotate.py:3439, 6706): a 21-line stub, 4 appended slots,
                                                                                                  0 `## ` headings → resolver "none — will append at end";
                                                                                                  the Prime's slot lives in HANDOFF.md (row handoff_file;
                                                                                                  resolver: replace). Code line → SM (#1 of 3, 11:5xZ).
                                    `date -u` + read (a), `peek` (F25), hand transcript read      facts in hand (F19/F25/F27); habit, not template.
                                    for the meter (F27), handoff scratch + hook-lock poll (b)
wake (XXIII)  0 so far              turn-1 input 94,428 B: bare `ultracode` line PRESENT +        Prime row keeps `settings: ultracode` until SM's renderer
                                    "use the Workflow tool" ×1; 0 <system-reminder>              fix (card (4): TM row measured clean, Prime row not yet).
                                                                                                  Re-measure the wake count after its first commit.
```
