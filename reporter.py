# reporter.py
# BUild the formatted tect report from all analysis results.
# pure string formatting 

from utils import bar_chart, fmt, rnd

def section(title, width=61):
    """Return a section headerline"""
    return[f"\n{title}", "-" * width]

def header_box(title, meta_dict, width=62):
    """Return a boxed header block"""
    lines = [
        "=" * width,
        title.center(width),
        "=" * width,
    ]
    for key, val in meta_dict.items():
        line = f" {key:<16}: {val}"
        lines.append(line)
    lines.append("=" * width)
    return lines

def fomat_overview(ov):
    """Format the dataset overview section"""
    lines = section("DATASET OVERVIEW")
    lines.append(f"Rows : {fmt(ov['rows'])}")
    lines.append(f"Columns : {ov['columns']}")
    lines.append(f"Total cells : {fmt(ov['total_cells'])}")
    lines.append(f"Total nulls : {fmt(ov['total_nulls'])}")
    flag = " [i]" if ov["null_pct"] > 5 else ""
    lines.append(f"Overall null pct : {ov['null_pct']}%{flag}")
    lines.append(f"\n column type breakdowm:")
    for dtype, count in sorted(ov["dtype_counts"].items()):
        lines.apppend(f"{dtype:<20}: {count}")
    if ov["pk_candidates"]:
        lines.append(f"\n primary key candidates : {ov['pk_candidates']}")
    if ov["constant_cols"]:
        lines.append(f"constant columns : {ov["constant_cols"]} [!]")
    return lines

def format_column(col_name, stats):
    ""