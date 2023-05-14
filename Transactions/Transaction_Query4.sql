use hawwkstore;

Start TRANSACTION;

Delete from category where name='stationary';

COMMIT;