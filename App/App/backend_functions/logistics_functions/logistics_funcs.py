import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate
from backend_functions.admin_functions.logistic_team_funcs import rm_warehouse as admin_rm_warehouse
from backend_functions.admin_functions.order_funcs import view_order_items as admin_view_order_items, generate_otp as admin_gen_otp

cursor: sql.connection.MySQLConnection.cursor
db: sql.connection.MySQLConnection


def set_cursor(c, d):
    global cursor
    global db
    cursor = c
    db = d


def rm_warehouse(id):
    admin_rm_warehouse(id)
    return


def view_warehouse_details(id):
    query = f'''
    Select * from warehouse
    where id = {id};
    '''
    fields = ['ID', 'Name', 'Phone', 'Plot', 'Locality', 'City', 'State']
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=fields))
    print()
    return


def modify_warehouse_details(id, attr, value):
    query = f'''
    update warehouse
    set {attr} = '{value}'
    where id = {id};
    '''
    cursor.execute(query)
    db.commit()
    return


def add_new_del_man(warehouse_id, first_name, last_name, phone):
    query = f'''
    Insert into delivery_man(warehouse_id, first_name, last_name, phone)
    values ({warehouse_id}, '{first_name}', '{last_name}', '{phone}');
    '''
    cursor.execute(query)
    db.commit()
    return


def modify_del_man_details(warehouse_id, del_man_id, attr, value):
    query = f'''
    update delivery_man
    set {attr} = '{value}'
    where warehouse_id = {warehouse_id} and id = {del_man_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def rm_del_man(warehouse_id, del_man_id):
    query = f'''
    Delete from delivery_man
    where warehouse_id = {warehouse_id} and id = {del_man_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def view_own_del_men(warehouse_id):
    query = f'''
    Select * from delivery_man
    where warehouse_id = {warehouse_id};
    '''
    fields = ['ID', 'Warehouse iD', 'First Name', 'Last Name', 'Phone', 'Status']
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=fields))
    print()
    return


def view_own_active_orders(warehouse_id):
    query = f'''
    Select m.order_id from map_delivery m
    where m.warehouse_id = {warehouse_id};
    '''
    fields = ['Order ID']
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=fields))
    print()
    return


def view_order_items(order_id):
    admin_view_order_items(order_id)
    return


def request_otp(order_id):
    admin_gen_otp(order_id)
    return


def update_active_order_status(warehouse_id, order_id, status):
    query = f'''
    update active_orders
    set status = '{status}'
    where id = {order_id} and id in
    (
        Select m.order_id from map_delivery m
        where m.warehouse_id = {warehouse_id}
    );
    '''
    cursor.execute(query)
    db.commit()
    return

