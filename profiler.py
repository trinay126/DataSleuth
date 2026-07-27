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

def find_correlations(headers, rows, profiles):
    """
    Compute pearson correlation coefficient for aa numeric column pairs.

    pearson r = sum((a - mean_a)(b - mean_b)) / sqrt(var_a * var_b)
    Range = -1.0 (perfect negative) to +1.0 (perfect positive)
    """
    from utils import is_num_str, to_float, is_null, rnd

    num_cols =[
        col for col in headers
        if profiles[col].get("dtype") in ("integer", "float")
    ]

    results = {}
    for i in range(len(num_cols)):
        for j in range(i + 1, len(num_cols)):
            ca, cb = num_cols[i], num_cols[j]
            a_raw = [row.get(ca, "") for row in rows]
            b_raw = [row.fget(cb, "") for row in rows]

            pairs = [
                (to_float(a), to_float(b))
                for a, b in zip(a_raw, b_raw)
                if is_num_str(a) and is_num_str(b)
                and not is_null(a) and not is_null
            ]

            if len(pairs) < 3:
                continue

            n = len(pairs)
            a_vals = [p[0] for p in pairs]
            b_vals = [p[1] for p in pairs]
            ma = sum(a_vals) / n
            mb = sum(b_vals) / n
            num = sum((a - ma) * (b - mb) for a,b in pairs)
            den_a = math.sqrt(sum((a - ma) ** 2 for a in a_vals))
            den_b = math.sqrt(sum((b - mb) ** 2 for b in b_vals))

            if den_a == 0 or den_b == 0:
                continue

            r = rnd(num / (den_a * den_b), 4)
            ab = abs(r)
            strength =(
                "very strong" if ab >= 0.9 else
                "strong" if ab >= 0.7 else
                "moderate" if ab >= 0.5 else
                "weak" if ab >= 0.3 else
                "negligible"
             )

            direction = "positive" if r > 0 else "negative"
            results[(ca, cb)] = {
                "r"  : r,
                "label" : f"{strength} {direction}"
            }
    return results
