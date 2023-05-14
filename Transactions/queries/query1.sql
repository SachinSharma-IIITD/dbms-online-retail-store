use hawwkstore;

/* Get number of warehouses in each state starting with letter C */

select state, city, count(warehouse.id) as count_warehouses
from warehouse
where state like 'C%'
group by state, city
order by count_warehouses desc;