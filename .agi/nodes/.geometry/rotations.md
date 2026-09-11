---
id: config:rotations
mint_id: ee0148fe1f4d4244aa2527dc961bdd20
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
edited_by: belam
locations: {}
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
    startup:
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:48'", "why": "gen XIV calls 2, 4-10, 22-23, 26-30: 16 wake calls re-deriving facts F1-F4 (owner 2026-09-11 12:4xZ); printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "gen X call 6"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "gen X calls 10-15: six calls spent learning write.py's verbs from source"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}; ListAgents ref {succ_ref}", "why": "gen X call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "gen X call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "written by rotate-self as the default; the successor may write `diff` later if the handoff needs a change"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}' || echo 'predecessor chain gone'", "why": "gen X calls 3, 9: the predecessor's process tree checked twice by hand"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ)."
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
    startup:
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:48'", "why": "belam gen IX calls 5-9, 10-12, 25-26 (ack grammar from source, record polled 18x, lock path grepped) + gen XIV's F1-F5; master-sensei gen I wake audit 13:1xZ; printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "gen X call 6"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "gen X calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "the prime's first duty is the tree's health; 26 s, no suite"}
        - {"label": "account", "cmd": "curl -s -m 20 https://openrouter.ai/api/v1/credits -H \"Authorization: Bearer $OPENROUTER_PROVISIONING_KEY\"", "why": "spend read from the ACCOUNT, never the .env key"}
        - {"label": "since-last-rotation", "cmd": "git diff --stat", "why": "belam gen IX calls 13-15: what changed in the tree since the last wake, read by hand (master-sensei gen I draft, judged None; the inbox half was already the inbox entry)"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}; ListAgents ref {succ_ref}", "why": "gen X call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "gen X call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "written by rotate-self as the default; the successor may write `diff` later if the handoff needs a change"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}' || echo 'predecessor chain gone'", "why": "gen X calls 3, 9: the predecessor's process tree checked twice by hand"}
        - {"label": "belam-chain", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep belam-S1", "why": "the chain must be five"}
        - {"label": "sensei-wake", "cmd": "python3 extensions/agi/bin/send.py send master-sensei 'rotation-alert: belam gen {gen} is live - audit its wake per your standing order (owner 2026-09-11 14:0xZ)'", "why": "owner 2026-09-11 14:0xZ: the Sensei wakes for helper, point AND Prime rotations; a Prime rotation posts to the rotation-alerts ROOM (no nudge), so the join nudges the Sensei by dm here"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ). The prime's `verify-suite` stays a granted-window command and is NOT run at startup; the Belam chain is kept by predecessor pins (hypothesis:l4-the-pin-is-the-lease), not by a reap step."
      after_join_delay_s: 20
thought_session: belam-S1-L4-VII
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

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) — the bootstrap facts a successor is handed instead of reading the handoff. 0b-b's emitter is not live yet; until it lands, the director template's `facts` first_turn entry prints this section by body range. MEASURED facts only, each with the wake that paid for it (owner 2026-09-11 12:4xZ, verbatim: "sanctuary director just rotated, did 60 tool calls straight first thing. Need to figure out what and why and add to his rotation config"; measured from gen XIV's transcript: 66 calls in 12 min, 11 wake + 55 harvest, of which 16 re-derived F1-F4).

- F1 (gen XIV calls 2, 4-7 — 6 calls): after YOUR ack the predecessor's wrapper reaps its own chain and writes the record `success` within ~60 s. ONE call proves it — `python3 extensions/agi/bin/rotate.py status --seat <seat> --record latest` (its `s12_self_reap` section) — never `ps`/`tmux` by hand. The record in your STARTUP OUTPUT reads `started` by construction: it ran before your ack.
- F2 (gen XIV calls 26-30 — 5 calls): a worktree seat's `config:seats` row (session_ref/pid/window/generation) is written in ITS OWN worktree at spawn and back-filled at its ack; it reaches `season/s2` at that seat's next merge-up. `send.py whois <ref>` against origin reads NO-MATCH until then — expected, not a defect; verify by the record + the seat worktree's row + the pane.
- F3 (gen XIV calls 8-10 — 3 calls): the channel to the Prime is `SendMessage` to the ListAgents row whose `[ref]` equals the `belam` row's `session_ref` (printed by `prime-authority` above), or `python3 extensions/agi/bin/send.py send belam "<one line>"` (which also nudges the pane). Only when necessary (owner 2026-09-10 05:0xZ): merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding.
- F4 (gen XIV calls 22-23 — 2 calls): the note verb is `python3 extensions/agi/bin/write.py <node-id> "note <text>" --actor <seat> --role director` — one note per call, no `&&` inside prose (write the word double-ampersand), backticks only inside a single-quoted script. A partial edit is `"read body N:M"` then `"replace body N:M <file>"`.
- F5 (gen XIV calls 12-16, 39-40, 48, 52-54, 60, 64 — harvest discovery, ~12 calls over 5 rounds): a round lands on branch `loop/<hypothesis-slug-prefix>-<agent>@s2` in worktree `.agi/worktrees/<agent>/`; diff it against the MERGE-BASE with the seat branch (never against a moved seat tip); its kid experiment nodes are under `.agi/nodes/experiment/` on that branch. Three calls per round is the shape until a `harvest-table` subcommand exists (proposed g15).
- F6 (belam gen IX calls 5-9 + 10-12 — ack grammar read from source, record hand-polled 18x; master-sensei gen I wake audit, 13:1xZ): the ack is `rotate.py ack --seat <seat> --gen <N> --ref <your ListAgents ref> continue|diff [--text -]` (rotate.py:1345) — `continue` vs `diff` is the successor's ONE decision on wake (a `diff` halts the rotation for inspection: the predecessor's wrapper returns 1 and leaves the window). The docstring's DEPRECATED note (rotate.py:1342-1354, L4.112(E)) is stale wording: the predecessor writes the PENDING ack, the successor's overwrite stays the decision. The record turns `success` ~40-60 s after the ack; ONE status read after that, never a poll loop (`--wait` arrives with `hypothesis:rotate-status-record-latest-gains-wait`).
- F7 (belam gen IX calls 25-26 — grepped the source for the lock path): the suite lock is `.agi/sessions/verify-suite.lock` under the graph root (verification.py:75 `SUITE_LOCK`); "lock FREE" for a merge-up window = that file absent in main AND in every `.agi/worktrees/seat-*/.agi/sessions/`; the window reply is lock state + tip + baseline in one line.

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 22:5xZ) ahead of merge-up 19, because L4.110's rotate.py refuses every rotate-self while this node is absent: creating it before the code lands decouples the two and keeps every seat rotatable in between. Body and templates are L4.110's shipped extensions/agi/briefs/rotations.geometry.md with the point gen VIII's two measured corrections (director brief_file = the quorum scratchpad with {seat}; parent and kid entries dropped). The file was moved from nodes/config/ to nodes/.geometry/ because that is the address rotate.py resolves (same as config:seats); the mint id is unchanged. spawn_check unverified is the gate's honest stamp: it found no active spawn rule for type config.
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 (date -u 02:5xZ), verbatim in doc:l4-owner-decisions: "sanctuary director still had a good few tool calls but it was like 3 before first words. But it said this: Gen X here. First acts: verify rotation, pin meter, ack. Those are all things that need to happen automatically. There's still way too many calls in his history. Look through it and find a way to fold all of it into the rotation itself. The rotation template for each role should specify which commands get ran for them automatically so they get to see the command output as their actual first input turn plus the other standard head, brief, etc". MEASURED by the Prime on gen X's transcript (first 16 tool calls, 02:38:10-02:40:41Z): 1-2 own row + ack file + rotation record + sequence by hand; 3 and 9 the predecessor's process tree, twice; 4-5 ListAgents join + own transcript + pin; 6 git status seat and main; 7 whois of the Prime's ref (authority); 8 the record again; 10-15 SIX calls learning write.py's verbs from its source; 16 the sessions json + bootstrap file. APPLIED as the CONFIG half here: each template gains `startup` = `first_turn` (commands rotate-self runs BEFORE spawn and appends to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`: rotation record, seat row, the Prime's authority, git state, inbox, live spawns, write.py verbs; the prime adds `run verify` and the account) and `after_join` (commands that need the successor's identity — the join, the pin on the derived transcript, the ack `continue` as the default, the reap proof, the prime's Belam chain — run by rotate-self after the join, delivered as the successor's SECOND input through the fixed nudge and written into the rotation record). The CODE half is the 0b round (hypothesis:l4-startup-is-one-script-or-a-driven-prompt): rotate-self executes the lists with the template's placeholders resolved from the join, refuses a template whose startup names a command that is not on the allowlist, and the successor brief carries ZERO instructions to run anything. Target: the seat's first tool call is graph work.