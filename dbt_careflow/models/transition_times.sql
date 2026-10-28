-- One row for every pair of steps that happen one after the other.
-- It shows how many patients made that move and how long it took on average.
with ordered as (
    select
        Case_ID,
        Activity_Name as from_activity,
        lead(Activity_Name) over (partition by Case_ID order by Event_Order) as to_activity,
        Timestamp as from_time,
        lead(Timestamp) over (partition by Case_ID order by Event_Order) as to_time
    from {{ ref('event_log') }}
)

select
    from_activity,
    to_activity,
    count(*) as patients,
    round(avg(timestamp_diff(to_time, from_time, second)) / 60, 1) as avg_minutes,
    round(max(timestamp_diff(to_time, from_time, second)) / 60, 1) as max_minutes
from ordered
where to_activity is not null
group by from_activity, to_activity