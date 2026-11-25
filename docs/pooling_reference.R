# Authored-but-not-executed R reference implementation.
# This environment has no R runtime; the real, executed methodology lives in
# src/pooling_optimization.py (a Python mirror of the same greedy allocation
# logic). This script documents how the same analysis would be expressed in R.

library(dplyr)

pooling_cost <- function(samples_df, cost_per_gb = 8.0) {
  samples_df %>%
    mutate(gb_needed = required_coverage / 10 * 3.0,
           cost = gb_needed * cost_per_gb) %>%
    summarise(total_cost = sum(cost))
}

naive_cost <- function(samples_df, cost_per_gb = 8.0) {
  equal_share <- mean(samples_df$available_yield_gb)
  samples_df %>%
    mutate(gb_needed_proxy = required_coverage / 10 * 3.0,
           allocated = pmax(equal_share, gb_needed_proxy),
           cost = allocated * cost_per_gb) %>%
    summarise(total_cost = sum(cost))
}

# run_batches <- samples_df %>% group_by(batch_id) %>%
#   summarise(naive = naive_cost(cur_data()), optimized = pooling_cost(cur_data()))
