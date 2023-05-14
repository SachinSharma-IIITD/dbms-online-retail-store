use hawwkstore;

/* Find average purchasing power (avg spent in each month/year) of every customer */

select 
	c.id, c.first_name, c.last_name, pp.*
from customers c
join 
	(select 
		id, year(dt) as `year`, monthname(dt) as `month`, 
		sum(price) as spent, 
		count(price) as no_of_orders, 
		sum(price) / count(price) as avg_purchasing_power
	from customers c, (
		select customer_id, price, date_of_order as dt from orders
		join map_prev_orders mp on id = mp.order_id
		) as o
	where c.id = o.customer_id
	group by id, `year`, `month` with rollup
	order by id, `year` desc, `month` desc
	) as pp
on c.id = pp.id;