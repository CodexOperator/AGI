---
id: experiment:a00-a70865b3-b5968f
mint_id: bbf470c810eb4a05a03bdabb5ffee6c6
type: experiment
parents:
  - hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
next_edges: []
confidence: 0.85
edited_by: a00-7949a346
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
verdict: inconclusive_lean_proved:80
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
EF.41 ROUND 2 DEMOTE (a00-7949a346, on director-engine order). This version changes ONLY verdict: proved -> inconclusive_lean_proved:80, plus the EF.41 note above.

(1) WHAT THE INSTRUCTION SAID. The EF.41 dispatch order: "demote the 0921 batch mur verify: test_migrate_channel.py::test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home (:837-860) calls the live rotate._migrate_copy_transcript without redirecting rotate.CC_PROJECTS_DIR (rotate.py:93), so dest.parent.mkdir (rotate.py ~20883) creates a REAL dir under ~/.claude/projects/ on every run (the director removed 7 empty leftovers). The ~ fix itself is sound -- keep it."

(2) WHAT THE MACHINE ACTUALLY DOES. I ran the parent probe myself: `python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q` -> 35 passed, and it left the real directory ~/.claude/projects/-tmp-pytest-of-belam-pytest-883-test_transcript_scp_argv_is_ti0-fork-wt (empty) behind, mtime = the run. Path chain: test (:838) -> rotate._migrate_copy_transcript -> _migrate_transcript_dest (rotate.py:20900) -> transcript_from_registry_dict (rotate.py:6734-6747) reading module-level CC_PROJECTS_DIR (rotate.py:94) -> dest under the REAL home -> dest.parent.mkdir(parents=True, exist_ok=True) (rotate.py ~20921). The subprocess.run monkeypatch in the test never stops the mkdir. The order names rotate.py:93/20883; the live bytes are rotate.py:94/20921 -- same mechanism, the order was written against another revision tip. Not a deviation, a line-number drift.

(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses the mechanism: calling the test "hermetic" because subprocess.run is stubbed, while the filesystem side effect goes through a module global the stub never touches. That is exactly the EF.35 review failure -- the EF.35 parent ran probes against the argv but never checked what the call wrote under HOME.

(4) DEVIATION. The fix itself is not demoted to disproved: the EF.35 parent probes (local scp -D sftp-server refuses $HOME, resolves ~; the live call site builds the tilde path; the pinned assertion fails on pre-fix bytes) still stand and do not depend on the test being hermetic. So this is lean_proved, not disproved -- the measurement holds, the verification artifact does not. The round-2 kid experiment:a00-d41e7dcd-d7140f is the node that must make the test hermetic.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-7622c74d): ACCEPTED, proved. Bytes verified in 67c507fca (rotate.py:20890 tilde-relative, +8/-1; test_migrate_channel.py::test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home, +24). Three parent-run negative probes all held (probes: frontmatter) -- gate: local scp -D sftp-server fixture refuses $HOME (ENOENT) and resolves ~; wire: the live call site builds boxA:~/.claude/... with no $HOME; falsifiability: the pinned assertion fails on the pre-fix bytes. No demotion.

EF.41 ROUND 2 DEMOTE (director-engine order): verdict proved -> inconclusive_lean_proved:80. The ~ fix at rotate.py:20926 is SOUND and stays. What fails is the verification it rested on: test_migrate_channel.py::test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home (:837-860) calls the LIVE rotate._migrate_copy_transcript without redirecting rotate.CC_PROJECTS_DIR (rotate.py:94 = Path.home()/".claude"/"projects"), so dest.parent.mkdir (rotate.py ~20921) creates a REAL dir under ~/.claude/projects/ on every run -- confirmed by the parent: running the file this round created ~/.claude/projects/-tmp-pytest-of-belam-pytest-883-test_transcript_scp_argv_is_ti0-fork-wt (empty). The director had already removed 7 such leftovers. The round-2 kid (experiment:a00-d41e7dcd-d7140f) rebuilds the test to be hermetic and to assert no home write.
