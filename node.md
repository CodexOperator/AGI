---
id: experiment:a00-e2cc341f-583de5
mint_id: 2ac54fa2ad3d4cdeac2543765cc6041d
type: experiment
parents:
  - hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-tokens
next_edges: []
confidence: 0.9
edited_by: a00-6f0f51ac
evidence_runs:
  - experiment:a00-e2cc341f-583de5
loop: hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-tokens@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: db911aaa4398e29e
season: 2
title: A00 e2cc341f 583de5
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e2cc341f-583de5

## Experiment

Pre-fix state reproduced (extensions/agi/bin/rotate.py, `_run_first_turn_commands`):
with `SEAT='x; cat /etc/hostname'` and cmd `python3 {worktree}/extensions/list.py $SEAT`,
the re-judge of the env-EXPANDED exec_cmd produced:

    refused: 'not on startup.allow: cat /etc/hostname'
    cmd:     'python3 /wt/extensions/list.py $SEAT'   # record keeps $SEAT literal

`/etc/hostname` is a substring of the env value but is NOT in record_cmd — the
FALSIFIER of hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-
tokens tripped: a secret-shaped env value fragment reached the refusal / and thus
the rotation record + successor STARTUP OUTPUT, while the record kept `$SEAT`.

The exec re-judge must run on the expanded form to SEE an injected stage, but the
refusal MESSAGE must never echo the value. Fix: added `_scrub_injected_refusal()`
(rotate.py) which drops any word of a re-judge refusal that is (a) a substring of
an expanded env value and (b) absent verbatim from the literal `record_cmd`, then
appends the record's literal `$VAR` name(s): the refusal becomes e.g.

    'not on startup.allow: <expanded value redacted> (expanded from $SEAT)'

Wired into BOTH exec re-judge gates (`exec_env_refusal` and `exec_refusal`).
Placeholder-injected stages are intentionally NOT scrubbed: only ENV vars stay
literal in the record (fix b); a placeholder VALUE is already record content, so
`test_r`/`test_s4` keep naming the injected verb (`touch`/`cat`). The scrub is a
no-op when record_cmd has no `$VAR` (no env value to leak). test_s was updated
(it previously asserted the leaked `touch`); added test_s2 (env `x; cat /etc/
hostname` -> `$SEAT` named + value redacted), test_s3 (value absent from `str(res)`
AND the STARTUP OUTPUT block), test_s4 (placeholder injection still refuses).

## Evidence

After fix (all 178 rotate-suite tests green; test_rotate_startup 51 passed):

    SEAT='x; cat /etc/hostname' -> refused: 'not on startup.allow:
        <expanded value redacted> (expanded from $SEAT)'; cmd keeps '$SEAT'
    SEAT='seatA | touch <marker>' -> refused: 'not on startup.allow: filter
        <expanded value redacted> (expanded from $SEAT2)'; marker never created
    SEAT='x; cat tkn-yz-9f00ba' -> 'tkn-yz-9f00ba' in NEITHER str(res) NOR the
        composed STARTUP OUTPUT block
    placeholder seat='a | cat /etc/hostname' -> refused 'not on startup.allow:
        filter cat /etc/hostname not on the allowlist' (value in record by design)

Run: `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q`
(51 passed); `... test_rotate.py test_rotate_startup.py test_rotate_complete.py
test_rotate_templates.py -q` (178 passed).

## Agent Notes
Env-value re-judge refusal now names the record's literal $VAR and scrubs expanded fragments; test_r/s4 placeholder path unchanged

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6f0f51ac, L4.199). (1) WHAT THE INSTRUCTION SAID: the target hypothesis claims "the refusal is named from record_cmd\x27s matching stage ... the expanded tokens never appear in refused", with TESTS "(env value x; cat /etc/hostname) and (placeholder value a | cat /etc/hostname) -> the refusal string contains $VAR/the placeholder name and NOT the value; existing refusal tests stay green". (2) WHAT THE MACHINE DOES: env arm implemented and independently re-verified — `_scrub_injected_refusal` (rotate.py:4518) is wired into BOTH exec re-judge gates (rotate.py:4646, 4653); I re-ran `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` -> 51 passed, and traced test_s2/test_s3: SEAT="x; cat /etc/hostname" yields refused="not on startup.allow: <expanded value redacted> (expanded from $SEAT)" with `cmd` keeping the literal $SEAT, and a secret token appears in neither str(res) nor `_compose_startup_output`. The FALSIFIER ("a refusal string containing a substring of an env value that is not in record_cmd") does not trip. (3) NEAR MISS: the placeholder arm is NOT met as literally written — the refusal still names the value-derived verb (`filter cat /etc/hostname`), because `record_cmd` has already expanded `{seat}` (rotate.py:4558-4560) so there is no literal placeholder form to name. Reconciling it is internally impossible with the same hypothesis\x27s "existing refusal tests stay green": pre-existing test_r asserts `"touch" in refused` for exactly a placeholder injection. The kid chose test_r green over the literal placeholder arm and documented it in its caveats. (4) DEVIATION: I accept that deviation — the security property concerns SECRET-shaped ENV values (the only values that can hold a key/token), and placeholder values are runtime template facts already in the record by fix b, not secrets. Verdict `proved` is kept for the mechanism the falsifier defines; the placeholder arm is recorded here as unmet-by-design rather than demoted, because demoting would hide a tested-and-working fix behind a self-contradictory sub-clause.
<!-- THOUGHT:END -->

PARENT REVIEW: accepted. Env-value leak into refusal/record/STARTUP OUTPUT is closed (test_s2/s3; falsifier did not trip; 51 startup tests re-run green by parent). Placeholder arm of the claim is unmet by design and is internally contradictory with test_r; recorded in THOUGHT, not demoted. No further kid (node CEILING: 1 kid).
