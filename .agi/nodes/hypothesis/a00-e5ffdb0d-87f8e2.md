---
id: hypothesis:a00-e5ffdb0d-87f8e2
mint_id: b15748d939f34904a2d6096d3af77933
type: hypothesis
parents:
  - goal:g7.31.2.1
next_edges: []
confidence: 0.85
edited_by: a00-e99aa251
evidence_runs:
  - experiment:a00-e5ffdb0d-session-pin-crosscheck
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "seat_occupation(row window @7, pid live, row session A, registry record session B @7)", "expected": "session-drift, never occupied", "observed": "state session-drift; session_drift director-seat: row session A != registry B", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "seat_occupation(row session A, registry record session A but window @9)", "expected": "session-drift, registry names no live @7", "observed": "state session-drift; registry names no live window @7", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "seat_occupation(row session A, no registry_dir)", "expected": "occupied, session_drift None, no registry read", "observed": "occupied, session_drift None", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "seat_occupation(row with NO session_id, registry session B)", "expected": "occupied, JOIN-miss sentinel fail-open", "observed": "occupied, session_drift None", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "seat_occupation(row session A, absent registry file) and unparseable registry file", "expected": "occupied, session_drift None, no crash", "observed": "occupied/None for both", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "seat_occupation(row window @7, pid 999999999 dead, registry session B)", "expected": "pane-drift, dead pane wins, session half not invented", "observed": "pane-drift, session_drift None", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "read committed seat_status.py: _session_pin_drift -> rotate._registry_read + _registry_matches_window_id; collect threads registry_dir; --list rebuilds its cell from seat_occupation", "expected": "call sites reach the changed bytes, one parser only", "observed": "seat_status.py +85/-9; --registry-dir wired in main; no second json parser", "result": "pass"}
profile: balanced
push_further: "Close the two goal-level gaps this node leaves open: (a) decide or enforce the absent-registry-record case so a pane-occupied row with NO session pin does not read occupied (probe E measured occupied today), and (b) give the session-drift fact a LIVE caller -- have viewport/formation pass registry_dir so the default injected view, not only --list, reads the session half."
role: kid
scaffold_hash: b6525b852aabeb41
season: 2
testable_claim: When registry_dir is supplied seat_occupation cross-checks the row session_id against rotate._registry_read for the row pid, window-matches via rotate._registry_matches_window_id, and a pane-occupied row whose parsed registry record disagrees reads session-drift; no registry_dir leaves the read byte-identical and reads no registry
title: "Session pin is read not only the pane pin: a stale registry record reads session-drift"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# Session pin must be read, not only the pane pin

## Hypothesis

`seat_status.seat_occupation` today compares only the PANE half of a seat's
pin: the row's `window` @id against live tmux, plus pid liveness. The SESSION
half — the `session_id`/`session_name` the seat-start JOIN wrote onto the row
from the per-session registry record `<pid>.json` — is never checked against
that record at read time, so a row whose pane is live but whose registry
record has moved on still reads `occupied`.

**Claim.** When `registry_dir` is supplied, `seat_occupation` cross-checks the
row's session pin against the registry record for the row's `pid`, reusing
rotate's EXISTING readers only (`rotate._registry_read` for the parse and
`rotate._registry_matches_window_id` for the live @id) — never a second
`<pid>.json` parser. A row whose `window` @id matches live tmux AND whose pid
is alive, but whose parsed registry record names a DIFFERENT `session_id` (or
no live `@id`), must NOT read `occupied`; it reads `session-drift`, naming the
seat. The fact must reach both the `seat_status.collect` rows and the
`seat_status.py --list` coherence surface, behind a `--registry-dir` flag.

## Falsifier

Row `window` @7, pid live, row `session_id` A, but `registry_dir/<pid>.json`
names `session_id` B (and/or a different window @id) -> the read must say
drift, not `occupied`.

## Fail-open edges (decided and documented)

- No `registry_dir` -> today's behavior byte-identical; the registry reader is
  never called.
- Row names NO `session_id` (the seat-start JOIN-miss sentinel) -> no drift is
  invented from an absent pin; the pane result stands.
- Registry file absent/unreadable while the pane matches -> fail-open, no
  crash, matching the existing absent-tmux-seam contract.

## Evidence

The claim was built and measured by
`experiment:a00-e5ffdb0d-session-pin-crosscheck`; see its probes and the
`test_seat_pane_registry.py` cases it names.

## Agent Notes
Built the session half of the seat pin: seat_status.seat_occupation now cross-checks the row session_id against rotate._registry_read/_registry_matches_window_id when --registry-dir is given; pane-occupied rows whose parsed record disagrees read session-drift, both fail-open edges tested, no-registry path byte-identical; 30+50 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.204 parent review (a00-e99aa251). (1) WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node" and "REVIEW THE BYTES, NOT THE RESULT FILE". (2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes I read and ran: the kid commit 27dd09bc5 changes seat_status.py +85/-9 -- a new _session_pin_drift() calls rotate._registry_read (the ONE <pid>.json parser) and _registry_matches_window_id, seat_occupation turns an otherwise-occupied row into session-drift when the parsed record disagrees, collect threads registry_dir, and --registry-dir rebuilds the --list cell from seat_occupation. I BUILT AND RAN rev_probe_kid.py against those committed bytes: 7 probes (session A vs registry B -> session-drift; registry @9 vs live @7 -> session-drift; no registry_dir -> occupied/None; no row session_id -> occupied; absent and unparseable registry files -> occupied with no crash; dead pid -> pane-drift; and a read of every changed call site) all pass. (3) NEAR MISS: an ABSENT registry record satisfies the kid words "absent/unreadable records fail open" but silently loses the goal case where a seat holds a pane and has no session pin at all -- probe E measured occupied there, so the strictly-worded goal falsifier is not settled; and NO live call site passes registry_dir (viewport/formation call collect pane-only), so the session half is opt-in and formation/pin readers do not yet see it by default. This is why the verdict is lean_proved:85, not proved. (4) DEVIATION: none; the kid own suite is its claim, these 7 probes are the parent evidence, and I recorded them through write.py, not by hand.
<!-- THOUGHT:END -->
