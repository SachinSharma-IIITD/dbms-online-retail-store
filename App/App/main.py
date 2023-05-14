# Full application for DBMS Online Retail Store- Hawwkstore

from mysql.connector import connect
from interfaces.app_gui import GUI
from interfaces.admin_interface import authenticate_admin
from interfaces.customer_interface import authenticate_customer
from interfaces.seller_interface import authenticate_seller
from interfaces.logistic_interface import authenticate_warehouse
from backend_functions.initialize_cursor import set_cursor_global

db = connect(user='root', password='F=Gm2/r2', database='hawwkstore')
cursor = db.cursor()
set_cursor_global(cursor, db)

gui = GUI()

gui.startApp()

# Main menu

while True:
    gui.subtitle('Please select your user type')
    gui.options(['Admin', 'Customer', 'Seller', 'Logistic Partner'])
    gui.subtitle('Enter 0 to exit\n')
    gui.prompt()

    response = int(input())

    if response == 0:
        gui.exitApp()
        break

    elif response == 1:
        authenticate_admin()

    elif response == 2:
        authenticate_customer()

    elif response == 3:
        authenticate_seller()
    
    elif response == 4:
        authenticate_warehouse()

    else:
        gui.errorLog('Invalid user type')
        gui.tryAgain()

    continue