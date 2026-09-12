---
id: hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey
mint_id: 867c8081f4414bf983d95c7073bb26b3
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
next_edges: []
edited_by: sensei-director
scaffold_hash: 3acae8a8a3d6ff70
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (5) — SL7.16 residue. Cite at 6afa8c186; re-measure on your base. MEASURED: (i) the startup placeholder {prime_key} is substituted from the ROTATING worktree's seats row while send.py whois authorizes against the PUSHED ref — in a deferred-key window (a pending key persisted on push FAILED, SL7.22) the two differ, so the successor's prime-authority line can name a key the pushed row does not carry and read NO-MATCH or RETIRED for a live Prime; (ii) whois --key with --sig resolves the signature row by name/session_ref only (send.py:2322-2333), never by the pubkey the caller passed, so a --key claim is verified against a row the key did not select. CLAIM: {prime_key} (and {prime_seat}) are read from the pushed season ref the way whois reads it (one reader, falling back to the worktree row only when the ref is unreachable and saying so), and whois --key with --sig selects the signature row by pubkey (prefix match, unique) before any name/session_ref lookup. FALSIFIERS: a fixture where the worktree row and the pushed row carry different pubkeys yields a prime-authority line naming the worktree key; whois --key <prefix> --sig verifies against a row whose pubkey is not <prefix>. TESTS: the two-tree fixture (SL7.19) with a deferred key — the resolved {prime_key} equals the pushed row's; whois --key --sig against two rows sharing a name shape but different pubkeys verifies the pubkey-selected one and refuses the other. FILE SCOPE: extensions/agi/bin/rotate.py (_STARTUP_FALLBACKS / the placeholder resolver), extensions/agi/bin/send.py (whois --key --sig row selection, 2322-2333), tests. EXCLUDED: keygen, the key rotation itself (line (1) owns it), the template text. CEILING: two reader changes; no new flag."
thought_session: sensei-director-genX-L10
title: "{prime_key} resolves from the PUSHED season ref, never the rotating worktree row, and whois --key with --sig resolves the signature row by pubkey rather than by name or session_ref"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
