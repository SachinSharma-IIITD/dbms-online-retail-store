use hawwkstore;

/* Get a list of customers who have ordered in both the months January and May */

select id, first_name, last_name from customers as c 
where not exists 
	(
		select date_of_order from orders where month(date_of_order) in (1, 5)
		and exists ( 
		select date_of_order from map_prev_orders 
			join orders on map_prev_orders.order_id = orders.id 
			where map_prev_orders.customer_id = c.id
		)
	)
order by id, first_name, last_name;