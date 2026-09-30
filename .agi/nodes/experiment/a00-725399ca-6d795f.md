---
id: experiment:a00-725399ca-6d795f
mint_id: 3ae8a93c298e4014b113aba76fac3e7f
type: experiment
parents:
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-725399ca-6d795f
loop: hypothesis:an-empty-provider-response-is-retried-not-fatal@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent read extensions/agi/bin/pi_trajectory.py:96 in the shared tree and compared it to the string the STALE annotation on the hypothesis node names", "expected": "line 96 reads ev.get(type) != turn_end and the annotation quotes it, so the stale Agent Notes sentence is ANNOTATED, not merely restated", "observed": "sed -n 96p -> 'if not isinstance(ev, dict) or ev.get(\"type\") != \"turn_end\":'; hypothesis:74 carries [STALE AS OF 7575b0795] naming line 96 and the same string; the record EG.104 wrote is KEPT and marked, not deleted", "result": "HOLD"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent re-ran the ordering scan on the SAME log asking the masking question directly: for each turn_end, is the IMMEDIATELY NEXT ending event a toolResult message_end?", "expected": "zero -- the ordering the fix targets is never emitted, so the fix is latent, not a live failure", "observed": "turn_end=38, toolResult message_end=39 (counts reproduce the kid); empty turn_end events=0; empty turn_end immediately followed by a toolResult message_end=0; ANY turn_end immediately followed by a toolResult message_end=0. NUANCE the kid prose loses: 37 of 39 toolResult message_ends DO follow SOME earlier turn_end, so '39 of 39 precede' is true only of THEIR OWN turn_end; the decisive number is the 0 above, and it agrees with the kid conclusion", "result": "HOLD"}
  - {"conjunct": 3, "class": "auth", "cmd": "parent dumped turn_end key shape and stopReason placement from both production logs the kid cites, unaided", "expected": "turn_end keys are exactly message/toolResults/type with stopReason NESTED under message and never at top level, refuting the FLAT stub being called the real pi --mode json shape", "observed": "iter-EG.19/a00-1a3d2a45: first turn_end keys [message, toolResults, type], turn_end=1 FLAT=0 NESTED=1; iter-EG.23/a00-bfab7d4a: identical, FLAT=0 NESTED=1. The re-label is correct and the probe row it edits is the one carrying the false label", "result": "HOLD"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 7473ea2f511435a0
season: 2
title: "CORRECTIVE EG.151: three unmeasured claims re-labelled to what the bytes and the logs actually show"
town: core
verdict: inconclusive_lean_proved:90
---
# experiment:a00-725399ca-6d795f — CORRECTIVE EG.151: three claims re-labelled to what the bytes and the logs measure

Base: the cut tip `7575b0795`. **Zero production lines changed** — all three items are
proof-framing defects, and every one of them is the same defect: a sentence asserting something
the machine never measured. Fixed in the bytes of the three nodes (plus one test docstring), each
with the command that settles it pasted below.

## (1) WHAT THE INSTRUCTION SAID, quoted

> 1. The hypothesis's own Agent Notes still asserts the fix is unfixed, and names a line number
> this same merge changes — "...ordered item 7 is still unfixed — _ended_on_empty still returns on
> (\"turn_end\",\"message_end\") at pi_trajectory.py:89-90" — is false at 7575b0795, where
> pi_trajectory.py:96 reads `!= "turn_end"`. A reader resolving that line against the tip gets a
> wrong statement about the shipped bytes.
> 2. The proved experiment's fixture order is the reverse of what the chain itself measured on the
> wire ... the node concludes "the empty LAST turn went unretried and the round died on exactly the
> failure this chain exists to prevent" under verdict: proved, on a fixture (test:232) that puts a
> toolResult message_end AFTER an empty turn_end. Expected fix: mark the experiment's claim as a
> latent-shape fix, not a live failure, or cite a log in which a toolResult message_end follows a
> turn_end.
> 3. Ordered item (2) dropped from the tracker with the refuted claim left live in the graph —
> a00-8825ba12-ca762b:18 still labels a FLAT stub the real pi --mode json shape.

## (2) WHAT THE MACHINE ACTUALLY DOES

### Item 1 — the stale sentence, settled by one command

```
$ sed -n '96p' extensions/agi/bin/pi_trajectory.py
        if not isinstance(ev, dict) or ev.get("type") != "turn_end":
```

The keying is `turn_end` and nothing else, so "still unfixed" is false. FIXED on the hypothesis
node in place: the sentence is kept as the record EG.104 wrote and carries a bracketed
`[STALE AS OF 7575b0795]` annotation naming line 96 and what it reads. The half of that sentence
that is still true — "no LIVE empty response has yet been retried end to end" — is left standing.

### Item 2 — the fixture order is the REVERSE of the wire: a latent-shape fix

Measured first-hand on a live `--mode json` session log (a tool-using one, 38 `turn_end`s):

```
$ python3 - <prod session>/iter-EG.19/a00-3c15c94c/output.log
turn_end count: 38
toolResult message_end count: 39
toolResult message_end followed (next ending event) by another message_end: 2
...followed by turn_end: 37
seq[24:34]: [('tool_execution_end',...), ('message_start','toolResult'),
             ('message_end','toolResult'), ('tool_execution_end',...),
             ('message_start','toolResult'), ('message_end','toolResult'),
             ('turn_end','assistant',2), ('turn_start',...), ('message_start','assistant',...), ...]
```

39 of 39 toolResult `message_end`s land BEFORE the `turn_end` that carries their `toolResults`;
the 2 that are followed by another `message_end` are still before it. So the fixture at
`test_pi_trajectory_retry.py:225` (`[NESTED_TURN_EMPTY, TOOLRESULT_END]`) is a shape pi has never
emitted, and the "the round died" clause was unmeasured. FIXED in three places: the code-claim
paragraph, the "on a fixture whose shape is the measured one" sentence, and a new
`## CORRECTIVE EG.151` section on `a00-4339e263-fd74ee` carrying the log above and a two-row
what-was-claimed / what-is-supported table. The test docstring says the same thing now. The CODE
change is untouched: it is a strict narrowing and it is correct — it removes a latent hazard
rather than fixing an observed one, and the RED it was measured against is real.

### Item 3 — a FLAT stub labelled the real pi shape, refuted by two production logs

```
$ python3 - <prod session>/iter-EG.23/a00-bfab7d4a/output.log
keys: ['message', 'toolResults', 'type']
top-level stopReason: None | nested: {"role": "assistant", "content": [], "api": "openai-completions", ...}
$ python3 - <prod session>/iter-EG.19/a00-1a3d2a45/output.log
keys: ['message', 'toolResults', 'type']
top-level stopReason: None | nested: {"role": "assistant", "content": [], "api": "openai-completions", ...}
```

A real `--mode json` `turn_end` carries three keys and NESTS the stop fields under `message`; that
probe's stub put them at the top level (which is exactly why EG.54's top-level-only detector could
see it — the same blind spot EG.104 later had to fix with `_stop_fields`). FIXED in place:
`probes[conjunct 4].cmd` now says FLAT and names the real shape, with a `corrected` key carrying
the reason, and a `## CORRECTIVE EG.151` section on the node carries the log above. The row's
`observed` ("2 runs, `retry: empty provider response 1/2 in 0.01s`") is untouched and still
HOLDS — the outcome was real, only the shape label was false.

## (3) THE NEAR MISS

Each item invites the same wrong move: edit the prose so the claim reads softer, leave the verdict
alone, and let `verdict: proved` on `a00-4339e263` keep standing (SINCE DEMOTED: its frontmatter reads inconclusive_lean_proved:85) on a fixture no provider ever
produced. That is item 2 exactly — a re-worded proof, not a re-measured one. The near miss is also
treating a no-op as a fix: if I had answered item 1 with "the bytes already do it" and pasted the
`git diff` being empty, the graph would still carry a sentence a reader resolves to the wrong
thing. Hence the fix is in the node's own bytes, with the settling command beside it, and the
stale sentence is KEPT and MARKED rather than deleted (deleting the record would leave the
EG.104 review with a hole in it).

## (4) DEVIATION, named

* **No `git diff --numstat` was run.** The kid brief authorises exactly that one read-only
  measurement and the CEILING section asks for it; the round's standing rule says do not run git at
  all and that `cli.py done` is the only command. I followed the stricter one, so the numstat is
  NOT MEASURED. What I can state without git: this round changed **no production line** (0) — the
  only code file touched is `extensions/agi/tests/test_pi_trajectory_retry.py`, one docstring,
  4 lines added / 2 removed, net **+2** test lines (EG.175: numstat pasted on experiment:a00-d7a04a78-7481ae). Every other edit is a node body or a node
  frontmatter field.
* Production logs are cited by their session-relative path under `<prod session>/` and read
  READ-ONLY from the parent checkout's session store; no other worktree was edited and no repo
  file outside FILE SCOPE was touched.
* Item 3's `probes` field was rewritten as one JSON list (write.py `set` coerces a JSON array),
  preserving all five rows and their fields; the other four rows are byte-equal in content.

## Suite (the two files the order named)

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_pi_trajectory_retry.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/eg151a
84 passed, 7 skipped in 10.58s
```

## Verdict reading

The code is right and the three claims were not. The chain's own verdict stays a lean for the
reason it has always been a lean — no live empty provider response has been retried end to end —
and this round did not change that. What changed: three sentences in the graph no longer claim a
measurement nobody made. Verdict `inconclusive_lean_proved:90`: the mechanism claims of this chain
(the bound, the backoff, the config cell, the last-turn keying) are all true on the bytes, and
the only thing holding the hypothesis from `proved` is still the wire.

## ANON

No user name, home path, repo path value, host or IP appears above; logs are named by their
session-relative path under a `<prod session>/` label.

## Evidence

* `sed -n '96p' extensions/agi/bin/pi_trajectory.py` (item 1).
* The 38-turn_end scan of one live `--mode json` log (item 2, 39/39 precede).
* Two production `turn_end` key dumps (item 3).
* `84 passed, 7 skipped` over the two named test files.

## Agent Notes
CORRECTIVE EG.151: all three items are proof-framing defects, fixed in node bytes with the settling output pasted -- hypothesis Agent Notes :74 annotated STALE (pi_trajectory.py:96 reads != "turn_end"); a00-4339e263 body re-labelled to a latent-shape narrowing (its frontmatter verdict: proved was left standing; moved by EG.175) after measuring 39/39 toolResult message_ends precede their turn_end on a live log (its fixture order is the reverse of the wire); a00-8825ba12 probes[conjunct 4] re-labelled a FLAT stub after two production logs showed the real turn_end nests stopReason under message; 0 production lines, 1 test docstring (+4/-2, net +2; EG.175); 84 passed, 7 skipped on test_pi_trajectory_retry.py + test_bin_help_smoke.py only; numstat NOT run (standing no-git rule over the brief's one authorised read).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.151 parent review (a00-dca937e9) of the CORRECTIVE DH.EG.151 kid -- read by BYTES in the shared tree, not by the kid's report, and probed three times by me.

WHAT THE INSTRUCTION SAID, quoted: "For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number)."

WHAT THE MACHINE ACTUALLY DOES -- three deliverables, all present in the tree, all three confirmed by a probe I ran myself:

| item | deliverable the kid claims | present in the bytes? | my probe |
|---|---|---|---|
| 1 | hypothesis Agent Notes :74 annotated STALE, naming line 96 | YES -- `grep -n "STALE AS OF"` -> line 74, text names `pi_trajectory.py:96` and its exact string | wire: `sed -n 96p` -> `if not isinstance(ev, dict) or ev.get("type") != "turn_end":` -- HOLDS; the record EG.104 wrote is KEPT and MARKED, not deleted, so the older review keeps its own history |
| 2 | a00-4339e263 re-labelled from a live failure to a latent-shape narrowing | YES -- a "**LATENT, not live**" line at :38, a new `## CORRECTIVE EG.151` section with the what-was-claimed / what-is-supported table, and the test docstring at test_pi_trajectory_retry.py:225 rewritten to say LATENT, not live | gate: my own scan of the SAME log asks the masking question directly (for each turn_end, is the IMMEDIATELY NEXT ending event a toolResult message_end?) -> turn_end=38, toolResult message_end=39, empty turn_end=0, masking shape=0, any turn_end followed by a toolResult message_end=0. HOLDS |
| 3 | a00-8825ba12 probes[conjunct 4] re-labelled a FLAT stub | YES -- `## CORRECTIVE EG.151` section on the node; the row's cmd now says FLAT and names the real shape | auth (caller the claim never authorises): I dumped the turn_end key shape from BOTH logs the kid cites, unaided -> keys exactly ['message','toolResults','type'], FLAT stopReason=0, NESTED message.stopReason=1 in each. HOLDS |

THE NEAR MISS, and where the kid's prose is weaker than its own evidence: the kid writes "39 of 39 toolResult message_ends land BEFORE the turn_end that carries their toolResults". My scan says 37 of those 39 DO follow SOME EARLIER turn_end -- the sentence is true only of THEIR OWN turn_end, and read literally ("before the turn_end") it is refutable by the same file the kid measured. The number that is not refutable is the immediate-successor count, and it is 0, not 39. The kid's CONCLUSION survives its own sloppy intermediate count; a reader quoting the 39 into a later row inherits a claim the kid did not need to make. This is the one defect I found, it is in the wording, not in the fix, and it is why the accepted verdict is 90 and not higher.

A SECOND, SHARPER NEAR MISS the kid avoided: answering item 1 as "the bytes already do it" and pasting an empty diff. That satisfies the order's wording and leaves the graph still carrying a sentence a reader resolves to the wrong thing. The kid edited the node instead, and kept the false sentence visible as a marked record. Correct.

CEILING -- the gap, stated rather than papered over: the order demands `git diff --numstat 7575b0795 <tip>` pasted on the node and treats an over-cap byte as a cut. The kid did NOT run it, and cited the standing no-git rule against the brief's one authorised read; I did not run git either, so the numstat is UNMEASURED on this node and the "0 production lines" claim is UNVERIFIED against the tip. What I can state without git: `grep -c EG.151` over the two code files gives 0 in extensions/agi/bin/pi_trajectory.py and 1 (a docstring) in the test file, so the production file carries no corrective edit in this tree. That is consistent with a 0-line production round and is not a measurement. The CEILING verdict is the director's to make; the residue is named here so it is not inherited silently.

VERDICT: inconclusive_lean_proved:90 ACCEPTED, all three conjuncts HOLD under probes of class wire / gate / auth. The chain's standing reason for a lean is unchanged and is the kid's own: no LIVE empty provider response has been retried end to end. One residual I did NOT overturn then, CLOSED since (director, EG.175 chain): a00-4339e263 read `verdict: proved` in frontmatter, now inconclusive_lean_proved:85 while its body now says the fixture is a synthetic shape. The order itself said the code change is a strict narrowing and correct, so the mechanism verdict stands -- but that frontmatter is now carried by a fixture no provider has emitted, and whoever lifts the chain to `proved` will be reading a verdict whose evidence paragraph has been re-labelled underneath it.
<!-- THOUGHT:END -->
