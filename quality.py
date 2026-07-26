# quality.py
# data quality checkks
# Each check returns (severity, coloumn_name, meesage)
# Secerities : "ERROR" | "WARN" | "INFO" | "OK"

from utils import is_null, is_num_str, to_float, pct, rnd, safe_div

def check_nulls(values, col):
    """Flag columns with too many missing values"""
    null_count = sum(1 for v in values if is_null(v))
    p          = pct(null_count, len(values))
    if p > 30:
        return ("ERROR", col, f"{p}% nulls - column is mostly empty")
    if p > 10:
        return ("WARN", col, f"{p}% nulls values present")
    if p > 0:
        return("INFO", col, f"{null_count} null values(s) ({p}%)")
    return ("OK", col, "No null values")

def check_duplicates(values, col):
    