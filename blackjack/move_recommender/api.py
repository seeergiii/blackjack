from fastapi import FastAPI
from move_recommender.recommender import Hand

app = FastAPI()

@app.get("/")
def hello():
    return{"response":"hellow"}


@app.get("/predict_move")
def predict(input):
    input = {'dealer': [7], 'player':['A', 6]}


    player_cards = input['player']
    dealer_cards = input['dealer']
    player_hand = Hand(player_cards)
    dealer_hand = Hand(dealer_cards, dealer=True)
    response = player_hand.recommend(dealer_hand)
    return {'next_move': response}
