import os

import google.generativeai as genai

from dotenv import load_dotenv

from rag.retriever import retrieve_documents

from services.weather_service import get_weather


# ==========================================================
# Load Gemini
# ==========================================================

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# ==========================================================
# Retrieve RAG Context
# ==========================================================

def build_context(question):

    docs = retrieve_documents(question)

    if not docs:
        return "", False

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context, True

# ==========================================================
# Build Farmer Context
# ==========================================================

def build_farmer_context(

    farmer=None,

    farm=None,

    activities=None,

    reminders=None

):

    weather = None

    if farmer:

        weather = get_weather(
            farmer.district
        )

    farmer_context = ""

    if farmer:

        farmer_context += f"""
Farmer Information

Name : {farmer.name}

District : {farmer.district}

Village : {farmer.village}

Preferred Language : {farmer.language}
"""

    if farm:

        farmer_context += f"""

Farm Information

Farm Name : {farm.farm_name}

Crop : {farm.crop}

Crop Stage : {farm.crop_stage}

Land Size : {farm.land_size} acres

Soil Type : {farm.soil_type}

Irrigation : {farm.irrigation}
"""

    activity_context = ""

    if activities:

        activity_context = "\n".join(

            f"- {a.activity_type}: {a.description}"

            for a in activities

        )

    reminder_context = ""

    if reminders:

        reminder_context = "\n".join(

            f"- {r.title}"

            for r in reminders

        )

    return (

        farmer_context,

        activity_context,

        reminder_context,

        weather

    )

# ==========================================================
# AI Assistant
# ==========================================================

def ask_ai(

    question,

    farmer=None,

    farm=None,

    activities=None,

    reminders=None

):

    # -----------------------------------------
    # Retrieve RAG Context
    # -----------------------------------------

    rag_context, rag_found = build_context(question)

    # -----------------------------------------
    # Farmer Context
    # -----------------------------------------

    farmer_context, activity_context, reminder_context, weather = build_farmer_context(

        farmer,

        farm,

        activities,

        reminders

    )

    # -----------------------------------------
    # If RAG Found
    # -----------------------------------------

    if rag_found:

        prompt = f"""

You are AgriMitra,
an intelligent AI farming assistant for Kerala farmers.

Use ONLY the agricultural information provided below.
Do NOT make up information.

============================

Farmer Profile

{farmer_context}

============================

Current Weather

{weather}

============================

Recent Activities

{activity_context}

============================

Pending Reminders

{reminder_context}

============================

Agricultural Knowledge

{rag_context}

============================

Farmer Question

{question}

============================

Answer the farmer in a practical,
easy-to-understand way.

Give step-by-step advice.

If weather affects the advice,
mention it.

Do not mention that you used documents.

"""

        response = model.generate_content(prompt)

        return response.text
    

    # -----------------------------------------
    # Gemini Fallback
    # -----------------------------------------

    prompt = f"""

You are AgriMitra,
an intelligent AI farming assistant
for Kerala farmers.

Provide accurate, practical, and personalized
agricultural advice.

====================================================

Farmer Profile

{farmer_context}

====================================================

Recent Activities

{activity_context}

====================================================

Pending Reminders

{reminder_context}

====================================================

Current Weather

{weather}

====================================================

Farmer Question

{question}

====================================================

Instructions

1. Answer using your agricultural knowledge.

2. Consider the farmer's crop, crop stage,
soil type, irrigation and weather.

3. Give practical step-by-step advice.

4. If rain is expected,
recommend postponing spraying.

5. If humidity is high,
warn about fungal diseases.

6. If temperature is high,
recommend irrigation and mulching.

7. Mention precautions whenever necessary.

8. If the problem appears serious,
advise contacting the nearest Krishi Bhavan.

9. Keep the answer simple and farmer-friendly.

"""

    response = model.generate_content(prompt)

    return response.text