#!/usr/bin/python
# -*- coding: utf-8 -*-
from viterbi import Viterbi
from Tkinter import *
import app as app

states = ('Healthy', 'Fever')
observations = ('normal', 'cold', 'dizzy')
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
transition_probability = {
    'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
    'Fever': {'Healthy': 0.4, 'Fever': 0.6}
}
emission_probability = {
    'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
}
#
# viterbi = Viterbi()
# viterbi.viterbi(observations,
#                 states,
#                 start_probability,
#                 transition_probability,
#                 emission_probability)

# root = Tk()

# frame = Frame(root, height=300, width=600)
# frame.pack()
#
# bottomframe = Frame(root)
# bottomframe.pack( side = BOTTOM )
#
# redbutton = Button(frame, text="Red", fg="red")
# redbutton.pack( side = LEFT)
#
# greenbutton = Button(frame, text="Brown", fg="brown")
# greenbutton.pack( side = LEFT )
#
# bluebutton = Button(frame, text="Blue", fg="blue")
# bluebutton.pack( side = LEFT )
#
# blackbutton = Button(bottomframe, text="Black", fg="black")
# blackbutton.pack( side = BOTTOM)
# root.title('HMM Algorithm')
# root.geometry("600x300")
#
# root.mainloop()
print('--------- STARTING ----------')
TITLE = 'HMM Simulator Application'
GEOMETRY = ''
setting = {
    'title': TITLE,
    'geometry': GEOMETRY
}
ap = app.Dialog(setting=setting)
# ap.title = TITLE
# ap.geometry = setting['geometry']
ap.mainloop()
print('--------- RUN SUCCESS ----------')
