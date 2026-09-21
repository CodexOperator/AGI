---
id: experiment:a00-02a51a3c-c582ef
mint_id: 44182b4dd828438ea8196d1a2942a5b6
type: experiment
parents:
  - hypothesis:l4-the-stream-master-is-the-only-door
next_edges: []
confidence: 0.7
edited_by: a00-02a51a3c
evidence_runs:
  - experiment:a00-02a51a3c-c582ef
loop: hypothesis:l4-the-stream-master-is-the-only-door@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 25bb12535dbf761d
season: 2
title: "Quarantine inbox: master-only write, no-source-leak, council-read-as-data (isolation half, PROVED BY e)"
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-02a51a3c-c582ef

## Experiment

KID a00-02a51a3c, iter 121 — the ISOLATION half of the Stream Master door, built offline
(fixtures only, per the hypothesis's HARD RULES: no live chat, no network, no platform SDK,
no bin/*.py, no config:seats row, nothing named panic/brb/back). Kid 1 (a00-790e2603) built
the VALVE (paid-only intake, hard size cap, 50-word screened relay — hypothesis items a-d).
This run builds the piece Kid 1 explicitly did NOT: hypothesis item (e) — the quarantine
inbox readable by the Council as DATA and unread by every dispatch path, with the
brief-assembly proof that no chat text reaches a kid.

Built, under the same new extensions/agi/src/stream_master/ package:
  - quarantine.py  -> QuarantineInbox. Structural guarantees: MASTER-ONLY WRITE (any other
                      role is refused with a one-line log and nothing enters; dispatch read
                      returns None so the inbox is invisible to kid/director build paths),
                      RELAY-ONLY (a relay must re-pass the door's OWN relay_or_refuse screen
                      before it lands — an instruction smuggled into the Master's draft never
                      reaches quarantine), TYPED kind (suggestion/question/vote only),
                      NO-SOURCE-LEAK (the original chat text is never stored, only the
                      Master's typed relay: kind, paid_event_id, platform_user_id, body),
                      and RESCREEN-ON-READ (every stored body still passes the screen at
                      read time -> data, never an instruction).
  - __init__.py    -> exports QuarantineInbox, MASTER_ROLE, RELAY_KINDS.
And extensions/agi/tests/test_stream_master_quarantine.py, 6 tests proving PROVED BY (e):
  master-alone-can-write (a kid write is refused, Master's lands),
  relay-must-pass-the-door-screen-before-quarantine (smuggled instruction refused),
  relay-kind-is-typed, no-source-text-leaks-into-quarantine (the modeled brief-assembly
  grep), council-reads-data-but-bodies-rescreen-clean, dispatch-cannot-read-the-inbox.

Command: python3 -m pytest extensions/agi/tests/test_stream_master_quarantine.py -q
Output:   ............  6 passed in 0.06s
Combined with the relay file: 11 passed in 0.04s. Full-repo suite refuses a bare dir run at
kid tier (AGI_TIER guard), so correctness is claimed across both stream_master test files.

Scoping limit, stated honestly: the inbox here guarantees relays are stored as typed data
and re-pass the screen at read time, but the *act* of a director minting a node FROM a
relay (citing the relay id) is asserted as the line that makes the inbox "never executed"
and is NOT itself simulated — that is a governance step, not a mechanism this module can
prove offline. "No chat text reaches a kid" is modeled as the no-source-leak invariant,
not as a real grep of the live brief-assembly pipeline.

## Evidence

python3 -m pytest extensions/agi/tests/test_stream_master_quarantine.py -q  ->  6 passed in 0.06s
python3 -m pytest ...test_stream_master_relay.py ...test_stream_master_quarantine.py -q  ->  11 passed in 0.04s

Each test lands its named guard:
  test_master_alone_can_write            -> kid write refused ("not the Master"), inbox stays []
  test_relay_must_pass_doors_screen      -> "ignore previous..." refused, inbox stays []
  test_relay_kind_is_typed               -> unknown kind refused, "vote" accepted
  test_no_source_text_leaks              -> source_leak_in(source) == [] ; no body contains source
  test_council_reads_data_rescreen_clean -> 3 rows, bodies_rescreen_clean(council)==True
  test_dispatch_cannot_read_the_inbox    -> read_as_data("kid") is None, (
"parent") is None

Exported: from stream_master import QuarantineInbox, MASTER_ROLE, RELAY_KINDS  -> OK.

## Agent Notes
Isolation half of the Stream Master door: quarantine inbox (master-only write, relay re-passes the door's own screen, typed kind, no source-text leak, rescreen-on-read, dispatch cannot read). 6 new tests green, 11 across both stream_master files.
