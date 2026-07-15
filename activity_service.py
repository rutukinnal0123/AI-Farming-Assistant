import re


def detect_activity(message: str):

    text = message.lower()

    activity = None

    if "irrigat" in text or "water" in text:
        activity = "Irrigation"

    elif "sow" in text or "plant" in text:
        activity = "Sowing"

    elif "fertilizer" in text or "manure" in text:
        activity = "Fertilizer"

    elif "spray" in text or "pesticide" in text:
        activity = "Pesticide Spraying"

    elif "harvest" in text:
        activity = "Harvesting"

    elif "weed" in text:
        activity = "Weeding"

    if activity is None:
        return None

    return {
        "activity_type": activity,
        "description": message
    }