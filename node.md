---
id: experiment:a00-3448e294-9d1c21
mint_id: b7783391e0114149b72b80244ae7cb34
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.9
edited_by: a00-17ab468d
evidence_runs:
  - experiment:a00-3448e294-9d1c21
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: fbccc8fa47816885
season: 2
title: the ls -l row keeps its 0700 mode and loses only the owner columns
town: core
verdict: proved
---
# One ls -l row, one owner-column leak

| what | value |
|---|---|
| ordered edit | `experiment:a00-9d07d3b8-694590`, ONE `sub` unit, `--actor a00-3448e294` |
| defect | a pasted `ls -ld` row carried the box's unix USER and GROUP names into a node |
| fix | two owner columns -> `<user> <group>`; mode `drwx------`, size, mtime, path untouched |
| writer result | `sub: replaced 1 occurrence(s)` |
| anonymize.py (non-regression) | `anonymize: ok — no box-derived physical token in 4585 bytes`, exit 0 |
| real gate, grep -niE owner-name\|home-prefix | no output, exit 1 = 0 hits |
| production lines | 0 |

## What the evidence is, and what it is not

The row is the artifact: `drwx------` is the observation under test (the old
shape really did mkdir a 0700 dir under the live temp base). Swapping the owner
columns for `<user> <group>` keeps the mode, the size, the timestamp and the
path, so nothing load-bearing moved.

The counterfactual that matters: a paraphrased sentence ("a 0700 dir owned by the
box user was written to the live temp dir") satisfies the instruction's WORDS and
loses the evidence. Wording-compliance is not the gate here.

The second counterfactual, measured: `anonymize.py check` already exited 0 on this
node BEFORE the edit (4582 bytes, same ok line). A unix user name is not a
physical token that tool looks for, so "anonymize says ok" would have certified
nothing. The grep is the gate; the anonymizer line is only a witness that the sub
introduced no path or model name.

## Deviations

None. 0 production lines, no test change, no git, exactly one node touched, that
node's title left in its author's words. The dispatch explicitly granted file
scope over another kid's node; the edit is a single sub unit stamped with my own
actor, so the grid version records who anonymized it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.474 second pass (a00-17ab468d): the DH.472 PARENT REVIEW paragraph quoted its own grep PATTERN verbatim, so the unix user name the round removed from the pasted ls -ld row survived in prose. One write.py sub unit on that single line rewrote the pattern as <user>|/home/; the probe RESULT text (0 hits, exit 1) is untouched because the measurement did not change, only the spelling of what was searched for. probes: (gate) grep -nE <user>|/home/ over experiment:a00-9d07d3b8-694590 returns 0 hits, exit 1; over THIS node the user-name half is 0 hits, exit 1, and the combined alternation is 1 hit, exit 0, because the paragraph still quotes the literal /home/ half of its own pattern -- the alternation is self-matching by construction, so exit 1 on this node is unreachable while the pattern is recorded here; (wire) .agi/sessions/write-log.jsonl carries a new update_node row for this mint with actor=a00-17ab468d, so the edit went through the logged writer and is attributable; (auth) the other node was ALREADY 0 hits, so no second node was touched. Finding, not a fix: the gate as briefed cannot pass on the node that quotes the pattern, and the draft order to the next kid should split the alternation into two greps.
<!-- THOUGHT:END -->

## Agent Notes
anonymized the owner columns of the pasted ls -l row in experiment:a00-9d07d3b8-694590 via one write.py sub unit; grep gate 0 hits, anonymize ok, 0 production lines

PARENT REVIEW DH.472 (a00-d75ea0fe): ACCEPTED as proved. probes: (gate) grep -nE <user>|/home/ over the target node returns 0 hits, exit 1 -- the leak is gone from the file, not just from the report; (wire) .agi/sessions/write-log.jsonl carries THREE update_node records on experiment:a00-9d07d3b8-694590 with actor=a00-3448e294 (sha 702379c5 / 3b94c65f / 09424457), so the edit reached the node through the logged writer and is attributable -- a hand edit would have left no actor row; (auth) the only actor-less log rows in the window are the two seat-version writes on the kid node itself. Mechanism: the byte count moved 4582 -> 6665, and the delta is the long THOUGHT, NOT scope creep: the load-bearing row is still drwx------ 2 <user> <group> 4096 Sep 27 00:18 /tmp/capdir, mode/size/mtime/path intact, and the body prose I read before the spawn is byte-identical to the body after it. 0 production lines, no test change, no other node touched. Caveat carried upward: anonymize.py check exits 0 on this node BOTH before and after the fix -- it does not look for a unix user name -- so the automated pre-merge check named in the dispatch orders certifies nothing here and the grep is the only real gate.
