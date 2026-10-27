select
    Case_ID,
    Activity as Activity_Name,
    Timestamp,
    row_number() over (partition by Case_ID order by Timestamp) as Event_Order,
    Condition,
    Age_Group,
    Ward
from {{ source('careflow_raw', 'event_log_raw') }}
where Case_ID is not null
  and Activity is not null
  and Timestamp is not null