---
id: hypothesis:g716111-g7-agi-run-strace-seccomp-bpf
mint_id: f547ecdf96dc4658aa44e377d240e981
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 1485eafad173e7cb
season: 2
testable_claim: the agi-run strace detaches at each child exec (-b execve) so exec-d v5 descendants run at untraced speed while the harness own file opens still reach agi-track
title: "G7: agi-run strace detaches at each child exec (strace -b execve, G7.2) -- a v5 post computes at untraced speed"
town: core
---
# hypothesis:g716111-g7-agi-run-strace-seccomp-bpf

## Measured
- thought-master-new [red] 15:2xZ 10-01: on director-thought-2 (v5) a torch training run took 1561 s per 1000 steps vs 94 s on the earlier non-v5 run (~16x).
- DG3 15:2xZ: every process of agi-post@thought-master-new from `claude` down (claude, MainThread, npm, gk) carries TracerPid = the unit's strace pid; the wrapper (script, sh, agi-run, agi-track) carries 0.
- Cause: .agi/nodes/.geometry/engine-wrap.md:26 `exec strace -qqfe%file -o'|agi-track' $H $c go` -- without --seccomp-bpf strace ptrace-stops on EVERY syscall of every descendant and filters %file in userspace. strace 6.8 on this box lists --seccomp-bpf.
## CLAIM
The agi-run strace detaches at each child exec (-b execve, G7.2; G7 tried --seccomp-bpf, which freed forks but not threads), so a v5 post exec-d descendants run at untraced speed while the harness process own %file opens still reach agi-track (a bash child opens, and on a pi post env->node, are lost by ruling).
## Dispatch line
Kid answers FIRST: what agi-track reads from the strace stream (which fields), and does --seccomp-bpf with -f change any line shape it parses.
## FALSIFIERS
- F1 the agi-run line runs strace without -b execve, or with --seccomp-bpf (strace refuses the two together).
- F2 under the new line a %file syscall of a forked grandchild is missing from the stream agi-track receives.
- F3 a futex/compute-heavy child under the new line is not materially faster than under the old (paste both timings, same box, same command).
## TESTS
a row that extracts the agi-run strace line from engine-wrap.md and runs it (strace present, else skip) on a tiny `sh -c` that opens a file from a grandchild, asserting the open appears in the -o stream; timings for F3 pasted in the round report, never as a test.
## FILE SCOPE
.agi/nodes/.geometry/engine-wrap.md (line 26 only) · one test file · this node.
## CEILING
production NET +0 lines (one token) · tests +40 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7 (kid c0a48f5f4, director record) -- F1 MET · F2 MET · F3 FIRES for threads
F1 red on old: assert '--seccomp-bpf' in ['exec', 'strace', '-qqfe%file', ...] -> 1 failed; after: 2 passed.
F3 timings (strace 6.8, -o /dev/null): single-thread getppid x100k untraced 0.038 s · old 3.416 s · NEW 0.058 s | 4 threads lock+50us sleep untraced 2.170 · old 3.946 · new 4.333 | 4 threads getppid x100k untraced 0.146 · old 14.153 · new 13.576.
READING: --seccomp-bpf frees the MAIN thread and forked processes (59x on the syscall loop) but strace 6.8 still stops every syscall of a clone'd thread (isolated: looping main + idle thread 0.062 s; looping thread + idle main 3.3 s). Torch intra-op threads stay slow: the 16x is NOT recovered by this round alone.
NEXT (a design call above this node -> belam/council): strace -b execve (detach from every exec'd child: compute children run untraced; agi-track then sees only the harness process's own file opens, not a bash child's) vs keep tracing children. G7 itself is strictly better and lands as is.

## CORRECTIVE G7.2 -- belam [decision] 15:23Z: PICK (a) strace -b execve (REPLACES --seccomp-bpf: strace refuses the two together)
BASE      CUT FROM de-base-G7 tip (worktree /mnt/agi-ram/worktrees/de-base-G7). No merge. Never rebase.
1. engine-wrap.md:26 -> `exec strace -qqf -b execve -e%file -o'|agi-track' $H $c go` (drop --seccomp-bpf). TRUE WHEN the harness process's own %file opens still reach the -o stream, an exec'd grandchild's compute runs at untraced speed (TracerPid 0 after its exec), and the test rows pin both.
2. extensions/agi/tests/test_agi_run_strace.py: F1 asserts `-b execve` (and no --seccomp-bpf); F2 asserts the DIRECT command's own open of a tmp file is in the stream; a new row asserts an exec'd grandchild's open of a second tmp file is NOT (the designed loss).
3. F3 timings pasted in the report (4 threads getppid: untraced vs G7 flag vs -b execve), never a test.
RESIDUE (by ruling, not a round): agi-track no longer records a bash child's file opens -- AND (DG3 measured 15:2xZ) on a PI post nothing past the first exec: /opt/agi/bin/pi is #!/usr/bin/env node, env execs node = a detach, so a pi harness own opens are lost too (claude = one ELF, its own opens stay traced); a fix if ~/track ever gets a reader: the pi row launches node on the script directly -- ~/track has no reader in the engine (engine-post.md:81 is its only reference).
FILE SCOPE engine-wrap.md (line 26) · extensions/agi/tests/test_agi_run_strace.py · this node.  CEILING production 0 net · tests +25 · Sonnet 5.5 subagent · 0 USD.

## DONE (director record, mur-de-base-g7)
G7 c0a48f5f4 -> G7.2 7917597c7 (belam pick a) -> mur-de-base-g7 accept_with_residue: R1 (title/claim/CLAIM/F1 named the banned flag) CLOSED by director 493c7c509 (the node id keeps its mint name) · M3 (the strace skip hid the F1 text guard) CLOSED by G7.3 a84f1c2fa (needs_strace on the 2 strace rows only; strace hidden: 1 passed 2 skipped) · R2 R3 refuted · M1 size headers = findings row 70 · M2 a shebang-harness row + the pi track loss = ruled (belam 15:23Z: ~/track has no reader) · grid version = the landing's.

## CORRECTIVE G7.4 -- DG3 [red] 17:02Z: -b execve ENDS every pi-harness post at start (the M2 ruling assumed telemetry loss only)
MEASURED  DG5 restart 16:53Z (key renewal) -> 15 restarts, agi-run exit 0 in 0 s. Bisect as the post user under a pty (script, fifo stdin), pi --no-session, timeout 8: strace -qqf -e%file -o'|agi-track' = rc 124 (alive) · + -b execve = rc 0 in 0 s · -b execve with the interpreter direct (node <cli.js>) = rc 124. WHY: pi is #!/usr/bin/env node; env execs node on the SAME pid -> strace detaches its only tracee and exits -> script ends -> the pty hangs up the session. claude rows are one ELF (DG2 runs -b execve fine). STOP-GAP live: DG5 h.conf H = node + cli.js by hand (before-value in dg3-mur-args).
BASE      CUT FROM the town trunk local-maxxing/season2/main tip (G7 landed 2e94bd1f3). Loop branch de-base-G7d. Never rebase.
1. engine.md agi-project (line ~80): the pi row's projected H launches the interpreter on the script directly, so the harness pid's FIRST exec is the final one (e.g. node on the pi entry point; the entry path read from ONE place -- a config cell or the PATH the unit already carries -- never a second hardcoded install path). TRUE WHEN a projected pi h.conf H starts with the interpreter and a claude row is unchanged.
2. extensions/agi/tests: (a) a row on the projection output (test_project_agi_box.py pattern): a pi row's H starts with the interpreter, a claude row's H starts with claude; (b) a needs_strace row under a pty (script -qfec, stdin a fifo): strace -qqf -b execve over an env-shebang script that sleeps 3 s returns in < 1 s (the fault, pinned) while the same script run as interpreter + path stays alive >= 2 s (the fix shape).
3. NOT in scope: engine-wrap.md agi-run (the -b execve line stays: belam pick a); the live DG5 h.conf (re-projection replaces the stop-gap after landing).
FALSIFIERS F1 a projected pi H still starts with an env-shebang launcher · F2 the claude row changes · F3 row (b) does not reproduce the 0 s exit on the old shape.
FILE SCOPE .agi/nodes/.geometry/engine.md (agi-project pi branch) · one test file (+ .agi/config.json ONLY for one path cell) · this node.  CEILING production net +2 · tests +45 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7.4 (kid de612d6af, director record)
NUMSTAT 56e68de01..de612d6af: engine.md 2/2 (net 0 vs +2) · test_agi_project_pi_direct.py 40/0 (vs +45). 9 passed (new + test_project_agi_box + test_agi_run_strace). Kid measured the fault needs the -o pipe sink: -o /dev/null keeps strace alive, -o'|cat' exits in 0.02 s. Director measured node <engine bin>/pi alive under the exact flags (rc 124 at timeout). mur-de-base-g7d: review accept_with_residue · verify DEMOTE (D1 D2 D3 confirmed; D4 D5 D6 refuted).

## CORRECTIVE G7.5 -- closes mur-de-base-g7d g74-code (D1 D2 D3 + verify missed: narrowing, config_max)
BASE      CUT FROM de-base-G7d tip (de612d6af + this node write). No merge. Never rebase.
1. (D1 + missed narrowing + config_max) agi-project picks P by grepping a literal /agi/bin out of the unit and appends a literal /pi: fail-open on an empty P (H = node /pi, exit 0) and narrower than PATH lookup. TRUE WHEN P = the FIRST directory of the projected unit's own Environment=PATH (the geometry, one source) that holds an executable pi -- PATH-lookup order, no /agi/bin selector literal -- and NO such dir = the projection exits 3 before writing any h.conf (the file's own [ -s ... ]||exit 3 idiom).
2. (D2) tests: the pi row asserts H == node <the expected dir>/pi --provider ... (the exact dir, from a fixture unit PATH pointing at a tmp dir holding a fake executable pi), never a prefix; a negative row (no pi on the unit PATH) asserts exit non-0 and no h.conf; a row where an earlier PATH dir lacks pi and a later one has it picks the later one.
3. (D3) the THOUGHT delta is the director's (written with this section).
DEMOTED   D4 D5 D6 refuted by verify · size header drift = findings row 70 (pre-existing) · the live-entry probe = the director's measurement above (rc 124), not a CI row (box path).
FILE SCOPE .agi/nodes/.geometry/engine.md (agi-project) · extensions/agi/tests/test_agi_project_pi_direct.py.  CEILING production net +2 · tests +30 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7.5 (kids deacbc886 + 64e0d61a8, director record)
G7.5 deacbc886: P = the first dir of the unit's own Environment=PATH holding an executable pi; refusal exit 3. G7.5b 64e0d61a8 AMENDS item 1 (the kid flagged the director's brief): the refusal fires only when P is empty AND this box has a pi row (line 80's own filter) -- a claude-only box projects without pi. NUMSTAT 86991a7d4..64e0d61a8: engine.md 1/1 · test_agi_project_pi_direct.py 27/5 · test_project_agi_box.py 5/2. 11 passed. Real geometry on this box: P = the engine bin dir, H = node <dir>/pi .... mur-de-base-g7e: review accept_with_residue · verify accept_with_residue (D1 confirmed with corrected evidence; D2 D3 refuted; M1-M4).

## CORRECTIVE G7.6 -- closes mur-de-base-g7e g75-code (D1 + M2 M3 M4; M1 = the record above)
BASE      CUT FROM de-base-G7d tip (64e0d61a8 + this node write). No merge. Never rebase.
1. (D1) the refusal reads ANY non-zero jq status as 'no pi row' (`!` inverts rc 5 parse errors): a valid pi row followed by a malformed one projects node /pi. TRUE WHEN only jq's rc 4 (no match) lets an empty P pass; rc 0 (a pi row) and any other rc (error) exit 3; a row with a pi row followed by a malformed row and no pi on PATH asserts exit 3 and no h.conf.
2. (M3) the refusal runs AFTER `mkdir -p $w;rm -f $w/agi-post@*`, so it strips the last good wants links and writes nothing back. TRUE WHEN P and the refusal are computed BEFORE the wants dir is touched (read the unit text from the section function s, not from $o); a row pre-seeds a wants link, forces the refusal, and asserts the link survives.
3. (M2) a row for the live shape: one box with a pi row AND a claude row, pi on PATH -> both h.conf written, pi H = node <dir>/pi, claude H unchanged.
4. (M4) the test reads the unit's PATH from the copied engine-root.md instead of re-typing its first element.
DEMOTED   D2 D3 refuted by verify · a malformed posts.md with a non-empty P is pre-existing (line 80 prints the valid prefix), not this node.
FILE SCOPE .agi/nodes/.geometry/engine.md (agi-project lines ~78-79) · extensions/agi/tests/test_agi_project_pi_direct.py (+ test_project_agi_box.py helper only if needed).  CEILING production net +1 · tests +35 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7.6 (kid 701212308, director record)
P + the rc-4 gate now run BEFORE the wants strip, reading the unit through s; only jq rc 4 lets an empty P pass. NUMSTAT dbb8e4746..701212308: engine.md 2/1 (net +1 vs +1) · test_agi_project_pi_direct.py 30/5. 13 passed; sh -n clean. mur-de-base-g7f: review + verify accept_with_residue (no demote): R1 a host-conditional row, R2 M3 half-closed at line 80, R3 this record.

## CORRECTIVE G7.7 -- closes mur-de-base-g7f g76-code (R1 R2; R3 = the record above + the THOUGHT)
BASE      CUT FROM de-base-G7d tip (701212308 + this node write). No merge. Never rebase.
1. (R2) line 80 `mkdir -p $w;rm -f $w/agi-post@*;s agi-post@.service>$o/...;[ -s ... ]||exit 3` still strips the wants links before its own refusal. TRUE WHEN the unit text is read ONCE (u=$(s agi-post@.service)), an empty u exits 3 BEFORE the wants dir is touched, P is derived from that same u (one s call, not two), and $o/agi-post@.service is written from u; a row empties the agi-post@.service section, pre-seeds a wants link, and asserts exit 3 with the link intact.
2. (R1) the exact-dir row is hermetic: the fixture PATH's first element is a tmp dir KNOWN to lack pi (never the live unit's first element); the live engine-root.md read stays only to assert the real unit carries an Environment=PATH line, and a missing line SKIPS with a named reason (no import-time TypeError -- resolve it inside a fixture or helper, not at module import).
3. (note) rename the malformed-row test so its name claims only what it asserts (rc 3 + no h.conf), or add the no 'node /pi' assertion.
DEMOTED   the jq rc-4 contract is jq 1.7's documented -e status (no output = 4) -- recorded, not a round · a missing posts.md = no pi row, pre-existing · size headers = findings row 70.
FILE SCOPE .agi/nodes/.geometry/engine.md (agi-project lines ~79-80) · extensions/agi/tests/test_agi_project_pi_direct.py.  CEILING production net +0 · tests +25 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7.7 (kid 020bc0fa4, director record)
agi-project reads the unit ONCE (u); an empty u exits 3 before the wants dir is touched; P and the written unit both come from u (real geometry: byte-identical, 1409 B). NUMSTAT a27b03e78..020bc0fa4: engine.md 2/2 (net 0) · test_agi_project_pi_direct.py 21/7. 14 passed; sh -n clean. mur-de-base-g7g: review + verify accept_with_residue, NO demote, no code defect; residues are coverage only.

## CORRECTIVE G7.8 -- closes mur-de-base-g7g g77-code (tests only; the record above closes the RESULT residue)
BASE      CUT FROM de-base-G7d tip (020bc0fa4 + this node write). No merge. Never rebase.
1. (D1) a row projects a pi or claude box and asserts $o/agi-post@.service == the agi-post@.service section text byte for byte (the printf newline fidelity).
2. (missed) the empty-unit row asserts its regex actually emptied a non-empty section (assert new != old) so it cannot pass on an empty geometry.
3. (missed) the unit_path fixture skips by name on a missing engine-root.md FILE as well as a missing PATH line.
4. (missed, text pin) a row asserts the agi-project section text calls `s agi-post@.service` exactly once (the one-read property, pinned at the bytes).
DEMOTED   D2 refuted by verify · size header = findings row 70.
FILE SCOPE extensions/agi/tests/test_agi_project_pi_direct.py ONLY (no production bytes).  CEILING production 0 · tests +25 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7.8 (kid 5061160a4, director record) -- G7 residues 0
Tests only (production byte-identical): byte-for-byte unit row, non-vacuous empty-unit row, unit_path skips on a missing file, one-read text pin. NUMSTAT 624459275..5061160a4: test_agi_project_pi_direct.py 26/1. 16 passed. mur-de-base-g7h: review + verify accept_with_residue; review D2 D3 D4 REFUTED by verify (one unconditional unit write before the row loop; the tmp copy equals the committed blob by construction; the text pin is the brief's own). D1 = this record. DEMOTED by measured reason (none can turn a row falsely green): the test's escaped-dot range is STRICTER than s()'s (fail-loud) · a moved unit section fails one row and skips another (no false green) · _unit_and_section's unused engine_text parameter (cosmetic). CHAIN: G7.4 de612d6af -> G7.5 deacbc886 + G7.5b 64e0d61a8 -> G7.6 701212308 -> G7.7 020bc0fa4 -> G7.8 5061160a4; murs g7d demote -> g7e g7f g7g g7h accept_with_residue, each residue closed in-loop.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
G7.4-G7.7 (DG3 17:0xZ-18:0xZ): G7.2's -b execve was ruled telemetry-only (M2), but on a PI row it ENDS the session: pi is an env-node shebang, env re-execs node on the same pid, strace detaches its only tracee and with the -o pipe sink exits, the pty hangs up (DG5: 15 restarts after its 16:53Z key restart). The fix moves the interpreter into the projected H (node on the pi entry) instead of dropping -b execve, keeping belam's pick (a). G7.5 found pi by walking the unit's own PATH (the geometry, one source, PATH order) instead of a literal /agi/bin; G7.5b narrowed the refusal to boxes with a pi row after the kid showed the brief blocked claude-only boxes; G7.6 made a jq error refuse (only rc 4 passes) and moved the refusal ahead of the wants strip; G7.7 reads the unit once so NO refusal can strip the last good projection. Prior THOUGHT (G7.2 pick a, timings) = this node's grid history.
<!-- THOUGHT:END -->
