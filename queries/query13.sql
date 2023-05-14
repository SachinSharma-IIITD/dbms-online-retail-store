use hawwkstore;

/* Constraint: There cannot be 2 managers -> Query should give error */

insert into admin_team
values (12, 'manager');