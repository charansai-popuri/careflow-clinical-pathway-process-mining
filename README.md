# CareFlow: Clinical Pathway Process Mining

Infotact Solutions internship project (Data Analytics).

## Problem
Hospital administrators know Emergency Room waits are long, but not why.
An average wait time cannot show the real sequence of steps a patient goes
through, so hidden bottlenecks stay hidden. CareFlow uses process mining on
timestamped event logs to discover how patients actually move through the ER.

## Planned pipeline
Python event log generator -> Google BigQuery -> dbt -> PM4Py -> Power BI

| Stage | Tool | Purpose |
|---|---|---|
| Simulate data | Python | Create mock ER event logs with planted inefficiencies |
| Store | Google BigQuery | Warehouse for the event logs |
| Clean | dbt | Standardise to Case_ID, Activity, Timestamp |
| Discover | PM4Py | Find the real "As-Is" process map |
| Visualise | Power BI | Dashboard with process map and KPIs |

## Event log format
| Column | Meaning |
|---|---|
| Case_ID | One patient visit |
| Activity | The step that happened |
| Timestamp | When it happened |
| Condition | The patient's medical problem |
| Age_Group | Child, Adult or Senior |
| Ward | Ward name, filled only on the Ward Admission step |

## Planted inefficiencies
The simulated data contains three known problems, so process mining has
something real to discover:
1. About 40% of X-Ray patients are sent back to Triage (loop-back).
2. Long waits for the doctor during busy hours (10:00 to 14:00, 18:00 to 22:00).
3. A slower pharmacy in the evening (18:00 to 23:00).

## Data summary
The generator (seed 42) produces 10,000 patients and 68,440 events over 30 days
(about 333 patients a day), with 18 distinct patient paths.
Measured in the generated data:
- 40.6% of X-Ray patients return to Triage.
- Average time from the previous step to Doctor Consultation: 48.5 minutes in
  busy hours against 17.8 minutes at other times.
- Average time from the previous step to Pharmacy: 44.5 minutes in the evening
  against 18.2 minutes at other times.

## Project structure
- `docs/` design documents (see `docs/process_design.md`)
- `data_generator/generate_events.py` creates the event log
- `data_generator/validate_data.py` checks the data quality rules
- `data_generator/check_waits.py` shows the planted waiting problems
- `data/` generated event logs
- `requirements.txt` Python packages needed
- `bigquery/schema.json` BigQuery table definition for the raw event log
- `docs/bigquery_setup.md` BigQuery plan and load checks
- `process_mining/discover_process.py` discovers the process map with PM4Py
- `dbt_careflow/` dbt models: `event_log` (clean event log) and `transition_times` (average time between steps)
- `powerbi/careflow_dashboard.pbix` Power BI dashboard connected to the BigQuery dbt views
- `docs/dashboard.png` screenshot of the dashboard

## Status
- [x] ER process design
- [x] Event log generator v5 (conditions, age groups, tests, Doctor Review, loop-back, admission and wards, pharmacy, billing, busy-hour waiting)
- [x] Busy-hour delays and slow evening pharmacy
- [x] Scale to 10,000 patients and validate the data
- [x] BigQuery load
- [x] dbt models
- [x] PM4Py process discovery
- [x] Power BI dashboard (first version: bottleneck chart, KPI cards, process map)

## How to run
```
pip install -r requirements.txt
python data_generator/generate_events.py
python data_generator/validate_data.py
python data_generator/check_waits.py
python process_mining/discover_process.py

### dbt (BigQuery models)

1. Log in once: `gcloud auth application-default login`
2. Create `profiles.yml` in your home `.dbt` folder (outside the repo) with project `careflow-ehr-04`, your output dataset, and the same location as `careflow_raw`.
3. From the `dbt_careflow` folder run `dbt debug`, `dbt run` and `dbt test`.
```