---
id: experiment:a00-7558b2d9-ac8d3b
mint_id: c4dfa9ff87634761ba89a0d5074eeaf5
type: experiment
parents:
  - hypothesis:l3w2-rollover-genesis
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-7558b2d9-ac8d3b
loop: hypothesis:l3w2-rollover-genesis@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5acf5ed94496a92a
season: 1
title: A00 7558b2d9 ac8d3b
verdict: proved
---
# experiment:a00-7558b2d9-ac8d3b

## Experiment

Built the wave-2 genesis rollover into `extensions/agi/bin/season.py` per
`hypothesis:l3w2-rollover-genesis`: the kid builds and dry-runs only; the real
rollover is for the prime.

**What I did**

1. Rewrote `cmd_rollover` to add four options on top of the existing skeleton:
   - `--visions-from <dir|file>`: reads one markdown file per vision, body
     taken **verbatim** (owner text + gloss) — the strip is only the leading
     `# Title` heading; vision prose is never invented or edited.
   - `--name <name>`: writes `season_names = {1: <name>}` on the ladder
     through `write.py` (shell out), merged over existing names.
   - `--branch`: after the graph writes, `git checkout -b season/s<new>`
     (never pushes), then prints the next commands for the prime.
   - `--allow-unjudged`: bypasses the brief §2.9 stage gate, which otherwise
     **refuses** the rollover while any season-current overview lacks a
     judgment, printing the count.
2. The dry run prints every node it would mint (title, parents, season_parents,
   actor, season, moral_adherence, full verbatim body) and every ladder field
   it would set — and changes nothing.
3. The real run mints via the canonical `node_writer.write_node(..., bypass=True)`
   (owner-tier mint: 5 moral parents exceed the vision schema's `max_parents: 4`,
   so the owner bypass is required and matches `--actor owner`), stamps season
   via `AGI_SEASON` env so new nodes carry the **new** season, writes the ladder
   through write.py, then opens the branch.

**Commands / results**

- Full suite: `python3 -m pytest extensions/agi/tests/ -q` → `1765 passed, 1 skipped`.
- New red-first tests (5, `test_season.py::TestRolloverGenesis`): visions-from
  verbatim print; name+branch print; dry-run changes nothing; refuse-while-
  unjudged gate + `--allow-unjudged`; real run mints + names + bumps + opens
  `season/s2`. All red-first (failed on the old skeleton, green after).

## Evidence

**Dry run on this repo (nothing written, count unchanged):**

```
$ python3 extensions/agi/bin/season.py rollover --dry-run --visions-from .agi/context/visions --name genesis --branch
Rollover: season 1 → 2
[DRY RUN — no changes will be written]
Visions to mint for season 2:
  MINT vision:alive
    title: Alive
    parents: moral:faith, moral:love, moral:empathy, moral:antifragility, moral:beauty
    season_parents: overview:a00-1467544f-aaaa25-overview, … (17 season-1 overviews)
    actor: owner
    season: 2
    moral_adherence: 'unknown' for each moral parent
    body (verbatim, text + gloss): "the project feels alive. …" + ## Owner's gloss
  MINT vision:all-is-one          (title: All is one — one hand, one path)
  MINT vision:self-perpetuating   (title: Self-perpetuating, + decision method gloss)
Ladder writes:
  season_names[1] = genesis
  Bump ladder current_season: 1 → 2
Branch: git checkout -b season/s2 (never pushes)
```

On-repo node count before/after the dry run: `1439` → `1439` (no vision minted,
ladder `current_season` still `1`, `season_names` unchanged); `git status`
after shows only my edits (`season.py`, `test_season.py`) plus pre-existing
other-agent files, no new files from the run.

**Red-first tests (all 5, after implementation):**
```
$ python3 -m pytest extensions/agi/tests/test_season.py -q
25 passed in 7.08s
```

**Full repo suite:**
```
$ python3 -m pytest extensions/agi/tests/ -q
1765 passed, 1 skipped in 97.17s
```

Unexpected files present and left untouched (not mine): `.agi/context/visions/`
(prime's staged vision sources), `extensions/agi/bin/brief.py` +
`extensions/agi/tests/test_brief.py` (another agent), and sibling node
`experiment:a00-a18f229f-023f5c.md`.

## Notes
- Does not push, does not commit, does not run `grid.py commit`.
- The real rollover (minting the three visions into the graph, renaming season
  1 "genesis", bumping to 2, opening `season/s2`) is deliberately NOT run here —
  that is the prime's step per the hypothesis and brief §2.9/§wave 2.

## Agent Notes
Parent review (a00-35f43809 L3.08): accepted as proved. Independently re-ran `season.py rollover --dry-run --visions-from .agi/context/visions --name genesis --branch` on this repo — node count 1439→1439, ladder current_season stayed 1, season_names untouched, three visions printed verbatim from the prime-staged sources with 5-moral parents, actor owner, 17 season-1 overviews as season_parents. Re-ran `test_season.py` → 25 passed; full suite claim (1765 passed) consistent with new red-first tests present. parents: hypothesis:l3w2-rollover-genesis resolves; evidence_runs is a list naming the run itself (legit for an experiment). Real rollover correctly NOT run (prime step). No demotion.
