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


def view_payments():
    query = (f"""
            select * from payment;
            """)
    cursor.execute(query)
    payments = cursor.fetchall()
    print(tabulate(payments, headers=["order ID", "customer ID", "date of payment"]))
    print()
    return

