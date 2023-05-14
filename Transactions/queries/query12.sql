use hawwkstore;

select * 
from product 
where product.cat_id in 
	(
    select id 
    from category 
    where name = 'grocery'
    );