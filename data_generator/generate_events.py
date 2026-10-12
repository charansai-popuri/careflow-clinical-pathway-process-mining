"""CareFlow event log generator (v1).

Generates mock ER event logs for patients who follow the normal path:
Registration -> Triage -> Doctor -> Discharge.
Loop-backs, conditions, tests and wards are added in later versions.
"""
import csv
import os
import random
from datetime import datetime, timedelta

# How long each step takes, in minutes (low, high)
DURATIONS = {
    "Registration": (2, 8),
    "Triage": (5, 15),
    "Doctor": (10, 30),
    "Discharge": (3, 10),
}

NORMAL_PATH = ["Registration", "Triage", "Doctor", "Discharge"]


def generate_patient(case_id, arrival):
    """Create all event rows for one patient."""
    events = []
    current_time = arrival
    for activity in NORMAL_PATH:
        events.append({
            "Case_ID": case_id,
            "Activity": activity,
            "Timestamp": current_time,
        })
        low, high = DURATIONS[activity]
        current_time += timedelta(minutes=random.randint(low, high))
    return events


def main():
    random.seed(42)  # same random numbers every run, so results repeat
    start = datetime(2026, 10, 1, 8, 0)
    all_events = []

    for i in range(1, 101):  # 100 patients
        arrival = start + timedelta(minutes=random.randint(0, 3 * 24 * 60))
        all_events += generate_patient(f"P{i:03d}", arrival)

    all_events.sort(key=lambda e: (e["Case_ID"], e["Timestamp"]))

    os.makedirs("data", exist_ok=True)
    with open("data/event_log.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Case_ID", "Activity", "Timestamp"])
        writer.writeheader()
        writer.writerows(all_events)

    print(f"Wrote {len(all_events)} events for 100 patients")


if __name__ == "__main__":
    main()