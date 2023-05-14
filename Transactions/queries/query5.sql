use hawwkstore;

/* Get the top 10 products with the highest number of units sold */

select brand, `name`, sum(order_item.qty) as units_sold, sum(order_item.qty)*price as overall_total_sales
from product
join order_item
on id = product_id
group by brand, `name`, price
order by overall_total_sales desc
limit 10;

