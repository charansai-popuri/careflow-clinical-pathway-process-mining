# Weekly progress



## Week 1 (10 to 16 Oct)

- Set up Git and GitHub and created this repository.

- Wrote the ER process design (docs/process_design.md): event log format, five patient conditions with test and admission chances, age groups, ten activities, patient flow, step durations and planned inefficiencies.

- Built the Python EHR simulator (generate_events.py), growing from a normal-path version to conditions, age groups, X-Ray and lab tests, Doctor Review and a 40% X-Ray to Triage loop-back.

- Wrote the README. Committed on 10, 11, 12, 13, 14 and 15 Oct.



## Week 2 (17 to 23 Oct)

- Added admission and wards, pharmacy and billing, busy-hour doctor waits and a slower evening pharmacy.

- Scaled the generator to 10,000 patients (68,440 events over 30 days).

- Wrote validate_data.py (9 data quality checks) and check_waits.py (shows the planted waiting problems).

- Added requirements.txt and .gitignore, updated the README, and wrote the BigQuery table schema.

- Committed on 17, 18, 19, 20, 21 and 22 Oct.



## Week 3 so far (24 to 26 Oct)

- Wrote the BigQuery setup notes and loaded 68,440 rows into careflow_raw.event_log_raw (25 Oct).

- Built the PM4Py process discovery and process map (25 Oct). It finds the X-Ray to Triage loop-back in 965 of 2,377 X-Ray patients (40.6%).

- I wrote the BigQuery setup notes and loaded the 68,440-row event log into careflow_raw.event_log_raw. I built the PM4Py process discovery and process map, which finds the X-Ray to Triage loop-back in 965 of 2,377 X-Ray patients (40.6%). I created the dbt project with two models: event_log (standard format with Event_Order) and transition_times (average minutes between every pair of steps). I installed dbt-bigquery and the Google Cloud SDK, fixed a region error, and dbt run built both models and dbt test passed 8 tests. Triage to Doctor Consultation averages about 26.6 minutes for all 10,000 patients. I connected Power BI to BigQuery and built a dashboard with a bottleneck chart, KPI cards and a process map page. 



## Next

- dbt models to standardise the event log, then PM4Py reading the dbt output, then the Power BI dashboard.

