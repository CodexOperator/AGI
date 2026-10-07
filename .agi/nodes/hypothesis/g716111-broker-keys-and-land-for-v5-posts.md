---
id: hypothesis:g716111-broker-keys-and-land-for-v5-posts
mint_id: 6c83505b01dd4adfa0415843e78574ea
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: f3b96e397a0ad78e
season: 2
testable_claim: one root broker unit, defined in one geometry section, mints a capped per-spawn key for a request signed by a post row key and fast-forwards the trunk for a master-signed ff-only request, never revealing the provisioning key and running no model
title: "ONE root broker for v5 posts: capped per-spawn keys + ff-only master lands, signed by row keys, no model in the loop"
town: core
---
# hypothesis:g716111-broker-keys-and-land-for-v5-posts

## Measured
- MAIN .env is mode 600 owner belam: a v5 post uid cannot read OPENROUTER_PROVISIONING_KEY, so provisioning.available() (extensions/agi/bin/provisioning.py:170) is false for every v5 director -> no per-spawn key -> no dispatch from v5 (belam card row 98; parity BLOCKER row 30). Today DG3 (old setup) is the ONLY dispatcher.
- v5 masters cannot write MAIN (and v5 uids cannot git push: goal:g7.33.19 row 93) -> sanctuary-master stays on the old setup (its MOVE verdict NO: "v5 cannot land on MAIN").
- The pieces already exist: provisioning.mint() (provisioning.py:888; caps + the min_account_remaining_usd floor, :554) · each post's ed25519 pubkey on its config:posts row (19 rows carry one) · send.py whois (:5308) verifies a session against the PUSHED rows · seatsig rings (extensions/agi/src/seatsig/rings.py: verify_decision :231, verify_ring :607) = the ring shape for member 1 now, the owner's secure key as member 2 later · the master's land is already ff-only (skill agi-master-gate: commit-tree, then git merge --ff-only).
- Owner 22:5xZ 10-01 (verbatim in THOUGHT): compact, under budget, nothing model-manual that could be automated; a broker key ring, for now one key stored on root on the box; land: reuse the existing setup, stream what a post needs on its first turn through the matrix base layer.
## CLAIM
ONE root broker unit (its text and script = ONE geometry section each, F4) serves v5 posts with NO model in the loop: (a) KEYS -- for a request signed by a post's own config:posts ed25519 key (verified against the pushed rows, as whois does) it mints ONE capped per-spawn key through provisioning.mint (same caps, same floor) using the root-held provisioning key (root 600, ring member 1), and hands back only that capped key -- never the provisioning key; (b) LAND -- for a request signed by a MASTER row it fast-forwards MAIN's trunk to the named commit only if the signature verifies, the update is ff-only and the commit is reachable from the request; it runs no review and makes no merge (the master already gated it).
## Dispatch line
config-max: the broker's paths, socket/spool dir, allowed request kinds and which roles may LAND = cells (.agi/config.json or the engine geometry), never literals / template-max: the request format + the refusal lines = one section text / code: the verify + mint + ff-only resolver that does not exist yet -- REUSE provisioning.mint, the seatsig verify, the row pubkeys; invent no new key format, no new layer (first-turn streaming = the existing agi-project projection). The kid answers this line FIRST: which existing function does each of sign/verify/mint/ff, where each cell lives, and how a request reaches root without a model (a spool dir + a path unit, or a socket unit -- pick the smaller).
## FALSIFIERS
- the broker ever writes the provisioning key (or any long-lived key) into a reply, a log, a node or a post's home
- a request with a bad / absent / non-row signature, or from a non-master row for LAND, gets a key or a trunk update
- LAND moves the trunk on a non-ff update, or to a commit the request does not name
- a minted key exceeds provisioning.mint's caps or ignores the floor
- the unit or script text lives anywhere but its one geometry section (a second copy)
- a model call anywhere in the request path
## TESTS
fixture-only: fake provisioning (no network, no real key), a tmp git repo for LAND, ed25519 test keys generated in the test; rows: signed KEY request -> one capped key returned, provisioning key never in output; unsigned / wrong-key / unknown-row -> refused by name; LAND by a master -> ff; LAND by a director -> refused; non-ff -> refused; unreachable commit -> refused; the section extracted and run under sh/python with fakes on PATH (as test_agi_boot.py does). No real key, no real systemd, no network in CI.
## FILE SCOPE
.agi/nodes/.geometry/engine-root.md (the broker unit + script sections) · the cells (.agi/config.json or the geometry) · one test file · this node (director). provisioning.py / send.py / seatsig only if a one-line seam is needed (named in the dispatch answer).
## CEILING
Sonnet 5.5 kids (parent/kid via dispatch.py, or Sonnet 5.5 subagents per the owner's lane) · <= 60 production lines in the sections + cells · tests <= 200 · 0 USD build · GATING mur on claude-code (ccrun.py) · INSTALL (sudo, /etc, the root key file) = a SEPARATE belam GO.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
FIRST VERSION (belam 22:5xZ 10-01, parity BLOCKER row 30; the owner lifts the 21:3xZ 09-30 key-machinery HOLD for this round). OWNER 22:5xZ (on the key broker), verbatim: "Key broker for what new posts? Sure if we can keep it compact and under budget. I’d prefer to not have anything be model manual that could be automated. We could have a broker key ring that also uses my secure key later for now just a key stored on root on box." OWNER 22:5xZ (on the land broker), verbatim: "For graph slicing or system resources? Either way yes we can implement it if our current guards aren’t enough but ideally we can use existing setup to stream in needed stuff on demand on first turn using the matrix base layer system." WHY this shape: v5 uids cannot read .env (600, belam), so no v5 director can mint per-spawn keys and none can dispatch; v5 masters cannot write MAIN, so SM stays on the old setup. One broker covers both, with NO model in the loop, reusing provisioning.mint, the row ed25519 keys + seatsig verify, and the master gate ff-only land; first-turn streaming = the existing agi-project projection, no new layer. Install = a separate belam GO.
<!-- THOUGHT:END -->
