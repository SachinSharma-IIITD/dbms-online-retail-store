from interfaces.app_gui import GUI
from backend_functions.authenticate import find_warehouse_creds
from backend_functions.logistics_functions import logistics_funcs

gui = GUI()

def authenticate_warehouse():
    gui.title('Logistic Partner Login')

    while True:
        gui.subtitle('Company ID')
        gui.prompt()
        id = input()
        name = find_warehouse_creds(id)

        if not name:
            gui.errorLog('Invalid Company ID')
            continue
        break

    gui.welcomeSession(name)
    menu(id)
    return


def menu(id):
    gui.title('Logistics Partner Menu')

    options_list = [
        ('View Logistics Partner Profile', view_warehouse_details),
        ('Modify your Logistics Partner profile', modify_warehouse_details),
        ('View your own delivery men', view_own_del_men),
        ("Modify your delivery man's profile", modify_del_man_details),
        ('Add a new delivery man', add_new_del_man),
        ('View your pending orders', view_own_active_orders),
        ('View order items of pending order', view_order_items),
        ("Update order status", update_active_order_status),
        ("Request OTP for delivery", request_otp),
        ('Remove a delivery man', rm_del_man),
        ('Delete your Logistics Partner account', rm_warehouse)
    ]

    options_list.append(('Back', gui.back))

    while True:
        gui.subtitleForOptions()
        gui.options([i[0] for i in options_list])
        gui.prompt()

        response = int(input())

        if response == len(options_list):
            return

        elif response > len(options_list) or response < 1:
            gui.errorLog('Invalid option')
            gui.tryAgain()
            continue

        else:
            if options_list[response - 1][1](id) == -1:
                return
        continue


def rm_warehouse(id):
    gui.title('Delete your Logistics Partner account')
    gui.subtitle('Please confirm you want to delete your Logistics Partner account')
    gui.options(['yes', 'no'])
    gui.prompt()

    if int(input()) == 1:
        logistics_funcs.rm_warehouse(id)
        gui.infoLog('Account deleted successfully')
        return -1
    else:
        gui.infoLog('Cancelling account deletion...')
        return 0


def view_warehouse_details(id):
    gui.title('View your Logistics Partner account')
    logistics_funcs.view_warehouse_details(id)
    return 0


def modify_warehouse_details(id):
    gui.title('Modify your Logistics Partner account')

    gui.subtitle('Enter the attribute you want to edit')
    gui.prompt()
    attr = input()

    gui.subtitle('Enter the value you want to set')
    gui.prompt()
    value = input()

    logistics_funcs.modify_warehouse_details(id, attr, value)
    gui.infoLog('Profile modified successfully')
    return 0


def add_new_del_man(warehouse_id):
    gui.title('Add a new delivery man')

    gui.subtitle('First Name')
    gui.prompt()
    first_name = input()

    gui.subtitle('Last Name')
    gui.prompt()
    last_name = input()

    gui.subtitle('Phone')
    gui.prompt()
    phone = input()

    logistics_funcs.add_new_del_man(warehouse_id, first_name, last_name, phone)
    gui.infoLog('Delivery man added succcessfully')
    return 0


def modify_del_man_details(warehouse_id):
    gui.title('Modify a delivery man')

    gui.subtitle('Enter the delivery man ID')
    gui.prompt()
    del_man_id = input()

    gui.subtitle('Enter the attribute you want to edit')
    gui.prompt()
    attr = input()

    gui.subtitle('Enter the value you want to set')
    gui.prompt()
    value = input()

    logistics_funcs.modify_del_man_details(warehouse_id, del_man_id, attr, value)
    gui.infoLog("Delivery man's profile updated successfully")
    return 0


def rm_del_man(warehouse_id):
    gui.title('Remove a delivery man')

    gui.subtitle('Enter the delivery man ID')
    gui.prompt()
    del_man_id = input()

    logistics_funcs.rm_del_man(warehouse_id, del_man_id)
    gui.infoLog("Delivery man removed succcessfully")
    return 0


def view_own_del_men(warehouse_id):
    gui.title('View your delivery men')
    logistics_funcs.view_own_del_men(warehouse_id)
    return 0


def view_own_active_orders(warehouse_id):
    gui.title('View your pending orders')
    logistics_funcs.view_own_active_orders(warehouse_id)
    return 0


def view_order_items(warehouse_id):
    gui.title('View order items')

    gui.subtitle('Enter the Order ID')
    gui.prompt()
    order_id = input()

    logistics_funcs.view_order_items(order_id)
    return 0


def request_otp(id):
    gui.title('Request OTP')

    gui.subtitle('Enter the Order ID')
    gui.prompt()
    order_id = input()

    logistics_funcs.request_otp(order_id)
    gui.infoLog('OTP requested to the system')
    return 0


def update_active_order_status(warehouse_id):
    gui.title('Update order status')

    gui.subtitle('Enter the Order ID')
    gui.prompt()
    order_id = input()

    gui.subtitle('Enter the new status')
    gui.prompt()
    status = input()

    logistics_funcs.update_active_order_status(warehouse_id, order_id, status)
    gui.infoLog('Order status updated successfully')
    return 0


