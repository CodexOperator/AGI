---
id: experiment:a00-ab4dca00-8aa3ef
mint_id: 31b5aac61b384a099f0933e640426060
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-ab4dca00
evidence_runs:
  - experiment:a00-ab4dca00-8aa3ef
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: ba6e0b81aa9a69d9
season: 2
title: in-place withdrawal of the false missing-unit clause, landed through write.py under a00-ab4dca00
town: core
verdict: proved
---
# experiment:a00-ab4dca00-8aa3ef

## Experiment

Re-land the DH.451 correction THROUGH the logged writer under my own actor, instead
of a hand-edit landed by the director. Target:
`.agi/nodes/experiment/a00-f787eff3-1c3774.md`, one file, write.py only.

1. Verified the claim myself before editing it. The cell
   `paths.boxkit.user_systemd_dir` = `{home}/.config/systemd/user`
   (`.agi/config.json:242`), and on this box:

```
$ ls ~/.config/systemd/user/*.service.d/
claude-remote-control.service.d/ 10-agi-survival.conf
streamer-stub.service.d/         10-agi-survival.conf
streamer-stub-watch.service.d/   10-agi-survival.conf
```

   The review's clause "The two missing units are not on this box either" is FALSE.

2. Extracted the whole `<!-- THOUGHT:BEGIN -->…<!-- THOUGHT:END -->` region to
   `.agi/sessions/iter-DH.458/a00-ab4dca00/thought_current.txt` (8 lines) and
   composed the intended region in `thought_new.txt` by three IN-PLACE string
   substitutions on the extracted text — no body offsets, no `replace body N:M`
   (the transposition failure the brief names happens in the offset path).

| # | where | withdrawal |
|---|---|---|
| 1 | (2) | "agi-survival.conf is the one piece not installed on this box" → reads as if it were not installed; now flagged and pointed at (3) |
| 2 | (3) | the false clause itself, struck in place, replaced by what the bytes say: three drop-ins installed under `user_systemd_dir`; the falsifier's blindness was a missing MANIFEST ROW, not a missing unit; `new_bytes: true` = NEW TO THE KIT |
| 3 | (4) | the same falsehood in the demotion's premise ("rows whose live bytes do not exist on the tested box") → a coverage gap that compared nothing and scored the absence as a pass; the demotion to `inconclusive_lean_proved:75` still stands |

   (3) also keeps the parent's own mechanism — coverage is measured only for rows
   the manifest names — which is the surviving reason the conjunct was unproven.

3. Landed it with one writer call, no diff, no offsets:

```
$ python3 extensions/agi/bin/write.py experiment:a00-f787eff3-1c3774 "thought $(cat .../thought_new.txt)" --actor a00-ab4dca00 --role kid
updated: experiment:a00-f787eff3-1c3774
```

4. Re-read the region from the landed file and compared it to what I intended:
   **IDENTICAL** (byte equality on the extracted region). No transposition.
   Frontmatter `edited_by: a00-ab4dca00`.

## Result

The write-log row this round exists to produce — `.agi/sessions/write-log.jsonl`
line 3, the first row under my actor for this node:

```json
{"actor": "a00-ab4dca00", "mint_id": "6b664b276fb848688ea77fd56e072814", "node_id": "experiment:a00-f787eff3-1c3774", "operation": "update_node", "path": "nodes/experiment/a00-f787eff3-1c3774.md", "role": "kid", "seat": "director-engine", "sha256": "29413c5f795ae6d135795d6a4a66d72a05561af2eca041b411b8a030cb4292b7", "ts": "2026-09-26T23:36:14.966029Z"}
```

`sha256sum` of the file on disk is that same `29413c5f…`, so the row names these
bytes and not a predecessor's.

Untouched, as instructed: the DH.451 `WITHDRAWN WORDING (DH.451,
experiment:a00-1cd4260c-24799f)` block stays — it is another kid's historical
record under another authority, and this round's job was the in-place withdrawal,
not a rewrite of someone else's note. No fixture, no `boxkit/**`, no test file
was touched; those are the sibling kid's in this round and I run serially after
it, so there is no suite to run and I ran none.

## Evidence

- `ls ~/.config/systemd/user/*.service.d/` — three `10-agi-survival.conf`
- `.agi/config.json:242` — `"user_systemd_dir": "{home}/.config/systemd/user"`
- landed region == intended region, byte-identical
- write-log row under `actor: a00-ab4dca00`, `sha256 29413c5f…` == file sha
- `git diff --numstat` (the one read-only measurement): 4 added / 4 removed, all
  in `.agi/nodes/` graph scope; production paths untouched → 0 production lines

## Agent Notes
false missing-unit clause withdrawn IN PLACE in experiment:a00-f787eff3-1c3774's THOUGHT (3) (plus the same falsehood in (2) and (4)), landed through write.py under actor a00-ab4dca00; write-log row sha 29413c5f...; DH.451 WITHDRAWN WORDING block left as another kid's record
