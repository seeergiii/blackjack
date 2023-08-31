import streamlit as st
from PIL import Image
import requests
import os
import cv2

from roboflow import Roboflow
from io import StringIO

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

        with st.sidebar:
            st.title("Hellow")
            container = st.container()
            container.write("Prediction")

            st.write(f"Next move: {data['next_move']}")
            st.write(f"Player score: {data['player_hand']}")
            st.write(f"Dealer card: {data['dealer_hand']}")
            st.toast(f"{data['message']}", icon=':coffee:')





        rf = Roboflow(api_key="qL8RDeNa21Ax9cDpCue3")
        project = rf.workspace().project("playing-cards-ow27d")
        model = project.version(4).model

        st.header("Card Recognition")


        frame_window = st.image([])

        video = cv2.VideoCapture(0)




        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            ret, frame = video.read()
            # To read file as bytes:
            success, encoded_image = cv2.imencode(".png", frame)
            rame_bytes = encoded_image.tobytes()
​
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
​
    # API call request
            response = requests.post(
            "http://127.0.0.1:8000/roboflow_predictions_image",  # TODO change when deployed
            files={"img": rame_bytes},
    )       .json()

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.write(stringio)



        def infer(img):
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

            return img


        ROBOFLOW_SIZE = 416



        while True:
            ret, frame = video.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame_with_boxes = infer(frame)

            height, width, channels = frame_with_boxes.shape
            frame_with_boxes = cv2.resize(frame_with_boxes, (width * 2, height * 2))

            frame_window.image(frame_with_boxes)

            # Stop the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release resources when finished
            video.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
