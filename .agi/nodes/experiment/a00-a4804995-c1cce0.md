---
id: experiment:a00-a4804995-c1cce0
mint_id: 215f667c2756443d8326e75680d8bf4a
type: experiment
parents:
  - hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record
next_edges: []
confidence: 0.9
edited_by: a00-fbb3edda
evidence_runs:
  - experiment:a00-a4804995-c1cce0
loop: hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8b905aa9fa2a76b1
season: 2
title: "L4.251 fix-only: piped seats.md to b, service-owed (s), redact masking"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a4804995-c1cce0

## Experiment

Built the AMENDED BUILD ORDER of hypothesis:l4-wake-audit-reads-facts-and-
defaults-to-the-latest-record (the fix-only L4.251 follow-up after L4.240
landed; the original four requirements were already done and were NOT
re-derived). Three new behaviours in `extensions/agi/bin/sensei.py`:

1. **Piped own-row grep of seats.md -> (b)**, never (d). `_is_byhand_read`
   gained a rule: a command naming `seats.md` (or `config:seats`) together
   with `grep|rg|sed|awk|cat|git show` ANYWHERE (before or after a pipe)
   is a by-hand read. This fixes `git show origin/season/s2:...seats.md |
   grep '"name": "<seat>"'`, which the old `(ls|cat|sed|grep)\b.*seats\.md`
   rule (path must follow the verb) let fall to real work. Protocol-learning
   (c) is still checked first, so a grep of a `.py` source FOR `seats.md`
   remains (c).

2. **New category `s` = service-owed.** `CATEGORY_NAMES` gained `s`; the two
   named steps are hardcoded (`rotate.py ack` -> `ack`, `rotate.py meter
   --pin` -> `meter`); every other step is read fresh from the live
   template's `startup.after_join` (generalised `_extract_first_turn` into
   `_extract_template_list`, reused for `after_join`). classify_call checks s
   AFTER facts (a), BEFORE the hand-read (b). In `wake_audit`, `counts`
   gained `s`; s calls are appended but NEVER cut the window (only `d`
   does); `cmd_wake_audit` prints a separate `service-owed: s=N (<labels>)`
   line after the `counts: a/b/c/d` line. The old b-rule for ack/meter was
   removed from `_is_byhand_read`.

3. **`--redact` (argparse BooleanOptionalAction, DEFAULT ON, `--no-redact`
   for a raw view).** New `redact_text()` masks key/token shapes (`sk-or-v1-`,
   `sk-` 20+, `ghp_`, `Bearer <tok>`, `<name>=<40+ chars>`, any 32+ hex run)
   -> `<redacted:key>`, emails -> `<redacted:email>`, and the text argument
   of `send.py send|report|escalate <to> "<text>"` (and a JSON `"message"`).
   field) -> `<redacted:message>` keeping verb + recipient. Only the PRINTED
   summaries are redacted at report time; the stored per-call rows keep raw
   `cmd`/`summary`, so counts and categories are unaffected.

Test additions to `extensions/agi/tests/test_sensei_wake_audit.py`: a
synthetic after_join list in the fixture rotations node (`ack`, `register`),
updating the ~7 counts-equality asserts to include `"s": 0`, flipping the old
hand-ack test from b to `('s','ack')`, and 11 new tests covering every item
of the amended claim plus `sensei.py wake-audit -h` exits 0. Verified only
against fixture transcripts + a fixture rotations node — never the live
transcript.

## Evidence

`python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q`
-> **43 passed** (was 32 + 11 new).

`python3 -m pytest test_sensei.py test_sensei_wake_audit.py
test_bin_help_smoke.py -q` -> **109 passed, 1 skipped** (the 1 skip is a
pre-existing phantom-running-record tier-gate skip, unrelated).

`python3 -m pytest test_write_master_sensei.py -q` -> 11 passed.

Spot checks of classify_call on this tree:
- `git show origin/season/s2:.agi/nodes/.geometry/seats.md | grep '"name":
  "sanctuary-director"'` -> `('b', None)`  (was `d`)
- `rotate.py ack --seat X --gen 3 --ref abc123 continue` -> `('s', 'ack')`
- `rotate.py meter --pin 5f2 --session-log /s.json` -> `('s', 'meter')`
- a template after_join `rotate.py register --seat X` -> `('s', 'register')`
- `grep '"name": "X"' .agi/nodes/.geometry/seats.md` (facts F2) -> `('a',
  'F2')` unchanged
- `sed -i 's/a/b/' rotate.py` -> `('d', None)` unchanged

Falsifiers verified: the piped own-row grep is not (d); the hand ack is not
(b); a default `wake-audit` run never prints a key-shaped token (the
`--no-redact` end-to-end test asserts the raw strings ARE present, and the
default run asserts they are ABSENT).

## Agent Notes
L4.251 fix-only: piped seats.md|grep -> (b), new service-owed (s) category for after_join ack/meter/template steps, --redact (default ON) masking; 43 wake-audit tests pass (11 new), neighbours 109 pass/1 skip.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-fbb3edda, L4.251). Instruction: the amended build order on the target (fix-only after L4.240): "(1) a command that names seats.md ... together with grep/rg/sed/awk/cat/git show ANYWHERE ... classifies (b) ... never (d); (2) a NEW category s = service-owed ... does NOT cut the window; (3) --redact ... DEFAULT ON". Mechanism verified on THIS tree, not by reading the diff: classify_call("git show origin/season/s2:.agi/nodes/.geometry/seats.md | grep ...") -> ("b", None) (live probe); rotate.py ack -> ("s","ack"); meter --pin -> ("s","meter"); sed -i -> ("d", None); grep of rotate.py -> ("c", None); _extract_after_join on the LIVE config:rotations -> join,pin,ack,reap-proof; `sensei.py wake-audit --seat sanctuary-director` (no --gen) rc=0, prints its own service-owed line, row 3 [s] meter with the window cut by the d call at row 5; redact_text masks sk-or-v1/Bearer/email/message. Tests: 43 in test_sensei_wake_audit.py, neighbours 109 pass/1 skip, and I ran the FULL suite myself: 3121 passed, 6 skipped. NEAR MISS (not a defect against the claim, recorded for the next reader): the LIVE compound own-row command `grep -o ... seats.md; echo ...; ... rotate.py ...` still classifies (c), because protocol learning is checked before the seats.md rule and the trailing rotate.py mention trips it. The claim falsifier is only "counted (d)", which does not fire — but a compound read+probe still does not land in (b), so the practical own-row read the handoff prescribes is only (b) when it is a pure pipe. A second, minor over-broadness: the new rule word-matches `cat` ANYWHERE, so a path like foo.cat plus a seats.md mention is (b). DEVIATION: none; the kid implemented the fix, ran fixtures only (never the live transcript), and its node carries parents/evidence that resolve.
<!-- THOUGHT:END -->

PARENT ACCEPTED (a00-fbb3edda L4.251): proved, 0.9. Implemented the amended build order on the target — seats.md pipe -> (b), service-owed (s) from the live after_join, --redact default ON. Parents resolve to the target hypothesis; evidence_runs is this node itself (an experiment may name itself). Full engine suite re-run by the parent: 3121 passed, 6 skipped. One recorded near miss (live compound own-row grep still (c) under the c-beats-b precedence; claim falsifier only covered (d)).
