import shutil
from a_global_variables import *
import os
import csv
                
#delete last row, used when for some reason yahoo was duplicating fridays data, sticks old files in errors in case you need to play with cleaning routine and restore originals
with os.scandir('stock_histories/') as entries:
    for entry in entries:
        with open('stock_histories/' + entry.name, 'r') as file:
            myreader = csv.DictReader(file)
            if len(list(myreader)) > stock_history_lines_expected:
                file.close()
                with open('stock_histories/' + entry.name + '_NEW', 'w', newline='') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
                    writer.writeheader()
                    counter = 1
                    for row in csv.DictReader(open('stock_histories/' + entry.name, 'r')):
                        writer.writerow(row)
                        counter += 1
                        if counter > stock_history_lines_expected:
                            break
                file.close()
                shutil.move('stock_histories/' + entry.name, 'errors/' + entry.name)
                os.rename('stock_histories/' + entry.name + '_NEW', 'stock_histories/' + entry.name)