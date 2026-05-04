---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit: Git Remote and Commit Hygiene

## Scope

Commit and push hygiene for the unified `~/.hermes/agi/` repository, the `~/.hermes/agi-tree/` data repository, and the legacy `CodexOperator/autoresearch-tree` github mirror. Fold work lands on a feature branch and is merged into main only after bug-sweep clears. The unified repo and the data repo each acquire a new remote on `CodexOperator`. The legacy github mirror is archived after verification with a README pointer to the new canonical home. Authentication is via the existing `CodexOperator` github session.

## Requirements

### R1: Fold work lands on a feature branch
**Description:** All fold work inside `~/.hermes/agi/` lands on a feature branch named `agi-unification` (or `agi-unification-*` if the work is split into sub-branches). The main branch is updated only via merge after bug-sweep clears.
**Acceptance Criteria:**
- [ ] A branch whose name is `agi-unification` or begins with `agi-unification-` exists in `~/.hermes/agi/`.
- [ ] All fold commits introduced by this cycle are reachable from that feature branch (or from a branch whose name matches the prefix).
- [ ] No fold commits are added directly to local `main` before bug-sweep records all checks passing.
- [ ] The merge of the feature branch into main occurs only after the most recent bug-sweep aggregate report records all checks passing.
**Dependencies:** cavekit-topology-fold.md R1.

### R2: Unified repo initialised against CodexOperator/agi and pushed
**Description:** `~/.hermes/agi/` is initialised against the `CodexOperator/agi` remote. After verification clears, the main branch is pushed and the pushed history includes the subtree-merged commits from both prior origins.
**Acceptance Criteria:**
- [ ] `git remote -v` inside `~/.hermes/agi/` lists an origin URL referencing `CodexOperator/agi`.
- [ ] After the final push, the local main branch tip equals the remote main branch tip.
- [ ] After the final push, `git log origin/main..HEAD` inside `~/.hermes/agi/` returns no commits.
- [ ] The pushed history contains at least one commit hash from the prior `~/.hermes/agi/` origin and at least one commit hash from the prior `~/autoresearch-tree/` origin.
- [ ] `gh repo view CodexOperator/agi` shows the new repository with content.
**Dependencies:** R1, cavekit-topology-fold.md R6.

### R3: Data repo initialised against CodexOperator/agi-tree and pushed verbatim
**Description:** `~/.hermes/agi-tree/` is initialised against the `CodexOperator/agi-tree` remote. The main branch is pushed verbatim — no project data is modified as part of this cycle.
**Acceptance Criteria:**
- [ ] `git remote -v` inside `~/.hermes/agi-tree/` lists an origin URL referencing `CodexOperator/agi-tree`.
- [ ] After the final push, the local main branch tip equals the remote main branch tip.
- [ ] After the final push, `git log origin/main..HEAD` inside `~/.hermes/agi-tree/` returns no commits.
- [ ] No commit on the pushed branch modifies project data files outside what was already present locally before the cycle began.
**Dependencies:** None.

### R4: Legacy github mirror archived after verification clears
**Description:** `github.com/CodexOperator/autoresearch-tree` is moved into archived state after bug-sweep records all checks passing. Before archival, the repo's README is updated to point at `CodexOperator/agi` as the new canonical home. The local `~/autoresearch-tree/` directory's git remote configuration is left intact until that legacy directory is removed (deferred to TODO).
**Acceptance Criteria:**
- [ ] Until bug-sweep records all checks passing, `gh repo view CodexOperator/autoresearch-tree` does not report archived status.
- [ ] After bug-sweep records all checks passing, `gh repo view CodexOperator/autoresearch-tree` reports archived status.
- [ ] Before archival, the README of `CodexOperator/autoresearch-tree` contains a pointer to `CodexOperator/agi`.
- [ ] The git remote configuration in the local `~/autoresearch-tree/` directory is unchanged by this kit.
**Dependencies:** R2, cavekit-bug-sweep.md R3, cavekit-topology-fold.md R10.

### R5: Verification of remotes and push completeness
**Description:** Each unified repo shows the expected origin URL, nothing is locally ahead of its remote after the final push, the new github repo is observable, and the legacy github mirror reports archived status.
**Acceptance Criteria:**
- [ ] `git remote -v` in `~/.hermes/agi/` lists exactly one origin and it references `CodexOperator/agi`.
- [ ] `git remote -v` in `~/.hermes/agi-tree/` lists exactly one origin and it references `CodexOperator/agi-tree`.
- [ ] `git log origin/main..HEAD` is empty in `~/.hermes/agi/` after the final push.
- [ ] `git log origin/main..HEAD` is empty in `~/.hermes/agi-tree/` after the final push.
- [ ] `gh repo view CodexOperator/agi` shows the new repository with content.
- [ ] `gh repo view CodexOperator/autoresearch-tree` reports archived status after the archival step.
**Dependencies:** R2, R3, R4.

### R6: GitHub authentication via CodexOperator and consistent commit style
**Description:** The github user used for all pushes is `CodexOperator`; authentication is already configured and no new credential setup is performed. Commit messages follow the conventions visible in the existing `~/autoresearch-tree/` and `~/.hermes/agi/` git logs.
**Acceptance Criteria:**
- [ ] `gh auth status` reports an authenticated session for the `CodexOperator` user.
- [ ] No prompt for credentials is required during the push step.
- [ ] Commit messages on the feature branch use the same prefix and style conventions visible in the most recent ten commits on each prior origin's main branch.
**Dependencies:** R1.

## Out of Scope

- Opening pull requests upstream to `davebcn87/pi-autoresearch`.
- Renaming `CodexOperator/autoresearch-tree`; it is archived rather than renamed.
- Configuring branch protection rules or required-status checks.
- Setting up CI workflows.

## Cross-References

- See also: cavekit-topology-fold.md (R6 motivates the subtree-merged history pushed under R2; R10 motivates the archive sequencing under R4).
- See also: cavekit-bug-sweep.md (R3 — push and archive gated on sweep clearance).
- See also: cavekit-deferred-todo.md (the TODO file committed under that kit is pushed under R2 here).

## Changelog

_(empty)_
