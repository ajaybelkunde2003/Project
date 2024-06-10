import re
from googletrans import Translator
from langdetect import detect_langs

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""



def detect_language(text):
    translator = Translator()
    try:
        # Detect the language of the text
        detection = translator.detect(text)
        language = detection.lang
        return language
    except Exception as e:
        print(f"Error in detecting language: {e}")
        return None



def translate_to_hindi(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='hi')
    return translation.text



def detect_mixed_languages(text):
    translator = Translator()
    words = text.split()
    detected_languages = []

    for word in words:
        detected_word_lang = translator.detect(word)
        detected_languages.append(detected_word_lang.lang)

    return detected_languages



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

