-- One row per patient: does the real path follow the ideal path?
-- The ideal path moves forward through the stages and never goes back
-- to an earlier stage or repeats a step (see docs/process_design.md).
with staged as (
    select
        Case_ID,
        Activity_Name,
        Event_Order,
        Condition,
        Age_Group,
        case Activity_Name
            when 'Registration' then 0
            when 'Triage' then 1
            when 'Doctor Consultation' then 2
            when 'X-Ray' then 3
            when 'Lab Test' then 3
            when 'Doctor Review' then 4
            when 'Ward Admission' then 5
            when 'Pharmacy' then 5
            when 'Billing' then 6
            when 'Discharge' then 7
        end as stage
    from {{ ref('event_log') }}
),

with_previous as (
    select
        *,
        lag(stage) over (partition by Case_ID order by Event_Order) as previous_stage
    from staged
)

select
    Case_ID,
    any_value(Condition) as Condition,
    any_value(Age_Group) as Age_Group,
    string_agg(Activity_Name, ' > ' order by Event_Order) as path,
    count(*) as steps,
    coalesce(logical_or(stage < previous_stage), false) as went_backwards,
    count(*) != count(distinct Activity_Name) as repeats_a_step,
    not (
        coalesce(logical_or(stage < previous_stage), false)
        or count(*) != count(distinct Activity_Name)
    ) as is_compliant
from with_previous
group by Case_ID