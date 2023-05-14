use hawwkstore;

/* Get a list of products in each category whose price is < 5000 and is in stock*/

select category.`name`, brand, product.`name`, price, qty as stock
from product
join category
on product.cat_id = category.id
where price < 5000
and qty > 0
order by category.`name`, brand, product.`name`;