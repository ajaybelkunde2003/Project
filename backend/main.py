from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import generic_helper
import db_helper

food_menu = [
    "pav bhaji", "bhaji pav", "mumbai pav bhaji",
    "chole bhature", "chole", "chhole", "puri", "puri chhole",
    "pizza", "pizzas", "cheese pizza",
    "mango lassi", "lassi", "aam lassi", "mango lassi", "mango yogurt", "drink","biriyani","vegetable biriyani",
    "veg biryani", "vegetable pulao", "vegetarian biryani", "veggie pilaf", "vegetable rice pilaf",
    "masala dosa", "masala thosa", "spiced dosa", "spicy dosa", "masala dose",
    "vada pav", "bombay burger", "aloo vada pav", "mumbai burger", "batata vada pav", "potato vada pav", "vada pav",
    "rava dosa", "rava dosa", "instant rava dosa", "sooji dosa", "semolina dosa", "dosa",
    "samosa", "potato patty", "aloo pie", "vegetable pastry", "triangular pastry"
]
hindi_food_menu = [
    "पाव भाजी", "भाजी पाव", "मुंबई पाव भाजी",
    "छोले भटूरे", "छोले", "पूरी", "पूरी छोले",
    "पिज्जा", "पिज्ज़ास", "चीज़ पिज्जा",
    "लस्सी", "आम लस्सी", "मैंगो लस्सी", "मैंगो योगर्ट", "ड्रिंक",
    "वेज बिरयानी", "वेजिटेबल पुलाव", "वेजिटेरियन बिरयानी", "वेजी पिलाफ", "वेजिटेबल राइस पिलाफ","बिरयानी",
    "मसाला डोसा", "मसाला थोसाई", "स्पाइसी डोसा", "मसाला डोसे",
    "वडा पाव", "बॉम्बे बर्गर", "आलू वडा पाव", "मुंबई बर्गर", "बटाटा वडा पाव", "पोटैटो वडा पाव",
    "रवा डोसा", "इंस्टेंट रवा डोसा", "सूजी डोसा", "सूजी का डोसा", "डोसा",
    "समोसा", "आलू पैटी", "आलू पाई", "वेजिटेबल पेस्ट्री", "तिकोनी पेस्ट्री"
]
menu_dictionary = {
    "पाव भाजी": "Pav Bhaji",
    "छोले भटूरे": "Chole Bhature",
    "पिज्जा": "Pizza",
    "मैंगो लस्सी":"Mango Lassi",
    "मसाला डोसा":"Masala Dosa",
    "वेज बिरयानी":"Vegetable Biriyani",
    "वडा पाव":"Vada Pav",
    "रवा डोसा":"Rava Dosa",
    "समोसा":"Samosa",
    "लस्सी":"Mango Lassi"
}



app = FastAPI()

inprogress_orders = {}

#global fulfillment_text


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    query_text = payload['queryResult']['queryText']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'order.add-context:ongoing-order': add_to_order,
        'order.remove-context:ongoing-order': remove_from_order,
        'order.complete-context:ongoing-order': complete_order,
        'track-order-context:ongoing-tracking': track_order,
        'new.order-context-ongoing-order': clear_cache,
    }

    return intent_handler_dict[intent](parameters, session_id,query_text)


def clear_cache(parameters: dict, session_id: str, query_text: str):
    if session_id in inprogress_orders:
        del inprogress_orders[session_id]
    else:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
            print("जारी रखें .... अब आप आर्डर प्लेस कर सकते हैं")
        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        print('continue .... now you can place order ')







def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
            if(menu_dictionary.get(food_item,-1)==-1):
               rcode = db_helper.insert_order_item(
               food_item,
               quantity,
               next_order_id)
               if rcode == -1:
                  return -1
            else:
              hrcode = db_helper.insert_order_item(
              menu_dictionary[food_item],
              quantity,
              next_order_id)
              if hrcode == -1:
                 return -1




    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id


def complete_order(parameters: dict, session_id: str, query_text: str):
    if session_id not in inprogress_orders:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
            fulfillment_text = "मुझे आपके आर्डर को ढूंढने में समस्या हो रही है। क्षमा करें! क्या आप कृपया एक नया आर्डर प्लेस कर सकते हैं?"

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"




    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            lan_code = generic_helper.detect_language(query_text)
            if lan_code=="hi":
               fulfillment_text = "क्षमा करें, मैं आपका आर्डर प्रोसेस करने में सक्षम नहीं था क्योंकि बैकएंड त्रुटि थी। कृपया पुनः एक नया आर्डर दें।"

            else:
                 for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"




        else:
            order_total = db_helper.get_total_order_price(order_id)
            lan_code = generic_helper.detect_language(query_text)
            if lan_code=="hi":
               fulfillment_text = f"बहुत बढ़िया। हमने आपका आर्डर दिया है। " \
                               f"यहाँ आपका आर्डर आईडी है # {order_id}. " \
                               f"आपके आर्डर की कुल कीमत है {order_total}  जिसे आप डिलीवरी के समय भुगतान कर सकते हैं"


            else:
                 for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id # {order_id}. " \
                               f"total price of your order is  {order_total}  which you can pay at the time of delivery!"






        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def add_to_order(parameters: dict, session_id: str, query_text: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]
    lan_code = generic_helper.detect_language(query_text)
    if lan_code=="hi":
        temp=[]
        for i in food_items:
            if i.lower() not in hindi_food_menu:
                      temp.append(i)
        if(len(temp)!=0):
            return JSONResponse(content={
        "fulfillmentText": f"माफ़ कीजिए, लेकिन ये [{temp}] उपलब्ध नहीं हैं। आप मेनू से खाद्य वस्तुएं ऑर्डर कर सकते हैं: [पाव भाजी: ₹ 30.00, छोले भटूरे: ₹ 120.00, पिज्जा: ₹ 90.00, मैंगो लस्सी: ₹ 20.00, मसाला डोसा: ₹ 70.00, वेजिटेबल बिरयानी: ₹ 100.00, वड़ा पाव: ₹ 15.00, रवा डोसा: ₹ 50.00, समोसा: ₹ 15.00]"})
    else:
        for lang in set(generic_helper.detect_mixed_languages(query_text)):
            if(lang=="en"):
                temp=[]
                for i in food_items:
                    if i.lower() not in food_menu:
                        temp.append(i)
                if(len(temp)!=0):
                    return JSONResponse(content={
        "fulfillmentText": f"Sorry but these {temp} are not available. You can order food-items from the menu: [Pav Bhaji  : ₹ 30.00  ,Chole Bhature  : ₹ 120.00 ,   Pizza  :₹ 90.00,  Mango Lassi :   ₹ 20.00   ,Masala Dosa : ₹ 70.00 ,Vegetable Biryani  :₹ 100.00 ,Vada Pav :₹ 15.00,  Rava Dosa  :₹ 50.00, Samosa :₹ 15.00]"})


    if(len(quantities)==0):
         if lan_code=="hi":
               return JSONResponse(content={
        "fulfillmentText": "कृपया खाद्य-सामग्री के लिए संख्या निर्दिष्ट करें"})
         else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        return JSONResponse(content={
        "fulfillmentText": "please specify number of food-items"})


    fulfillment_text=""
    if len(food_items) != len(quantities):
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
               fulfillment_text = "मुझे माफ़ कीजिए मुझे समझ नहीं आया। क्या आप कृपया भोजन आइटम और मात्रा स्पष्ट रूप से निर्दिष्ट कर सकते हैं?"
        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"





    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
               fulfillment_text = f"अब तक आपके पास है {order_str}. क्या आपको कुछ और चाहिए?"

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"






    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str, query_text: str):
    #if session_id in inprogress_orders:
    for i in inprogress_orders:
         print(i)
    print(session_id)
    if session_id not in inprogress_orders:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
            return JSONResponse(content={
            "fulfillmentText": "मुझे आपके आर्डर को ढूंढने में समस्या हो रही है। क्षमा करें! क्या आप कृपया एक नया आर्डर प्लेस कर सकते हैं?"
        })

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
               fulfillment_text = f'हटाया गया {",".join(removed_items)} आपके आर्डर से!'

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
               fulfillment_text = f' आपके वर्तमान आर्डर में नहीं है {",".join(no_such_items)}'

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'


    if len(current_order.keys()) == 0:
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
                fulfillment_text += " आपका आर्डर खाली है!"

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text += "Now your order is empty!"


    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        lan_code = generic_helper.detect_language(query_text)
        if lan_code=="hi":
               fulfillment_text += f" यहाँ वह है जो आपके आर्डर में बचा है: {order_str} क्या आपको कुछ और चाहिए?"

        else:
             for lang in set(generic_helper.detect_mixed_languages(query_text)):
                   if(lang=="en"):
                        fulfillment_text += f" Here is what is left in your order: {order_str} Do you need anything else"


    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters: dict, session_id: str, query_text: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        lan_code = generic_helper.detect_script(query_text)
        if lan_code=="Devanagari":
            fulfillment_text = f"आर्डर आईडी: {query_text} के लिए आदेश की स्थिति है: {generic_helper.translate_to_hindi(order_status)}"

        else:
            fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"





    else:
        lan_code = generic_helper.detect_script(query_text)
        if lan_code=="Devanagari":
            fulfillment_text = f"आर्डर आईडी :{query_text} के साथ कोई आदेश नहीं मिला: "

        else:
            fulfillment_text = f"No order found with order id: {order_id}"






    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
