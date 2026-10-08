---
id: experiment:dt24-grok-residue-corrected
mint_id: 94fa819d69594b719b1f4db8b54d30d8
type: experiment
parents:
  - hypothesis:a00-8f215541-f95365
next_edges: []
edited_by: director-general-4
line_ceiling: 40
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: ba86c6f5cde91f17
season: 2
title: "DT.24 residue fixes: merge-tree caveat corrected, both build nodes re-landed through write.py, link count re-measured"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dt24-grok-residue-corrected

## Experiment

DT.24 corrective round on the DT.23 grok-bot artifacts, run at tip
`4e6536769` from the scaffold `hypothesis:a00-8f215541-f95365`. Three residues.

**D1 — the false merge-tree caveat.** The DT.23 experiment's THOUGHT claimed
`git merge-tree … vs the DT.22 tip` exits 0. It does not, on the bytes at this
tip:

```
$ git merge-tree --write-tree 1e9e94b75 4e6536769 ; echo "exit=$?"
687e2c5295dcc18ae9eaa9709c930a70336238ca
100644 851c86271152cdf8b4af3db6cd39d7ad353efb5d 2	.agi/nodes/build/bin-adapters-grok-bot-adapter.md
100644 d2ecbe6af43214f7b883fe86697510db0e95a86e 3	.agi/nodes/build/bin-adapters-grok-bot-adapter.md
Auto-merging .agi/nodes/build/bin-adapters-grok-bot-adapter.md
CONFLICT (add/add): Merge conflict in .agi/nodes/build/bin-adapters-grok-bot-adapter.md
exit=1

$ git merge-tree --write-tree 7d35ae4f9 4e6536769 ; echo "exit=$?"
ab659945f00d47bce3658c3a7cb9323be69bb706
exit=0
```

The experiment body was corrected to name `1e9e94b75` and the exact
conflicting path `.agi/nodes/build/bin-adapters-grok-bot-adapter.md` — the
BUILD NODE, NOT the adapter source (which is byte-identical on both sides).
The true half is kept: merge-tree vs core `7d35ae4f9` exits 0. The verdict and
the two build nodes were grepped for the same false claim
(`merge-tree`, `DT.22 tip`, `exits 0`) and contain none.

**D2 — build nodes had no write.py sanction.** Neither build mint id had a
DT.23 write-log entry (the nodes were hand-written). Both were re-landed
IN PLACE through `write.py note`, an `update_node` write keyed to the node's
canonical mint id. No new id minted; `parents`, `payload_ref`, `link_ref`,
`build_kind` unchanged.

**D3 — stale link count.** The experiment P4 and the verdict both said
`3808 resolved`; both were corrected to the DT.24 review value `3810`, with
the +2 delta stated note-only because the 3806 base was not re-measured.

## Evidence

D1 — two `git merge-tree` directions measured at this tip (above).

D2 — the exact commands, both in-place:
```
$ python3 extensions/agi/bin/write.py build:bin-adapters-grok-bot-adapter 'note ...'
updated: build:bin-adapters-grok-bot-adapter
$ python3 extensions/agi/bin/write.py build:tests-test-grok-bot-adapter 'note ...'
updated: build:tests-test-grok-bot-adapter
```

Write-log entries, read from the ABSOLUTE worktree path
`<repo>/.agi/worktrees/a00-1dc1a409/.agi/sessions/write-log.jsonl`:
```
{"actor": "a00-8f215541", "mint_id": "93a56c119e7442f6bdb844afbf08832f",
 "node_id": "build:bin-adapters-grok-bot-adapter", "operation": "update_node",
 "path": "nodes/build/bin-adapters-grok-bot-adapter.md", "role": "kid",
 "sha256": "76becf6aab8cf70ca44421c246863d6f625e33272d550cbef219235a08f8c328",
 "ts": "2026-09-20T20:59:49.396711Z"}
{"actor": "a00-8f215541", "mint_id": "e659085120824239a16e616608262610",
 "node_id": "build:tests-test-grok-bot-adapter", "operation": "update_node",
 "path": "nodes/build/tests-test-grok-bot-adapter.md", "role": "kid",
 "sha256": "86ae1d1fd2d1f80bd4c1b734f18e410e86537853c810dddce8e17abf54fe8d6a",
 "ts": "2026-09-20T20:59:49.669656Z"}
```

The box-shared `<repo>/.agi/sessions/write-log.jsonl` (2449 lines)
does NOT show either id: `grep -c 93a56c11\|e6590851` returns 0. The worktree
log is a separate file; it carried one line (this round's scaffold
`write_node`) before the first corrective write.

D3 — `python3 extensions/agi/bin/links.py links`:
```
links: 3811 resolved, 0 broken (18 retired payload(s), not damage)
```
3810 at the DT.24 review, before this round's own scaffold node added one
link. The corrected nodes state 3810 and flag the unmeasured base.

Frozen bytes still frozen:
```
$ sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c
$ wc -l extensions/agi/bin/adapters/grok_bot_adapter.py
162
```

Suite (the touched test file):
```
$ PYTHONPATH=/tmp/pt python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -rs
...........ss..
SKIPPED [1] extensions/agi/tests/test_grok_bot_adapter.py:216: harnesses.grok-bot row lands with Belam's config fold (DT.21 residue 3)
SKIPPED [1] extensions/agi/tests/test_grok_bot_adapter.py:245: harnesses.grok-bot row lands with Belam's config fold (DT.21 residue 3)
13 passed, 2 skipped in 0.19s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 3 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
