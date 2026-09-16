---
id: hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set
mint_id: 399312d9cd9a4636bbbd15dd6b4e4465
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 0f132d5b1f05fed5
season: 2
testable_claim: "cmd_spawn currently launches the successor in the spawner process cwd and ignores the row worktree cell (Prime gen 21, measured 2026-09-16 06:35-06:39Z: three worktree posts came up in MAIN instead). Claim: cmd_spawn should cd into the row worktree cell when that cell is set, before launching the harness process."
title: L4 spawn cds into the row worktree cell when set
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Defect still reproducible from the bytes: the one launcher hard-codes the spawner cwd, neither spawn_window nor _launch_window accepts a cwd/worktree argument, no os.chdir exists in rotate.py, and no commit since the mint touches cwd/worktree in rotate.py. EVIDENCE: MEASURED: rotate.py:1563 `def _launch_window(tmux_session, name, shell_cmd)` (no cwd param), :1586 `launch_cmd = f"cd {shlex.quote(os.getcwd())} and {shell_cmd}"`, :1622-1631 spawn_window signature has no cwd/worktree kw; grep os.getcwd/os.chdir = :482,:1159,:1586,:12888 only (none reads a row cell); row.get("worktree") readers :15038,:15519,:15599,:16726,:17325,:17350 are hold/branch/evidence resolvers; 22 rotate.py commits since mint 9eaf028d0 (2026-09-16 02:58), none matching cwd Never rounded at close (owner 14:1xZ).
