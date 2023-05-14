import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate

cursor: sql.connection.MySQLConnection.cursor
db: sql.connection.MySQLConnection


def set_cursor(c, d):
    global cursor
    global db
    cursor = c
    db = d


def new_warehouse(name, phone, plot, locality, city, state):
    query = (f"""
    insert into warehouse
    (name, phone, plot_no, locality, city, state)
    values
    ('{name}', '{phone}', '{plot}', '{locality}', '{city}', '{state}')
    """)
    cursor.execute(query)
    db.commit()
    return


def rm_warehouse(id):
    query = (f"""
    delete from warehouse
    where id = {id}
    """)
    cursor.execute(query)
    db.commit()
    return


def view_all_warehouses():
    query = (f"""
    select *
    from warehouse
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=["id", "name", "phone", "plot", "locality", "city", "state"]))
    print()
    return


def view_delivery_men(warehouse_id):
    query = (f"""
    select *
    from delivery_man
    where warehouse_id = {warehouse_id}
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=["id", "warehouse_id", "first_name", "last_name", "phone", "status"]))
    print()
    return


