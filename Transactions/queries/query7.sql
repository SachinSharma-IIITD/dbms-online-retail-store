use hawwkstore;

/* Get all details of customers having order value > 3000 */

select distinct id, first_name, last_name, gender from customers 
where id in 
	(select customer_id
    from map_active_orders 
    join orders as table1 
    where price > 3000 
    union 
		select customer_id 
		from map_prev_orders 
		join orders as table2 
		where price > 3000);
