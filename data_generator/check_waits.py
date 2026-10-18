"""Check that the planted waiting problems are visible in the event log."""
import pandas as pd

BUSY_HOURS = [10, 11, 12, 13, 18, 19, 20, 21]
EVENING_HOURS = [18, 19, 20, 21, 22]

df = pd.read_csv("data/event_log.csv", parse_dates=["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

# Minutes between a step and the step before it, for the same patient
previous = df.groupby("Case_ID")["Timestamp"].shift(1)
df["Minutes_Since_Previous"] = (df["Timestamp"] - previous).dt.total_seconds() / 60


def report(activity, hours, label):
    rows = df[df["Activity"] == activity]
    inside = rows["Timestamp"].dt.hour.isin(hours)
    print(label)
    print("  inside those hours :", round(rows[inside]["Minutes_Since_Previous"].mean(), 1),
          "min on average,", inside.sum(), "patients")
    print("  outside those hours:", round(rows[~inside]["Minutes_Since_Previous"].mean(), 1),
          "min on average,", (~inside).sum(), "patients")


report("Doctor Consultation", BUSY_HOURS, "Minutes from previous step to Doctor Consultation")
report("Pharmacy", EVENING_HOURS, "Minutes from previous step to Pharmacy")