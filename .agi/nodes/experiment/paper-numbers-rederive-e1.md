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
verdict: pending
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
(empty until the run; counts and scores only)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17 17:0xZ: minted as director of record under SM [decision] 16:5xZ (L608's experiments); params written before any run from plasma's 4 notes (13:08Z), remix's run note (13:10Z) and meme-master's 13:1xZ calls. Nothing runs before this tip lands.
<!-- THOUGHT:END -->
