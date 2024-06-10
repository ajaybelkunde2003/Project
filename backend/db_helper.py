import mysql.connector
global cnx

# noinspection PyRedeclaration
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Darshan@1234",
    database="pandeyji_eatery"
)
food_item_dict = {
    'Pav Bhaji': 1,
    'pav bhaji':1,
    'Bhaji Pav': 1,
    'Mumbai pav bhaji': 1,
    'Chole Bhature': 2,
    'chole bhature':2,
    'Chole': 2,
    'Chhole': 2,
    'Puri': 2,
    'Puri chhole': 2,
    'Pizza': 3,
    'pizza':3,
    'Pizzas': 3,
    'Cheese pizza': 3,
    'Mango Lassi': 4,
    'mango lassi':4,
    'Lassi': 4,
    'Aam lassi': 4,
    'Mango lassi': 4,
    'Mango yogurt': 4,
    'Drink': 4,
    'Vegetable Biriyani': 6,
    'vegetable biriyani':6,
    'Veg Biryani': 6,
    'biriyani':6,
    'Vegetable Pulao': 6,
    'Vegetarian Biryani': 6,
    'Veggie Pilaf': 6,
    'Vegetable Rice Pilaf': 6,
    'Masala Dosa': 5,
    'masala dosa':5,
    'Masala Thosai': 5,
    'Spiced Dosa': 5,
    'Spicy Dosa': 5,
    'Masala Dose': 5,
    'Vada Pav': 7,
    'vada pav':7,
    'Bombay Burger': 7,
    'Aloo Vada Pav': 7,
    'Mumbai Burger': 7,
    'Batata Vada Pav': 7,
    'Potato Vada Pav': 7,
    'Rava Dosa': 8,
    'rava dosa':8,
    'Instant Rava Dosa': 8,
    'Sooji Dosa': 8,
    'Semolina Dosa': 8,
    'Dosa': 8,
    'Samosa': 9,
    'samosa':9,
    'Potato Patty': 9,
    'Aloo Pie': 9,
    'Vegetable Pastry': 9,
    'Triangular Pastry': 9
}



#Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()
        # Calling the stored procedure
        item_id=food_item_dict[food_item]
        cursor.callproc('insert_order_item', (food_item,item_id,quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Function to get the next available order_id
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None


