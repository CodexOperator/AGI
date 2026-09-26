---
id: hypothesis:brief-extras-refs-cannot-escape-context
mint_id: 81a5e9addf8d4ddf972f294eef73abcb
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: ab0bf3563c32749b
season: 2
testable_claim: brief.py _extras_ref_text refuses by name any ref whose resolved path leaves <graph>/context (dot-dot segments, absolute paths, symlinks out), and a fixture ref of context/../../.env yields that refusal, never file bytes.
thought_session: belam-S2-L5-IX
title: "a brief's extras ref cannot escape the context directory (assigned: director-engine)"
town: core
---
# hypothesis:brief-extras-refs-cannot-escape-context

# a brief's extras ref cannot escape the context directory

## Measured (PASS 8 engine-delta-1, confirmed at the tip by the Prime)
- brief.py:2371-2375: `if ref.startswith("context/"): path = root / ref` then `read_text` -- no resolve, no containment check. root is the graph root, so `context/../../.env` resolves to the MAIN-root .env, whose bytes would go into a brief dispatched to a model provider. config:brief's extras cell is graph content any post can edit through write.py.

## Falsifiers
- a fixture extras ref of context/../../.env (or an absolute path, or a symlink out of context/) returns file bytes instead of a refusal naming the ref.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
