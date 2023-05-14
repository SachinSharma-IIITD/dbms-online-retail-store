use hawwkstore;

DELIMITER //
drop trigger if exists complete_order;
create TRIGGER complete_order
after update on active_orders
for each row
if new.status = 'delivered'
then
BEGIN
    delete from map_active_orders
    where order_id = new.id;

    delete from map_delivery
    where order_id = new.id;

    delete from offers
    where order_id = new.id;

    delete from verify_orders
    where order_id = new.id;
END;
end if//
