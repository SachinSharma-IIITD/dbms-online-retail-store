from interfaces.app_gui import GUI
from backend_functions.authenticate import find_seller_creds
from backend_functions.seller_functions import seller_funcs

gui = GUI()

def authenticate_seller():
    gui.title('Seller Login')

    while True:
        gui.subtitle('Company ID')
        gui.prompt()
        id = input()
        name = find_seller_creds(id)

        if not name:
            gui.errorLog('Invalid Company ID')
            continue
        break

    gui.welcomeSession(name)
    menu(id)
    return


def menu(id):
    gui.title('Seller Menu')

    options_list = [
        ('View Seller Profile', view_seller_details),
        ('View you own products', view_own_products),
        ('Modify your Seller profile', modify_seller_details),
        ('Add a new product', add_new_product),
        ("Change a product's quantity", change_product_qty),
        ("Change a product's price", change_product_price),
        ('Delete a product', rm_product),
        ('Delete your Seller account', rm_seller)
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


def rm_seller(id):
    gui.title('Delete your Seller account')
    gui.subtitle('Are you sure you want to delete your Seller account?')
    gui.options(['Yes', 'No'])
    gui.prompt()

    response = int(input())
    if response == 1:
        seller_funcs.rm_seller(id)
        gui.infoLog('Your Seller account has been deleted')
        return -1
    
    else:
        gui.infoLog('Cancelling account removal...')
        return 0


def view_seller_details(id):
    gui.title('View your Seller Profile')
    seller_funcs.view_seller_details(id)
    return 0


def modify_seller_details(id):
    gui.title('Modify your Seller Profile')

    gui.subtitle('Enter the attribute you want to modify')
    gui.prompt()
    attribute = input()

    gui.subtitle('Enter the value you want to set')
    gui.prompt()
    value = input()

    seller_funcs.modify_seller_details(id, attribute, value)
    gui.infoLog('Profile modified successfully')
    return 0


def add_new_product(seller_id):
    gui.title('Add a new product')

    gui.subtitle('Enter the brand')
    gui.prompt()
    brand = input()

    gui.subtitle('Enter the product name')
    gui.prompt()
    name = input()

    gui.subtitle('Enter the category ID')
    gui.prompt()
    cat_id = input()

    gui.subtitle('Enter the price')
    gui.prompt()
    price = input()

    gui.subtitle('Enter the quantity')
    gui.prompt()
    qty = input()

    gui.subtitle('Enter the specifications')
    gui.prompt()
    specs = input()

    seller_funcs.add_new_product(seller_id, brand, name, cat_id, price, qty, specs)
    gui.infoLog('Product added successfully')
    return 0


def change_product_qty(seller_id):
    gui.title('Change the quantity of a product')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    gui.subtitle('Enter the new quantity')
    gui.prompt()
    qty = input()

    seller_funcs.change_product_qty(product_id, qty)
    gui.infoLog('Quantity changed successfully')
    return 0


def change_product_price(seller_id):
    gui.title('Change the price of a product')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    gui.subtitle('Enter the new price')
    gui.prompt()
    new_price = input()

    seller_funcs.change_product_price(product_id, new_price)
    gui.infoLog('Price changed successfully')
    return 0


def rm_product(seller_id):
    gui.title('Remove a product')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    seller_funcs.rm_product(product_id)
    gui.infoLog('Product removed successfully')
    return 0


def view_own_products(id):
    gui.title('View your own products')
    seller_funcs.view_own_products(id)
    return 0
