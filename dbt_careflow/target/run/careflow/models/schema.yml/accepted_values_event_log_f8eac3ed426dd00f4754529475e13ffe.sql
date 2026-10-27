
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        Activity_Name as value_field,
        count(*) as n_records

    from `careflow-ehr-04`.`careflow_clean`.`event_log`
    group by Activity_Name

)

select *
from all_values
where value_field not in (
    'Registration','Triage','Doctor Consultation','X-Ray','Lab Test','Doctor Review','Ward Admission','Pharmacy','Billing','Discharge'
)



  
  
      
    ) dbt_internal_test