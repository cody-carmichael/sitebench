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
