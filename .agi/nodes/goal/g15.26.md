---
id: goal:g15.26
mint_id: 9d9ae5c621d94fd28a1f4c66b395b6ad
type: goal
parents:
  - goal:g15.25
  - build:bin-send
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.26
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 3423cb5fc8279e24
season: 2
seeds:
  - hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review
status: active
tags:
  - goal
  - subgoal
  - l4
  - sensei-director
thought_session: sensei-director-genV-L5
title: "G15.26: signature verification flips to ENFORCING — a reader refuses a FORGED block under comms.verify=enforcing; the flip of the value follows a named review"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.26

**OWNER GO (22:1xZ, verbatim in `doc:l4-owner-decisions` lines 657-658; relayed by Prime XII 22:14Z):** "I'm good to GO, go for fix and flip" — after the FIX lands (SL5.02: injective canonical form, ONE seatsig registry, verify-side RFC vector), the FLIP to ENFORCING is its OWN round on its OWN goal line; readers may refuse on a bad signature; labels stay until then; it is reviewed by name before any reader refuses.

## Why this exists

This goal exists because `goal:g15.25` line (1) (SL4.06, merge-up SL2#6 at 0ca5a801b) put a signature on every send and a label — VERIFIED / UNSIGNED / FORGED / RETIRED — on every read, under the Prime's 21:17Z gate *SIGN NOW, VERIFY LATER*: the label is informational, no reader exits or refuses on it (`send.py _verify_block`, `_label_for_sig`, `_whois_sig_label`). `build:bin-send` is the mechanism this goal changes: the reader's response to a FORGED block moves from "label and print" to "refuse and withhold", switched by ONE config value (`comms.verify`, reserved by `hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built` under g15.25) so the code for enforcing lands first and the VALUE flips only after the named review the owner asked for. mur-39's three crypto orders (SL5.02, `hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged`) are the precondition: a reader must never refuse on a signature the canonical form could have mis-bound.

## Testable claim

Under `comms.verify: enforcing` a `read`/`peek` WITHHOLDS the body of a FORGED block and prints one refusal line (`REFUSED FORGED from <from> ts <ts> fp <fp>: withheld to <quarantine path>`), moving the block's bytes to `<sessions>/inbox/quarantine/<seat>.md` (appended, never deleted); UNSIGNED and RETIRED blocks keep their labels and print in full (UNSIGNED is not a bad signature — kids and parents are not keyed seats; RETIRED is a good signature under a retired key — whether it is refused is the named review's call, recorded here); `whois --sig` under enforcing exits non-zero on FORGED. Under `informational` (the default, and the value on season/s2 until the review) nothing changes byte-for-byte. The flip of the VALUE is a one-line `.agi/config.json` edit made by the Prime after the review names the round.

**Falsifiers:** a FORGED block prints its body under enforcing; a quarantined block's bytes differ from the inbox bytes; a VERIFIED, UNSIGNED or RETIRED block is withheld; `informational` output differs from today's by one byte; any reader refuses while the config still says informational.

## Status

Minted 2026-09-11 22:2xZ (loop L5). Serial after SL5.02 + merge-up SL2#7; brief `hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review`.

## Agent Notes

SL5.04 harvested 23:22Z into the seat: the enforcing CODE is in — under comms.verify=enforcing a read/peek withholds a FORGED block (one REFUSED FORGED line, bytes appended verbatim to inbox/quarantine/<seat>.md, never deleted), VERIFIED/UNSIGNED/RETIRED print in full, informational output is byte-identical, whois --sig exits 2 on FORGED; the season/s2 value is still informational. Kids lean-proved 85/90; caveat for the named review: a repeated peek of the same FORGED block re-appends it (append-only, duplicates accumulate) — a dedupe by (ts, from, sig) is the obvious fix-only if the review wants it. The VALUE flip is the Prime one-line edit after that review.
