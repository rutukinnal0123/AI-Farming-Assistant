import os
import tensorflow as tf


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


print("=" * 80)
print("CNN MODEL CLASS MAPPING INSPECTION")
print("=" * 80)


for crop in sorted(
    os.listdir(MODELS_DIR)
):

    crop_dir = os.path.join(
        MODELS_DIR,
        crop
    )

    if not os.path.isdir(crop_dir):
        continue


    keras_files = [

        f

        for f in os.listdir(crop_dir)

        if f.lower().endswith(
            ".keras"
        )

    ]


    if not keras_files:
        continue


    model_path = os.path.join(
        crop_dir,
        keras_files[0]
    )


    print("\n" + "-" * 80)
    print("CROP:", crop)
    print("MODEL:", keras_files[0])
    print("-" * 80)


    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )


    print(
        "Input shape:",
        model.input_shape
    )

    print(
        "Output shape:",
        model.output_shape
    )


    # --------------------------------------------------------
    # SEARCH MODEL CONFIGURATION FOR CLASS INFORMATION
    # --------------------------------------------------------

    found = False


    # Some training pipelines store class information
    # in model attributes.

    possible_attributes = [

        "class_names",
        "classes",
        "class_indices",
        "label_names"

    ]


    for attribute in possible_attributes:

        if hasattr(
            model,
            attribute
        ):

            value = getattr(
                model,
                attribute
            )

            print(
                f"{attribute}:",
                value
            )

            found = True


    if not found:

        print(
            "No class mapping stored directly "
            "inside the Keras model."
        )


print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)
