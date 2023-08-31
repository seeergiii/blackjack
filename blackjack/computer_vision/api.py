from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from pathlib import Path

import numpy as np
import pandas as pd
import cv2
import io
import os

from blackjack.computer_vision.model import load_roboflow_model, predict_roboflow_model
from blackjack.computer_vision.clustering import cluster_one_player

app = FastAPI()

# Allow all requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Cache model
app.state.model = load_roboflow_model()


@app.get("/")
def index():
    return {"status": "ok"}


@app.post("/roboflow_predictions_image")
async def receive_image(img: UploadFile = File(...)):
    """
    Api endpoint, given image, returns predictions and clusters
    Returns None if there are no predictions
    """

    # Receiving and decoding the image
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # type(cv2_img) => numpy.ndarray

    # Image directory and file name
    directory = os.path.join("blackjack", "computer_vision", "temp_image")
    filename = "input.png"

    # Temporarly saves image
    cv2.imwrite(os.path.join(directory, filename), cv2_img)

    # Call roboflow model function
    predictions = predict_roboflow_model(app.state.model)

    # delete the temp image
    os.remove(os.path.join(directory, filename))

    # Check if there is prediction, return clustered pred
    if predictions is None:
        return None

    else:
        # clustered_cards = cluster_one_player(predictions)
        card_predictions_dict = predictions.to_dict("records")
        return card_predictions_dict