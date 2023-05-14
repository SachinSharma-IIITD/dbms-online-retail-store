from backend_functions.admin_functions import customer_team_funcs, inventory_team_funcs, finance_team_funcs, logistic_team_funcs, employee_funcs, order_funcs, seller_team_funcs
from backend_functions.customer_functions import customer_funcs
from backend_functions.logistics_functions import logistics_funcs
from backend_functions.seller_functions import seller_funcs
import backend_functions.authenticate as auth

def set_cursor_global(cursor, db):
    auth.set_cursor(cursor, db)
    customer_team_funcs.set_cursor(cursor, db)
    seller_team_funcs.set_cursor(cursor, db)
    logistic_team_funcs.set_cursor(cursor, db)
    inventory_team_funcs.set_cursor(cursor, db)
    finance_team_funcs.set_cursor(cursor, db)
    order_funcs.set_cursor(cursor, db)
    employee_funcs.set_cursor(cursor, db)

    customer_funcs.set_cursor(cursor, db)
    seller_funcs.set_cursor(cursor, db)
    logistics_funcs.set_cursor(cursor, db)
    return

