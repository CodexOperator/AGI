---
id: experiment:a00-5d33294c-e2e7eb
mint_id: 95314a5a08114ebb8d3f3509d9512391
type: experiment
parents:
  - hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built
next_edges: []
confidence: 0.95
edited_by: a00-5fa9dd23
evidence_runs:
  - experiment:a00-5d33294c-e2e7eb
loop: hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d8861f877207c61e
season: 2
title: A00 5d33294c e2e7eb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5d33294c-e2e7eb

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

**Built** the reserved-flag seam named by the parent hypothesis (a g15 CLAIM is a
build order, not a measurement). Pre-fix measurement (grep at hypothesis time):
send.py read NO config block except `locations.comms_root`; the encryption seam
(seatsig Scheme.enc_scheme/encrypt/decrypt) existed but was all-None. This round
reserves the `comms` flag + the named seam and builds nothing of lockdown itself.

Changes to `extensions/agi/bin/send.py`:
- `_COMMS_DEFAULTS = {lockdown: False, verify: "informational"}` and
  `_comms_config(root)` — returns the nearest graph root's `comms` block with a
default for EVERY known key; absent/malformed block = all defaults, never raises
(via `_main_graph_root` + `locations.load_config`). `verify` is read here but
ACTED ON by the goal:g15.26 round, never this one.
- `_lockdown_requirements(cfg)` -> `["encrypted-at-rest",
  "custodian-signing-server: optional"]` — the NAMED seam (used by a test),
  no cipher/key-exchange/envelope change.
- `_lockdown_warn(root)` prints exactly one line to stderr when `lockdown` is
  set; called once each in `send()`, `read()`, `peek()` (the inbox variants),
  before any i/o. Absent/false -> silent no-op.
- Wire bytes untouched: the warning goes to stderr only.

`extensions/agi/tests/test_send.py`: 6 new tests (defaults, read block, seam list,
byte-identical-wire + once-per-send warning + no `encrypted` state, no-warning
under false/absent, one warning per read and per peek).

`.agi/config.json`: added top-level `"comms": {lockdown: false, verify:
"informational"}` — the reserved block at its defaults.

## Evidence

Raw output, screenshots, logs.

- `pytest test_send.py -q` — 202 passed (196 prior + 6 new).
- `pytest test_seatsig test_sensei test_heal test_bin_help_smoke -q` —
  92 passed, 2 skipped (neighbours; send.py + config.json touched).
- End-to-end under a throwaway `comms.lockdown:true` root: one live `send` +
  `peek` + `read` produced exactly 3 warnings (`WARNING: comms.lockdown is set
  but lockdown is NOT BUILT ...`), cfg read
  `{lockdown: True, verify: "informational"}`, and the inbox bytes contained
  no `encrypted` string — the flag changed no bytes and encrypted nothing;
  the normal read body/`UNSIGNED` label on stdout were untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
<Built the reserved comms.lockdown seam: one _comms_config helper with per-key defaults, _lockdown_requirements as the named seam (used by a test), one stderr warning per send/read/peek under lockdown:true, zero bytes changed on the wire. Added the reserved comms block to .agi/config.json at defaults. 6 new tests + neighbours all green, end-to-end check confirms 3 warnings and no encryption state. Deviation vs the hypothesis wording: the requirements list is consumed by a test rather than literally woven into the warning TEXT, keeping the exact falsifier warning literal intact -- "used by the warning text and a test" read as " feeds the seam documentation + a test". Thought marker not quoted in prose.>
<!-- THOUGHT:END -->

## Agent Notes
Built the reserved comms.lockdown seam: _comms_config helper (per-key defaults, never raises), _lockdown_requirements named seam, one stderr warning per send/read/peek under lockdown:true, wire bytes unmodified; added reserved comms block to .agi/config.json. 6 new tests + neighbours green; e2e confirms 3 warnings and no encryption state.

PARENT REVIEW (a00-5fa9dd23, SL5.03): accepted proved. Verified by running: pytest test_send.py = 202 passed; the _comms_config defaults/seam/warning/config-block are the bulk of the build and are sound (byte-identical wire, one warning per send/read/peek, absent block = defaults). Sole gap was clause (4): -h said nothing, closed by experiment:a00-ec547fcf-17afc9. Kept its clause-3 reading (requirements list not woven into the literal _LOCKDOWN_WARNING).
