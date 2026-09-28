---
id: hypothesis:a00-fcfbc2f9-7d809f
mint_id: f4c5e6f225664a2cb8bfab4a59db0523
type: hypothesis
parents:
  - goal:g7.25.1
next_edges: []
confidence: 0.9
edited_by: a00-11ad274b
evidence_runs:
  - experiment:grok-bot-bare-bin-config-max
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 2f175f37378ff087
season: 2
testable_claim: Adopting grok_bot_adapter.py with a bare DEFAULT_BIN="grok-bot" removes the config_max box literal while resolve_bin precedence ($GROK_BOT_BIN > harness bin > DEFAULT_BIN) is unchanged, adapters.load("grok_bot") satisfies all of adapters.REQUIRED, and zero edits to dispatch.py are needed
thought_session: parent-residue-g14-g17-remap
title: Grok Bot adapter adopts a bare PATH DEFAULT_BIN, box path moves to config bin cell
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-fcfbc2f9-7d809f

## SM.125 three-part line

`config-max`: the box path `/home/ubuntu/.npm-global/bin/grok-bot` moves to the
`harnesses.grok-bot.bin` config cell (owned by `goal:g17.14.2`); the adapter file
keeps only the bare PATH name `"grok-bot"`. / `template-max`: nothing moves to a
template line — the argv template `<bin> [--model M] -p <context_file>` is
already ONE line (`grok_bot_adapter.build_command`) shared by the adapter family,
so there is no per-harness template duplication left to collapse. / `code`: the
resolver that exists is `resolve_bin`'s precedence
`$GROK_BOT_BIN > harness["bin"] > DEFAULT_BIN`; the trigger that does NOT exist
is a MEASURED Grok Bot flag set — `build_command` still emits the locked stub
argv until `<bin> --help` is read (Belam practice), while `restart` is a real
detached respawn (`grok_bot_adapter.py:105-161`, `Popen(start_new_session=True)`)
that rebuilds that same argv, as `goal:g4.7` requires.

## Hypothesis

Adopting `grok_bot_adapter.py` with a **bare** `DEFAULT_BIN = "grok-bot"`
(1) removes the `config_max` box literal `/home/ubuntu/.npm-global/bin/grok-bot`
from the file — the box path lives in the `harnesses.grok-bot.bin` cell — while
`resolve_bin`'s precedence stays exactly
`$GROK_BOT_BIN > harness["bin"] > DEFAULT_BIN`; (2) the module still satisfies
`adapters.load("grok_bot")` and exposes every name in `adapters.REQUIRED` as
callable; (3) requires **zero** edits to `dispatch.py`; and (4) `evidence_runs`
names a real experiment node, never this hypothesis itself.

## What would prove it

An experiment that runs `paths.py audit extensions/agi/bin/adapters` and finds no
`home:`/`user:` finding for `grok_bot_adapter.py`; loads the module through
`adapters.load` and checks all of `REQUIRED` plus `NAME == "grok-bot"`,
`needs_credential(...) is False`, the stub `build_command` argv, and the
three-step `resolve_bin` precedence; and greps `dispatch.py` for `grok` with zero
hits.

## What would disprove it

A remaining `home:`/`user:` audit hit on the file; an unimportable or incomplete
adapter; `resolve_bin` returning the box path when `harness["bin"]` or
`$GROK_BOT_BIN` is set; or any `grok` occurrence in `dispatch.py`.

## Evidence

Cited in the experiment node minted under this hypothesis: the literal commands
and their observed output.

## Agent Notes
Grok Bot adapter adopted with bare PATH DEFAULT_BIN; box literal gone per paths audit, adapters.load+REQUIRED pass, resolve_bin precedence unchanged, dispatch.py zero grok hits, mirror test file 15 passed (the restart clause corrected to the real detached respawn).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R14 #1 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. The body claimed `restart` refuses with NotImplementedError until `<bin> --help` is read; the live byte grok_bot_adapter.py:105-161 is a real detached respawn via subprocess.Popen(start_new_session=True), and the committed test (test_grok_bot_adapter.py:40-45) expects TypeError from the keyword-only contract. Corrected in place; the bare DEFAULT_BIN / config_max and adapters.load claims are unchanged. Agent Notes also updated from "helper test file 8 passed" to 15. No verdict/lean/confidence field touched.
<!-- THOUGHT:END -->
