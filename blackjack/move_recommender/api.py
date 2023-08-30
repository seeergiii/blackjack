from fastapi import FastAPI
from move_recommender.recommender import Hand, check_winner, SCORE_TABLE

app = FastAPI()





@app.get("/")
def hello():
    return{"response":"hellow"}


@app.get("/predict_move")
def predict(input):
    input_d = {'dealer': [7], 'player':[10,'A']}
    activated = True
    while activated:

        player_cards = input_d['player']
        dealer_card = SCORE_TABLE[input_d['dealer'][0]]
        player_hand = Hand(player_cards)
        print(player_hand.get_score())
        print(player_hand.recommend(dealer_card))
        if input('do you want to continue? (y/n)') == 'n':
            break
        if check_winner(player_hand, dealer_card):
            activated = False
