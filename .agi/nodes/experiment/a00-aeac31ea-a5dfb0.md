---
id: experiment:a00-aeac31ea-a5dfb0
mint_id: 5932163a3669467eaf90e68c28d9ef54
type: experiment
parents:
  - hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review
next_edges: []
confidence: 0.8
edited_by: a00-3a5689fc
evidence_runs:
  - experiment:a00-aeac31ea-a5dfb0
loop: hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cae186dc200c9d8b
season: 2
title: A00 aeac31ea a5dfb0
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-aeac31ea-a5dfb0

## Experiment

G15.26 is a BUILD ORDER, not a measurement: this round implements clause
(1) (2) (4) of hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-
and-the-value-flips-after-a-named-review in the ONE delivery path, and proves
clause (4) by byte-equality. Scope for this kid is clauses (1)(2)(4); whois
(clause 3) and the flip recording (clause 5) go to the second kid and were
left untouched.

### What I built

Enforcement lives ONLY in `_print_blocks_with_labels(root, me, blocks, wrap)`
in `extensions/agi/bin/send.py` (the single path both `read` and `peek`
call), plus one helper `_quarantine_block(...)` — no new bin/ file. It reads
`_comms_config(root)["verify"]` and enforces ONLY when that value is the
exact string `"enforcing"`; any other value, an absent `comms` block, or an
unreadable config is informational/identical to today.

For a block whose label (from `_labels_for_blocks`/`_verify_block`) is EXACTLY
`FORGED` (never `RETIRED:<fp>`, never `UNSIGNED`, never `VERIFIED ...`), under
enforcing it prints ONE refusal line INSTEAD of the block:

    REFUSED FORGED from <from> ts <ts> fp <fp>: withheld to <quarantine path>

`<fp>` is the fingerprint from the block's `sig:` line (`scheme:fp:hex`);
`<quarantine path>` is `<inbox_dir>/quarantine/<me>.md` absolute. The block's
RAW inbox bytes (the `MSG_SEP`-rejoined block, since `_scan_messages` splits
the separator off) append to that file with `open(path, "a", newline="")` —
create the dir on first use, never rewrite or truncate, `newline=""` so CR
bytes survive (mur-39 order (d)).

`read` and `peek` were each changed by ONE line (pass `me` into the delivery
path); the read-marker/advance logic is untouched. The inbox file's content is
left exactly as the reader found it apart from the read marker — the refused
block is not deleted or edited; the quarantine append is a second file.

VERIFIED, UNSIGNED and RETIRED blocks print in FULL with today's label under
BOTH modes. The value in `.agi/config.json` stays `{"lockdown": false,
"verify": "informational"}` — the flip is the Prime's one-line edit after the
named review names this round (sentence below).

### Tests added (extensions/agi/tests/test_send.py, with the neighbours)

1. `test_enforcing_refuses_forged_and_quarantines_raw_bytes` — good bytes:
   FORGED body does NOT print; one `REFUSED FORGED from seat-a ts <ts> fp
   <fp>: withheld to ...` line prints INSTEAD; quarantine file is byte-equal
   to the refused block's raw inbox bytes.
2. `test_peek_enforcing_refuses_forged_too` — same refusal via `peek` (one
   delivery path, both verbs).
3. `test_enforcing_prints_verified_and_unsigned_in_full` — nothing but FORGED
   is withheld; no quarantine for non-FORGED.
4. `test_enforcing_prints_retired_in_full` — RETIRED prints in full under
   enforcing, never refused (see case below).
5. `test_absent_and_informational_print_identical_bytes` — clause (4): the
   same inbox under a comms block ABSENT and under `verify:informational`
   prints byte-identical output (peek toggled config, cursor not advanced; ts
   pinned via monkeypatch). Fails if informational differs by a byte.
6. `test_quarantine_appends_never_truncates` — two refused blocks append both
   raw copies (mode "a", never truncating).

Exact commands and results:

    python3 -m pytest extensions/agi/tests/test_send.py -q \
      -k "enforcing or absent_and_informational or quarantine or retired \
          or forged or unsigned or verified"
    -> 18 passed, 194 deselected

    python3 -m pytest extensions/agi/tests/test_send.py \
      extensions/agi/tests/test_seatsig.py extensions/agi/tests/test_sensei.py \
      extensions/agi/tests/test_heal.py extensions/agi/tests/test_bin_help_smoke.py -q
    -> 305 passed, 2 skipped

### End-to-end demo (informational→enforcing config written to a temp project)

Command: a signed send to seat-a, body tampered on disk to break the sig
(header untouched), then `send.read(root, "recv", None)` under
`{comms:{verify:"enforcing"}}`. Output:

    === send.py read under comms.verify=enforcing ===
    REFUSED FORGED from seat-a ts 2026-09-11T23:04:51.473512+00:00 fp
      d39eea30e57471c1: withheld to /tmp/qdemo/proj/.agi/sessions/inbox/quarantine/recv.md

No block body printed. The quarantine file held the raw bytes verbatim
(`---` separator, header, `sig:` line, `FORGED-BUT-KEPT` body).

### RETIRED refusal — case for/against (per the hypothesis requirement)

REFUSE nothing but FORGED, and this round builds that line as decided.
Case AGAINST refusing RETIRED: a retired key is still a genuine past key of
a live seat, audited out of the current set intentionally — a message it
signed was real when written, so quarantining it applies the forgery penalty
to legitimate history and could strand a seat's own old mail. Case FOR
refusing RETIRED: a tightened reader might prefer any non-current signature
held out for human review, since an attacker holding an old leaked priv can
replay all retired windows. The deciding fact is severity: FORGED is a live
imposture to stop; RETIRED is a provenance question, not a boundary breach,
so today's refusal line stays FORGED-only and the tradeoff is recorded here
for the named review to weigh.

### Clause (5) sentence

Flip to `"enforcing"` is the Prime's one-line `.agi/config.json` edit made
after the named review names this round.

## Evidence

- Green suite: `305 passed, 2 skipped` (5 files, exactly the required set).
- End-to-end refusal line and verbatim quarantine bytes captured above.
- The config value on season/s2 was NOT changed (still informational); the
  file in the published tree holds the enforcing value only in the throwaway
  temp project that proved the built path.

## Agent Notes
Built g15.26 enforcing FORGED-refusal in the ONE delivery path _print_blocks_with_labels (both read+peek): REFUSED line instead of block + verbatim quarantine append (mode a, newline=''); VERIFIED/UNSIGNED/RETIRED print in full; absent/informational byte-identical to today. 6 new tests; 305 passed, 2 skipped. Config NOT flipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-3a5689fc, SL5.04). WHAT THE INSTRUCTION SAID: implement clauses (1)(2)(4) of hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review -- under comms.verify exactly 'enforcing' a reader withholds a FORGED block, prints one 'REFUSED FORGED from <from> ts <ts> fp <fp>: withheld to <quarantine path>' line, appends the block's RAW inbox bytes to <inbox>/quarantine/<seat>.md, refuses nothing else (VERIFIED/UNSIGNED/RETIRED print in full), and informational stays byte-identical. WHAT THE MACHINE ACTUALLY DOES, measured on the staged bytes I read: send.py:2197 _print_blocks_with_labels(root, me, blocks, wrap) reads _comms_config(root).get('verify')=='enforcing' (exact string equality, so absent/any-other-value is informational), and for a label equal to FORGED exactly it calls _quarantine_block (send.py:2183: qdir.mkdir(parents=True, exist_ok=True), open(path,'a',newline=''), raw=block if startswith MSG_SEP else MSG_SEP+block) and prints the REFUSED line instead of the block; read (send.py:2282) and peek (send.py:2330) are the only callers, both passing me. I RAN pytest extensions/agi/tests/test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py -q -> 305 passed, 2 skipped; 6 new tests cover refusal-instead-of-body, quarantine==raw-inbox-bytes, peek parity, no-quarantine-for-non-FORGED, RETIRED full-print, absent-vs-informational byte equality, append-not-truncate. .agi/config.json stays {lockdown:false, verify:'informational'}. THE NEAR MISS: building quarantine by re-rendering the parsed block (MSG_SEP + 'ts: ...' + text) instead of returning the raw slice -- _parse_block strips exactly one trailing newline, so a CR-carrying or trailing-whitespace body would silently differ from the inbox bytes; the falsifier 'quarantine bytes != the block's inbox bytes' catches exactly that, and the kid avoided it by slicing. A second near miss: gating enforcement on a substring test for FORGED rather than exact equality would still pass today (RETIRED/UNSIGNED/VERIFIED do not contain the word) but would refuse any future label that embeds it. DEVIATION FROM A STANDING RULE: none. CAVEAT recorded, not a blocker: peek does not advance the read cursor, so a repeated peek under enforcing re-appends the same FORGED bytes to quarantine each time -- append-only and within the literal claim ('never deleted, never rewritten'), but a reader who peeks repeatedly accumulates duplicates. ACCEPTED as inconclusive_lean_proved:85 (clauses 3 and 5 remain; clause 2's RETIRED case is written out in the body).
<!-- THOUGHT:END -->

PARENT REVIEW (a00-3a5689fc, SL5.04): ACCEPTED inconclusive_lean_proved:85. Implementation read on the staged bytes (send.py:2197 _print_blocks_with_labels gates on _comms_config(root).get('verify')=='enforcing', refuses only labels[i]=='FORGED' via _quarantine_block at send.py:2183, both read:2282 and peek:2330 route through it). I re-ran the 5-file suite myself: 305 passed, 2 skipped. Config value NOT flipped, as required. Clauses (3) whois --sig exit 2 and (5) the flip sentence are the second kid's scope. Caveat recorded in THOUGHT: repeated peek re-appends the same FORGED bytes (append-only, within the literal claim, but duplicates accumulate).
