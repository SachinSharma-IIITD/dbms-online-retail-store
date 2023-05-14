use hawwkstore;

/* Get the top 50 products with the highest number of units sold
Therefore, analyse the top 50 selling products */

select 
	IF(GROUPING(c.`name`) = 1, 'ALL CATEGORIES', c.`name`) AS `category`,
	IF(GROUPING(brand) = 1, 'ALL BRANDS', brand) AS brand,
	IF(GROUPING(sold.`name`) = 1, 'ALL PRODUCTS', sold.`name`) AS `product`,
    sum(quantity) as units_sold 
from category c join    
	(
	SELECT 
		cat_id, brand, `name`, order_item.qty as quantity
	FROM product
	JOIN order_item ON id = product_id
	order by order_item.qty desc
	limit 50
) as sold
on c.id = cat_id
group by c.`name`, brand, sold.`name` with rollup;