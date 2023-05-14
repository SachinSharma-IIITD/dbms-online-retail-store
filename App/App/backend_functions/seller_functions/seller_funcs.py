import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate
from backend_functions.admin_functions.seller_team_funcs import rm_seller as admin_rm_seller

cursor: sql.connection.MySQLConnection.cursor
db: sql.connection.MySQLConnection


def set_cursor(c, d):
    global cursor
    global db
    cursor = c
    db = d


def rm_seller(id):
    query = f'''
    Delete from seller
    where id ={id};
    '''
    cursor.execute(query)
    db.commit()
    admin_rm_seller(id)
    return


def view_seller_details(id):
    query = f'''
    Select * from seller
    where id = {id};
    '''
    cursor.execute(query)
    row = cursor.fetchall()
    print(tabulate(row, headers=['id', 'name', 'office_no', 'locality', 'city', 'state', 'phone']))
    return


def modify_seller_details(id, attr, value):
    query = f'''
    update seller
    set {attr} = '{value}'
    where id = {id};
    '''
    cursor.execute(query)
    db.commit()
    return


def add_new_product(seller_id, brand, name, cat_id, price, qty, specs):
    query = f'''
        insert into product (brand, name, cat_id, price, qty, specs)
        values ('{brand}', '{name}', {int(cat_id)}, {price}, {qty}, '{specs}');
        '''
    cursor.execute(query)
    db.commit()

    query2 = (f"""
            select max(id) from product;
            """)
    cursor.execute(query2)
    product_id = int(cursor.fetchall()[0][0])
    print(product_id)

    query3 = (f"""
            insert into map_sellers (seller_id, product_id, qty)
            values ({seller_id}, {product_id}, {qty});
            """)
    cursor.execute(query3)
    db.commit()
    return


def change_product_qty(product_id, qty):
    query2 = f'''
    Update product
    set qty = {qty}
    where id = {product_id};
    '''
    cursor.execute(query2)
    db.commit()
    return


def change_product_price(product_id, price):
    query2 = f'''
    Update product
    set price = {price}
    where id = {product_id};
    '''
    cursor.execute(query2)
    db.commit()
    return


def rm_product(product_id):
    query2 = f'''
    Delete from product
    where id = {product_id};
    '''
    cursor.execute(query2)
    db.commit()
    return


def view_own_products(seller_id):
    query = f'''
        Select s.product_id from map_sellers s
        where s.seller_id = {seller_id};
        '''

    cursor.execute(query)
    new_output = cursor.fetchall()
    # print(new_output)
    products = []

    for p_id in new_output:
        query3 = f'''
        Select * from product
        where id = {p_id[0]};
        '''
        cursor.execute(query3)
        products.append(cursor.fetchall()[0])

    fields = ['ID', 'BRAND', 'NAME', 'CAT_ID', 'PRICE', 'QTY', 'SPECS']
    print(tabulate(products, headers=fields))
    print()
    return

