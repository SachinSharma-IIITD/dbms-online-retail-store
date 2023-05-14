use hawwkstore;

/* Get a list of customers who have ordered in both the months December and January */

select c.id, first_name, last_name from customers as c 
where not exists 
	(
		select distinct month(date_of_order)
        from orders 
        where month(date_of_order) in (12, 1)
        and month(date_of_order) not in 
        (
			select distinct month(date_of_order) from map_prev_orders
				join orders on map_prev_orders.order_id = orders.id 
				where map_prev_orders.customer_id = c.id
		)
	)
order by id, first_name, last_name;