from interfaces.app_gui import GUI
from backend_functions.authenticate import find_admin_creds
from backend_functions.admin_functions import employee_funcs, inventory_team_funcs, customer_team_funcs, seller_team_funcs, logistic_team_funcs, finance_team_funcs

gui = GUI()


def authenticate_admin():
    gui.title('Admin Login')

    while True:
        gui.subtitle('Employee ID')
        gui.prompt()
        id = input()

        team_id, first_name, password = find_admin_creds(id)

        if not password:
            gui.errorLog('Invalid Username')
            continue
        break

    while True:
        gui.subtitle('Password')
        gui.prompt()
        if input() != password:
            gui.errorLog('Invalid Password')
            continue
        break

    gui.welcomeSession(first_name)
    main_menu(int(team_id))
    return


def main_menu(team_id):
    gui.title('Admin Main Menu')

    inventory_options_list = [('Add a new category', new_category),
                              ('Remove an existing category', rm_category),
                              ('View all categories', view_all_categories),
                              ('View all products', view_all_products),
                              ('View products of a particular category', view_products_of_category)]

    seller_options_list = [('Add a new seller', new_seller),
                           ('Remove an existing seller', rm_seller),
                           ('View all sellers', view_all_sellers)]

    customer_options_list = [('Remove an existing customer', rm_customer),
                             ('View all customers', view_all_customers),
                             ('View all orders', view_all_active_orders),
                             ('View order items', view_order_items)]

    logistic_options_list = [('Add a new logistics partner', new_warehouse),
                             ('Remove an existing logistics partner', rm_warehouse),
                             ('View all logistics partners', view_all_warehouses),
                             ('View all delivery men', view_delivery_men)]

    finance_options_list = [('View all payment details', view_payments)]

    admin_options_list = [('View all employees', view_all_employees)]

    options_list = []

    if int(team_id) == 1:
        # Manager
        options_list = admin_options_list + customer_options_list + inventory_options_list + \
            seller_options_list + logistic_options_list + finance_options_list

    elif int(team_id) == 2:
        # Customer
        options_list = customer_options_list

    elif int(team_id) == 3:
        # Inventory
        options_list = inventory_options_list

    elif int(team_id) == 4:
        # Seller
        options_list = seller_options_list

    elif int(team_id) == 5:
        # Logistics
        options_list = logistic_options_list

    elif int(team_id) == 6:
        # Finance
        options_list = finance_options_list

    options_list.append(('Sign Out', gui.exitSession))

    while True:
        gui.subtitleForOptions()
        gui.options([i[0] for i in options_list])
        gui.prompt()

        response = int(input())

        if response == len(options_list):
            return

        elif response < len(options_list) and response > 0:
            options_list[response-1][1].__call__()

        else:
            gui.tryAgain()

        continue


# Inventory Management Interface functions

def new_category():
    gui.title('Add a new category')
    gui.subtitle('Enter the name of the new category')
    gui.prompt()
    inventory_team_funcs.new_category(input())
    gui.infoLog('Category added successfully')
    return


def rm_category():
    gui.title('Remove an existing category')
    gui.subtitle('Enter the id of the category to be removed')
    gui.prompt()
    inventory_team_funcs.rm_category(input())
    gui.infoLog('Category removed successfully')
    return


def view_all_categories():
    gui.title('View all categories')
    inventory_team_funcs.view_all_categories()
    return


def view_all_products():
    gui.title('View all products')
    inventory_team_funcs.view_all_products()
    return


def view_products_of_category():
    gui.title('View products of a particular category')
    gui.subtitle('Enter the id of the category')
    gui.prompt()
    inventory_team_funcs.view_products_of_category(input())
    return


# Seller Management Interface functions

def new_seller():
    gui.title('Add a new seller')

    gui.subtitle('Company Name')
    gui.prompt()
    name = input()

    gui.subtitle('Office No')
    gui.prompt()
    office_no = input()

    gui.subtitle('Locality')
    gui.prompt()
    locality = input()

    gui.subtitle('City')
    gui.prompt()
    city = input()

    gui.subtitle('State')
    gui.prompt()
    state = input()

    gui.subtitle('Phone Number')
    gui.prompt()
    phone_no = input()

    seller_team_funcs.new_seller(
        name, office_no, locality, city, state, phone_no)

    gui.infoLog('Seller registered successfully')
    return


def rm_seller():
    gui.title('Remove a seller')
    gui.subtitle('Enter the id of the seller')
    gui.prompt()
    seller_team_funcs.rm_seller(input())
    gui.infoLog('Seller removed successfully')
    return


def view_all_sellers():
    gui.title('View all sellers')
    seller_team_funcs.view_all_sellers()
    return


# Customer Management Interface functions

def rm_customer():
    gui.title('Remove a customer')
    gui.subtitle('Enter the id of the customer')
    gui.prompt()
    customer_team_funcs.rm_customer(input())
    gui.infoLog('Customer removed successfully')
    return


def view_all_customers():
    gui.title('View all customers')
    customer_team_funcs.view_all_customers()
    return


def view_all_active_orders():
    gui.title('View all orders')
    customer_team_funcs.view_all_active_orders()
    return


def view_order_items():
    gui.title('View order items')
    gui.subtitle('Enter the order id')
    gui.prompt()
    customer_team_funcs.view_order_items(input())
    return


# Logistic Managament Inteface functions

def new_warehouse():
    gui.title('New Logistics Partner')

    gui.subtitle('Company Name')
    gui.prompt()
    name = input()

    gui.subtitle('Phone Number')
    gui.prompt()
    phone = input()

    gui.subtitle('Plot No')
    gui.prompt()
    plot_no = input()

    gui.subtitle('Locality')
    gui.prompt()
    locality = input()

    gui.subtitle('City')
    gui.prompt()
    city = input()

    gui.subtitle('State')
    gui.prompt()
    state = input()

    logistic_team_funcs.new_warehouse(
        name, phone, plot_no, locality, city, state)
    gui.infoLog('Logistics Partner registered successfully')
    return


def rm_warehouse():
    gui.title('Remove a logistics partner')
    gui.subtitle('Enter the id of the logistics partner')
    gui.prompt()
    logistic_team_funcs.rm_warehouse(input())
    gui.infoLog('Logistics partner removed successfully')
    return


def view_all_warehouses():
    gui.title('View all logistics partners')
    logistic_team_funcs.view_all_warehouses()
    return


def view_delivery_men():
    gui.title('View all delivery men')
    gui.subtitle('Enter the id of the logistics partner')
    gui.prompt()
    logistic_team_funcs.view_delivery_men(input())
    return


# Finance Management Interface functions

def view_payments():
    gui.title('View payments')
    finance_team_funcs.view_payments()
    return


# Admin Management Interface functions

def view_all_employees():
    gui.title('View all employees')
    employee_funcs.view_all_employees()
    return
