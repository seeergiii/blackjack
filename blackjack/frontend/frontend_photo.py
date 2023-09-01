
import streamlit as st
from PIL import Image
import requests
import os
import cv2

from roboflow import Roboflow
from io import StringIO

pre_url = 'https://recommend-okumlrfyiq-ew.a.run.app/predict_move'

img_url ='https://computervision-4egbiupfiq-ew.a.run.app/receive_image_roboflow_predictions_image_post'

""" def infer(img):
            # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
            # height, width, channels = img.shape
            # scale = ROBOFLOW_SIZE / max(height, width)
            # resized_img = cv2.resize(img, (round(scale * width), round(scale * height)))

            resized_img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            cv2.imwrite("temp.jpg", resized_img_rgb)

            prediction = model.predict("temp.jpg", confidence=40, overlap=30).json()
            print(prediction)

            os.remove("temp.jpg")

            # Draw boxes on the original frame
            for pred in prediction["predictions"]:
                x, y, width, height = pred["x"], pred["y"], pred["width"], pred["height"]
                cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 20), 9)
                cv2.putText(img, 'you won', (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, 2)

            return img """
def main():

        st.set_page_config(
            page_title="Card Recognition",
            page_icon=":hearts:",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.title("Black Jack :black_joker: :money_with_wings: :pizza: :whale:")

        st.sidebar.title("Hellow")

        st.sitebar.write("Prediction")







        img_file_buffer = st.file_uploader('Upload an image')


        if img_file_buffer is not None:

            col1, col2 = st.columns(2)

            with col1:
                ### Display the image user uploaded
                resized_img_rgb = cv2.cvtColor(img_file_buffer, cv2.COLOR_BGR2RGB)
                st.image(Image.open(resized_img_rgb), caption="Here's the image you uploaded ☝️")

            with col2:
                with st.spinner("Wait for it..."):
                    ### Get bytes from the file buffer
                    img_bytes = img_file_buffer.getvalue()


                    # API call request
                    response_computer_vision = requests.post(
                        "https://computervision-4egbiupfiq-ew.a.run.app/roboflow_predictions_image",
                        files={"img": img_bytes},
                    ).json()

                    for pred in response_computer_vision:
                        x, y, width, height = pred["x"], pred["y"], pred["width"], pred["height"]
                        cv2.rectangle(resized_img_rgb, (x, y), (x + width, y + height), (0, 255, 20), 9)
                        cv2.putText(resized_img_rgb, pred["class"], (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, 2)
                    st.image(resized_img_rgb, use_column_width=True,clamp = True)

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

                    data = requests.post(
                        "https://moverecommender-7brpco5hnq-ew.a.run.app/predict_move",
                        input={"input": cards}
                    ).json()



                    data = requests.post(pre_url, input={"cards": cards}).json()
                    st.write(f"Next move: {data['next_move']}")
                    st.write(f"Player score: {data['player_hand']}")
                    st.write(f"Dealer card: {data['dealer_hand']}")
                    st.toast(f"{data['message']}", icon=':coffee:')

if __name__ == '__main__':
    main()
