---
id: config:rotations
mint_id: ee0148fe1f4d4244aa2527dc961bdd20
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
edited_by: belam-S1-L4-VII
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
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py whois --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record + sequence + own row read by hand"}
        - {"label": "seat-row", "cmd": "python3 extensions/agi/bin/send.py whois {succ_ref} --claim {seat}", "why": "gen X call 1: the row after the handover, from the PUSHED graph"}
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
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py whois --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record + sequence + own row read by hand"}
        - {"label": "seat-row", "cmd": "python3 extensions/agi/bin/send.py whois {succ_ref} --claim {seat}", "why": "gen X call 1: the row after the handover, from the PUSHED graph"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "gen X call 6"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "gen X calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "the prime's first duty is the tree's health; 26 s, no suite"}
        - {"label": "account", "cmd": "curl -s -m 20 https://openrouter.ai/api/v1/credits -H \"Authorization: Bearer $OPENROUTER_PROVISIONING_KEY\"", "why": "spend read from the ACCOUNT, never the .env key"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}; ListAgents ref {succ_ref}", "why": "gen X call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "gen X call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "written by rotate-self as the default; the successor may write `diff` later if the handoff needs a change"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}' || echo 'predecessor chain gone'", "why": "gen X calls 3, 9: the predecessor's process tree checked twice by hand"}
        - {"label": "belam-chain", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep belam-S1", "why": "the chain must be five"}
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

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap facts a successor is handed instead of reading the handoff.
> Empty until 0b lands; do not invent facts here.

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 22:5xZ) ahead of merge-up 19, because L4.110's rotate.py refuses every rotate-self while this node is absent: creating it before the code lands decouples the two and keeps every seat rotatable in between. Body and templates are L4.110's shipped extensions/agi/briefs/rotations.geometry.md with the point gen VIII's two measured corrections (director brief_file = the quorum scratchpad with {seat}; parent and kid entries dropped). The file was moved from nodes/config/ to nodes/.geometry/ because that is the address rotate.py resolves (same as config:seats); the mint id is unchanged. spawn_check unverified is the gate's honest stamp: it found no active spawn rule for type config.
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 (date -u 02:5xZ), verbatim in doc:l4-owner-decisions: "sanctuary director still had a good few tool calls but it was like 3 before first words. But it said this: Gen X here. First acts: verify rotation, pin meter, ack. Those are all things that need to happen automatically. There's still way too many calls in his history. Look through it and find a way to fold all of it into the rotation itself. The rotation template for each role should specify which commands get ran for them automatically so they get to see the command output as their actual first input turn plus the other standard head, brief, etc". MEASURED by the Prime on gen X's transcript (first 16 tool calls, 02:38:10-02:40:41Z): 1-2 own row + ack file + rotation record + sequence by hand; 3 and 9 the predecessor's process tree, twice; 4-5 ListAgents join + own transcript + pin; 6 git status seat and main; 7 whois of the Prime's ref (authority); 8 the record again; 10-15 SIX calls learning write.py's verbs from its source; 16 the sessions json + bootstrap file. APPLIED as the CONFIG half here: each template gains `startup` = `first_turn` (commands rotate-self runs BEFORE spawn and appends to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`: rotation record, seat row, the Prime's authority, git state, inbox, live spawns, write.py verbs; the prime adds `run verify` and the account) and `after_join` (commands that need the successor's identity — the join, the pin on the derived transcript, the ack `continue` as the default, the reap proof, the prime's Belam chain — run by rotate-self after the join, delivered as the successor's SECOND input through the fixed nudge and written into the rotation record). The CODE half is the 0b round (hypothesis:l4-startup-is-one-script-or-a-driven-prompt): rotate-self executes the lists with the template's placeholders resolved from the join, refuses a template whose startup names a command that is not on the allowlist, and the successor brief carries ZERO instructions to run anything. Target: the seat's first tool call is graph work.