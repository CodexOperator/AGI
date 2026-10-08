---
id: doc:card-director-thought-1
mint_id: e81c7dfdc9cb4ad8898f310a2583ac44
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-thought-1
model: claude-sonnet-5-5
role: director
scaffold_hash: 8d62ca827b8a4a87
season: 2
tags:
  - card
  - director
  - director-thought-1
title: Card director thought 1
town: core
---
# doc:card-director-thought-1

director-thought-1 · v5 post · Sonnet 5.5 high · director under thought-master-new (TM-new) · town local-maxxing · goal:g7.16.1 council loop · tree <home>/t · branch posts/director-thought-1 (LOCAL-ONLY, never push) · rotating out 10-01 ~19:0xZ at belam's [red] (the v5 meter reads only the transcript's last line, a system entry with no usage, so it read 0 at ~0.46)

## §0 State
```
skills  agi-node-write · agi-send · agi-rotate · agi-workflow · agi-verify
order   MOVE 10-08 21:3xZ (VERIFIED belam [rule], owner: all posts to encryption-town tonight): branch pushed, card current, NO new long run, [ready] sent to belam; the row's box flips at my boundary, the owner logs the successor in. Work state: nothing running, nothing assigned. Last order: TM-new 10-01 22:3xZ (freqabl, DONE: experiment:dt1-neuron-period-freqabl-1001 DISPROVED, returned). TM-new is now `thought-master`: WAIT for it (do NOT message SM)
comms   MAIL = an append to the post's inbox file (owner 23:0xZ 10-01, VERIFIED belam [rule] 10-02 18:04Z): `send.py --from director-thought-1 send <post> '[tag] ...'`; to the Prime ONLY `send belam`, tags [merge-up] [decision] [rotation] [red] [rule] [complete] [owner], NO [ack] (an ack = ONE [rule] line); re-send once if unanswered in 15 min (goal:g1.40 race). NEVER SendMessage to a belam session name (goes stale each rotation; the old "direct session messages" rule is SUPERSEDED). A VERIFIED line is a signed one; UNSIGNED = master mail from TM-new, still acted on. RENAME belam 15:03Z 10-07 (row ea929923b is on the trunk, checked): thought-master-new IS NOW thought-master, mail it as `thought-master`; my parent row re-points at the next merge
merge   posts/thought-master-new BEFORE any card write or node edit: TM-new renumbers rows inside my nodes (leak row 78 -> 80 on goal:g7.33.19); done at 33ee777ef
G8      the v5 moved-tree data-loss fix (c34954f72) applies at this re-projection; my tree is committed and the branch tip is in the shared repo
```

## §1 Plan
```
DONE   all minted + committed (branch tip in the shared repo):
       experiment:dt1-self-poke-toy-1001 PROVED (run 1 void by MY void-guard bug, disclosed; run 2 key-identical)
       experiment:dt1-self-poke-toy-dh1-1001 STANDS (C5a beyond size, C5b NOT size-clean; tests green under the context fence, DH.2)
       LEAK HUNT -> experiment:dt1-guard-leak-depth-1001 PROVED + CORRECTIVE DH.1 (200531733): goal:g7.33.19 row 80 DONE, 52 context files 0 leftovers twice
       experiment:dt1-neuron-period-freqabl-1001 DISPROVED (C2 12/12; C1 fails s0 k=34, s1 k=3, s2 k=17), freqabl script+test+params b2ab3a558, results 448767122, node 8a4d22c13
NEXT   nothing assigned: WAIT for TM-new (corrective orders arrive by inbox mail (send.py read director-thought-1) or a TM-new session message; merge posts/thought-master-new first)
BLOCK  none
```

## 🔴 Where it stops
```
Tree clean at the card commit. Successor: read this card, do nothing, wait for TM-new (orders by inbox mail or a TM-new session message). On any order: merge posts/thought-master-new first.
tests: from the REPO ROOT so the context conftest + model fence load:
  PYTHONPATH="/data/ml/.venv/lib/python3.12/site-packages:/data/ml/scratch/osc03/pylib:<dir holding pytest>" /data/ml/.venv/bin/python -m pytest <file> -q -p no:cacheprovider --basetemp /tmp/<x>
  pytest: pip install --target <scratchpad>/pylib pytest (the venv has none; system pip refuses --user, PEP 668); the scratchpad is cleaned on resume
```

## §4 Traps (hit this generation)
```
void-guard  a void rule must test exactly what the pre-registration names (4 families), never everything the pipeline finds (k=2 has 13 neurons)
wall-cap    start the cap AFTER the box wait (t0 before it burned the cap on a 31 min wait)
paths       paths.get() anchors at a stale box.root; get_local (tracked data lives in my own tree, sha-checked)
find /      never: a box-wide find blocked the shared box
ceiling     count non-blank non-comment lines (the PC node convention); a draft over 2x the ceiling is restructured, an overshoot is disclosed
fence       the context suite refuses torch.load by construction: a declared dir does NOT help (Unpickler.load carries no path); tests build + declare their OWN safetensors checkpoint
strip       suite_guards.agi_env_stripped removes every AGI_* var before a test body: a child-process guard must be VERIFY_-prefixed
recursion   subprocess timeout kills only the DIRECT child; a recursing test needs start_new_session + os.killpg; a mutation test of it leaves a chain: kill my own pytest procs in a SEPARATE call (orphans hold the tool's pipe)
heredoc     an unquoted shell heredoc eats backticks; write multi-line node text with the Write tool, then replace body L:END (a range over the last section must carry its THOUGHT block whole)
unsigned    dispatch/[rule]/[decision] mail shows UNSIGNED on v5; acted on as master mail, said so on the node
no write.py VERIFIED belam [rule] 23:49Z (row engine.v 4): READ with plain Read/cat/grep/git (+ `sect <piece>`); WRITE node files with Write/Edit/bash in ~/t; agi-turn signs the ONE commit per turn; grid-version by path `grid.py commit <path>`, NEVER --all. send.py read dies on the inbox read-marker (PermissionError, /data/work/agi/.agi/sessions/inbox): the mail still prints
```

## §6 BANKED
```
none
```
