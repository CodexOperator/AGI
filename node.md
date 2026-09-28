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
  - "gate: MUTATED excerpt (one await this._checkCompaction(...) line inserted into the toolResult/appendMessage block at line 305) makes BOTH call-site tests FAIL with expected 2 _checkCompaction call sites, found [305, 337, 738] -- the load-bearing conjunct is not a vacuous count; the unmutated suite re-runs 5 passed, 1 xfailed since the PASS 8 residue round"
  - "wire: grep of the whole installed dist for _checkCompaction/_runAutoCompaction/shouldCompact( returns hits ONLY in agent-session.js (337, 738, 1421, 1448) plus the shouldCompact definition at compaction.js:149, so the test enumerates every trigger that exists and the real tool loop carries none"
  - "hand-derivation: from a00-d0e2727c-request-log.json, max estimated_tokens 65700.3 at 1-based seq 36 (0-based list index 35), first index past W=60000 is 19 (62446.8), first past 65,536 is 20 (65656.1), 400 at seq 21 and compaction at seq 22 -- both match the node table; the b6ec457f DECLARED arm carries no is_compaction field (phase/request rows, so that arm is a dash row now, not a whole-test xfail) and the 3a7f8962 xfail (arms: [] because its stub selftest FAILED) were re-read in the bytes and are true"
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
`test_excerpt_is_from_the_version_the_claim_names` asserts it from the header alone.

CORRECTED (PASS 8 item 3): that guard is NOT a live pi-bump tripwire. It reads the committed
header and compares it to the committed `CLAIM_VERSION` constant; it never opens the installed
pi, and this fixture lives outside `extensions/agi/tests/`, so no declared `verify`/`rotation`
command collects it. It fails only if a LATER round re-copies the excerpt without bumping the
constant. What does pin it is provenance, not a watcher: the excerpt header carries the sha256 of
both installed files (above) plus `pi_version_installed`, and the mutation gate below is what
showed the test is not vacuous. Re-run command for a real bump:
`PYTHONPATH=.agi/context/local-maxxing python3 -m pytest .agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py -q -rs -s`.

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
`appendMessage` handling in the lines above either call site (45 for 738, 37 for 337 -- see the
lookback note below), and each has an `agent_end` /
pre-prompt boundary). Inside one tool loop the context grows with every tool result while NO check
runs, so the request that crosses W is sent first and only the refusal that follows can trigger the
overflow path. The threshold itself is `contextTokens > contextWindow - reserveTokens`
(compaction.js:149-152), read from the LAST REPLY's server usage -- a number that lags the request
being assembled by exactly one tool turn.

Lookback limit, stated exactly (PASS 8 item 6): (b) reads the lines ABOVE each call site in the
excerpt -- a full 45 above site 738 (source 306-737), and 37 above site 337 (source 300-336),
because the excerpt itself starts at 300. Any toolResult/appendMessage pairing above source line
300 is invisible to (b); the shortfall is printed by the test (`lookback shortfall ... (337, 37)`)
rather than clamped silently.

The single other `isContextOverflow` site (line 1928, `_isRetryableError`) is a negative guard
(returns false so overflow is not retried), never a trigger.

## Table -- the test's own stdout, VERBATIM (TMM.213 fix 3, 09-26)
Captured with `cd /tmp && PYTHONPATH= python3 -m pytest -q -s .agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py`;
the leading `.` / `x` characters are pytest's own progress marks. One block per log, as printed.
```
..lookback shortfall (excerpt starts mid-window), (source lineno, lines available): [(337, 37)]
.| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 | compaction index | 400 index | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a00-d0e2727c | declared | 36 | 65700.3 | 19 | 20 | 22 | 21 | measured |
| a00-d0e2727c | missing | - | - | - | - | - | - | no request rows (probe did not run) |
.| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 | compaction index | 400 index | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a00-b6ec457f | declared | 36 | 65698.4 | 19 | 20 | - | 21 | no is_compaction field |
| a00-b6ec457f | missing | - | - | - | - | - | - | no request rows (probe did not run) |
.| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 | compaction index | 400 index | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a00-3a7f8962 | (no arms) | - | - | - | - | - | - | no arms (inconclusive: FAILED before arms: fixture client produced an empty body and Stub JSON decoding failed) |
x
5 passed, 1 xfailed in 0.02s
```

Every row above is emitted by the test itself (PASS 8 item 5: before this round only the
`a00-d0e2727c` declared row was ever printed and the rest was hand-transcribed). The `past W` /
`past 65,536` columns are 0-based list positions inside the arm's `requests`; `compaction index` /
`400 index` are the `seq` / `request` VALUES the log records (1-based).

- run: `PYTHONPATH=.agi/context/local-maxxing python3 -m pytest .agi/context/local-maxxing/pi/test_compaction_sites_fixture_a00-6cbe5da1.py -q -rs -s`
  -> 5 passed, 1 xfailed (was 3 passed, 3 xfailed).
- the single xfail is `a00-3a7f8962`: `arms: []`, `status: inconclusive` (its stub selftest FAILED).
- an UNMEASURED arm is now a dash row with a reason, never a whole-test abort (PASS 8 items 1/4):
  `b6ec457f`'s DECLARED arm carries no `is_compaction` field (it uses `request`/`phase`), so its
  compaction index is unknown, not null -- and that arm is still read for the slot crossing and
  the 400, while `a00-d0e2727c`'s ordering assert (400 at 21 < compaction at 22) now actually
  runs instead of dying on the next arm. Both logs' `missing` arms carry zero request rows.

## Caveats / limits
- The request logs were produced by EARLIER probes (a00-d0e2727c, a00-b6ec457f), not by this round;
  this round only committed the source-side fixture. Those logs' arms disagree on the 400 index
  semantics (one records a 400 at 21 and a second 400 at 36 after the compaction), which the
  test does not adjudicate.
- `production_lines`: 0 production code -- one test file and one data fixture. Fixture excerpt is
  195 lines.
- dataset locations are read, not literal (PASS 8 items 8/10): the test takes its log directory
  from the cell `paths.local_maxxing.brain_swap_out_dir` and locates the excerpt by a glob under
  that cell's parent family, so the excerpt and the logs can no longer drift apart behind two
  date literals.

## Agent Notes
Fixture-only: committed pi 0.67.68 excerpt (matches claimed version) + pytest read it alone; two _checkCompaction sites (agent_end, pre-prompt), none in the tool loop; declared-W arm still crossed W at 19 and the slot at 20, 400 at 21, compaction at 22 -- the 'compacts before the ceiling' half is false; the no-entry arm stays unmeasured (logs carry no rows, xfail).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 33 (director-thought, PASS 8 residue round P8.07, TMM.210): corrected IN PLACE by kid a00-5728f5a0 (ledger experiment:a00-5728f5a0-91895a), carried into the commit by the director because cli.py done refuses a kid's edit to any node but its own. PASS 8 items answered here: (1/4) the ordering assert was dead code behind a whole-test xfail -> an unmeasured arm is now a dash row with a reason, and the d0e2727c ordering assert (400 at seq 21 < compaction at seq 22) runs -- parent a00-e06f5921 mutation-probed it (moving is_compaction to seq 19 FAILS the suite); (5) the table was partly hand-transcribed -> every row is now emitted by the test; the suite now reads 5 passed, 1 xfailed (was 3 passed, 3 xfailed -- the iter-44 parent review below keeps the OLD count as history); (3) the version guard is provenance, not a live pi-bump tripwire -- said in the body; (6) the lookback above site 337 is 37 lines, not 45 -- stated; (8/10) dataset paths come from the cell paths.local_maxxing.brain_swap_out_dir, not date literals; seq 35 -> 1-based seq 36 for the 65,700.3 maximum. NEW, named so PASS 9 need not find it: resolving that cell through paths.get_local runs a read-only `git rev-parse` subprocess, so the test is no longer I/O = read_text + json.loads only; no pi, node, model or network is launched. Verdict unchanged (disproved on conjunct 1; conjunct 2 unmeasured).
<!-- THOUGHT:END -->
