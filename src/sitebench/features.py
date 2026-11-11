import pandas as pd

# Categories with fewer training sites than this get pooled into "Other",
# so no weight gets learned from a handful of sites
MIN_SITES = 15

# The three columns that get one-hot encoded
CATEGORICAL = ["industry", "state", "establishment_type"]


def build_raw_features(df: pd.DataFrame, naics_digits: int = 3) -> pd.DataFrame:
    """Pick and derive the model's input columns from the OSHA columns."""
    # Start an empty table with the same row labels as the input
    out = pd.DataFrame(index=df.index)
    # Keep the first few NAICS digits (3 = subsector); missing codes become "Other"
    out["industry"] = df["naics_code"].astype("string").str[:naics_digits].fillna("Other")
    # State as text; missing becomes "Other"
    out["state"] = df["state"].astype("string").fillna("Other")
    # Ownership code (private, state gov, local gov) as text; missing becomes "Other"
    out["establishment_type"] = df["establishment_type"].astype("string").fillna("Other")
    # Headcount passes through unchanged
    out["annual_average_employees"] = df["annual_average_employees"]
    # Separates part-time, full-time, and overtime-heavy sites, independent of headcount
    out["hours_per_employee"] = df["total_hours_worked"] / df["annual_average_employees"]
    return out


class SiteFeatures:
    """Turns site rows into the model's X matrix.

    fit() learns from training data which categories to keep, which category is each
    feature's baseline, and which columns X has. transform() applies exactly those
    decisions to any data: validation, test, or a new site sent to the API.
    """

    def __init__(self, naics_digits: int = 3):
        # How many NAICS digits define an industry; 3 by default, adjustable for experiments
        self.naics_digits = naics_digits

    def fit(self, df: pd.DataFrame) -> "SiteFeatures":
        # Build the raw feature columns from the training data
        raw = build_raw_features(df, self.naics_digits)
        # Will hold, for each category column, the set of values common enough to keep
        self.kept_ = {}
        # Will hold the one-hot column name for each feature's baseline category
        baseline_columns = []
        for col in CATEGORICAL:
            # Count how many training sites have each value, most common first
            counts = raw[col].value_counts()
            # Keep only values with at least MIN_SITES sites
            self.kept_[col] = set(counts[counts >= MIN_SITES].index)
            # The most common value is the baseline; dropping its column avoids the dummy variable trap
            baseline_columns.append(f"{col}_{counts.index[0]}")
        # One-hot encode everything, then record every column except the baselines
        full = self._one_hot(raw)
        self.columns_ = [c for c in full.columns if c not in baseline_columns]
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # Build and one-hot encode using the rules learned in fit()
        full = self._one_hot(build_raw_features(df, self.naics_digits))
        # Line up with training's columns: unseen categories drop out, missing ones become 0
        return full.reindex(columns=self.columns_, fill_value=0.0)

    def _one_hot(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Work on a copy so the caller's table isn't changed
        raw = raw.copy()
        for col in CATEGORICAL:
            # Any value not in the kept set gets replaced with "Other"
            raw[col] = raw[col].where(raw[col].isin(self.kept_[col]), "Other")
        # One column per category value, filled with 1.0 or 0.0
        return pd.get_dummies(raw, columns=CATEGORICAL, dtype=float)
