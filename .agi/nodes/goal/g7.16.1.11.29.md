---
id: goal:g7.16.1.11.29
mint_id: 5d760a84a38b4c259191a2a0b15f3cf1
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.29
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 4437571a477ec0d3
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - guard
  - anonymize
  - g7.16.1.11
title: "G7.16.1.11.29: the anonymize guard allows the public Co-Authored-By trailer address of the model vendor (config cell anonymize.email_allow, one pattern, no code)"
town: core
---
# goal:g7.16.1.11.29

## Why this exists
goal:g7.16.1.11: every landing message carries the public trailer (the vendor's no-reply address, written <email> in this leaf because the guard refuses the literal) `Co-Authored-By: Claude ... <email>`, and belam's full guard REFUSED SM's .13.2 message on it: a false positive (belam [decision] 09:5xZ, SM placement 09:5xZ). Reproduced by me: `python3 extensions/agi/bin/anonymize.py check --text 'Co-Authored-By: Claude Sonnet 5.5 <email>'` prints REFUSED (text carries email). The allow list is the config cell `anonymize.email_allow` in .agi/config.json (read by anonymize.py `_email_allow`, :77), four FULL-match regexes today: agi-* unit names, example.com/org/net, openssh.com, `N.service`.

## Target end-state
- ONE more pattern, the vendor's public no-reply address with its dot escaped, is added in `anonymize.email_allow`, a config cell and nothing else: no code change, no new class.
- The trailer passes the guard; any other `<anyone>@<real domain>` still refuses.

## Invariants
- The patterns are FULL-matched regexes, so the new one allows exactly that address and no sibling (another local part at the same domain still refuses).
- The guard's other classes (home paths, hardware, tokens from this box) are unchanged.

## Falsifier
1. `test -n "$(git grep -n 'noreply' -- .agi/config.json)"` (0 hits today).
2. `python3 extensions/agi/bin/anonymize.py check --text "$(printf 'Co-Authored-By: Claude Sonnet 5.5 <noreply@%s>' anthropic.com)"` exits 0, and the same call on `"$(printf 'x <someone@%s>' gmail.com)"` and on `"$(printf 'x <other@%s>' anthropic.com)"` still prints REFUSED (the addresses are built at run time so no literal address sits in this file). ORDER (SM C6, reproduced): this check crashes for every uid but belam today, because `box_tokens` reaches `_secret_tokens` -> `envfile.read_env` (anonymize.py:139) and the .env is 640 belam (PermissionError). So F2 runs under `AGI_ANONYMIZE_FIXTURE=<a fixture json>` (box_tokens returns before the .env read when it is set, anonymize.py:150), or the leaf is ordered BEHIND goal:g7.16.1.11.30, which makes the unreadable .env a named skip instead of a crash.

## Out of scope
The guard reading .env (goal:g7.16.1.11.30) · the E full-suite baseline (goal:g7.16.1.11.31) · any change to anonymize.py.

## RULE SM placement 09:5xZ 10-09, from belam [decision] 09:5xZ (SM's relay text; cites SM's, the refusal re-run above)
"(A) GUARD EMAIL ALLOW, a config cell only: .agi/config.json anonymize.email_allow (4 patterns today: agi-* units, example.com/org/net, openssh.com, N.service) gains '<email>' (the vendor no-reply address, dot escaped; written <email> here because the guard refuses the literal) -- the public Co-Authored-By trailer every landing carries (belam's full guard REFUSED my .13.2 message on it: a false positive). Falsifier: anonymize.py check --text on a line carrying that trailer exits 0, and on '<anyone>@<real domain>' still refuses."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 02:5xZ: carried, one delta on SM's 01:3xZ return (C6): F2 as first cut crashes with a PermissionError for every non-belam uid (reproduced by SM as its uid; anonymize.py:139), so it would never go green for the post that builds it; it now runs under AGI_ANONYMIZE_FIXTURE (anonymize.py:150 returns before the .env read) or lands behind .30. Content otherwise unchanged from the first cut (10-09).
<!-- THOUGHT:END -->
