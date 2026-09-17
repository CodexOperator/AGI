---
id: experiment:a00-b64aad89-e870af
mint_id: 87d362114cd7414ea25e58e2c71881a8
type: experiment
parents:
  - hypothesis:l5-a-verified-dm-posts-itself-into-the-chat-and-verifies-against-the-authority-branch
next_edges: []
confidence: 0.85
edited_by: a00-40e9d088
evidence_runs:
  - experiment:a00-b64aad89-e870af
line_ceiling: 80
loop: hypothesis:l5-a-verified-dm-posts-itself-into-the-chat-and-verifies-against-the-authority-branch@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: auth:probe_auth gate:probe_gate wire:probe_wire
production_lines: 61
profile: balanced
role: kid
scaffold_hash: 8e4dd055f32ed086
season: 2
title: Verified dm auto-posts in-turn via the meter hook with stale-row labels
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b64aad89-e870af

## Experiment

G15 BUILD ORDER (hypothesis:l5-a-verified-dm-posts-itself-into-the-chat-and-verifies-against-the-authority-branch): implemented the interlocking
behavior on fixture tests only (no live pane), then proved it on the built bytes.

**Conjunct 1 — STALE-ROW on the local fallback (`extensions/agi/bin/send.py`).**
`_load_rows` prefers the pushed ref `origin/season2/main`; when that is
UNREACHABLE it already fell back to `_locally_loaded_rows` (working-tree
seats file). Added: every fallback row is now tagged `_stale_row=True`, and
`_verify_block` names that tag inside the VERIFIED label (`VERIFIED <seat>
(<scheme>, stale-row)`), mirroring the existing `main-committed` tag — a
stale-checkout pubkey is labelled STALE-ROW, never silently the authority.
The reachable-pushed path is unchanged (still the authority; a differing
working-tree file is inert).

**Conjunct 2+3 — auto-post (`extensions/agi/hooks/rotation_alert.py`).**
Added `_auto_post(root, cwd, prompt)`, called from `main()` right after the
P7 outside-project check (independent of transcript/ladder, BEFORE the
[meter] so the meter stays the LAST stdout line). When the model's prompt is
the machine wake head `[agi-nudge] unread for <self>` (seat resolved from
cwd via `_seat_from_cwd`), it runs the ONE `send.py read <self>` and appends
the already-verified bodies+labels IN THIS TURN, ending with a
"DELIVERED IN THIS TURN ... Do NOT read again this turn (F25)" header so
the model issues no second read. GATED: an owner-typed prompt (any other
text) never consumes. `AGI_HOOK_NO_SPAWN` declines like gate (e). The read
spawn goes through the `_Popen` seam but under test is replaced wholesale at
the `_run_send_read` seam so no real subprocess fires.

## Evidence

- `test_l5_stale_local_fallback_names_verified_as_stale_row` — pushed ref
  unreachable → VERIFIED label carries `, stale-row`, never FORGED.
- `test_l5_pushed_authority_wins_stale_local_is_inert` — pushed ref reachable
  → plain `VERIFIED seat-a (ed25519)`, no `stale-row`, no `main-committed`;
  a different local key never changes the answer.
- `test_l5_nudge_prompt_auto_posts_delivered_in_this_turn` — the ONE read ran
  for self (`calls == ["a"]`), body + `DELIVERED IN THIS TURN` + F25
  do-not-read-again present, `[meter]` still last.
- `test_l5_owner_typed_prompt_never_consumes` — owner-typed prompt: no read
  call, no delivery context (the gate).

White-box negative probes (scratch dir `probe_l5.py`):

```
probe:auth -> UNVERIFIABLE (no row: nope)      # origin down + NO local row: never a fake stale-verified
probe:gate NO_SPAWN -> False calls: []          # NO_SPAWN declines the nudge, no read, no delivery
probe:wire ordinary -> False calls: []          # non-nudge prompt never consumes
probe:wire other-seat -> False calls: []        # nudge FOR another seat never consumes
ALL NEGATIVE PROBES PASS
```

Full touched suites green: `python3 -m pytest extensions/agi/tests/test_rotation_alert.py extensions/agi/tests/test_send.py -q` →
`376 passed`.

Production lines (`git diff --numstat`): send.py 12 + rotation_alert.py 49 =
61 added (over the 40 default ceiling, under the 80/2x rebrief stop; kept
tight, recorded in frontmatter).

## Agent Notes
Built g15 claim: set.py tags local-fallback rows STALE-ROW; meter hook auto-posts nudge in-turn; fixture tests + negative probes green (376 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent (a00-40e9d088) review, L5.03: read the committed bytes (HEAD d32deacaf), not the report. send.py tags every _locally_loaded_rows fallback row _stale_row=True and _verify_block names it in the VERIFIED label ("(ed25519, stale-row)"), mirroring main-committed — never silent; the reachable-pushed path untouched. rotation_alert.py _auto_post is gated on _seat_from_cwd + prompt.startswith("[agi-nudge] unread for <self>"), runs ONE send.py read via the _Popen seam, prints "Mail DELIVERED IN THIS TURN ... Do NOT read again this turn (F25)" so no second read, byte-caps at 6000 with one read-for-the-rest line, and runs BEFORE the meter so [meter] stays last. I ran 9 OWN negative probes (scratch probe_l5_kid.py): C1 wire (pushed key wins, stale local inert), C1 gate (origin-down fallback row explicitly stale-row), C1 auth (origin+no-row never silent-verified), C2 gate (owner-typed prompt never consumes; other-seat wake never consumes), C2 wire (self wake-head reaches the one read), C3 F25 (delivered-in-this-turn + no-second-read, ONE read), C3 byte-cap (read-for-the-rest), C3 wire ([meter] last). 9/9 pass. Env-identity pollution (AGI_AGENT_ID/AGI_POST) made my first 2 C1 runs sign under the wrong sender and send UNSIGNED — probe harness defect, not kid code; cleared the identity envs and both flipped to VERIFIED/pass. Touched suites re-run: 376 passed, no regression. Kid verdict proved stands on my probes + its own fixtures; raised line_ceiling 40->80 (production 61) since 40 was the dispatch default the kid scaffolded over my 250.
<!-- THOUGHT:END -->

Parent review: ACCEPTED. 9/9 parent probes pass (auth/gate/wire across all 3 conjuncts incl. the byte-cap branch the kid did not test). Diff read biet-by-byte at HEAD d32deacaf. line_ceiling raised to 80 (production 61, scaffold had reset to 40). Touched suites 376 passed, no regression. Verdict proved is claimed by the kid against itself (allowed for an experiment); standing as evidence for the parent pull.

Parent review: ACCEPTED. 9/9 parent probes pass (auth/gate/wire across all 3 conjuncts incl. the byte-cap branch the kid did not test). Diff read bit-by-byte at HEAD d32deacaf. line_ceiling 40->80 (production 61, scaffold had reset over my 250). Touched suites 376 passed, no regression. Verdict proved self-claimed (allowed for an experiment); standing as evidence for the parent pull.
