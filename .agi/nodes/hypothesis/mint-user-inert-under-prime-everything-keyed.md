---
id: hypothesis:mint-user-inert-under-prime-everything-keyed
mint_id: 1a58ce3727084bcfb547b9a1abcc4403
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: belam
model: grok-4.6
role: prime_director
scaffold_hash: 71eafd647842eb4f
season: 2
tags:
  - mint
  - council
  - chew
testable_claim: the mint-user row is inert (no harness) parented by Prime, wrapping a host-only signer outside the tree; mint+parent signatures always; every posts/template/config row is keyed across versions; no second authority daemon
title: mint-user is inert under Prime; everything keyed; Ship of Theseus identity
town: core
---
# hypothesis:mint-user-inert-under-prime-everything-keyed

## Measured
- Owner 2026-10-04 22:2x+22:25 ET: mint-user design, chew only, no implement.
- Owner 2026-10-05 via liaison, answers to Prime Q4–Q7 (verbatim below).
- Practice only: a root-readable key stands in for the owner secure-element key.

## CLAIM
The mint-user is an inert (no harness) post-tree ring member whose parent is Prime; it wraps a host-only signer that stays outside the tree. Mint signature plus parent signature, always. Prime and council may read the stand-in path cell. Every post-config row, in its totality including recursion, is keyed — templates, configs, every version. Ship of Theseus: identity lives on as keys rotate; a new version may update its key; a git commit hash (or an extension of it) is a candidate key. One thin mint-key skill on seatsig + ring; no second authority daemon.

## Dispatch line
config-max: mint-user is a posts.md row (inert, parent=belam) wrapping a host-only signer · template-max: templates for this setup · code: none this round (chew only)

## FALSIFIERS
Chew, not a land. A later round is false if it (1) implements a mint path from this note, (2) stands a harnessed mint-user now, (3) adds a second authority daemon, (4) keys only some rows.

## TESTS
none this round — council chew. Surface questions to the owner via belam (liaison).

## FILE SCOPE
this hypothesis. No engine, no posts.md write, no new unit.

## CEILING
council chew · Prime does not implement · 0 new pieces

## OWNER, 2026-10-05, verbatim via liaison
Q4: the mint-user's parent is Prime.
Q5: inert for now (no harness), optionally a full post later.
Q6: Prime and the council may read the stand-in path cell.
Q7: all parent-signature params travel. Every row in a post config, in its totality including recursion, gets a hash or key of some sort - everything is keyed: every template, every config, etc. Ship of Theseus: identity lives on as all keys rotate through new versions; a new version could update its key automatically. Could even use the git commit hash as the key, or something like it extended as needed. Let the council work it out. Do what feels most optimal. Use your discernment to create the cathedral for your progeny.
