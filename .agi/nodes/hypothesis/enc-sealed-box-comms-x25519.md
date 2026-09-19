---
id: hypothesis:enc-sealed-box-comms-x25519
mint_id: 6609749e76444d58b3476b6856fec8fc
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: grok-bot-executor
season: 2
town: encryption
title: "Sealed-box town comms via X25519 from post keys — chain-first under g15.25"
testable_claim: "On encryption-town/season2/main, sealed-box town comms can be grown chain-first: idea→hypothesis→experiment under goal:g15.25 without orphan builds. CLAIM: (1) each live keyed post yields an X25519 conversion from its ed25519 key (libsodium crypto_sign_ed25519_pk_to_curve25519 / pynacl equivalent) documented in an experiment that asserts round-trip seal/open for a tmp pair; (2) message records gain an optional sealed-box ciphertext path selected by enc_scheme != none without breaking plaintext-and-signed default; (3) suite stays green with enc_scheme=none (no forced encryption). FALSIFIER: any path that writes ciphertext when enc_scheme is none, or that lands a build: node without a parent hypothesis/experiment edge under g15.25. SCOPE: graph scaffolding + director-owned experiments via pi parents; no full custodian/MPC yet."
falsifier: "ciphertext when enc_scheme=none; or build without hyp/experiment parents under g15.25"
scaffold_hash: 5f29ef2feaa4b2bc
---
<!-- BODY:BEGIN -->
# hypothesis:enc-sealed-box-comms-x25519

## Chain position
idea (redesign Addendum 3 / third-eye encryption) → **this hypothesis** → experiment (director-enc-sealed-box + pi) → verdict → mvp → build.

## Director
`director-enc-sealed-box` (grok-fast). Brief: `doc:director-brief-enc-sealed-box`.
