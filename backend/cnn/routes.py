# ============================================================
# AI FARMING ASSISTANT
# CNN API ROUTES
# ============================================================

import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from cnn.predictor import predict_image


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/cnn",
    tags=["CNN Disease Detection"]
)


# ============================================================
# ALLOWED IMAGE FORMATS
# ============================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# ============================================================
# PLANT DISEASE PREDICTION
# ============================================================

@router.post("/predict")
async def predict_plant_disease(
    image: UploadFile = File(...)
):

    # --------------------------------------------------------
    # CHECK FILENAME
    # --------------------------------------------------------

    if not image.filename:

        raise HTTPException(
            status_code=400,
            detail="Image filename is missing."
        )


    # --------------------------------------------------------
    # CHECK EXTENSION
    # --------------------------------------------------------

    extension = os.path.splitext(
        image.filename
    )[1].lower()


    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Please upload JPG, JPEG, PNG or WEBP."
            )
        )


    temporary_path = None


    try:

        # ----------------------------------------------------
        # SAVE UPLOADED IMAGE TEMPORARILY
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temporary_path = temp_file.name

            shutil.copyfileobj(
                image.file,
                temp_file
            )


        # ----------------------------------------------------
        # RUN CNN
        # ----------------------------------------------------

        result = predict_image(
            temporary_path
        )


        # ----------------------------------------------------
        # CLEAN API RESPONSE
        #
        # Crop confidence is NOT returned.
        # Class indices are NOT returned.
        # Only crop + top 2 diseases are returned.
        # ----------------------------------------------------

        return {

            "crop":
                result["crop"],

            "diseases": [

                {
                    "name":
                        disease["name"],

                    "confidence":
                        disease["confidence"]

                }

                for disease
                in result["diseases"]

            ]

        }


    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


    except Exception:

        raise HTTPException(
            status_code=500,
            detail="CNN prediction failed."
        )


    finally:

        # ----------------------------------------------------
        # DELETE TEMPORARY FILE
        # ----------------------------------------------------

        if (
            temporary_path
            and
            os.path.exists(
                temporary_path
            )
        ):

            try:

                os.remove(
                    temporary_path
                )

            except OSError:

                pass
