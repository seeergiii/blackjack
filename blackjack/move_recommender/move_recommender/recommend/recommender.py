import pandas as pd
import numpy as np

DH = np.array([
    ['H']*10,
    ['H']+['Dh']*4 + ['H']*5,
    ['Dn']*8 + ['H']*2,
    ['Dn']*9 + ['H'],
    ['H']*2 + ['S']*3 + ['H']*5,
    ['S']*5 + ['H']*5,
    ['S']*5 + ['H']*5,
    ['S']*5 + ['H']*3 + ['Rh'] + ['H'],
    ['S']*5 + ['H']*2 + ['Rh']*3,
    ['S']*10
])

DS = np.array([
    ['H']*3 + ['Dh']*2 + ['H']*5,
    ['H']*3 + ['Dh']*2 + ['H']*5,
    ['H']*2 + ['Dh']*3 + ['H']*5,
    ['H']*2 + ['Dh']*3 + ['H']*5,
    ['H'] + ['Dh']*4 + ['H']*5,
    ['S'] + ['Ds']*4 + ['S']*2 + ['H']*3,
    ['S']*10
])
HARD = pd.DataFrame(DH, index=[8, 9, 10, 11, 12, 13, 14, 15, 16, 17], columns=(2,3,4,5,6,7,8,9,10,"A"))
SOFT = pd.DataFrame(DS, index=[13, 14, 15, 16, 17, 18, 19], columns=(2,3,4,5,6,7,8,9,10,"A"))



SCORE_TABLE = {"A":11, "J":10, "K":10, "Q":10, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10}



class Hand():
    def __init__(self, cards:list, score:int=None, state:str=None, dealer=False)->None: #cards is list of cards [2,10] ['J','K']
        self.state = state
        self.cards = cards
        self.score = score
        if self.cards == ["A", "A"]:
            self.score = 12

        else:
            self.score = sum([SCORE_TABLE[i] for i in self.cards])

        if "A" in self.cards:
            self.state = 'soft'
        else:
            self.state = 'hard'





    def is_blackjack(self):
        if self.score == 21:
            return True


    def recommend(self, dealer):# dealer is dealer hand 'J', 'K', 10, 8,...
        if self.state == 'hard':
            table = HARD
            if self.score <= 8:
                score = 8
            elif self.score >= 17:
                score = 17
            else:
                score = self.score
        else:
            table = SOFT
            if self.score <= 13:
                score = 13
            elif self.score >= 19:
                score = 19
            else:
                score = self.score

        response = table.loc[score,dealer]
        print(score)
        return response


    def get_score(self):
        return self.score








if __name__ == '__main__':
    input_d = {'dealer': [7], 'player':[10,'A']}
    activated = True
    player_hand = None
    while activated:

        player_cards = input_d['player']
        dealer_card = SCORE_TABLE[input_d['dealer'][0]]
        player_hand = Hand(player_cards)
        if player_hand.get_score() > 21:
            print('You busted!')
            activated = False
        elif player_hand.is_blackjack():
            print('Blackjack')
            activated = False

        else:
            print(player_hand.recommend(dealer_card))

        if input('do you want to continue? (y/n)') == 'n':
            break
