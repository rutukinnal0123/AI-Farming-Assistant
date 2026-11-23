# ============================================================
# AI FARMING ASSISTANT
# CNN INFERENCE ENGINE
#
# FLOW:
#
# IMAGE
#   ↓
# CROP CLASSIFIER
#   ↓
# CROP
#   ↓
# CROP-SPECIFIC DISEASE MODEL
#   ↓
# TOP 2 DISEASES
#
# IMPORTANT:
# - No training
# - No fine-tuning
# - No training augmentation
# - No TTA
# - No model modification
# - Crop confidence is NOT returned
# - Class indices are NOT returned
# ============================================================

import os
import json
import threading

import numpy as np
import tensorflow as tf


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "config",
    "class_labels.json"
)


# ============================================================
# MODEL FILES
# ============================================================

MODEL_FILES = {

    "plant":
        "crop_classifier.keras",

    "banana":
        "best_banana_stage2_model.keras",

    "coconut":
        "best_corrected_finetuned_efficientnetb3.keras",

    "coffee":
        "best_targeted_efficientnetb3.keras",

    "mango":
        "best_domain_generalization_model.keras",

    "rice":
        "best_stage1_efficientnetb3.keras"
}


# ============================================================
# MODEL-SPECIFIC PREPROCESSING
# ============================================================

PREPROCESSING = {

    "plant": {
        "resize": "standard",
        "size": (300, 300),
        "scale": "0-255"
    },

    "banana": {
        "resize": "standard",
        "size": (300, 300),
        "scale": "0-255"
    },

    "coconut": {
        "resize": "standard",
        "size": (300, 300),
        "scale": "0-1"
    },

    "coffee": {
        "resize": "standard",
        "size": (300, 300),
        "scale": "0-255"
    },

    "mango": {
        "resize": "pad",
        "size": (224, 224),
        "scale": "0-255"
    },

    "rice": {
        "resize": "standard",
        "size": (300, 300),
        "scale": "0-1"
    }
}


# ============================================================
# MODEL CACHE
# ============================================================

_MODELS = {}

_CONFIG = None

_MODEL_LOCK = threading.Lock()


# ============================================================
# LOAD CLASS CONFIGURATION
# ============================================================

def _load_config():

    global _CONFIG

    if _CONFIG is not None:
        return _CONFIG

    if not os.path.isfile(CONFIG_PATH):

        raise FileNotFoundError(
            f"CNN class configuration not found:\n"
            f"{CONFIG_PATH}"
        )

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        _CONFIG = json.load(file)

    return _CONFIG


# ============================================================
# GET MODEL PATH
# ============================================================

def _get_model_path(model_name):

    if model_name not in MODEL_FILES:

        raise ValueError(
            f"Unknown CNN model: {model_name}"
        )

    return os.path.join(
        MODELS_DIR,
        model_name,
        MODEL_FILES[model_name]
    )


# ============================================================
# LOAD ONE MODEL
# ============================================================

def _load_model(model_name):

    if model_name in _MODELS:
        return _MODELS[model_name]

    with _MODEL_LOCK:

        if model_name in _MODELS:
            return _MODELS[model_name]

        model_path = _get_model_path(
            model_name
        )

        if not os.path.isfile(model_path):

            raise FileNotFoundError(
                f"Model not found:\n"
                f"{model_path}"
            )

        model = tf.keras.models.load_model(
            model_path,
            compile=False
        )

        _MODELS[model_name] = model

        return model


# ============================================================
# LOAD ALL MODELS
# ============================================================

def load_all_models():

    _load_config()

    for model_name in MODEL_FILES:

        _load_model(
            model_name
        )

    return _MODELS


# ============================================================
# LOAD IMAGE
# ============================================================

def _load_image(image_path):

    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"Image not found:\n"
            f"{image_path}"
        )

    image_bytes = tf.io.read_file(
        image_path
    )

    image = tf.io.decode_image(
        image_bytes,
        channels=3,
        expand_animations=False
    )

    image.set_shape(
        [None, None, 3]
    )

    image = tf.cast(
        image,
        tf.float32
    )

    return image


# ============================================================
# MODEL-SPECIFIC PREPROCESSING
# ============================================================

def _preprocess_for_model(
    image,
    model_name
):

    settings = PREPROCESSING[
        model_name
    ]

    height, width = settings[
        "size"
    ]

    # --------------------------------------------------------
    # MANGO
    # --------------------------------------------------------

    if settings["resize"] == "pad":

        image = tf.image.resize_with_pad(
            image,
            target_height=height,
            target_width=width,
            method=tf.image.ResizeMethod.BILINEAR
        )

    # --------------------------------------------------------
    # OTHER MODELS
    # --------------------------------------------------------

    else:

        image = tf.image.resize(
            image,
            [height, width],
            method=tf.image.ResizeMethod.BILINEAR
        )

    # --------------------------------------------------------
    # FLOAT32
    # --------------------------------------------------------

    image = tf.cast(
        image,
        tf.float32
    )

    # --------------------------------------------------------
    # MODEL INPUT RANGE
    # --------------------------------------------------------

    if settings["scale"] == "0-1":

        image = image / 255.0

        image = tf.clip_by_value(
            image,
            0.0,
            1.0
        )

    elif settings["scale"] == "0-255":

        image = tf.clip_by_value(
            image,
            0.0,
            255.0
        )

    else:

        raise ValueError(
            f"Invalid preprocessing scale "
            f"for {model_name}"
        )

    # --------------------------------------------------------
    # BATCH DIMENSION
    # --------------------------------------------------------

    image = tf.expand_dims(
        image,
        axis=0
    )

    return image


# ============================================================
# RUN MODEL
# ============================================================

def _predict_model(
    model_name,
    image
):

    model = _load_model(
        model_name
    )

    output = model(
        image,
        training=False
    )

    probabilities = np.asarray(
        output
    )[0]

    return probabilities


# ============================================================
# GET CLASS NAME
# ============================================================

def _get_class_name(
    model_name,
    class_index
):

    config = _load_config()

    classes = config[
        model_name
    ]["classes"]

    return classes[
        int(class_index)
    ]


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def predict_image(
    image_path
):

    # --------------------------------------------------------
    # LOAD ORIGINAL IMAGE ONCE
    # --------------------------------------------------------

    image = _load_image(
        image_path
    )

    # --------------------------------------------------------
    # STEP 1
    # CROP CLASSIFICATION
    # --------------------------------------------------------

    crop_input = _preprocess_for_model(
        image,
        "plant"
    )

    crop_probabilities = _predict_model(
        "plant",
        crop_input
    )

    crop_index = int(
        np.argmax(
            crop_probabilities
        )
    )

    crop_name = _get_class_name(
        "plant",
        crop_index
    )

    # --------------------------------------------------------
    # MAP CROP TO DISEASE MODEL
    # --------------------------------------------------------

    disease_model = crop_name.lower()

    if disease_model not in MODEL_FILES:

        raise RuntimeError(
            f"No disease model configured "
            f"for crop: {crop_name}"
        )

    # --------------------------------------------------------
    # STEP 2
    # DISEASE CLASSIFICATION
    # --------------------------------------------------------

    disease_input = _preprocess_for_model(
        image,
        disease_model
    )

    disease_probabilities = _predict_model(
        disease_model,
        disease_input
    )

    # --------------------------------------------------------
    # TOP 2 DISEASES
    # --------------------------------------------------------

    top_two_indices = np.argsort(
        disease_probabilities
    )[-2:][::-1]

    diseases = []

    for index in top_two_indices:

        disease_name = _get_class_name(
            disease_model,
            index
        )

        disease_confidence = float(
            disease_probabilities[
                int(index)
            ]
        )

        diseases.append(
            {
                "name":
                    disease_name,

                "confidence":
                    round(
                        disease_confidence * 100,
                        2
                    )
            }
        )

    # --------------------------------------------------------
    # FINAL CLEAN RESULT
    # --------------------------------------------------------

    return {

        "crop":
            crop_name,

        "diseases":
            diseases

    }
