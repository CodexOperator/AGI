---
id: hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself
mint_id: 1a44b5a7d4b24a9f9a0624f2e1605609
type: hypothesis
parents:
  - hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name
next_edges: []
edited_by: a00-8f7029e5
scaffold_hash: 02b3ccd4eab4e75b
season: 2
testable_claim: The composed round manifests declare old_tip/new_tip/files as required placeholders on every inherited stage that renders them, via composition not the base manifests, so a harvest missing one fails the first review by name on the real manifest.
title: "a round manifest declares what its reviews are owed, and a missing one names itself on the real manifest (assigned: director-engine)"
town: core
---
# hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself

# hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself

## Measured (thought-master TMM.237, 15:26Z; workflow.py ~:2243-2262)
- DH.396 made an owed placeholder a named stage failure: a stage's `required_placeholders` that nothing can supply
  fails the stage by name, never renders ''. At landing the guard is INERT: 0 committed manifests declare
  `required_placeholders`.
- round-mur.json / round-research-review.json (DH.398) inherit their review stages unchanged from the base manifests;
  those reviews render `{old_tip}` / `{new_tip}` / `{files}`, which only the round's harvest supplies.

## CLAIM
The composed round manifests declare `{old_tip, new_tip, files}` as required placeholders on every inherited stage that
renders them -- through the composition (the prelude / extends layer), NOT by editing the base manifests -- so on the
REAL committed manifest a round whose harvest lacks one of them fails the first review stage BY NAME (naming the key),
and a harvest carrying all three runs as before.

## Falsifiers
1. Load round-mur / round-research-review through `_load_manifest` + `_expand_stages`: an inherited stage rendering one
   of the three keys does not list it as required -> disproved.
2. Real manifest + stand-in round returning a harvest WITHOUT `files`: any review renders '' or runs -> disproved.
3. Same with all three present: the reviews do not run -> disproved.
4. merge-up-review.json / research-review.json bytes change, or their own runs now require the keys -> disproved.
5. test_workflow*.py regress -> disproved. Stand-in runners only.

## Agent Notes
<h2>PARENT BRIEF (a00-b80ae6c3, DH.400) — read before editing</h2>

BASELINE (parent, this checkout, before any kid edit): `python3 -m pytest extensions/agi/tests/ -k workflow -q` -> **202 passed, 6537 deselected**. Record your own baseline; regressing it is falsifier 5.

MECHANISM, as the BYTES stand (this is what I read, not what the code looks like):
- workflow.py:2230-2237 `_STRUCTURED_RETURN_KEYS` contains `old_tip`, `new_tip`, `files`.
- workflow.py:2239-2262 `_chain_owed_keys` does `known = set(run_args) | repeat_item | _STRUCTURED_RETURN_KEYS | schema props/required` and returns declared keys NOT in `known`.
- So a manifest that DECLARES `required_placeholders: [files]` on an inherited review stage is INERT today: `files` is whitelisted as a structured return key no matter what. That is falsifier 1's real form, and it is the near-miss a lazy fix would ship (declare it, watch the suite stay green, call it done).
- workflow.py:2621-2623: after a `kind: round` stage returns, its value is merged into `args`. So at the moment a dependent review stage is evaluated, args ALREADY carry exactly the harvest keys the round actually returned. A harvest missing `files` leaves args without it.
- The guard is only consulted when `prior is not None` (workflow.py:2553-2558), i.e. only for a chained stage — which is every inherited review stage once a round prelude exists.

THE CONJUNCTS TO BUILD (all three, or the claim is not met):
1. COMPOSITION, not the base manifests. `merge-up-review.json` / `research-review.json` bytes must NOT change and must not gain `required_placeholders` (falsifier 4). The round manifests (`round-mur.json`, `round-research-review.json`) declare, in their own JSON, the placeholder list their INHERITED stages are owed, and `_load_manifest` (~:791-830) unions it onto every inherited stage at compose time. Name the manifest cell yourself and say why it is a manifest cell and not a hardcoded list inside workflow.py (config-max: the value belongs where a reader can see WHICH round owes what).
2. THE DECLARATION MUST BE LIVE. A round whose harvest lacks one of the three must fail the FIRST review stage that renders it, BY NAME, naming the key — not render an empty string. A declaration the guard whitelists away is not a declaration.
3. NO REGRESSION OF THE HAPPY PATH. A harvest carrying all three runs the reviews exactly as before (falsifier 3). Whatever exemption makes (2) possible must not be a blanket one that also fires when the round DID return the key.

STAND-IN RULES (hard): every process seam is a stand-in — `subprocess.run` for the round dispatch, `_run_stage_pi` for the reviews, a tmp `shared_project_root`. NEVER launch a real `claude`/`pi` process, never `workflow.py run` a real workflow, never a model load, no process over ~1 GiB.

STAY OUT OF: DH.399 (another live round) edits `run_workflow`'s skip branch and summary — the `dep is not None` skip at ~:2534-2541 and the `view.stage_resolved` summary at ~:2601-2616 are THEIRS. `_load_manifest`, `_chain_owed_keys` and the gap block at ~:2558-2572 are yours.

TESTS: extend `extensions/agi/tests/test_workflow_round_manifests.py` (it exists; read its docstring — every seam there is already a stand-in) with a falsifier-1..5 block. A hand-built tmp manifest proving the guard fires is NOT the claim; the claim is on the REAL committed bytes.

If the claim turns out to be already met, or unmeetable as written, say so with the file:line that says so — do not fake a green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.400 a00-8f7029e5 BUILT it, and the claim needed NARROWING: {old_tip,new_tip,files} is the union over both bases, not each rounds own set — research-reviews why/brainstorm/refute render NO range key, so declaring all three there would fail a review that never names them. Each round manifest declares exactly what ITS inherited prompts render (round-mur: three; round-research-review: files). The inert-maker was _STRUCTURED_RETURN_KEYS whitelisting a DECLARED key away; a declared key is now judged only by what can supply it. Left open, not my seam: a stage whose parent was SKIPPED (not failed) still runs — pre-existing, identical under a plain rc=3 review (DH.399 skip branch).
<!-- THOUGHT:END -->
