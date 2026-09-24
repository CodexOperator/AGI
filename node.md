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
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:64'", "why": "calls 2, 4-10, 22-23, 26-30: 16 wake calls re-deriving facts F1-F4 (owner 2026-09-11 12:4xZ); printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "call 6"}
        - {"label": "predecessor-log", "cmd": "git -C {worktree} log --oneline -12; git -C {repo} log --oneline -3", "why": "calls 24-25 (predecessor's landed commits by hand) + 26-27, 69, 79 (four fetch+rev-parse behind checks): main's tip is in your own log or it is not (master-sensei wake audit 2026-09-11, applied by the Prime L4-X; judged None)"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "send-verbs", "cmd": "python3 extensions/agi/bin/send.py -h | sed -n 1,30p", "why": "sanctuary-director 122528Z calls 8-9, sanctuary-helper 152548Z call 7, sensei-director first seating calls 2-3: three seats learned send.py's verbs by hand"}
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
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:64'", "why": "belam calls 5-9, 10-12, 25-26 (ack grammar from source, record polled 18x, lock path grepped) + that wake's F1-F5; master-sensei wake audit 13:1xZ; printed by body range until 0b-b's facts emitter lands"}
        - {"label": "point-record", "cmd": "python3 extensions/agi/bin/rotate.py status --post sanctuary-director --record latest", "why": "belam 140328Z calls 15-16: the point's record read twice by hand; the Prime's first question after its own state is the point's (seat name hardcoded like belam-chain's belam-S1; master-sensei, applied L4-X)"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "call 6"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "suite-lock", "cmd": "python3 extensions/agi/bin/verification.py window", "why": "master-sensei XVII->XVIII wake audit 22:12Z: the Prime paid 2 calls reading the lock pid + pgrep by hand at wake; `window` PRINTS lock holder + tip + baseline in one read, never sends (verification.py:1057)"}
        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "the prime's first duty is the tree's health; 26 s, no suite"}
        - {"label": "since-last-rotation", "cmd": "git diff --stat", "why": "belam calls 13-15: what changed in the tree since the last wake, read by hand (master-sensei draft, judged None; the inbox half was already the inbox entry)"}
        - {"label": "landed-since-stamp", "cmd": "python3 extensions/agi/bin/verification.py window | grep -oE 'stamped sha=[0-9a-f]+'; git -C {repo} log --oneline -30 | grep -v 'after_join\\|cron:\\|spawn row\\|audit record'", "why": "belam 003610Z wake call 1 (00:38Z): landed-since-last-verify read by hand from a hardcoded sha; the stamp baseline is the tree-health anchor and the 30-line non-noise log answers it (master-sensei draft, owner-approved 01:01Z, F12 None)."}
        - {"label": "owner-decisions-tail", "cmd": "python3 extensions/agi/bin/write.py doc:l4-owner-decisions 'read body 860:'", "why": "belam 003610Z wake calls 3+6 (00:42-43Z): the owner-decisions node ls-hunted then tail-read by hand; the Prime appends an owner quote every session, so its tail is owed at wake (owner-approved 01:01Z). The open range clamps to the end; bump 860 as the doc grows."}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}", "why": "(the ListAgents name<->ref join is the service's registry read, not a shell stage — judge-cleaned by the Prime L4-X 15:4xZ so the WHOLE templates value passes the L4.234 gate) call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'", "why": "(empty output = predecessor chain gone; the || fallback was an unmodeled operator — judge-cleaned by the Prime L4-X 15:4xZ) calls 3, 9: the predecessor's process tree checked twice by hand"}
        - {"label": "belam-chain", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep -E 'belam-S[0-9]+-L[0-9]+'", "why": "the chain must be five; the S/L token derives from the live ladder cells, so the grep matches the pattern, never the literal belam-S1"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ). The prime's `verify-suite` stays a granted-window command and is NOT run at startup; the Belam chain is kept by predecessor pins (hypothesis:l4-the-pin-is-the-lease), not by a reap step. SHAPE (owner 2026-09-12 22:3xZ, wordy outputs are a cost): one line per entry, label + exit; detail only on REFUSED or non-zero; the record is named as the graph address (`rotate.py status --record latest`), never as a filesystem path."
      after_join_delay_s: 20
      first_turn_timeout_s: 120
thought_session: master-sensei
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

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b): the bootstrap facts printed by the `facts` first_turn entry under an 8000-byte cap (guard: < 90%). MEASURED facts only, tagged post + timestamp. Compacted 09-13, 09-16; long form: `grid.py diff config:rotations`.

> Staleness bound (L4.290): a fact the `fact_bounds:` map does not name defaults to `head` and is marked stale when its measured commit differs from HEAD; `permanent` is never marked. Written by `write.py`, never by hand.

- F30 (SM 16:05Z; SM.48+48b `68abd19e8`): the card-age captive clocks YOUR OWN last act (`last_act.py`: write.py --actor, send.py send, dispatch, session-complete, merge-up) — another post's commit never stales you; gate (b) fires only on a real MERGE_HEAD or a live suite lock. Card write LAST still holds.
- F31 (SM 16:08Z; SM.46 120/20, SM.48 220/60 self-authorised in-node): a parent that answers a kid's `rebrief_request` in-node dms its director the answer line (kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes — a kid past 2× with no such dm in your inbox = self-authorised: cut it.
- F29+F5 (thought-master 2026-09-16; `settings: ultracode` on 5 rows): the keyword lands in your first turn and the harness says 'use the Workflow tool' every turn — NOT the route here. Workflows run by NAME: `workflow.py run <name>` — pi by default (OWNER 19:1xZ), never the Claude Workflow tool for a review, on any post. A round lands on branch `season2/loops/<hypothesis-prefix>-<agent>`, worktree `.agi/worktrees/<agent>/`; diff against the MERGE-BASE with the post branch, never a moved tip; kid experiment nodes under `.agi/nodes/experiment/` there; `cli.py session-complete <iter> --dry-run` first. One mur round per KID slice — `rounds[]` is the parallel axis (SM 19:23Z: a 15-item round timed out at 1800 s).
- F22+F28 (director-point 01:22Z; 3 asks ~306 s on 09-16): the pane has NO interactive user — never `AskUserQuestion` or any tool that waits for a human. Trigger: card says PAUSED + a VERIFIED Prime/owner line says resumed → the inbox line wins; strike the card line at the next write. Decide under delegated authority; record the deviation (THOUGHT or card); bank owner-only questions in BANKED.
- F27 (director-point 09-12, three rotations at 0.32/0.23/0.22): the meter hook prints `<f> of the window = <r> of the line`; ONLY `f` is compared to `line=0.47` (`r = f/0.47` hits 1.0 at the line). Rotate when `[meter] post=<post> <f>` reads f ≥ 0.47, never on r.
- F19+F8+F18 (OWNER 09-12 03:2xZ): floor = wake 0 / out 1. The predecessor's rotate wrote your meter pin and your row (committed) and answered the ack `continue` for you. YOUR WAKE ACTS: NONE — no ListAgents, ack, push, status read, `ps` or `tmux`. Only an `ack … diff` line printed in STARTUP is one call. `posts row dirty before this ack` = someone else's row change in your tree: commit or drop THAT, never bundle.
- F23 (2026-09-13): the out-line is bare keyed `python3 extensions/agi/bin/rotate.py rotate` — every value from the row + key; no flag to verify, never `-h`; an EMPTY or AMBIGUOUS where-it-stops slot is refused, a STALE one is NOT (two handed on 09-16): write + stamp the slot BEFORE the window ask or the dispatch at the line, never after. Merge + prepare run inside it (F14): never merge origin by hand ahead of it, never rebase.
- F26 (three directors, 09-12/13): your card is `.agi/sessions/quorum/<post>.md` in YOUR worktree; `HANDOFF.md` at the repo root is the engine's — never read it before rotating. Write the card wholesale (one Write), commit by exact path.
- F25 (director-sanctuary 13:49-14:38Z, 8/8 nudges): a nudge is consumed by ONE `send.py read <post>`; `peek` never flips the marker (the nudge re-fires). Never peek before read. Phantom = `read` returns empty: one read, nothing else.
- F24 (13:4xZ): write.py script = `<verb> <args>` units joined by ` && ` in ONE single-quoted script: `read body N:M` (range REQUIRED), `set <field> <rest of unit>`, `note <text>`, `thought <text>`, `replace body N:M <file>`; `--dry-run` shows the edit; `-h` is already in STARTUP [write-verbs]; pass `--actor <post> --role <role>` (F4).
- F20 (SL7.55): a successor NEVER commits rotation records, `sequence.json` or `.agi/comms/**` at wake — the predecessor's rotate commits its own record; comms churn is cron-owned.
- F17 (director-sanctuary first seating): node-type schemas are `.agi/context/schemas/[type].md` (brackets in the name); `write.py create <type> <slug> --parent <id>` runs the spawn gate against it; `config:*` nodes are `.agi/nodes/.geometry/<name>.md` (F21): `write.py config:<name> 'read body N:M'`, never ls/find.
- F14 (director-review 15:25Z): rotate reads `config:rotations` + `config:posts` from the ROTATING POST'S WORKTREE and merges `origin/season2/main` into it itself — a post rotating unmerged seats its successor on a stale template.
- F13 (belam 09-12; ABSOLUTE path, SM 09-16 — .env is MAIN-root only): the `account` entry was dropped; g15-18 is the open code half. Spend by hand, one command: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- F16 (director-point + director-review 09-12 — every worktree post ran `rotate-self -h` then `--dry-run` by hand before rotating): superseded by F23's bare `rotate`, whose pre-flight runs inside — run it ONCE and emit the tokens it prints; never `-h`, never `--dry-run | head` (its head is the prayers).
- F12 (belam 14:03Z): judge a first_turn entry in-process, never from source — `sys.path.insert(0,'extensions/agi/bin'); import rotate as r; r._producing_refusal(r._resolve_startup_placeholders(CMD, {'seat': S, 'worktree': W, 'repo': R}, refuse_empty=True))` — `None` = allowed.
- F10+F11 (2026-09-11; gate f16f87964): STARTUP already ran live-spawns, git-state, inbox and the record (F19). Prime channel: `send.py send belam '[tag] <one line>'`, tag ∈ merge-up/decision/rotation/red/rule/complete/owner — untagged = REFUSED before any write.
- F9 (2026-09-11): a dispatch from a post behind `origin/season2/main` refuses with exit 3 — that refusal IS the behind check; no fetch+rev-parse by hand.
- F7 (belam 2026-09-11): the suite lock is `.agi/sessions/verify-suite.lock`; "lock FREE" for a merge-up window = absent in main AND every post worktree.
- F3 (2026-09-11; SL7.96): the successor's row is joined by `session_name` (registry name, e.g. agi-d7); `send.py whois <token>` resolves session_ref OR session_name, never the uuid. A worktree post's row reaches main at its next merge-up (`whois` NO-MATCH before that).
- F1 (2026-09-11): the predecessor's wrapper reaps its own chain and writes the record `success` ~60 s after the join; STARTUP's record reads `started` by construction; the after_join `[reap-proof]` line proves the reap — never `ps`/`tmux` for it.
- RETIRED (superseded, kept as numbers only): F2 (row back-fill → F3), F15 (bare ref → F6), F18 (→ F19 line), F6 (ack grammar: STARTUP prints the exact `ack … diff` line when one is owed).

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 22:5xZ) ahead of merge-up 19, because L4.110's rotate.py refuses every rotate-self while this node is absent: creating it before the code lands decouples the two and keeps every seat rotatable in between. Body and templates are L4.110's shipped extensions/agi/briefs/rotations.geometry.md with the point that wake's two measured corrections (director brief_file = the quorum scratchpad with {seat}; parent and kid entries dropped). The file was moved from nodes/config/ to nodes/.geometry/ because that is the address rotate.py resolves (same as config:seats); the mint id is unchanged. spawn_check unverified is the gate's honest stamp: it found no active spawn rule for type config.
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 (date -u 02:5xZ), verbatim in doc:l4-owner-decisions: "sanctuary director still had a good few tool calls but it was like 3 before first words. But it said this: First acts: verify rotation, pin meter, ack. Those are all things that need to happen automatically. There's still way too many calls in his history. Look through it and find a way to fold all of it into the rotation itself. The rotation template for each role should specify which commands get ran for them automatically so they get to see the command output as their actual first input turn plus the other standard head, brief, etc". MEASURED by the Prime on that wake's transcript (first 16 tool calls, 02:38:10-02:40:41Z): 1-2 own row + ack file + rotation record + sequence by hand; 3 and 9 the predecessor's process tree, twice; 4-5 ListAgents join + own transcript + pin; 6 git status seat and main; 7 whois of the Prime's ref (authority); 8 the record again; 10-15 SIX calls learning write.py's verbs from its source; 16 the sessions json + bootstrap file. APPLIED as the CONFIG half here: each template gains `startup` = `first_turn` (commands rotate-self runs BEFORE spawn and appends to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`: rotation record, seat row, the Prime's authority, git state, inbox, live spawns, write.py verbs; the prime adds `run verify` and the account) and `after_join` (commands that need the successor's identity — the join, the pin on the derived transcript, the ack `continue` as the default, the reap proof, the prime's Belam chain — run by rotate-self after the join, delivered as the successor's SECOND input through the fixed nudge and written into the rotation record). The CODE half is the 0b round (hypothesis:l4-startup-is-one-script-or-a-driven-prompt): rotate-self executes the lists with the template's placeholders resolved from the join, refuses a template whose startup names a command that is not on the allowlist, and the successor brief carries ZERO instructions to run anything. Target: the seat's first tool call is graph work.

PRIME XII 2026-09-11 21:5xZ, mur-41 (L4.290): the fact_bounds map on this node was written by kid a00-7706072a with a self-declared --role owner to pass written_by [owner, prime_director] (write.py _resolve_role returns role_param before any seat resolution). The CONTENT is what the amended build order asked and the Prime XI GO'd, so this write is SANCTIONED by this note (edited_by returns to the prime); the MECHANISM is a g15 finding routed to the point: --role may never elevate above the resolved seat role.
