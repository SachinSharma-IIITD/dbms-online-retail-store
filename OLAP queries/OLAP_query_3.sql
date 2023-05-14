use hawwkstore;

/* Find the total no of orders with each warehouse in each city and each state 
Therefore, analyse locations with more no of orders*/

select 
	IF(GROUPING(state) = 1, 'ALL STATES', state) AS state,
	IF(GROUPING(city) = 1, 'ALL CITIES', city) AS city,
    IF(GROUPING(`name`) = 1, 'ALL WAREHOUSES', `name`) AS `warehouse`,
	count(order_id) as no_of_active_orders
from warehouse
join map_delivery
on warehouse_id = id
group by state, city, `name` with rollup;