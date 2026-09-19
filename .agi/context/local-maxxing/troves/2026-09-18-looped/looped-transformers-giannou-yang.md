# looped-transformers-giannou-yang — theory of looped transformers — reading digest
READ-ONLY. MEASURED = quoted from a page read today; ESTIMATE = inferred, arithmetic shown.

## A. Looped Transformers as Programmable Computers — arXiv 2301.13196
URL: https://arxiv.org/abs/2301.13196 ; PMLR v202 (ICML 2023)
- TITLE (MEASURED): "Looped Transformers as Programmable Computers".
- AUTHORS (MEASURED): Angeliki Giannou, Shashank Rajput, Jy-Yong Sohn, Kangwook Lee, Jason D. Lee,
  Dimitris Papailiopoulos. DATE (MEASURED): submitted 2023-01-30.
- MECHANISM (2 lines, MEASURED): transformer networks used as universal computers by programming
  specific weights and placing them in a loop; the input sequence is a "punchcard" of instructions +
  memory. A constant number of encoder layers emulate lexicographic ops, non-linear functions,
  function calls, program counters and conditional branches, building a small instruction-set
  computer.
- UNIQUE PARAMS vs EFFECTIVE DEPTH (MEASURED): a looped, 13-LAYER transformer (constant layer count)
  executes iterative algorithms; effective depth = layers x loop iterations. So the parameter count
  is fixed by the 13 layers; the loop count sets the computation depth.
- RELEASED WEIGHTS (MEASURED): none — constructive/theoretical, no trained model released.
- CPU RUNNABILITY: n/a (no weights). Constructive proof, not an inference artifact.
- QUALITY vs NON-LOOPED: theoretical emulation result; it shows shallow looped transformers can
  execute general-purpose programs, not a benchmark accuracy comparison.
- TRAINING COST: n/a (weights are constructed, not trained).

## B. Looped Transformers are Better at Learning Learning Algorithms — arXiv 2311.12424
URL: https://arxiv.org/abs/2311.12424
- TITLE (MEASURED): "Looped Transformers are Better at Learning Learning Algorithms".
- AUTHORS (MEASURED): Liu Yang, Kangwook Lee, Robert Nowak, Dimitris Papailiopoulos.
  DATE (MEASURED): submitted 2023-11-21. (This is the "Yang 2024 reasoning" reference.)
- MECHANISM (2 lines, MEASURED): add an iterative structure to the transformer by LOOPING the
  architecture with a dedicated training methodology, so the model can emulate the iterative
  algorithms (gradient descent, etc.) used to solve in-context data-fitting problems.
- UNIQUE PARAMS vs EFFECTIVE DEPTH (MEASURED): looped block re-applied; unique params ~ one block,
  effective depth = loop count. Exact counts experiment-dependent.
- RELEASED WEIGHTS (MEASURED): none found; paper + training methodology only. (GAP)
- CPU RUNNABILITY: n/a (no released weights).
- QUALITY vs NON-LOOPED (MEASURED abstract): "the looped transformer achieves performance comparable
  to the standard transformer in solving various data-fitting problems, while utilizing **less than
  10% of the parameter count**." This is the cleanest theory-line statement that looping buys
  parameter efficiency at matched quality.
- TRAINING COST: not extracted (gap); small in-context regression tasks.

## WHY IT MATTERS HERE
- These two papers are the theoretical spine: (i) a constant-depth looped transformer is
  computationally universal (Giannou), and (ii) looping matches a standard transformer with <10% of
  the parameters on algorithmic tasks (Yang). They justify the town's hypothesis that DEPTH
  recurrence buys capability per parameter — but they are NOT runnable models and must not be cited
  as benchmark evidence. The runnable evidence is Huginn (2502.05171) and Ouro (2510.25741).
