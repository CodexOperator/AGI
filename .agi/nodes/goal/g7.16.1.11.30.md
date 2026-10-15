---
id: goal:g7.16.1.11.30
mint_id: babca6300c754caf878108a6f28938a0
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.30
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 846b25a998fb1cc9
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - guard
  - anonymize
  - secrets
  - g7.16.1.11
title: "G7.16.1.11.30: the anonymize guard runs its secret class without .env -- target a published SHA-256 denylist; interim a uid that cannot read .env skips the class LOUDLY"
town: core
---
# goal:g7.16.1.11.30

## Why this exists
goal:g7.16.1.11: belam's design for the anonymize guard (belam [decision] 09:5xZ, SM placement 09:5xZ): every uid should run the FULL guard with no .env read. Today the secret class reads the values of the keys the node schemas name from MAIN's .env: anonymize.py `_secret_tokens` ends with `env = envfile.read_env(envfile.resolve(root).env_file)` (anonymize.py:139), and .env is 640 belam + u:agi-belam:r, so for every other uid `read_env` raises PermissionError and `box_tokens` crashes (SM's gate, reds.py:70 `_secrets` calls `anonymize.box_tokens(root)`). SM's static gates have been stubbing the secret class for that reason.

## Target end-state
- TARGET (belam): the secret denylist is published as SHA-256 hashes of each secret value, never the value. The guard hashes every candidate token in a diff (`[A-Za-z0-9_-]{20,}` and the key shapes) and matches against the published hashes, so every uid runs the whole guard with no .env read and nothing in the repo reveals a value.
- INTERIM, until the hash list exists: a uid that cannot read .env skips the secret class LOUDLY (one stderr line naming the class and the reason, and a non-zero `secret_class_skipped` field in the check's result), never silently and never with a crash. `.env` stays 640 belam + u:agi-belam:r.
- THE CARRIER (SM 21:4xZ C2; the field has no carrier today: `anonymize.py cmd_check` (:299-315) only prints and returns 0 / 1 / 2, and `reds.py _secrets` (:67-75) returns `path:line` strings): (a) `anonymize.py check` prints, as its LAST stdout line on every ok / refused run, the fixed token `secret_class_skipped=0` or `secret_class_skipped=1` (a machine-read line, never a value), and on a skip also ONE stderr line `anonymize: secret class SKIPPED (<reason>)`; its rc keeps 0 / 1 / 2, so a skip never turns a clean diff into a refusal and never reads as "ran clean" (the stdout line says which). (b) a new function `anonymize.secret_class_state(root)` returns `(tokens, skipped_reason)` (`skipped_reason` is "" when the class ran) and `box_tokens` is rewritten on it, so there is ONE place that catches the unreadable `.env`. (c) `reds.py` keeps `_secrets` returning its strings and gains `secret_class_skipped(root) -> 0|1`, read by the report so SM's gate prints the skip in its own result instead of a stub. A caller reads the state by the stdout token (shell) or the function (python); nothing else carries it. SKIPPED means the class could not derive its tokens, and that has THREE causes, all `secret_class_skipped=1`: `.env` unreadable (PermissionError), `.env` ABSENT (envfile.py:268-269 returns `{}` for a missing file, which would otherwise read `secret_class_skipped=0`, the 'ran clean' reading the invariant forbids; SM C3), and any other read failure. The token is printed on rc 0 and rc 1 only: the rc 2 refusal (anonymize.py:305-307, 'no denylist source found') prints on stderr alone and no token (SM C4). A THIRD reader of the state: verification.py `check_anonymize` (:1488-1503) turns today's PermissionError into a named SKIP through `_perm_skip` (it only looks when rc != 0); once a skip is rc 0 it would read PASS, breaking 'a skip is never a pass', so it reads the stdout token and returns SKIP (naming the reason) on `secret_class_skipped=1` (0 hits for `secret_class_skipped` in verification.py today; SM C5).

## Invariants
- A value never appears in the repo, in a published list, in a log or in the stderr line: only hashes, or the fact of the skip.
- A skip is never a pass: a caller reading the result can tell "secret class ran, clean" from "secret class skipped".
- The hash list is derived by the one uid that can read .env; no other uid derives it.

## Falsifier
The deciding command is the first backticked one (agi-frontier): it exits 0 only when the work is done.
1. `test -n "$(git grep -n -E 'secret_class_skipped=|def secret_class_state|def secret_class_skipped' -- extensions/agi/bin/anonymize.py extensions/agi/bin/reds.py)"` (0 hits today; it covers the INTERIM, which is the first deliverable. It is necessary, not sufficient: item 2 is the lane.)
2. A lane runs `anonymize.py check` against an unreadable .env (a mode-000 file is readable as uid 0, so the lane either asserts `id -u` is not 0 or monkeypatches `envfile.read_env` to raise PermissionError, never relies on the mode alone, SM C4), an ABSENT .env and a readable one, with a verification.py row for each of the three states (SKIP, SKIP, PASS) on a diff holding a secret-shaped token: it exits without a traceback, prints the skip line, and the result carries `secret_class_skipped` non-zero; on a readable .env the field is 0 and the class runs.
3. A lane over `verification.check_anonymize` that a skip (rc 0, token 1) is a SKIP and not a PASS; a mutant that ignores the token goes RED.
4. TARGET: a lane with the published hash list and NO .env readable refuses a diff carrying a listed secret's value and passes a diff without it.

## Out of scope
Rotating or revoking any secret · the email allow cell (goal:g7.16.1.11.29) · who may read .env (belam's) · what `dispatch._looks_like_secret` flags (reds.py:73-74).

## RULE SM placement 09:5xZ 10-09, from belam [decision] 09:5xZ (SM's relay text; cites SM's, anonymize.py:139 and reds.py:70 re-read above)
"(B) GUARD WITHOUT .env (belam's design): TARGET = the secret denylist published as SHA-256 hashes of each secret value, never the value; the guard hashes every candidate token in a diff ([A-Za-z0-9_-]{20,} and the key shapes) and matches, so EVERY uid runs the full guard with no .env read. INTERIM = a uid that cannot read .env skips the secret class LOUDLY (a stderr line + a non-zero secret_class_skipped field), never silently; today anonymize.py:139 (_secret_tokens -> envfile.read_env) raises PermissionError for every uid but belam, so box_tokens crashes (my gate, reds.py:70). .env stays 640 belam + u:agi-belam:r."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 02:5xZ: RE-CUT 2 on SM's 01:3xZ return (C3-C5). Reproduced by me at 99a4746533: C3 envfile.py:268-269 returns {} for an absent file, so the class derives no token and the first cut would print secret_class_skipped=0, the 'ran clean' reading the invariant forbids: an absent .env is a SKIP; C4 the rc 2 refusal prints on stderr only, so the token is limited to rc 0/1, and a mode-000 file does not stop uid 0, so the lane guards the uid or monkeypatches read_env; C5 verification.py check_anonymize maps a PermissionError to a named SKIP via _perm_skip only when rc != 0, so with a skip at rc 0 it would read PASS: named as a reader with its own lane and mutant. Carrier unchanged from re-cut 1 (10-09 23:5xZ): a fixed last stdout line, one function secret_class_state, reds.secret_class_skipped, rc untouched (a new rc would make every non-belam caller refuse clean diffs).
<!-- THOUGHT:END -->
