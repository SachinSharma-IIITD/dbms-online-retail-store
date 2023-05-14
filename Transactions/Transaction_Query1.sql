use hawwkstore;

Start TRANSACTION;

UPDATE product p
set p.qty = 150
where p.qty < 10
and p.id in
(Select m.product_id from map_sellers m
where p.id = m.product_id and m.seller_id in
(Select seller.id from seller
where m.seller_id = seller.id
)
);
COMMIT;