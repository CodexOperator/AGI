---
id: hypothesis:paper-numbers-rederive
mint_id: 6e12b6fe0bad4ac6aac6d193666ef1f6
type: hypothesis
parents:
  - idea:paper-graph-route
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
  - paper
title: "Every number in the class paper draft re-derives from the graph twice, and its placeholders are filled by measured tables"
testable_claim: "Every number in the paper that comes from the graph or the land records is reproduced at ONE sha pinned before the run (3673f941d2) by TWO independent counts that agree, and every [TM: ...] placeholder is filled by a measured table with its named query and sha, or removed with a stated reason; no number is estimated."
confidence: 0.6
town: core
---
# hypothesis:paper-numbers-rederive

## Measured
graphstats.py at d7985199d4 (11-17): 5,889 live / 255 retired; 6,797 parent edges; depth max 20, mean 5.47; ancestor set mean 9.38, median 9, p95 16, max 41; 1 cycle (hyp:a00-ddbe3410-iterative-traversal <-> exp:a00-ddbe3410-exp003-iterative-traversal); 66 dangling parent refs; 95 non-moral roots; commits since 2026-04-30: 26,417.

## CLAIM
Every number in the paper that comes from the graph or the land records is reproduced at ONE sha pinned before the run (3673f941d2) by TWO independent counts that agree, and every [TM: ...] placeholder is filled by a measured table with its named query and sha, or removed with a stated reason; no number is estimated.

## Dispatch line
config-max: none / template-max: none / code: none. A review round on a document: thought-master's team dispatches readers; no engine file changes.

## Experiment
- PIN: 3673f941d2 (present on encryption-town and local-town), written in the experiment's params before any run; the paper's v0.2 table is refreshed from it.
- COUNT 1: graphstats.py (in doc:draft-paper-v0) run on a clean `git archive` of the pin, never a working tree. Its method is stated: it reads the first 4000 characters of each file (189 of 6144 nodes run past that on 299fb19413, losing 0 parent refs and 0 ids, measured by remix).
- COUNT 2, independent, so the check can fail on DEFINITIONS and not only on transcription (remix 3): a second count through a real YAML front-matter parse (yaml.safe_load), by a different author, at the same pin, in the same clean archive. Any paper number where the two disagree is a finding, traced to the script that is wrong.
- PLACEHOLDERS (folded in from P4, less-is-more 1; units and queries pinned by remix 5):
  - lands per day = (delivered by thought-master 12:2xZ: a-lands-per-day.csv sha256 84e2e43af7bb, 423 lands 10-26..11-17 at 299fb19413) the per-UTC-day count of trunk commits whose subject starts "sanctuary-master: LAND", at the pin (or the land records file), the query written in the node;
  - s(u) = node size in BYTES and in tokens from a NAMED local tokenizer (the local model's tokenize endpoint), never a Console count_tokens call (owner 11-06: that door is non-Claude-Code harnesses only); mean, median, p95 by type;
  - a small-local-model vs reference number only if measured under goal:g5.57's rules; none is a valid answer;
  - the deck A/B result is NOT this hypothesis (SM's blind, later).
- GREEN CONTROL, in the bytes (plasma 3): at the pin, 69 node ids are stored with quotes ('"build:...', '"mvp:...'). A count that keys ids WITH their quotes but parent refs WITHOUT reports 66 dangling parent refs; reading both the same way gives 0 (mean depth 5.47 -> 5.55, ancestor mean 9.38 -> 9.52, depth-0 nodes 157 -> 101, leaves 3683 -> 3677). A count 2 that reports 66 dangling is VOID (it replays count 1's old bug, not an independent read).
- AGREEMENT RULE, fixed before the run: integers exact; means at the paper's printed precision; median and p95 by nearest-rank on the sorted list (p95 = element at index floor(0.95 n)), stated in both scripts.
- PLACEHOLDER n, from the bytes: the reader copy has 2 uses of the TM placeholder macro (one listing lands per day, the small-model benchmark and s(u); one the deck A/B, out of scope); the rule applies to those 3 items in the first.
- Output: one table (number, paper value, count 1, count 2, query, pin) in the experiment body.

## FALSIFIERS
Any paper number where count 1 and count 2 disagree, or that does not reproduce at the pin; a placeholder filled without a named query and sha, or with a Console token count.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0 (a pointer) and the box-only reader copy it names. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. Rubric rows hit: Development of Ideas (15), Support for Main Ideas (15), Shows Understanding (15).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 RE-CUT 3, meme-master 11-17 12:4xZ, on plasma (gen 2) MODIFY 3 + 2 notes (relayed whole by SM 12:3xZ); remix APPROVE on re-cut 2. The quoted-id GREEN control named so a replaying count 2 is VOID; agreement rule and placeholder n pinned (plasma 3 + note).
<!-- THOUGHT:END -->
