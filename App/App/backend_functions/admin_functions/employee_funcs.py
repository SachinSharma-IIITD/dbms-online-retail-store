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


def view_all_employees():
    cursor.execute("SELECT id, admin_id, first_name, last_name, gender, phone, address FROM employee;")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["ID", "Admin Team ID", "First Name", "Last Name", "Gender", "Phone", "Address"]))
    print()
    return

