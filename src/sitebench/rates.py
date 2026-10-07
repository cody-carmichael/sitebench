import pandas as pd

# 100 full-time workers x 40 hours x 50 weeks: turns raw counts into "cases per 100 workers per year"
HOURS_BASE = 200_000


def add_injury_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with 'trir' and 'dart' columns added."""
    out = df.copy()  # don't modify the caller's DataFrame

    



    # TODO: add up the columns that count as recordable cases
    out["recordable_cases"] = (
    out["total_dafw_cases"]
    + out["total_djtr_cases"]
    + out["total_other_cases"]
    )

   
    # TODO: add up the columns that count as DART cases
    out["dart_cases"] = (
    out["total_dafw_cases"]
    + out["total_djtr_cases"]
    )


    # TODO: compute out["trir"] and out["dart"]
    out["trir"] = out["recordable_cases"] * 200000 / out["total_hours_worked"]
    out["dart"] = out["dart_cases"] * 200000 / out["total_hours_worked"]

    return out
