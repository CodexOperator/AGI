---
id: hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller
mint_id: b33b577a2f98473a8ec8a172ba0ff775
type: hypothesis
parents:
  - goal:g1.10
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 3044096fad95a883
season: 2
testable_claim: "MEASURED BY A READ-ONLY SURVEY WITH AN ADVERSARIAL PASS (Prime, 2026-09-10; registered as workflow prime-open-questions): verification.py:226-255 acquire_suite_lock is a plain pid-file at <graph>/sessions/verify-suite.lock, no fcntl/flock anywhere in the file, written ONLY behind --suite (verification.py:517-519) and unlinked in a finally (:543-547) — one caller, confirmed by repo-wide grep whose only other hits are unit tests. AT LEAST SEVEN lock-free ways start the same suite, and two are ENGINE CODE, not documentation: season.py's merge-up suite-green gate runs DEFAULT_SUITE = 'python3 -m pytest extensions/agi/tests/ -q' (season.py:1016) with no lock, and commands.py run tests is a first-class graph-declared command that also takes none. So every merge-up this loop has run the suite past the window the Prime believed it was granting. PRIME RULING already recorded in goal:g17.1: the window is ADVISORY until this lands. CLAIM: the acquisition moves to the resource — a session-scoped AUTOUSE FIXTURE (a fixture, never a pytest_* hook) in extensions/agi/tests/conftest.py that calls the existing verification.acquire_suite_lock against a root resolved from Path(__file__), never cwd, and that NO-OPS when an inherited environment marker is already set. THE MARKER IS NOT POLISH, IT IS THE WHOLE ROUND: the suite already runs pytest inside pytest (test_tier_gate.py, three nested runs asserting code == 0) and verification.py --suite spawns pytest as a child that inherits os.environ (verification.py:384-386 passes no env=), so without the marker the fix self-refuses and breaks four tests plus --suite entirely. The marker name must NOT begin with AGI_ or AUTORESEARCH_ because extensions/agi/conftest.py:37-39 strips those prefixes — e.g. VERIFY_SUITE_LOCK_PID, set into os.environ by whichever process acquires. Then DELETE the acquisition at verification.py:517-519 and the release at :543-547 so there is exactly one acquirer. PROVED BY: a bare python3 -m pytest extensions/agi/tests/ creates the lock file with its own pid and removes it on exit; a second bare pytest started while the first runs REFUSES with a message naming the holder pid; verification.py --suite still passes end to end; test_tier_gate.py's nested runs still pass; season.py merge-up's gate now contends for the same lock. DISPROVED BY: any path that starts the engine's tests without the lock file existing during the run, or a nested pytest that deadlocks. HARD RULES: only ONE suite at a time on this box while proving it — coordinate the window with the Prime; conftest.py is engine source under extensions/, edited through write.py if it is a build node and directly if it is not; never weaken test_tier_gate.py to make this pass."
thought_session: f3b92df1
title: The suite lock guards a caller, not the resource; it moves into conftest.py behind a reentrancy marker
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
