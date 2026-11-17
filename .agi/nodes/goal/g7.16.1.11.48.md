---
id: goal:g7.16.1.11.48
mint_id: 9b5a7992cd2848bcb5be2dd88062988f
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.48
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: prime_director
scaffold_hash: 86469f3bfbeb12a1
season: 3
seeds: []
status: active
tags:
  - quo
  - owner-reach
  - council-design
title: "G7.16.1.11.48: a Prime-exclusive phone channel to the owner through Quo (SMS, voice later), designed by the council and seen by the owner before any account is wired (owner 11-15, P2)"
town: core
---

# goal:g7.16.1.11.48

## Why this exists
goal:g7.16.1.11 (the season bundle): the owner reaches the Prime today only through a Remote Control link or another post's relay. On 11-15 a Remote Control link dropped for hours with nobody healing it (the sibling network leaf, Q1). On 11-15 the owner added a Quo subscription so the Prime has its own phone channel. sanctuary-master placed it as P2 (19:39:37Z 11-15, 3/3), a sibling of the network leaf (both are the owner's reach from the phone); belam mints it.

## OWNER 11-15 18:57:53Z, verbatim (relayed whole by meme-master [owner], in the same chunk as the 8 answers; owner chunk c:696556deb72a)
"Separately, I also got a quo subscription so we could integrate actual texting and later even calling into the flow. We could let Prime have an exclusive channel to me via phone directly at any time. Quo has websocket things and other deep programmatic integrations"

## Target end-state
- A design doc node, doc:quo-prime-channel, states the Prime-exclusive SMS channel (voice later) between belam and the owner through Quo. It says what may be sent (secrets never: no key, token, private address or owner chunk body), how a reply reaches the Prime (and only the Prime), and how the [owner] / alarm grammar reads on a phone. It also names the send rate, the cost bound, and what happens when the channel is down.
- The design is a council decision (three lenses). The owner sees it before any account, number or webhook is wired.

## Invariants
- No Quo account, API key, number or webhook is touched in this leaf: it designs, it does not wire.
- Only the Prime sends or receives on the channel; another post reaches the owner through the Prime, as today.
- The owner's words above are quoted, never paraphrased.

## Falsifier
1. `D=.agi/nodes/doc/quo-prime-channel.md; test -f $D && for h in '## May be sent' '## Never sent' '## Replies' '## Rate and cost'; do [ "$(sed -n "/^$h/,/^## /p" $D | grep -cv '^## \|^$')" -ge 1 ] || { echo "EMPTY $h"; exit 1; }; done` exits 0: each of the four sections exists and is non-empty.
2. `grep -Eq '^owner seen: c:[0-9a-f]{12}' .agi/nodes/doc/quo-prime-channel.md` exits 0: the owner's read of the design is cited by its chunk id.
3. `grep -c 'c:696556deb72a' .agi/nodes/doc/quo-prime-channel.md` prints a number >= 1: the design doc cites the owner's chunk (sp 04:12:43Z: pointed at the leaf's own file it could not fail).
4. Negative: `{ /usr/bin/grep -h -i -P '(api[_-]?key|_key|\bkey|token|secret)["\x27]?\s*[:=]\s*["\x27]?(?=[A-Za-z0-9_-]*[0-9])[A-Za-z0-9_-]{8,}|\b(?:[A-Za-z]{2,8}_){0,2}(?=[A-Za-z0-9]*[0-9])(?=[A-Za-z0-9]*[g-zG-Z])[A-Za-z0-9]{16,}\b' .agi/nodes/doc/quo-prime-channel.md 2>/dev/null; git grep -h -A3 -P '(?<![A-Za-z])[Qq]uo(?![a-z])|(?<![A-Za-z])QUO(?![A-Z])|(?i:openphone)' -- . ':!.agi/nodes/goal/g7.16.1.11.48.md' ':!.agi/nodes/doc/card-*' ':!.agi/nodes/doc/quo-prime-channel.md' | /usr/bin/grep -i -P '(api[_-]?key|_key|\bkey|token|secret)["\x27]?\s*[:=]\s*["\x27]?(?=[A-Za-z0-9_-]*[0-9])[A-Za-z0-9_-]{8,}|\b(?:[A-Za-z]{2,8}_){0,2}(?=[A-Za-z0-9]*[0-9])(?=[A-Za-z0-9]*[g-zG-Z])[A-Za-z0-9]{16,}\b'; }` prints nothing: no Quo / OpenPhone credential in the design doc (scanned WHOLE) or anywhere else in the tree (a quo / openphone line and the 3 lines after it, so nested yaml counts; nodes included; the leaf and the cards excluded). A credential is a NAME (api_key / *_KEY / key / token / secret) assigned a value of 8+ chars holding a digit, or a VALUE shape: a 16+ run with a digit and a letter OUTSIDE hex, after at most two short prefixes like sk_live_. Quo = Quo, quo, QUO or quoApiKey, never quote / QUOTE. RE-CUT 3 (aio + sp + alive): a correct doc's mint_id, scaffold_hash, '- quo' tag and a SHA beside Quo read 0. RE-CUT 4 (aio 04:28:57Z): the Never-sent prose ('API key: kept in belam env file only', 'token: never', 'secret = none of them ride in a text', 'Webhook signing key: rotated by belam') reads 0; RED on api_key = Zx9Q2mK7pL4vN8rT and OPENPHONE_API_KEY=k3yv4lu3 and a bare mixed token in the doc, QUO_KEY=Zx9Q2mK7, quo: / api_key: "a1b2c3d4", const quoApiKey = "Ab12cd34Ef", a Quo sk_live_ token. The trades, named: a placeholder (QUO_KEY=x) and an all-hex or all-letter key with no digit-bearing value read 0.

## Out of scope
goal:g7.16.1.11.47 (the town network design) · the send guards' key rule (P10, waits on the capsule leaf) · voice calls (a later version of this leaf)

## Agent Notes
Assigned to **belam**.
