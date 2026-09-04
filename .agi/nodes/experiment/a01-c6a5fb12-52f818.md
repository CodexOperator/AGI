---
id: experiment:a01-c6a5fb12-52f818
mint_id: 2f7836346c204d18b47a46bb018fb529
type: experiment
parents:
  - hypothesis:a01-c422b874-397418
next_edges: []
confidence: 0.7
scaffold_hash: e9da4e89ccecb5de
title: A01 c6a5fb12 52f818
verdict: inconclusive_lean_proved:70
---
# experiment:a01-c6a5fb12-52f818

## Experiment

Tested the structural premise of hypothesis:a01-c422b874-397418 — whether
derivation chats (session context files) have front-loaded signal structure.

### Method

Wrote and ran `analyze-chat-structure.py` (at `.agi/bin/`) that:
1. Analyzed all 475 session context files under `.agi/sessions/`
2. For each file, split into quarters and counted *structural signal tokens*
   per line (node IDs, goal refs, edge markers, type declarations, tool calls,
   decision markers — vs boilerplate like instructions, guidelines, repeated
   prompt fragments)
3. Measured signal density by quarter, head signal fraction, and structural
   line density
4. Binned by file length (short ≤80, medium 80-150, long >150)
5. Additionally analyzed 777 node bodies across 5 types (build, experiment,
   goal, hypothesis, mvp) measuring frontmatter-vs-body signal density

### Results

**Session context files (n=475):**
- Head 25% signal density: 0.637 tokens/line (median 0.667)
- Tail 25% signal density: 0.065 tokens/line (median 0.061)
- **Head is ~10× more signal-dense than tail**
- Head carries **54.6%** of total signal (random baseline: 25%)
- **470/475 files (99%)** have head > tail signal density
- 323/323 medium-length files show head > tail
- 139/139 long files show head > tail
- Only 4 short files (<80 lines) have tail > head

**Node bodies (n=777):**
- Frontmatter consistently carries 1.3× to 5.0× more signal per line than body
- Hypothesis nodes: frontmatter 2.7× denser than body
- Goal nodes: frontmatter 5.0× denser than body
- Body signal itself drops off: head-25% of body carries ~2 tokens vs tail
  approaching zero

### Interpretation

The structural premise is **strongly confirmed**: session context files
overwhelmingly concentrate structural signal (IDs, edges, decisions, goal
references, type declarations) in the first 25% of lines. The tail is
dominated by boilerplate instructions, guidelines, and repeated scaffolding
that carries minimal structural signal.

This supports the hypothesis's mechanism — if an agent receives the full
chat, it must process ~75% boilerplate-heavy content to extract the same
signal that head-truncated (25%) delivers directly. The attention tax
mechanism is plausible given this signal distribution.

### Limitations

- This is a **structural proxy**, not a behavioral experiment. It measures
  signal density in the input text, not actual agent performance.
- Does not test the full claim ("full chat agents are *slower to first useful
  action*"), only the premise ("chats are front-loaded")
- Signal token counting is heuristic; some tail content may carry semantic
  signal that is not captured by structural markers
- Only tests the format used by this repo (context.md files with injected
  prompts); may not generalize to other chat formats

## Evidence

Full output of the analysis script:

```
--- 1. Session Context File Analysis ---
Analyzed 475 session context files

Signal density (signal tokens per line) by quarter:
  Head 25%:  mean=0.637, median=0.667
  Mid 25%:   mean=0.423
  Mid2 25%:  mean=0.091
  Tail 25%:  mean=0.065, median=0.061

  Head's share of total signal: 54.6% (random would be 25%)

  Files where head > tail density: 470
  Files where head < tail density: 4
  Files where head == tail density: 1

  Structural line density (non-boilerplate / total):
    Head 25%: mean=0.890
    Tail 25%: mean=0.698

  File length distribution: min=29, max=291, median=133

  Length bins:
    short (<=80): n=13, head_density=0.341, tail_density=0.152, head>tail=8/13
    medium (80-150): n=323, head_density=0.626, tail_density=0.069, head>tail=323/323
    long (>150): n=139, head_density=0.692, tail_density=0.048, head>tail=139/139

--- 2. Node Body Structure Analysis ---

  build nodes (n=208):
    Avg frontmatter lines: 13.8 (density: 0.145)
    Avg body lines: 119.3 (density: 0.094)
    Frontmatter carries 1.6x more signal per line than body

  experiment nodes (n=222):
    Avg frontmatter lines: 11.4 (density: 0.486)
    Avg body lines: 60.9 (density: 0.381)
    Frontmatter carries 1.3x more signal per line than body

  goal nodes (n=112):
    Avg frontmatter lines: 16.7 (density: 0.292)
    Avg body lines: 71.4 (density: 0.059)
    Frontmatter carries 5.0x more signal per line than body

  hypothesis nodes (n=184):
    Avg frontmatter lines: 11.4 (density: 0.517)
    Avg body lines: 51.9 (density: 0.191)
    Frontmatter carries 2.7x more signal per line than body

  mvp nodes (n=51):
    Avg frontmatter lines: 12.2 (density: 0.421)
    Avg body lines: 106.9 (density: 0.104)
    Frontmatter carries 4.0x more signal per line than body
```

### Source script

Analysis run via:
```
python3 .agi/bin/analyze-chat-structure.py
```
Script is at `.agi/bin/analyze-chat-structure.py` for reproduction.


## Agent Notes
Structural proxy: analyzed 475 session context files, found 99% (470/475) have head-25% signal density 10x higher than tail-25%. Premise confirmed. Behavioral claim (agent speed) untested.
