import tempfile

import whisper

from gtts import gTTS


# Load Whisper model once
model = whisper.load_model("base")


# ==========================================================
# Speech -> Text
# ==========================================================

def speech_to_text(audio_path):

    result = model.transcribe(audio_path)

    return result["text"]


# ==========================================================
# Text -> Speech
# ==========================================================

def text_to_speech(
    text,
    language="ml"
):

    # Support English and Malayalam
    if language.lower() in ["english", "en"]:
        lang = "en"
    else:
        lang = "ml"

    tts = gTTS(
        text=text,
        lang=lang
    )

    output_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(output_file.name)

    return output_file.name