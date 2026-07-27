# ============================================================
# cnn.py
# FastAPI Router for CNN Prediction
# ============================================================

import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse

from cnn.predict import predict_disease

router = APIRouter(
    prefix="/cnn",
    tags=["CNN Disease Prediction"]
)

# ============================================================
# Upload Directory
# ============================================================

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============================================================
# Prediction Endpoint
# ============================================================

@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image."
        )

    # Create unique filename
    extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        result = predict_disease(file_path)

        return PlainTextResponse(
            f"Crop: {result['crop']}\n"
            f"Disease: {result['disease']}\n"
            f"Confidence: {result['confidence']}%"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Delete uploaded image
        if os.path.exists(file_path):
            os.remove(file_path)
