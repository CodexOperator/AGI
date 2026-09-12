# parent role pass — from the demoted round L4.327 (owner ask via the point, 22:0xZ)

Record: `.agi/sessions/iter-L4.327/` — parent **a00-6b41b0ad** (tier parent, level small, deepseek-v4.1-flash; the point's dm named kid 1 `a00-0ce94716` as the parent), kids a00-0ce94716 / a00-6f15cc42 / a00-ec46a138, orphan scaffold a00-2d68b988. Demoted 21:5xZ by Prime XVII (mur-48): veto answer unauthenticated, HELD line on the wrong push leg, no filing wire, empty lists → null, expires_at = filing time. Kids' tests passed against the defect; parent accepted lean_proved 65/70 from reports; director harvest re-ran suites.

## what the parent was handed (measured)
- `context.md` 78,731 bytes = **75 KB subtree dump** (Zoom SMALL: ~40 sibling hypotheses under g15) + **3.6 KB "Your Task" = the generic KID contract** (spawn one child, report fields, verdict grammar, "stuck >2 → pending"). Zero parent-role text in the prompt.
- `spawn.json.brief` 11,113 bytes: "kid" ×37, **"bytes" 0, "probe" 0, "refut*" 0, "adversar*" 0, "harvest" 0, "re-run" 0**. The parent is told how to cut and merge kids, never how to disbelieve one.
- Parent's own log: it DID re-run `test_veto+test_rings+test_send+test_write = 423 passed` "on the disk bytes, not on the reports" — and still passed a defect, because the tests were the kids' tests. Re-running a kid's tests is agreeing with its report at one remove. Struggle logged: `dispatch.py` exit 0 on a spawn that scaffolded a node and never registered (480 s of polling; orphan deprecated by hand).

## the pass — three verdicts, in order
1. **ELIMINATED** — the 75 KB sibling dump. A parent's zoom = its target hypothesis, the goal, the claim conjuncts, its own kids' nodes. Template: a per-tier zoom shape (`parent` ≠ `kid` ≠ `director`); ~95% of the parent's input bytes are not needed for its task.
2. **AUTOMATED** — a parent may not accept `≥ inconclusive_lean_proved:50` from a kid without a **negative probe it ran itself**, one per claim conjunct, recorded on the round (`probes:` on the experiment/verdict, like `evidence_runs`). Harness: `cli.py done` for tier parent refuses without the probe record; template: the probe classes a claim type owes (auth: call the path with no identity; gate: exercise the other leg; wire: file through the CLI, not the function). After the harness half, a new probe class is a template line.
3. **CONSOLIDATED** — the parent prompt carries a **parent section** in the same "Your Task" slot (one template, tier-keyed): "a kid's tests are its claim, not your evidence; the harness hands you the kid's DIFF (bytes), not `kidN-result.txt` (report) — read the diff, run the negative probe, then verdict." Consolidates report-reading + verification into the one harvest call the parent already makes.
4. **code** — `dispatch.py` must exit non-zero when it scaffolds a node and no agent record follows (the parent's struggle; 480 s + a hand deprecation).

## routed
Lines 1-4 → sensei-director (g15; the parent prompt lives in dispatch/zoom, not `config:rotations`). Received-line → point. Deeper pass (read all three kids' reports vs their diffs for the exact sentence each layer believed) banked to the successor.
