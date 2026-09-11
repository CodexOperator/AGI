---
id: config:rotations
mint_id: ee0148fe1f4d4244aa2527dc961bdd20
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
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
      byte_cap: 8000
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:56'", "why": "gen XIV calls 2, 4-10, 22-23, 26-30: 16 wake calls re-deriving facts F1-F4 (owner 2026-09-11 12:4xZ); printed by body range until 0b-b's facts emitter lands"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "gen X call 6"}
        - {"label": "predecessor-log", "cmd": "git -C {worktree} log --oneline -12; git -C {repo} log --oneline -3", "why": "gen XIV calls 24-25 (predecessor's landed commits by hand) + 26-27, 69, 79 (four fetch+rev-parse behind checks): main's tip is in your own log or it is not (master-sensei gen I wake audit of gen XIV, applied by the Prime L4-X; judged None)"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "gen X calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "send-verbs", "cmd": "python3 extensions/agi/bin/send.py -h | sed -n 1,30p", "why": "sanctuary-director 122528Z calls 8-9, sanctuary-helper 152548Z call 7, sensei-director first seating calls 2-3: three seats learned send.py's verbs by hand"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}", "why": "(the ListAgents name<->ref join is the service's registry read, not a shell stage \u2014 judge-cleaned by the Prime L4-X 15:4xZ so the WHOLE templates value passes the L4.234 gate) gen X call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "gen X call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "written by rotate-self as the default; the successor may write `diff` later if the handoff needs a change"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'", "why": "(empty output = predecessor chain gone; the || fallback was an unmodeled operator \u2014 judge-cleaned by the Prime L4-X 15:4xZ) gen X calls 3, 9: the predecessor's process tree checked twice by hand"}
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
      byte_cap: 40000
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "gen X call 1-2, 8: the record (with successor_row) + sequence read by hand; L4.179: status --record latest, whois was never a rotate.py verb"}
        - {"label": "facts", "cmd": "python3 extensions/agi/bin/write.py config:rotations 'read body 37:56'", "why": "belam gen IX calls 5-9, 10-12, 25-26 (ack grammar from source, record polled 18x, lock path grepped) + gen XIV's F1-F5; master-sensei gen I wake audit 13:1xZ; printed by body range until 0b-b's facts emitter lands"}
        - {"label": "handoff-head", "cmd": "python3 extensions/agi/bin/write.py build:HANDOFF.md 'read payload 1:175'", "why": "belam 093748Z calls 2-3, 140328Z calls 1,3,4,5,7 (a 1,200p read overflowed the tool-result cap, then four ranges): the handoff read by hand in ranges every prime rotation; this IS the range the file's own rule asks for (bare sed is refused: filter-only); byte_cap 40000 truncates a handoff past the trim line, marked (master-sensei gen I, applied by the Prime L4-X 15:4xZ)"}
        - {"label": "point-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat sanctuary-director --record latest", "why": "belam 140328Z calls 15-16: the point's record read twice by hand; the Prime's first question after its own state is the point's (seat name hardcoded like belam-chain's belam-S1; master-sensei gen I, applied L4-X)"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "gen X call 7: authority verified against the graph, never the message"}
        - {"label": "git-state", "cmd": "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3", "why": "gen X call 6"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms are the first thing a seat owes a reply to"}
        - {"label": "live-spawns", "cmd": "python3 extensions/agi/bin/spawn_budget.py status; python3 extensions/agi/bin/provisioning.py status | head -4", "why": "the seat inherits its predecessor's live spawns (owner 02:0xZ)"}
        - {"label": "write-verbs", "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p", "why": "gen X calls 10-15: six calls spent learning write.py's verbs from source"}
        - {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "the prime's first duty is the tree's health; 26 s, no suite"}
        - {"label": "since-last-rotation", "cmd": "git diff --stat", "why": "belam gen IX calls 13-15: what changed in the tree since the last wake, read by hand (master-sensei gen I draft, judged None; the inbox half was already the inbox entry)"}
      after_join:
        - {"label": "join", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep {succ_name}", "why": "(the ListAgents name<->ref join is the service's registry read, not a shell stage \u2014 judge-cleaned by the Prime L4-X 15:4xZ so the WHOLE templates value passes the L4.234 gate) gen X call 4-5: the name<->ref<->@id join, derived by rotate-self at spawn (L4.114)"}
        - {"label": "pin", "cmd": "python3 extensions/agi/bin/rotate.py meter --pin {pin_ref} --session-log {succ_transcript}", "why": "gen X call 5: the pin claim on the successor's own transcript, path derived from ~/.claude/sessions/<pid>.json"}
        - {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "written by rotate-self as the default; the successor may write `diff` later if the handoff needs a change"}
        - {"label": "reap-proof", "cmd": "ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'", "why": "(empty output = predecessor chain gone; the || fallback was an unmodeled operator \u2014 judge-cleaned by the Prime L4-X 15:4xZ) gen X calls 3, 9: the predecessor's process tree checked twice by hand"}
        - {"label": "belam-chain", "cmd": "tmux list-windows -t {tmux_session} -F '#{window_id} #{window_name}' | grep belam-S1", "why": "the chain must be five"}
        - {"label": "sensei-wake", "cmd": "python3 extensions/agi/bin/send.py send master-sensei 'rotation-alert: belam gen {gen} is live - audit its wake per your standing order (owner 2026-09-11 14:0xZ)'", "why": "owner 2026-09-11 14:0xZ: the Sensei wakes for helper, point AND Prime rotations; a Prime rotation posts to the rotation-alerts ROOM (no nudge), so the join nudges the Sensei by dm here"}
      delivery: "first_turn outputs are appended to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`. after_join is PERFORMED BY THE SERVICE (the persistent watcher, or rotate-self's post-spawn tail) after_join_delay_s after spawn as ONE flow — the agent runs nothing; its outputs are written into the rotation record and delivered as the successor's SECOND input (one dm through the fixed nudge); where a decision remains (only `diff` against the handoff) the dm is CAPTIVE: it prints the exact next tokens to emit (owner 2026-09-11 03:0xZ). The prime's `verify-suite` stays a granted-window command and is NOT run at startup; the Belam chain is kept by predecessor pins (hypothesis:l4-the-pin-is-the-lease), not by a reap step."
      after_join_delay_s: 20
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

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) — the bootstrap facts a successor is handed instead of reading the handoff. 0b-b's emitter is not live yet; until it lands, the director template's `facts` first_turn entry prints this section by body range. MEASURED facts only, each with the wake that paid for it (owner 2026-09-11 12:4xZ, verbatim: "sanctuary director just rotated, did 60 tool calls straight first thing. Need to figure out what and why and add to his rotation config"; measured from gen XIV's transcript: 66 calls in 12 min, 11 wake + 55 harvest, of which 16 re-derived F1-F4).

> Staleness bound (L4.290): a fact the `fact_bounds:` map does not name defaults to `head` — treated as head-bound and marked stale when its measured commit differs from HEAD; a `permanent` fact is never marked. Written by `write.py`, never by hand.

- F1 (gen XIV calls 2, 4-7 — 6 calls): after the ack (the PENDING `continue` the service wrote for you — F8 — or your own overwrite) the predecessor's wrapper reaps its own chain and writes the record `success` within ~60 s. ONE call proves it — `python3 extensions/agi/bin/rotate.py status --seat <seat> --record latest` (its `s12_self_reap` section) — never `ps`/`tmux` by hand. The record in your STARTUP OUTPUT reads `started` by construction: it ran before your ack.
- F2 (gen XIV calls 26-30 — 5 calls): a worktree seat's `config:seats` row (session_ref/pid/window/generation) is written in ITS OWN worktree at spawn and back-filled at its ack; it reaches `season/s2` at that seat's next merge-up. `send.py whois <ref>` against origin reads NO-MATCH until then — expected, not a defect; verify by the record + the seat worktree's row + the pane.
- F3 (gen XIV calls 8-10 — 3 calls): the channel to the Prime is `SendMessage` to the ListAgents row whose `[ref]` equals the `belam` row's `session_ref` (printed by `prime-authority` above), or `python3 extensions/agi/bin/send.py send belam "<one line>"` (which also nudges the pane). Only when necessary (owner 2026-09-10 05:0xZ): merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding.
- F4 (gen XIV calls 22-23 — 2 calls): the note verb is `python3 extensions/agi/bin/write.py <node-id> "note <text>" --actor <seat> --role director` — one note per call, no `&&` inside prose (write the word double-ampersand), backticks only inside a single-quoted script. A partial edit is `"read body N:M"` then `"replace body N:M <file>"`.
- F5 (gen XIV calls 12-16, 39-40, 48, 52-54, 60, 64 — harvest discovery, ~12 calls over 5 rounds): a round lands on branch `loop/<hypothesis-slug-prefix>-<agent>@s2` in worktree `.agi/worktrees/<agent>/`; diff it against the MERGE-BASE with the seat branch (never against a moved seat tip); its kid experiment nodes are under `.agi/nodes/experiment/` on that branch. Three calls per round is the shape until a `harvest-table` subcommand exists (proposed g15).
- F6 (belam gen IX calls 5-9 + 10-12 — ack grammar read from source, record hand-polled 18x; master-sensei gen I wake audit, 13:1xZ): the ack is `rotate.py ack --seat <seat> --gen <N> --ref <your ListAgents ref> continue|diff [--text -]` (rotate.py:1345) — `continue` vs `diff` is the successor's ONE decision on wake (a `diff` halts the rotation for inspection: the predecessor's wrapper returns 1 and leaves the window). The docstring's DEPRECATED note (rotate.py:1342-1354, L4.112(E)) is stale wording: the predecessor writes the PENDING ack, the successor's overwrite stays the decision. The record turns `success` ~40-60 s after the ack; ONE status read after that, never a poll loop (`--wait` arrives with `hypothesis:rotate-status-record-latest-gains-wait`).
- F7 (belam gen IX calls 25-26 — grepped the source for the lock path): the suite lock is `.agi/sessions/verify-suite.lock` under the graph root (verification.py:75 `SUITE_LOCK`); "lock FREE" for a merge-up window = that file absent in main AND in every `.agi/worktrees/seat-*/.agi/sessions/`; the window reply is lock state + tip + baseline in one line.
- F8 (sanctuary-director 122528Z calls 1, 3-7; CORRECTED by master-sensei on sanctuary-helper 155017Z, where the first wording cost 8 calls — the seat waited for a `continue` that is never written; RE-CUT by the Prime XII 22:1xZ at merge-up SL2#6, SL5.01 + SL4.03 landed): at spawn rotate-self writes your meter pin, your row's `session_id`/`generation`/`window`/`pid` (`session_ref` stays empty) AND COMMITS THAT ROW WRITE ITSELF (SL5.01 — before it, the uncommitted spawn row made the ack's pre-dirty gate refuse every wake; Prime XII paid 2 calls at 21:25Z, four posts hand-committed that day), and `seats/<seat>.ack.json` with `answer: pending`. NOTHING ELSE ARRIVES — there is no after_join executor yet. Your ONE required wake act: `python3 extensions/agi/bin/rotate.py ack --seat <seat> --gen <N> --ref <bare ListAgents ref> continue` (or `diff` if the handoff needs a change). The ack back-fills `session_ref` (and pid/session_id when the join by your row's own @id says they differ — L4.288), COMMITS its own row write as one pathspec commit and PRINTS the +/- lines and the exact `git push` line (SL4.03) — you push; nothing to `git diff` or commit by hand. The ref is harness-only (not in `~/.claude/sessions/<pid>.json`), so ONE `ListAgents` is legitimate; nothing else is — never `ps`, `tmux`, `ls seats/`, the record by hand, or a grep of rotate.py for the ack path. Minimum wake = ListAgents + ack + push. If the ack refuses `seats.md is dirty before this ack`, someone else's row change is in your tree: commit or drop THAT first, never bundle it.
- F9 (gen XIV calls 26-27, 69, 79 — 4 calls): L4.108 — a `--branch` dispatch from a seat behind `season/s2` refuses with exit 3 and names it; that refusal IS the behind check. `predecessor-log` shows main's tip; there is no fetch+rev-parse to run by hand.
- F10 (gen XIV calls 12, 36, 82 — 3 calls): live-spawns, git-state and inbox are ALREADY in your STARTUP OUTPUT — re-running any of them in the first turn buys nothing; your brief's headings are the brief you are reading.
- F11 (gen XIV call 10 — 1 call): `SendMessage` costs a ToolSearch call first; `python3 extensions/agi/bin/send.py send belam "<one line>"` costs none and nudges the pane — prefer it (F3's two forms in that order).
- F12 (belam 140328Z calls 20-24 — 5 calls): judge a first_turn entry in-process, never from source: `python3 - <<'EOF'` / `import sys; sys.path.insert(0,'extensions/agi/bin'); import rotate as r; print(r._producing_refusal(r._resolve_startup_placeholders(CMD, {'seat': S, 'worktree': W, 'repo': R}, refuse_empty=True)))` / `EOF` — `None` = allowed. Positional revisions/paths (`HEAD..x`, `seat/x@s2`) and bare sed/grep/cat as the LEADING unit are refused.
- F13 (belam 140328Z calls 37-38): the `account` first_turn entry was dropped 15:4xZ — it refused on every prime wake (the executor has no `.env`; g15-18 is the open code half). Spend by hand, one command: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' .env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"` (verified 15:4xZ: total_credits/total_usage).
- F14 (sanctuary-helper 152548Z, whole wake): rotate-self reads `config:rotations` AND `config:seats` from the ROTATING SEAT'S WORKTREE. Before `rotate-self`, merge `season/s2` into your worktree (`git merge --no-edit origin/season/s2`; never rebase) or your successor wakes on a stale template with a stale `{prime_ref}` (the helper's was 218 behind: NO facts, prime-authority NO-MATCH) and re-derives every fact by hand.
- F15 (sanctuary-helper 152548Z): `rotate.py ack --ref` takes the BARE ref (`fbb88c`), never the ListAgents row (`name [ref]`); the value lands verbatim in your row's `session_ref` and `whois` matches by prefix on it.
- F16 (sanctuary-director 135144Z rotate-out calls 206-207 and 163547Z 246-247, sanctuary-helper 152548Z 542 — every worktree seat ran `rotate-self -h` then `--dry-run` by hand before rotating): the grammar is `rotate.py rotate-self --name <seat> --model <m> --effort <e> --prompt-file .agi/sessions/quorum/<seat>.md [--timeout S]`; the pre-flight is `rotate-self --prepare` (landed by sensei-director 17:12Z) — run it ONCE and emit the tokens it prints; never `-h`, and never `--dry-run | head` (its head is the prompt file's prayers).
- F17 (sensei-director first seating calls 12-13 — hunted `schemas/goal.md`): node-type schemas live at `.agi/context/schemas/[type].md`, brackets in the filename; `ls .agi/context/schemas/` lists them; `write.py create <type> <slug> --parent <id>` runs the spawn gate against that file.

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 22:5xZ) ahead of merge-up 19, because L4.110's rotate.py refuses every rotate-self while this node is absent: creating it before the code lands decouples the two and keeps every seat rotatable in between. Body and templates are L4.110's shipped extensions/agi/briefs/rotations.geometry.md with the point gen VIII's two measured corrections (director brief_file = the quorum scratchpad with {seat}; parent and kid entries dropped). The file was moved from nodes/config/ to nodes/.geometry/ because that is the address rotate.py resolves (same as config:seats); the mint id is unchanged. spawn_check unverified is the gate's honest stamp: it found no active spawn rule for type config.
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 (date -u 02:5xZ), verbatim in doc:l4-owner-decisions: "sanctuary director still had a good few tool calls but it was like 3 before first words. But it said this: Gen X here. First acts: verify rotation, pin meter, ack. Those are all things that need to happen automatically. There's still way too many calls in his history. Look through it and find a way to fold all of it into the rotation itself. The rotation template for each role should specify which commands get ran for them automatically so they get to see the command output as their actual first input turn plus the other standard head, brief, etc". MEASURED by the Prime on gen X's transcript (first 16 tool calls, 02:38:10-02:40:41Z): 1-2 own row + ack file + rotation record + sequence by hand; 3 and 9 the predecessor's process tree, twice; 4-5 ListAgents join + own transcript + pin; 6 git status seat and main; 7 whois of the Prime's ref (authority); 8 the record again; 10-15 SIX calls learning write.py's verbs from its source; 16 the sessions json + bootstrap file. APPLIED as the CONFIG half here: each template gains `startup` = `first_turn` (commands rotate-self runs BEFORE spawn and appends to the successor's first input turn after the head and the brief, under `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`: rotation record, seat row, the Prime's authority, git state, inbox, live spawns, write.py verbs; the prime adds `run verify` and the account) and `after_join` (commands that need the successor's identity — the join, the pin on the derived transcript, the ack `continue` as the default, the reap proof, the prime's Belam chain — run by rotate-self after the join, delivered as the successor's SECOND input through the fixed nudge and written into the rotation record). The CODE half is the 0b round (hypothesis:l4-startup-is-one-script-or-a-driven-prompt): rotate-self executes the lists with the template's placeholders resolved from the join, refuses a template whose startup names a command that is not on the allowlist, and the successor brief carries ZERO instructions to run anything. Target: the seat's first tool call is graph work.

PRIME XII 2026-09-11 21:5xZ, mur-41 (L4.290): the fact_bounds map on this node was written by kid a00-7706072a with a self-declared --role owner to pass written_by [owner, prime_director] (write.py _resolve_role returns role_param before any seat resolution). The CONTENT is what the amended build order asked and the Prime XI GO'd, so this write is SANCTIONED by this note (edited_by returns to the prime); the MECHANISM is a g15 finding routed to the point: --role may never elevate above the resolved seat role.