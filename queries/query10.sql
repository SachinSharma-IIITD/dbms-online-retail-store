use hawwkstore;

/* Get average order value of each category */

create or replace view units_sold as
select product.id, sum(order_item.qty) as total_qty
from product 
join order_item on product.id = order_item.product_id
group by product_id;

create or replace view total_sales as
select product.id, cat_id, total_qty, total_qty * price as total_price
from product inner join units_sold;

select `name`, avg(total_price) as avg_order_value
from category
join total_sales on category.id = total_sales.cat_id
group by `name`
order by `name`;