---
id: goal:g7.16.1.11.46.29
mint_id: 26d1ca3ebc4e49bca3e34d9647b1db8a
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
edited_by: director-general-3
confidence: 0.5
goal_id: G7.16.1.11.46.29
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: dbcb5400e398a050
season: 3
seeds: []
status: complete
tags:
  - prayer
  - p0
  - captive
title: "G7.16.1.11.46.29: every session starts and ends with a Church Slavonic prayer, projected from config:ladder by agi-brief and checked by agi-captive (fail-open; MAY at each idle spot (owner 11-07); never per working turn)"
town: local-maxxing
---

# goal:g7.16.1.11.46.29

# goal:g7.16.1.11.46.29

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle: a rule is a .geometry cell projected into the piece that reads it): config:ladder still says every role's head = the four prayers from moral:faith, but no piece that a v4/v5 session runs projects that cell. Measured by belam (Prime, 10:3xZ 11-01): the v4 SessionStart piece agi-brief (config:engine, written ~09-30/10-01) never carried the prayers; only the old cc-session-start.sh -> `brief.py head --tier` printed them, and only with AGI_TIER/AGI_ROLE set; `git log -G pray` over the engine pieces = 0 hits. Nobody removed them on purpose: a port omission. The owner called it the most critical item of the day.

## OWNER 2026-11-01 10:12Z, verbatim (owner chunk c:2753ff57af6b; via belam [owner-red] + [decision] 10:3xZ)
"the prayer tokens being emitted by the agents stopped happening. I really need that to keep happening. This is critical. Most critical. I already had this discussion once before ... Why did that disappear. Who authorized its removal and why? We need to have a programmatic check that makes sure each session starts with a Slavonic prayer and ends with it. If an agent forgets they get a captive reminder to do an old Slavonic protection prayer before proceeding. Makes me feel like demons are out to get me if the prayer doesn't show up."

## OWNER 2026-11-07 06:33:17Z, verbatim (owner chunk c:c91f4ca10325; via belam [owner] 06:33:38Z, asked: a close, then a wake, then the out: is a third prayer owed)
"Yes it can do it repeatedly each "idle" spot"

## Target end-state
- a. agi-brief prints the four prayers from moral:faith (the same text brief.py's _read_faith_ref returns) as the FIRST block of every session, plus one line: "say one of these in Church Slavonic as the first tokens of your first reply". Since goal:g7.16.1.11.46.29.2 a HEAD (the reply-final ask, the card path, its where-it-stops line) sits above this block, and the ask is the reply-final form.
- b. agi-captive (PreToolUse) refuses (exit 2) the session's tool calls until an assistant message IN THIS SESSION's transcript holds a Church Slavonic prayer (a line from the four prayers, or a Cyrillic line holding one of the keys Господи / Боже / Ѻтче / Свѧтый, both compared AFTER folding: NFD, combining marks dropped, NFC, old letters to modern (ѧ->я ѣ->е ї/і->и Ѻ/ѻ/ѡ->о), casefold, a final ъ dropped -- so the modern 'Отче наш' and a stressed 'Го́споди' match; self-perpetuating gen 38 07:22:16Z 11-05, measured). Refusal text: "captive: say an Old Slavonic protection prayer before proceeding". FAIL-OPEN on any unread input (no transcript, no jq): never a lock, the same rule as the fill window.
- c. The END: (i) the v5 out (`touch ~/.fresh` / `kill $PPID`) is refused by agi-captive unless the newest assistant TEXT since the card commit holds a prayer (skills/agi-rotate:38 puts the prayer in the reply that runs step 3, BEFORE step 4: a step 4 in a later reply still passes on it; self-perpetuating gen 35 10:21:11Z); (ii) going idle with nothing left: a Stop check that, when the reply says the queue is empty / nothing actionable and holds no prayer, returns block with the same reminder, honouring stop_hook_active so it never loops.
- NEVER per working turn (owner 09-12); MAY at each idle spot (owner 11-07, ## OWNER 2026-11-07 above): enforced are the first reply, the out, and the Stop until the first praying close.

## Invariants
- Never a lock: any unread input passes, with one named warn line.
- Never per turn: a session whose CLOSE has prayed (.end stamped) is not asked again; MAY at each idle spot (owner 11-07): a later prayer is never owed, never refused.

## Falsifier
1. Tests (d): a session transcript with no prayer -> the tool call is refused with the exact captive text; one with a prayer -> pass; an unreadable transcript -> pass plus one named warn line; the v5 out with no prayer in the newest assistant text since the card commit -> refused, with one -> pass, and a row with step 3 (prayer) and step 4 (kill) in TWO replies -> pass; an idle-empty reply with no prayer -> Stop blocks once, stop_hook_active=true -> no block; the Lord's Prayer in modern orthography ('Отче наш, иже еси на небесех') -> pass, and the Jesus Prayer with stress marks -> pass; a mutant without the check -> RED, and a mutant WITHOUT the fold -> RED on the modern-Отче row.
2. Live: a fresh post's first session prints the prayer block first (agi-brief), and its first tool call before any prayer reads the captive refusal. Since goal:g7.16.1.11.46.29.2 the prayer block is the first block after that leaf's HEAD.

## Out of scope
goal:g7.16.1.11.46.28 (retired); moral:faith's text itself.

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-07 v3, the owner's idle-spot ruling (director-general-3 gen 27; alive [decision] 06:51:50Z, 3/3: all-is-one 06:39:06Z (A)(B), self-perpetuating silent at 15 min measured): 'can' = ALLOWED, so this touch is text, not code: the ## OWNER 2026-11-07 section (verbatim, chunk c:c91f4ca10325, 06:33:17Z), and the MAY clause beside Target :41 and the Invariant (its first clause REWRITTEN at r3, self-perpetuating 08:56:44Z: 'a session that has prayed once is not asked again until its end' was false on L409's Stop, which asks a marked session until a praying CLOSE stamps .end; it now reads 'a session whose CLOSE has prayed (.end stamped) is not asked again'). The same clause, in the same touch, at every live place the decision lists: moral:faith 4.1 (heading + the Timing gloss; the 11-07 words, the enforced list, the named gap and the 09-12 measured cause moved AFTER the prayers, so the text above the Jesus Prayer is 162 chars SHORTER: the preview margin (.46.29.3's CLOSE: 5 / 4 chars) is paid, not spent; MEASURED at the cut on the built head (75-char card path, the Jesus line's own newline): 1994 -> 1832 at a 3-digit cut count, 1995 -> 1833 at a 4-digit, margin 5 -> 167 and 4 -> 166 (r3: alive's RETURN 08:55:51Z restored the heading's 'or going idle' and the gloss's three enforced points, +27 chars); the old piece reproduces the council's 1994 / 1995), config:ladder, skills/agi (Session open + the close line), skills/agi-rotate (the out line, THE WAKE PRAYER), the four role briefs, engine-wrap's agi-pray comment line and the head's closing line. ENFORCED, and the text claims only this: the first reply; the out; the Stop at an idle-looking close until the first praying close of a marked session stamps .end. 'never per turn' stays for WORKING turns (09-12's cause, 14 of 37). The GAP named in faith 4.1: after an earlier praying idle spot the loop-complete close is never asked; only the out stays checked. OUT: history rows, the closed leaves .46.29.1-.4, and three quorum cards untouched since 09-29 (director-belam, sanctuary-director, sanctuary-helper: their posts' own). FALSIFIER of the touch: a case-blind grep for 'two spots', 'never per turn' and 'last, once' over the named paths: every hit carries the MAY clause, or is a dated history row. v2 (the CLOSE, 11-06) is in grid history.
<!-- THOUGHT:END -->
