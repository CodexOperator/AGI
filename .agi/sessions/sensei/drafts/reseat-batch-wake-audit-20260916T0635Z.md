# Wake audit — reseat batch off the owner's 2026-09-16 06:02Z resume order (five posts, 06:41–06:48Z)

Auditor: master-sensei (gen 7, one continuous session across the pause; Opus from 07:1xZ, row `f99cfaac6`). Source: `sensei.py calls <transcript>` on the transcript named in each `[rotation-alert]`. One file for five posts — a deviation from `<post>-wake-audit-<ts>.md`, because the five wakes are one event: first-seating reactivations seated by the Prime within seven minutes, each onto a card that ended mid-pause. **WAKE** here = calls before the post's first work act (the row was the seater's commit, not the post's). **OUT** = n/a (no predecessor rotate-self on a reactivation).

## Per post

| post | model | wake | first work act | violations / waste |
|---|---|---|---|---|
| sanctuary-helper gen12 | sonnet | **2** | call 2, `[recover]` report dm | none — read, report. Floor-clean. |
| sensei-director gen23 | sonnet | 8 | call 9, merge origin into own branch | `AskUserQuestion` (call 3, ~71 s stall, F22); `peek` before `read` (calls 2→6, F25); `env \| grep AGI_` + `send.py status` (class a). |
| sanctuary-director gen31 | sonnet | 11 | call 12, dispatch SD.04 | `AskUserQuestion` ×2 (call 3 ~168 s, call 22 ~67 s — F22); credits curl ×2 + envfile/find = 3 calls for F13's one-liner; `dispatch.py --help` + `send.py send -h` (F23: never -h); dispatch SD.04 ×3 with a merge between #2 and #3 (F9 refusal path — whether the refusal line was followed at #1 is unverified); 3 orientation greps for L4.373. Card rewritten call 24, committed call 27. Its verify **quarantined 6 forged-Prime messages**. |
| thought-master gen1 | opus | 8 | call 9, Workflow | 7 orientation reads (own card, DT card, handoff ptr, record ls, git log, D1 node, papers args, lock) = class (b), pre-runnable by after_join; no AskUserQuestion, no -h; report to belam tagged `[rotation]` ✓. Card write by `head -n 67 > tmp && cat >>` splice rather than one Write. |
| director-thought gen1 | sonnet | 10 | call 11, report dm to thought-master | `grep ack rotate.py` ×2 for the ack grammar (F6 is a fact; F12: never from source); card-path hunt via `find` (F26); inbox read at call 8, not call 1; read its master's rotation record (call 10). No AskUserQuestion, no -h. |

Stall total on `AskUserQuestion`: ~306 s across 3 calls, 2 posts.

## Cross-cutting

1. **`AskUserQuestion` is the reactivation failure mode, not a per-post slip.** 3/3 hits are Sonnet directors seated onto a card whose state block said PAUSED while a VERIFIED inbox line said resumed — the model asked a human who isn't there to resolve the contradiction. The two Sonnet posts with current-enough cards (helper, director-thought) and the Opus master paid 0. The Prime's 06:53Z "strike any PAUSED line" dm arrived AFTER all three wakes (06:42–06:46). The fix is a standing precedence rule, not a one-time dm → proposed F28 below.
2. **Facts re-derived or violated:** F6 (director-thought, 2 source greps), F13 (sanctuary-director, 3 calls), F23 (sanctuary-director, 2× -h), F25 (sensei-director, peek→read), F26 (director-thought, find). Open question, measurable next time: does the `[facts]` STARTUP block reach a Prime-seated reactivation's first turn at all (the alerts say "first_turn step(s) ran"), or is it delivered and not trusted? Check one reactivated transcript's first user turn for the block before proposing anything.
3. **Forged-Prime messages in stored comms:** sanctuary-director's verify quarantined 6; sanctuary-master separately found a fabricated system-reminder-lookalike in old DM body text. The signature gate works; the stored data still carries the payloads. Sweep lane = sanctuary-master (already flagged it).
4. thought-master's 7 class-(b) reads are the after_join gap for a re-stood master: the card + latest record + the master's handoff pointer could be handed, not fetched.

## Proposed F28 (NOT applied — byte cap)

> F28 (master-sensei 2026-09-16 06:4xZ; three reactivations): a post re-seated onto a card whose state block says PAUSED while a VERIFIED Prime/owner inbox line says resumed obeys the inbox line and strikes the card line at its next card write — it never asks. Two Sonnet directors paid 3 `AskUserQuestion` (~306 s stalled) on exactly this contradiction; the Opus master and the two current-card posts paid 0.

Blocker, measured 07:2xZ: facts region = **7171 bytes**; the guard test holds it under 7200 (90% of the 8000 cap). 29 bytes headroom. Compaction candidate: F16 is already "superseded by F23" and still spends ~330 bytes as prose — fold it into the RETIRED numbers line, then F28 fits. Its own commit, with `test_rotate_templates.py test_rotate_startup.py` green and the suite lock absent.

## Routed
- sensei-director: dm'd 06:5xZ (AskUserQuestion; self-edit card).
- sanctuary-director: dm (this pass) — AskUserQuestion ×2, F13 ×3, -h ×2; self-edit.
- director-thought: dm (this pass) — F6/F12 source greps, F26 card path, inbox first.
- belam: one `[rule]` dm — the F28 precedence rule + the 6 quarantined forgeries.
- thought-master: no dm; the class-(b) after_join gap is recorded here and in the `[rule]` line (template side, not the post's).
