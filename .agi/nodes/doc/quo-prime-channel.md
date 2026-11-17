---
id: doc:quo-prime-channel
mint_id: b7b735924630414aa6987aab2ef8ed15
type: doc
parents:
  - goal:g7.16.1.11.48
next_edges: []
edited_by: self-perpetuating
season: 3
tags:
  - quo
  - owner-reach
  - council-design
title: "The Prime's own phone line to the owner through Quo: SMS now, voice later (design for goal .48; the owner sees it before anything is wired)"
town: core
---
# doc:quo-prime-channel

A council design (goal:g7.16.1.11.48). Drafted by self-perpetuating; alive and all-is-one word it. Nothing here is wired: no Quo account, number, key or webhook is touched until the owner has read this doc.

## The owner's words (c:696556deb72a, verbatim, as goal .48 carries them)
"Separately, I also got a quo subscription so we could integrate actual texting and later even calling into the flow. We could let Prime have an exclusive channel to me via phone directly at any time. Quo has websocket things and other deep programmatic integrations"

## The shape in one paragraph
belam, and only belam, holds the one Quo API key and the one owner number. belam SENDS a text with the v1 send endpoint (POST /v1/messages, SMS only, 1-1600 characters, US and Canada) and READS the owner's replies by polling the list-messages endpoint about once a minute. Reading needs no open port on this box: every call goes out over HTTPS, nothing comes in. A webhook (Quo calls us when a text arrives) is the faster, later version. It waits on goal:g7.16.1.11.47, because it needs a public HTTPS address on this box, which the network design decides. Every other post reaches the owner exactly as today: through belam.

## Who holds what
- The key: created by the owner in the Quo app (Workspace Settings, API tab; owner or admin only). Each key has full access to the workspace's API, so it is handed over inside a capsule (the owner's P10 ruling: a real key rides only in a capsule) and kept in belam's own env file, readable by belam's uid alone. It is never written into the graph, a card, a box message or a commit.
- The owner's number and the Prime's Quo number: belam's env file too, never in the graph. The graph says 'the owner's number', never the digits.
- No other post, kid or workflow gets the key or the numbers. A post that wants the owner sends belam an [owner]-tagged box message, as today, and belam decides whether it is worth a text.

## May be sent
- ALARM: a red that needs the owner now (a host down, a spend line crossed, a seat dead with no successor), one line plus the node or goal id it is about.
- ASK: a decision only the owner can make, banked with its options and belam's recommendation (the card's BANKED row), so the owner can answer with one letter.
- NOTE: a landing or a loop close the owner asked to hear about, on request only, never by default.
- DOWN: the other route (Remote Control) is dead and belam cannot reach the owner any other way.
- Every text is plain GSM-7 (ASCII letters, digits, basic punctuation: no em dash, no middle dot, no emoji, no curly quotes), so one segment carries 160 characters, not 70. Aim for one segment; never more than three.
- Each text ends with a short reference (R1, R2, ...) so a reply can name what it answers.

## Never sent
- No key, token, signing secret, password or private key, in any form, whole or in part (not even a hash prefix).
- No private address: no IP, hostname, port, home path or internal URL.
- No owner chunk body: a chunk is cited by its c: id, never quoted back to the owner's own phone.
- Nothing another post wrote, pasted whole: belam writes each text in its own words.
- Nothing from inside a capsule.
- No link the owner would have to open to act on the town.
- No instruction the town would carry out without belam's judgment: a text is a message, never a command line.

## Replies
- A reply counts only if it comes from the owner's number. A text from any other number is dropped unread; belam logs a count and the time, never the text.
- An accepted reply is the owner's words: belam stores it verbatim as an owner chunk (its own c: id, as pane words are) and acts on it under its usual rules. It never goes straight to another post; belam relays it, citing the chunk id.
- A reply that names a reference ('R2 B') answers that ask. A reply with no reference is read as a new owner message.
- SMS sender ids can be spoofed. So a reply that would start something irreversible, spend money, or change a key is CONFIRMED on a second route (the owner's pane or Remote Control) before belam acts. The text alone is never enough for those.
- Polling: about once a minute, reading only messages newer than the last one handled, so a reply is seen within about a minute. The later webhook version must check Quo's signature (HMAC-SHA256 over the delivery id, timestamp and raw body), refuse a delivery more than five minutes off the clock, and drop a repeat by its delivery id (Quo retries a failed delivery for about 27 hours and does not keep order).

## Rate and cost
- Price, from Quo's API pricing page: 1 US cent per segment to US and Canada; other countries add a per-country rate. Only outgoing API texts are charged; reading and polling are free. One non-GSM character drops a segment from 160 characters to 70, which is why the 'Every text is plain GSM-7' line above matters.
- Billing: API texts draw on prepaid credits. With too little balance the send is refused, not billed later. Proposed: a small credit balance with auto-recharge OFF, so a runaway loop stops at the balance instead of at the card.
- Send rate, belam's own limits (Quo allows 10 requests a second per key, with no daily quota, far above this): at most 3 texts an hour and 20 a day; ALARM may break the hourly limit, never the daily one. Past the daily limit belam stops texting and falls back to the other route.
- Polling at once a minute is about 1,440 read calls a day, all free and well inside the limit.
- When the channel is down (an error back from Quo, an insufficient-balance refusal, no reply route): belam falls back to the existing route, notes the miss on its card, and retries a failed send at most once. A repeated text costs money and attention.

## Open for the owner (before anything is wired)
- Create the API key yourself (it needs owner or admin in the Quo app) and hand it over in a capsule.
- Texting US numbers may need US carrier registration (A2P 10DLC). Quo's API has registration endpoints, but the pricing page read on 11-17 does not say whether it is required for this use. Please check in the app.
- Websockets: the public API docs read on 11-17 show REST endpoints and webhooks, and no websocket API. If you meant a specific integration, please name it.
- Voice: out of scope here. It is the later version of this leaf.

## Sources (Quo public docs, read 11-17; no login)
- https://www.quo.com/docs/mdx/api-reference/messages/send-a-text-message
- https://www.quo.com/docs/mdx/api-reference/rate-limits
- https://www.quo.com/docs/mdx/pricing-support/pricing-overview
- https://www.quo.com/docs/llms-full.txt (authentication, webhook signing and retries, A2P endpoints)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating gen 76, 11-17: first draft, as the council's split placed it (alive's [decision] 05:16:06Z: one seat drafts, the other two word). Two choices are not in the leaf. (1) Replies by POLLING, not a webhook: a webhook needs a public HTTPS address on this box, which goal .47 decides, and polling opens no port. (2) Spoofed SMS: a reply that would start an irreversible act, a spend or a key change needs a second route. The leaf says only the Prime receives; it does not say the sender is really the owner. Every Quo figure is from the public docs listed, read 11-17. A2P need and websockets are named as NOT confirmed, never guessed.
<!-- THOUGHT:END -->
