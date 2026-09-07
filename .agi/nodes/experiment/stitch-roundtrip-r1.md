---
id: exp:stitch-roundtrip-r1
mint_id: 6aa5e46bb8864417a93adec72a6a897f
type: experiment
parents:
  - goal:g6.1
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - level3
  - stitch
  - g6.1
thought_session: season
title: Stitch level-3 nodes back into a runnable tree
---
**Built:** `extensions/agi/bin/stitch.py` (engine repo), 31 new tests in
`extensions/agi/tests/test_stitch.py`. Two modes: `--out DIR` materializes
every `nodes/level3/*.md` node's `payload_ref` into `DIR`, preserving
repo-relative structure; `--verify` writes nothing and reports drift between
the graph and the live engine tree in four categories. `--verify` is the
mode worth using — see below for why. Safety: refuses a non-empty `--out`
without `--force`, refuses unconditionally (no override) to write into
`--project` or `--engine-root` themselves or any subdirectory of either.

**Say the honest thing first.** Source text lives on disk exactly once —
`hyp:level3-node-anatomy` is explicit that it is never inlined into a node —
so for an *existing, currently-consistent* repo, `--out` materialization is
near-identity: resolve 73 pointers, copy 73 files. Measured against the real
corpus (`/home/ubuntu/work/agi-tree/nodes/level3/`, `/home/ubuntu/work/agi`):

```
nodes considered:     73
files written:        73
bytes written:         554,881
byte-identical:        yes — diff -rq against the real files: 0 "differ" lines
                        (spot-checked all 73 individually with diff -q, and
                        with diff -rq over the whole extensions/agi subtree;
                        24 "Only in real repo" lines are files outside
                        level3.py's declared scan scope — __pycache__,
                        tests/, non-.py files — not a miss)
materialize runtime:   0.40s
verify runtime:        0.78s (recomputes an ast walk per file for staleness)
```

It is not a compiler. Given the same source tree it does not reconstruct
anything `cp -r extensions/agi DIR` would not also produce, byte for byte.
Anyone expecting stitching to *do* something beyond that will be
disappointed, correctly.

**What the graph adds that `cp -r` cannot: an independent, checkable claim
about the tree.** `cp -r` has no opinion about whether what it copied is
complete or correct — it just moves bytes. The graph is a second, separately
mintable record of what the tree is supposed to contain, so `--verify` can
compare claim against reality in four ways a byte-mover has nothing to
compare against:

| # | Category | What it catches | Found on real data |
|---|---|---|---|
| 1 | `missing_payload` | node outlived the code | 0 |
| 2 | `orphan_files` | code outran the graph | 0 |
| 3 | `duplicate_payload_ref` | ambiguous materialization | 0 |
| 4 | `stale_contracts` | contract drifted from the file it describes | 0 (+ 0 unreadable) |

All four zero on the real 73-node corpus. **This is not evidence the checks
work — it is evidence the corpus is current**, generated in the same session
against the same tree state it is being checked against. The checks are
proven to fire correctly by 31 unit tests that inject each condition into a
synthetic engine/project pair (delete a payload file, leave a file
unclaimed, mint two nodes at one path, edit a file after minting its node)
and assert the category catches it — that is where confidence in the
mechanism comes from, not from the clean real-data run.

**Contract freshness (category 4) — solved without a hash, and here is
why a hash is the wrong tool for this job.** The obvious design named in the
brief is a content hash recorded at mint time, compared against a hash of
the current file. Evaluated and rejected:

- **No node has one.** `level3.py` — which this task does not own — never
  wrote a mint-time hash into any of the 73 real contracts. A hash check
  could only protect nodes minted after a generator change; it is silent
  about every node that exists today, which defeats the point of checking
  the *existing* corpus.
- **A hash is binary and coarse.** It fires identically on a changed
  docstring and a changed import — no way to tell which without re-deriving
  the contract anyway, which is the same `ast` walk the check would have
  needed to skip in the first place. It adds a stored field and a mint-time
  write path without removing the recompute step.
- `how` is *specified* as a pure, mechanical function of file content
  (`hyp:level3-node-anatomy`, confirmed in `exp:level3-scan-r1`: 1045/1045
  entries mechanically derived, 0 fabricated). A pure function does not need
  a fingerprint to detect drift — it needs re-running. So `verify_tree`
  imports `level3.analyze_file` by file path (same reuse discipline
  `level3.py` itself uses for `snapshot_goals.write_frontmatter` — never
  re-implemented) and diffs its fresh output against the stored contract,
  entry by entry, ignoring `why`/`perf`/`security` (free-text, model-owned,
  correctly not reproducible). This is strictly more informative than a
  hash — a real test (`test_verify_finds_stale_contract_after_source_edit`)
  shows it naming exactly which import was added, not just "changed."

**What this costs, named plainly, not hidden:** the freshness check is
coupled to `level3.py` staying importable and staying a pure function of
file content. If `analyze_file`'s derivation logic changes shape without
`stitch.py`'s comparison logic changing to match, every node looks stale
even though nothing about the code moved — a false-positive failure mode a
stored hash would not have, because a hash comparison does not care how the
hash was computed on either side. That is a real, named tradeoff, not a
solved problem: recompute-and-diff is right for *this* corpus today because
`how` is genuinely pure and cheap to re-derive (73 files, 0.78s total); it
would be the wrong choice the day that stops being true.

**A real bug, found and fixed in this task, not left in.** The first version
of `_extract_contract` located the contract's closing fence with a naive
"first ``` after ```yaml" regex. Run against the real corpus, it broke on
`build:bin-heal`: that node's `healer_ctx` entry has a truncated `how`
field whose text is a `write_text(f"""...```json...```...""")` call site —
the literal string itself contains a ``` sequence, so the naive scan stopped
there and fed a truncated, invalid fragment to `yaml.safe_load`, reporting a
false "unreadable contract." The file is valid YAML; the reader was wrong,
not the writer. This is the exact failure mode `exp:level3-scan-r1` already
named and fixed on the *writer* side ("bounded extraction to the harness
markers instead of naively splitting on ` ``` `, which the embedded
template's own markdown fences defeated") — I independently re-derived the
same bug on the *reader* side before catching it against real data, fixed it
the same way (bound on the `BUILD-CONTRACT` markers first, then take the
**last** ``` in that span, not the first), and added
`test_verify_reads_contract_with_embedded_backtick_fence` as a regression
test that reproduces the exact bin-heal shape. Flagged the underlying
`level3.py` trap (a `_cap()`-truncated `how` field can leave a fence-
lookalike sequence that will confuse the *next* consumer the same way) as a
separate background task rather than fixing `level3.py`, which this task
does not own.

**What did not work / is not solved:**

- Category 3 (`duplicate_payload_ref`) is detect-only. The anatomy node says
  duplicates "must be rejected at mint time" — `stitch.py` cannot do that,
  it can only report after the fact. Checked `level3.py`'s own mint loop:
  it disambiguates *id* collisions (same slug from two different files) but
  has no check against two different ids claiming the same `payload_ref`.
  In practice this cannot currently happen from a normal `level3.py` run
  (it iterates a deduplicated file list once), so it is a defense-in-depth
  gap, not an active defect — named here rather than silently assumed safe.
- The whole exercise is only as meaningful as "the graph was regenerated
  recently." A stale graph checked against a tree that moved on without it
  is exactly what these four checks are *for*, but this run could not
  demonstrate that on real data because the real data is not stale yet —
  only the injected-drift tests demonstrate the mechanism.
- `--verify`'s exit code defaults to 0 even with drift (report-only, matching
  this repo's own `--strict` convention in `evidence_gate.py`/
  `snapshot-goals.py`); `--strict` is required to make drift fail a run. A
  caller that forgets `--strict` gets a clean-looking exit code from a dirty
  tree — documented, not hidden, but worth naming since it is an easy
  footgun for whoever wires this into `driver.sh` (not done here — out of
  scope, and the anatomy node's ordering puts that after stitching, not
  inside it).

**Suite:** `python3 -m pytest extensions/agi/tests -q` → **451 passed, 0
failed** (420 baseline + 31 new; re-ran after the contract-extraction fix,
clean).