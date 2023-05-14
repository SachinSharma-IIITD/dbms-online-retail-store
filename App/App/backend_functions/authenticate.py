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


def find_admin_creds(id):
    query = f'''
    select admin_id, first_name, password
    from employee
    where id = {id};
    '''
    cursor.execute(query)
    output = cursor.fetchall()

    if not output:
        return None
    else:
        return output[0]


def find_customer_creds(id):
    query = f'''
    select first_name
    from customers
    where id = {id};
    '''
    cursor.execute(query)
    output = cursor.fetchall()

    if not output:
        return None
    else:
        return output[0][0]


def find_seller_creds(id):
    query = f'''
    select name
    from seller
    where id = {id};
    '''
    cursor.execute(query)
    output = cursor.fetchall()

    if not output:
        return None
    else:
        return output[0][0]


def find_warehouse_creds(id):
    query = f'''
    select name
    from warehouse
    where id = {id};
    '''
    cursor.execute(query)
    output = cursor.fetchall()
    
    if not output:
        return None
    else:
        return output[0][0]
    

