# SiteBench (SafeSite Benchmark)

## Problem statement

Safety managers and underwriters need a tool to determine if a particular location is high risk. SiteBench lets them provide a list of locations and see each one's injury rate compared to a benchmark built from established OSHA data. The tool compares the type of location, the number of workers, and the injury rate against similar sites in the OSHA data. For each location, it returns the injury rate compared to the expected rate for similar sites, the peer group it belongs to described in plain English, and a risk level (low, medium, or high) with the rules behind it. This supports safety managers' decisions to audit locations or allocate additional spending, and underwriters' decisions to adjust pricing based on the level of risk. Users can trust the results because every risk level comes with readable reasons, accuracy is measured on sites the model never saw while learning, and the tool states which OSHA data it uses and its known limits.

## Glossary
Definitions in my own words, added as terms come up.

- **Metric:**
- **Benchmark:**
- **Rate:**
- **Clustering:**
- **Interpretable:**

## Data cleaning
Rule 1, keep sites with 100 to 8,760 hours per employee:
Why:

Rule 2, drop sites with more than 2x as many recordable cases as average employees:
Why:

## Glossary additions
- **Feature:**
- **Target:**
- **Data dictionary:**
- **TRIR:**
- **DART:**
- **Outlier:**
- **Training / validation / test set:**
- **Data leakage:**

## Phase 3 results: decision tree (validation set)
Risk levels from training percentiles: low < 1.67, medium 1.67 to 11.28, high >= 11.28 (top 10%).
Scores below are for the high-risk class. Base rate: 10% of sites are high risk.

| Model | Leaves | Sites flagged high | High recall | High precision | F1 | F2 |
|---|---|---|---|---|---|---|
| Depth 5, default rule | 32 | 0.5% | 4.3% | 85.5% | 0.08 | 0.05 |
| Depth 5, class_weight balanced | n/a | 19.3% | 40.0% | 20.9% | 0.27 | 0.34 |
| Depth 5, high if P(high) >= 0.15 | 32 | 14.6% | 29.8% | 20.6% | 0.24 | 0.27 |
| Depth 5 + pruning (alpha 0.0005), high if P(high) >= 0.15 | 17 | about 17% | 33.3% | 19.7% | 0.25 | 0.29 |

Profile-only features limit how well any model can separate high-risk sites; a flag is a screening signal, not a verdict.
