# ============================================================
# STEP 2 — VERIFY ALL TRAINED KERAS MODELS
# ============================================================

import os
import tensorflow as tf

PROJECT_ROOT = os.getcwd()

CNN_MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "backend",
    "cnn",
    "models"
)

print("=" * 80)
print("CNN MODEL VERIFICATION")
print("=" * 80)

print("\nProject root:")
print(PROJECT_ROOT)

print("\nModels directory:")
print(CNN_MODELS_DIR)

if not os.path.isdir(CNN_MODELS_DIR):
    raise FileNotFoundError(
        f"Models directory not found:\n{CNN_MODELS_DIR}"
    )

# ------------------------------------------------------------
# FIND ALL KERAS MODELS
# ------------------------------------------------------------

keras_files = []

for root, dirs, files in os.walk(CNN_MODELS_DIR):

    for file in files:

        if file.lower().endswith(".keras"):

            keras_files.append(
                os.path.join(root, file)
            )

keras_files = sorted(keras_files)

print("\nKeras models found:", len(keras_files))

if len(keras_files) == 0:
    raise FileNotFoundError(
        "No .keras files found inside backend/cnn/models"
    )

print()

for i, path in enumerate(keras_files, 1):
    print(f"{i:02d} | {path}")

# ------------------------------------------------------------
# LOAD AND INSPECT
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("MODEL INSPECTION")
print("=" * 80)

for index, model_path in enumerate(keras_files, 1):

    print("\n" + "-" * 80)
    print(f"MODEL {index}")
    print("-" * 80)

    print("Path:")
    print(model_path)

    try:

        model = tf.keras.models.load_model(
            model_path,
            compile=False
        )

        print("\nLOAD: PASSED")

        print("Model name:")
        print(model.name)

        print("Input shape:")
        print(model.input_shape)

        print("Output shape:")
        print(model.output_shape)

        print("Number of parameters:")
        print(f"{model.count_params():,}")

        print("Number of layers:")
        print(len(model.layers))

        # ----------------------------------------------------
        # INPUT DETAILS
        # ----------------------------------------------------

        if isinstance(model.input_shape, list):

            print("Multiple inputs: YES")

        else:

            print("Multiple inputs: NO")

        # ----------------------------------------------------
        # OUTPUT DETAILS
        # ----------------------------------------------------

        if isinstance(model.output_shape, list):

            print("Multiple outputs: YES")

        else:

            print("Multiple outputs: NO")

        print("\nSTATUS: VERIFIED")

    except Exception as e:

        print("\nSTATUS: FAILED")

        print("Error:")
        print(repr(e))

print("\n" + "=" * 80)
print("STEP 2 COMPLETE")
print("=" * 80)

print("\nNo model weights were modified.")
print("No training performed.")
print("No fine-tuning performed.")
print("No predictions performed.")