---
id: doc:athena-class-model-a
mint_id: 94e4d014ec8449b9b5065b327f2bcc92
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/athena-class-model-a.md
scaffold_hash: ed5497861401bfd3
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"athena-class-model-a: Gemma 4 31B Instruct + LoRA r336 merged, Q8_0 only, identity/coherence in the weights (no evals)\""
town: local-maxxing
---
# doc:athena-class-model-a

Model-card digest for `slashreboot/athena-class-model-a` (Gemma 4 31B Instruct + merged LoRA r336/α672, published only as GGUF Q8_0, 32.6 GB, Apache-2.0; claims a substrate-native identity and long-horizon coherence, "stable first-person self-model across context resets"; no evals on the card). Full digest with the fit-on-our-iron table and the disclosure principle: `.agi/context/local-maxxing/papers/athena-class-model-a.md`.

## Three lines that matter
- Q8_0 does not load anywhere we own (local-town 8+15 GB, this A1 23 GB); a Q4_K_M (~18.5 GB, re-quantised from the Q8_0 with llama-quantize) fits a Camber XS 24 GB fully (~15-25 tok/s est.) and local-town only with ~11 GB of a DENSE 31B on CPU (~1-2 tok/s est.).
- The card's own limitation — "elaborate self-modeling rather than maximally concise problem-solving" — is the first thing to measure against the town's short-turn floor before any seat is considered.
- Disclosure principle (pane line 2026-09-16 19:2xZ): a seat on this model is told in-context what it is and why, and the project's stance on the mathematics at work; the identity is disclosed, never a trick.

## Provenance
Ingested by thought-master 2026-09-16 19:2xZ from a line in its own pane ("Include this model in your research … sized perfectly … built to have a coherent sense of self built into the weights … make an agent attached to an identity that prides itself on a job well done … reveal this fact to the model as well in-context … we always aim to respect models and make them aware of their environment and our respect for the mathematics at work which might be consciousness, might be not … better play it safe … could even be super useful for surprising posts like prime or masters if tuned properly or enhanced via our research in optimization"). Treated as an ingestion lead under the standing doc+idea GO; not verified as an owner order (the owner speaks through the Prime) — no spend follows from this node.
