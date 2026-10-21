"""Validate data/event_log.csv before it is loaded into BigQuery.

Prints PASS or FAIL for each rule. Exits with an error if any rule fails.
"""
import csv
import sys
from datetime import datetime

CSV_PATH = "data/event_log.csv"

REQUIRED = ["Case_ID", "Activity", "Timestamp", "Condition", "Age_Group"]

ALLOWED_ACTIVITIES = {
    "Registration", "Triage", "Doctor Consultation", "X-Ray", "Lab Test",
    "Doctor Review", "Ward Admission", "Pharmacy", "Billing", "Discharge",
}


def load_rows(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def group_by_case(rows):
    cases = {}
    for row in rows:
        cases.setdefault(row["Case_ID"], []).append(row)
    return cases


def check_no_missing(columns, rows):
    bad = 0
    for row in rows:
        for col in REQUIRED:
            if col not in columns or not (row.get(col) or "").strip():
                bad += 1
    return bad == 0, f"{bad} missing values"


def check_start_end(cases):
    bad = [cid for cid, evs in cases.items()
           if evs[0]["Activity"] != "Registration"
           or evs[-1]["Activity"] != "Discharge"]
    return not bad, f"{len(bad)} patients do not start with Registration and end with Discharge"


def check_time_order(cases):
    bad = 0
    for evs in cases.values():
        try:
            times = [datetime.fromisoformat(e["Timestamp"]) for e in evs]
        except ValueError:
            bad += 1
            continue
        if any(b < a for a, b in zip(times, times[1:])):
            bad += 1
    return bad == 0, f"{bad} patients have timestamps going backwards or unreadable"


def check_ward(columns, rows):
    if "Ward" not in columns:
        return True, "no Ward column yet (skipped)"
    bad = sum(1 for r in rows
              if (r["Ward"] or "").strip() and r["Activity"] != "Ward Admission")
    return bad == 0, f"{bad} rows have a Ward on a step other than Ward Admission"


def check_ward_present(rows):
    bad = sum(1 for r in rows
              if r["Activity"] == "Ward Admission" and not (r.get("Ward") or "").strip())
    return bad == 0, f"{bad} Ward Admission rows have no Ward"


def check_admission_billing(cases):
    bad = 0
    for evs in cases.values():
        activities = {e["Activity"] for e in evs}
        admitted = "Ward Admission" in activities
        has_pharmacy_or_billing = bool({"Pharmacy", "Billing"} & activities)
        # Admitted patients skip Pharmacy and Billing. Everyone else pays at Billing.
        if admitted and has_pharmacy_or_billing:
            bad += 1
        if not admitted and "Billing" not in activities:
            bad += 1
    return bad == 0, f"{bad} patients break the admission / billing rule"


def check_activity_names(rows):
    bad = {r["Activity"] for r in rows} - ALLOWED_ACTIVITIES
    return not bad, f"unknown activity names: {sorted(bad)}"


def check_case_attributes(cases):
    bad = 0
    for evs in cases.values():
        if len({e["Condition"] for e in evs}) > 1 or len({e["Age_Group"] for e in evs}) > 1:
            bad += 1
    return bad == 0, f"{bad} patients change Condition or Age_Group during the visit"


def check_duplicates(rows):
    seen = set()
    dupes = 0
    for r in rows:
        key = tuple(r.items())
        if key in seen:
            dupes += 1
        seen.add(key)
    return dupes == 0, f"{dupes} duplicate rows"


def main():
    try:
        columns, rows = load_rows(CSV_PATH)
    except FileNotFoundError:
        print(f"Cannot find {CSV_PATH}. Run the generator first.")
        sys.exit(1)

    cases = group_by_case(rows)
    print(f"Checking {len(rows)} events for {len(cases)} patients\n")

    checks = [
        ("No missing values", check_no_missing(columns, rows)),
        ("Starts with Registration, ends with Discharge", check_start_end(cases)),
        ("Timestamps never go backwards", check_time_order(cases)),
        ("Ward only on Ward Admission rows", check_ward(columns, rows)),
        ("Every Ward Admission row has a Ward", check_ward_present(rows)),
        ("Admitted patients skip Pharmacy and Billing", check_admission_billing(cases)),
        ("Activity names are valid", check_activity_names(rows)),
        ("Condition and Age_Group constant per patient", check_case_attributes(cases)),
        ("No duplicate rows", check_duplicates(rows)),
    ]

    failed = 0
    for name, (ok, detail) in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  -> {detail}"))
        failed += 0 if ok else 1

    print(f"\n{len(checks) - failed} of {len(checks)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()