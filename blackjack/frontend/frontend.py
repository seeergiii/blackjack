import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import StringIO
import requests
from move_recommender.recommender import Hand
'''
#BLACKJACK
'''


#picture = st.camera_input("Take a picture")
#
#if picture:
#    picture = st.image(picture)
#
#
#params = {'picture': picture}

#response = requests.get(url, params)
response = {'dealer': [10], 'player':[10,4]}

player_cards = response['player']
dealer_cards = response['dealer']
player_hand = Hand(player_cards)
dealer_hand = Hand(dealer_cards, dealer=True)

reccomendation = player_hand.recommend(dealer_hand)
st.write('Next move: ', reccomendation)
