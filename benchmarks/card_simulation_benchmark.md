# card_simulation.py benchmark

## Test
- Hand 1: ACE SPADES + KING SPADES
- Hand 2: TWO HEARTS + TWO CLUBS
- 10,000 runs, seed 42

```
printf 'ACE\nSPADES\nKING\nSPADES\nTWO\nHEARTS\nTWO\nCLUBS\n10000\n42\n' | python3 card_simulation.py
```

## Results (counts must stay identical after any optimization)

| version | Hand 1 wins | Hand 2 wins | Ties | time (median of 3) |
|---|---|---|---|---|
| baseline | 5074 | 4879 | 47 | 1.05 s (1.03, 1.05, 1.10) |
| easy optimizations | 5074 | 4879 | 47 | 0.65 s (0.65, 0.65, 0.65) |

About 1.6x faster (38% less time).

Easy optimizations:
- the deck is built once per simulation, not once per run
- the duplicate `rank_values` dict in `hand_classification` was removed
- `is_flush` and `is_straight` are called once per hand
- the sorted rank values are built only for the royal-flush check

## cProfile (`python3 -m cProfile -s tottime`, monte_carlo only)

Profiling adds overhead, so these totals are higher than the times above.

Baseline: 14.07 M function calls, 2.58 s

| function | calls | own time | incl. subcalls |
|---|---|---|---|
| hand_classification | 420,000 | 0.64 s | 1.96 s |
| is_straight | 836,760 | 0.63 s | 0.95 s |
| list.append | 8,106,482 | 0.40 s | |
| get_rank_counts | 574,055 | 0.17 s | |
| get_tiebreak_value | 154,055 | 0.13 s | 0.21 s |
| create_deck | 10,000 | 0.04 s | 0.07 s |

After the easy optimizations: 7.64 M function calls, 1.54 s

| function | calls | own time | incl. subcalls |
|---|---|---|---|
| is_straight | 420,000 | 0.34 s | 0.50 s |
| hand_classification | 420,000 | 0.29 s | 1.03 s |
| list.append | 3,402,769 | 0.17 s | |
| get_rank_counts | 574,055 | 0.16 s | |
| get_tiebreak_value | 154,055 | 0.12 s | 0.21 s |
| create_deck | 1 | ~0 | ~0 |
