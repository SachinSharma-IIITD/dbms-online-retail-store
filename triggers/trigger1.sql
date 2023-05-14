use hawwkstore;

DELIMITER //
drop trigger if exists check_qty;
create trigger check_qty
before insert on cart
for each row
if not exists
(select product.qty from product
        where product.qty >= new.qty and product.id = new.product_id)
then
insert into cart
        values (new.customer_id, new.product_id, new.qty);
END if//