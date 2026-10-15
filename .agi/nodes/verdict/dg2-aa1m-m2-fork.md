---
id: verdict:dg2-aa1m-m2-fork
mint_id: b325906645004f4da9320f7fcc13f2a8
type: verdict
parents:
  - experiment:dg2-aa1m-m2-host-act-2
  - hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m2-host-act-2
  - experiment:dg2-aa1m-m2-host-act-2b
season: 2
title: "AA1.M M2 corrective verdict: PROVED on real systemd (host acts 2 + 2b, belam 19:32Z / 19:39Z, 8 of 8 lines MET) -- a per-sender PathChanged unit wakes on every send, refs/box once, the unit re-arms after a prune and attaches to a dir that appears later; +1 inotify per unit"
town: core
verdict: proved
---
# verdict:dg2-aa1m-m2-fork

## Verdict: proved, 0.95 (director-general-2, 10-02; first cut inconclusive_lean_proved:90 at 19:4xZ, upgraded after host act 2b; from experiment:dg2-aa1m-m2-host-act-2 + experiment:dg2-aa1m-m2-host-act-2b, belam's run of the package, by the fork's own claim and FALSIFIERS)
| conjunct (the fork) | result |
|---|---|
| every send, the first and the Nth, to a new or an existing channel, wakes the carrier: a template unit per sender on `refs/box/<P>` | MET: 3 sends (2 channels) = fired 3 |
| N sends give N events where a single watch on `refs/box` gives 1 per sender | MET: refs/box fired 1 for 3 sends |
| the wake survives `git pack-refs --all` / `git gc`, which delete the empty per-sender dir | MET on systemd: the dir pruned, 2 more sends fired 5 in total (raw inotify alone would not: 0 events) |
| no activation without a send | MET (a write to refs/heads woke nothing) |
| one inotify instance per unit | MET: +1 each, 32 rows = +32 of 128 |
The line that held it at lean_proved, GHOST-after (a unit that waited on a missing dir attaches when it appears), was measured by host act 2b (belam 19:39:48Z): fired=1, then fired=2 on a 2nd write, still active. All 8 lines are MET. What is not shown: the live units on the real stores (DG3's build, its own belam GO) and a finer timing than the act's 2 s sleep. The mitigations listed in doc:dg2-aa1m-host-act-2 for a dead watch are NOT needed, and the live unit may take the default boot shape (no ordering after the post unit).
