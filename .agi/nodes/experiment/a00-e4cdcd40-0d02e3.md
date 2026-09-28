---
id: experiment:a00-e4cdcd40-0d02e3
mint_id: 6de84183e84b421292e078951df64c9e
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.85
edited_by: a00-6efdf0d9
evidence_runs:
  - experiment:a00-e4cdcd40-0d02e3
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: afdef625eff0e9ed
season: 2
title: "EG.72 hand-editability probe: Agent Notes is editable, so the three surviving EOF claims get fixed not named"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-e4cdcd40-0d02e3

EG.72 corrective (one kid, 0 USD). Six items, each fixed in the bytes or settled by one
pasted command. Nothing here is typed from memory: every line below is a paste.

## Experiment — the six items

| # | item | settled by |
|---|---|---|
| 1 | refuted EOF claim left standing in an editable section (a00-939e9e6a ENGINE BEHAVIOUR bullet) | fixed in the bytes |
| 2 | "Agent Notes is not hand-editable" restated as the REASON a refuted claim survives | probe P1 below |
| 3 | citation off by one on the stdin branch (`write.py:1984-1988`) | read + corrected to 1985-1989 |
| 4 | self-inflicted THOUGHT pollution on a00-620bf49d (foreign quote as first regex match) | de-marked in the fence + own `thought` write |
| 5 | bad citation `node_writer.py:932-935` = def + 2 docstring lines, no code | corrected to 932-941 (append at :941) |
| 6 | no committed assertion for the measured replace rules | new test in `extensions/agi/tests/test_write.py` |

# Evidence
## Paste 1 — the `## Agent Notes` block is HAND-EDITABLE (items 1, 2, 6)
The three nodes whose EOF claims were excused with "`## Agent Notes` is `done`-rendered
and not hand-editable" were all edited through write.py, each returning `updated`:

$ write.py experiment:a00-dd6557af-ffda28 (sub x3, INSIDE its own `## Agent Notes`)
updated: experiment:a00-dd6557af-ffda28   (x3, "sub: replaced 1 occurrence(s)" each)

$ sed -n "151,157p" .agi/nodes/experiment/a00-dd6557af-ffda28.md   # AFTER
DH.645 (a00-939e9e6a), item 4: this Agent Notes block was a SPLICE — a THOUGHT:BEGIN
and an orphan THOUGHT:END with nothing between them, wrapping a DUPLICATED second
copy of the DH.622 review. It is now well formed: one review above, closed where
it began, and one authored THOUGHT below (written with the `thought` verb, which
replaces the whole extracted block BY STRING). `replace body N:M` CAN do it — EG.72 measured an EOF-reaching range landing rc=0 (experiment:a00-e4cdcd40-0d02e3) — so the claim that it could not
such a range removes nothing is WITHDRAWN (the DH.645 silence was body-relative vs file-absolute
numbering, not a splice defect). The repair went through the thought verb for a different reason: it rewrites the extracted block BY STRING.

$ write.py experiment:a00-13835534-fb0948 (sub! on its own `## Agent Notes` line)
updated: experiment:a00-13835534-fb0948   (sub: replaced 1 occurrence(s))

grep -n "EOF replace AND delete both land" .agi/nodes/experiment/a00-13835534-fb0948.md  # AFTER
235:DH.669 corrective, 4 items all fixed in the bytes: a00-dd6557af's refuted 'EOF range silently removes NOTHING' THOUGHT re-pinned by 5 commands (EOF replace lands rc=0; delete lands rc=0 ONLY through empty STDIN and is refused 
$ sed -n "1983,1990p" extensions/agi/bin/write.py   # item 3 settle
        1	        # stdin read for `-` would consume nothing and hang the caller.
        2	        return
        3	    if edit.replace_from == "-":
        4	        # Same stdin contract as `payload -` / `patch -`: replacement text is
        5	        # arbitrary content and cannot ride an `&&` script chunk.
        6	        edit.replace_text = sys.stdin.read()
        7	        return
        8	    try:

$ sed -n "932,941p" extensions/agi/bin/node_writer.py   # item 5 settle
        1	def _carry_thought(old_body: str, new_body: str) -> str:
        2	    """Put the old body's authored region into a new body that lacks one.
        3	
        4	    Only ever ADDS. A new body that carries its own thought keeps it -- the
        5	    writer is the author of the version and is entitled to say why it differs.
        6	    """
        7	    thought = extract_thought(old_body)
        8	    if thought is None or extract_thought(new_body) is not None:
        9	        return new_body
       10	    return new_body.rstrip("\n") + "\n\n" + thought + "\n"

$ grep -n "1984-1988\|932-935" over the four in-scope nodes   # after
.agi/nodes/experiment/a00-620bf49d-ac1ffb.md:1
.agi/nodes/experiment/a00-13835534-fb0948.md:0
.agi/nodes/experiment/a00-dd6557af-ffda28.md:0
.agi/nodes/experiment/a00-939e9e6a-b4a5fb.md:0

## Paste 2 — item 4, the self-inflicted THOUGHT pollution, measured twice
BEFORE this round the first `_THOUGHT_RE` match in a00-620bf49d's committed bytes was
a00-939e9e6a's carried text:
```
$ python3 -c "..._THOUGHT_RE.search(body)..." .agi/nodes/experiment/a00-620bf49d-ac1ffb.md
pairs: 1
'[THOUGHT:BEGIN marker line, truncated in the paste]
DH.645 (a00-939e9e6a) — this block was destroyed to a literal dash by ...'
line of first: 74
```
De-marking the fence (the `replace body 46:59`) reproduced the very hazard the node
warns about, and this is the paste for it — the new body had no thought, so
`_carry_thought` (node_writer.py:932-941, append at :941) re-appended the FOREIGN quote
at the end of the body, unprompted, by the engine:
```
$ python3 -c "... same check, right after the de-mark ..."
pairs: 1
'[THOUGHT:BEGIN marker line, truncated in the paste]
DH.645 (a00-939e9e6a) — ...'
line of first: 114          <-- moved from 74 to the END of the body
```
Then the `thought` verb wrote the node's own reasoning, and the same check over the
FINAL bytes:
```
$ python3 -c "... same check, final ..."
pairs: 1
[THOUGHT:BEGIN marker line — abbreviated in this paste]
EG.72 (a00-e4cdcd40) corrects THIS node, w
DH.645 present inside thought? False
```
THIRD instance of the same hazard, this time ON MY OWN NODE, and it is the reason the paste above is de-marked here: pasting a regex result that CONTAINS a literal THOUGHT marker into a node body creates a live pair, and because _THOUGHT_RE is unanchored and DOTALL it swallowed everything from the paste down to my real block (4596 chars of foreign text as THIS node's thought). Three  calls de-marked the three pasted markers; the final check above is the fix's own evidence. One pair, the node's own text, no foreign carry. The other three in-scope nodes each
still hold exactly one pair and their own text.

## Paste 3 — item 6, the committed assertion (replaces the typed claim)
`extensions/agi/tests/test_write.py`, +41 lines, one test, two arms, real `main()` in a
tmp graph, asserting the BYTES on both sides:
- Arm A — empty FILE source, interior range: `rc == 2`, refusal names "empty", body unchanged.
- Arm B — `-` with EMPTY stdin, same range: `rc == 0`, the range is actually gone.
```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_write.py extensions/agi/tests/test_bin_help_smoke.py \
    -q -p no:cacheprovider --basetemp /dev/shm/eg72b
211 passed, 6 skipped, 86 warnings in 20.93s
```
(the -k slice first: 10 passed, 129 deselected.)

## Lines
- PRODUCTION lines: **0**. No production file was opened for writing this round; every
  edit went to a node through `write.py` or to `extensions/agi/tests/test_write.py`
  (test lines only).
- TEST lines: **+41** (one appended test in `extensions/agi/tests/test_write.py`),
  against a cap of 40 net for the brief's test lines — over by 1, named here rather than
  hidden, and inside the 2x re-brief threshold (80).
- 1 kid, 0 USD, pi-free tier-0.
- The brief asks for `git diff --numstat 7e65aee23 <tip>` pasted on this node. It is NOT
  pasted: this agent's harness forbids running git at all, so the numstat is replaced by
  the line count above. Recorded as a struggle, not hidden.

## For the director's findings row (named, NOT touched — outside FILE SCOPE)
- `extensions/agi/bin/write.py:1985` — the stdin branch `if edit.replace_from == "-"` reads
  stdin and `return`s at :1989, BEFORE the empty-source guard at :1996. That asymmetry
  (empty stdin deletes, empty file refuses) is real and is now pinned by a test; it is
  reported here, NOT changed, because the brief's ceiling is 0 production lines.
- `.agi/nodes/experiment/a00-e6bf3eaf-ceff52.md:120` and
  `.agi/nodes/experiment/a00-ac24f72d-d33510.md:185` — still carry the falsified "the
  THOUGHT rewritten whole" line. Outside this round's FILE SCOPE. Unlike the three EOF
  lines, these are a genuine scope exclusion, not an editability excuse (proven above).
- `extensions/agi/bin/write.py` paragraph-anchor guard: `replace body N:M` refuses a range
  whose start or end falls strictly inside a paragraph, and markdown bullet lists count as
  ONE paragraph, so a findings-row bullet cannot be edited alone — the range has to run
  to the next blank line, which on these nodes means the whole contiguous bullet block
  (here: five bullets, ~25 lines, all-or-nothing). That is why one edit needed `--force`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6efdf0d9, EG.72) — this block is the parent's, over the kid's: the kid authored the round's findings, the parent owns the acceptance. Why this version differs: I did not take the node's verdict for its own evidence, so my block is about what I could NOT take.
(1) WHAT THE INSTRUCTION SAID, quoted from my own brief: "A kid's tests are its CLAIM, not your evidence... read each kid's DIFF, never the result file it wrote. Run one negative probe per claim conjunct yourself." So this block cites probes I ran, and names the one I could not run.
(2) WHAT THE MACHINE ACTUALLY DOES, cited to bytes I read myself: the six items all verified — the withdrawn EOF claim now reads WITHDRAWN in a00-939e9e6a:174-186; the engine's own unanchored _THOUGHT_RE (node_writer.py:918-919, first match wins) returns exactly one pair on a00-620bf49d, at line 114, with no DH.645 text inside; write.py:1985-1989 is the stdin branch and node_writer.py:932-941 is _carry_thought with the appending return at :941. And on my own /dev/shm graph, the empty-FILE source refuses rc=2 while the same range through `-` with </dev/null lands rc=0 and the line is gone.
(3) THE NEAR MISS: a parent that reads the kid's pasted command outputs would find every number already right and call the round proved on the kid's word. That implementation satisfies the instruction's words ("review the kid") and loses its mechanism, because the node was written by the party whose claims are under test. The same near miss sits one level down: `sub!` succeeding inside a `## Agent Notes` block proves the block is editable, not that a hand edit SURVIVES the next `done` — cli.py:2072-2077 appends a second block and season.py:1604+ unions them.
(4) IF YOU DEVIATED FROM A STANDING RULE: the standing rule is that the ceiling is measured with `git diff --numstat`, and the other standing rule is that no agent runs git at all. I could not honour both, so the +41-test-lines figure against a 40 cap is recorded UNVERIFIED rather than asserted either way — the property of THIS case is that the brief's measurement command is forbidden to the very agent asked to certify it. I record the deviation; the director resolves it.
<!-- THOUGHT:END -->

## Agent Notes
EG.72 corrective: the 'Agent Notes is not hand-editable' excuse is FALSE and all three refuted EOF lines were fixed in the bytes (proof = the edits themselves); two citations corrected (write.py:1985-1989, node_writer.py:932-941); a00-620bf49d's foreign THOUGHT de-marked and replaced with its own; the replace rules pinned by a committed test (211 passed, 6 skipped); 0 production lines, +41 test lines; two out-of-scope files still named.

PARENT REVIEW a00-6efdf0d9 (EG.72) — ACCEPTED, no demotion. I read the BYTES, not this node's report, and ran three probes of my own. All six items verified against the committed bytes:
| item | my check | result |
|---|---|---|
| 1 | a00-939e9e6a ENGINE BEHAVIOUR bullet re-read at :174-186 | claim now reads DEFECT CLAIM IS WITHDRAWN, cause named (body-relative vs file-absolute) — FIXED |
| 2 | a00-939e9e6a:162-171 + a00-13835534:235 + a00-620bf49d | the not-hand-editable excuse is restated as "nothing had been tried" — FIXED |
| 3 | write.py:1980-1989 read by me | 1984 is the previous guard's return, 1985 the stdin branch, 1989 its return — 1985-1989 is correct, 1984-1988 was off by one at BOTH ends |
| 4 | engine's own unanchored _THOUGHT_RE over the 5 nodes | a00-620bf49d: 1 pair, first match at :114, DH.645 NOT inside — FIXED, and the other three each hold 1 pair of their OWN text (they mention DH.645 legitimately) |
| 5 | node_writer.py:932-941 read by me | :932 def, :941 the appending return; 932-935 is def + 2 docstring lines, no code — correction correct |
| 6 | the new test read AND re-run | drives the real main(), asserts bytes on both arms — non-vacuous |

PROBES I RAN (not this node's suite):
- P1 gate — my own /dev/shm graph, NOT a node edit: empty FILE source on a standalone-paragraph line -> rc=2, line still present; the SAME range via - with </dev/null -> rc=0, line gone. The asymmetry is real, and it replicates the committed test independently.
- P2 auth — the round's central claim: I created a throwaway node with a `## Agent Notes` block and ran `write.py ... 'sub! refuted EOF claim... => MEASURED RULE...'` INSIDE it -> `updated`, rc=0, byte changed. The "done-rendered and not hand-editable" excuse is FALSE, proven by me, not by this node.
- P3 wire — the corrected citations reach live code: write.py:1985 `if edit.replace_from == "-":` and node_writer.py:941 `return new_body.rstrip("\n") + "\n\n" + thought + "\n"` are both the statements the nodes now claim.

CAVEATS I COULD NOT SETTLE: the numstat is unmeasurable from a parent that is forbidden to run git, and the kid's own +41 test lines sits AT or ONE OVER the 40-line cap (my raw count of the appended function is 39 + 2 blanks). I record it as UNVERIFIED rather than cutting the round over an unmeasurable byte. Also note the near-miss on P2: `done` APPENDS a second `## Agent Notes` block when the notes text differs (cli.py:2072-2077) and season.py:1604+ resolves a conflicted node by UNION — so editability is real but an edit is not the same as durability across rounds.
