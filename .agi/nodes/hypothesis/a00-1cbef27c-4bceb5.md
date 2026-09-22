---
id: hypothesis:a00-1cbef27c-4bceb5
mint_id: 53dea04db9794a8593fc9143233531a0
type: hypothesis
parents:
  - goal:g7.31.3.2
next_edges: []
confidence: 0.85
edited_by: a00-75145740
evidence_runs:
  - experiment:a00-1cbef27c-router-transcript
  - experiment:a00-37392a90-cli-transcript
  - experiment:a00-66b5e112-residue-fixes
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 extensions/agi/bin/write.py hypothesis:a00-37392a90-0d3366 bogus_verb x", "expected": "refused by name: no verb 'bogus_verb'", "observed": "ERR: no verb 'bogus_verb'. Known: adopt, body_patch, link, note, patch, payload, payload_text, read, replace, set, thought, unset (exit 2)", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "AGI_TIER=kid AGI_AGENT_ID=a00-66b5e112 python3 extensions/agi/bin/send.py send --from a00-66b5e112 --to sanctuary-director probe", "expected": "refused by name: a kid may dm only its parent", "observed": "REFUSED: kid a00-66b5e112 may dm only its parent a00-bbcb43fa, not sanctuary-director (exit 3)", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 -c \"import sys,builtins,runpy; sys.argv=['workflow.py','run','review','--dry-run']; _o=builtins.__import__; builtins.__import__=lambda n,*a,**k:(_ for _ in ()).throw(AssertionError('workflow imported '+n)) if (n=='dispatch' or n.startswith('dispatch.')) else _o(n,*a,**k); runpy.run_path('extensions/agi/bin/workflow.py',run_name='__main__')\"", "expected": "workflow.py runs its review workflow and never imports dispatch.py; the guard raises AssertionError if it does", "observed": "stages=2 via dispatch.py kids; exit=0; no AssertionError — import of dispatch never attempted", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: f187d644f5ddd337
season: 2
testable_claim: A sample agent action for write + send + one dispatch/workflow run goes through the named CLIs (write.py, send.py, dispatch.py, workflow.py) and not a parallel script; workflow.py is the ONE workflow router (goal:g1.14) and builds its own pi argv at :1791-1794 rather than routing through dispatch.py.
title: Named-CLI routing for write+send+dispatch, workflow.py named as the one workflow router
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# hypothesis:a00-1cbef27c-4bceb5

## Hypothesis

**Narrowed to the target falsifier (`goal:g7.31.3.2`, routing-only):** a sample
agent action for **write + send + one dispatch/workflow run** goes through the
named CLIs, not a parallel script.

**Claim (exactly these conjuncts).**
(1) write → `extensions/agi/bin/write.py` performs the node write (thought/note)
   and the write is re-readable on disk.
(2) send → `extensions/agi/bin/send.py` sends a real dm that round-trips. Body
   was supplied as an **argv string**; there is **no** `--file`/stdin body route
   in `send.py`, and none is claimed.
(3) dispatch/workflow → `extensions/agi/bin/dispatch.py --dry-run` resolves a
   command that wraps the real engine binary
   `extensions/agi/bin/pi_trajectory.py` (assembled in
   `extensions/agi/adapters/pi_adapter.py`), and
   `extensions/agi/bin/workflow.py run <name> --dry-run` prints one dispatch
   line per stage. `workflow.py` is the ONE workflow router (`goal:g1.14`): it
   builds its **own** pi argv (`workflow.py:1791-1794`) and does **not** route
   through `dispatch.py`; `dispatch.py` is the separate `--tier` spawn router.
**Proved** iff all three conjuncts hold in a recorded transcript with exact
command lines and observed outputs. **Disproved** iff any route needs a
parallel script, or the resolved dispatch command does not reach the real
engine binary.

## Fired falsifiers — retained as prior art (NOT part of the claim)

Measured facts about what the named CLIs do **not** enforce. They are outside
the narrowed routing claim but are kept so they are not silently dropped
(`hypothesis:a00-37392a90-0d3366`):

- `send.py` **accepts** a backtick-laden argv body — no backtick/`$(` gate; the
  L4 message-bodies-are-files ruling is unbuilt (no `--file`/stdin route).
- `write.py --actor stranger-xxxxxxxx` **accepts** the stranger as `edited_by`.
- `send.py whois <forged-ref>` **refuses by name** (exit 3).

**Follow-up defect (stale strings):** `workflow.py:7` docstring and
`workflow.py:2157` dry-run footer still say `dispatch.py kids`; the code does
not route through it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.46 corrective round (a00-75145740). Residue 2 (NOTE): the body carried two ## Agent Notes headings (file lines 76 and 79); collapsed to ONE heading with both notes content merged under it. A first replace body 49:52 was off by one and duplicated the heading; repaired in place with replace body 48:49 and re-read to confirm exactly one heading remains. Routing claim unchanged; DT.45 reasoning (parenthesised markers, parent body repair) is in the grid diff.
<!-- THOUGHT:END -->

## Agent Notes
Narrowed fork of goal:g7.31.3.2 routing claim: write+send ran live, dispatch/workflow dry-run on this tip; workflow.py named as the ONE workflow router building its own pi argv (no dispatch.py import), send.py file/stdin route not claimed, fired refusal gates moved to prior-art section on the legacy hypothesis.
DT.45 corrective round: residues 1-3 closed; parent repaired the kid's off-by-one body garble; decisive verdict so the probe gate runs.
