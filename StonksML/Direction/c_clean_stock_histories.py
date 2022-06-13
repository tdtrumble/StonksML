from a_global_variables import *
import os
import csv
import numpy as np
import shutil
                
bad_counter = 0

#error those with less than stock_history_lines_expected
with os.scandir('stock_histories/') as entries:
    for entry in entries:
        with open('stock_histories/' + entry.name) as file:
            myreader = csv.DictReader(file)
            if len(list(myreader)) < stock_history_lines_expected:
                bad_counter += 1
                file.close()
                shutil.move('stock_histories/' + entry.name, 'errors/' + entry.name)

#error those with bad array shape
with os.scandir('stock_histories/') as entries:
    for entry in entries:
        testarr = []
        testnparr = []
        try:
            with open('stock_histories/' + entry.name, newline='') as csvfile:
                data = list(csv.reader(csvfile))
                testarr.append(data)
                testnparr = np.array(testarr)
                if testnparr.shape != (1, stock_history_lines_expected + 1, 7):
                    bad_counter += 1
                    shutil.move('stock_histories/' + entry.name, 'errors/' + entry.name)
        except:
            bad_counter += 1
            shutil.move('stock_histories/' + entry.name, 'errors/' + entry.name)

#error those with nulls/non-floats in data
with os.scandir('stock_histories/') as entries:
    for entry in entries:
        testarr = []
        testnparr = []
        try:
            with open('stock_histories/' + entry.name, newline='') as csvfile:
                data = list(csv.reader(csvfile))
                testarr.append(data)
                testnparr = np.array(testarr)
                testnparr = np.delete(testnparr, 0, 1) #delete row 1
                testnparr = np.delete(testnparr, 0, 2) #delete column 1
                testnparr = testnparr.astype('float64')
        except:
            bad_counter += 1
            shutil.move('stock_histories/' + entry.name, 'errors/' + entry.name)

print('Errored ' + str(bad_counter) + ' files')

if dup_row == True:
    print('Duplicating row ' + str(row_to_dup))

#copy all clean into stock_histories_clean, add in dup row for short weeks
with os.scandir('stock_histories/') as entries:
    for entry in entries:
        counter = 2 #must initialize at 2 for row_to_dup to work correctly
        with open('stock_histories/' + entry.name, 'r') as infile, open('stock_histories_clean/' + entry.name, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            writer.writeheader()
            for row in csv.DictReader(infile):
                writer.writerow(row)
                if counter == row_to_dup:
                    if dup_row == True:
                        writer.writerow(row)
                counter += 1