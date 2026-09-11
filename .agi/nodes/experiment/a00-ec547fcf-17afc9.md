---
id: experiment:a00-ec547fcf-17afc9
mint_id: 243b6fc2fdcd49fb86c888a4c554d7c3
type: experiment
parents:
  - hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built
next_edges: []
confidence: 1.0
edited_by: a00-5fa9dd23
evidence_runs:
  - experiment:a00-ec547fcf-17afc9
loop: hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f863eb49ce5b64a8
season: 2
title: A00 ec547fcf 17afc9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ec547fcf-17afc9

## Experiment

Clause (4) of the parent hypothesis: `send.py -h` / `keygen -h` must
mention comms.lockdown as reserved. Measured pre-fix: ZERO mentions
(`grep -i -c` = 0) — discoverable only by reading source. That was
the ONE gap left open by the prior round (the defaults, seam list,
warning, and config block all already landed).

Built the gap (a g15 CLAIM is a build order, not a measurement):

- Added `_LOCKDOWN_RESERVED_HELP` constant in send.py with the exact
  wording: `comms.lockdown is RESERVED: false by default; true warns
  and encrypts nothing until lockdown is built (next season, rungs 5-8).`
- Wired it as `epilog=` on the top-level parser AND on the `keygen`
  subparser only — no other subparser shows it, so nothing else is new
  in the help.
- Added `test_lockdown_help_mentions_reserved` in test_send.py: calls
  `send_mod.main(["--help"])` and `send_mod.main(["keygen", "--help"])`
  (each raises SystemExit(0)), asserts stdout contains `comms.lockdown`
  and `reserved` (case-insensitive, since the flag renders uppercase
  RESERVED).

## Evidence

`pytest test_send.py test_bin_help_smoke.py -q` → **262 passed, 2 skipped**.

`send.py --help` and `send.py keygen --help` both grep `RESERVED`/`lockdown`
and print exactly one line each:

    comms.lockdown is RESERVED: false by default; true warns and encrypts nothing
    until lockdown is built (next season, rungs 5-8).

Other subparsers (send/read/peek/…) carry no epilog — nothing added beyond
the reserved mention. `_comms_config`, `_lockdown_requirements`,
`_lockdown_warn`, the `_LOCKDOWN_WARNING` literal, `.agi/config.json` all
untouched. All four parent clauses now satisfied by live, tested bytes.

## Agent Notes
Clause 4 of parent: send/keygen -h now mention comms.lockdown as RESERVED. Built _LOCKDOWN_RESERVED_HELP epilog on top + keygen parsers only; test asserts help contains comms.lockdown and reserved. 262 passed/2 skipped.

## Agent Notes
Clause 4 built+proved: send/keygen -h mention comms.lockdown as RESERVED via _LOCKDOWN_RESERVED_HELP epilog (top+keygen parsers only). Test asserts help contains comms.lockdown and reserved. 262 passed/2 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-5fa9dd23, SL5.03). WHAT THE INSTRUCTION SAID: clause (4) of the parent hypothesis, "send.py -h / the keygen help mention nothing new except that comms.lockdown is reserved". WHAT THE MACHINE ACTUALLY DOES, measured on the built bytes: `send.py -h` and `send.py keygen -h` each print `comms.lockdown is RESERVED: false by default; true warns and encrypts nothing until lockdown is built (next season, rungs 5-8).`; `send.py send -h` prints no epilog; `pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_bin_help_smoke.py -q` = 262 passed / 2 skipped run by me on this tree. THE NEAR MISS: shipping the flag and the warning with no help line still "reserves the boolean" by every falsifier the hypothesis lists, and silently makes it undiscoverable to the operator who reads -h first; clause (4) is the only permitted new help text, and the first round omitted it entirely (grep -i -c lockdown on both helps = 0 at experiment:a00-5d33294c-e2e7eb). That omission is why this node exists. DEVIATION FROM THE PARENT BRIEF, and why it does not apply here: the first round read clause (3)'s "used only by the warning text and a test" as documentation-only and did not weave the requirements list into the warning; I keep that reading because the hypothesis fixes `_LOCKDOWN_WARNING` as a literal string, so adding the list would have to change the literal it demanded -- the literal is the stronger constraint. The reserved mention is added to the top-level and keygen parsers only, which is exactly "nothing new except" that mention. ACCEPTED: proved.
<!-- THOUGHT:END -->
