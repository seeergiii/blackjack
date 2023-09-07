import time
import os

from training.params import *
from training.cloud import (
    save_model_to_gcloud,
    download_model_from_gcloud,
    check_specific_model_in_bucket,
    download_nested_gcloud_folder,
)
from training.model import build_compile_model, EvaluateCOCOMetricsCallback
from training.preprocessing import (
    get_dataset,
    transform_train_dataset,
    transform_val_test_dataset,
)

# If there are starting model weights in GCloud bucket, download and store locally
# Overwrites local starting weights!
if check_specific_model_in_bucket(
    bucket_name=BUCKET_NAME, model_name="starting_model_weights.h5"
):
    download_model_from_gcloud(
        bucket_name=BUCKET_NAME,
        model_path=os.path.join(WEIGHTS_START_PATH, "starting_model_weights.h5"),
    )

# Get training data from GCloud if not yet exists locally
if not os.path.exists(os.path.join(DATA_DATA_PATH)):
    os.makedirs(os.path.join(DATA_DATA_PATH))
    download_nested_gcloud_folder(
        bucket_name=BUCKET_NAME,
        prefix="data/",
        local_folder=os.path.join(DATA_DATA_PATH),
    )

# Get tf dataset objects from data
train_source_dataset = get_dataset(TRAIN_DIR_LABELS, TRAIN_DIR_IMGS)
valid_source_dataset = get_dataset(VALID_DIR_LABELS, VALID_DIR_IMGS)
test_source_dataset = get_dataset(TEST_DIR_LABELS, TEST_DIR_IMGS)

train_ds = transform_train_dataset(train_source_dataset)
valid_ds = transform_val_test_dataset(valid_source_dataset)
test_ds = transform_val_test_dataset(test_source_dataset)

# Build and compile model
yolo_model = build_compile_model()

# If starting weights exist load into model
if os.path.exists(os.path.join(WEIGHTS_START_PATH, "starting_model_weights.h5")):
    yolo_model.load_weights(
        os.path.join(WEIGHTS_START_PATH, "starting_model_weights.h5")
    )
    print("✅ Starting model weights loaded successfully")

# Train the model
yolo_model.fit(
    train_ds,
    validation_data=valid_ds,
    epochs=100,
    callbacks=[
        EvaluateCOCOMetricsCallback(valid_ds, os.path.join(WEIGHTS_CHECKPOINTS_PATH))
    ],
    verbose=1,
)

# Save final model weights locally
timestamp = time.strftime("%Y%m%d-%H%M")
model_path = os.path.join(
    WEIGHTS_FINAL_PATH, f"{timestamp}_model_weights_final_epoch.h5"
)
yolo_model.save_weights(model_path)
print("✅ Final model saved locally")

# Save weights also to Gcloud
save_model_to_gcloud(model_path, BUCKET_NAME)
