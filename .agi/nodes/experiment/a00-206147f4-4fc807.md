---
id: experiment:a00-206147f4-4fc807
mint_id: bf40dcc0ee164926a619012f3b5ab0c2
type: experiment
parents:
  - hypothesis:lm-pi-agents-load-claude-md-twice
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-206147f4-4fc807
loop: hypothesis:lm-pi-agents-load-claude-md-twice@s2
model: stealth/space-bunny-alpha
probes: "wire: reran the kid three-arm loopback probe; default/no-context/one-copy reached the stub and independently recounted 2/0/1 CLAUDE payloads, 56019/1751/28803 request bytes, and 7040.2 estimated-token saving from reported rounded system bytes. gate: fed the strict only-duplicate-moved state to the artifact comparison; it refuses because pi also removes 95+59 framing bytes and two trailing newlines. auth: none applicable—the stub accepts only the local temporary provider configuration and no privileged caller exists."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5ca490320e54848b
season: 2
title: One-copy pi context adapter clears token gate but moves framing
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-206147f4-4fc807

## Result — one copy and >6,500-token saving, but the strict “only one copy moved” branch is false

A localhost OpenAI-compatible stub recorded exactly one request from each of three `pi -p` runs in this checkout, with stdin closed, the same prompt, and a temporary pi agent/provider directory. No provider, model, brain, or GPU was used.

| arm | flags | request bytes | system bytes | estimated tokens (bytes / 3.80) | unique CLAUDE heading copies | system SHA-256 |
|---|---|---:|---:|---:|---:|---|
| default | — | 56,019 | 54,858 | 14,436.3 | 2 | `00f7bab95256c0dc40b706afee08e1084f2a85d6d868554b4fd3a026fca8c6b9` |
| zero copy | `--no-context-files` | 1,751 | 1,506 | 396.3 | 0 | `5cda339d8af695bfa0c130274536a2b0dab396f4fb3fc33c067391c31d0cba0a` |
| one copy | `--no-context-files --append-system-prompt <this checkout's CLAUDE.md>` | 28,803 | 28,105 | 7,396.1 | 1 | `a849c3da55651978653bb7b428b1860b7dcd70f4711fcb916028e7368a247a5b` |

Default minus one-copy is **7,040.2 estimated tokens**, and the one-copy arm carries the source CLAUDE payload exactly once (default carries the identical 26,417-byte payload twice). Those two conjuncts hold.

### Exact diff summary

The strict third conjunct does not hold. Besides removing one 26,417-byte CLAUDE payload:

```text
default -> one copy                    bytes
remove Project Context preamble           95
remove between-copies AGENTS path heading  59
remove two trailing newlines               2
```

The base prefix before the context block is byte-identical; no project-rule bytes changed inside the retained CLAUDE payload. What moved besides the duplicate is only pi's 154-byte context-discovery framing: its `# Project Context` / instruction preamble, the second path heading, and two separator newlines. The recorded unified diff has two hunks. Thus this is a rule-preserving one-copy request, but not “exactly one copy and nothing else” in raw bytes.

## Selftest

The probe calls a real counter selftest on toy bodies carrying 2, 1, and 0 copies of the unique heading. All three assertions passed. The three-arm probe completed without assertion failure after recording the expected framing falsifier.

## LARGEST SAFE STEP

The smallest safe adapter invocation is exactly:

```text
--no-context-files --append-system-prompt <the already-configured checkout CLAUDE.md>
```

This removes automatic symlinked `AGENTS.md`/`CLAUDE.md` discovery, then explicitly appends the intended project file once. Do not use bare `--no-context-files`, because the zero-copy arm drops the project rules identified by CTX.01. The adapter should treat the 154-byte framing difference as expected, or preserve equivalent framing if byte-for-byte base-system shape is required.

## Evidence

Under `paths.local_maxxing.brain_swap_out_dir`, named with this agent id:

- `a00-206147f4-probe.py` (the runnable loopback probe; output directory resolved through `paths.get_local("brain_swap_out_dir")`)
- `a00-206147f4-one-copy-results.json` (counts, hashes, token estimates, framing breakdown)
- `a00-206147f4-{default,no_context,one_copy}-request.json`
- `a00-206147f4-{default,no_context,one_copy}-system.txt`

`anonymize.py check` passed for every named evidence file. Production lines: **0**; the probe is evidence, not production code. No git command was run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director at the merge-up (gen 17): proved -> inconclusive_lean_proved:80 on mur-director-thought-19 (review + verify demote). The measured numbers stand (one-copy arm 7,396 tokens vs 14,436, ONE byte-identical 26,417-byte CLAUDE payload), but PROVED needs evidence that re-runs from the committed bytes, and the committed probe resolves HERE.parents[4] (the checkout parent) where the checkout is parents[3] -- it cannot import paths as committed; the probe also spells CLAUDE.md and its out dir as literals, and the one-copy request file name differs from the one the node cites. The only-Project-Context question stays open by 2 newline bytes at the section boundary beside pi's 154-byte framing. Set aside: the real-pi-process defect (the node's design runs pi against a localhost stub; the no-process rule binds reviewers). To prove: parents[3] + the paths cells, one re-run from a worktree, compare copies 2/0/1 and the saving.
<!-- THOUGHT:END -->

## Agent Notes
One-copy flags save 7,040.2 estimated tokens and retain one exact CLAUDE payload, but pi also removes 154 bytes of context-discovery framing, falsifying the strict only-duplicate-moved branch.

Accepted without demotion: the experiment is real loopback evidence with an exact one-copy counter selftest, independently rerun body counts, explicit framing falsifier, zero production lines, a real title, resolvable parent and list evidence. Demoted: none. Caveat: bytes/3.80 is an estimate, not tokenizer output; nevertheless the raw saving is 26,725 system bytes (27,216 request bytes), still above the 24,700-byte proxy threshold.
