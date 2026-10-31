"""Discover the as-is process map from the event log with PM4Py.

Reads the event log, discovers the directly-follows graph (which step directly
follows which, and how often), prints the findings and saves a picture.

Two sources are supported:
  csv       reads data/event_log.csv                        (the default)
  bigquery  reads the dbt view careflow_clean.event_log     (the dbt output)

Run from the project folder:
  python process_mining/discover_process.py
  python process_mining/discover_process.py bigquery
"""
import sys

import matplotlib
matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pm4py

SOURCE = sys.argv[1] if len(sys.argv) > 1 else "csv"

CSV_PATH = "data/event_log.csv"
BIGQUERY_PROJECT = "careflow-ehr-04"
BIGQUERY_VIEW = "careflow-ehr-04.careflow_clean.event_log"
PICTURE_PATHS = {
    "csv": "docs/process_map.png",
    "bigquery": "docs/process_map_bigquery.png",
}

# Where each step is drawn: (column, row). Left to right follows the patient flow.
POSITIONS = {
    "Registration": (0, 0),
    "Triage": (1, 0),
    "Doctor Consultation": (2, 0),
    "X-Ray": (3, 1),
    "Lab Test": (3, -1),
    "Doctor Review": (4, 0),
    "Ward Admission": (5, 1),
    "Pharmacy": (5, -1),
    "Billing": (6, -1),
    "Discharge": (7, 0),
}


def load_from_csv():
    """Read the raw CSV file."""
    return pd.read_csv(CSV_PATH, parse_dates=["Timestamp"], keep_default_na=False)


def load_from_bigquery():
    """Read the clean dbt view straight from BigQuery (needs gcloud login)."""
    from google.cloud import bigquery

    client = bigquery.Client(project=BIGQUERY_PROJECT)
    query = f"""
        select Case_ID, Activity_Name as Activity, Timestamp
        from `{BIGQUERY_VIEW}`
        order by Case_ID, Event_Order
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)


if SOURCE not in PICTURE_PATHS:
    sys.exit("Unknown source. Use: csv or bigquery")

# 1. Load the event log and tell PM4Py which column is which
df = load_from_csv() if SOURCE == "csv" else load_from_bigquery()
print(f"Source: {SOURCE}" + (f" ({BIGQUERY_VIEW})" if SOURCE == "bigquery" else f" ({CSV_PATH})"))
log = pm4py.format_dataframe(
    df, case_id="Case_ID", activity_key="Activity", timestamp_key="Timestamp"
)

# 2. Discover the directly-follows graph
dfg, start_activities, end_activities = pm4py.discover_dfg(log)

# 3. Print what was discovered
cases = log["case:concept:name"].nunique()
print(f"Discovered from {cases} patients and {len(log)} events")
print(f"{len(dfg)} directed connections between {len(POSITIONS)} activities\n")

print("Ten most common connections:")
for (source, target), count in sorted(dfg.items(), key=lambda item: -item[1])[:10]:
    print(f"  {count:6d}  {source} -> {target}")

variants = pm4py.get_variants(log)
print(f"\n{len(variants)} distinct patient paths (variants). Most common:")
for path, count in sorted(variants.items(), key=lambda item: -item[1])[:3]:
    print(f"  {count:6d}  {' > '.join(path)}")

loop_back = dfg.get(("X-Ray", "Triage"), 0)
xray_exits = sum(c for (s, t), c in dfg.items() if s == "X-Ray")
print(f"\nLoop-back found: {loop_back} patients went from X-Ray back to Triage "
      f"({100 * loop_back / xray_exits:.1f}% of everyone who left the X-Ray)")

# 4. Draw the graph: thicker arrows mean more patients
graph = nx.DiGraph()
for (source, target), count in dfg.items():
    graph.add_edge(source, target, count=count)

top = max(dfg.values())
widths = [1 + 7 * graph[s][t]["count"] / top for s, t in graph.edges]
colors = ["#d62728" if (s, t) == ("X-Ray", "Triage") else "#4c72b0" for s, t in graph.edges]

fig, ax = plt.subplots(figsize=(16, 7))
nx.draw_networkx_nodes(graph, POSITIONS, node_size=3200, node_color="#f2f2f2",
                       edgecolors="#333333", ax=ax)
nx.draw_networkx_labels(graph, POSITIONS, labels={n: n.replace(" ", "\n") for n in graph.nodes},
                        font_size=8, ax=ax)
nx.draw_networkx_edges(graph, POSITIONS, width=widths, edge_color=colors, arrows=True,
                       arrowsize=18, node_size=3200,
                       connectionstyle="arc3,rad=0.12", ax=ax)
nx.draw_networkx_edge_labels(graph, POSITIONS,
                             edge_labels={(s, t): graph[s][t]["count"] for s, t in graph.edges},
                             font_size=7, label_pos=0.35, ax=ax)
ax.set_title("CareFlow: discovered patient flow (red arrow = X-Ray back to Triage loop-back)")
ax.axis("off")
fig.tight_layout()
fig.savefig(PICTURE_PATHS[SOURCE], dpi=130)
print(f"\nSaved the process map to {PICTURE_PATHS[SOURCE]}")