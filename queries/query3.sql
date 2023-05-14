use hawwkstore;

/* Get total number of orders of each customer */ 

select id, first_name, last_name, count(order_id) as total_active_orders
from customers
join map_active_orders
on id = customer_id
group by id
order by total_active_orders desc;
