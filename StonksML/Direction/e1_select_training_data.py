from a_global_variables import *
import os
import csv
import shutil
import sys

move_files = True  #if false just produce counts, if true sort files
debug = False #verbose output

learn_period_start_day = 1  #this isn't used anywhere, only learn_period_end_day used just to set initial buy price, 
                            #so its ok if learn period is short during this eval, short weeks will be fixed in clean_training_data
learn_period_end_day = 10
eval_period_start_day = 11
eval_period_end_day = 15

def test_eval_ok(test_direction):
    movement_direction = ''
    buy_price = float((stock[learn_period_end_day])['Adj Close'])
    sell_price = float((stock[eval_period_end_day])['Adj Close'])

    if (sell_price - buy_price) > 0:
        movement_direction = 'UP'
    elif (sell_price - buy_price) < 0:
        movement_direction = 'DOWN'
    else:
        movement_direction = 'ZERO'

    if test_direction == 'UP' and movement_direction == 'UP':  
         return(True)
    elif test_direction == 'UP' and movement_direction == 'DOWN':  
         return(False)
    elif test_direction == 'DOWN' and movement_direction == 'UP':  
         return(False)
    elif test_direction == 'DOWN' and movement_direction == 'DOWN':  
         return(True)
    elif movement_direction == 'ZERO':  
         return(False)
    else:    
        sys.exit("not sure what happened")


#shift variables to align with arrays starting at 0
learn_period_start_day -= 1
learn_period_end_day -= 1
eval_period_start_day -= 1
eval_period_end_day -= 1

#####
##### this only seems to be doing 1 and 2, need to add one to range for some reason????
######
for current_test in ['UP', 'DOWN']:
    count_y = 0
    count_n = 0
    count_err = 0
    list_y = []
    list_n = []
    list_err = []
    with os.scandir('stock_histories_clean/') as entries:
        for entry in entries:
            if debug == True:
                print(entry.name)
            stock = list(csv.DictReader(open('stock_histories_clean/' + entry.name)))
            try:
                if test_eval_ok(current_test):
                    count_y += 1
                    list_y.append(entry.name)
                else:
                    count_n += 1
                    list_n.append(entry.name)
            except:
                    count_err += 1
                    list_err.append(entry.name)
                    continue
    if move_files:
        print('Creating fileset for ' + str(current_test))

        destinationpath_positive = 'training_positive/' + str(current_test) + '/'
        os.makedirs(os.path.dirname(destinationpath_positive), exist_ok=True)

        destinationpath_negative = 'training_negative/' + str(current_test) + '/'
        os.makedirs(os.path.dirname(destinationpath_negative), exist_ok=True)

        for entryname in list_y:
            shutil.copyfile('stock_histories_clean/' + entryname, destinationpath_positive + entryname)
        for entryname in list_n:
            shutil.copyfile('stock_histories_clean/' + entryname, destinationpath_negative + entryname)
        for entryname in list_err:
            shutil.move('stock_histories_clean/' + entryname, 'errors/' + entryname + '_' + str(current_test)) #moving errors so when i prep testing data the garbage files arent in stock_histories
    else:
        print('negative = ' + str(count_n))
        print('yaas = ' + str(count_y))
        print('ERR OR = ' + str(count_err))
        print('printing matches')
        print(list_y)