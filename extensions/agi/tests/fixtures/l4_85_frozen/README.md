# l4_85_frozen — committed frozen copy of the L4.85 kid artifact

**hypothesis:l4-frozen-evidence-lives-outside-the-reapers-scan** — this fixture
is the committed, read-only capture of the real L4.85 frozen artifact. It sits
UNDER `extensions/agi/tests/fixtures/`, deliberately OUTSIDE the live reaper's
scan roots, so the live `heal.py` service can never mutate it in place.

## Provenance

- Source: `/home/ubuntu/work/agi/.agi/worktrees/a00-e9572046/.agi/sessions/iter-L4.85/`
  (the kid `a00-d0a67d4f`, iteration L4.85).
- The LIVE copy of that `agent.json` was mutated IN PLACE by the live reaper
  service: status was rewritten from `running` to `stalled` and a `stalled_at`
  field was added. The original `running` record no longer exists on the live
  disk.
- These fixture files were RECONSTRUCTED AFTER that mutation from the real
  artifact:
  - `manifest.json` — byte copy of the real manifest (`agents[0]: status
    "running", pid 2130989`).
  - `a00-d0a67d4f/agent.json` — the real record restored to its pre-reaper
    state: `status "running"`, pid `2130989`, `stalled_at` REMOVED. Every
    other field is the real one.
- This is a frozen copy of a real artifact, NOT a hand-fabricated record. The
  pid and all fields are the real ones. Nothing here is invented.
- The `command` / `context_file` / `log_file` strings still point at the
  original live paths; they are kept verbatim for authenticity even though
  those paths no longer resolve for this fixture.

## Why outside the scan

The reaper's `_discover_rounds` globs (heal.py) are exactly:

    <root>/sessions/iter-*/manifest.json
    <root>/worktrees/*/.agi/sessions/iter-*/manifest.json

with root = `<repo>/.agi`. This fixture lives at
`<repo>/extensions/agi/tests/fixtures/l4_85_frozen/`, which matches neither
glob and is not under `<repo>/.agi/worktrees` nor `<repo>/.agi/sessions`. The
reaper cannot reach it.
