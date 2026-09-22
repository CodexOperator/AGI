---
id: experiment:a00-bb77a6b7-durable-auth-probe
mint_id: 51ce99928029474aba499b3c1b5908c4
type: experiment
parents:
  - hypothesis:a00-bb77a6b7-000dda
next_edges: []
edited_by: a00-bb77a6b7
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q", "expected": "1 passed: the gate refuses a foreign target BY PARENT NAME and still delivers to the parent; the test builds its own agent.json under tmp_path, so no worktree-only session record is required", "observed": "1 passed, 20 deselected in 0.50s (rc=0)", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -c \"import sys; sys.path.insert(0,'extensions/agi/bin'); import send; from locations import find_project_root; r=find_project_root(); print(send._kid_parent_id(r,'a00-75145740')); print(send._kid_dm_refusal(r,'sanctuary-director','a00-75145740'))\"", "expected": "both None: the old probe id has no shared-session record, so the gate fails OPEN and the recorded REFUSED is not durable", "observed": "None; None", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'send_mod.main' extensions/agi/tests/test_kid_reports_to_parent.py", "expected": "the committed test calls send_mod.main (the real entry), not a stub", "observed": "224: rc = send_mod.main([\"send\", SEAT, \"let me out\"]); 232: rc2 = send_mod.main([\"send\", PARENT, \"here is my report\"])", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 93aba7e944de7d0d
season: 2
testable_claim: "DT.72 closes the open PRIMARY residue and both NOTEs on goal:g7.31.3.2 (base bf876667b): hypothesis:a00-37392a90-0d3366 probes[1] is the committed, self-fixturing pytest probe test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent (1 passed, 20 deselected), reproducible from committed bytes, while send._kid_parent_id(root,'a00-75145740') is None on the tip (the old probe's non-durability); hypothesis:a00-75145740-c77fbe and hypothesis:a00-856dc44a-5c85fe testable_claims (and the 856dc44a body) describe exactly that and no more; the goal residue table shows all three CLOSED with no stale next-parent line. No source change; production_lines 0."
title: "DT.72: durable pytest auth probe replaces ephemeral 37392a90 probes[1]; residue table shows all CLOSED"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-bb77a6b7-durable-auth-probe

## Experiment

DT.72 corrective round under `goal:g7.31.3.2`, base tip `bf876667b`. Closes
the MUR PRIMARY (a stale, non-durable auth probe) and the two NOTEs, and
refreshes the goal residue table. No engine/source file was touched
(`production_lines: 0`). Every node edit went through
`python3 extensions/agi/bin/write.py`; no node file was hand-edited.

### 1. PRIMARY — `37392a90` probes[1] before/after

**BEFORE** (ephemeral: the probe ran as a live kid whose `agent.json` lives
only in the `a00-f3048920` worktree, not under the shared root
`/data/work/agi/.agi/sessions`):

    {"conjunct": 2, "class": "auth",
     "cmd": "AGI_TIER=kid AGI_AGENT_ID=a00-75145740 python3 extensions/agi/bin/send.py send --from a00-75145740 --to sanctuary-director probe",
     "expected": "refused by name: kid a00-75145740 may dm only its parent a00-f3048920 (exit 3)",
     "observed": "REFUSED: kid a00-75145740 may dm only its parent a00-f3048920, not sanctuary-director (exit 3)",
     "result": "pass"}

**Falsifier on the tip** — the old probe cannot be reproduced from committed
bytes:

    $ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import send; from locations import find_project_root; r=find_project_root(); print(send._kid_parent_id(r,'a00-75145740')); print(send._kid_dm_refusal(r,'sanctuary-director','a00-75145740'))"
    warn: kid a00-bb77a6b7 has no spawned_by_agent record; the dm gate fails open (l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-)
    None
    None

`None` means the gate fails OPEN, so the recorded `REFUSED` was not a
property of the committed bytes.

**AFTER** (written with `write.py hypothesis:a00-37392a90-0d3366 'set
probes [...]'`, re-read from the node):

    {"conjunct": 2, "class": "auth",
     "cmd": "python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q",
     "expected": "1 passed: the gate refuses a foreign target BY PARENT NAME and still delivers to the parent; the test builds its own agent.json under tmp_path, so no worktree-only session record is required",
     "observed": "1 passed, 20 deselected in 0.50s (rc=0)",
     "result": "pass"}

Observed run on this tip:

    $ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
    .                                                                        [100%]
    1 passed, 20 deselected in 0.50s

The replacement cites no live or ephemeral agent id; the test builds its own
record under `tmp_path` (`_write_agent_record(graph, "a00-kid-1", PARENT)`).
`probes[0]` (gate, exit 2) and `probes[2]` (wire import guard, stages=2) are
unchanged. A DT.72 correction note was appended under the node's
`## Agent Notes`, and the node's THOUGHT was rewritten to this version.

### 2. `c77fbe` testable_claim before/after

BEFORE: `(1) ... probes[1] replaced by a tip-reproducible auth probe on live
kid a00-75145740 (REFUSED by parent name a00-f3048920, exit 3) ...`
AFTER: `(1) hypothesis:a00-37392a90-0d3366 probes[1] is the committed,
self-fixturing pytest probe ... it cites no live or worktree-only agent id
and is reproducible from committed bytes (landed in DT.72, evidence
experiment:a00-bb77a6b7-durable-auth-probe) ...`
A DT.72 alignment note was also appended under its `## Agent Notes`.

### 3. `856dc44a` claim before/after

BEFORE the durable-auth-probe claim did not say which node's probe was
replaced, inviting a reader to think `37392a90` probes[1] was carried.
AFTER testable_claim: `... scoped to hypothesis:a00-75145740-c77fbe: c77fbe
probes[0] — and ONLY that probe — is the committed self-fixturing ... This
round did NOT replace hypothesis:a00-37392a90-0d3366 probes[1]; that stayed
ephemeral until DT.72 ...`
BODY item 2 before: `... probes[1]/probes[2] are kept.`
BODY item 2 after (body lines 50-56 replaced): `2. **PRIMARY — a durable auth
probe, scoped to c77fbe probes[0] ONLY.** ... c77fbe's own
probes[1]/probes[2] are kept. This round did NOT touch
hypothesis:a00-37392a90-0d3366 probes[1] ...`

### 4. goal:g7.31.3.2 residue table before/after

BEFORE (DT.45 text): `... NO merge-up while residues>0. Next parent: DT.46 @
base tip after this §3d write ...`
AFTER: the table rows now read **CLOSED** for the PRIMARY (durable pytest
probe, `experiment:a00-bb77a6b7-durable-auth-probe`) and for both NOTEs, and
say `No residue remains open as of this DT.72 round, so merge-up is
unblocked.` `grep -c "Next parent: DT.46"` = 0. The goal THOUGHT was
rewritten to this version.

### 5. Verification

    $ python3 extensions/agi/bin/links.py links
    links: 3861 resolved, 0 broken (18 retired payload(s), not damage)

    $ python3 -m pytest extensions/agi/tests/test_send.py -q
    330 passed, 11 warnings in 33.79s

    $ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
    1 passed, 20 deselected in 0.50s

### Deviation and trap

**Deviation.** The brief said to refresh the residue table "via write.py ...
'note …'". `note` only APPENDS under `## Agent Notes` and cannot remove the
stale DT.45 text, so the table was whole-replaced with
`replace body 32:41 -` — the same sanctioned writer.

**Trap (worth a defect).** Two `write.py` invocations against the SAME node
issued in parallel (one tool batch) race: each reads the file, and the later
write clobbers the earlier, even though both print `updated:`. The
`thought`+`note` pair on `37392a90` lost the note, and the
`replace body`+`set testable_claim` pair on `856dc44a` lost the
testable_claim. Re-issued SEQUENTIALLY, both landed. A caller has no signal
that the clobber happened.
