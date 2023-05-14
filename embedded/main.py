import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate
from app_gui import *

gui = GUI()
gui.startApp()

try:
    connection = sql.connect(
        user='root', password='F=Gm2/r2', host='localhost', database='hawwkstore')

except sql.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        gui.errorLog("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        gui.errorLog("Database does not exist")
    else:
        gui.errorLog(err)

else:
    gui.infoLog('Database Connected')

    cursor = connection.cursor()

    while(True):
        gui.subtitleForOptions()
        gui.options(['Show your invoices', 'Show your buying statistics', 'exit'])
        gui.prompt()
        response = input()
        query = ""
        fields = []

        if response == '3':
            break

        elif response == '1':
            print()
            gui.subtitle("What's your customer_id ?")
            gui.prompt()
            id = input()

            query = (f"""select c.id, first_name, last_name, payment.order_id, 
                        price as order_value,
                        date_of_order as order_date,
                        date_of_delivery as delivery_date, 
                        date_of_payment as payment_date, 
                        mode_of_payment
                        from customers as c, payment
                        join map_prev_orders
                        on map_prev_orders.order_id = payment.order_id
                        join orders
                        on map_prev_orders.order_id = orders.id
                        where map_prev_orders.customer_id = c.id
                        and c.id = {id}
                        group by c.id, order_id
                        order by c.id, payment_date desc;""")

            fields = ['customer_id', 'first_name', 'last_name', 'order_id', 'order_value', 'order_date',
                    'delivery_date', 'payment_date', 'mode_of_payment']

        elif response == '2':
            print()
            gui.subtitle("What's your customer_id ?")
            gui.prompt()
            id = input()

            query = (f"""select id, first_name, last_name, count(order_id) as total_active_orders
                        from customers as c
                        join map_active_orders
                        on id = customer_id
                        where id = {id}
                        group by id
                        order by total_active_orders desc;""")

            fields = ['customer_id', 'first_name', 'last_name', 'total_active_orders']

        else:
            gui.tryAgain()
            continue

        cursor.execute(query)
        output = cursor.fetchall()
        print()

        if len(output) == 0:
            gui.infoLog('No matching record found')
        else:
            gui.title('Output')
            print(tabulate(output, headers=fields))
        print('\n')

    cursor.close()
    connection.close()

gui.exitApp()
