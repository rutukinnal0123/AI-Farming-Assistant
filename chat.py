from datetime import date
import shutil
import tempfile

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

import crud
import schemas

from database import SessionLocal
from security import get_current_farmer

from services.ai_service import ask_ai
from services.activity_service import detect_activity
from services.translation_service import (
    detect_language,
    translate_to_english,
    translate_to_malayalam,
)

from services.voice_service import (
    speech_to_text,
    text_to_speech,
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


# ==========================================================
# Database Dependency
# ==========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Request Model
# ==========================================================

class ChatRequest(BaseModel):

    message: str

# ==========================================================
# Text Chat API
# ==========================================================

@router.post("/")
def chat(
    request: ChatRequest,
    current_farmer=Depends(get_current_farmer),
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # Get Farmer Farm
    # -------------------------------------------------

    farms = crud.get_farmer_farms(
        db,
        current_farmer.id
    )

    farm = farms[0] if farms else None

    # -------------------------------------------------
    # Activities
    # -------------------------------------------------

    activities = []

    if farm:

        activities = crud.get_farm_activities(
            db,
            farm.id
        )

    # -------------------------------------------------
    # Reminders
    # -------------------------------------------------

    reminders = []

    if farm:

        reminders = crud.get_farm_reminders(
            db,
            farm.id
        )

    # -------------------------------------------------
    # Detect Farming Activity
    # -------------------------------------------------

    activity = detect_activity(
        request.message
    )

    if activity and farm:

        activity_data = schemas.ActivityCreate(

            farm_id=farm.id,

            activity_type=activity["activity_type"],

            description=activity["description"],

            quantity=None,

            unit=None,

            activity_date=date.today()

        )

        crud.create_activity(
            db,
            activity_data
        )

    # -------------------------------------------------
    # Detect Language
    # -------------------------------------------------

    language = detect_language(
        request.message
    )

    if language.lower() == "malayalam":

        ai_question = translate_to_english(
            request.message
        )

    else:

        ai_question = request.message

    # -------------------------------------------------
    # Ask AI
    # -------------------------------------------------

    answer = ask_ai(

        question=ai_question,

        farmer=current_farmer,

        farm=farm,

        activities=activities,

        reminders=reminders

    )

    # -------------------------------------------------
    # Translate Response
    # -------------------------------------------------

    if language.lower() == "malayalam":

        answer = translate_to_malayalam(
            answer
        )

    # -------------------------------------------------
    # Save Chat
    # -------------------------------------------------

    crud.save_chat(

        db,

        schemas.ChatHistoryCreate(

            farmer_id=current_farmer.id,

            question=request.message,

            answer=answer

        )

    )

    # -------------------------------------------------
    # Return
    # -------------------------------------------------

    return {

        "answer": answer

    }

# ==========================================================
# Voice Chat API
# ==========================================================

@router.post("/voice")
def voice_chat(
    audio: UploadFile = File(...),
    current_farmer=Depends(get_current_farmer),
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # Save uploaded audio
    # -------------------------------------------------

    temp_audio = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    shutil.copyfileobj(
        audio.file,
        temp_audio
    )

    temp_audio.close()

    # -------------------------------------------------
    # Speech -> Text
    # -------------------------------------------------

    question = speech_to_text(
        temp_audio.name
    )

    # -------------------------------------------------
    # Detect Language
    # -------------------------------------------------

    language = detect_language(question)

    if language.lower() == "malayalam":
        ai_question = translate_to_english(question)
    else:
        ai_question = question

    # -------------------------------------------------
    # Get Farmer Farm
    # -------------------------------------------------

    farms = crud.get_farmer_farms(
        db,
        current_farmer.id
    )

    farm = farms[0] if farms else None

    activities = []

    reminders = []

    if farm:

        activities = crud.get_farm_activities(
            db,
            farm.id
        )

        reminders = crud.get_farm_reminders(
            db,
            farm.id
        )

    # -------------------------------------------------
    # Detect Farming Activity
    # -------------------------------------------------

    activity = detect_activity(question)

    if activity and farm:

        activity_data = schemas.ActivityCreate(

            farm_id=farm.id,

            activity_type=activity["activity_type"],

            description=activity["description"],

            quantity=None,

            unit=None,

            activity_date=date.today()

        )

        crud.create_activity(
            db,
            activity_data
        )

    # -------------------------------------------------
    # Ask AI
    # -------------------------------------------------

    answer = ask_ai(

        question=ai_question,

        farmer=current_farmer,

        farm=farm,

        activities=activities,

        reminders=reminders

    )

    # -------------------------------------------------
    # Translate Answer
    # -------------------------------------------------

    if language.lower() == "malayalam":

        answer = translate_to_malayalam(answer)

    # -------------------------------------------------
    # Text -> Speech
    # -------------------------------------------------

    if language.lower() == "malayalam":
        audio_path = text_to_speech(
            answer,
            language="ml"
        )
    else:
        audio_path = text_to_speech(
            answer,
            language="en"
        )

    # -------------------------------------------------
    # Save Chat
    # -------------------------------------------------

    crud.save_chat(

        db,

        schemas.ChatHistoryCreate(

            farmer_id=current_farmer.id,

            question=question,

            answer=answer

        )

    )

    # -------------------------------------------------
    # Delete Temporary Audio
    # -------------------------------------------------

    try:
        temp_audio.close()
    except:
        pass

    # -------------------------------------------------
    # Return
    # -------------------------------------------------

    return {

        "question": question,

        "answer": answer,

        "audio_file": audio_path

    }