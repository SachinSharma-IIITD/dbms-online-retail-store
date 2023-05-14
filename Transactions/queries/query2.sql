use hawwkstore;

/* Find the categories whose atleast 1 product is present in atleast 1 cart */

Select distinct name, id 
from category 
where id in  
	( Select product.cat_id 
    from product 
    join cart on cart.product_id = product.id
    )
order by name;