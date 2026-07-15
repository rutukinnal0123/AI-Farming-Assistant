from deep_translator import GoogleTranslator
from langdetect import detect


# ==========================================================
# Detect Language
# ==========================================================

def detect_language(text: str):

    try:
        lang = detect(text)

        if lang == "ml":
            return "Malayalam"

        return "English"

    except:
        return "English"


# ==========================================================
# Malayalam -> English
# ==========================================================

def translate_to_english(text: str):

    return GoogleTranslator(
        source="ml",
        target="en"
    ).translate(text)


# ==========================================================
# English -> Malayalam
# ==========================================================

def translate_to_malayalam(text: str):

    return GoogleTranslator(
        source="en",
        target="ml"
    ).translate(text)