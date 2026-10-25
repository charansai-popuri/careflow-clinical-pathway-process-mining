"""Discover the as-is process map from the event log with PM4Py.

Reads data/event_log.csv, discovers the directly-follows graph (which step
directly follows which, and how often), prints the findings and saves a picture
to docs/process_map.png.

Run from the project folder:  python process_mining/discover_process.py
"""
import matplotlib
matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pm4py

CSV_PATH = "data/event_log.csv"
PICTURE_PATH = "docs/process_map.png"

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

# 1. Load the event log and tell PM4Py which column is which
df = pd.read_csv(CSV_PATH, parse_dates=["Timestamp"], keep_default_na=False)
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
fig.savefig(PICTURE_PATH, dpi=130)
print(f"\nSaved the process map to {PICTURE_PATH}")