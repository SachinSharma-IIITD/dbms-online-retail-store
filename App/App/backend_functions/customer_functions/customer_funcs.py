import mysql.connector as sql
from mysql.connector import errorcode
from tabulate import tabulate
from backend_functions.admin_functions.customer_team_funcs import rm_customer as admin_rm_customer
from backend_functions.admin_functions.inventory_team_funcs import view_all_categories as admin_view_all_categories
from backend_functions.admin_functions.inventory_team_funcs import view_products_of_category as admin_view_products_of_category
from backend_functions.admin_functions.inventory_team_funcs import find_category_name as admin_find_category_name
from backend_functions.admin_functions.inventory_team_funcs import find_product_details as admin_find_product_details
from backend_functions.admin_functions.order_funcs import get_max_discount as admin_get_max_discount, generate_offer as admin_generate_offer, view_order_items as admin_view_order_items


cursor: sql.connection.MySQLConnection.cursor
db: sql.connection.MySQLConnection


def set_cursor(c, d):
    global cursor
    global db
    cursor = c
    db = d


def new_customer(first_name, last_name, gender, house_no, locality, city, state):
    query = f'''
    Insert into customers (first_name, last_name, gender, house_no, locality, city, state)
    values ('{first_name}', '{last_name}', '{gender}', '{house_no}', '{locality}', '{city}', '{state}');
    '''
    cursor.execute(query)
    db.commit()
    return


def view_customer_details(id):
    query = f'''
    Select * from customers
    where id = {id};
    '''
    cursor.execute(query)
    fields = ['Customer ID', 'First Name', 'Last Name',
              'Gender', 'House No', 'Locality', 'City', 'State']
    result = cursor.fetchall()
    print(tabulate(result, headers=fields))
    print()
    return


def rm_customer(id):
    admin_rm_customer(id)
    return


def view_all_categories():
    admin_view_all_categories()
    return


def view_products_of_category(cat_id):
    admin_view_products_of_category(cat_id)
    return


def modify_customer_details(id, attr, value):
    query = f'''
    Update customers
    set {attr} = '{value}'
    where id = {id};
    '''
    cursor.execute(query)
    db.commit()
    return


def view_cart(id):
    query2 = f'''
    Select c.product_id from cart c
    where c.customer_id = {id};
    '''
    cursor.execute(query2)
    new_output = cursor.fetchall()

    if not new_output:
        return False
    
    products = []

    for p_id in new_output:
        p_id = p_id[0]
        query3 = f'''
        Select pro.brand, pro.name from product pro
        where pro.id = {p_id};
        '''
        cursor.execute(query3)
        result = cursor.fetchall()
        products.append(result[0])

    fields = ['BRAND', 'NAME']
    print(tabulate(products, headers=fields))
    print()
    return True


def add_to_cart(customer_id, product_id, qty):
    query = f'''
    Insert into cart()
    values ({customer_id}, {product_id}, {qty});
    '''
    cursor.execute(query)
    db.commit()
    return


def rm_from_cart(customer_id, product_id):
    query = f'''
    Delete from cart
    where customer_id = {customer_id} and product_id = {product_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def change_qty_in_cart(customer_id, product_id, qty):
    query = f'''
    Update cart
    set qty = {qty}
    where customer_id = {customer_id} and product_id = {product_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def empty_cart(customer_id):
    query = f'''
    Delete from cart
    where customer_id = {customer_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def is_cart_empty(customer_id):
    query = f'''
    Select c.product_id from cart c
    where c.customer_id = {customer_id};
    '''
    cursor.execute(query)
    new_output = cursor.fetchall()
    if (len(new_output) > 0):
        return False
    else:
        return True


def view_offers(order_id):
    query = f'''
    Select discount from offers
    where order_id = {order_id};
    '''
    cursor.execute(query)
    final_output = cursor.fetchall()
    fields = ['DISCOUNTS AVAILABLE ']
    print(tabulate(final_output, headers=fields))
    print()
    return


def get_max_discount(order_id):
    return admin_get_max_discount(order_id)


def get_cart_items(customer_id):
    query = f'''
    Select product_id, qty from cart
    where customer_id = {customer_id};
    '''
    cursor.execute(query)
    output = cursor.fetchall()
    return output


def get_cart_value(customer_id):
    query = f'''
    create or replace view cart_value as 
    (Select c.qty as selected_qty, price as value, c.customer_id from cart c
    join product p
    on p.id = c.product_id);
    '''
    cursor.execute(query)
    db.commit()

    query2 = f'''
    Select sum(selected_qty * value) from cart_value
    where customer_id = {customer_id};
    '''
    cursor.execute(query2)
    output = cursor.fetchall()
    return float(output[0][0])


def rm_offers(order_id):
    query = f'''
    Delete from offers
    where order_id = {order_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def delete_order(order_id):
    rm_offers(order_id)

    query = f'''
    Delete from orders
    where id = {order_id};
    '''
    cursor.execute(query)
    db.commit()
    return


def find_delivery(state):
    query = f'''
    select id from warehouse
    where state = '{state}';
    '''
    cursor.execute(query)
    warehouses = cursor.fetchall()

    delivery_man = None
    warehouse = None

    query = f'''
    create or replace view available_del_men as
    (select id, warehouse_id from delivery_man
    where status = 'available');
    '''
    cursor.execute(query)
    db.commit()

    for w in warehouses:
        query = f'''
        select id from available_del_men
        where warehouse_id = {w[0]};
        '''
        cursor.execute(query)
        delivery_man = cursor.fetchall()
        if delivery_man:
            warehouse = w[0]
            delivery_man = delivery_man[0][0]
            break

    if not delivery_man:
        return False
    else:
        return warehouse, delivery_man


def get_customer_state(customer_id):
    query = f'''
    select `state` from customers
    where id = {customer_id};
    '''
    cursor.execute(query)
    state = cursor.fetchall()[0][0]
    return state


def checkout_cart(customer_id):
    state = get_customer_state(customer_id)
    delivery = find_delivery(state)

    if not delivery:
        return -1
    
    cart_items = get_cart_items(customer_id)
    
    for pid, selected_qty in cart_items:
        query = (f"""
                select qty from product
                where id = {pid};
                """)
        cursor.execute(query)
        inv_qty = cursor.fetchall()[0][0]

        if selected_qty > inv_qty:
            return -2

    raw_order_value = get_cart_value(customer_id)

    insert_query = (f"""
                    insert into orders (price)
                    values ({raw_order_value});
                    """)
    cursor.execute(insert_query)

    select_id_query = f'''
    Select max(id) from orders;
    '''
    cursor.execute(select_id_query)
    order_id = cursor.fetchall()[0][0]

    rm_offers(order_id)
    admin_generate_offer(order_id, raw_order_value)
    return order_id


def place_order(customer_id, order_id, raw_price, final_price, mode_of_payment):

    query = f'''
    insert into active_orders (id, raw_price)
    values ({order_id}, {round(raw_price, 2)});
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
    insert into map_active_orders (order_id, customer_id)
    values ({order_id}, {customer_id});
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
    insert into map_prev_orders (order_id, customer_id)
    values ({order_id}, {customer_id});
    '''
    cursor.execute(query)
    db.commit()

    rm_offers(order_id)

    query = f'''
    select product_id, qty
    from cart
    where customer_id = {customer_id};
    '''
    cursor.execute(query)
    products = cursor.fetchall()

    for product_id, qty in products:
        query = f'''
        insert into order_item (product_id, order_id, qty)
        values ({product_id}, {order_id}, {qty});
        '''
        cursor.execute(query)
        db.commit()
    
    cart_items = get_cart_items(customer_id)
    for pid, qty_bought in cart_items:
        query =f'''
        update product
        set qty = qty - {qty_bought}
        where id = {pid};
        '''
        cursor.execute(query)
        db.commit()

    empty_cart(customer_id)

    query = f'''
    update orders
    set date_of_order = curdate(), date_of_delivery = curdate() + 2, mode_of_payment = '{mode_of_payment}', price = {final_price}
    where id = {order_id};
    '''
    cursor.execute(query)
    db.commit()

    state = get_customer_state(customer_id)

    warehouse_id, del_man_id = find_delivery(state)

    query = f'''
    insert into map_delivery (order_id, del_man_id, warehouse_id)
    values ({order_id}, {del_man_id}, {warehouse_id});
    '''
    cursor.execute(query)
    db.commit()

    update_del_man_status(del_man_id)
    return


def update_del_man_status(del_man_id):
    query = f'''
    select count(order_id) as c
    from map_delivery
    where del_man_id = {del_man_id}
    group by del_man_id;
    '''
    cursor.execute(query)
    count = int(cursor.fetchall()[0][0])

    if count > 5:
        query = f'''
        update delivery_man
        set status = 'busy'
        where id = {del_man_id};
        '''
        cursor.execute(query)
        db.commit()
    else:
        query = f'''
        update delivery_man
        set status = 'available'
        where id = {del_man_id};
        '''
        cursor.execute(query)
        db.commit()
    return


# def get_order_invoice(order_id):
#     pass


def make_payment(customer_id, order_id):
    query = f'''
            insert into payment (customer_id, order_id, date_of_payment)
            values ({customer_id}, {order_id}, curdate());
            '''
    cursor.execute(query)
    db.commit()


def track_active_order(order_id):
    # Details of active order and delivery
    query = f'''
    select a.id, a.`status`, o.price, o.date_of_order, o.date_of_delivery, o.mode_of_payment, m.warehouse_id, m.del_man_id
    from active_orders a
    join orders o on o.id = a.id
    join map_delivery m on o.id = m.order_id
    where o.id = {order_id};
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        print(tabulate(result, headers=['Order ID', 'Status', 'Order Value', 'Date of Order',
              'Date of Delivery', 'Mode of Payment', 'Warehouse ID', 'Delivery Man ID']))
        print()
        return 0
    else:
        return 1


def view_order_history(customer_id):
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
                and c.id = {customer_id}
                group by c.id, order_id
                order by c.id, payment_date desc;""")

    fields = ['customer_id', 'first_name', 'last_name', 'order_id', 'order_value', 'order_date',
              'delivery_date', 'payment_date', 'mode_of_payment']

    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        print(tabulate(result, headers=fields))
        print()
        return 0
    else:
        return 1


def find_category_name(cat_id):
    return admin_find_category_name(cat_id)


def find_product_details(product_id):
    return admin_find_product_details(product_id)


def view_active_orders(customer_id):
    query = f'''
    select order_id from map_active_orders
    where customer_id = {customer_id};
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        print(tabulate(result, headers=['order_id']))
        print()
        return 0
    else:
        return 1

# def get_order_price(order_id):
#     pass


# def update_order_price(order_id, price):
#     pass
