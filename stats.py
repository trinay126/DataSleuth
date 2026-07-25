#statistical calculations for DataSleuth
#Implements : type detection, mean, median, mode, std dev, IQR, Outliers

import math
from utils import is_null, is_num_str, to_float, safe_div, rnd, pct

def detect_type(values):
    """
    Infer the data type of a colums from its string values.

    Returns one of:
        'integer' - all non-null vlaues are whole numbers
        'float' - all non-null values are numbers with decimals
        'boolean' - all non-null values look like true/false/yes/no
        'text' - mixed or non-numeric values
        'empty' - no non-null values at all
    """
    non_null = [v for v in values if not is_null(v)]

    if not non_null:
        return "empty"

    bool_set = {"true", "false", 'yes', "no", '1',"0", "t", "f", "y", "n"}
    if all(v.strip().lower() in bool_set for v in non_null):
        return "boolean"

    numeric = [v for v in non_null if is_num_str(v)]
    if len(numeric) == len(non_null):
        has_decimal = any("." in v for v in non_null)
        return "float" if has_decimal else "integer"

    return "text"

def numeric_stats(numbers):
    """
    Compute descriptive statistics for a list of numbers.

    Uses:
        Mean = sum/count
        Median = middle value of sorted list
        Mode = most frequent value
        variance = average squared distance from mean
        Std Dev = Square root of variance
        IQR = Q3 - Q1 (inter - quartile range)
        Outliers = Values below Q1 - 1.5*IQR or above Q3+1.5IQR
    """
    if not numbers:
        return{}

    n = len(numbers)
    total = sum(numbers)
    mean = total / n
    sorted_n = sorted(numbers)
    mid = n // 2
    median = (sorted)