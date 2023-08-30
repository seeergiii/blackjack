import pandas as pd
import numpy as np

deals_hard = np.array([
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

deals_soft = np.array([
    ['H']*3 + ['Dh']*2 + ['H']*5,
    ['H']*3 + ['Dh']*2 + ['H']*5,
    ['H']*2 + ['Dh']*3 + ['H']*5,
    ['H']*2 + ['Dh']*3 + ['H']*5,
    ['H'] + ['Dh']*4 + ['H']*5,
    ['S'] + ['Ds']*4 + ['S']*2 + ['H']*3,
    ['S']*10
])



hard = pd.DataFrame(deals_hard, index=[8, 9, 10, 11, 12, 13, 14,15, 16, 17], columns=(2,3,4,5,6,7,8,9,10,'A'))

soft = pd.DataFrame(deals_soft, index=[13, 14, 15, 16, 17, 18, 19], columns=(2,3,4,5,6,7,8,9,10,'A'))
