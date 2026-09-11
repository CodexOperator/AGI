---
id: hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built
mint_id: 6175f52c0a8f492882a753b90072d333
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged
next_edges: []
edited_by: sensei-director
scaffold_hash: 772941ab89b01524
season: 2
testable_claim: "goal:g15.25 rung 1-4 constraint from the OWNER 22:1xZ (verbatim in doc:l4-owner-decisions:657-658, relayed by Prime XII 22:14Z): comms stay PLAINTEXT-AND-SIGNED by default, and a 'lockdown' BOOLEAN config must be able to flip comms to encrypted-at-rest LATER (next season, rungs 5-8; Vultisig, the open-source MPC wallet, is the owner's reference for the custodian design) with warnings printed and an optional 'run your own custodian signing server' requirement — RESERVE the flag + the seam NOW, build nothing of lockdown itself. MEASURED at 7090046f7: extensions/agi/bin/send.py reads NO config today (grep 'config.json' hits only _graph_root 212-219); the enc seam exists from SL4.06 (src/seatsig/__init__.py: Scheme.enc_scheme/encrypt/decrypt all None, DEFAULT_SCHEME; every send carries an env v1 line). CLAIM: (1) ONE config block `comms` in .agi/config.json (the project's loop-tuning file, beside agent_dispatch/harnesses) read by ONE helper `_comms_config(root)` in send.py that returns a dict with defaults for EVERY key it knows (absent block = all defaults, never raises) — keys reserved now: `lockdown: false` (this round) and `verify: \"informational\"` (read here, ACTED ON by the goal:g15.26 flip round, never by this one — this round only returns it); (2) `lockdown: true` changes NO bytes on the wire and encrypts NOTHING — every `send` and every `read`/`peek` under lockdown:true prints exactly one WARNING line to stderr: `WARNING: comms.lockdown is set but lockdown is NOT BUILT (next season, rungs 5-8): messages stay plaintext-and-signed; no custodian signing server is required yet` — and the env line gains nothing that claims encryption (enc_scheme stays none); (3) the seam is NAMED, not built: the ONE place a future cipher plugs in is documented on the Scheme (enc_scheme/encrypt/decrypt, already there) plus ONE stub `_lockdown_requirements(cfg)` in send.py returning the list of what lockdown WILL require (`encrypted-at-rest`, `custodian-signing-server: optional`) used only by the warning text and a test — no key exchange, no cipher, no envelope change; (4) `send.py -h` / the keygen help mention nothing new except that comms.lockdown is reserved. FALSIFIERS: with lockdown:true a sent message's inbox bytes are byte-identical to the same send with lockdown:false except the ts/sig (assert on a tmp root); the warning line appears exactly once per send and once per read under lockdown:true and never under false/absent; an absent comms block yields the defaults and no warning; any string 'encrypted' printed as a STATE (not inside the warning) fails the test. TESTS: test_send.py + test_seatsig.py + test_sensei.py + test_heal.py + test_bin_help_smoke.py, with neighbours. RULES: merge, never rebase; the kid's experiment-node prose never quotes the literal THOUGHT marker; no new bin/ file — the helper lives in send.py; do NOT touch keygen/_cli_keygen/_parse_block/_canonical_msg/_verify_block (SL5.02 a00-821727e6 is live on those seams — disjoint by design). FILE SCOPE: send.py (_comms_config, the warning at send/read/peek, _lockdown_requirements), .agi/config.json (the reserved block, both keys at their defaults), tests. EXCLUDED: any cipher, any envelope change, rotate.py, write.py, config:* nodes, the label/refusal logic (g15.26). CEILING: 1 parent, 1 kid, small."
thought_session: sensei-director-genV-L5
title: "comms.lockdown is a reserved boolean read by one send.py helper: false by default, true prints one warning per send/read and encrypts nothing until lockdown is built next season"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
