#!/usr/bin/python
# -*- coding: utf-8 -*-
from viterbi import Viterbi
from Tkinter import *
import app as app
import ConfigParser
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='Main: %(message)s')

# states = ('Healthy', 'Fever')
# observations = ('normal', 'cold', 'dizzy')
# start_probability = {'Healthy': 0.6, 'Fever': 0.4}
# transition_probability = {
#     'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
#     'Fever': {'Healthy': 0.4, 'Fever': 0.6}
# }
# emission_probability = {
#     'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
#     'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
# }
states = ('Price_up', 'Price_keep', 'Price_down')
observations = ['DS_increase']
start_probability = {'Price_up': 0.33, 'Price_keep': 0.26, 'Price_down': 0.41}
transition_probability = {
    'Price_up': {'Price_up': 0.2, 'Price_keep': 0.3, 'Price_down': 0.5},
    'Price_keep': {'Price_up': 0.3, 'Price_keep': 0.3, 'Price_down': 0.4},
    'Price_down': {'Price_up': 0.3, 'Price_keep': 0.4, 'Price_down': 0.3}
}
emission_probability = {
    'Price_up': {'DS_increase': 0.43, 'DS_decrease': 0.57},
    'Price_keep': {'DS_increase': 0.5, 'DS_decrease': 0.5},
    'Price_down': {'DS_increase': 0.65, 'DS_decrease': 0.35}
}

logging.debug('----------- STARTED ------------')
TITLE = 'HMM Simulator Application'
GEOMETRY = ''

# ---- variable -----
old_status = 'Price_up'
old_prob = 0.40
old_DS = 100
new_DS = 90
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

# ap = app.Dialog(setting=_setting, data=_data)
# ap.mainloop()
config = ConfigParser.ConfigParser()
config.read('setting.cfg')

logging.debug('--------- RUN SUCCESS ----------')
