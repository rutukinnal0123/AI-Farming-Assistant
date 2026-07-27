# ============================================================
# predict.py
# ============================================================

import os
import json
import numpy as np
import tensorflow as tf

from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input

# ============================================================
# Paths
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "best_efficientnet_b3.keras")
LABEL_PATH = os.path.join(BASE_DIR, "labels.json")

# ============================================================
# Load Model
# ============================================================

model = tf.keras.models.load_model(MODEL_PATH)

# ============================================================
# Load Labels
# ============================================================

with open(LABEL_PATH, "r") as f:
    class_names = json.load(f)

# ============================================================
# Image Configuration
# ============================================================

IMAGE_SIZE = (300, 300)

# ============================================================
# Prediction Function
# ============================================================

def predict_disease(image_path):
    """
    Predict crop disease from an image.

    Args:
        image_path (str): Path to the uploaded image.

    Returns:
        dict: Prediction result containing crop, disease, and confidence.
    """

    # Load image
    image = Image.open(image_path).convert("RGB")

    # Resize image
    image = image.resize(IMAGE_SIZE)

    # Convert to NumPy array
    image = np.array(image, dtype=np.float32)

    # EfficientNet preprocessing
    image = preprocess_input(image)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Predict
    predictions = model.predict(image, verbose=0)[0]

    # Best prediction
    predicted_index = int(np.argmax(predictions))

    confidence = float(predictions[predicted_index]) * 100

    label = class_names[predicted_index]

    # Split label into crop and disease
    if "___" in label:
        crop, disease = label.split("___", 1)
    else:
        crop = "Unknown"
        disease = label

    return {
        "crop": crop,
        "disease": disease,
        "confidence": round(confidence, 2)
    }
