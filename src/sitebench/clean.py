import pandas as pd

# Nobody can work more than 24 x 365 hours in a year, so anything above this is a typo
MAX_HOURS_PER_EMPLOYEE = 24 * 365

# About 2 hours a week: keeps volunteer and seasonal sites, catches obvious typos
# like a staffed site reporting 2 total hours
MIN_HOURS_PER_EMPLOYEE = 100

# One worker can be hurt more than once, and turnover can push cases past the average
# headcount, but more than 2 cases per average employee is far likelier a typo than a real site
MAX_CASES_PER_EMPLOYEE = 2


def drop_implausible_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return only the rows whose hours, headcount, and case counts could be real.

    Expects the recordable_cases column from add_injury_rates, so the definition
    of a recordable case lives in one place.
    """
    hours = df["total_hours_worked"]
    employees = df["annual_average_employees"]

    # Zero employees makes this inf or NaN, and zero hours makes it 0,
    # so both fail the range check without needing their own rules
    hours_per_employee = hours / employees
    plausible_hours = hours_per_employee.between(MIN_HOURS_PER_EMPLOYEE, MAX_HOURS_PER_EMPLOYEE)

    plausible_cases = df["recordable_cases"] <= employees * MAX_CASES_PER_EMPLOYEE

    return df[plausible_hours & plausible_cases].copy()
