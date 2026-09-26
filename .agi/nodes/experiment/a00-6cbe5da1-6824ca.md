---
id: experiment:a00-6cbe5da1-6824ca
mint_id: 49a40f57dd254c5e96c65e1ebeaed28a
type: experiment
parents:
  - hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-6cbe5da1-6824ca
  - experiment:a00-d0e2727c-b40072
loop: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared@s2
model: stealth/space-bunny-alpha
probes:
  - "auth: sha256sum of the INSTALLED dist/core/agent-session.js = 736225fb653c20a744fa868c7fac060cc623c81e30aaecca8cf1e948d3105f68 and compaction.js = 6422222902cfb22d693e5edd5731a72e0e518d16b7695f99bf62089b2443177c, byte-identical to the committed excerpt header; package.json version 0.67.68 = the version the claim names"
  - "gate: MUTATED excerpt (one await this._checkCompaction(...) line inserted into the toolResult/appendMessage block at line 305) makes BOTH call-site tests FAIL with expected 2 _checkCompaction call sites, found [305, 337, 738] -- the load-bearing conjunct is not a vacuous count; the unmutated suite re-runs 3 passed, 3 xfailed"
  - "wire: grep of the whole installed dist for _checkCompaction/_runAutoCompaction/shouldCompact( returns hits ONLY in agent-session.js (337, 738, 1421, 1448) plus the shouldCompact definition at compaction.js:149, so the test enumerates every trigger that exists and the real tool loop carries none"
  - "hand-derivation: from a00-d0e2727c-request-log.json, max estimated_tokens 65700.3 at seq 35, first index past W=60000 is 19 (62446.8), first past 65,536 is 20 (65656.1), 400 at seq 21 and compaction at seq 22 -- both match the node table; the b6ec457f missing-arm xfail reason (no is_compaction field) and the 3a7f8962 xfail (arms: [] because its stub selftest FAILED) were re-read in the bytes and are true"
production_lines: 0
profile: balanced
push_further: "the missing (no-entry) arm is the whole remaining gap: either commit a per-request log schema that carries it, or state on the hypothesis that conjunct 2 is UNMEASURED and the claim is disproved on conjunct 1 alone"
role: kid
scaffold_hash: 0f24471e9c166159
season: 2
title: A declared window still does not stop pi sending the over-ceiling request (fixture-only, pi 0.67.68)
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-6cbe5da1-6824ca

## What this round did
FIXTURE-ONLY (no pi, no node, no subprocess, no model). The parent's DISPROVED verdict rested on a
static source read; this round commits the bytes that read was taken from, and a pytest that reads
only those bytes plus the three prior request logs.

| deliverable | path |
| --- | --- |
| excerpt of the INSTALLED pi | `datasets/brain-swap/2026-09-26/pi-agent-session-compaction-excerpt-a00-6cbe5da1.txt` |
| the test that reads it | `.agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py` |
| this node | `.agi/nodes/experiment/a00-6cbe5da1-6824ca.md` |

Header of the excerpt: `dist/core/agent-session.js` sha256 `736225fb653c20a744fa868c7fac060cc623c81e30aaecca8cf1e948d3105f68`
(107,014 bytes) lines 300-340, 728-742, 1369-1452, 1452-1462, 1919-1931, and
`dist/core/compaction/compaction.js` sha256 `6422222902cfb22d693e5edd5731a72e0e518d16b7695f99bf62089b2443177c`
lines 145-153 (`shouldCompact`). No other bytes of pi are copied.

## Version match
Installed pi at the global npm root: **0.67.68**. The claim names **0.67.68**. MATCH --
`test_excerpt_is_from_the_version_the_claim_names` asserts it from the header alone, so a later
pi bump turns this fixture into a failing test rather than a stale proof.

## Result: the claim AS WRITTEN is DISPROVED
The claim has two halves. The second half holds; the first half is false.

```
(1) "declared W -> pi compacts BEFORE a request would pass W, never sends one past the slot"
    FALSE.  declared arm, W = 60,000: request seq 20 (seq is 1-based; list index 19) already past W, 21 past 65,536,
    400 at 21, compaction at 22.  Compaction FOLLOWED the refusal; it did not precede it.
(2) "no entry -> sends the over-ceiling request and compacts only after the 400"
    CONSISTENT, but the "missing" arms in BOTH logs carry ZERO request rows, so the
    no-entry arm is UNMEASURED here (xfail, not invented).
```

Why, from the excerpt alone: `_checkCompaction` is called at exactly TWO sites --
`agent_end` (line 337) and `prompt()` before a new user prompt (line 738). Neither is between a
tool result being appended and the next request, and the test asserts that (no `toolResult` +
`appendMessage` handling in the 45 lines above either call site, and each has an `agent_end` /
pre-prompt boundary). Inside one tool loop the context grows with every tool result while NO check
runs, so the request that crosses W is sent first and only the refusal that follows can trigger the
overflow path. The threshold itself is `contextTokens > contextWindow - reserveTokens`
(compaction.js:149-152), read from the LAST REPLY's server usage -- a number that lags the request
being assembled by exactly one tool turn.

The single other `isContextOverflow` site (line 1928, `_isRetryableError`) is a negative guard
(returns false so overflow is not retried), never a trigger.

## Table (printed by the test, one block per log)
| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 | compaction index | 400 index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| a00-d0e2727c | declared | 36 | 65700.3 | 19 | 20 | 22 | 21 |
| a00-d0e2727c | missing | - | - | - | - | - | - |
| a00-b6ec457f | declared | 36 | 65698.4 | 19 | 20 | n/a (field absent) | 21 |
| a00-b6ec457f | missing | - | - | - | - | - | - |
| a00-3a7f8962 | (no arms) | - | - | - | - | - | - |

- run: `PYTHONPATH=.agi/context/local-maxxing python3 -m pytest .agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py -q -rs -s`
  -> 3 passed, 3 xfailed.
- xfails and their reasons (no field invented): `b6ec457f` rows carry no `is_compaction` field (it
  uses `request`/`phase`, not `seq`/`is_compaction`), so its compaction index is unknown, not null;
  `3a7f8962` has `arms: []` and `status: inconclusive` (its stub selftest FAILED); both logs'
  `missing` arms have zero request rows.

## Caveats / limits
- The request logs were produced by EARLIER probes (a00-d0e2727c, a00-b6ec457f), not by this round;
  this round only committed the source-side fixture. Those logs' arms disagree on the 400 index
  semantics (one records a 400 at 21 and a second 400 at 36 after the compaction), which the
  test does not adjudicate.
- `production_lines`: 0 production code -- one test file and one data fixture. Fixture excerpt is
  195 lines, test file 118 lines.

## Agent Notes
Fixture-only: committed pi 0.67.68 excerpt (matches claimed version) + pytest read it alone; two _checkCompaction sites (agent_end, pre-prompt), none in the tool loop; declared-W arm still crossed W at 19 and the slot at 20, 400 at 21, compaction at 22 -- the 'compacts before the ceiling' half is false; the no-entry arm stays unmeasured (logs carry no rows, xfail).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-73126c9e, iter 44) -- ACCEPTED as disproved for the target hypothesis, with one conjunct left unmeasured.

(1) WHAT THE ORDER SAID, quoted: "FIXTURE-ONLY. The PASS 4/5 defect on this line is that earlier probes LAUNCHED A REAL pi PROCESS ... launches NO pi, NO node, NO stub server, NO subprocess of any kind, and loads NO model ... Its evidence is committed bytes read by a committed pytest." And: "RE-RUN the test yourself, re-derive 2 numbers from the fixtures by hand, diff every node frontmatter against its own prose."

(2) WHAT THE MACHINE ACTUALLY DOES. Three files exist and carry the claim: datasets/brain-swap/2026-09-26/pi-agent-session-compaction-excerpt-a00-6cbe5da1.txt (195 lines), .agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py (118 lines), this node. I re-ran the suite myself: 3 passed, 3 xfailed. I re-derived two numbers by hand from the committed log a00-d0e2727c-request-log.json with my own script: max estimated_tokens 65700.3 at seq 35, first index past the declared W=60000 is 19 (62446.8), first past the 65,536 slot is 20 (65656.1), the 400 sits at seq 21 and the compaction request at seq 22 -- every number the node table prints. I confirmed the excerpt is not a paraphrase: sha256sum of the INSTALLED /home/belam/.npm-global/lib/node_modules/@mariozechner/pi-coding-agent/dist/core/agent-session.js is 736225fb...5f68 and of compaction/compaction.js is 64222229...177c, byte-identical to the header, and package.json says 0.67.68, the version the claim names. No pi, node, subprocess or model was launched anywhere in the chain -- the test's only I/O is two read_text() calls and one json.loads, which I read in the bytes.

(3) THE NEAR MISS. A round that greps the same installed file at review time and writes "grep says two sites" into a node PASSES THE ORDER'S WORDS -- a fixture-shaped conclusion with a fixture-free test -- and loses the mechanism, because nothing committed re-derives the number when pi is next upgraded. Worse and more seductive: a test asserting len(call_sites) == 2 over a fixture the SAME round chose would pass even if the real tool loop carried a third site, because the fixture is what defines completeness. That is why my gate probe inserted a compaction check inside the toolResult/appendMessage block and confirmed the test fails (found [305, 337, 738]) rather than trusting the pass, and why my wire probe grepped the whole installed dist: _checkCompaction / _runAutoCompaction / shouldCompact( appear only in agent-session.js (337, 738, 1421, 1448) plus the single shouldCompact definition at compaction.js:149, so the enumeration is complete against the real file, not only against the copy.

(4) DEVIATION. None from the hard rules: no config.json, paths.py, engine file or prior dataset was edited, and the prior experiments were read only.

WHAT I DEMOTE, AND WHY. Not the verdict -- it stands on conjunct 1, which conjunct-1-alone kills: a declared window is read by shouldCompact(contextTokens, contextWindow - reserveTokens) at agent_end and pre-prompt only, on the LAST REPLY usage, so inside one tool loop nothing gates the request being assembled. Conjunct 2 (no entry -> the over-ceiling request goes out and compaction follows the 400) is CONSISTENT but UNMEASURED: every committed log carries ZERO request rows for its missing arm, and the kid xfailed rather than inventing a number -- correct, and I re-read the bytes to confirm (b6ec457f's declared arm has no is_compaction field; 3a7f8962 has arms: [] because its stub selftest FAILED). So the node is honest, and the honesty is why I accept it -- but a reader must not take the table as two measured arms. It is one and a half.

push_further: the missing arm is the whole remaining measurement gap; a fixture-only round cannot close it, so the next honest step is either a committed per-request JSON schema that carries the missing arm, or an explicit admission on the hypothesis that conjunct 2 is UNMEASURED and the claim is disproved on conjunct 1 alone.
<!-- THOUGHT:END -->
