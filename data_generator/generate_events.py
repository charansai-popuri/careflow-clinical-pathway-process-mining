"""CareFlow event log generator (v3).

Generates mock ER event logs. Each patient has a Condition and an Age_Group
(case attributes). The path now depends on the condition:

Registration -> Triage -> Doctor Consultation
  -> X-Ray (chance depends on condition; 40% are sent back to Triage)
  -> Lab Test (chance depends on condition)
  -> Doctor Review (only if the patient had any test)
  -> Discharge

Admission, wards, pharmacy and billing come in later versions.
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
    "X-Ray": (10, 30),
    "Lab Test": (20, 60),
    "Doctor Review": (5, 15),
    "Discharge": (3, 10),
}

# Share of patients, and the chance of each test, per condition
# (from docs/process_design.md)
CONDITIONS = {
    "Fracture or injury": {"share": 15, "xray": 0.85, "lab": 0.10},
    "Chest pain":         {"share": 10, "xray": 0.30, "lab": 0.80},
    "Fever or infection": {"share": 25, "xray": 0.10, "lab": 0.70},
    "Stomach pain":       {"share": 15, "xray": 0.20, "lab": 0.60},
    "Minor illness":      {"share": 35, "xray": 0.05, "lab": 0.15},
}

# Share of patients in each age group (from docs/process_design.md)
AGE_GROUP_SHARES = {
    "Child": 20,
    "Adult": 55,
    "Senior": 25,
}

# Planted problem: this share of X-Ray patients is sent back to Triage
LOOP_BACK_CHANCE = 0.40


def pick(shares):
    """Pick one key from a {name: share} dictionary, using the shares as weights."""
    names = list(shares)
    weights = list(shares.values())
    return random.choices(names, weights=weights)[0]


def build_path(chances):
    """Decide the list of steps one patient goes through."""
    path = ["Registration", "Triage", "Doctor Consultation"]
    had_test = False

    if random.random() < chances["xray"]:
        path.append("X-Ray")
        had_test = True
        if random.random() < LOOP_BACK_CHANCE:
            path.append("Triage")  # the loop-back

    if random.random() < chances["lab"]:
        path.append("Lab Test")
        had_test = True

    if had_test:
        path.append("Doctor Review")

    path.append("Discharge")
    return path


def generate_patient(case_id, arrival):
    """Create all event rows for one patient."""
    condition = pick({name: info["share"] for name, info in CONDITIONS.items()})
    age_group = pick(AGE_GROUP_SHARES)
    path = build_path(CONDITIONS[condition])

    events = []
    current_time = arrival
    for activity in path:
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
    patient_count = 100

    for i in range(1, patient_count + 1):
        arrival = start + timedelta(minutes=random.randint(0, 3 * 24 * 60))
        all_events += generate_patient(f"P{i:03d}", arrival)

    all_events.sort(key=lambda e: (e["Case_ID"], e["Timestamp"]))

    os.makedirs("data", exist_ok=True)
    columns = ["Case_ID", "Activity", "Timestamp", "Condition", "Age_Group"]
    with open("data/event_log.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_events)

    print(f"Wrote {len(all_events)} events for {patient_count} patients")


if __name__ == "__main__":
    main()