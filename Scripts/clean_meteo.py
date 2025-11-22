#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
INPUT = BASE.parent / "CSVs" / "meteo.csv"
OUTPUT = BASE.parent / "CSVs" / "meteo_filtered.csv"
REPORT = BASE.parent / "CSVs" / "cleaning_report.txt"
DATETIME_COL = "datetime"
TOLERANCE_MINUTES = 30

SESSIONS = [
    ("2025-10-21","12:00","12:30"),
    ("2025-10-22","12:00","12:30"),
    ("2025-10-23","11:50","12:30"),
    ("2025-10-24","15:00","15:45"),
    ("2025-10-27","12:00","12:35"),
    ("2025-10-28","12:10","12:50"),
    ("2025-10-29","12:05","12:45"),
    ("2025-10-30","12:00","12:40"),
    ("2025-10-31","15:00","15:40"),
    ("2025-11-03","12:00","12:30"),
    ("2025-11-03","12:00","12:30"),
    ("2025-11-04","12:00","12:35"),
    ("2025-11-05","11:55","12:35"),
    ("2025-11-06","12:00","12:30"),
    ("2025-11-06","12:10","12:50"),
    ("2025-11-07","15:00","15:40"),
    ("2025-11-10","12:00","12:40"),
    ("2025-11-11","12:00","12:30"),
    ("2025-11-12","12:00","12:30"),
    ("2025-11-12","12:05","12:40"),
    ("2025-11-13","12:00","12:30"),
    ("2025-11-13","12:00","12:45"),
    ("2025-11-14","12:00","12:30"),
    ("2025-11-14","12:00","12:30"),
    ("2025-11-14","15:00","15:35"),
    ("2025-11-17","12:00","12:30"),
    ("2025-11-18","12:00","12:30"),
    ("2025-11-18","12:00","12:30"),
    ("2025-11-19","12:00","12:30"),
    ("2025-11-21","12:00","12:30"),
    ("2025-11-21","12:00","12:30"),
    ("2025-11-21","15:00","15:40"),
    ("2025-11-17","12:10","12:50"),
    ("2025-11-19","11:55","12:40"),
    ("2025-11-20","12:10","12:45"),
]

def round_to_hour(time_str):
    """Retourne HH:00"""
    return f"{int(time_str.split(':')[0]):02d}:00"

def to_timestamp(date_str, time_str):
    return pd.to_datetime(f"{date_str} {time_str}")

def main():
    df = pd.read_csv(INPUT)
    df[DATETIME_COL] = pd.to_datetime(df[DATETIME_COL], errors="coerce")
    ts = df[DATETIME_COL].dropna()
    tol = pd.Timedelta(minutes=TOLERANCE_MINUTES)
    kept_idx = set()
    report = []

    for i, (date, start, end) in enumerate(SESSIONS, 1):
        # arrondi simple à l'heure pile
        start_ts = to_timestamp(date, round_to_hour(start))
        end_ts = to_timestamp(date, round_to_hour(end))
        matched = ts[(ts >= start_ts) & (ts <= end_ts)]
        if not matched.empty:
            idxs = matched.index.tolist()
            kept_idx.update(idxs)
            report.append(f"Session {i}: exact matches {len(idxs)} rows (range {start_ts} to {end_ts})")
        else:
            midpoint = start_ts + (end_ts - start_ts) / 2
            diffs = (ts - midpoint).abs()
            nearest_idx = diffs.idxmin() if not diffs.empty else None
            if nearest_idx is not None and diffs.loc[nearest_idx] <= tol:
                kept_idx.add(nearest_idx)
                report.append(f"Session {i}: no exact match, included nearest row at {ts.loc[nearest_idx]} (diff {diffs.loc[nearest_idx]})")
            else:
                report.append(f"Session {i}: NO match within tolerance ({TOLERANCE_MINUTES}min) for {start_ts} - {end_ts}")

    filtered = df.loc[sorted(kept_idx)].copy()
    filtered.sort_values(DATETIME_COL, inplace=True)
    filtered.to_csv(OUTPUT, index=False)

    with open(REPORT, "w") as f:
        f.write("Cleaning report\n================\n")
        f.write(f"Input file: {INPUT}\nOutput file: {OUTPUT}\n")
        f.write(f"Total input rows: {len(df)}\nTotal kept rows: {len(filtered)}\n\n")
        f.write("\n".join(report))

    print(f"Done. Kept {len(filtered)} rows -> {OUTPUT}")
    print(f"Report -> {REPORT}")

if __name__ == "__main__":
    main()
