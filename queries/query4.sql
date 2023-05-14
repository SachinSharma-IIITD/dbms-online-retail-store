use hawwkstore;

/* Get maximum discount available on each order */

select order_id, max(discount) as max_discount 
from offers 
right join orders on order_id = id
group by order_id
order by max_discount desc;