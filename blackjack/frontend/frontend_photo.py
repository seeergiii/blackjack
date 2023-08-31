import streamlit as st
import cv2
import requests
import os
from PIL import Image
import json
import numpy as np
import io

st.set_page_config(
    page_title="Card Recognition",
    page_icon=":hearts:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Card Recognition")
st.write("Using Roboflow API")


img_file_buffer = st.file_uploader('Upload an image')

if img_file_buffer is not None:

  col1, col2 = st.columns(2)

  with col1:
    ### Display the image user uploaded
    st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")

  with col2:
    with st.spinner("Wait for it..."):
        ### Get bytes from the file buffer
        img_bytes = img_file_buffer.getvalue()


        # API call request
        response_computer_vision = requests.post(
            "https://computervision-4egbiupfiq-ew.a.run.app/roboflow_predictions_image",
            files={"img": img_bytes},
        ).json()


        # st.write(response_computer_vision)

        dealer_hands = []
        player_hands = []

        for index, card in enumerate(response_computer_vision):
            cluster = 'dealer' if index ==0 else 'player'
            card_processed = ''.join(card['class'][:-1])

            try:
                card_processed = int(card_processed)
            except:
                pass

            if cluster == "dealer":
                st.write(card['class'])


                dealer_hands.append(card_processed)
            else:
                player_hands.append(card_processed)

        cards = {"dealer": dealer_hands, "player":player_hands}

        st.text(cards)

        response_move_recommender = requests.post(
            "https://moverecommender-7brpco5hnq-ew.a.run.app/predict_move",
            data={"cards": cards}
        ).json()

        st.write(response_move_recommender)
