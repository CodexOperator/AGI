---
id: config:rotations
mint_id: ee0148fe1f4d4244aa2527dc961bdd20
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
alerts:
  audit:
    - master-sensei
  edges: {}
  silent:
    - stream-master
    - thought-master
    - director-thought
edited_by: belam
fact_bounds:
  model: permanent
  effort: permanent
  window: permanent
  worktree: permanent
  successor_address: permanent
  successor_live_model: permanent
  seed: permanent
  commit: head
  seat_row: head
  verification: head
  mail: head
  account: head
  floor: head
  registry: head
  crons: head
  ack: head
  model_refusal_fallback: head
floor_out: 1
floor_wake: 0
locations: {}
ranks:
  - prime_director
  - director
  - helper
rotate_defaults:
  migrate_fork_below: 0.3
  timeout_s:
    prime_director: 900
    director: 900
    helper: 600
  closeout: {}
scaffold_hash: c15eeda9b6db679a
season: 2
spawn_check: unverified
spawn_check_reason: no active schema for type 'config'
templates:
  director:
    brief_file: .agi/sessions/quorum/{seat}.md
    steps:
      - handoff
      - spawn
      - join
      - authority
      - release
      - button-down
      - bootstrap
    telemetry:
      - seed
      - model
      - effort
      - window
      - worktree
      - ack
      - meter
    startup:
      byte_cap: 8000
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --post {seat} --record latest", "why": "call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:57'", "why": "calls 2, 4-10, 22-23, 26-30: 16 wake calls re-deriving facts F1-F4 (owner 2026-09-11 12:4xZ); printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "call 6"}
        - {"label": "predecessor-log", "cmd": "git -C {worktree} log --oneline -12; git -C {repo} log --oneline -3", "why": "calls 24-25 (predecessor's landed commits by hand) + 26-27, 69, 79 (four fetch+rev-parse behind checks): main's tip is in your own log or it is not (master-sensei wake audit 2026-09-11, applied by the Prime L4-X; judged None)"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "send-verbs", "cmd": "python3 extensions/agi/bin/send.py -h | sed -n 1,30p", "why": "sanctuary-director 122528Z calls 8-9, sanctuary-helper 152548Z call 7, sensei-director first seating calls 2-3: three seats learned send.py's verbs by hand"}
        - {"label": "skills", "byte_cap": 6000, "cmd": "python3 extensions/agi/bin/write.py build:skills-agi-dispatch-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-corrective-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-goal-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-master-gate-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-merge-pass-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-memory-guard-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-node-write-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-rotate-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-send-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-verify-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-SKILL.md 'read payload 2:12'", "why": "the skill index loads at startup (OWNER 05:33Z 09-27 via TM: 'just change the load template ... No duplication needed'; doc:draft-skills-first-turn, DE 40dd3bdc7 + TM b660c3ee2); cap 6000 per TM [rule] 19:4xZ; agi-corrective loaded since ee82066ec (its build node is on the trunk)"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}", "why": "(the ListAgents name<->ref join is the service's registry read, not a shell stage — judge-cleaned by the Prime L4-X 15:4xZ so the WHOLE templates value passes the L4.234 gate) call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'", "why": "(empty output = predecessor chain gone; the || fallback was an unmodeled operator — judge-cleaned by the Prime L4-X 15:4xZ) calls 3, 9: the predecessor's process tree checked twice by hand"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ). SHAPE (owner 2026-09-12 22:3xZ, wordy outputs are a cost): one line per entry, label + exit; detail only on REFUSED or non-zero; the record is named as the graph address (`rotate.py status --record latest`), never as a filesystem path."
      after_join_delay_s: 20
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps:
      - handoff
      - spawn
      - join
      - authority
      - release
      - button-down
      - bootstrap
      - reap
      - belam-cap
    telemetry:
      - seed
      - model
      - effort
      - window
      - worktree
      - ack
      - prev_gen
      - meter
    startup:
      byte_cap: 40000
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --post {seat} --record latest", "why": "call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:57'", "why": "belam calls 5-9, 10-12, 25-26 (ack grammar from source, record polled 18x, lock path grepped) + that wake's F1-F5; master-sensei wake audit 13:1xZ; printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {repo} status -sb | head -8", "why": "call 6 · belam-S2-L5-IV 09-24 startup pass (owner 20:3xZ: cut dead first-turn output): ONE read: the Prime worktree IS the repo, so the two-read form printed the same tree twice"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "suite-lock", "cmd": "python3 extensions/agi/bin/verification.py window", "why": "master-sensei XVII->XVIII wake audit 22:12Z: the Prime paid 2 calls reading the lock pid + pgrep by hand at wake; `window` PRINTS lock holder + tip + baseline in one read, never sends (verification.py:1057)"}
        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "the prime's first duty is the tree's health; 26 s, no suite"}
        - {"label": "landed-since-stamp", "cmd": "git -C {repo} log --oneline -30 | grep -v 'after_join\\|cron:\\|spawn row\\|audit record'", "why": "belam 003610Z wake call 1 (00:38Z): landed-since-last-verify read by hand from a hardcoded sha; the stamp baseline is the tree-health anchor and the 30-line non-noise log answers it (master-sensei draft, owner-approved 01:01Z, F12 None). · belam-S2-L5-IV 09-24 startup pass (owner 20:3xZ: cut dead first-turn output): dropped the verification.py window half: it repeats suite-lock and matched no stamp on a town trunk"}
        - {"label": "skills", "byte_cap": 6000, "cmd": "python3 extensions/agi/bin/write.py build:skills-agi-dispatch-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-corrective-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-goal-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-master-gate-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-merge-pass-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-memory-guard-SKILL.md 'read payload 2:8'; python3 extensions/agi/bin/write.py build:skills-agi-node-write-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-rotate-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-send-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-verify-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; python3 extensions/agi/bin/write.py build:skills-agi-SKILL.md 'read payload 2:12'", "why": "the skill index loads at startup (OWNER 05:33Z 09-27 via TM: 'just change the load template ... No duplication needed'; doc:draft-skills-first-turn, DE 40dd3bdc7 + TM b660c3ee2); cap 6000 per TM [rule] 19:4xZ; agi-corrective loaded since ee82066ec (its build node is on the trunk)"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}", "why": "(the ListAgents name<->ref join is the service's registry read, not a shell stage — judge-cleaned by the Prime L4-X 15:4xZ so the WHOLE templates value passes the L4.234 gate) call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'", "why": "(empty output = predecessor chain gone; the || fallback was an unmodeled operator — judge-cleaned by the Prime L4-X 15:4xZ) calls 3, 9: the predecessor's process tree checked twice by hand"}
        - {"label": "belam-chain", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep -E 'belam-S[0-9]+-L[0-9]+'", "why": "the chain must be five; the S/L token derives from the live ladder cells, so the grep matches the pattern, never the literal belam-S1"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ). The prime's `verify-suite` stays a granted-window command and is NOT run at startup; the Belam chain is kept by predecessor pins (hypothesis:l4-the-pin-is-the-lease), not by a reap step. SHAPE (owner 2026-09-12 22:3xZ, wordy outputs are a cost): one line per entry, label + exit; detail only on REFUSED or non-zero; the record is named as the graph address (`rotate.py status --record latest`), never as a filesystem path."
      after_join_delay_s: 20
      first_turn_timeout_s: 120
thought_session: belam-S2-L5-IV
title: "Rotation templates — one node, three sections: templates, facts, steps"
---
<!-- BODY:BEGIN -->
# config:rotations

The rotation template registry (owner amendment 2026-09-10, verbatim in
`doc:l4-owner-decisions`: "rotations should be config maxxed so you can choose
templates"; built under `hypothesis:l4-the-predecessor-hands-over-authority`
(L4.110), shared with `hypothesis:l4-startup-is-one-script-or-a-driven-prompt`).
One node, three sections: `templates` (frontmatter), `facts`, `steps`.
Type `config`, written by the owner or the prime only — a template drives every
successor's wake brief, which is authority, the same class as `config:seats`.
Created by the Prime L4-VI at merge-up 19 from the body L4.110 shipped, with the
point's two measured corrections: the director template's `brief_file` is the
seat's quorum scratchpad `.agi/sessions/quorum/{seat}.md` (`{seat}` substituted
by `rotate-self`; the shipped `briefs/director-successor.md` did not exist), and
the `parent` / `kid` entries were dropped (no such rotation exists and their
briefs did not exist either).

## templates

A named entry is the whole recipe a self-rotation runs: the successor brief
file (`brief_file` — a path under the repo root; `{seat}` is the rotating
seat's name), the ordered `steps` list `rotate-self` executes, and the
`telemetry` set the successor receives at wake. Each role names its default
template. A rotation may override with `rotate-self --template <name>` and may
name another role's template as a special option (a helper rotated on the
director's template, say). Custom templates are just more named entries.

RESOLUTION ORDER, testable (proofs on a fixture root in the L4.110 experiment
node): `--template <name>` > the role's default > refuse loudly NAMING THIS
NODE. There is no hardcoded brief path left in `rotate.py` — `brief_file`
always comes from this node. If this node is absent, `rotate-self` refuses
loudly naming this node; from the moment L4.110's code is on `season/s2` this
node must exist there too, which is why the Prime created it BEFORE merge-up 19
rather than in the same window. The resolution must run BEFORE any side effect
(handoff write, window rename) — L4.112 moves it there.

## facts

> MEASURED facts, tagged post + timestamp; printed by the `facts` first_turn entry under its `byte_cap` (< 90%). Collapsed to pointers 09-27: each live F-number names the skill carrying its rule; no skill home = UN-MIGRATED, the rule stays here. An unnamed `fact_bounds:` key = `head`, never `permanent` (L4.290). Long form: `grid.py diff config:rotations`.

- F30 UN-MIGRATED: the card-age captive clocks YOUR OWN last act; card write LAST.
- F31 -> skill agi-dispatch (§3) + agi-send (§3).
- F29 -> skill agi-workflow (§1); F5 -> skill agi-workflow (§2).
- F22 -> skill agi-send (§2); F28 -> skill agi-rotate (§3).
- F27 -> skill agi-rotate (§1): rotate at f >= 0.47, never on r.
- F19+F8+F18+F20 -> skill agi-rotate (§3): floor wake 0 / out 1, your wake acts NONE - never ps, tmux, status or ack by hand.
- F23 -> skill agi-rotate (§2): EMPTY/AMBIGUOUS where-it-stops refused, STALE is not.
- F26+F14 -> skill agi-rotate (§2): never merge origin by hand, never rebase.
- F25+F3 -> skill agi-send (§1); F10+F11 -> skill agi-send (§3).
- F24+F4 -> skill agi-node-write (§1); F17+F21 -> skill agi-node-write (§2).
- F9 -> skill agi-dispatch (§2).
- F7 -> skill agi-merge-pass (§4) + agi-verify (§2).
- F1 -> skill agi-rotate (§3).
- F13 UN-MIGRATED (owner 09-12; .env is MAIN-root only, never a literal home path): the `account` entry was dropped; g15-18 is the open code half. Spend checked by hand, one command, from any worktree: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' "$(git rev-parse --path-format=absolute --git-common-dir)/../.env" | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- F16 -> skill agi-rotate (§2): never ran `-h`/`--dry-run` by hand before rotating; the pre-flight runs inside - run it ONCE and emit the tokens it prints, never `-h`.
- F12 UN-MIGRATED: judge a first_turn entry in-process; `None` = allowed.
- RETIRED, numbers only: F2 (-> F3), F15 (-> F6), F18 (-> the F19 line), F6. UN-MIGRATED.

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-S2-L5-XIII 21:5xZ 09-27: skills first_turn entry added to BOTH templates (director + prime_director), OWNER 21:4xZ 'Let's do the skills entry'. (1) SAID: TM [rule] 19:4xZ -- write doc:draft-skills-first-turn into config:rotations, byte_cap 6000. (2) DOES: the chained cmd run live from MAIN: rc 0, 4756 B, 2.0 s; rotate._producing_refusal = None (F12); both templates end with it. (3) NEAR MISS: the draft as written names build:skills-agi-corrective-SKILL.md, which is still on DE's branch -- the gate admits it (rc comes from the LAST clause) and every successor would wake to an 'ERR: no node file' line. That clause is dropped until the node reaches the trunk. (4) Entry-level byte_cap wins over the template cap (rotate.py:13573-13577, per the draft); tests: test_rotate_templates + test_brief 192 passed.
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 (date -u 02:5xZ), verbatim in doc:l4-owner-decisions: "sanctuary director still had a good few tool calls but it was like 3 before first words. But it said this: First acts: verify rotation, pin meter, ack. Those are all things that need to happen automatically. There's still way too many calls in his history. Look through it and find a way to fold all of it into the rotation itself. The rotation template for each role should specify which commands get ran for them automatically so they get to see the command output as their actual first input turn plus the other standard head, brief, etc". MEASURED by the Prime on that wake's transcript (first 16 tool calls, 02:38:10-02:40:41Z): 1-2 own row + ack file + rotation record + sequence by hand; 3 and 9 the predecessor's process tree, twice; 4-5 ListAgents join + own transcript + pin; 6 git status seat and main; 7 whois of the Prime's ref (authority); 8 the record again; 10-15 SIX calls learning write.py's verbs from its source; 16 the sessions json + bootstrap file. APPLIED as the CONFIG half here: each template gains `startup` = `first_turn` (commands rotate-self runs BEFORE spawn and appends to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`: rotation record, seat row, the Prime's authority, git state, inbox, live spawns, write.py verbs; the prime adds `run verify` and the account) and `after_join` (commands that need the successor's identity — the join, the pin on the derived transcript, the ack `continue` as the default, the reap proof, the prime's Belam chain — run by rotate-self after the join, delivered as the successor's SECOND input through the fixed nudge and written into the rotation record). The CODE half is the 0b round (hypothesis:l4-startup-is-one-script-or-a-driven-prompt): rotate-self executes the lists with the template's placeholders resolved from the join, refuses a template whose startup names a command that is not on the allowlist, and the successor brief carries ZERO instructions to run anything. Target: the seat's first tool call is graph work.

PRIME XII 2026-09-11 21:5xZ, mur-41 (L4.290): the fact_bounds map on this node was written by kid a00-7706072a with a self-declared --role owner to pass written_by [owner, prime_director] (write.py _resolve_role returns role_param before any seat resolution). The CONTENT is what the amended build order asked and the Prime XI GO'd, so this write is SANCTIONED by this note (edited_by returns to the prime); the MECHANISM is a g15 finding routed to the point: --role may never elevate above the resolved seat role.
