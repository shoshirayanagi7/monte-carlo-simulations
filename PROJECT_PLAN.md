# Monte Carlo Project Plan

## 1. Dice Sum Simulation
**Status:** In Progress / Mostly Complete

### Goals
- Simulate rolling two six-sided dice
- Let the user choose a target sum
- Let the user choose the number of simulations
- Estimate the probability of rolling that sum
- Calculate the exact theoretical probability
- Compare simulated and theoretical results

### Math / Stats Concepts
- Sample spaces
- Discrete probability
- Empirical probability
- Theoretical probability
- Monte Carlo convergence

### Tasks
- [x] Build dice rolling functions
- [x] Count target-sum matches
- [x] Add user input
- [x] Calculate estimated probability
- [x] Calculate theoretical probability
- [x] Add basic input validation
- [ ] Show difference/error between estimated and theoretical probability
- [ ] Test multiple simulation sizes
- [ ] Add convergence graph

---

## 2. Card Draw Simulation

### Goals
- Model a standard 52-card deck
- Simulate card draws
- Start with simple probabilities
- Extend to multiple draws without replacement
- Compare simulated and theoretical probabilities

### Math / Stats Concepts
- Conditional probability
- Dependent events
- Sampling without replacement
- Combinatorics
- Empirical vs theoretical probability

### Possible Questions
- Probability of drawing an Ace
- Probability of drawing a Heart
- Probability of drawing two Aces without replacement
- Probability of drawing two cards of the same suit

### Tasks
- [ ] Represent a deck of 52 cards
- [ ] Simulate one-card draws
- [ ] Simulate multiple draws without replacement
- [ ] Calculate theoretical probability
- [ ] Compare simulated and theoretical results
- [ ] Add visualization

---

## 3. Binomial Coin Simulation

### Goals
- Simulate repeated groups of coin flips
- Count the number of heads in each experiment
- Compare the simulated distribution with the theoretical binomial distribution

### Math / Stats Concepts
- Binomial distribution
- Combinations
- Expected value
- Variance
- Standard deviation
- Probability distributions

### Example Experiment
Flip a fair coin 20 times and record the number of heads.

Repeat this experiment thousands of times.

### Tasks
- [ ] Build basic coin flip function
- [ ] Simulate groups of multiple flips
- [ ] Record number of heads per experiment
- [ ] Learn and implement the binomial probability formula
- [ ] Calculate theoretical expected value
- [ ] Calculate theoretical variance
- [ ] Calculate standard deviation
- [ ] Compare theoretical and simulated statistics
- [ ] Add histogram of outcomes

---

## 4. Random Walk / Gambler's Ruin

### Goals
- Simulate a value changing over time based on random outcomes
- Study how expected value affects the process
- Estimate probabilities of reaching different boundaries
- Measure how long the process lasts

### Example Setup
Start with $10.

- Heads: +$1
- Tails: -$1
- Stop at $0 or $20

### Math / Stats Concepts
- Expected value
- Variance
- Random walks
- Stochastic processes
- Hitting probabilities
- Stopping times

### Extensions
- Change starting balance
- Change upper boundary
- Use a biased coin
- Compare positive, negative, and zero expected value

### Tasks
- [ ] Build one random walk
- [ ] Add upper and lower stopping boundaries
- [ ] Run thousands of complete walks
- [ ] Estimate probability of reaching each boundary
- [ ] Calculate average stopping time
- [ ] Calculate average profit/loss
- [ ] Compare fair and biased walks
- [ ] Plot several example paths
- [ ] Plot stopping-time distribution

---

## 5. Coin Streak Simulation + Markov Chain

### Goals
- Simulate the number of flips needed to reach a streak such as HH
- Solve the same problem mathematically with a Markov chain
- Compare the theoretical result with Monte Carlo

### Math / Stats Concepts
- Conditional probability
- Conditional expectation
- States
- Transition probabilities
- Markov chains
- Absorbing states
- Expected stopping time

### Tasks
- [ ] Build coin-streak Monte Carlo simulation
- [ ] Estimate average flips needed for HH
- [ ] Learn Markov chain states
- [ ] Draw the state diagram
- [ ] Build the transition matrix
- [ ] Derive expected-value equations
- [ ] Solve for the theoretical expected number of flips
- [ ] Compare theoretical and simulated results
- [ ] Extend from HH to HHH or another pattern

---

## 6. Financial Monte Carlo Simulation

### Goals
- Apply concepts from the earlier simulations to finance
- Model many possible future outcomes
- Analyze the resulting distribution and risk

### Math / Stats Concepts
- Expected return
- Probability distributions
- Variance
- Standard deviation
- Volatility
- Random processes
- Percentiles
- Risk analysis

### Tasks
- [ ] Learn the required financial model
- [ ] Choose what to simulate
- [ ] Define model assumptions
- [ ] Generate many simulated outcomes
- [ ] Calculate mean outcome
- [ ] Calculate variance and standard deviation
- [ ] Calculate percentile-based risk measures
- [ ] Graph simulated paths
- [ ] Graph final outcome distribution
- [ ] Explain model assumptions and limitations

---

# Project-Wide Improvements

## Visualizations
- [ ] Add Matplotlib
- [ ] Create consistent graph formatting
- [ ] Show simulated vs theoretical results
- [ ] Show convergence as simulation count increases
- [ ] Show probability distributions

## Code Quality
- [ ] Use consistent Python naming conventions
- [ ] Add comments where useful
- [ ] Organize simulations into separate files
- [ ] Add input validation
- [ ] Reduce repeated code where possible
- [ ] Test edge cases

## GitHub / Documentation
- [ ] Finish README
- [ ] Keep PROJECT_PLAN updated
- [ ] Commit after meaningful milestones
- [ ] Add explanation of math behind each simulation
- [ ] Add example outputs and graphs to README
- [ ] Write final project summary