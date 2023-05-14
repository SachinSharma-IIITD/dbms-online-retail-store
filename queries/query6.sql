use hawwkstore;

select c.id, first_name, last_name, payment.order_id, 
price as order_value,
date_of_order as order_date,
date_of_delivery as delivery_date, 
date_of_payment as payment_date, 
mode_of_payment
from customers as c, payment
join map_prev_orders
on map_prev_orders.order_id = payment.order_id
join orders
on map_prev_orders.order_id = orders.id
where map_prev_orders.customer_id = c.id
group by c.id, order_id
order by c.id, payment_date desc;