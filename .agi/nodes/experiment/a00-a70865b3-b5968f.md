---
id: experiment:a00-a70865b3-b5968f
mint_id: bbf470c810eb4a05a03bdabb5ffee6c6
type: experiment
parents:
  - hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
next_edges: []
confidence: 0.85
edited_by: a00-7622c74d
evidence_runs:
  - experiment:a00-a70865b3-b5968f
line_ceiling: 40
loop: hypothesis:migrate-transcript-copy-survives-sftp-mode-scp@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probe_C1_gate.py -- scp -D /usr/lib/openssh/sftp-server, fixture cwd holds .claude/projects/<slug>/<sess>.jsonl", "expected": "~ -> rc=0 and dest written; $HOME -> rc!=0", "observed": "~ -> rc=0, dest present; $HOME -> rc=1, scp: $HOME/.claude/... No such file or directory, dest absent", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 probe_C2C3_wire.py -- live rotate._migrate_copy_transcript with subprocess.run monkeypatched", "expected": "argv[2] == boxA:~/.claude/projects/<slug>/sess-1.jsonl and no $HOME anywhere in argv", "observed": "argv[2] == boxA:~/.claude/projects/-tmp-ef35-parent-forkwt/sess-1.jsonl, $HOME absent", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 probe_C2C3_wire.py -- replay the pinned assertion against the pre-fix remote spelling", "expected": "the committed test assertion fails on the pre-fix bytes (test is falsifiable, not vacuous)", "observed": "boxA:$HOME/.claude/... -> assert \"$HOME\" not in join(argv) is False, so the pinned test would have caught the regression", "result": "held"}
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 14aaea1f8e2af960
season: 2
title: Migrate transcript scp argv passes a literal $HOME the SFTP server never expands; fixed to ~ and pinned
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a70865b3-b5968f

## Experiment

FR-B3 (goal:g15.27.3), migrate transcript copy in `extensions/agi/bin/rotate.py`
`_migrate_copy_transcript` (L20878). MEASURED FIRST, then built.

### 1. Measurement — `$HOME` arrives literal

- Box: `OpenSSH_9.6p1 Ubuntu-3ubuntu13.19, OpenSSL 3.0.13` (`ssh -V`).
- `man scp` (L14) "scp uses the SFTP protocol"; (L220-221) "Since OpenSSH 9.0,
  scp has used the SFTP protocol for transfers by default"; (L81-85) `-O`
  selects the legacy SCP protocol, needed "for expanding paths with a '~'
  prefix for older SFTP servers" — i.e. modern SFTP servers DO expand `~`.
- The pre-fix argv, reconstructed by monkeypatching `rotate.subprocess.run`
  (`sessions/iter-EF.35/a00-a70865b3/probe_argv.py`):

      ['scp', '-q', 'boxA:$HOME/.claude/projects/-tmp-wt-post-p/abc-123.jsonl',
       '<dest>']

  `$HOME` is literal in argv[2] — a Python list, no shell, and scp's default
  SFTP mode runs no remote shell either.

### 2. sshd-free fixture (no ssh, no network, no other box)

`scp -D /usr/lib/openssh/sftp-server` connects directly to a local SFTP
server program (`man scp` L56-59). Fixture cwd holds
`.claude/projects/ef35-slug/ef35-sess.jsonl`:

    scp -D $S 'boxA:~/.claude/projects/ef35-slug/ef35-sess.jsonl' out  -> rc=0, copied
    scp -D $S 'boxA:$HOME/.claude/projects/ef35-slug/ef35-sess.jsonl' out -> ENOENT, rc=1

A raw SFTP probe (`sftp_probe3.py`) against the same server shows:

- `SSH_FXP_REALPATH` does NOT expand `~` (it resolves `~` as a literal dir).
- `SSH_FXP_EXTENDED(expand-path@openssh.com)` DOES: `~/.bashrc` ->
  `<server cwd>/.bashrc`; `$HOME/.bashrc` -> STATUS `No such file` (the
  `$HOME` spelling is a literal directory name).
- The server advertises the extension in its INIT reply:
  `expand-path@openssh.com v 1` (also shown by `sftp-server -Q requests`,
  and present in the `scp` binary as
  `Sending SSH2_FXP_EXTENDED(expand-path@openssh.com) "%s"`).
- `~` expanded to the fixture cwd here because sftp-server was launched
  directly; under sshd it is the authenticated user's home. The mechanism
  (server-side `~` expansion, none for `$HOME`) is what is measured.

### 3. Fix (built, not merely proposed)

`rotate.py` L20884, one line — argv only, same alias prefix, same dest, same
`-q`, same chmod 0600, same `check=False`:

    -    remote = f"$HOME/.claude/projects/{dest.parent.name}/{dest.name}"
    +    remote = f"~/.claude/projects/{dest.parent.name}/{dest.name}"

plus a 6-line comment recording the measurement and why `~` is mode-safe
(`~` resolves under both SFTP mode via expand-path and legacy SCP mode via the
remote shell; `$HOME` resolves under neither without a shell).

### 4. Pinned test

`extensions/agi/tests/test_migrate_channel.py::test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home`
monkeypatches `rotate.subprocess.run`, calls `rotate._migrate_copy_transcript`,
and asserts argv[2] == `boxA:~/.claude/projects/<slug>/sess-1.jsonl`, ends in
`/sess-1.jsonl`, and that `$HOME` appears nowhere in the argv. No network.

### Verdict

`proved`: the pre-fix literal `$HOME` was measured on this box's OpenSSH, the
SFTP server was measured expanding `~` and refusing `$HOME` under a local
sshd-free fixture, the fix is built, and its argv is pinned by a committed test.

<!-- BODY:END -->

## Agent Notes
Measured on OpenSSH_9.6p1: argv[2] carried a literal $HOME (no shell in SFTP mode); sshd-free scp -D + raw SSH_FXP_EXTENDED(expand-path@openssh.com) fixture shows ~ resolves and $HOME is ENOENT. Fixed rotate.py L20884 to ~-relative and pinned the argv in test_migrate_channel.py. 8 production lines, 35+131 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7622c74d, EF.35). Verdict accepted: proved. Three parent-run
negative probes recorded in `probes:` above; all three held.

(1) WHAT THE INSTRUCTION SAID. The tier-parent brief: "A kid's tests are its
CLAIM, not your evidence ... Read the bytes that moved, not the summary ...
One negative probe per claim conjunct, run by YOU, recorded as `probes:` in the
kid's node". The kid's claim came as three conjuncts (the target hypothesis
carries no numbered enumeration, so I enumerated them): C1 the `$HOME` path is
MEASURED under this box's SFTP-mode scp against an sshd-free fixture; C2 the
fix uses a path scp resolves and C3 a committed test pins the argv.

(2) WHAT THE MACHINE ACTUALLY DOES.
  - Bytes: `git show --stat 67c507fca` carries exactly three files -- the node,
    `extensions/agi/bin/rotate.py` (+8/-1), `extensions/agi/tests/test_migrate_channel.py`
    (+24). `rotate.py:20890` now reads `remote = f"~/.claude/projects/{...}"`.
    Every deliverable the kid named is in that commit; none is missing.
  - C1 (gate probe, run by me): `scp -D /usr/lib/openssh/sftp-server` against a
    fixture cwd -- no ssh, no network, no other box. `boxA:~/.claude/...` -> rc=0,
    dest written; `boxA:$HOME/.claude/...` -> rc=1, `scp: $HOME/.claude/...: No
    such file or directory`, dest absent. The defect is real on OpenSSH_9.6p1 and
    `~` is the spelling the SFTP server resolves.
  - C2 (wire probe, run by me): calling the LIVE `rotate._migrate_copy_transcript`
    with `subprocess.run` monkeypatched yields argv[2] ==
    `boxA:~/.claude/projects/-tmp-ef35-parent-forkwt/sess-1.jsonl`, `$HOME` absent.
    The call site reaches the changed bytes; no stub sees it.
  - C3 (falsifiability probe, run by me): replaying the kid's own assertion against
    the PRE-FIX spelling, `"$HOME" not in " ".join(argv)` is False -- the committed
    test fails on the old bytes, so it is falsifiable rather than vacuous. `git show
    67c507fca -- tests` confirms the test drives the real function, not a
    re-implemented f-string.

(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses
the mechanism: a test that rebuilds the remote string itself and asserts on its own
reconstruction, or a test that only asserts `"~" in argv[2]`. Both pass while the
real call site still hands scp `$HOME`; the first would not notice the function
changed at all. This kid's test calls `_migrate_copy_transcript` and asserts the
full argv equality plus the `$HOME`-absent clause, and my C3 probe confirms a
regression of exactly the kind SL7.136 describes would fail it.

(4) DEVIATION. None from a standing rule. I did not re-run the kid's suite as
evidence (its 35+131 pytest figures are the kid's claim); the three probes above
are the parent-run evidence. The kid's node title is its own words, not the
derived filename title.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-7622c74d): ACCEPTED, proved. Bytes verified in 67c507fca (rotate.py:20890 tilde-relative, +8/-1; test_migrate_channel.py::test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home, +24). Three parent-run negative probes all held (probes: frontmatter) -- gate: local scp -D sftp-server fixture refuses $HOME (ENOENT) and resolves ~; wire: the live call site builds boxA:~/.claude/... with no $HOME; falsifiability: the pinned assertion fails on the pre-fix bytes. No demotion.
