# ============================================================
# STEP 9 — CHECK SAVED MODEL PREPROCESSING
# ============================================================

import os
import tensorflow as tf


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


MODEL_FILES = {
    "plant": "crop_classifier.keras",
    "banana": "best_banana_stage2_model.keras",
    "coconut": "best_corrected_finetuned_efficientnetb3.keras",
    "coffee": "best_targeted_efficientnetb3.keras",
    "mango": "best_domain_generalization_model.keras",
    "rice": "best_stage1_efficientnetb3.keras"
}


print("=" * 80)
print("SAVED MODEL PREPROCESSING AUDIT")
print("=" * 80)


for model_name, filename in MODEL_FILES.items():

    print("\n" + "=" * 80)
    print(f"MODEL: {model_name.upper()}")
    print("=" * 80)

    model_path = os.path.join(
        MODELS_DIR,
        model_name,
        filename
    )

    print("Path:")
    print(model_path)

    if not os.path.isfile(model_path):

        print("STATUS: MODEL NOT FOUND")
        continue

    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )

    print("\nModel name:")
    print(model.name)

    print("\nInput shape:")
    print(model.input_shape)

    print("\nLayers:")
    print("-" * 80)

    preprocessing_found = False

    for index, layer in enumerate(model.layers):

        layer_name = layer.name
        layer_type = layer.__class__.__name__

        print(
            f"{index:02d} | "
            f"{layer_type:<30} | "
            f"{layer_name}"
        )

        # ----------------------------------------------------
        # CHECK COMMON PREPROCESSING LAYERS
        # ----------------------------------------------------

        preprocessing_types = (
            "Rescaling",
            "Normalization",
            "CenterCrop",
            "Resizing",
            "RandomFlip",
            "RandomRotation",
            "RandomZoom",
            "RandomContrast",
            "RandomBrightness",
            "RandomTranslation",
            "RandomCrop"
        )

        if layer_type in preprocessing_types:

            preprocessing_found = True

            print(
                f"     >>> PREPROCESSING LAYER FOUND: "
                f"{layer_type}"
            )

            # Show important configuration
            try:

                config = layer.get_config()

                for key in [
                    "scale",
                    "offset",
                    "mean",
                    "variance",
                    "height",
                    "width"
                ]:

                    if key in config:

                        print(
                            f"         {key}: "
                            f"{config[key]}"
                        )

            except Exception as e:

                print(
                    "     Could not read layer config:",
                    repr(e)
                )

    # --------------------------------------------------------
    # FINAL RESULT FOR THIS MODEL
    # --------------------------------------------------------

    print("\n" + "-" * 80)

    if preprocessing_found:

        print(
            "MODEL PREPROCESSING:"
            " FOUND INSIDE MODEL"
        )

    else:

        print(
            "MODEL PREPROCESSING:"
            " NO STANDARD PREPROCESSING LAYER DETECTED"
        )

    print("-" * 80)


print("\n" + "=" * 80)
print("PREPROCESSING AUDIT COMPLETE")
print("=" * 80)

print("\nIMPORTANT:")
print("No training performed.")
print("No fine-tuning performed.")
print("No predictions performed.")
print("No model weights modified.")
