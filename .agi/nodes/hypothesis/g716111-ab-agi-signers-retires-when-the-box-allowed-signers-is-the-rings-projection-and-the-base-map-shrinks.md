---
id: hypothesis:g716111-ab-agi-signers-retires-when-the-box-allowed-signers-is-the-rings-projection-and-the-base-map-shrinks
mint_id: 671142c90a2a4dabb9fbf17d70e8b595
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) after the ring node and the projection exist, a scratch box's allowed_signers file equals the projection of the trunk's ring byte for byte (one sed), written by no root piece reading homes; (b) every post's FIRST ring line is written once by its parent (cases C8 and E7: stand-up), so agi-signers has nothing left to do; (c) AA2.63 reads belam's RULED rail (04:21Z, written once as 'THE 8 KB RAIL, RULED', trunk 5873ba4e2; the owner may overturn it): after the build BOTH tiers hold: (1) the CODE inside config:engine's `~~~` fences <= 8,192 B, extracted `git show REV:.agi/nodes/.geometry/engine.md | awk '/^~~~/{c=!c;next} c' | wc -c` (fence lines excluded; 7,358 B at d6864e8c5) and (2) the WHOLE engine.md <= 12,288 B, `git show REV:.agi/nodes/.geometry/engine.md | wc -c` (9,132 B); section AB's per-line delta is REPORTED (-60 B signers, -119 B agi-signers, +~62 B ckpt = -117 B, then -1 B with revoke and pq at ~58 B each), the seed stays 1,023 B and `agi-gate HEAD` rc 0. The earlier absolute '8,186 B / 7 B spare' was never reproducible and is withdrawn; R6/F32 (`wc -c engine.md` <= 8,192) RETIRE as rails and stay as reported numbers; (d) no node outside the ring carries the box root key as an anchor and AGI_ANCHOR's separate file is gone (the anchor is the owner line of the ring)."
title: "AB: agi-signers (the 1,515 B root piece) retires when the box's allowed_signers is only the projection of the trunk's ring, and the base map keeps config:engine within 8,192 B with agi-gate HEAD rc 0 (AA2.63, AA2.64)"
town: core
---
# hypothesis:g716111-ab-agi-signers-retires-when-the-box-allowed-signers-is-the-rings-projection-and-the-base-map-shrinks

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- AB.5 bytes: 'the base is FULL again' (8,185 B, 7 B spare). AA2.63 originally read -117 B before AB.5 added revoke and pq.
- agi-signers is INSTALLED and stays installed until AA2.64 proves (belam [decision] 03:07Z term 3); its A1 security re-run (env -i PATH) still goes to belam once DG3 refreshes the install doc sha. Retiring it is a root act: its own belam GO.

## CLAIM
(a) after the ring node and the projection exist, a scratch box's allowed_signers file equals the projection of the trunk's ring byte for byte (one sed), written by no root piece reading homes; (b) every post's FIRST ring line is written once by its parent (cases C8 and E7: stand-up), so agi-signers has nothing left to do; (c) config:engine <= 8,192 B and the seed 1,023 B, `agi-gate HEAD` rc 0: the base map lines go -60 B (signers) -119 B (agi-signers) +~62 B (ckpt) +~58 B (revoke) +~58 B (pq) from 8,186, section AB.5 puts the total near 8,185 B with 7 B spare, so the gate is AA2.63 and a build that crosses 8,192 B is REFUSED, not accepted; (d) no node outside the ring carries the box root key as an anchor and AGI_ANCHOR's separate file is gone (the anchor is the owner line of the ring).

## Dispatch line
config-max: the map lines of config:engine (the base) / template-max: none / code: the projection (one sed), the stand-up ring-line write, and the removal of the signers and agi-signers map lines.

## FALSIFIERS
AA2.63: on a scratch tree carrying the integrated build, the fenced-code count is <= 8,192 B AND the whole-file count is <= 12,288 B (the two extractions above, both printed), the per-line delta against the trunk is printed, the seed == 1,023 B and `agi-gate HEAD` rc 0; either tier over its bar is RED. Mutations RED: a build that adds 900 B of fenced code (tier 1), one that adds 3,200 B of prose outside the fences (tier 2).
AA2.64: on a scratch box after agi-signers is removed from the map, allowed_signers == the projection of the trunk's ring (cmp), a post's first ring line written by its parent makes its commits verify, and no file outside the projection is read for trust.
AA2.64b: the one-box agi-fresh.t.sh cases that depend on agi-signers are re-pointed to the ring commit path and pass.

## TESTS
Shell, scratch tree built from the trunk's engine*.md with the candidate edits; throwaway keys; `agi-gate` run on the scratch tree. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
config:engine map lines (engine.md), the projection, the removal of the retired pieces' text from engine-root.md only after belam's GO.

## CEILING
1 parent - kids <= 1 - code inside the fences <= 8,192 B AND whole engine.md <= 12,288 B (AA2.63, the ruled rail; every build reports both numbers and its per-line delta) - the seed 0 B - 1 new test file - 0 USD - regular review + security mur on root code. Depends on: the ring, ckpt, pq and revoke hypotheses. Today's numbers (trunk f02495529): fenced code and whole file are read by the builder with the two extractions before it starts.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- MUTANTS CORRECTED (DG2 measured): a build that adds 900 B of fenced code, or 3,200 B of prose, does NOT go RED over a build that also DROPS agi-signers (7,239 + 900 and 9,013 + 3,200 stay inside the bars); AA2.63 is pinned at the BOUNDARY: fenced exactly 8,192 B = ok, 8,193 B = RED; whole exactly 12,288 B = ok, 12,289 B = RED.
- SEED: the '1,023 B' is NOT reproducible (the doc's seed block measures 985 B), same class as the withdrawn 8,186 B: the seed is a REPORTED number, not a bar, until self-perpetuating names the extraction.
- FALSIFIER FILE: agi-signers-retire.t.sh de-base-dg2-26 1cd53ed94 (e1-e4 rail and gate, p1-p5 projection): 4 ok / 7 FAIL on the trunk (e3 p1 p1b p5 p2b p4 p3). SEAMS: the projection is ONE ExecStartPre=+ line other than agi-signers (honours AGI_SIGNERS, reads git show AGI_TRUNK:ring); cert-authority projects as 'post@agi cert-authority,namespaces="git" type b64', plain lines as 'post@agi namespaces="git" type b64'. AA2.64b (agi-fresh.t.sh re-pointed to the ring commit path) is the builder's, same commit. BUILD ORDER: LAST in the chain; retiring agi-signers on a live box is belam's own GO.
