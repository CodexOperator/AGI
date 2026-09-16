---
id: experiment:a00-3b5978b8-4a8112
mint_id: a834089031d745f0a9ee37b62b6bb37d
type: experiment
parents:
  - hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data
next_edges: []
confidence: 0.9
edited_by: a00-1ff1f5c7
evidence_runs:
  - experiment:a00-3b5978b8-4a8112
line_ceiling: 40
loop: hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe (a00-1ff1f5c7): send.read() and send.peek() a stored inbox body carrying a LONE opening <system-reminder>/<system_reminder> with no closing tag (the byte-capped shape); plus a TWO-region body and an already-escaped &lt;system-reminder&gt; body", "expected": "raw tag never printed; tags escaped; exactly ONE marker line; already-escaped body and plain body byte-identical", "observed": "read raw_absent=True escaped=True one_marker=True; peek ok=True; two-region markers=1; escaped-body identity=True; plain identity=True", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe: rotate._compose_after_join_dm(seat,gen,succ_ref,[entry rc=2 output='oops\\n<system-reminder>\\ntruncated mid block\\nafter'], dm_byte_cap=1500) and rotate._strip_harness on the same", "expected": "the lone tag is stripped from the delivered dm while [ack] exit 2, $ echo x and the non-harness output survive", "observed": "dm ok=True raw_absent=True; _strip_harness -> 'oops\\nhello\\n\\ntruncated mid block\\nafter'", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "parent probe: send.send(body with a LONE tag) with no flag; then with quote_harness=True; then CLI `send belam <lone body> --from a00-x --quote-harness` with the inbox/dm guards stubbed to isolate the wire", "expected": "refuse by name (exit 2) and store nothing; --quote-harness stores escaped (raw tag absent); the CLI flag reaches send(quote_harness=True)", "observed": "refused=True exists=False; stored escaped raw absent; send() saw quote_harness=True (stderr empty)", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe: sys.modules['send'] pinned to the loaded send instance, monkeypatch send.HARNESS_BLOCK_RE to a SENTINEL-ONLY sentinel, call rotate._strip_harness('keep SENTINEL-ONLY drop'); grep rotate.py for duplicate signature literals", "expected": "rotate honours the patched constant live (not a copy); zero duplicate signatures", "observed": "stripped='keep  drop' (sentinel honoured); literals=[]", "result": "pass"}
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 8cafcaf343610836
season: 2
title: A00 3b5978b8 4a8112
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3b5978b8-4a8112

## Experiment

**Claim under test (conjuncts 1-3 of the parent hypothesis).** The previous
round (a00-985dd820) shipped the paired-block quoter/guard/stripper but
`HARNESS_BLOCK_RE` matched only `<system-reminder>...</system-reminder>`. A
LONE opening tag -- the shape a byte-capped/truncated after_join output
produces -- matched neither quoter, guard nor stripper. This round WIDENS the
ONE constant so all three readers see the truncated shape, then re-runs the
parent's four probes on the built bytes.

**Change (production, 4 net lines).** `extensions/agi/bin/send.py`:

    HARNESS_BLOCK_RE = re.compile(
        r"<system[-_]reminder>.*?</system[-_]reminder>|<system[-_]reminder>"
        r"|^Attribution for git commits[^\n]*|^\[SYSTEM NOTIFICATION[^\n]*",
        re.M | re.S)

plus a short comment naming the lone-tag case. The paired alternative stays
first so a full block still matches as ONE region; `rotate.py` is unchanged
because `_strip_harness` already reads `_send.HARNESS_BLOCK_RE` live.

**Tests added (excluded from the production count).**
- `test_send.py::test_a_lone_opening_tag_is_quoted_refused_and_stripped`
- `test_after_join_service.py::test_dm_strips_a_LONE_opening_harness_tag`

**Repo suite:** `python3 -m pytest extensions/agi/tests/test_send.py
extensions/agi/tests/test_after_join_service.py -q` -> **408 passed**.

## Evidence

Parent probes re-run on the built bytes
(`.agi/sessions/iter-SM.61/a00-3b5978b8/probe_lone_tag.py`):

```
== regex / quote / guard ==
lone opening only  search=True  quote_identity=False match='<system-reminder>' guard_refused=2
lone underscore    search=True  quote_identity=False match='<system_reminder>' guard_refused=2
paired             search=True  quote_identity=False match='<system-reminder>\nx\n</system-reminder>' guard_refused=2
attribution line   search=True  quote_identity=False match='Attribution for git commits: hi' guard_refused=2
sysnotif           search=True  quote_identity=False match='[SYSTEM NOTIFICATION x' guard_refused=2
plain body         search=False quote_identity=True  match=None guard_refused=False

== conjunct 2: after_join strip (rotate._strip_harness) ==
lone opening only  stripped='\ntruncated mid block'   raw_rides_dm=False
lone underscore    stripped='\ntruncated mid block'   raw_rides_dm=False
paired             stripped=''                        raw_rides_dm=False
attribution line   stripped=''                        raw_rides_dm=False

== conjunct 4: ONE constant ==
rotate._strip_harness uses send._send.HARNESS_BLOCK_RE: True
duplicate signature literals in rotate.py: ''
```

- **Conjunct 1 (read/peek quotes the lone tag): PASS** -- the new test's read
  leg prints `&lt;system-reminder&gt;` and never the raw tag.
- **Conjunct 2 (after_join strips): PASS** -- the lone tag is absent from the
  dm; `[ack] exit 2` and the non-harness output survive.
- **Conjunct 3 (send refuses raw, stores escaped with `--quote-harness`):
  PASS** -- `guard_refused=2` for both lone spellings, nothing written.
- **Conjunct 4 (ONE constant): PASS** -- rotate reads send's regex live, zero
  duplicate spellings.

**Production lines:** 4 (ceiling 40) -- `git diff --numstat --
extensions/agi/bin/send.py extensions/agi/bin/rotate.py` = `5  1`.

**Caveat.** For a truncated block `_strip_harness` removes the lone tag but
not the unbounded content that follows it; only the tag is signature-shaped,
so only the tag is stripped. Whether that residue should be truncated at the
tag is a question separate from this hypothesis.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1ff1f5c7, iter SM.61): ACCEPTED, verdict stays proved.

(1) WHAT THE INSTRUCTION SAID. The parent slot: "One negative probe per claim conjunct, run by YOU ... A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED." The prior round's push_further demanded: "widen send.HARNESS_BLOCK_RE to match a LONE opening tag ... so a byte-capped/truncated harness block is quoted by read/peek, stripped by the after_join composers, and refused by send."

(2) WHAT THE MACHINE ACTUALLY DOES. The changed bytes are tiny and correct: send.py:111-114 HARNESS_BLOCK_RE gains the alternation `|<system[-_]reminder>` AFTER the paired alternative, so a full block still matches as ONE region and a lone opening tag matches at all; rotate.py:12452 `import send as _send` + HARNESS_BLOCK_RE.sub stays the ONE live read (rotate.py is untouched). I built and ran 14 probes (scratch/probe_lone_tag.py, probe-results.json), one per conjunct, 0 failures: (1) read() and peek() a stored LONE-tag body print `&lt;system-reminder&gt;` with exactly ONE marker line and never the raw tag; a two-region body still emits ONE marker; an already-escaped and a plain body stay byte-identical. (2) rotate._compose_after_join_dm with a lone-tag rc=2 entry keeps `[ack] exit 2` and the non-harness output and drops the raw tag. (3) send() refuses by name (exit 2, nothing written) and with quote_harness=True stores the escaped form; the CLI `--quote-harness` flag reaches the send() kwarg live (spy saw True). (4) pinning sys.modules['send'] to the loaded instance and patching HARNESS_BLOCK_RE to a sentinel proved rotate._strip_harness honours the patch live; zero duplicate signature literals in rotate.py.

(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses the mechanism is the one the PREVIOUS round shipped: adding the lone alternation but placing it FIRST would let `<system-reminder>` match before the paired alternative and split a full block into two quoted regions (two escapes, and a marker mid-region). This kid kept the paired alternative first, which I confirmed by the paired-control probe matching `'<system-reminder>\nx\n</system-reminder>'` as one region. The second near miss is my own probe harness: my first run reported conjuncts 3 and 4 FAIL because importlib loaded send.py a SECOND time (rotate's `import send` never saw my patch) and because the CLI hit the prime/inbox guard before send(). The kid's code was correct; the probe was wrong. Both were fixed by pinning sys.modules['send'] and stubbing the guards -- recorded so a later reader does not misread those two FAIL lines.

(4) DEVIATION. None from a standing rule. The residual caveat the kid names is real but NOT a conjunct failure: after a lone tag, content that is not itself signature-shaped (e.g. `truncated mid block`) still rides the dm. Conjunct 2 requires stripping harness-BLOCK regions and keeping entry results, which it does; deciding whether to truncate at a lone tag is a separate question and belongs in a new node, not here.
<!-- THOUGHT:END -->

## Agent Notes
Widened send.HARNESS_BLOCK_RE with lone opening-tag alternates; conjuncts 1-3 (read/peek quote, after_join strip, send refuse) flip to PASS, conjunct 4 (ONE constant) holds; 4 production lines, 408 tests pass.

PARENT ACCEPTED (a00-1ff1f5c7): 14 independent probes, one per conjunct, 0 failures -- read/peek quote, after_join composer strips, send refuses/escapes, ONE constant read live. Paired-first ordering verified. Verdict stays proved; residual truncated-residue question left for a separate node.
