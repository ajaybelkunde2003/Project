from googletrans import Translator

def translate_to_hindi(text):
    translator = Translator()
    translation = translator.translate(text,dest='hi')
    return translation.text


import mysql.connector
from mysql.connector import Error
global connection
try:
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Darshan@1234",
            database="pandeyji_eatery")
    if connection.is_connected():
            print("Connected to MySQL database")
except Error as e:
        print(f"Error: {e}")



def get_next_order_id():
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        print(1)
    else:
        print(result+1)


cursor = connection.cursor()
query="SELECT * FROM orders"
cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()
cursor.close()

# Print the fetched rows
# for row in rows:
# print(row)


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
    'Vegetable Biriyani': 5,
    'vegetable biriyani':5,
    'Veg Biryani': 5,
    'Vegetable Pulao': 5,
    'Vegetarian Biryani': 5,
    'Veggie Pilaf': 5,
    'Vegetable Rice Pilaf': 5,
    'Masala Dosa': 6,
    'masala dosa':6,
    'Masala Thosai': 6,
    'Spiced Dosa': 6,
    'Spicy Dosa': 6,
    'Masala Dose': 6,
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

def gooogle_detect_language(text):
    translator = Translator()
    try:
        # Detect the language of the text
        detection = translator.detect(text)
        language = detection.lang
        return language
    except Exception as e:
        print(f"Error in detecting language: {e}")
        return None

from langdetect import detect_langs

def detect_language(text):
    # Detect the language probabilities
    lang_probabilities = detect_langs(text)

    # Get the language with the highest probability
    dominant_language = lang_probabilities[0]
   # print(dominant_language.lang)

    # Check if the detected language is Hindi (hi) and the probability is significant
    if dominant_language.lang == 'hi' and dominant_language.prob >= 0.5:
        return "hi"
    else:
        return "Unknown or Non-Hindi"

import re

def detect_script(numeral_text):
    # Regular expression patterns for Devanagari and English numerals
    devanagari_pattern = re.compile(r'^[०-९]+$')
    english_pattern = re.compile(r'^\d+$')

    # Check if the numeral text contains Devanagari numerals
    if devanagari_pattern.match(numeral_text):
        return "Devanagari"
    # Check if the numeral text contains English numerals
    elif english_pattern.match(numeral_text):
        return "English"
    else:
        return "Unknown"

menu_dictionary = {
    "पाव भाजी": "Pav Bhaji",
    "छोले भटूरे": "Chole Bhature",
    "पिज्जा": "Pizza",
    "मैंगो लस्सी":"Mango Lassi",
    "मसाला डोसा":"Masala Dosa",
    "वेज बिरयानी":"Vegetable Biryani",
    "वडा पाव":"Vada Pav",
    "रवा डोसा":"Rava Dosa",
    "समोसा":"Samosa"
}
