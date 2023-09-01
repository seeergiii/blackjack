from fastapi import FastAPI
from move_recommender.recommend.recommender import Hand, SCORE_TABLE, check_winner, EX
import re
app = FastAPI()


@app.get("/")
def hello():
    return{"response":"hellow"}


@app.post("/predict_move")
def predict(input:dict):
    player_cards = [re.sub("[SCDH]", "", i) for i in input.get('player')]
    dealer_cards = [re.sub("[SCDH]", "", i) for i in input.get('dealer')]
    player_hand = Hand(player_cards)
    dealer_hand = Hand(dealer_cards)
    if len(dealer_cards) > 1:
        message = check_winner(player_hand, dealer_hand)
        return {'next_move': '', 'player_hand': '', 'dealer_hand': '', 'message': message}
    else:
        player_score = player_hand.get_score()
        if player_hand.get_score() > 21:
                rec = 'You busted!'

        elif player_hand.is_blackjack():
                rec = 'Blackjack'

        else:
            rec = EX.get(player_hand.recommend(dealer_hand))
        return {'next_move': rec, 'player_hand': player_score, 'dealer_hand': dealer_hand.get_score(), 'message': ''}
