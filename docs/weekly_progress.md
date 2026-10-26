\# Weekly progress



\## Week 1 (10 to 16 Oct)

\- Set up Git and GitHub and created this repository.

\- Wrote the ER process design (docs/process\_design.md): event log format, five patient conditions with test and admission chances, age groups, ten activities, patient flow, step durations and planned inefficiencies.

\- Built the Python EHR simulator (generate\_events.py), growing from a normal-path version to conditions, age groups, X-Ray and lab tests, Doctor Review and a 40% X-Ray to Triage loop-back.

\- Wrote the README. Committed on 10, 11, 12, 13, 14 and 15 Oct.



\## Week 2 (17 to 23 Oct)

\- Added admission and wards, pharmacy and billing, busy-hour doctor waits and a slower evening pharmacy.

\- Scaled the generator to 10,000 patients (68,440 events over 30 days).

\- Wrote validate\_data.py (9 data quality checks) and check\_waits.py (shows the planted waiting problems).

\- Added requirements.txt and .gitignore, updated the README, and wrote the BigQuery table schema.

\- Committed on 17, 18, 19, 20, 21 and 22 Oct.



\## Week 3 so far (24 to 26 Oct)

\- Wrote the BigQuery setup notes and loaded 68,440 rows into careflow\_raw.event\_log\_raw (25 Oct).

\- Built the PM4Py process discovery and process map (25 Oct). It finds the X-Ray to Triage loop-back in 965 of 2,377 X-Ray patients (40.6%).



\## Next

\- dbt models to standardise the event log, then PM4Py reading the dbt output, then the Power BI dashboard.

