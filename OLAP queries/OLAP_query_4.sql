use hawwkstore;

/* Find the total no of products from each seller in each city and each state 
Therefore, analyse top sellers and top manufacturing locations */

select 
	IF(GROUPING(c.`name`) = 1, 'ALL CATEGORIES', c.`name`) AS category,
	IF(GROUPING(state) = 1, 'ALL STATES', state) AS state,
	IF(GROUPING(city) = 1, 'ALL CITIES', city) AS city,
    IF(GROUPING(s.`name`) = 1, 'ALL SELLERS', s.`name`) AS `seller`,
	count(product_id) as no_of_products_listed
from seller s
join map_sellers mp on seller_id = s.id
join product p on product_id = p.id
join category c on p.cat_id = c.id
group by c.`name`, state, city, s.`name` with rollup;