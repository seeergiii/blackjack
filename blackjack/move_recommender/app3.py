from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import requests
import cv2

from roboflow import Roboflow
import os

url = ''
data = requests.get(url).json()


st.set_page_config(
    page_title="Card Recognition",
    page_icon=":hearts:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header("Black Jack")


def main():
    with st.sidebar:
        st.title("Navigation Bar")
        container = st.container()
        container.write("Prediction")
        if st.button('Predict'):
            #st.write(f"Next move: {data['next_move']}")
            st.write('next_move')



rf = Roboflow(api_key="qL8RDeNa21Ax9cDpCue3")
project = rf.workspace().project("playing-cards-ow27d")
model = project.version(4).model

st.title("Card Recognition")
st.write("Using Roboflow API")

frame_window = st.image([])

video = cv2.VideoCapture(0)












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
if st.button('Start'):


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
elif st.button('End'):
    cv2.destroyAllWindows()
