use hawwkstore;

Start TRANSACTION;

Insert into delivery_man (warehouse_id, first_name, last_name, phone)
values (2, 'Honey', 'Kakkar', 9182730465);

COMMIT;