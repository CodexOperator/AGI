# Autoresearch ideas (not yet pursued)

- **SM.105 / workflow.py — a true wall extension, not a re-dispatch.**
  `_run_stage_proc` (workflow.py ~L1541) grants a producing stage one
  `extension_s` but implements it as a fresh `subprocess.run` after the first
  one was killed, so a stage that needs `wall + epsilon` is killed on the
  re-run too and a real pi stage pays a re-run (double spend). A true
  continuation needs `Popen` + a poll loop that checks the stage's
  `progress_file` mtime between polls and kills only when silent for
  `silence_s`, capturing stdout/stderr to temp files to avoid PIPE deadlock.
  Cost: ~15 of the test_workflow.py tests mock `subprocess.run` and would need
  their seam moved to the new helper. Measured on 2026-09-18 (SM.105, parent
  a00-cbd7ac18, probe `extension-producing-stage-extended`).
