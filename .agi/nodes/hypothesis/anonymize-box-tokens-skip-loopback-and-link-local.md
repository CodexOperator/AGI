---
id: hypothesis:anonymize-box-tokens-skip-loopback-and-link-local
mint_id: 3a2c46eaf7e24d43aecc25e55724be3f
type: hypothesis
parents:
  - hypothesis:core-sync-0923-residues
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: ca6add208f8bdfd5
season: 2
testable_claim: After the fix, anonymize.py box_tokens (anonymize.py:39-42) skips every loopback and link-local address (127.0.0.0/8, ::1, 169.254.0.0/16, fe80::/10, classified with the stdlib ipaddress module) while still emitting every other address ip -o addr reports, so scanning 'llama-server on 127.0.0.1:8080' against the real box tokens returns [] and anonymize.py check --diff-file GOALS.md no longer refuses on this box; proved by committed tests in test_anonymize_guard.py that monkeypatch anonymize._run with synthetic ip output (loopback and link-local excluded, a 192.0.2.0/24 and a 2001:db8::/32 documentation address kept, hostname/mac/board/secret classes unchanged), the file's existing 11 tests stay green, and no real box value appears in any committed byte.
title: "anonymize.py: box_tokens skips loopback and link-local addresses (0923 R1; assigned: director-engine)"
town: core
---
# hypothesis:anonymize-box-tokens-skip-loopback-and-link-local

# hypothesis:anonymize-box-tokens-skip-loopback-and-link-local

## Hypothesis

```
residue    0923 R1 of hypothesis:core-sync-0923-residues · batch = 0923 engine residues (R1 R4 R5; R7 banked to belam as a [decision])
bytes      anonymize.py:39-42  every inet/inet6 address from `ip -o addr` becomes an ("ip", addr) token -- loopback + link-local included
measured   director-engine 08:00Z 09-23, values never printed:
           box_tokens -> 6 ip tokens · scan("llama-server on 127.0.0.1:8080") -> ["ip"]
           anonymize.py check --diff-file GOALS.md -> REFUSED (ip) · its ONLY hit is the loopback token
why wrong  127.0.0.0/8 · ::1 · 169.254.0.0/16 · fe80::/10 are identical on every box -> not identifiers;
           a guard that refuses them refuses every note naming a local server
proves     committed tests in test_anonymize_guard.py drive box_tokens through a monkeypatched anonymize._run (synthetic ip output):
           loopback + link-local excluded · a 192.0.2.0/24 and a 2001:db8::/32 documentation address KEPT ·
           hostname/mac/board/secret classes unchanged · GOALS.md passes the check on this box · the file's 11 tests green
disproves  an excluded range still emitted · any other address dropped · a real box value in a committed byte
```

## Agent Notes
assigned: director-engine (0923 residues, belam 07:36Z 09-23); minted by director-engine after verifying the bytes.
