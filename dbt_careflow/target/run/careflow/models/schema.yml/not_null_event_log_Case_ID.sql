
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select Case_ID
from `careflow-ehr-04`.`careflow_clean`.`event_log`
where Case_ID is null



  
  
      
    ) dbt_internal_test