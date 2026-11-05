import pandas as pd

# Categories with fewer training sites than this get pooled into "Other",
# so no weight gets learned from a handful of sites
MIN_SITES = 15

CATEGORICAL = ["industry", "state", "establishment_type"]


def build_raw_features(df: pd.DataFrame) -> pd.DataFrame:
    """Pick and derive the model's input columns from the OSHA columns."""
    out = pd.DataFrame(index=df.index)
    # First 3 NAICS digits = subsector, specific enough to be a fair peer group
    out["industry"] = df["naics_code"].astype("string").str[:3].fillna("Other")
    out["state"] = df["state"].astype("string").fillna("Other")
    out["establishment_type"] = df["establishment_type"].astype("string").fillna("Other")
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

    def fit(self, df: pd.DataFrame) -> "SiteFeatures":
        raw = build_raw_features(df)
        self.kept_ = {}
        baseline_columns = []
        for col in CATEGORICAL:
            counts = raw[col].value_counts()
            self.kept_[col] = set(counts[counts >= MIN_SITES].index)
            # The most common category is the baseline; dropping its column avoids the dummy variable trap
            baseline_columns.append(f"{col}_{counts.index[0]}")
        full = self._one_hot(raw)
        self.columns_ = [c for c in full.columns if c not in baseline_columns]
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        full = self._one_hot(build_raw_features(df))
        # Lines up with training's columns: unseen categories drop out, missing ones become 0
        return full.reindex(columns=self.columns_, fill_value=0.0)

    def _one_hot(self, raw: pd.DataFrame) -> pd.DataFrame:
        raw = raw.copy()
        for col in CATEGORICAL:
            raw[col] = raw[col].where(raw[col].isin(self.kept_[col]), "Other")
        return pd.get_dummies(raw, columns=CATEGORICAL, dtype=float)
