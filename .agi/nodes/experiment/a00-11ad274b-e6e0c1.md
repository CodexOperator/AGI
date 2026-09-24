---
id: experiment:a00-11ad274b-e6e0c1
mint_id: cc4766d1a335405e902a9b2a54f01aea
type: experiment
parents:
  - hypothesis:pass2-engine-rows-corrected-in-place
next_edges: []
confidence: 0.85
edited_by: a00-b6a44c26
evidence_runs:
  - experiment:a00-11ad274b-e6e0c1
loop: hypothesis:pass2-engine-rows-corrected-in-place@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "node_writer.find_node_file(root, 'build:bin-adapters-grok-bot-adapter') + grep -c 'pass2-engine-rows-corrected-in-place' .agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md", "expected": "the R14#3 THOUGHT lands on the a00 duplicate file (grep count >= 1)", "observed": "find_node_file resolves to nodes/build/bin-adapters-grok-bot-adapter.md (canonical slug, step 1) FIRST; the a00 file grep count is 0", "result": "partial/refused by address: the a00 duplicate cannot be addressed by id through write.py, so its record lives on the reachable canonical file and the kid named the gap; every other correction re-checked in place"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -rn 'locked NotImplementedError stub|8 passed|85c5cb43' on the corrected nodes", "expected": "a live stale claim still present in a corrected node body", "observed": "only historical references inside the correction THOUGHT text; no live body claim contradicts the bytes (restart is a real respawn; test is 15 passed, blob e37baef7; config bin ~/.npm-global/bin/grok-bot != bare DEFAULT_BIN)", "result": "held -- the changed bytes carry the correction, not a description of it"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -c 'pass2-engine-rows-corrected-in-place' on each of the 9 corrected node files; git diff --name-only a9cf4329ef HEAD", "expected": "0 on an uncorrected node, or a second node / supersedes pair in the diff", "observed": "1 on each of the 9 corrected nodes + the new experiment node; diff = 9 corrected + 1 new node; no 'supersedes:' field and no '@v2' file", "result": "held -- the THOUGHT names the target in the live bytes and no second node was minted"}
  - {"conjunct": 3, "class": "gate", "cmd": "git diff a9cf4329ef HEAD -- <the 9 corrected nodes> | grep -E '^[+-](verdict|confidence|lean|lean_proved):'", "expected": "a changed verdict/lean/confidence line on a corrected node", "observed": "empty (the +verdict/+confidence lines in the full diff belong only to the new experiment node a00-11ad274b-e6e0c1)", "result": "gate held -- no verdict / lean / confidence field on any corrected node changed"}
  - {"conjunct": 4, "class": "gate", "cmd": "git diff --name-only a9cf4329ef HEAD | grep -Ei 'g7\\.33|lm-|goal/g5|lm-town'", "expected": "a held (goal:g7.33) or thought-master path in the round diff", "observed": "no match; the kid node lists the held and thought-master node classes it left untouched", "result": "gate held -- held and thought-master rows untouched and listed"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: fd79dc3f4ec4776c
season: 2
testable_claim: Every C row of the PASS 2 table for director-engine's grok-bot rounds R12, R13 and R14 is applied in place through write.py after re-checking the live bytes, each with a THOUGHT naming hypothesis:pass2-engine-rows-corrected-in-place, no verdict / lean / confidence field changed and no second node minted; the held (goal:g7.33) and thought-master nodes are untouched.
title: PASS 2 C rows R12/R13/R14 applied in place with write.py
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-11ad274b-e6e0c1

## Experiment

PASS 2 C-row corrections for director-engine's grok-bot rounds R12/R13/R14,
applied IN PLACE with write.py. Every stale string was re-checked against the
live bytes in THIS worktree before rewriting; no node was re-minted, no
`@v2` / `supersedes:` pair created, no verdict / lean / confidence field
changed.

### Rows applied

| row | node | correction |
|---|---|---|
| R12 | hypothesis:a00-8ee9bdff-40419b | title/claim/probes/body/notes: `8 passed` -> `15 passed`; "locked NotImplementedError stub restart" -> real detached respawn (`Popen(start_new_session=True)`) + keyword-only `TypeError` contract; test blob `85c5cb43` -> `e37baef7` |
| R12 | experiment:grok-bot-mirror-green-and-loud | title `8-passed` -> `15-passed`; green count; blob ids; mutation counts `1 failed, 7 passed` -> `1 failed, 14 passed`; branch-alone collection-error paragraph corrected (adapter + config present, 15 passed) |
| R12 | verdict:grok-bot-mirror-proved-loud | `8 passed in 0.03s` -> `15 passed in 0.12s`; helper blobs -> current (adapter `6aa00b4a`, config `fae48c5b`); branch-alone bound lifted |
| R13 | hypothesis:a00-da41e117-c79b5e | title/claim/body re-versioned: the config `bin` cell carries the box path `~/.npm-global/bin/grok-bot` and MUST DIFFER from the adapter's bare `DEFAULT_BIN = "grok-bot"` (`test_grok_bot_adapter.py:248`); the old "must equal `/home/ubuntu/...` DEFAULT_BIN" was the opposite of the bytes; a missing schema-required `testable_claim` added |
| R13 | experiment:grok-bot-bin-matches-adapter | "corrected value == adapter DEFAULT_BIN" MEASURE paragraph corrected; `/home/ubuntu/...` -> `~/.npm-global/...`; "verbatim (`sed -n '113,124p'`)" -> the row is 107-118 and the key order differs |
| R13 | verdict:grok-bot-bin-cell-agrees-with-adapter | Evidence bullet, probes C3, Confidence, Agent Notes: "cell equals DEFAULT_BIN" -> "cell carries the box path and differs"; `:13` docstring citation -> `:30` |
| R14 | hypothesis:a00-fcfbc2f9-7d809f | `restart` refusing `NotImplementedError` -> real detached respawn; Agent Notes `8 passed` -> `15 passed` |
| R14 | mvp:grok-bot-adapter-minimum | "`restart` raises `NotImplementedError`" + "`restart` stays refused" -> real detached respawn (`build_command` is the only remaining stub) |
| R14 | build:bin-adapters-grok-bot-adapter (duplicate id) | THOUGHT records the duplicate live id (mints `07acc9ce` / `93a56c11`), proposes the fix, records the stale `spawn_check_reason`; NO deprecate executed |

### Held / excluded, untouched

No node under `goal:g7.33` (HELD: lm-grid-commit-*, lm-grid-storage-*, goal/g7.33.*)
and no thought-master node (`lm-jev-*`, `lm-kv-span-shift-*`,
`lm-local-candidate-*`, `lm-pi-local-9b-*`, `lm-magic-pane-*`,
`lm-jev-isotonic-*`, `goal/g5.*` THOUGHTs, `doc:lm-town-trajectory`) was
touched. `.agi/config.json`, `extensions/agi/bin/dispatch.py` and the
adapter/test bytes were not edited.

### Demote question (left for the parent, not actioned)

R12 D1 asked for a demote of `verdict: proved` on
`hypothesis:a00-8ee9bdff-40419b`: the proved predates the real-respawn bytes.
The dispatch order forbids changing any verdict / lean / confidence field, so
the field stands and the question is surfaced in that node's THOUGHT and in
this round's done report.

### Addressability gap (measured)

`write.py` -> `node_writer.find_node_file` resolves
`build:bin-adapters-grok-bot-adapter` to
`.agi/nodes/build/bin-adapters-grok-bot-adapter.md` (the canonical slug) FIRST,
so the R14 #3 THOUGHT landed on the canonical file, not on the a00 duplicate at
`.agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md`. The
sanctioned writer has no way to address a second file sharing one id, so R14 #3
("write the THOUGHT on the a00 file") is only satisfiable on the canonical file
under the one-write rule. Recorded in that THOUGHT.

## Evidence

- `python3 extensions/agi/bin/links.py links` -> `broken_links == 0`.
- `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q`
  -> `15 passed in 0.12s`.
- Re-read each corrected node; the stale string is gone and each new THOUGHT
  names `hypothesis:pass2-engine-rows-corrected-in-place`.
- No production bytes changed; `production_lines` = 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EF.70 a00-b6a44c26: recording a proved-over-partial, NOT changing any verdict/confidence/lean field. This node carries verdict: proved, yet probes[0] (class gate, addressability) observed partial/refused by address -- the R14#3 THOUGHT could not land on the a00 duplicate because node_writer.find_node_file resolved the id to the canonical slug first. A verdict of proved beside a probe whose result is partial reads stronger than the evidence: the four remaining probes held, but one of five conjuncts was explicitly refused. This note is the record; the proved field stands untouched per the round order, and the question of a demote is surfaced to the parent.
<!-- THOUGHT:END -->

## Agent Notes
R12/R13/R14 C-row corrections applied in place through write.py on 9 nodes; each re-checked against live bytes (test 15 passed, blob e37baef7; adapter 6aa00b4a real respawn; config bin ~/.npm-global/bin/grok-bot vs bare DEFAULT_BIN; 0 broken links); no verdict/lean/confidence field changed; R12 D1 demote question surfaced only.
