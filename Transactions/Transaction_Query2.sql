use hawwkstore;

/* Update the phone number of customer with given name and phone number */

Start TRANSACTION;
update customer_phone
set phone = '8542687456'
where phone = '6177222794'
and id in 
	(select id 
    from customers 
    where first_name = 'Aleda' and last_name = 'Le Grys')
    ;
    
select customers.id, phone from customer_phone
join customers
on customer_phone.id = customers.id
where first_name = 'Aleda' and last_name = 'Le Grys';
COMMIT;