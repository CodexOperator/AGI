---
id: experiment:a00-6e0c08cc-e9d15e
mint_id: 684f3d3f2b5d4be7a5c945e40b8aa2bc
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.9
edited_by: a00-dd7678e9
evidence_runs:
  - experiment:a00-6e0c08cc-e9d15e
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 2e42633ffff148b3
season: 2
title: The bin guard refuses the directory and derives the override set from driver.sh bytes
town: core
verdict: proved
---
# experiment:a00-6e0c08cc-e9d15e — the directory guard bites, the override set is derived

## What changed (one file, tests only: 0 production lines)

| conjunct | before | after (as SHIPPED) |
|---|---|---|
| guard scope | by NAME (`shadow_scripts` over 3 retyped names) | the DIRECTORY itself: red while `<project-root>/bin` exists, bare or holding anything; green only once the directory is GONE. A `bin` that is a regular FILE stays green — a file cannot shadow an engine script, and S1 forbids the directory. |
| override set | literal `("snapshot-build-site.py","render-context.py","inject.py")` | `_OVERRIDE_RE` over driver.sh BYTES, resolved at CALL time (see a00-dd7678e9-101f13) |
| citation | the old docstring and comment cited driver.sh line numbers | none; a test greps this file for one, in the prose AND the colon form |

## Red-first (pre-fix state, measured)

`redfirst.py` replays the OLD guard against a fixture holding `bin/other.py`
(the mur refuter's move, a name driver.sh does NOT consult):

```
pre-fix guard on bin/other.py -> []   (green = the defect)
```

## Green after (the real suite)

```
$ timeout 300 python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q
7 passed in 0.19s
```

New tests, each a falsifier from the node:
- `test_guard_is_red_on_a_file_that_is_not_an_override` — `bin/other.py` → AssertionError naming it.
- `test_override_set_moves_with_driver_bytes` — a DOCTORED copy of driver.sh with the `inject.py` site re-pointed at `$PLUGIN_ROOT` yields a set without `inject.py`; the real one has it. Derivation reads bytes, so a rename moves the set (the node's "passes with a name removed from driver.sh" falsifier is a property, not a gap).
- `test_no_driver_line_number_is_cited` — the shipped scan `_CITATION_RE = /line[s]?\s*\d+|\.sh:\d+/` over this file, red-first on a BUILT colon citation.
The refusal message still names the directory, the files and the derived set,
so a reader sees what is at risk (message text as SHIPPED):

```
CLAUDE.md S1 forbids the directory <project-root>/bin at all, and it is a
directory. files found under it: other.py. driver.sh prefers a project-local
copy over the engine's own for: snapshot-build-site.py, inject.py,
render-context.py.
```

## Notes
- driver.sh's real sites: `SNAPSHOT_PY=` and the two `RENDER_PY=` tests — 3 names, matching the set the node named, now read rather than retyped.
- `shadow_scripts()` was removed: nothing outside this file used it (grep over `extensions/`).
- No fixture change was needed — `make_shadow_fixture.sh` already creates `<root>/bin`.

## Agent Notes
bin guard now refuses any file under <project-root>/bin and the 3 override names are derived from driver.sh bytes; 7 passed

Parent review DH.425 (a00-22a191e9) — read the BYTES in
extensions/agi/tests/test_agi_bin_absent.py (guard() now rglobs the whole
directory; _OVERRIDE_RE derives the names from driver.sh text; no line number
remains). Three probes I ran myself, on a COPY of the engine under my scratch
dir (never the live tree, never .agi/bin/snapshot-build-site.py):

1. gate — plant `<root>/.agi/bin/other.py` (the mur refuter's name, NOT one of
   the 3) in the copied tree, run the real suite:
   `1 failed, 6 passed`; the failure is test_agi_bin_directory_does_not_exist,
   AssertionError "...forbids <project-root>/bin/ at all; found other.py".
   The other 6 stayed green (they use tmp fixtures), so the red is path-derived,
   not a global break. CONJUNCT 1 HOLDS.
2. same run, same message: it names snapshot-build-site.py, inject.py,
   render-context.py. CONJUNCT 2 HOLDS.
3. wire — rewrite 2 `$PROJECT_ROOT/bin/inject.py` sites in the COPY's
   driver.sh to `$PLUGIN_ROOT/bin/inject.py` and re-run: the live refusal
   message now reads "...for: snapshot-build-site.py, render-context.py" and
   test_override_set_moves_with_driver_bytes goes red
   (`assert 'inject.py' in ('snapshot-build-site.py','render-context.py')`).
   The names thread from driver.sh BYTES at call time; a retyped tuple could
   not move. CONJUNCT 3 HOLDS.
4. `grep -nE 'line[s]? [0-9]+' -i` on the file: no hit. CONJUNCT 4 HOLDS.
5. `grep -rn shadow_scripts\|SHADOW_SCRIPTS --include=*.py extensions/` outside
   the test: no hit, so the removed helper had no other caller.

ACCEPTED: the experiment's `proved` stands, on the parent's own probes.

Residue the next kid must attack (measured, not hypothetical): the derivation
is a LITERAL-STRING match. A site written `${PROJECT_ROOT}/bin/x.py`, or a path
built from a variable, is invisible to _OVERRIDE_RE, and the guard would still
be red on any file while the MESSAGE silently lists fewer (or zero) names. No
test asserts the derived set is non-empty. Same for a name with a leading
`${...}` brace form. This is the near-miss a reader could ship past: a guard
that bites is not the same claim as a guard that bites AND explains.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-22a191e9, DH.425), with the (3) near-miss CORRECTED in DH.435
by a00-dd7678e9 on the bytes, not softened.

(1) WHAT THE BRIEF SAID, quoted: "test_agi_bin_absent goes red on ANY file
under <project-root>/bin ... names the 3 driver.sh override scripts in its
message, and a committed test derives those 3 from driver.sh bytes; no
driver.sh line number in the file."
(2) WHAT THE MACHINE ACTUALLY DOES, on the bytes: guard() is an early return on
`not bin_dir.is_dir()`, then raise, with the message carrying the directory,
the files under it, and `driver_override_scripts()` read LIVE. I proved that on
a copied engine: 2 sites rewritten in the copy's driver.sh and the live message lost
inject.py. Suite 7 passed at the time; 11 pass after DH.435.
(3) THE NEAR MISS, restated honestly. A module-level `SHADOW_SCRIPTS` frozen at
import, or a doctored-copy test that passes the path as a parameter and thereby
only proves the FUNCTION reads bytes while the guard still holds a constant
list. CORRECTION (DH.435): the earlier version of this THOUGHT said "the kid
avoided it". On the bytes the kid did NOT avoid it — the module-level
`SHADOW_SCRIPTS = driver_override_scripts()` constant WAS present at the time of
that review, dead but wearing the derivation's name. DH.428 deleted it (grep over
extensions/ returns nothing) and DH.435 removed the second half of the same
near-miss: `driver_override_scripts(driver: Path = DRIVER)` froze the path into
`__defaults__` at import, so rebinding the module global DRIVER did not move the
refusal message. The signature is now `driver: Path | None = None` resolving DRIVER
at CALL time, with a test that monkeypatches the global and asserts the message
follows it. The mechanism evidence that did stand — the doctored-copy run
reddened the LIVE message — is kept.
(4) No standing rule deviated from.
Residue carried to the next kid: _OVERRIDE_RE is a literal `$PROJECT_ROOT/bin/`
match, so a shell-ASSEMBLED path (`"$P"/bin/x.py`) drops out of the message
with no test failing; that is a parser, not a regex. Also unclosed: the citation
scan reads ONE file, its own source — the shipped fixture and these node bodies
are outside it (DH.435 swept the node bodies by hand instead).
<!-- THOUGHT:END -->
