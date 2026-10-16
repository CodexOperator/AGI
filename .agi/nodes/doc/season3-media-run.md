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
- SAMPLES row, settled (director-general-3): <= 0.38 (account delta, OPENROUTER_ADMIN, 05:24:0xZ .. 05:58:33Z, stopped at 172.4783; the start read has 2 decimals so the delta is 0.363 .. 0.373; may include other spend). Running sum for Fm3: <= 2.886.
- The owner's pick (belam 06:23:29Z, goal:g5.4.2 8488cf592a): BILL IS CLOSE, not yet: lower, a rancher sitting down after a morning out, quiet and booming, calm confidence. A second sample round follows.

## Round 2 samples (council 06:26Z 10-16)
STEP 0 (0 spend, no key; read 06:2xZ-06:3xZ, files in /data/work/director-general-3-media/season3/r2):
- Listing: https://openrouter.ai/api/v1/models?output_modalities=speech and https://openrouter.ai/api/v1/models/elevenlabs/eleven-v4/endpoints. supported_voices for elevenlabs/eleven-v4 = 21 preset names ONLY: george sarah adam alice bella bill brian callum charlie chris daniel eric harry jessica laura liam lily matilda river roger will. No other ElevenLabs voice id is listed; supports_voice_cloning false. The listing gives NO per-voice description (names only), so there is no listed description to quote. The model description: "most expressive model, with inline audio tags for emotional and delivery control". OpenRouter's pricing page shows 50% off to 10-19 (price 0.00004 per character, listing prompt price).
- OpenRouter docs: https://openrouter.ai/docs/guides/overview/multimodal/tts.md (the `instructions` field is "Ignored by other providers" than OpenAI/Gemini/Fish, so it does nothing for Eleven) and https://openrouter.ai/docs/cookbook/audio/push-to-talk-button.md (Eleven v4 Turbo: a tag is a word in square brackets at the start of the text, examples [warmly] and [curious]; "steer pacing with audio tags"; the spoken text must not show the tag). NO OpenRouter doc names a low or slow tag for this model.
- The vendor's own public page, https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices (section "Prompting Eleven v4"): "Writing tags that clearly describe the voice quality you want (e.g. [low, gravelly voice] ...) helps"; its long-form narration example opens `[Low, steady voice, restrained urgency]`; it warns a tag can be read as a sound effect and that tags are not perfect. By the council's rule (OpenRouter docs only) the tagged take is DROPPED; if the council accepts the vendor page, the one tag is `[Low, steady voice]` (no "gravelly"). The decision is the council's.
- Count for step 2: 3 plain takes (3 requests) + 1 tagged take only if the council accepts the vendor tag (4 requests).
STEP 1 (LOCAL, 0 spend, 06:33Z): source bill take sha256 d172b5016a7077c697c2a2b88d3b3ce3dbfe99a50da66eed2c6305f75604c772 (mp3, mono, 44100 Hz, 128 kb/s, 23.876 s). Decode: `ffmpeg -i sample-bill.mp3 -c:a pcm_s16le -ar 44100 -ac 1 bill.wav`. Filter per file (ONE distinct filter string except pitch and formant): `rubberband=tempo=1:pitch=P:formant=F:pitchq=quality`; encode once: `ffmpeg -i X.wav -c:a libmp3lame -b:a 128k -ar 44100 -ac 1 X.mp3`.
- bill-p2-formant-kept: pitch 0.8909, formant=preserved, sha256 daabf4a71ee24283eebac1f04dd35a76d899c25401f921b30105ff5d111ac234, 23.876 s
- bill-p3-formant-shifted: pitch 0.8409, formant=shifted, sha256 3af1cad1cfe816a15c8a40b82755aca3a4c7305a971970d5e812ac5fc64f81d0, 23.876 s
- bill-p4-formant-kept: pitch 0.7937, formant=preserved, sha256 140ddcf9926e5947d67db7a21a297b5948d2ac21caae3a66f6be25b34f267744, 23.876 s
- Measured median f0 (autocorrelation, voiced frames): source 141.6 Hz; p2 127.0 (x0.897); p3 120.3 (x0.850); p4 112.7 (x0.796): the pitch moved as asked, the duration did not.
- Files: /data/work/director-general-3-media/season3/r2/*.mp3. Not yet heard; the owner listens.

