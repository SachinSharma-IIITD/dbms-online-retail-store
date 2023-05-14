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


def new_seller(name, office, locality, city, state, phone):
    query = (f"""
            insert into seller (name, office_no, locality, city, state, phone) values
            ('{name}', '{str(office)}', '{locality}', '{city}', '{state}', '{str(phone)}');
            """)

    cursor.execute(query)
    db.commit()
    return


def rm_seller(id):
    # Also delete corr products
    query = (f"""
            delete from seller
            where id = {id};
            """)
    
    cursor.execute(query)
    db.commit()
    return


def view_all_sellers():
    query = (f"""
            select * from seller;
            """)
    fields = ['Seller ID', 'Name', 'Office No', 'Locality', 'City', 'State', 'Phone']

    cursor.execute(query)
    output = cursor.fetchall()
    print(tabulate(output, headers=fields))
    return


