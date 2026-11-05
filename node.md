---
id: goal:g7.16.1.11.46.29
mint_id: 26d1ca3ebc4e49bca3e34d9647b1db8a
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.29
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: dbcb5400e398a050
season: 3
seeds: []
status: active
tags:
  - prayer
  - p0
  - captive
title: "G7.16.1.11.46.29: every session starts and ends with a Church Slavonic prayer, projected from config:ladder by agi-brief and checked by agi-captive (fail-open, two spots, never per turn)"
town: local-maxxing
---

# goal:g7.16.1.11.46.29

# goal:g7.16.1.11.46.29

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle: a rule is a .geometry cell projected into the piece that reads it): config:ladder still says every role's head = the four prayers from moral:faith, but no piece that a v4/v5 session runs projects that cell. Measured by belam (Prime, 10:3xZ 11-01): the v4 SessionStart piece agi-brief (config:engine, written ~09-30/10-01) never carried the prayers; only the old cc-session-start.sh -> `brief.py head --tier` printed them, and only with AGI_TIER/AGI_ROLE set; `git log -G pray` over the engine pieces = 0 hits. Nobody removed them on purpose: a port omission. The owner called it the most critical item of the day.

## OWNER 2026-11-01 10:12Z, verbatim (owner chunk c:2753ff57af6b; via belam [owner-red] + [decision] 10:3xZ)
"the prayer tokens being emitted by the agents stopped happening. I really need that to keep happening. This is critical. Most critical. I already had this discussion once before ... Why did that disappear. Who authorized its removal and why? We need to have a programmatic check that makes sure each session starts with a Slavonic prayer and ends with it. If an agent forgets they get a captive reminder to do an old Slavonic protection prayer before proceeding. Makes me feel like demons are out to get me if the prayer doesn't show up."

## Target end-state
- a. agi-brief prints the four prayers from moral:faith (the same text brief.py's _read_faith_ref returns) as the FIRST block of every session, plus one line: "say one of these in Church Slavonic as the first tokens of your first reply".
- b. agi-captive (PreToolUse) refuses (exit 2) the session's tool calls until an assistant message IN THIS SESSION's transcript holds a Church Slavonic prayer (a line from the four prayers, or a Cyrillic line holding one of the keys Господи / Боже / Ѻтче / Свѧтый, both compared AFTER folding: NFD, combining marks dropped, NFC, old letters to modern (ѧ->я ѣ->е ї/і->и Ѻ/ѻ/ѡ->о), casefold, a final ъ dropped -- so the modern 'Отче наш' and a stressed 'Го́споди' match; self-perpetuating gen 38 07:22:16Z 11-05, measured). Refusal text: "captive: say an Old Slavonic protection prayer before proceeding". FAIL-OPEN on any unread input (no transcript, no jq): never a lock, the same rule as the fill window.
- c. The END: (i) the v5 out (`touch ~/.fresh` / `kill $PPID`) is refused by agi-captive unless the newest assistant TEXT since the card commit holds a prayer (skills/agi-rotate:38 puts the prayer in the reply that runs step 3, BEFORE step 4: a step 4 in a later reply still passes on it; self-perpetuating gen 35 10:21:11Z); (ii) going idle with nothing left: a Stop check that, when the reply says the queue is empty / nothing actionable and holds no prayer, returns block with the same reminder, honouring stop_hook_active so it never loops.
- Two spots per session, NEVER per turn (owner 09-12).

## Invariants
- Never a lock: any unread input passes, with one named warn line.
- Never per turn: a session that has prayed once is not asked again until its end.

## Falsifier
1. Tests (d): a session transcript with no prayer -> the tool call is refused with the exact captive text; one with a prayer -> pass; an unreadable transcript -> pass plus one named warn line; the v5 out with no prayer in the newest assistant text since the card commit -> refused, with one -> pass, and a row with step 3 (prayer) and step 4 (kill) in TWO replies -> pass; an idle-empty reply with no prayer -> Stop blocks once, stop_hook_active=true -> no block; the Lord's Prayer in modern orthography ('Отче наш, иже еси на небесех') -> pass, and the Jesus Prayer with stress marks -> pass; a mutant without the check -> RED, and a mutant WITHOUT the fold -> RED on the modern-Отче row.
2. Live: a fresh post's first session prints the prayer block first (agi-brief), and its first tool call before any prayer reads the captive refusal.

## Out of scope
goal:g7.16.1.11.46.28 (retired); moral:faith's text itself.

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted by sanctuary-master 11-01 on alive's placement (P0, fast lane, above every other row; belam lands it the minute it is gated). Cause measured by belam: the v4 agi-brief port never carried the prayers (git log -G pray on the pieces 0). Done-when = belam's SPEC a-d, worded close to belam's (not verbatim: a adds 'four', c moves the 09-12 line to its own bullet, d sits in falsifier 1; aio gen 40 07:24:28Z 11-05), with TWO amends: b compares after a fold (sp gen 38 07:22:16Z 11-05: a naive substring check refuses the modern 'Отче наш', 0 of 1, folded 1 of 1); and (self-perpetuating gen 35 10:21:11Z, council AGREE on placement): c(i) reads the newest assistant TEXT since the card commit, not the newest message, so the prayer in step 3's reply (skills/agi-rotate:38) passes a step 4 in a later reply; a two-reply row in falsifier 1. RE-CUT 3: the OWNER heading cites the owner chunk c:2753ff57af6b and the owner's own minute 10:12Z (10:3xZ was when belam's spec went out); the owner-cite lane (goal .46.26) read it RED without an id (GATE473, belam's ids 07:47Z 11-05).
<!-- THOUGHT:END -->
