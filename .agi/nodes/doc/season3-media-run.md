---
id: doc:season3-media-run
type: doc
mint_id: 1d0975bd751d4de79f6df747236b00c7
parents:
- goal:g5.4.2
next_edges: []
key: 3dbc163531a12b56
schema: doc@5d9146e2fcfd
title: season3-media-run
tags:
- media
- season3
- run-record
origin: doc-version
---

# doc:season3-media-run: the run record of goal:g5.4.2

Times come from `date -u` or a file's own mtime, never from memory. Spend rows follow the council's Fm3 USAGE rule (05:48Z 10-16): the account /credits delta is the upper bound; a per-key read of zero while the delta is positive is logged as counter lag, never as spend zero.

## Keys and spend
- Before the first mint, belam revoked the two old media keys (limits 15 and 25, usages 2.502 and 0.004): season-3 media spend before this run = 2.506.
- Run cap = 22 (the owner allows up to 25 in total). Stage keys: samples 0.50, voice 8, a second voice pass 8, music 2; the reserve of 3.50 stays unminted.
- SAMPLES key: minted 05:42:29Z, limit 0.50, expires_at 06:42:29Z (read back non-null); revoked 05:46:54Z (deleted); live media keys afterwards = 0 on both accounts.
- SAMPLES row (belam, 05:48:40Z): <= 0.29, window top-up read .. 05:48:20Z (account delta, OPENROUTER_ADMIN, may include other spend by the Default key). Per-key usage read 0 before, after and at revoke: counter lag. Settle reads at +10 and +30 minutes are belam's.
- Running sum for Fm3: 2.506 + <= 0.29.

## Samples (Fm3 sample rows)
- Text: the council-approved fixed text, 344 characters, sha256 d7a6c56394fdb5553a4e8d564c56c474da53a243faea834952cea475db46edd8; the text sent had 1 distinct sha256 across the 3 voices.
- Run time: 05:45Z (file mtimes 05:45:16Z, 05:45:21Z, 05:45:26Z), model elevenlabs/eleven-v4, response format mp3, 3 voices x 1 take, no retry, no error.
- george: 22.8 s, sha256 a5000ad937d3c556cc18d666817fb1a18d3d475b71c9d788ee33f70e1d50c86a
- bill: 23.9 s, sha256 d172b5016a7077c697c2a2b88d3b3ce3dbfe99a50da66eed2c6305f75604c772
- brian: 21.9 s, sha256 7580fa7fa14907dd5e9d8d0195978b691cc1061f7d289a7fdd383cbfb58b1640
- The owner picks one name via belam; the pick is recorded here when it arrives.
