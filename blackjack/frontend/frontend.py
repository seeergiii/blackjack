import streamlit as st
import cv2
import requests
import os
import cv2

from roboflow import Roboflow
from io import StringIO
import numpy as np
import io

pre_url = 'https://recommend-okumlrfyiq-ew.a.run.app/predict_move'
data = requests.get(pre_url)
img_pro ='https://computervision-4egbiupfiq-ew.a.run.app/docs#/default/receive_image_roboflow_predictions_image_post'
def main():

        st.set_page_config(
            page_title="Card Recognition",
            page_icon=":hearts:",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.title("Black Jack :black_joker: :money_with_wings: :pizza: :whale:")





        frame_window = st.image([])
        video = cv2.VideoCapture(0)



        st.header("Card Recognition")

        with st.sidebar:
                st.title("Hellow")
                container = st.container()
                container.write("Prediction")

                st.write(f"Next move: {data['next_move']}")
                st.write(f"Player score: {data['player_hand']}")
                st.write(f"Dealer card: {data['dealer_hand']}")
                st.toast(f"{data['message']}", icon=':coffee:')






        while True:
            ret, frame = video.read()
            # Resize the frame
            # resized_frame = cv2.resize(frame, (ROBOFLOW_SIZE, ROBOFLOW_SIZE))
            # cv2_img = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # type(cv2_img) => numpy.ndarray
            # st.write("Type", type(cv2_img))
            success, encoded_image = cv2.imencode(".png", frame)
            frame_bytes = encoded_image.tobytes()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # API call request
            response_computer_vision = requests.post(
                "https://computervision-4egbiupfiq-ew.a.run.app/roboflow_predictions_image",  # TODO change when deployed
                files={"img": frame_bytes},
            ).json()


            # if there is no response continue with next iteration
            if response_computer_vision is None:
                height, width, channels = frame.shape
                frame = cv2.resize(frame, (width * 2, height * 2))
                frame_window.image(frame)
                continue



            # Draw boxes on the original frame
            for pred in response_computer_vision:
                x, y, width, height = (
                    pred["x"],
                    pred["y"],
                    pred["width"],
                    pred["height"],
                )  # TODO predictions shouls also return ==> pred["width"], pred["height"]
                cv2.rectangle(
                    frame, (x, y), (x - width, y - height), (0, 255, 0), 2
                )  # TODO replace 50 to width and height

                height, width, channels = frame.shape
                frame = cv2.resize(frame, (width * 2, height * 2))





                frame_window.image(frame)

            st.write(response_computer_vision)

            dealer_hands = []
            player_hands = []

            for card in response_computer_vision:
                if card['cluster'] == "dealer":
                    dealer_hands.append(card)
                else:
                    player_hands.append(card)



            cards = {"dealer": dealer_hands, "player":player_hands}

            data = requests.post(
                "https://moverecommender-7brpco5hnq-ew.a.run.app/predict_move",  # TODO change when deployed
                data={"cards": cards}
            ).json()



if __name__ == '__main__':
    main()
