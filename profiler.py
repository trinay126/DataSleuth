# profiler.py
# Orchestrates all column level profiling
# calls reader, stats - no direct I/O or calcualtions here.

import math
from reader import get_col
from stats import detect_type, column_stats
from utils import safe_div, pct

def profile_dataset(headers, rows):
    """
    profile every column in the dataset

    Returns :
        dict{col_name: stats_dict}
    """
    profiles = {}
    for col in headers:
        values = get_col(rows, col)
        dtype = detect_type(values)
        stats = column_stats(values, dtype)
        stats["name"] = col
        profiles[col] = stats
    return profiles

def dataset_overview(headers, rows, profiles):
    """
    Return a hgih-level summary of the entire dataset
    """
    total_cells = len(headers) * len(rows)
    total_nulls = sum(p.get("null_count", 0) for p in profiles.values())
    null_pct = round(safe_div(total_nulls * 100, max(1, total_cells)), 2)

    dtpye_counts = {}
    for p in profiles.values():
        dt = p.get("dtype", "Unknown")
        dtpye_counts[dt] = dtpye_counts.get(dt, 0) + 1

    pk_cols =[
        col for col in headers
        if (profiles[col].get("null_count", 1) == 0 and profiles[col].get("unique", 0) == profiles[col].get("total", -1))
        ]

    constant_cols = [
        col for col in headers
        if profiles[col].get("Unique", 999) <= 1
    ]

    return{
        "rows"           : len(rows),
        "coloumns"       : len(headers),
        "total_cells"    : total_cells,
        "total_nulls"    : total_nulls,
        "null_pct"       : null_pct,
        "dtype_counts"   : dtpye_counts,
        "pk_candidates"  : pk_cols,
        "constant_cols"  : constant_cols,
    }