from a_global_variables import *
import os
import csv
import shutil
import sys

learn_period_start_day = 1  #this isn't used anywhere, only learn_period_end_day used just to set initial buy price, 
                            #so its ok if learn period is short during this eval, short weeks will be fixed in clean_training_data
learn_period_end_day = 10
eval_period_start_day = 11
eval_period_end_day = 15

learn_period_start_day -= 1
learn_period_end_day -= 1
eval_period_start_day -= 1
eval_period_end_day -= 1

with os.scandir('training_negative/UP/') as entries:
    for entry in entries:
        stock = list(csv.DictReader(open('training_negative/UP/' + entry.name)))
        movement_direction = ''
        buy_price = float((stock[learn_period_end_day])['Adj Close'])
        sell_price = float((stock[eval_period_end_day])['Adj Close'])

        if (sell_price - buy_price) > 0:
            movement_direction = 'UP'
        elif (sell_price - buy_price) < 0:
            movement_direction = 'DOWN'
        else:
            movement_direction = 'ZERO'

        print(movement_direction, end='.')