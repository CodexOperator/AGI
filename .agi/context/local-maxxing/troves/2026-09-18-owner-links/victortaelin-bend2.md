# X-THREAD: @VictorTaelin — Bend 2 launch
Slice X-THREADS / local-maxxing town. READ-ONLY (no key, no install, no clone). Read 2026-09-18Z.
Tag legend: MEASURED = quoted from a page/file read here; ESTIMATE = inference.

## 0. The post (pointer)
- Post: https://x.com/VictorTaelin/status/2100374221671051472 — @VictorTaelin, created **Thu Sep 17 2026** (MEASURED, fxtwitter `created_at`; 1,975 bookmarks-class post, 31k? — see JSON). JSON via `https://api.fxtwitter.com/VictorTaelin/status/2100374221671051472`.
- `is_note_tweet: true`; **no `urls` facets, no card, no quoted tweet** (MEASURED — the post itself carries no outbound link; the artifact is named, not linked).

## 1. What is claimed (all MEASURED, verbatim from post text)
- "Bend2 launches tomorrow (maybe?)" (post dated Sep 17; site last-updated 2026-09-17).
- "Bend2 doesn't have interaction nets, because I could not make them as fast as lower-order variants on everyday hardware … closer to C than to Haskell."
- "JS-like closures and allocation (**yet no GC**!), **Lean-like dependent types**, and … Bend1-like parallelism (**with up to 100x faster raw speeds**)."
- "fast like C, parallel like CUDA, feels like Python … a complete proof system, like Lean."
- "we have 32-bit numbers now, and **Bend1's 2 GB memory limit has been lifted to 8 TB**."
- "**u64 and f64 are out**. I did try adding them, but **Metal doesn't even support f64**."
- "our team of 4 humans (and 25 non-humans!)"; "expect bugs and limitations"; kernel "drifted", "early days exploits are not impossible".

## 2. The artifact it points to
- Repo moved: `HigherOrderCO/Bend2` (created 2026-09-16T16:26Z) → **`github.com/bendlang/bend`** (API description: "Bend 2: a fast language that blocks AI mistakes via proof"; pushed 2026-09-18T03:03Z; **20,546 stars**; Apache-2.0). MEASURED, GitHub API 2026-09-18.
- Old repo: `github.com/HigherOrderCo/Bend` (created 2023-08-29, 19,452→20,546 stars across reads) — Bend 1 lineage.
- Site: **https://bend-lang.com/** (install `curl -fsSL https://bend-lang.com/install.sh | sh`) and explainer **https://bend2.dev/notes/what-is-bend2/** (Last updated 2026-09-17). MEASURED.
- Papers: **BendTT** (affine dependent type theory, the core) and **BendRT** (parallel CPU/GPU runtime, the VM) — `paper/BendTT.pdf`, `paper/BendRT.pdf` (MEASURED, bend-lang.com references).
- Version public: **Bend 2.0.5**; runs `.bend` via Bun or compiles to JS, C, native (MEASURED, bend2.dev).

## 3. The headline numbers
- Post: "**up to 100x faster raw speeds**" vs Bend1 (MEASURED, post).
- bend-lang.com: "C speed · CUDA parallelism · Lean proofs · Python syntax"; "the same binary … on sixteen cores, or on the GPU, running **up to a hundred times faster than one core**" (MEASURED).
- bend-lang.com: "Bend's type checker is a proof checker … Those can take minutes … **Bend takes a second at most**" (MEASURED).
- bend2.dev benchmark file (`bench/runtime/_pin_/apple_m4_max.txt`, MEASURED, quoted upstream — NOT rerun here):
  - Game of Life: **7.803 s** 1 CPU thread → **0.647 s** parallel CPU → **0.063 s** GPU.
  - Lexer: **2.144 s** 1 CPU thread → **0.198 s** parallel CPU → **1.075 s** GPU.
  - ⇒ **GPU beats parallel CPU on Game of Life, but LOSES on the lexer** (1.075 vs 0.198). Directly on-point for "is the GPU always worth it?".
- bend2.dev checker file: **Bend 0.295 s vs Lean 36.177 s** on a 12,800-definition fixture; four Bend cases 0.295–0.834 s (MEASURED, upstream).
- Runtime caveats (MEASURED, bend2.dev): released runtime is **BendRT**, "compiles functions into a **flat C evaluator**", "**does not execute interaction nets**", scheduler "assigns tasks once, **without work stealing**; an uneven split can leave workers idle". GPU = Metal or CUDA, enabled with `--gpu`.

## 4. Town chain it touches
- **GPU-less compute** (primary): BendRT emits plain C; the parallel-CPU path is the one available on this box (arm-cloud, no Metal, no CUDA). The M4 benchmark is the first place the town has a **measured case where parallel CPU beats the GPU**.
- **Local inference / lighter hardware** (secondary): "fast like C, parallel like CUDA" targets everyday hardware; "100x on 16 cores" is a CPU claim, not a GPU-only claim.
- **Oscillators/metronome** (tertiary/weak): affine types + `a b = f(x) g(y)` parallel-call scheduling is a deterministic join model, adjacent to coupled-oscillator scheduling but not the same thing — note as a possible **scheduling primitive** for many tiny workers.
- Not a model/weights post: it is a **language + runtime**, so it touches the "smarter way to infer on lighter hardware" vision only via execution efficiency, not learning.

## 5. Hypothesis seeds (smallest experiment)
- **B1 (THIS box, 4-core arm-cloud, 23 GB, no GPU) — install Bend 2.0.5 and measure the CPU-parallel speedup.** Requires Bun + a C compiler (no GPU backend on ARM Linux ⇒ Metal/CUDA paths unavailable). Run the shipped `pow2` / Game-of-Life fixture at 1 thread vs 4 threads; report wall-clock and the CPU-only speedup. Est cost **$0.00**, **~20–30 min**. Falsifier: 4-core ARM speedup ≪ the "100x/16-core" headline, or install needs a GPU/Bun the box lacks.
- **B2 (THIS box) — proof-checker latency.** Run `bend PROOF.bend` on the bundled `app_win_is_bug_2d` demo; time it. Tests "checker under a second" on 4-core ARM. Est cost **$0.00**, **~10 min**.
- **B3 (local-town, ssh alias, gpu-8g + 15 GB RAM) — GPU vs parallel-CPU crossover.** Reproduce the Game-of-Life and lexer comparison to see whether the "GPU loses on lexer" result holds on a GPU2070S. Est cost **$0.00** (own box), **~30–45 min**. Camber XS (24 GB) NOT needed and NOT authorised here.
- Explicitly **not** proposed: renting Camber for this — 3 GPU-h/month is spend, and the interesting Bend result is the CPU path.

## 6. Open questions
- Is "100x" measured against 1 core or vs Bend 1? Post says "Bend1-like parallelism (with up to 100x faster raw speeds)"; site says "vs one core". Two different baselines — **do not merge them**.
- Windows/JS limitations, no LSP/debugger, "mismatches between the Lean formalization and `bend.ts`", "incomplete compiler audit" (MEASURED, bend2.dev) — trust boundary is the trusted proof kernel, not the compiler.
