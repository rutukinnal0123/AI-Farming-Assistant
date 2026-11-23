# ============================================================
# CNN PREDICTOR TEST
# ============================================================

import os
import sys

from predictor import predict_image


# ============================================================
# IMAGE ARGUMENT
# ============================================================

if len(sys.argv) != 2:

    print()
    print("Usage:")
    print(
        'python test_predictor.py "PATH_TO_IMAGE"'
    )
    print()

    sys.exit(1)


image_path = os.path.abspath(
    sys.argv[1]
)


# ============================================================
# FILE CHECK
# ============================================================

if not os.path.isfile(image_path):

    raise FileNotFoundError(
        f"Image not found:\n{image_path}"
    )


# ============================================================
# START
# ============================================================

print("=" * 80)
print("CNN END-TO-END PREDICTION TEST")
print("=" * 80)

print()
print("Image:")
print(image_path)

print()
print("Running CNN inference...")

print()
print("Training: NO")
print("Fine-tuning: NO")
print("Augmentation: NO")
print("TTA: NO")
print("Model modification: NO")


# ============================================================
# PREDICTION
# ============================================================

result = predict_image(
    image_path
)


# ============================================================
# CLEAN DISPLAY
# ============================================================

print()
print("=" * 80)
print("PREDICTION RESULT")
print("=" * 80)

print()

print(
    f"Crop: {result['crop']}"
)

print()

print("Top 2 Diseases:")

for rank, disease in enumerate(
    result["diseases"],
    start=1
):

    print(
        f"{rank}. "
        f"{disease['name']} — "
        f"{disease['confidence']:.2f}%"
    )

print()
print("=" * 80)
print("PREDICTION COMPLETE")
print("=" * 80)
