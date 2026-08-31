# ============================================================
# STEP 7 — VERIFY MODEL OUTPUTS AGAINST CLASS CONFIGURATION
# ============================================================

import os
import json
import tensorflow as tf


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "config",
    "class_labels.json"
)


# ------------------------------------------------------------
# EXPECTED MODEL FILES
# ------------------------------------------------------------

MODEL_FILES = {
    "plant": "crop_classifier.keras",

    "banana": "best_banana_stage2_model.keras",

    "coconut": "best_corrected_finetuned_efficientnetb3.keras",

    "coffee": "best_targeted_efficientnetb3.keras",

    "mango": "best_domain_generalization_model.keras",

    "rice": "best_stage1_efficientnetb3.keras"
}


print("=" * 80)
print("CNN CONFIGURATION ↔ MODEL VERIFICATION")
print("=" * 80)


# ------------------------------------------------------------
# CONFIG CHECK
# ------------------------------------------------------------

if not os.path.isfile(CONFIG_PATH):

    raise FileNotFoundError(
        f"\nConfiguration file not found:\n{CONFIG_PATH}"
    )


with open(
    CONFIG_PATH,
    "r",
    encoding="utf-8"
) as f:

    config = json.load(f)


print("\nConfiguration loaded:")
print(CONFIG_PATH)


# ------------------------------------------------------------
# VERIFY EACH MODEL
# ------------------------------------------------------------

all_passed = True


for crop, model_filename in MODEL_FILES.items():

    print("\n" + "-" * 80)
    print(f"MODEL: {crop.upper()}")
    print("-" * 80)


    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    if crop not in config:

        print("CONFIGURATION: FAILED")
        print(f"Missing '{crop}' section.")

        all_passed = False

        continue


    classes = config[crop].get(
        "classes"
    )

    class_to_index = config[crop].get(
        "class_to_index"
    )


    if not isinstance(classes, list):

        print("CLASSES: FAILED")

        all_passed = False

        continue


    if not isinstance(class_to_index, dict):

        print("CLASS_TO_INDEX: FAILED")

        all_passed = False

        continue


    # --------------------------------------------------------
    # CHECK CONFIG CONSISTENCY
    # --------------------------------------------------------

    config_indices = list(
        class_to_index.values()
    )

    expected_indices = list(
        range(len(classes))
    )


    if config_indices != expected_indices:

        print("CLASS INDEX ORDER: FAILED")

        print(
            "Expected:",
            expected_indices
        )

        print(
            "Found:",
            config_indices
        )

        all_passed = False

        continue


    # --------------------------------------------------------
    # CHECK REVERSE CONSISTENCY
    # --------------------------------------------------------

    reverse_ok = True


    for index, class_name in enumerate(classes):

        if class_to_index.get(class_name) != index:

            reverse_ok = False

            print(
                f"Mapping error: "
                f"{class_name} should be {index}"
            )


    if not reverse_ok:

        print("CLASS MAPPING: FAILED")

        all_passed = False

        continue


    # --------------------------------------------------------
    # MODEL PATH
    # --------------------------------------------------------

    model_path = os.path.join(
        MODELS_DIR,
        crop,
        model_filename
    )


    if not os.path.isfile(model_path):

        print("MODEL FILE: FAILED")

        print(
            f"Missing:\n{model_path}"
        )

        all_passed = False

        continue


    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    try:

        model = tf.keras.models.load_model(
            model_path,
            compile=False
        )

    except Exception as e:

        print("MODEL LOAD: FAILED")

        print(repr(e))

        all_passed = False

        continue


    # --------------------------------------------------------
    # MODEL OUTPUT COUNT
    # --------------------------------------------------------

    output_shape = model.output_shape


    if isinstance(
        output_shape,
        list
    ):

        print("OUTPUT SHAPE: FAILED")

        print(
            "Multiple outputs detected:",
            output_shape
        )

        all_passed = False

        continue


    model_classes = output_shape[-1]

    config_classes = len(classes)


    print("Model file:")
    print(model_filename)

    print("Input shape:")
    print(model.input_shape)

    print("Model output classes:")
    print(model_classes)

    print("Configured classes:")
    print(config_classes)


    if model_classes != config_classes:

        print("CLASS COUNT: FAILED")

        print(
            f"Model has {model_classes} outputs "
            f"but configuration has "
            f"{config_classes} classes."
        )

        all_passed = False

        continue


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print("\nClass mapping:")

    for index, class_name in enumerate(classes):

        print(
            f"  {index:02d} → {class_name}"
        )


    print("\nCONFIGURATION: PASSED")
    print("MODEL LOAD: PASSED")
    print("OUTPUT COUNT: PASSED")
    print("CLASS MAPPING: PASSED")


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("FINAL VERIFICATION")
print("=" * 80)


if not all_passed:

    print(
        "RESULT: FAILED"
    )

    print(
        "\nFix the reported issue before "
        "creating the inference engine."
    )

    raise RuntimeError(
        "CNN configuration verification failed."
    )


print("RESULT: PASSED")

print("\nAll six models match their class configuration.")
print("All class indices are internally consistent.")
print("No model weights were modified.")
print("No training performed.")
print("No predictions performed.")

print("\n" + "=" * 80)
print("STEP 7 COMPLETE")
print("=" * 80)
