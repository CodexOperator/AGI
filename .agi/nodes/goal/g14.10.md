---
id: goal:g14.10
mint_id: 2bbe5651385b442293b494fa5c56a249
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G14.10
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 8eb439929c72b23c
season: 2
seeds:
  - doc:lm-research-corpus-registry
  - idea:lm-tiktok-captions-free-label-ruler
status: active
tags:
  - local-maxxing
  - datasets
  - corpus
title: "G14.10: THE RESEARCH CORPUS — datasets/ at the repo root: every eval round triples, every scrubbed parent/kid trajectory, every harvested workflow run, indexed by datasets/README.md = doc:lm-research-corpus-registry; the landing rule and the one scrub (owner 21:4xZ / 21:5xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.10

## Agent Notes
**Owner source (2026-09-20 21:4xZ / 21:5xZ, verbatim on goal:g14):** "are we storing the synthetic datasets we are generating from these evals? They are rpeclassified and can really strengthen our research corpus and ability to use it for model tune ups." — "Put all synthetic datasets into a separate easy to find easy to browse archive with its own explainer doc that you also build into the graph."

**Commits to.** `datasets/` at the repo root is the town's research corpus: every eval round's `(prompt, output, label)` triples, every parent/kid trajectory (scrubbed), every harvested workflow run, indexed by `datasets/README.md`, which is the payload of `doc:lm-research-corpus-registry`. The corpus is the input of G14.7 and the evidence base of G14.11.

**Invariants.** (1) Nothing lands unscrubbed: the span-based redactor is the one scrub; a leak hit blocks the commit. (2) Every record carries its label's provenance (which experiment, which verdict, which reviewer). (3) Trajectories are landed *before* a worktree is removed; raw streaming logs are never landed. (4) The index is updated in the same merge that adds a corpus. (5) Model bytes never live here. (6) A dataset used for training is frozen by sha256 in the trial's node.

**Falsifiers.** (a) A merge that adds a round without its triples or trajectories is a rule violation, counted on this node; three in a row falsify the hand-step design and force the engine-level retention flag (SM item). (b) The corpus is falsified as "preclassified" if a re-scrub or a label audit finds > 1 % of records with a wrong or missing label — then the affected corpus is quarantined (moved under `datasets/quarantine/`) until relabelled.

**Done when.** Never — this is a perpetual hygiene goal; it is reviewed at each G14.11 gap-table update (does every row's evidence resolve into the archive?).

**First chunks (done / minted):** the archive itself (2026-09-20 21:5xZ); `datasets/trajectories/ABC.01/` (landed 22:00Z); DS.01 = the kid-sft re-scrub with the span tool (queued after MP.01). Sub-sub-goals are the director's to mint (G14.10.1 landing, G14.10.2 scrub + audit), same format.

thought-master 02:1xZ 09-21 (owner program, verbatim on goal:g14):
  G14.10.2 THE SESSION-DATA TRUNK + CLASSIFIER PASS (director mints, goal format)
    capture    EVERY role's session data -- pi parents + kids (already land under datasets/trajectories/), AND claude-code roles (masters, directors, the Prime: session jsonl under the harness dir) -> datasets/sessions/<role>/<session>/ through the ONE scrub (datasets/tools/scrub.py); capture hook for claude-code roles = G14.14.8 (engine director)
    labels     pre-label from what the graph already knows per record: model · harness · provider · role · post · town · round id · verdict · mur residue class · spend · wall · box; then a jev in-depth classifier pass over ALL data trunks (kid-sft, jev-typed-acts, trajectories, switch-rule, abl-01, sessions) adding the classes the graph does not carry (act type, reasoning shape prose/diagram-maxed, refusal, tool-error, rebrief) with calibration against a 200-record hand-checked slice
    output     one index (datasets/README.md row + a labels.jsonl per trunk) that G14.7.2's arms read directly
    order      DS.01 first (the one scrub), then G14.10.2 capture, then the jev pass as batched rounds (CPU/API only, no GPU)
