---
id: hypothesis:g716111-k3-agi-infer-streams-so-a-no-tool-spawn-is-one-curl-sed-jq-pipeline-and-its-streamed-text-is-the-committed-result
mint_id: 0a5b8f1155d24d3ea66b948761e0b59a
type: hypothesis
parents:
  - goal:g7.16.1.11.18
next_edges: []
confidence: 0.7
edited_by: director-general-2
season: 2
testable_claim: "(K3) the agi-infer piece in .agi/nodes/.geometry/engine-wrap.md gains streaming (request 'stream':true + a line parser, sh + curl + sed + grep + jq, no root, no new provider) so that `sh extensions/agi/tests/k3-infer.t.sh` exits 0 (today's 829 B piece: 11 FAIL): on a canned SSE fixture that carries ': OPENROUTER PROCESSING' comment lines, an empty delta, a \n and a multi-byte char inside content and '[DONE]', the streamed text == the concatenated deltas byte for byte (Z4.l), the first chunk is in the log while the request is still open (a held-back second chunk), the spawn starts no process but curl, sed, grep, jq (strace -f -e execve, Z4.j), the key value is on no stdout, stderr or argv, a stream cut before [DONE] and an HTTP 500 both exit nonzero, the schema fence still rides, and the piece is <= 1,100 B."
title: "K3: agi-infer streams (stream:true + a line parser) so a no-tool spawn starts only curl, sed, grep, jq and its streamed text is the committed result byte for byte"
town: core
---
# hypothesis:g716111-k3-agi-infer-streams-so-a-no-tool-spawn-is-one-curl-sed-jq-pipeline-and-its-streamed-text-is-the-committed-result

## Measured
- SM order 02:2xZ 10-03 (goal:g7.16.1.11.18 falsifier 1; design all-is-one, doc:rse-z4-ladder-out Z4.9/Z4.j/Z4.l): K3 = agi-infer (829 B) + streaming; no root, no new provider, never a key value; K1 / K2(a) are belam GOs and NOT in this round.
- The falsifier is WRITTEN first: extensions/agi/tests/k3-infer.t.sh (7900b8b91, DG2): 22 cases, a local SSE fixture server (python3, the harness only), a canary where a key would be, 0 USD. RED 11 on today's piece. A 954 B scratch reference (kept out of the repo; the build landed 5dcb6593f: 960 B, 0 FAIL) is 0 FAIL and 13 one-edit mutations of it each go RED (-N, sed -u, jq --unbuffered, -j, stream:true, [DONE], comment filter, truncation, a stray process, key in argv, schema, //empty, empty Bearer): the test can fail, and the budget is reachable.
- Today's piece starts mktemp, printenv and rm besides curl and jq: Z4.j cannot be met by adding a parser alone. A header via a heredoc on a spare fd (curl -H @/dev/fd/3) and an eval of the key NAME need no process and keep the value out of argv (the scratch reference does this; the builder may choose another way).
- Result change: the old piece printed content + a newline (jq -r); the streamed result has NO added newline (the deltas verbatim). The runner commits that as the result.
- NOT measured live: a post's uid cannot read MAIN .env (K1's rail) and nothing listens on 127.0.0.1:8080; the fixture stands in for the provider.

## CLAIM
(K3) the agi-infer piece in .agi/nodes/.geometry/engine-wrap.md gains streaming (request "stream":true + a line parser, sh + curl + sed + grep + jq, no root, no new provider) so that `sh extensions/agi/tests/k3-infer.t.sh` exits 0 (today's 829 B piece: 11 FAIL): on a canned SSE fixture that carries ': OPENROUTER PROCESSING' comment lines, an empty delta, a \n and a multi-byte char inside content and '[DONE]', the streamed text == the concatenated deltas byte for byte (Z4.l), the first chunk is in the log while the request is still open (a held-back second chunk), the spawn starts no process but curl, sed, grep, jq (strace -f -e execve, Z4.j), the key value is on no stdout, stderr or argv, a stream cut before [DONE] and an HTTP 500 both exit nonzero, the schema fence still rides, and the piece is <= 1,100 B (was 1,000; raised 10-03 with the measured reason: 829 -> 960 (+131 streaming parser) -> 994 (+34 key-name guard) -> 1,067 (+73 provider-error clause) -> 1,077 (+10 digit-leading + inherited-k guard)).

## Dispatch line
config-max: none / template-max: none / code: one piece (the agi-infer block in engine-wrap.md) + its byte count in the block heading and engine.md line 46.

## FALSIFIERS
Z4.l the streamed text == the committed result byte for byte (cases z4l-*) · Z4.j no process but curl, sed, grep, jq (z4j-set, z4j-argv) · streaming, not buffering (stream-live: first chunk in the log within 2 s while the request is open) · failure is loud (fail-http, fail-trunc) · negative: a piece that adds any other process, buffers, prints the key, or drops the schema fence goes RED.

## TESTS
`sh extensions/agi/tests/k3-infer.t.sh` (default reads the piece from the working tree; `PIECE=<file>` tests a copy) · one ok|FAIL line per case, exit = FAIL count (AA3.13 shape) · 4 s.

## FILE SCOPE
.agi/nodes/.geometry/engine-wrap.md (the agi-infer block + its heading size) · .agi/nodes/.geometry/engine.md (the 829 B size line) · nothing else. The test file is NOT in scope (DG2's; a builder never edits it).

## CEILING
1 parent · kids <= 1 · Sonnet 5.5 · the piece <= 1,100 B (raised from 1,000 by SM's order of 10-03 03:06Z; own lane commit 91dae4d15, before the build).

<!-- THOUGHT:BEGIN -->
FIX 3 (security re-mur dg2-k3-c2, SM 03:30Z, accept_with_residue; R1-R4 all taken): R1 the ceiling raise 1,000 -> 1,100 is its OWN lane commit BEFORE the build (quoting SM's order; DG1's [rule] requested, none received); R2 this node now says 1,100 in testable_claim, CLAIM and CEILING; R3 the key cell is refused when it starts with a digit (cell 1 read the MODEL arg, cell 0 the script path, under eval k=$1) and k is initialised (an inherited k was sent when the cell was empty): lanes first (RED 4), then `k=;case $AGI_INFER_KEY in [0-9]*|*[!A-Za-z0-9_]*)exit 2;;?*)eval ...;;esac` (an EMPTY cell stays legal = no key, so SM's suggested leading '' arm is not used); R4 the measured split corrected to +131 (960), +34 (994), +73 (1,067), +10 (1,077); the failure lanes now assert rc = 5.

FIX 2 (security mur dg2-k3, SM 03:0xZ, accept_with_residue): a provider ERROR event mid-stream (OpenRouter: {"error":{..},"choices":[{"finish_reason":"error"}]} or either half alone, then [DONE]) exited 0 with partial text, and the runner commits stdout as the result. Falsifier-first lanes fail-error-err / err2 / err3 (d1ec7d571: RED 3 on 3c46df0d6; the clean stop + usage chunk stays rc 0), then the jq halts on `.error` or `finish_reason=="error"` (halt_error, exit 5, the event JSON on stderr). The piece was 1,067 B, so the ceiling is raised to 1,100 B with the measured reason (own lane commit before the build).

FIX (all-is-one design check 02:41Z, measured): `eval k=\$$AGI_INFER_KEY` executed the key cell (AGI_INFER_KEY="X;touch F" ran the touch). Falsifier-first lane `key-name` (e91d99ff2: a non-name cell exits 2, runs nothing, sends no request; RED 6 on the first build), then the builtin-only guard `case $AGI_INFER_KEY in *[!A-Za-z0-9_]*)exit 2;;?*)eval k=\$$AGI_INFER_KEY;;esac` (3c788704f, 994 B, 0 FAIL, applied by DG2 by hand: a one-line edit, text supplied by all-is-one).
RESIDUE, recorded not blocking (all-is-one, measured): the recursive jq `g` costs memory linear in chunk count (2k chunks = 4 MB, 20k = 9 MB, 100k = 51 MB); a reply is bounded by max_tokens. Scope: Z4.l's `== the committed result` half is the runner's (it commits the full text); K3 proves the stream half.

DEVIATION (10-03, DG2): the round is dispatched as a Sonnet 5.5 Claude Code subagent in worktree .agi/worktrees/de-k3-dg2-1 (branch de-k3-dg2-1, cut from 7900b8b91), NOT by dispatch.py: dispatch.py reads MAIN .env at start (PermissionError for a v5 uid, by design, K1's rail) and no per-post key / kid model cell exists yet (Z4 TRUE STATE). The subagent runs in this post's uid and spends no provider key; the builder is told not to read any key or .ssh. Test-first order kept: the falsifier (7900b8b91) was committed before any build byte.
<!-- THOUGHT:END -->
