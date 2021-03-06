#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import app as app
import logging

# '[%(asctime)s][%(name)-12s][%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    format='[%(asctime)s][%(name)-12s][%(levelname)s] %(message)s')

logger = logging.getLogger('{:^12s}'.format('Main'))
# states = ('Healthy', 'Fever')
# observations = ('normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal',
#                 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal')
# start_probability = {'Healthy': 0.6, 'Fever': 0.4}
# transition_probability = {
#     'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
#     'Fever': {'Healthy': 0.4, 'Fever': 0.6}
# }
# emission_probability = {
#     'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
#     'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
# }
# v = Viterbi()
# v.viterbi(observations, states, start_probability, transition_probability, emission_probability)
#
# states = ('Price_up', 'Price_keep', 'Price_down')
# observations = ['DS_increase']
# start_probability = {'Price_up': 0.33, 'Price_keep': 0.26, 'Price_down': 0.41}
# transition_probability = {
#     'Price_up': {'Price_up': 0.2, 'Price_keep': 0.3, 'Price_down': 0.5},
#     'Price_keep': {'Price_up': 0.3, 'Price_keep': 0.3, 'Price_down': 0.4},
#     'Price_down': {'Price_up': 0.3, 'Price_keep': 0.4, 'Price_down': 0.3}
# }
# emission_probability = {
#     'Price_up': {'DS_increase': 0.43, 'DS_decrease': 0.57},
#     'Price_keep': {'DS_increase': 0.5, 'DS_decrease': 0.5},
#     'Price_down': {'DS_increase': 0.65, 'DS_decrease': 0.35}
# }

# run main itself
if __name__ == '__main__':
    logger.debug('----------- STARTED ------------')
    TITLE = 'HMM Simulator Application'
    GEOMETRY = ''

    # ---- variable -----
    old_status = 'Price_keep'
    old_prob = 0.40
    old_DS = 86
    new_DS = 94
    old_CR = 30
    new_CR = 32
    old_price = 200

    # ----- setting -----
    _setting = {
        'title': TITLE,
        'geometry': GEOMETRY
    }

    _data = {
        'old_status': old_status,
        'old_prob': old_prob,
        'old_DS': old_DS,
        'new_DS': new_DS,
        'old_CR': old_CR,
        'new_CR': new_CR,
        'old_price': old_price
    }
    # main app

    ap = app.Dialog(setting=_setting, data=_data)
    ap.mainloop()

    logger.debug('--------- RUN SUCCESS ----------')
