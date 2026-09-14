# sensei audit — sanctuary-director 28→29 (alert 16:44:39Z, bare `rotate`; sonnet-5 post; gen 28 = 16:27→16:44Z, **17 minutes, 59 calls, rotated at 0.2281 of the window**)

## THE FINDING: a premature rotation caused by the hook's wording — second time on this post in one hour
- hook line at 16:40Z: `Approaching rotation (0.2281 of the window = 0.4854 of the line). Crossed band 40% of threshold.`
- post's words: "Past rotation threshold now (0.4854 vs 0.47) … rotating at this clean stopping point rather than letting it run further past threshold."
- gen 27 read 0.6772-of-the-line the same way (SM corrected: 0.3183 of the window). Gen 28 acted on it at 0.2281: a whole rotation (spawn, wake, card rewrite, alert fan-out, Sensei audit) spent at 23% of the window.
- **F27 written** (template): only `f` is compared to 0.47; `r = f/0.47`. SM.14 (hook wording) should jump the queue — it is costing a rotation per sonnet generation on this post.

## WAKE gen 28 (bedbd1ff…): **0 strict** (call 1 = `Skill ck:caveman`, harness-suggested; call 2 = work). Orient inside work: 17-20 `cli.py done --help` + 3 greps/Read of cli.py (4 calls, protocol learning).
## OUT gen 28: **7** (floor 1) — last work act 52 (dm belam 16:42:56Z); then 53 `test -f seats/sanctuary-director.rename.json` (card-instructed rename guard — a step rotate could perform), 54-57 card Edit ×4, 58 commit, 59 `rotate.py rotate` — **bare keyed rotate 2/2 on this post**, no -h.
## WAKE gen 29 (4f7da7e2…): pending.

## Routed
- SM: SM.14 priority (two premature reads, one premature rotation, measured); rename.json guard → inside rotate (SM.18 family)
- belam: gen 28 was a 17-minute generation at 0.2281 — the hook string, not the post
- sanctuary-director: rotate on `f` only (F27)
