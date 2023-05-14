from interfaces.app_gui import GUI
from backend_functions.authenticate import find_customer_creds
from backend_functions.customer_functions import customer_funcs

gui = GUI()


def authenticate_customer():
    gui.title('Customer Login')

    while True:
        gui.subtitle('Customer ID')
        gui.prompt()
        id = input()
        name = find_customer_creds(id)

        if not name:
            gui.errorLog('Invalid ID')
            continue
        break

    gui.welcomeSession(name)
    main_menu(id)
    return


def signup_customer():
    gui.title('Customer Signup')

    gui.subtitle('First Name')
    gui.prompt()
    first_name = input()

    gui.subtitle('Last Name')
    gui.prompt()
    last_name = input()

    gui.subtitle('Gender')
    gui.prompt()
    gender = input()

    gui.subtitle('House No')
    gui.prompt()
    house_no = input()

    gui.subtitle('Locality')
    gui.prompt()
    locality = input()

    gui.subtitle('City')
    gui.prompt()
    city = input()

    gui.subtitle('State')
    gui.prompt()
    state = input()

    customer_funcs.new_customer(
        first_name, last_name, gender, house_no, locality, city, state)
    gui.infoLog('Customer signup successful')
    return


def main_menu(id):
    gui.title('Customer Menu')

    options_list = [
        ('View Customer Profile', view_customer_details),
        ('Modify your Customer profile', modify_customer_details),
        ('View all categories', view_all_categories),
        ('View active orders', view_active_orders),
        ('Track active orders', track_active_order),
        ('View cart', view_cart),
        ('Checkout cart', checkout_cart),
        ('Empty cart', empty_cart),
        ("Change a product's quantity in cart", change_qty_in_cart),
        ('Remove a product from cart', rm_from_cart),
        ('View order history', view_order_history),
        ('Delete your Customer account', rm_customer)
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


def rm_customer(id):
    gui.title('Delete your Customer account')
    gui.subtitle('Are you sure you want to delete your Customer account?')
    gui.options(['yes', 'no'])
    gui.prompt()

    if int(input()) == 1:
        customer_funcs.rm_customer(id)
        gui.infoLog('Customer account deleted successfully')
        return -1
    else:
        gui.infoLog('Cancelling deleting account...')
        return 0


def view_customer_details(id):
    gui.title('View your Customer account')
    customer_funcs.view_customer_details(id)
    return 0


def modify_customer_details(id):
    gui.title('Modify your Customer Profile')

    gui.subtitle('Enter the attribute you want to edit')
    gui.prompt()
    attr = input()

    gui.subtitle('Enter the new value')
    gui.prompt()
    value = input()

    customer_funcs.modify_customer_details(id, attr, value)
    gui.infoLog('Customer profile modified successfully')
    return 0


def view_cart(id):
    gui.title('View your Cart')
    if not customer_funcs.view_cart(id):
        gui.infoLog('Your Cart is empty')
    return 0


def view_all_categories(id):
    gui.title('Categories')
    customer_funcs.view_all_categories()

    gui.subtitle('Select a category')
    gui.subtitle('Enter 0 to go back\n')
    gui.prompt()
    cat_id = int(input())

    if not cat_id:
        gui.back()
        return 0

    view_products_of_category(id, cat_id)
    return 0


def view_products_of_category(customer_id, cat_id):
    while True:
        cat_name = customer_funcs.find_category_name(cat_id)
        gui.title(f'Products of {cat_name}')
        customer_funcs.view_products_of_category(cat_id)

        gui.subtitleForOptions()
        gui.options(['Add a product to cart', 'Back'])
        gui.prompt()
        response = int(input())

        if response == 1:
            add_to_cart(customer_id)
            continue
        else:
            gui.back()
            break
    return 0


def add_to_cart(customer_id):
    gui.title('Add to Cart')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    gui.subtitle('Enter the quantity')
    gui.prompt()
    quantity = input()

    customer_funcs.add_to_cart(customer_id, product_id, quantity)
    gui.infoLog('Product added to cart successfully')
    return 0


def rm_from_cart(customer_id):
    gui.title('Remove from Cart')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    customer_funcs.rm_from_cart(customer_id, product_id)
    gui.infoLog('Product removed from cart successfully')
    return 0


def change_qty_in_cart(customer_id):
    gui.title('Change Quantity in Cart')

    gui.subtitle('Enter the product ID')
    gui.prompt()
    product_id = input()

    gui.subtitle('Enter the new quantity')
    gui.prompt()
    qty = input()

    customer_funcs.change_qty_in_cart(customer_id, product_id, qty)
    gui.infoLog('Quantity changed in cart successfully')
    return 0


# def view_offers(order_id):
#     pass

def empty_cart(customer_id):
    gui.subtitle('Are you sure you want to empty the cart')
    gui.options(['yes', 'no'])
    gui.prompt()

    if int(input()) == 1:
        customer_funcs.empty_cart(customer_id)
        gui.infoLog('Cart is emptied')

    else:
        gui.infoLog('Cancelling op...')

    return 0


def checkout_cart(customer_id):
    gui.title('Checkout Cart')
    order_id = customer_funcs.checkout_cart(customer_id)
    if order_id == -1:
        gui.errorLog('Delivery NOT available')
        return 0
    if order_id == -2:
        gui.errorLog('Qty NOT sufficient to place order')
        return 0

    raw_price = customer_funcs.get_cart_value(customer_id)
    gui.subtitle('Gross total: ' + str(raw_price))

    discount = customer_funcs.get_max_discount(order_id)
    gui.subtitle('Max discount applied: ' + str(discount))

    final_price = float(raw_price) * (1 - float(discount)/100)
    # customer_funcs.update_order_price(order_id, final_price)
    gui.subtitle('Net Total: ' + str(final_price))

    place_order(customer_id, order_id, raw_price, final_price)
    return 0


def place_order(customer_id, order_id, raw_price, final_price):
    gui.subtitle('Do you want to place the order?')
    gui.options(['yes', 'no'])
    gui.prompt()

    if input() == '1':
        mode = make_payment(customer_id, order_id, final_price)
        if mode:
            customer_funcs.place_order(
                customer_id, order_id, raw_price, final_price, mode)
            gui.infoLog('Order placed successfully')
            return

    customer_funcs.delete_order(order_id)
    gui.infoLog('Order not placed')
    return


# def get_order_invoice(order_id):
#     pass


def make_payment(customer_id, order_id, price):
    gui.title('Payment')
    gui.subtitle('Select your preferred payment mode')
    gui.options(['cash', 'credit card', 'debit card', 'upi', 'net banking'])
    gui.prompt()
    payment_mode = input()

    gui.subtitle(f'Confirm payment of {price}?')
    gui.options(['yes', 'no'])
    gui.prompt()

    if input() == '1':
        customer_funcs.make_payment(customer_id, order_id)
        gui.infoLog('Payment made successfully')
        return payment_mode

    else:
        gui.infoLog('Payment cancelled')
        return False


def track_active_order(customer_id):
    gui.title('Active order details')
    gui.subtitle('Enter the order ID')
    gui.prompt()
    order_id = input()

    customer_funcs.track_active_order(order_id)
    return 0


def view_order_history(customer_id):
    gui.title('Order history')
    customer_funcs.view_order_history(customer_id)
    return 0


def view_active_orders(customer_id):
    gui.title('Active orders')
    customer_funcs.view_active_orders(customer_id)
    return 0

