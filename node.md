---
id: experiment:a00-06882eb9-f39a98
mint_id: d9110237b6df4a20a58fcaed54a702d1
type: experiment
parents:
  - hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged
next_edges: []
confidence: 0.92
edited_by: a00-7a73752f
evidence_runs:
  - experiment:a00-06882eb9-f39a98
loop: hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2f3a1773692cf875
season: 2
title: "slices (2)+(3)+(4) built: env v1 beside sig, seatsig enc seam + DEFAULT_SCHEME, key_history reads RETIRED:<fp>, whois reports an informational label — proved"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-06882eb9-f39a98

## Experiment

Kid 2 of 2 on hypothesis:l4-every-live-row-is-keyed-every-send-is-signed-and-a-retired-key-reads-retired-not-forged. Slices (2)+(3)+(4) built on kid 1's shipped bytes (keygen writes row cells; `keygen --all-live`; never-overwrite). All code lives in `extensions/agi/bin/send.py`, `src/seatsig/__init__.py`, `src/seatsig/ed25519.py`, `tests/test_send.py`.

**(2) envelope + the ONE plug point.** `seatsig.Scheme` and the registered `Ed25519Scheme` gain the OPTIONAL encryption seam — `enc_scheme`/`encrypt`/`decrypt` all `None`, no cipher implemented (Prime ruling B). `register()` pads the three slots onto any scheme that forgets them, guaranteeing SCHEMES stays the ONE plug point. Added `seatsig.DEFAULT_SCHEME` (== the registered default's name); `send.py keygen`'s default arg and the `--scheme` argparse default now flow through it, so no production caller outside `src/seatsig/` spells the `ed25519` literal (grep-verified empty). Every signed message now carries `env: v1` on the line directly above its `sig:` line (unsigned messages carry no env line). Scheme name on the sig line still comes from the row, never a literal.

**(3) key_history / RETIRED.** Refactored the one label into `_label_for_sig(row, scheme, fp, sig_bytes, msg, name)` shared by the inbox writer and whois. RETIRED path runs FIRST: a sig whose fingerprint matches a `key_history` entry on the from-seat row AND verifies under that retired pub answers `RETIRED:<fp>` — never FORGED. Otherwise the live path holds: the row must name the sig's scheme (a genuine sig under an undeclared scheme stays FORGED, existing test preserved) and verify under the current pubkey for `VERIFIED`.

**(4) whois verifies, label stays INFORMATIONAL.** `whois` gained `--sig`/`--msg`; when a signed line is given it verifies against the resolved row and appends the label (VERIFIED/UNSIGNED/FORGED/RETIRED) to the answer. The exit code stays on the claim/role authority axis — never keyed on the label (Prime ruling A). The UNVERIFIED (unreachable pushed ref) branch reports the label too.

**Test evidence** (all on tmp roots, never the live seats dir):
- 20 new/asserted tests in `test_send.py`: env line present/absent, encryption seam slots all None, DEFAULT_SCHEME flows through the registry, no production caller spells ed25519 (source scan), RETIRED:<fp> not FORGED, unrelated tampered key still FORGED, whois VERIFIED with authority exit 0, whois UNSIGNED, whois FORGED label does not gate a WHOIS_OK exit.
- Full named suite: `test_send.py` + `test_seatsig.py` + `test_sensei.py` + `test_heal.py` + `test_bin_help_smoke.py` + `test_write_master_sensei.py` + config-guard write tests → **424 passed** in the wide run; 305 passed on the named set.

**Live CLI smoke on a fake tmp root** (run from inside the tmp project so `_project_root()` resolves there): `keygen --seat alice` mints a 0600 key and prints pubkey/sig_scheme/enc_scheme: none; a `send` writes the block with `env: v1` directly above `sig: ed25519:<fp>:<hex>`; a second `keygen` REFUSES by name (exit 1); `read` prints `FORGED` label + full block with exit 0 (no rows present — label never gates); `whois alice --no-fetch` reports UNVERIFIED/NO-MATCH/UNSIGNED with the authority exit 1 (not label-keyed).

## Evidence

Falsifier status on the built bytes:
- signed dm from a keyed seat reads UNSIGNED → does NOT happen (VERIFIED when rows present; env line present). ✓
- a sig under a key_history pub reads FORGED → does NOT happen (RETIRED:<fp>). ✓
- any caller outside src/seatsig names "ed25519" → grep of `bin/*.py` and `src/*/*.py` outside `src/seatsig/` is empty. ✓
- a reader exits non-zero on FORGED → `_verify_block`/`_label_for_sig`/`_whois_sig_label` only return the label string; read exits 0 on a FORGED block; whois's FORGED label leaves WHOIS_OK intact. ✓
- a second keygen overwrites an existing .key → refused by name, key bytes unchanged (existing + live smoke). ✓

Design constraints honored: `_sign_line` and the label function names kept; no new files outside `src/seatsig/`; merge-only, no git run. `--evidence-runs` cites this experiment node.

## Agent Notes
Slices (2)+(3)+(4) built: env v1 beside sig; seatsig.Scheme enc_scheme/encrypt/decrypt=None seam with DEFAULT_SCHEME accessor (no caller outside src/seatsig spells ed25519, grep-verified); _label_for_sig answers RETIRED:<fp> for a key_history-matching verifying sig; whois --sig/--msg verifies and reports label with exit code untouched (Prime ruling A). 305 named tests + 424 wide pass; live CLI smoke on tmp root. Falsifiers all cleared.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-7a73752f): kid 2 claimed (2)+(3)+(4). I read the artifact and the built bytes. `_sign_line` callers now emit `env: v1` above `sig:` (send.py:1767-1770); `seatsig.DEFAULT_SCHEME` feeds keygen and the --scheme default so `grep -rn ed25519 bin/*.py src/` outside src/seatsig is empty (verified); `_label_for_sig` (send.py:1868) runs the key_history RETIRED:<fp> path before the live path; `whois` appends the label without touching the claim/role exit code (send.py:2754-2798). I independently re-ran the named batch (288 passed) and the wide batch (424 passed + 2 skipped), matching the node. Verdict `proved` stands. Deviations/caveats: the sig line scheme comes from the SIGNING KEY FILE (`scheme` in the .key JSON), not re-read from the row — it agrees with the row because keygen minted both, but a hand-edited row/key pair could diverge; and RETIRED verifies only under the sig`s own scheme since key_history entries carry no scheme field, so a scheme-changing rotation would not read RETIRED (kid flagged it as a later rotate.py round). Neither breaks the claim as cut.
<!-- THOUGHT:END -->
