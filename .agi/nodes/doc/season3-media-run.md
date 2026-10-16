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

## Round 2, voices and custom voice (council 06:36Z-06:39Z; read 06:3xZ-06:4xZ, 0 spend, no key)
VENDOR PAGES for the preset names (files in /data/work/director-general-3-media/season3/r2, the vend folder):
- https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-default-voices.md only maps old Default voice names to new ones (Roger -> "Darian - Warm Grounded Storyteller", Charlie -> "Baxter - Dry Calm Aussie", Callum -> "Kellan - Casual Friendly Speaker", Harry -> "Kaelen - Amateur Warrior", Liam -> "Lawrence - Bright and Informative", Will -> "Warren - Effortless and Cool", Eric -> "Eddie - Helpful and Comforting"); it quotes no description of the old voice itself, and Adam, Brian, Bill and Daniel are not in it. Default voices expire 2026-12-31.
- https://elevenlabs.io/voice-library/adam is a library entry named "Adam - Dark Storyteller" (voiceId IRHApOXLvnW57QJPQH2P, description "Adam - Brooding, Dark, Tough American - A tough hero, weathered by years of experience. American accent."). That voice id is a library voice, NOT shown to be the preset OpenRouter calls adam, so it is not used as the preset's description. The pages for roger, daniel, eric, callum, charlie, chris, will, harry, liam, river return 404 under /voice-library/NAME.
- Result: NO vendor page describes the OpenRouter presets by name. By the council's fallback (06:37Z, all-is-one's merge 3/3): adam, roger, eric, labelled "named by the council from the preset names; no listed description". Third-party mentions, NOT vendor pages and not used as listings: json2video.com quotes ElevenLabs's label for Roger "Laid-Back, Casual, Resonant"; voximplant.com lists Eric as "male, middle-aged, American, friendly, conversational".
CUSTOM VOICE on OpenRouter (read, 0 spend): the `voice` field takes a name from the model's supported_voices (the cookbook's error: `Unknown voice "alloy".` -> "Use a name from the model's `supported_voices` list"); elevenlabs/eleven-v4 lists 21 names and its endpoint has supports_voice_cloning false, so a custom ElevenLabs voice_id and `input_references` clips are NOT accepted there. Speech models whose endpoints say supports_voice_cloning true: bytedance-seed/seed-audio-1-0 (also multiple clips and a scene image; voice design accepts an image only), fish-audio/s2.1-pro-free:free, fish-audio/s2.1-pro (clone from one clip; delivery tags in square brackets; listing price 0.000015 per character). A custom ElevenLabs voice therefore needs the owner's ElevenLabs account and API key and calls ElevenLabs directly, not through OpenRouter.


## Seed Audio 1.0 parameters (council ask 06:46Z; read 06:4xZ from https://openrouter.ai/docs/guides/overview/multimodal/tts.md and the models API; 0 spend, no probe)
- BOTH witnesses are right, they describe two modes. (1) TEXT PROMPT: "Seed Audio 1.0 instead treats `input` as a prompt that is forwarded unchanged to the model, so it can describe the delivery of the speech, or describe sound that is not speech at all ... Omit `voice` and `input_references` when you want the model to infer everything from the prompt." (2) IMAGE: "Seed Audio's voice-design mode accepts only an image, with no `input_audio` clips alongside it" (exactly one image_url part). (3) CLONE: up to three input_audio clips with `@Audio1..3` placeholders. `voice` is "a Seed speaker ID" and a request that sends both `voice` and `input_references` is a 400; the models API lists no speaker ids (supported_voices empty).
- NOT documented: how a prompt separates the words to be spoken from the description of the voice, so whether a designed voice can be asked for by text and made to read a fixed script is UNKNOWN from the docs; only a paid call would show it (the council said no paid probe to settle it).
- Limits: `input` <= 3000 characters, `speed` 0.5 to 2.0, audio <= 120 s per request, no provider options. Price is PER SECOND of audio: pricing.completion 0.0025 per second, so 30 minutes of audio is about $4.50 and 60 minutes about $9.00, not per character.
- Other described-voice routes: fish-audio/s2.1-pro puts `instructions` into the text as a square-bracket direction at the start (delivery, not a voice identity; listing 0.000015 per character); google/gemini-3.8-flash-tts takes `instructions` as a style on one of 30 NAMED voices (Zephyr, Puck, Charon, Kore, Fenrir, Leda, ...; pricing prompt 0.0000005, completion 0.000009), so it styles a preset, it does not design a voice.

## Round 2, step 2 RESULT (director-general-3; key dg3-g5.4.2-round2-20261016, hash 79630642ff, limit 0.50, expires_at 2026-10-16T07:43:34Z; script season3/r2/step2.py; log season3/r2/requests.log)
- Run 06:44:20Z .. 06:44:43Z (`date -u`), model elevenlabs/eleven-v4, mp3, 4 requests, each logged before it was sent, NO retry, NO error. The voices adam, roger, eric are "named by the council from the preset names; no listed description" (no vendor page describes the presets).
- Per-key reads (the key's own /key): before 06:44:21Z usage 0, after 06:44:43Z usage 0 = counter lag, never spend 0. Settled usage is belam's: disable at this return, reads at +1 h and +3 h until two agree, then delete.
- Generation ids (for the optional /generation read): adam gen-tts-1792133062-TWp5su6vDKCdnNMaSOLU, roger gen-tts-1792133067-xF8ZyZjnIR3hQRaeZVQ5, eric gen-tts-1792133073-ijHn5YQOkYWFYGZK6jWV, bill-tags-low gen-tts-1792133078-0jJp6LcGkYMlJcazxTtk. GET /api/v1/generation?id= with the round-2 key returned HTTP 404 for all four at 06:45Z: the cost for each take is MISSING (never 0); retry once at the settle.
- adam-plain.mp3: 22.67 s, 363249 bytes, sha256 c611530fe776199a47b7deabfad34e9f75e21d45d3054ea18c9133eaa165a885, text sent sha256 d7a6c563...edd8 (344 characters). Median f0 132.2 Hz.
- roger-plain.mp3: 22.52 s, 360741 bytes, sha256 168d877ce202eda8bc719abe9f5e6c4c95813ddcd09c0564a7a405147899d914, text sha256 d7a6c563...edd8. Median f0 121.7 Hz.
- eric-plain.mp3: 21.47 s, 344023 bytes, sha256 80846350704c63e3483423ddfd72ea8a94cd00a76186ec750eefbf550857d287, text sha256 d7a6c563...edd8. Median f0 148.1 Hz.
- bill-tags-low.mp3 (THE TAGGED TAKE): bill + the prefix `[Low, steady voice] ` + the approved text (364 characters sent), sent text sha256 3e5afc05c64d4141c0d0c6493a724557cf34f0100cf9c39206865e3e747ea2a7; 23.33 s (plain bill 23.88 s: the take is shorter, not longer by a spoken tag), 373698 bytes, sha256 9d455587f3a7bd75733036669dc89b5dc557c446e81731461ea624774b965111. Median f0 124.0 Hz (plain bill 141.6). Not heard by me: the owner listens for a spoken tag or sound effect.
- Reference points (autocorrelation f0, voiced frames; not a listening): plain bill 141.6; the round-2 local files 127.0 / 120.3 / 112.7.
