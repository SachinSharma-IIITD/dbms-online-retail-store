import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate
from backend_functions.admin_functions.order_funcs import view_order_items as admin_view_order_items

cursor: sql.connection.MySQLConnection.cursor
db: sql.connection.MySQLConnection


def set_cursor(c, d):
    global cursor
    global db
    cursor = c
    db = d


def rm_customer(id):
    query = (f"""
    delete from customers
    where id = {id};
    """)
    cursor.execute(query)
    db.commit()
    return


def view_all_customers():
    query = (f"""
    select *
    from customers;
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=["id", "first_name", "last_name", 'gender', "house no", "localiy", 'city', 'state']))
    print()
    return


def view_all_active_orders():
    query = (f"""
    select o.*, customer_id
    from orders o
    join map_active_orders m
    on order_id = o.id;
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=["id", "price", "date_of_order", "date_of_delivery", "mode_of_payment", "customer_id"]))
    print()
    return


def view_order_items(order_id):
    admin_view_order_items(order_id)
    return
