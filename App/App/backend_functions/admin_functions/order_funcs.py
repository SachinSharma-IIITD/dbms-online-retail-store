from random import randint
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


def view_order_items(order_id):
    query = (f"""
            select id, brand, name from product
            where id in 
            (select product_id from order_item
            where order_id = {order_id});
            """)
    fields = ['id', 'brand', 'name']
    cursor.execute(query)
    print(tabulate(cursor.fetchall(), headers=fields))


def generate_otp(order_id):
    otp = randint(1111, 9999)
    query = (f"""
    insert into verify_orders
    (order_id, pin)
    values
    ({order_id}, {otp});
    """)
    cursor.execute(query)
    db.commit()
    return


def verify_otp(order_id, otp: str):
    query = (f"""
    select pin from verify_orders
    where order_id = {order_id}
    """)
    cursor.execute(query)
    row = cursor.fetchall()
    if row:
        if row[0] == otp:
            return True
        else:
            return False
    else:
        return False
    

def generate_offer(order_id, price):
    disc_limit = [5, 10, 20, 30, 50]
    price_limit = [1000, 5000, 10000, 50000, 100000]

    for i in range(len(price_limit)-1, -1, -1):
        if price >= price_limit[i]:
            limit = disc_limit[i]
            break
        else:
            limit = 1

    for i in range(randint(1, 5)):
        discount = randint(1, limit)
        query = (f"""
        insert into offers
        (order_id, discount)
        values
        ({order_id}, {discount})
        """)
        cursor.execute(query)
    db.commit()
    return


def get_max_discount(order_id):
    query = (f"""
            select max(discount) as max_discount 
            from offers 
            where order_id = {order_id}
            group by order_id
            order by max_discount desc;
            """)
    cursor.execute(query)
    return float(cursor.fetchall()[0][0])

