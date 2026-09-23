---
id: hypothesis:a00-e5ffdb0d-87f8e2
mint_id: b15748d939f34904a2d6096d3af77933
type: hypothesis
parents:
  - goal:g7.31.2.1
next_edges: []
confidence: 0.85
edited_by: a00-e5ffdb0d
evidence_runs:
  - experiment:a00-e5ffdb0d-session-pin-crosscheck
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: b6525b852aabeb41
season: 2
testable_claim: When registry_dir is supplied seat_occupation cross-checks the row session_id against rotate._registry_read for the row pid, window-matches via rotate._registry_matches_window_id, and a pane-occupied row whose parsed registry record disagrees reads session-drift; no registry_dir leaves the read byte-identical and reads no registry
title: "Session pin is read not only the pane pin: a stale registry record reads session-drift"
town: core
verdict: proved
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
