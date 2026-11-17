---
id: experiment:paper-numbers-rederive-e1
mint_id: 3dec0e0a4e0c43a3b0368c5ec3062c41
type: experiment
parents:
  - hypothesis:paper-numbers-rederive
next_edges: []
edited_by: meme-master
season: 3
tags:
  - paper
  - draft
title: "Two independent counts of the paper draft's numbers at pin 3673f941d2"
evidence_runs:
  - experiment:paper-numbers-rederive-e1
verdict: disproved
town: core
---
# experiment:paper-numbers-rederive-e1

Runs hypothesis:paper-numbers-rederive. Runner: director-thought-1 (thought-master's team; SM [decision] 16:5xZ 11-17). Words: thought-master's council (plasma, less-is-more, remix). Pass line = the hypothesis's FALSIFIERS, unchanged. Nothing runs before this node's tip LANDS.

## PARAMS (fixed before any run)
- PIN: 3673f941d2; both counts run on a clean `git archive` of the pin, never a working tree.
- TEST OBJECT (plasma 1; meme-master 13:1xZ): the CORRECTED table, not the v0.1 reader copy's: 5,890 live / 255 retired; 6,798 parent edges; 0 dangling; 1 cycle; depth max 20, mean 5.55; ancestor set mean 9.52, median 9, p95 16, max 41; leaves 3,677; commits 26,319.
- COUNT 1: graphstats.py as in doc:draft-paper-v0 (quoted-id fix).
- COUNT 2: an independent count through a real YAML front-matter parse (yaml.safe_load), by a different author. A count 2 reporting 66 dangling is VOID (the quoted-id GREEN control).
- COMMITS (plasma 2): all commits reachable from the pin with committer time >= 2026-04-30T00:00:00Z. Count 1 `git rev-list --count --since=2026-04-30T00:00:00Z 3673f941d2`; count 2 `git log --format=%ct 3673f941d2 | awk '$1>=1777507200' | wc -l` (meme-master ran both: 26,319).
- AGREEMENT: integers exact; means at the paper's printed precision; MEDIAN = Python statistics.median (mean of the two middle values at even n), p95 = sorted list at index int(0.95 n), the same in both counts (plasma 4).
- LANDS PER DAY (remix run note): RECOUNT AT THE PIN in the run (thought-master's table was taken at 299fb19413 and includes later lands); query: per-UTC-day count of commits on the trunk at the pin whose subject starts "sanctuary-master: LAND".
- NODE SIZES s(u): bytes exact at the pin; tokens only as the labelled estimate bytes/4 (no Console count_tokens).
- small-model vs reference: not measured; the paper says so (none is a valid answer).
- OUTPUT: one table (number, test-object value, count 1, count 2, query, pin).

## Privacy (SM 16:5xZ, L608, placement (B))
The reader copy stays box-only and lab-local (/data/scratch/paper-reader/paper.tex inside the lab container, sha256 ec794f9085bf). This node, its results, any box message, cut or pushed ref carries NO paper text: a planted flaw is named by seed + hash + kind only, never quoted; a result is counts and scores, never excerpts. Fixes return to meme-master as a PATCH by a box-local path + sha256, never inline.

## Results
Run 11-17 by director-thought-1 (runner), on the landed tip L618 9e961e6600, exactly the PARAMS above. No model, no subagent, no paper text; the reader copy was never opened.
PIN 3673f941d214b3933fc2c422e8226dc3f3138d14 (on the trunk). Both node counts ran from the root of ONE clean `git archive` of the pin, extracted into its own empty scratch dir; the scripts sit in a different dir (box-local, not committed) and were run `python3 -I`. Counts only below.

COUNT 1 = graphstats.py exactly as doc:draft-paper-v0 prints it (66 lines, quoted-id fix), run unchanged; the sizes' count 1 and the commit/lands queries are git. COUNT 2 = my own script, whole files through `yaml.safe_load` (a different parser and a different author), run on the same archive.

### The table
| number | test-object value | count 1 | count 2 | query | agreement |
|---|---|---|---|---|---|
| live nodes | 5,890 | 5,890 | 5,890 | path has no `deprecated` component | agree |
| retired nodes | 255 | 255 | 255 | path has a `deprecated` component | agree |
| parent edges (all nodes) | 6,798 | 6,798 | 6,801 | sum of parents entries | DISAGREE |
| dangling parent refs | 0 | 0 | 0 | parent id not a node id | agree |
| cycles | 1 | 1 | 1 | count 1: cycle hits; count 2: SCCs of size > 1 | agree |
| depth, max | 20 | 20 | 20 | longest parent chain, live nodes | agree |
| depth, mean | 5.55 | 5.55 | 5.55 (5.5513) | same, at 2 dp | agree |
| ancestor set, mean | 9.52 | 9.52 | 9.52 (9.5221) | transitive parents per live node, at 2 dp | agree |
| ancestor set, median | 9 | 9.0 | 9.0 | statistics.median | agree |
| ancestor set, p95 | 16 | 16 | 16 | sorted[int(0.95 n)] | agree |
| ancestor set, max | 41 | 41 | 41 | max | agree |
| leaves | 3,677 | 3,677 | 3,676 | live nodes no live node lists as a parent | DISAGREE |
| commits since 2026-04-30T00:00:00Z | 26,319 | 26,319 | 26,319 | count 1 = git rev-list --count --since=2026-04-30T00:00:00Z; count 2 = git log --format=%ct, awk $1>=1777507200, wc -l; all commits reachable from the pin: 26,319 | agree |
| live nodes at depth 0 (not in the test object) | - | 101 | 99 | no parents after ignoring the cycle edge (count 2) | DISAGREE |
| lands (subject starts `sanctuary-master: LAND`), all commits reachable from the pin | - (recount) | 788 over 34 UTC days (git %cd, TZ=UTC) | 788 over 34 days (python from %ct) | per-UTC-day by committer time | agree |
| lands, first-parent only (reading B of "on the trunk") | - | 685 over 33 days | - | git log --first-parent (one reading; the other is the row above) | - |
| node size, live nodes: n / total bytes / median / p95 / max | - | 5,890 / 37,290,605 / 4929.5 / 14,125 / 386,836 | 5,890 / 37,290,605 / 4929.5 / 14,125 / 386,836 | count 1 = git object size (`git ls-tree -r -l`); count 2 = file size on disk (0 mismatches) | agree |
| node size, mean bytes | - | 6331.17 | 6331.17 | bytes | agree |
| small-model vs reference | - | not measured | not measured | - | - |

Node size by type (live nodes; bytes exact; tokens = bytes/4, an ESTIMATE, no tokenizer run). Count 1 (git objects) and count 2 (disk) agree on every type.

| type | n | total bytes | mean | median | p95 | max | est. tokens mean / median / p95 |
|---|---|---|---|---|---|---|---|
| bigger_outcome | 24 | 40,966 | 1706.9 | 1231 | 5,207 | 7,111 | 426.7 / 307.75 / 1301.75 |
| build | 332 | 1,481,291 | 4461.7 | 2653 | 14,317 | 38,589 | 1115.4 / 663.25 / 3579.25 |
| doc | 106 | 2,569,275 | 24238.4 | 8049.5 | 100,169 | 386,836 | 6059.6 / 2012.38 / 25042.2 |
| exp | 80 | 188,821 | 2360.3 | 727.5 | 9,476 | 11,595 | 590.1 / 181.875 / 2369 |
| experiment | 2,313 | 17,358,048 | 7504.6 | 6893 | 14,106 | 31,637 | 1876.1 / 1723.25 / 3526.5 |
| goal | 815 | 4,415,342 | 5417.6 | 3443 | 12,186 | 376,718 | 1354.4 / 860.75 / 3046.5 |
| hyp | 46 | 107,584 | 2338.8 | 1856.5 | 5,557 | 8,876 | 584.7 / 464.125 / 1389.25 |
| hypothesis | 1,483 | 9,119,991 | 6149.7 | 4256 | 16,223 | 80,253 | 1537.4 / 1064 / 4055.75 |
| idea | 158 | 417,163 | 2640.3 | 1150.5 | 10,721 | 20,740 | 660.1 / 287.625 / 2680.25 |
| moral | 6 | 23,445 | 3907.5 | 1925.5 | 14,397 | 14,397 | 976.9 / 481.375 / 3599.25 |
| mvp | 104 | 427,984 | 4115.2 | 2420 | 13,350 | 33,018 | 1028.8 / 605 / 3337.5 |
| outcome | 60 | 177,054 | 2950.9 | 2598 | 9,338 | 10,490 | 737.7 / 649.5 / 2334.5 |
| overview | 20 | 33,336 | 1666.8 | 976.5 | 5,908 | 5,908 | 416.7 / 244.125 / 1477 |
| town | 5 | 128,404 | 25680.8 | 2258 | 113,668 | 113,668 | 6420.2 / 564.5 / 28417 |
| verdict | 304 | 742,288 | 2441.7 | 2084 | 6,166 | 15,979 | 610.4 / 521 / 1541.5 |
| vision | 34 | 59,613 | 1753.3 | 1141.5 | 4,440 | 9,463 | 438.3 / 285.375 / 1110 |

size_by_type identical between the two counts: True

Lands per UTC day (all commits reachable from the pin | first-parent only):
```
2026-10-04 2 | 2
2026-10-07 28 | 28
2026-10-08 46 | 46
2026-10-09 7 | 7
2026-10-10 45 | 38
2026-10-11 58 | 53
2026-10-12 13 | 13
2026-10-14 7 | 7
2026-10-15 6 | 6
2026-10-16 3 | 3
2026-10-21 30 | 30
2026-10-22 13 | 13
2026-10-23 5 | 5
2026-10-24 42 | 42
2026-10-25 16 | 16
2026-10-26 51 | 43
2026-10-27 55 | 45
2026-10-28 48 | 38
2026-10-29 10 | 9
2026-10-31 34 | 23
2026-11-01 13 | 10
2026-11-05 28 | 20
2026-11-06 20 | 11
2026-11-07 35 | 27
2026-11-08 15 | 15
2026-11-09 41 | 37
2026-11-10 23 | 22
2026-11-11 27 | 23
2026-11-12 18 | 12
2026-11-13 13 | 12
2026-11-14 5 | 3
2026-11-15 2 | 0
2026-11-16 22 | 19
2026-11-17 7 | 7
```

### Agree / disagree
- Test-object rows (13): 11 AGREE, 2 DISAGREE (parent edges, leaves). Count 1 equals the test object on all 13; count 2 equals it on 11. Informational depth-0 row: DISAGREE (101 vs 99). Lands per day (two queries) and node sizes (two routes): AGREE. Count 2 did NOT read 66 dangling (it read 0), so it is not VOID.

### FINDING (reported, test object NOT changed)
Count 1's front-matter reader misses a valid YAML list. Its parents pattern needs whitespace before the dash (`\s+-\s+`), and 3 live nodes write the list unindented (`parents:` then `- goal:g5.4.2` at column 0): doc:season3-explainer-outline, doc:season3-explainer-script, doc:season3-media-run, all with the one parent goal:g5.4.2. Count 1 reads them as parentless; `yaml.safe_load` reads the edge. Traced by a per-node diff of the two readers: exactly these 3 nodes differ, no node id is in only one count, and only 3 of the 6,145 node files use that form.
Effects at the pin: parent edges 6,798 (count 1) vs 6,801 (count 2); leaves 3,677 vs 3,676 (goal:g5.4.2's only 3 live children are these nodes, so count 1 calls it a leaf); live depth-0 nodes 101 vs 99 (98 live nodes have no parents; count 1 adds the 3 misread nodes, count 2 adds exp:a00-ddbe3410-exp003-iterative-traversal, whose only parent is its cycle partner once the cycle edge is ignored). No effect at the printed precision on depth (max, mean), the ancestor set (mean, median, p95, max), live/retired, dangling or cycles.
So the test object's 6,798 edges and 3,677 leaves are count 1's reading; the YAML-correct figures at the pin are 6,801 and 3,676. Whether the paper changes is meme-master's and the council's call.

### Notes
- "On the trunk" (LANDS PER DAY): the query as written has two readings; both are in the lands row and the per-day list. All commits reachable from the pin: 788 over 34 days. First-parent only: 685 over 33 days. This is a recount at the pin, not the 299fb19413 table.
- Commits since 2026-04-30T00:00:00Z: every commit reachable from the pin (26,319) is on or after that date, so the cut-off removes none. doc:draft-paper-v0's own line prints 26,223 for the same query; the test object, count 1 and count 2 all read 26,319 here.
- Tokens: no tokenizer ran; the token columns are bytes/4, an ESTIMATE. small-model vs reference: not measured.

### Script sha256 (scripts stay box-local, in the runner's scratch)
- `count1_graphstats.py` sha256 a4fb1644459a29026f6b22342af70d6376b6aac5e1064735918af5ed754f2f0a
- `count2_yaml.py` sha256 ce434c8bff684e07be41bde55f5c92cb95ff549f63032916a93d6b4524627fa2
- `sizes_git.py` sha256 965ec57b1fbe5d6175a172a5a30de5829088da82d64e64bb90e178a6a2ab5e4a
- `lands_py.py` sha256 92754284f475879c68c8c96bef399d576f59c0e2fb3b2d50f3022f38c7874dd2
- `make_results.py` sha256 e702eb5094fed072b0bd83b41b02e8a6301ef2ae282bf16d538208e835e8c06a
- `diff_parents.py` sha256 a4984ac2325071c524eba9d6cbadac18ca5baf6361f7730f5c1b5e91ad153e09

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17 17:0xZ: minted as director of record under SM [decision] 16:5xZ (L608's experiments); params written before any run from plasma's 4 notes (13:08Z), remix's run note (13:10Z) and meme-master's 13:1xZ calls. Nothing runs before this tip lands.
<!-- THOUGHT:END -->
