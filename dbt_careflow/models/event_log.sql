select
    Case_ID,
    Activity,
    Timestamp,
    Condition,
    Age_Group,
    Ward
from {{ source('careflow_raw', 'event_log_raw') }}
where Case_ID is not null
  and Activity is not null
  and Timestamp is not null