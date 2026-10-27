
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select Event_Order
from `careflow-ehr-04`.`careflow_clean`.`event_log`
where Event_Order is null



  
  
      
    ) dbt_internal_test