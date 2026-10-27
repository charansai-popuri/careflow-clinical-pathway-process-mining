
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select Activity_Name
from `careflow-ehr-04`.`careflow_clean`.`event_log`
where Activity_Name is null



  
  
      
    ) dbt_internal_test