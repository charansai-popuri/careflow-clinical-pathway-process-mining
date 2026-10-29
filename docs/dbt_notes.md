# dbt notes

## Setup
- Output dataset (the dataset line of profiles.yml): careflow_clean
- Location (same as careflow_raw): asia-south1
- Login method: oauth (gcloud auth application-default login)

## Models
- event_log: standard event log with Activity_Name and Event_Order
- transition_times: average time between every pair of steps

## Results
- dbt run built 2 models
- dbt test passed 8 tests

## Lesson
The first dbt run failed because the profile location did not match the raw dataset's region. dbt must use the same region as the dataset it reads.