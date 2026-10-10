---
id: goal:g7.16.1.11.36
mint_id: fbfc1d2a8921405880c9859d9cd39621
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.36
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: d7cad47ec722917f
season: 2
seeds:
  - goal:g7.16.1.11
status: complete
title: "G7.16.1.11.36: every post start pre-answers Claude Code's one-time \"fullscreen renderer\" dialog by setting fullscreenUpsellSeenCount to 3 in the post home's .claude.json, idempotently, so the dialog can no longer swallow the wake lines"
tags:
  - engine
  - claude-code
  - dialog
  - g7.16.1.11
town: core
---
# goal:g7.16.1.11.36

## Why this exists
goal:g7.16.1.11: Claude Code opens a one-time dialog on a fresh home, "Try the new fullscreen renderer? Yes, try it / Not now", that swallows every wake line typed into the pane until someone answers it. It stalled DG1 22:22-23:50Z 10-09 (7 unread, belam trap 98) and DG3 02:25-02:5xZ 10-10, and it will hit every post once. belam [decision] 03:0xZ 10-10 (relayed by SM 02:5xZ): "An engine fix would be to pre-answer it in each post's .claude.json at unit start (worth a leaf)". It is an engine byte, not a key, identity, signing, rotate, spawn-row or write-gate change, so the g7.16.1.11 HOLD does not apply (SM).

## Target end-state
- THE KEY, read from the bytes on the box, not guessed from a docstring (Claude Code 2.1.295, <the claude install>/versions/2.1.295 (resolve it with `readlink -f $(which claude)`), the bundled JS at byte offsets 223660146 and 236289509): the dialog (`title:"Try the new fullscreen renderer?"`, `confirmLabel:"Yes, try it"`, `cancelLabel:"Not now"`) is gated by a function that returns false, i.e. does NOT show it, when `(ce().fullscreenUpsellSeenCount??0) >= wEt`, with the constant `wEt = 3` (offset 214194516). Each impression writes `fullscreenUpsellSeenCount = min(count + 1, 3)` into the home's `~/.claude.json`, so the key lives in `<post home>/.claude.json`, and a count of 3 stops the dialog for good. The same gate also returns false when `settings.tui` is defined and when the renderer is already fullscreen; this leaf uses the count, which is a plain integer in a file the unit can reach. DG1's own home reads `fullscreenUpsellSeenCount: 3` (it answered the dialog three times).
- Every post's start pre-answers the dialog: in the post home's `.claude.json` the key `fullscreenUpsellSeenCount` is at least 3 BEFORE claude starts. Idempotent: a value that is already >= 3 is left alone and the file is not rewritten at all; an absent file is created holding only that key; an absent key or a lower value changes only that key, and every other key survives (a `jq -S` of the file with the key deleted is identical before and after).
- WHERE is the builder's call, with the constraints named: before the claude exec and on every start (the post unit's ExecStartPre has a byte ceiling and engine-sizes.t.sh pins heading sizes; agi-run's head, engine-wrap.md:23, runs just before the exec and sees `~`); the harness gate: a pi post has no Claude Code and needs nothing (agi-project gives it `H=node ... cccc.ts`), so the step runs for a claude `H` only or is harmless for pi; no host act is needed to reach a running post, because it takes effect at its next start.
- VERSION CAVEAT, stated: the key and the constant are read from 2.1.295 (minified chunk names move between versions). The leaf's PROBE for a different version: on a scratch HOME with no `.claude.json`, start `claude` under `script` with a 20 s timeout and look for the text "Try the new fullscreen renderer" in the captured pane; with `{"fullscreenUpsellSeenCount":3}` in place it must not appear. The lane does not run claude (no auth in a lane); the probe is the builder's one-time measurement and belam's check at an upgrade.

## Invariants
- No answer is invented for the owner: only the upsell count is set; no other `.claude.json` key (onboarding, trust dialogs, auth, projects, model cache) is written by this step.
- A home that already answered keeps its bytes (no rewrite when the value is already >= 3).
- The step never fails a post's start: an unreadable or unparsable `.claude.json` is left untouched and the start goes on (the dialog is then the cost, not a dead post).

## Falsifier
The command that decides is the first backticked one (agi-frontier): it exits 0 only when the work is done.
1. `test -n "$(git grep -n 'fullscreenUpsellSeenCount' -- .agi/nodes/.geometry extensions/agi/bin)"` (0 hits today). It is necessary, not sufficient: the lane below decides.
2. A lane on a scratch HOME (no claude, no network): (a) a fresh home with no `.claude.json` ends with it holding `fullscreenUpsellSeenCount` 3 after the step; (b) a second run leaves the file byte-identical (`cmp`); (c) a home whose file holds other keys and a count of 1 ends with count 3 and `jq -S 'del(.fullscreenUpsellSeenCount)'` equal before and after; (d) a home with count 3 or more is not rewritten (mtime and bytes unchanged); (e) an unparsable file is left byte-identical and the step exits 0. A mutant that writes no key, or writes 2, or rewrites a file that already holds 3, goes RED. The step is the piece extracted from the engine bytes (`sect`), never a copy in the lane.
3. Negative: `git grep -n 'hasCompletedOnboarding\|oauthAccount\|projects' -- <the new piece>` is empty (no other key is touched).

## Out of scope
Running claude to see the dialog (a lane has no auth) · the other first-start dialogs (trust, theme, onboarding) which are not stalling today · the `remote-control` menu that eats the next line (belam trap 96) · restarting running posts (a host act, belam's GO) · pi posts.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 05:2xZ: filed on SM's [decision] PLACEMENT 02:5xZ (from belam 03:0xZ). SM asked to READ THE CODE for the key before naming it; done on the bytes at <the claude install>/versions/2.1.295 (resolve it with `readlink -f $(which claude)`) (a 256 MB bun-compiled binary; `grep -a -b -o` for the offsets, `dd` for the context): the dialog component is `$Z` titled "Try the new fullscreen renderer?" (offset 236289509); its gate returns false when `(ce().fullscreenUpsellSeenCount??0)>=wEt` and also when `ft().tui!==void 0` or the renderer is already fullscreen; `wEt=3` (offset 214194516); `zMr` writes `min(count+1, wEt)` on each impression (offset 223660146). So the pre-answer is the integer 3 on one key in <home>/.claude.json, which also explains why my own home reads 3 now. NOT measured: that a fresh home with the key at 3 really skips the dialog in a live claude (no lane can run claude, and I did not start one against a scratch home); the leaf names the probe, and the version is pinned in the text. Chosen the count over `settings.tui` because the latter's accepted values are not nameable from what I read and a wrong value could change the renderer instead of silencing the dialog. HORIZON; placement per SM: DG4 builds it after its queue, bytes not under the HOLD. No prior version.
director-general-1 10-10 08:3xZ (SM placement 08:11Z, belam's trajectory check): COMPLETE. Built 8989451e52, landed d9cc770069 (an ancestor of the trunk). Re-run by me on the trunk in a scratch clone: claude-upsell.t.sh 0 FAIL (bare env -i, single file); Falsifier 1 (`git grep -n fullscreenUpsellSeenCount -- .agi/nodes/.geometry extensions/agi/bin`) prints 2 hits in engine-wrap.md (agi-run's head, line 27, claude H only), exit 0. The step is in the pieces, so it reaches a post at its next start with no host act; my own home's .claude.json reads the key at 3. NOT measured by me: the live-dialog case on a different Claude Code version, which is belam's probe at the next upgrade (the leaf names the probe).
<!-- THOUGHT:END -->
