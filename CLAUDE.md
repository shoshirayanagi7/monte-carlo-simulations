# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Learning project: Monte Carlo simulations that compare simulated estimates with exact theoretical results. Tick off tasks in `PROJECT_PLAN.md` when they are done.

## Rules

- Use snake_case (PEP 8).
- Keep the existing probability math (formulas, estimators, transition probabilities, payouts) unless the user asks to change it.
- Explain every change in plain language, including the probability or Python concept behind it, because the user is learning.
- Don't change the strategy logic in `interesting_problem_simulation.py`.
- Save plots with `plt.savefig("images/<name>.png")` and `plt.close()`. Call `plt.show()` only behind a y/n prompt (like `card_simulation.py`), so piped runs never open a window.

## Conventions

- Scripts are standalone and interactive; there are no tests and no shared module. Run them from the repo root (plots save to a relative `images/` path). To skip the prompts, pipe answers in: `printf '7\n10000\n' | python3 dice_simulation.py`.
- `dice_simulation.py` and `card_simulation.py` follow the reference layout: `main()` behind a `__main__` guard, plus `get_int_input()` for input validation that re-asks. The other scripts still run at import time; copy this pattern when updating them.
- `gamblers_ruin_simulation.py` reads module globals (`run_amount`, `money_start`, …) that are set by the input code at the bottom of the file.
- `gamblers_ruin_simulation.py` still uses `plt.show()`.
- `card_simulation.py` asks for an optional seed after the run count (Enter = random). Any optimization must keep the seeded benchmark in `benchmarks/card_simulation_benchmark.md` printing identical counts.
- In `card_simulation.py`, the exact calculation `theoretical_probability()` loops over all 1,712,304 possible boards (about 60 s), so it only runs if the user answers `y` to the "Calculate exact odds?" prompt. Piped input that ends before that prompt counts as `n`, so the benchmark command still works unchanged.
- In `card_simulation.py`, `monte_carlo()` returns four values: the three counts plus Hand 1's running win % after every run. `images/card_convergence.png` is always saved (even on the benchmark run); the window opens only on `y` to "Show the convergence plot?".
- In `gamblers_ruin_simulation.py`, the theoretical result `start / goal` is valid only for a fair coin.
