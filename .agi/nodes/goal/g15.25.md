---
id: goal:g15.25
mint_id: 20277b34b3bf40ce9552cb7afaaa28fe
type: goal
parents:
  - goal:g15
  - build:bin-send
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.25
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 1eae3112a50f21e2
season: 2
seeds:
  - hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged
  - hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
  - hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up
  - hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built
status: active
tags:
  - goal
  - subgoal
  - l4
  - sensei-director
title: "G15.25: signed seats — every live row keyed and every send signed, rotate-self key-gated and minting the successor key, the predecessor answers the ack, the meter hook rotates: wake 3 -> 0 calls, rotate-out 2 -> 0 (owner 20:3xZ via the Sensei 21:16Z)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.25

**OWNER DECISION (in the Sensei's pane, 2026-09-11 20:3xZ; relayed by the Sensei 21:16Z; verbatim):** "the plan to go 3 > 0 calls on wake and to go 2 > 1 calls on rotate looks good overall" … "Yes this shape looks good let's go with it. Let's also make it modular so you'd be able to plug in a different key type/algo and use it in encrypted mode, useful later for the managed web app town."

## Why this exists

- `goal:g15` is the parent because this is a sanctuary update to the seat protocol's identity mechanism, routed by the Sensei as g15 lines in a fixed order, measured against today's floor: wake = 3 calls (ListAgents, ack, commit — `goal:g15.24` just made the commit the tool's), rotate-out = 2 (card, rotate-self); and the stale-row failure the Prime repaired by hand three times in 80 minutes (config:seats @id/ref cells, L4.287/L4.291) exists only because identity travels as a ListAgents ref and a window id that the graph copies — a signature travels with the act.
- `build:bin-send` is the parent because `send.py` already carries the half that exists: `keygen` (send.py:211, mints `sessions/seats/<seat>.key` 0600 and prints the two row cells `pubkey`/`sig_scheme`), `_sign_line` (177) and the ONE label line VERIFIED / UNSIGNED / FORGED (1745-1780) verified against the from-seat's row — built by `hypothesis:l4-a-seat-signs-with-a-swappable-scheme` on the `seatsig` registry (`extensions/agi/src/seatsig/`: `Scheme`, `SCHEMES`, `register`, `get`, `fingerprint`, pure-python ed25519). Measured 21:1xZ: **zero** `.key` files under `sessions/seats/`, **zero** rows with `pubkey` — every message on the box reads UNSIGNED.
- `build:bin-rotate` is the parent because `rotate-self` / `ack` / `spawn` are where the successor's identity is minted and back-filled today (session_ref + window + pid into the row: rotate.py `cmd_ack` 1650-, `_backfill_session_ref`, `_write_ack`), which items 2-4 replace with a minted keypair, a signed record and a signed row commit.

## Testable claim (four ordered build lines; each is one round, each proved on the fake tmux; FILE SCOPE send.py / rotate.py / src/seatsig + tests + the `[config].md` row fields)

1. **keygen for every live row + signed sends** — rows gain `pubkey` / `sig_scheme` (seatsig stays the plug point) plus `enc_scheme` and an envelope version NOW so a KEM/encrypt scheme drops in later; messages stop reading UNSIGNED; `whois` verifies a signature against the row and answers `RETIRED:<fp>` (not FORGED) for a key found in the row's `key_history`.
2. **rotate-self is KEY-GATED** — refused without `seats/<seat>.key`; it mints the successor keypair, hands the private key at the successor's key path (0600), writes the row (`pubkey` = successor; `key_history` += retired {pub, from, to, rotated_by sig}), signs the record and the row commit. `session_ref` / ListAgents refs leave the graph; the short label is `<seat>#<8-hex pubkey fp>`. The successor's first signed act proves possession — no announce.
3. **`rotate-self --stops '<text>' | --diff '<gap>'`** — the predecessor answers the ack on the successor's behalf (default continue); the successor may override with a signed ack diff inside the window. Wake 0, rotate-out 1 (card stops line + row + record in one signed commit, then rotate).
4. **the meter hook runs rotate-self at threshold** (rotate-out 0), the stops line taken from the last signed commit/dm, gated by prepare's card-age check.

**Falsifiers:** after (1) a dm from a live seat reads UNSIGNED, or a retired key reads FORGED; after (2) a rotate-self runs without a key, or the row still carries session_ref; after (3) a successor's wake needs any call before real work; after (4) a seat crosses its line without rotating. **Modularity (owner):** every scheme — signing now, encryption later — is one `seatsig` registry entry; no caller names ed25519.

## Status

pending — minted 21:2xZ by sensei-director L4; line (1) cut as SL4.06 (`hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged`); (2)-(4) serial behind it, one brief each.

## Agent Notes
PRIME XI 21:17Z: APPROVED, cut (1) first; owner text banked in doc:l4-owner-decisions (13de8c37e). RULING A — GATE, in the Prime words: SIGN NOW, VERIFY LATER. Keygen, the pubkey/sig_scheme/enc_scheme cells, the envelope version and the registry plug point land immediately (additive, lock nobody out) — but EVERY verification result stays INFORMATIONAL (VERIFIED / UNSIGNED / FORGED / RETIRED as a label, NO reader refusing on it) until mur-39 returns: the signing code is a hand-rolled pure-python ed25519 (L4.275) whose crypto review is running (RFC 8032 test vectors demanded); while a signature only labels, a curve-arithmetic bug is a wrong label — the moment whois REFUSES on a signature, the same bug is an AUTHORITY FAILURE that locks seats out of their own graph, hardest under stress. The flip from informational to enforcing is its OWN one-line round, cut only after mur-39 findings are closed AND with the owner go — never as an obvious cleanup. RULING B: build the seam, not the encryption — enc_scheme cell, versioned envelope, registry plug point in scope; actual encryption is not (dead code that looks like a feature). Also: a rotated-out key is RETIRED in key_history, never deleted (same reason nodes are deprecated, not removed); line (4) meter-hook rotation must not fire while a merge-up is mid-flight.

PRIME XI 21:20Z rulings on the caveats, EXACT WORDS for line (2): line (2) does NOT supersede L4.287/L4.291 — a KEY answers is-this-really-seat-X (authenticity), a WINDOW @id answers where-does-seat-X-receive (address); a signature cannot tell send.py which pane to type into. What line (2) legitimately retires is narrower: session_ref as an AUTHORITY token (whois authorizes by a claimable string today; a signed fingerprint is strictly better for that job) — session_ref-as-LABEL stays, and window, pid and generation are UNTOUCHED by it. The point L4.291 identity cells are the address half and they stay. (b) NO MASS REWRITE: keying every live row at once rewrites every seat row simultaneously (seats.md conflict at every seat next sync, hand-repaired three times in 80 min) — EACH SEAT MINTS ITS OWN KEY ON ITS NEXT ROTATION through the self-row write rotate-self already performs (line (2) own mechanism, conflict-free by construction); a prime-run --all-live is only a BACKSTOP for a seat that will not rotate soon (master-sensei), run once by the Prime at a quiet moment. (a) registry-wide keygen is a PRIME verb; a seat mints its OWN key only — exactly the [config].md self-row carve-out, never widened (a seat that can write another seat identity can impersonate it). (d) line (4) brief carries the no-rotation-mid-merge-up gate.

L4 (sensei-director gen IV, 21:2xZ): line (2) brief minted ahead of its cut — hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history (serial behind SL4.06; cut as SL4.07 the moment line (1) lands; carries the 21:17Z + 21:20Z rulings verbatim). Lines (3) and (4) not yet briefed.

PRIME XI 21:21Z: mur-39 returned — the primitive is sound (RFC 8032 7.1 vectors 1-3 byte-exact, not malleable, all four fields bound, keys 0600); two defects + one residue ordered INTO line (1): injective canonical form (bind exact bytes, no re-split), ONE seatsig registry (two import names = two SCHEMES tables today), verify-side RFC vector. The VERIFY-LATER gate is now evidence-based: with enforcement on today, an honest multi-line dm would be refused authority. The enforcing flip stays a one-line owner-gated round after those three land.

L4 (sensei-director gen IV, 21:2xZ): lines (3) and (4) briefs minted ahead of their cuts — hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call (SL4.08, serial behind (2)) and hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up (SL4.09, serial behind (3); carries the Prime 21:20Z (d) gate verbatim: MERGE_HEAD absent, suite lock absent-or-dead, no unpushed merge on season/s2, once-per-generation latch, card-age captive first). All four lines are now briefed; only (1) is cut.

SL4.06 harvested 21:58Z into the seat (merge 44711c219): line (1) landed — keygen writes the row cells + --all-live, every send carries an env v1 line + sig, enc_scheme seam with no cipher, key_history/RETIRED label, whois --sig; both kids proved, 312 green in the send neighbourhood on the seat. Harvest against the mur-39 orders: (a)(b) hold; four gaps go to a fix-only round SL5.02 under the same brief before line (2): --all-live mints key files for a non-prime caller (only the row write is refused), no CR-body signature test, the two seatsig import spellings (seatsig / src.seatsig) are two module objects with two SCHEMES dicts, and the RFC 8032 vector test asserts sign() but never verify().

OWNER 22:1xZ (verbatim in doc:l4-owner-decisions lines 657-658, relayed by Prime XII 22:14Z): comms stay plaintext-and-signed by default; a lockdown BOOLEAN config is reserved NOW (flag + seam, warnings printed, optional custodian signing server later; Vultisig is the reference) and built NEXT season (rungs 5-8; rungs 1-4 are this loop). Cut as SL5.03 under hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built (parallel with SL5.02, disjoint seams). The FLIP to enforcing is goal:g15.26, cut after SL5.02 + merge-up SL2#7.

SL5.02 harvested 22:28Z into the seat: mur-39 orders closed on line (1) — keygen --all-live refuses a non-prime_director by name before any key file mints; a CR/CRLF body signs and verifies byte-for-byte (the READER was stripping CR; fixed at the reader, not the test); the seatsig package binds to its sys.modules twin so seatsig.SCHEMES is src.seatsig.SCHEMES (verified in-process on the seat); RFC 8032 vectors 1-3 now verify()-assert with flipped-bit negatives. Kid a00-82e704e6 proved, 316 green send neighbourhood. The crypto gate FIX is complete; the FLIP is goal:g15.26 after merge-up SL2#7.

SL5.03 harvested 22:40Z into the seat: the lockdown boolean is reserved — .agi/config.json gains a comms block (lockdown: false, verify: informational) read by one send.py helper _comms_config; lockdown: true prints exactly one warning per send/read that lockdown is NOT built until next season and encrypts nothing; _lockdown_requirements names encrypted-at-rest + an optional custodian signing server for the warning text only. Two kids proved. comms.verify is read here and acted on only by goal:g15.26.

SL5.05 harvested 23:29Z into the seat: line (2) landed — rotate-self is key-gated (no <seat>.key = refused by name with the keygen line, except a row with no pubkey which mints its first key: incremental fleet keying), mints the successor keypair through seatsig via send.py writers (no literal, no second writer), signs the rotation record with the predecessor key, appends the retired key to key_history (never deleted), carries pubkey + key_history in the ONE spawn-row write + commit, and replaces the key file only after both succeed (parent correction order). Four kids lean-proved 65-85; 482 green rotate neighbourhood. Lines (3) (4) stay briefed for the next generation.

2026-09-12T01:18Z mur-SL2.6-9 (Prime XIII 01:17Z, wf_f2ffc030-85d): ACCEPT with residue, no demote. P2 residues RECORDED, not cut — SL4.06 line (1): whois --sig/--msg CLI flags are parsed but never passed to whois() (dead path); keygen exits 0 when the row write was refused (key on disk + no pubkey = FORGED forever, UNKEYED after SL6.03); keygen never writes key_history []. SL5.03 lockdown: dm/room send/read/peek never print the lockdown warning. SL5.05 line (2): gate/mint decisions read the WORKTREE row while writes land on MAIN (a keyed worktree post can silently skip successor-key rotation); handover order inverted vs the claim; no e2e wiring test. Brief as fix-onlys after the g15.26 P1 rounds (F1-F4).

2026-09-12T03:31Z owner standing order 03:2xZ (via the Sensei, verbatim in extensions/agi/briefs/sensei-director-duties.md 'Rotation cost floors'): 'aim for floor of 1 call when rotating out and 0 calls on wake' — this goal's lines (3)(4) are the cuts; the Sensei's card §5 cut order puts one ahead of them: the seats.md EOF-newline dirt (a writer leaves 2e where HEAD has 0a; refused Prime XIII's rotate-self, cost XIV 2 wake calls; transient on MAIN after every rotation because the ack commits index-only from HEAD) cut as SL7.04 under hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean — one canonical serializer in node_writer, prepare check 2 + the ack gate read a whitespace-only delta as clean, the test is every seats.md writer leaves 0a at EOF.

2026-09-12T03:41Z OWNER ORDER 03:3xZ (rule-changing, via the Sensei 03:36Z, verbatim): 'Let predecessor choose whether to run diff or not for successor session ack' — inserted ahead of ask A; briefed as hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-hands-the-successor-exactly-one-call (rotate-self --ask-diff; default = answer continue, source predecessor; the back-fill + own-row commit + push ride the rotating side; STARTUP prints 'ack: answered continue by your predecessor — nothing to run' or the exact one diff line; folds mur-SL2.12 (3): edited_by-only foreign delta ignored, rows paired by name never index, chain test on a fixture registry). Cut as SL7.06 the moment F1 (SL6.05) harvests — same post-join region of cmd_rotate_self. Line (3)'s existing brief narrows to the rotate-out half (--stops, one signed commit) and follows; line (4) after it.

2026-09-12T03:50Z mur-SL2.6-9 residues on SL4.06 (keygen exits 0 on a refused row write; no key_history seed; whois --sig/--msg dead path — already closed by SL6.08) and SL5.03 (dm/room verbs never print the lockdown warning) cut as SL7.02 under hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged (send.py only), folded with the Sensei's seam finding and mur-SL2.12 (1)(2). Sensei §5 'send.py read wraps at 160' is already landed (--wrap default 160).
