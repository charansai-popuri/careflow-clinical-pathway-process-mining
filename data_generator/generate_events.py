"""CareFlow event log generator (v2).

Generates mock ER event logs. Every patient now has a medical Condition and
an Age_Group (case attributes). The path is still the normal one:
Registration -> Triage -> Doctor Consultation -> Discharge.
Tests, loop-backs, wards, pharmacy and billing come in later versions.
"""
import csv
import os
import random
from datetime import datetime, timedelta

# How long each step takes, in minutes (low, high)
DURATIONS = {
    "Registration": (2, 8),
    "Triage": (5, 15),
    "Doctor Consultation": (10, 30),
    "Discharge": (3, 10),
}

NORMAL_PATH = ["Registration", "Triage", "Doctor Consultation", "Discharge"]

# Share of patients with each condition (from docs/process_design.md)
CONDITION_SHARES = {
    "Fracture or injury": 15,
    "Chest pain": 10,
    "Fever or infection": 25,
    "Stomach pain": 15,
    "Minor illness": 35,
}

# Share of patients in each age group (from docs/process_design.md)
AGE_GROUP_SHARES = {
    "Child": 20,
    "Adult": 55,
    "Senior": 25,
}


def pick(shares):
    """Pick one key from a {name: share} dictionary, using the shares as weights."""
    names = list(shares)
    weights = list(shares.values())
    return random.choices(names, weights=weights)[0]


def generate_patient(case_id, arrival):
    """Create all event rows for one patient."""
    condition = pick(CONDITION_SHARES)
    age_group = pick(AGE_GROUP_SHARES)

    events = []
    current_time = arrival
    for activity in NORMAL_PATH:
        events.append({
            "Case_ID": case_id,
            "Activity": activity,
            "Timestamp": current_time,
            "Condition": condition,
            "Age_Group": age_group,
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
    columns = ["Case_ID", "Activity", "Timestamp", "Condition", "Age_Group"]
    with open("data/event_log.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_events)

    print(f"Wrote {len(all_events)} events for 100 patients")


if __name__ == "__main__":
    main()