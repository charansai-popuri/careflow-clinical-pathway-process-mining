\# CareFlow: ER Process Design



\## Goal

Simulate hospital Emergency Room event logs with built-in inefficiencies,

so process mining can discover them later.



\## Event log format

| Column | Meaning |

|---|---|

| Case\_ID | One patient visit |

| Activity | The step that happened |

| Timestamp | When it happened |



\## Normal patient flow

Registration -> Triage -> Doctor -> (X-Ray or Lab, if needed) -> Discharge



\## Planned inefficiencies (to be discovered later)

\- About 40% of patients sent for an X-Ray return to Triage afterwards

&#x20; (loop-back caused by missing paperwork).

\- Long waits at the Doctor step during busy hours.



\## Assumed step durations (minutes)

| Activity | Duration |

|---|---|

| Registration | 2 to 8 |

| Triage | 5 to 15 |

| Doctor consultation | 10 to 30 |

| X-Ray | 10 to 30 |

| Discharge | 3 to 10 |

## Next step

Write generate_events.py to produce this data.



