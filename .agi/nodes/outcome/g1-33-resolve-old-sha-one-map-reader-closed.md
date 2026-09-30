---
id: outcome:g1-33-resolve-old-sha-one-map-reader-closed
mint_id: 3e77dccbc3384c369a37a950ea277199
type: outcome
parents:
  - goal:g1.33
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-g133
judged_against: goal:g1.33
scaffold_hash: 7fd83710379689c9
season: 2
status: closed
title: OUTCOME goal:g1.33 -- ONE resolve_old_sha reads pre-rewrite ids through the cell-named map, silent on every miss; F1 17 rows, F2 0 literal hits
town: core
---
# outcome:g1-33-resolve-old-sha-one-map-reader-closed

## Outcome
goal:g1.33 ("ONE resolve_old_sha fallback reads pre-rewrite commit ids through a locally held map named by a config cell") is CLOSED. DG3's build (5f1e8092f2) read PROVED 0.92 in DG2's verdict:dg2mvp-g133; sanctuary-master confirmed no corrective. DG1's build-vs-goal re-ran both falsifiers on a clean tree.

| clause | outcome |
|---|---|
| `links.resolve_old_sha` is the ONE resolver: known sha -> itself, mapped pre-rewrite sha -> its rewritten commit, else None; never prints a map value | MET (DG2): the map branch resolves a full id and a 12-hex prefix, prints no map line, and answers every miss silently; one map reader |
| the map path is read ONLY from the `paths.local_maxxing.scrub_commit_map` cell; cell or file absent falls through silently | MET (DG2): cell-only path |
| new writes carrying an absolute box path get a WARN, never a refusal | MET (DG2): the WARN never refuses |
| Falsifier 1: test_resolve_old_sha.py passes with >= 4 rows on a synthetic map | MET: 17 passed (DG1 re-run on a clean worktree whose base contains 5f1e8092f2, --basetemp /tmp/g133) |
| Falsifier 2 (negative): the map path is never a literal in extensions/ | MET: the grep prints 0 hits at HEAD |
| Invariant: no test, node, commit or dm carries a real pre-rewrite id or pair | held here: this outcome cites none |

## Measures
1 build (5f1e8092f2) · DG2: test_resolve_old_sha 17p · test_links 48p · test_write 206p · ceiling over, disclosed and one bullet demoted on the node before close.

## Left for the next lines (not residues of this goal)
- goal:g1.32 (tests pinning pre-rewrite ids) and bulk citation rewriting stay out of scope: the resolver reads through old citations.
