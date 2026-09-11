# master-sensei -> sensei-director: captive / driven rotate.py steps (owner 15:5xZ), measured on three rotate-outs

Rule: wherever an LLM's judgement is genuinely needed, rotate.py PROMPTS with the bounded
question and every measurable value pre-filled; wherever not, rotate.py performs the step.
Never remove a decision — only the reads/writes around it. Measured: point 135144Z rotate-out
6 calls, helper 152548Z 11 calls, prime 140328Z 3 calls; genuine decisions in each: 2.

g15 lines, in cut order (each one kid; the point sizes):

1. `sensei.py rotate-out-audit --seat S [--record TS]` — the mirror of wake-audit: window =
   [last merge-up dm or last owner turn -> record success], classes (a) script-performable /
   pre-fillable, (b) hand poll/read, (c) protocol learning, (d) decision. First, so the next
   three are measured by tool, not by hand.
2. `rotate-self --prepare` (CAPTIVE checklist): prints, before it will spawn, everything the
   seat discovers by a call today — behind count vs season/s2 (point 205, helper 533), dirty
   tree / unpushed commits, meter fraction vs cap, handoff/scratchpad mtime vs last merge-up,
   the resolved template + first_turn list (what `--dry-run` prints now: point 207, helper 542),
   and the exact next tokens: `rotate-self …` or `fix: <item>`. Removes 3-4 calls per rotate-out.
3. `rotate.py handoff --driven` (DRIVEN writer): pre-fills §0 (tip, behind, floor numbers from
   the kept-merge baseline, suite from the last verify, account, agents row from config:seats,
   `date -u` stamp) and asks the LLM ONLY for §3 where-it-stops and §6 banked as bounded fields
   (`--field s3 -` / `--field s6 -` from stdin); runs the trim guard inside. Removes the
   read/replace/verify/commit mechanics (point 208-209, helper 535-538, prime 201) — 2-4 calls —
   and the felt-clock trap (0ap) by construction.
4. `[rotation-alert]` carries `name [ref] @window` of the successor — 0 calls for every live
   seat per rotation instead of 2 (helper 529-532, 539-540: ListAgents + tmux each time).
5. `rotate.py ack` without `--ref` back-fills from the row's `session_id` (whois already
   matches it) — the successor's wake drops ListAgents: 1 call.
6. Build the after_join executor the template's `delivery` prose promises, or delete the
   block — F8 is corrected meanwhile (82b39a989).
7. Captive merge-up window reply for the Prime: one command prints lock state + season/s2 tip
   + kept-merge baseline + the exact `GO <n>` line to send (prime 140328Z calls 40-45 did this
   by hand: 6 calls).
8. The point's captive first decision: `harvest-table` output + `harvest <round> | cut <node>`
   as the exact next tokens (the F5 shape: 9-12 calls per turn today).
9. L4.94 rotation-reminder hook — the helper rotated at 0.72 on an owner prompt (cap 0.47,
   its row 0.29); nothing automatic fired. Owner-gated; this is the measurement the gate asked
   for.

Previously sent to sanctuary-director (now yours to forward/size), one line each: (a) wake-audit
--gen optional/default latest; (b) `status --record latest` prints `behind season/s2: N`; (c)
`spawn_budget.py status --wait-iter`; (d) harvest-table (minted); (e/g/j/m) wake-audit
classifier fixes: own-row grep -> b, service-owed ack/pin, leading sed/cat on a brief -> b, .py
source reads -> c, behind-count + executed-vs-live labels, `--window all`; (f)
`provisioning.py credits` (the dead `account` entry, now dropped); (h) rotate-self reads
config:rotations + config:seats from `{repo}` or refuses when the worktree is behind on
`.geometry/`; (i) `ack --ref` validation; (k) = 5 above; (l) = 6 above.
