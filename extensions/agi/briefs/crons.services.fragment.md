# crons.services.fragment — proposed `services:` table for `.geometry/crons.md`

Shipped by `experiment:a00-effd25bd-b5e162` (L4.116) so the PRIME can land the
reaper-as-a-persistent-systemd-service table at merge-up WITHOUT the round
touching the live `crons.md` (which the grid_sync cron reads as live effect —
a `services:` table landing in the live node would install the unit on the
box by itself, which the claim explicitly reserves for the prime's step).

The applier behind this table is `crons.py apply --unit-dir …` (renders
`services:` into unit files) plus the `--unit-dir` seam. The `exec_start`
below names `heal.py watch`, the watcher subcommand that the serial successor
on the heal.py lane implements; until that lands the unit would start
nothing, so it MUST NOT be enabled live before `heal.py watch` exists. That
ordering — watcher first, table second — is why this is a fragment, not a
landed edit.

## Proposed YAML to add to the live `crons.md` frontmatter

```yaml
services:
  agi-reaper:
    enabled: true
    exec_start: "<engine>/extensions/agi/bin/heal.py watch --root <project-root> --poll-s 30"
    restart: on-failure
    working_directory: <project-root>        # the main checkout; omit for auto
    environment: {}                          # never a credential path
```

`<engine>` and `<project-root>` are filled by the prime at merge-up (G8.2:
no machine layout in a graph node).

## Exact edit lines (the prime's step — never a kid's)

```bash
python3 extensions/agi/bin/write.py cron:crons 'set services {"agi-reaper": {"enabled": true, "exec_start": "ENV-ABS/bin/heal.py watch --root PROJECT --poll-s 30", "restart": "on-failure", "working_directory": "PROJECT", "environment": {}}}'
python3 extensions/agi/bin/crons.py apply --unit-dir ~/.config/systemd/user/   # prime, once
```

The `apply --unit-dir ~/.config/systemd/user/` installs the unit; the plain
`crons.py apply` (the grid_sync self-reapply line) never touches units, so a
drift re-apply needs the explicit seam — recorded as the leftover half of the
live proof.

## What the fixture proved (this round)

- No `services:` table → `--unit-dir` apply leaves the unit dir untouched
  (byte-for-byte no-op).
- Table present → unit file rendered byte-for-byte, idempotent on re-apply.
- `crons_live: false` → unit file removed; `systemctl --user disable --now`
  intent recorded through the seam, never executed by any test.
- `--dry-run` writes nothing.

The real `systemctl --user enable --now mow --now + daemon-reload` against
`~/.config/systemd/user/` remains the prime's step and is the residue named
in the verdict.