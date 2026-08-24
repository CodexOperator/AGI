---
confidence: 0.95
evidence_runs: []
id: "mvp:strict-goal-refs"
parents:
  - goal:g5
subgraph: false
tags:
  - g5
  - integrity
title: "Add --strict-goals flag to make goal refs fail loudly"
type: mvp
---

**What --strict does today:** 
`snapshot-goals.py` lines 315-316 describe `--strict` as "exit 1 if a node references an unknown goal id". However, lines 425-428 show the actual behavior: it exits non-zero if ANY `unresolved` parent reference exists (not just goal references). The distinction between goal-prefixed refs and other parent refs (lines 393-407) is only used for message formatting, not for the exit logic. Both types increment the same `unresolved` counter that gates the failure.

**Counts on the live tree:** 
Total INTEGRITY lines: 88 (split: 7 empty entries [malformed frontmatter] + 81 unresolved parent references). All 81 references say "references unknown parent" — zero say "references unknown goal".

**Would adding --strict to driver.sh break the loop:** 
YES. The 81 unresolved parent references (mostly typos like `hypothesis:*` instead of `hyp:*`, and dangling verdicts) would cause every run to fail on line 80 of driver.sh (line numbers from current HEAD).

**The change, as applicable code:** 

G5 asks specifically: "fail loudly when a seed node points at a goal id that does not exist." This is narrower than all parent references — it is only goal-prefixed refs. So option (b) is correct: add a `--strict-goals` flag that narrows the failure condition.

**In `snapshot-goals.py`:**

Current (line 315-316):
```python
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a node references an unknown goal id")
```

Replace with (add new flag):
```python
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a node references an unknown parent id")
    ap.add_argument("--strict-goals", action="store_true",
                    help="exit 1 if a node references an unknown goal id")
```

Current (line 425-428):
```python
    if unresolved and args.strict:
        print(f"ERR: {unresolved} unresolved parent reference(s) (--strict)",
              file=sys.stderr)
        return 1
```

Replace with:
```python
    if unresolved and args.strict:
        print(f"ERR: {unresolved} unresolved parent reference(s) (--strict)",
              file=sys.stderr)
        return 1
    if unresolved and args.strict_goals:
        # Count and fail only on unresolved goal references (goal:* prefixed)
        unresolved_goals = sum(
            len(refs[ref]) for ref in sorted(refs)
            if ref not in known_ids and GOAL_ID_RE.match(ref)
        )
        if unresolved_goals:
            print(f"ERR: {unresolved_goals} unresolved goal reference(s) (--strict-goals)",
                  file=sys.stderr)
            return 1
```

**In `driver.sh` line 80:**

Current:
```bash
      python3 "$PLUGIN_ROOT/bin/snapshot-goals.py" 2>&1 | tee -a "$LOG"
```

Replace with:
```bash
      python3 "$PLUGIN_ROOT/bin/snapshot-goals.py" --strict-goals 2>&1 | tee -a "$LOG"
```

**What this does not fix:** 
The 81 existing unresolved parent references (non-goal) remain and continue to print to the log as warnings. These are mostly prefix typos (`hypothesis:` vs `hyp:`) and broken node chains in the experiment → verdict flow. They should be fixed separately. This change makes only goal-reference failures hard-stop the loop per G5's wording.

