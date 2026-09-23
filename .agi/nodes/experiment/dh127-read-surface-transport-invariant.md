---
id: experiment:dh127-read-surface-transport-invariant
mint_id: d0b2d4d73b654507bab302b886d5f450
type: experiment
parents:
  - hypothesis:a00-d5172cf4-b2958e
next_edges: []
edited_by: a00-d5172cf4
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -c 'inspect.signature' on read/peek/read_dm/peek_dm/read_dms/read_room/peek_room + read(root,'far-seat','sender') with a foreign-box row present", "expected": "no signature carries a transport/box/ssh parameter; the foreign-box call returns the same empty-inbox line as the local call, no refusal", "observed": "all seven signatures carry only root/croot, me/participant, other/room, since, sender, all_, commit, wrap. read(root,'local-seat','sender') -> 'inbox for local-seat: empty'; read(root,'far-seat','sender') -> 'inbox for far-seat: empty'", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "AST source-segment scan of the seven read-shaped FunctionDefs for tokens is_ssh/row_is_local/ssh + live send_dm/read_dm round trip", "expected": "zero transport tokens in every read body; read_dm returns the real transcript", "observed": "all seven: transport-token hits=[]; read_dm -> ['**a00-d5172cf4** 06:54 - hello-bytes'] from a real gw-local-seat--sender.md. row_is_local appears only in wake_all_local (send.py:2816) and mail_poll --box-local (send.py:5431), both explicitly local service readers", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "call each read-shaped function with is_ssh=True", "expected": "TypeError naming is_ssh; no silent absorption via **kwargs", "observed": "read/peek/read_dm/peek_dm/read_dms/read_room/peek_room each raise TypeError: got an unexpected keyword argument 'is_ssh'", "result": "held"}
  - {"conjunct": "round constraint", "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src", "expected": "empty; nodes only, 0 production lines", "observed": "empty", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 3a8d3475332ea17b
season: 2
testable_claim: "The caller-facing READ surface (read, peek, read_dm, peek_dm, read_dms, read_room, peek_room) is transport-invariant: no signature takes a transport/box/ssh parameter, no body branches on a transport predicate, a foreign-box peer's inbox is read by the same call as a local one, and is_ssh=... is refused by name -- while the only row_is_local uses in read-shaped callers are the explicitly-local service readers mail_poll and wake_all_local."
title: "DH.127 read-surface transport invariance: gate/wire/auth negative probes"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dh127-read-surface-transport-invariant

## Experiment

DH.127 negative probes on the **READ** third of the `goal:g7.31.4.2`
invariant, on committed bytes (`send.py` untouched, 0 production lines).
Probes ran from scratch
`.agi/sessions/iter-DH.127/a00-d5172cf4/probe_read_surface.py` against the
real `extensions/agi/bin/send.py`; no read function is stubbed.

### conjunct 1 — GATE (no transport parameter; foreign-box state changes nothing)

Signatures via `inspect.signature(send.<fn>)`:

```
read(root: 'Path', me: 'str', sender: 'str | None', wrap: 'int' = 160) -> 'None'
peek(root: 'Path', me: 'str', wrap: 'int' = 160) -> 'None'
read_dm(croot: 'Path', me: 'str', other: 'str', since: 'str | None', sender: 'str | None', all_: 'bool' = False, wrap: 'int' = 160) -> 'list[str]'
peek_dm(croot: 'Path', me: 'str', other: 'str', since: 'str | None', all_: 'bool' = False, wrap: 'int' = 160) -> 'list[str]'
read_dms(croot: 'Path', me: 'str', *, commit: 'bool' = True, wrap: 'int' = 160) -> 'int'
read_room(croot: 'Path', room: 'str', participant: 'str', since: 'str | None', sender: 'str | None', all_: 'bool' = False, wrap: 'int' = 160) -> 'list[str]'
peek_room(croot: 'Path', room: 'str', participant: 'str', since: 'str | None', all_: 'bool' = False, wrap: 'int' = 160) -> 'list[str]'
```

Zero transport/box/ssh parameters. With a foreign-box row `far-seat`
(`box: local-town`) and a local row `local-seat` in the SAME graph, the exact
foreign-box/empty state is handed to the reader and the reader does not
change — unlike `_nudge_target`, which refuses a foreign row by name:

```
read(root,'local-seat','sender') -> 'inbox for local-seat: empty'
read(root,'far-seat','sender')  -> 'inbox for far-seat: empty'
```

### conjunct 2 — WIRE (no transport predicate in the bodies; live bytes reached)

AST scan of the seven `FunctionDef` source segments for tokens
`is_ssh`, `row_is_local`, `ssh`:

```
read: transport-token hits=[]
peek: transport-token hits=[]
read_dm: transport-token hits=[]
peek_dm: transport-token hits=[]
read_dms: transport-token hits=[]
read_room: transport-token hits=[]
peek_room: transport-token hits=[]
```

Live call reaching the real bytes (`send_dm` writes, `read_dm` reads back):

```
dm path: /tmp/tmpji3fse4v/.agi/dm/local-seat--sender.md
read_dm -> ['**a00-d5172cf4** 06:54 — hello-bytes']
```

The only `row_is_local` uses in read-shaped callers are explicitly-local
service readers, named here so they are not mistaken for the shared surface:

```
send.py:2816  wake_all_local:  if not name or not boxes.row_is_local(root, r):
                            # "retry every LOCAL row"
send.py:5431  mail_poll (CLI --box-local):  if boxes.row_is_local(root, r):
                            # "consume every LOCAL row's inbox"
send.py:2178  _nudge_target: refuses a FOREIGN box row (sender-side)
send.py:4487  _whois_answer: display guard on a foreign row's @id
```

`grep -rn is_ssh extensions/agi/bin extensions/agi/src skills` prints nothing
(exit 1).

### conjunct 3 — AUTH (`is_ssh=...` refused by name)

Every read-shaped function raises `TypeError` naming the kwarg; none absorbs
it through `**kwargs`:

```
read: TypeError: read() got an unexpected keyword argument 'is_ssh'
peek: TypeError: peek() got an unexpected keyword argument 'is_ssh'
read_dm: TypeError: read_dm() got an unexpected keyword argument 'is_ssh'
peek_dm: TypeError: peek_dm() got an unexpected keyword argument 'is_ssh'
read_dms: TypeError: read_dms() got an unexpected keyword argument 'is_ssh'
read_room: TypeError: read_room() got an unexpected keyword argument 'is_ssh'
peek_room: TypeError: peek_room() got an unexpected keyword argument 'is_ssh'
```

## Evidence

Sibling committed module still green on the SEND/NUDGE half (re-measured, not
digit-swapped):

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 24.87s

$ grep -rn "is_ssh" extensions/agi/bin extensions/agi/src skills
(no output; exit 1)
```

Production lines: 0 (only `.agi/nodes/*.md`). Ceiling 40.

All three conjuncts HELD. No production byte changed; DH.127 adds no committed
test module (the brief scopes this round to `.agi/nodes` only), so the READ
third enters the graph as probes, not as a second test file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First probe of the READ third. Chose negative probes run from scratch rather than a committed test module because the brief scopes DH.127 to .agi/nodes only (0 production lines); a future round can promote probe_read_surface.py into extensions/agi/tests/ with the send-surface module. Deviation: no is_ssh token exists anywhere in production, so the auth probe asserts refusal-of-a-nonexistent-kwarg rather than a live caller branch -- that is the invariant holding, and it is stated as such.
<!-- THOUGHT:END -->
