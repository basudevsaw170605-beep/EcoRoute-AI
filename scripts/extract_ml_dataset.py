"""Extract real dataset from Chicago Traffic Tracker SODA2 API for ML pipeline.

Extracts data for 7 dates: 2024-06-11 through 2024-06-17.
Uses simple chunked API requests (one chunk per date).
Excludes records where speed = -1.
Saves REAL data to data/processed/ecoroute_ml_dataset.csv
"""

import requests
import json
import os
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = "https://data.cityofchicago.org/resource/4g9f-3jbs.json"

# Columns to request (as specified)
COLUMNS = [
    "time", "segment_id", "speed", "street", "direction",
    "from_street", "to_street", "length", "bus_count",
    "message_count", "hour", "day_of_week", "month",
    "start_latitude", "start_longitude", "end_latitude", "end_longitude"
]

# Date ranges: 2024-06-11 through 2024-06-17
DATES = [
    "2024-06-11", "2024-06-12", "2024-06-13",
    "2024-06-15", "2024-06-16", "2024-06-17"
]

# chunk size - one request per date (no offset pagination for speed)
CHUNK_SIZE = 200


def build_where_clause(date_str):
    """Build $where clause for a given date."""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    next_d = (d + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    return f"time >= '{date_str}T00:00:00' AND time < '{next_d}'"


def fetch_chunk(params):
    """Fetch a chunk of records from the API."""
    try:
        r = requests.get(BASE_URL, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            return []
    except Exception as e:
        print(f"  API error: {str(e)[:80]}")
        return []


def extract_ml_dataset():
    """Main extraction function - one chunk per date."""
    all_records = []

    extraction_summary = {
        "dates_requested": DATES,
        "api_rows_retrieved": 0,
        "rows_removed_speed_minus_1": 0,
        "rows_removed_invalid_length": 0,
        "duplicates_removed": 0,
        "final_row_count": 0,
        "unique_segments": 0,
        "min_timestamp": None,
        "max_timestamp": None
    }

    for date_str in DATES:
        print(f"\nProcessing {date_str}...")
        where_clause = build_where_clause(date_str)

        # Single chunk request (no offset pagination for speed)
        params = {
            "$select": ",".join(COLUMNS),
            "$where": where_clause,
            "$limit": CHUNK_SIZE
        }

        records = fetch_chunk(params)
        api_rows = len(records)

        print(f"  API returned {api_rows} records")

        # Process records
        valid_records = []
        removed_speed = 0
        removed_length = 0

        for rec in records:
            # Check speed = -1
            speed_val = rec.get("speed", "")
            if speed_val == "-1" or speed_val == -1 or speed_val is None:
                removed_speed += 1
                continue

            # Check length validity
            length_val = rec.get("length", "")
            try:
                float(length_val)
            except (ValueError, TypeError):
                removed_length += 1
                continue

            # Convert to numeric
            try:
                rec["speed"] = float(speed_val)
                rec["length"] = float(length_val)
            except (ValueError, TypeError):
                removed_length += 1
                continue

            # Check for missing essential fields
            if not rec.get("segment_id") or not rec.get("time"):
                removed_speed += 1
                continue

            valid_records.append(rec)

        # Remove exact duplicate records
        seen = set()
        unique_records = []
        for rec in valid_records:
            key = (rec.get("segment_id"), rec.get("time"))
            if key not in seen:
                seen.add(key)
                unique_records.append(rec)
            else:
                extraction_summary["duplicates_removed"] += 1

        all_records.extend(unique_records)

        # Update summary
        extraction_summary["api_rows_retrieved"] += api_rows
        extraction_summary["rows_removed_speed_minus_1"] += removed_speed
        extraction_summary["rows_removed_invalid_length"] += removed_length
        print(f"  {date_str}: kept {len(unique_records)} of {api_rows} rows")

    # ---- Post-processing ----
    # Create DataFrame
    df = pd.DataFrame(all_records)

    # Update final stats
    extraction_summary["final_row_count"] = len(df)

    if len(df) > 0:
        # Unique segments
        extraction_summary["unique_segments"] = df["segment_id"].nunique()

        # Timestamps
        if "time" in df.columns and len(df) > 0:
            times = pd.to_datetime(df["time"])
            extraction_summary["min_timestamp"] = times.min()
            extraction_summary["max_timestamp"] = times.max()

    extraction_summary["unique_segments"] = df["segment_id"].nunique() if len(df) > 0 else 0

    # ---- Save outputs ----

    # Save CSV
    csv_path = os.path.join("data", "processed", "ecoroute_ml_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nSaved dataset to: {csv_path}")
    print(f"Final row count: {len(df)}")

    # Save summary JSON
    summary_path = os.path.join("data", "processed", "extraction_summary.json")
    with open(summary_path, "w") as f:
        json.dump(extraction_summary, f, indent=2)
    print(f"\nSaved extraction summary to: {summary_path}")

    # Print final summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    for k, v in extraction_summary.items():
        print(f"  {k}: {v}")

    return df, extraction_summary


if __name__ == "__main__":
    print("=" * 60)
    print("ECOURTE AI - ML DATASET EXTRACTION")
    print("=" * 60)
    print(f"Dates: {', '.join(DATES)}")
    print(f"Chunk size: {CHUNK_SIZE} records per API request")
    print(f"Columns: {', '.join(COLUMNS)}")
    print("=" * 60)

    df, summary = extract_ml_dataset()

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print("No ML models trained.")
    print("No synthetic data created.")
    print("Dataset source: Chicago Traffic Tracker SODA2 API (real data only)")