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


def new_category(cat_name):
    query = (f"""
    insert into category (`name`)
    values ('{cat_name}');
    """)

    cursor.execute(query)
    db.commit()
    return


def rm_category(id):
    query = (f"""
    delete from category
    where id = {id};
    """)
    cursor.execute(query)
    db.commit()
    return


def view_all_categories():
    query = (f"""
    select *
    from category;
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=["id", "name"]))
    print()
    return


def view_all_products():
    query = (f"""
    select *
    from product;
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=[
          "id", 'brand', "name", 'category_id', 'qty in inventory' "price", 'specifications']))
    print()
    return


def view_products_of_category(cat_id):
    query = (f"""
    select *
    from product
    where cat_id = {cat_id};
    """)
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=[
          "id", 'brand', "name", 'category_id', 'qty in inventory' "price", 'specifications']))
    print()
    return


def find_category_name(cat_id):
    query = (f"""
    select name
    from category
    where id = {cat_id};
    """)
    cursor.execute(query)
    return cursor.fetchall()[0]


def find_product_details(product_id):
    query = (f"""
    select *
    from product
    where id = {product_id};
    """)
    cursor.execute(query)
    return cursor.fetchall()

