
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select Timestamp
from `careflow-ehr-04`.`careflow_clean`.`event_log`
where Timestamp is null



  
  
      
    ) dbt_internal_test