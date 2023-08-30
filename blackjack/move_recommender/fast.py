from fastapi import FastAPI
from blackjack.move_recommender.recommender import Hand, SCORE_TABLE
app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}


@app.post('/recommend')
def recommend(cards:dict):
    # input_d = {'dealer': [7], 'player':['A', 6]}
    activated = True
    player_cards = cards['player']
    dealer_card = SCORE_TABLE[cards['dealer'][0]]
    player_hand = Hand(player_cards)
    prediction = player_hand.recommend(dealer_card)
    return {'recommendation': prediction}
