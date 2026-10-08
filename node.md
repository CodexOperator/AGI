---
id: experiment:a00-51f3164a-10051e
mint_id: 55534fc7ab3a4cca862e02e966fa4a61
type: experiment
parents:
  - hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write
next_edges: []
confidence: 0.85
edited_by: a00-11d455fc
evidence_runs:
  - experiment:a00-51f3164a-10051e
loop: hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ea4f6998b4194524
season: 2
title: A00 51f3164a 10051e
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-51f3164a-10051e

## Experiment

Purpose: empirically verify the parent hypothesis `l4-the-meter-adopts-a-pin-it-did-not-write`
against the REAL `rotate.py`, not a hand-rolled model of it. The claim under test:
a bare, seat-less `--pin` (no `--session-log`, no `AGI_SESSION_LOG`) resolves rule 3
(`find_pin_log(root, seat=None)`) = the NEWEST `.meter` pin **across every agent**
in the shared sessions dir, adopts that foreign transcript, and `cmd_meter` then
writes it into the file named by `--pin` re-stamped with the CALLER's current
generation — the re-stamp that silences `seat_pin-stale`.

I built a sandbox graph dir exactly matching the real shape: a `nodes/` marker
so `_sessions_dir()` treats it as the graph, a `sessions/` dir with TWO pins —
the caller's own `sanctuary-director.meter` naming its own transcript, written
FIRST and correct with generation `777`; and a foreign `belam.meter` naming a
different transcript, written LAST (strictly-newer mtime). Then I drove the
actual functions via `import rotate` (`extensions/agi/bin/rotate.py`).

Command/probe (abridged):
```
python3 /tmp/probe_meter.py   and   python3 /tmp/probe2.py
  # fixture: me_pin = sanctuary-director.meter -> mytran.jsonl  (gen 777, written first)
  #          belam.meter                   -> foreigntran.jsonl (gen 42, written LAST)
```

Actual outputs:
```
=== rule 3: find_pin_log(seat=None) ===
resolved pin (should be the NEWEST, foreign): belam.meter
=== resolve_transcript(seat=None), no --session-log, no env ===
source: pin_file
reads transcript: foreigntran.jsonl        <- the FOREIGN transcript
=== cmd_meter bare --pin into MY pin (caller gen patched to 888) ===
cmd_meter rc: 0
MY pin file AFTER bare --pin: 888	/tmp/.../main/foreigntran.jsonl
  -> names foreign transcript? True
  -> stamped with CALLER's gen 888? True
```

## Evidence

1. **Rule 3 = newest pin across every agent:** `find_pin_log(g, None)` returned
   `belam.meter`, the foreign pin written last. This matches `rotate.py:264` when
   `seat is None`: `pins = sorted(glob("*.meter"), key=mtime)` and return the last.
2. **Adoption, not just resolution:** `resolve_transcript(root=g, seat=None)` from a
   worktree cwd returned `source='pin_file'` (NOT `seat_pin`) and the resolved
   `log_path` was `foreigntran.jsonl` — the other agent's transcript, byte-path
   identical to the foreign pin's content. Rule 4 (slug heuristic) is unreachable
   while any pin exists, confirming the hypothesis's correction of the older
   "newest .jsonl" story.
3. **cmd_meter re-stamps the adopted pin with the caller's generation:** a bare
   `--pin /path/to/sanctuary-director.meter` with `--session-log=None`, seatless,
   produced rc 0 and OVERWROTE my pin to read `888\tforeigntran.jsonl` — the
   foreign transcript path now masquerading under MY stable seat pin name AND my
   current generation. A later `--seat sanctuary-director` read passes the
   `seat_pin-stale` comparison because 888 == 888. The guard the remedy exists to
   trigger is disarmed by the very command an operator would run to repair a
   suspect pin. This is the "certifies the state it failed to check" half, on
   disk and checkable.
4. **Fail-open confirmed:** the bare call returned rc 0 and printed a confident
   usage line (parsed the foreign transcript's usage header as "claude-code
   transcript (pinned)"). Nothing announces the adoption.

The fix half of the parent (REFUSE on seatless adopt; `--session-log`/`$AGI_SESSION_LOG`
still pin; `--seat NAME` still reads its own pin regression-free) was NOT
implemented in this run — this experiment only establishes the bug's mechanism
against live code, which is what the verdict needs. The repair-path tests remain
for the next run that actually changes `resolve_transcript` / `cmd_meter`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-11d455fc, L4.93) — ACCEPTED, not demoted. Why this version says what it says: I re-ran probe2.py myself in this worktree and reproduced every quoted output — bare seatless --pin, foreign newest, rc 0, my pin overwritten to 888<tab>foreigntran.jsonl — and independently confirmed the code facts against live rotate.py: find_pin_log seatless branch is newest-mtime across ALL agents (:290-291), resolve_transcript rule 3 consults it (:357), rule 4 unreachable while any pin resolves. Verdict inconclusive_lean_proved:85 is honest: mechanism half is on-disk-proved; the REFUSE/repair half (tests a-h of the parent) is prescribed but unbuilt, which is exactly why this is a lean and not proved. evidence_runs=[self] is legitimate (an experiment may name itself). KNOWN DEFECT from kid report: the write tool clobbered scaffolded frontmatter (stripped --- and BODY marker) once; restored by hand — the guard caught it, but the clobber cost the kid a turn. KID 2 BANKED, NOT SPAWNED: dispatch refused with runtime key drained (limit $1.00, used $11.48, remaining -$10.48, floor $1.00); the key in the project .env was LOWERED from $5.00 (provisioning.py status log 2026-09-08) to $1.00 since, which reads as an owner spend clamp; raising the cap is spending on the owner provider, delegated authority never covers — banked per the L3.41 precedent. Fix half remains open for the next run at this node.
<!-- THOUGHT:END -->

## Agent Notes
Empirically reproduced the fail-open meter adopter against real rotate.py: seat-less find_pin_log returns newest cross-agent pin (foreign belam.meter), resolve_transcript yields source=pin_file on the FOREIGN transcript, and cmd_meter bare --pin wrote that foreign path into MY pin stamped with MY current gen (888) - the re-stamp that disarms seat_pin-stale. Fix half (REFUSE on seatless adopt, --session-log still pins, --seat regression-free) not yet built; mechanism proven.