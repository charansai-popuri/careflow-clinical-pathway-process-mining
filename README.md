# CareFlow: Clinical Pathway Process Mining

Infotact Solutions internship project (Data Analytics, Group 11).

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

## Project structure
- `docs/` design documents (see `docs/process_design.md`)
- `data_generator/` event log generator
- `data/` generated event logs

## Status
- [x] ER process design
- [x] Event log generator v4 (conditions, age groups, tests, Doctor Review, loop-back, admission and wards, pharmacy, billing)
- [x] Busy-hour delays and slow evening pharmacy
- [x] Scale to 10,000 patients and validate the data
- [ ] BigQuery load
- [ ] dbt models
- [ ] PM4Py process discovery
- [ ] Power BI dashboard

## How to run
```
python data_generator/generate_events.py
python data_generator/validate_data.py
```