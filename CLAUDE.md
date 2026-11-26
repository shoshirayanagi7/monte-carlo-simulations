# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Learning project: Monte Carlo simulations that compare simulated estimates with exact theoretical results. Tick off tasks in `PROJECT_PLAN.md` when they are done.

## Rules

- Use snake_case (PEP 8).
- Keep the existing probability math (formulas, estimators, transition probabilities, payouts) unless the user asks to change it.
- Explain every change in plain language, including the probability or Python concept behind it, because the user is learning.
- Don't change the strategy logic in `interesting_problem_simulation.py`.
- Save plots with `plt.savefig("images/<name>.png")` and `plt.close()`, never `plt.show()`.

## Conventions

- Scripts are standalone and interactive; there are no tests and no shared module. Run them from the repo root (plots save to a relative `images/` path). To skip the prompts, pipe answers in: `printf '7\n10000\n' | python3 dice_simulation.py`.
- `dice_simulation.py` and `card_simulation.py` follow the reference layout: `main()` behind a `__main__` guard, plus `get_int_input()` for input validation that re-asks. The other scripts still run at import time; copy this pattern when updating them.
- `gamblers_ruin_simulation.py` reads module globals (`run_amount`, `money_start`, …) that are set by the input code at the bottom of the file.
- `gamblers_ruin_simulation.py` still uses `plt.show()`.
- In `card_simulation.py`, the exact calculation `theoretical_probability()` loops over all 1,712,304 possible boards and is too slow, so its call is commented out.
- In `gamblers_ruin_simulation.py`, the theoretical result `start / goal` is valid only for a fair coin.
