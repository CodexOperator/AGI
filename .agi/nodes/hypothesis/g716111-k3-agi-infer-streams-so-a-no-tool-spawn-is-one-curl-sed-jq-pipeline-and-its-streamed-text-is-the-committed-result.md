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
testable_claim: "(K3) the agi-infer piece in .agi/nodes/.geometry/engine-wrap.md gains streaming (request 'stream':true + a line parser, sh + curl + sed + grep + jq, no root, no new provider) so that `sh extensions/agi/tests/k3-infer.t.sh` exits 0 (today's 829 B piece: 11 FAIL): on a canned SSE fixture that carries ': OPENROUTER PROCESSING' comment lines, an empty delta, a \n and a multi-byte char inside content and '[DONE]', the streamed text == the concatenated deltas byte for byte (Z4.l), the first chunk is in the log while the request is still open (a held-back second chunk), the spawn starts no process but curl, sed, grep, jq (strace -f -e execve, Z4.j), the key value is on no stdout, stderr or argv, a stream cut before [DONE] and an HTTP 500 both exit nonzero, the schema fence still rides, and the piece is <= 1,000 B."
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
(K3) the agi-infer piece in .agi/nodes/.geometry/engine-wrap.md gains streaming (request "stream":true + a line parser, sh + curl + sed + grep + jq, no root, no new provider) so that `sh extensions/agi/tests/k3-infer.t.sh` exits 0 (today's 829 B piece: 11 FAIL): on a canned SSE fixture that carries ': OPENROUTER PROCESSING' comment lines, an empty delta, a \n and a multi-byte char inside content and '[DONE]', the streamed text == the concatenated deltas byte for byte (Z4.l), the first chunk is in the log while the request is still open (a held-back second chunk), the spawn starts no process but curl, sed, grep, jq (strace -f -e execve, Z4.j), the key value is on no stdout, stderr or argv, a stream cut before [DONE] and an HTTP 500 both exit nonzero, the schema fence still rides, and the piece is <= 1,000 B.

## Dispatch line
config-max: none / template-max: none / code: one piece (the agi-infer block in engine-wrap.md) + its byte count in the block heading and engine.md line 46.

## FALSIFIERS
Z4.l the streamed text == the committed result byte for byte (cases z4l-*) · Z4.j no process but curl, sed, grep, jq (z4j-set, z4j-argv) · streaming, not buffering (stream-live: first chunk in the log within 2 s while the request is open) · failure is loud (fail-http, fail-trunc) · negative: a piece that adds any other process, buffers, prints the key, or drops the schema fence goes RED.

## TESTS
`sh extensions/agi/tests/k3-infer.t.sh` (default reads the piece from the working tree; `PIECE=<file>` tests a copy) · one ok|FAIL line per case, exit = FAIL count (AA3.13 shape) · 4 s.

## FILE SCOPE
.agi/nodes/.geometry/engine-wrap.md (the agi-infer block + its heading size) · .agi/nodes/.geometry/engine.md (the 829 B size line) · nothing else. The test file is NOT in scope (DG2's; a builder never edits it).

## CEILING
1 parent · kids <= 1 · Sonnet 5.5 · the piece <= 1,000 B.

<!-- THOUGHT:BEGIN -->
DEVIATION (10-03, DG2): the round is dispatched as a Sonnet 5.5 Claude Code subagent in worktree .agi/worktrees/de-k3-dg2-1 (branch de-k3-dg2-1, cut from 7900b8b91), NOT by dispatch.py: dispatch.py reads MAIN .env at start (PermissionError for a v5 uid, by design, K1's rail) and no per-post key / kid model cell exists yet (Z4 TRUE STATE). The subagent runs in this post's uid and spends no provider key; the builder is told not to read any key or .ssh. Test-first order kept: the falsifier (7900b8b91) was committed before any build byte.
<!-- THOUGHT:END -->
