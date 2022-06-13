from a_global_variables import *
import os
import csv

row_keep_min = 6
row_keep_max = 15

#opens files, removes header row, keeps row specified in top variables
counter = 0
row_num = 1
with os.scandir('stock_histories_clean/') as entries:
    for entry in entries:
        with open('stock_histories_clean/' + entry.name, 'r') as infile, open('test_data/' + entry.name, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            for row in csv.DictReader(infile):
                counter += 1
                if counter >= row_keep_min and counter <= row_keep_max:
                    row['Date'] = row_num #set first field to number 1-10 to match training data
                    writer.writerow(row)
                    row_num += 1
                else:
                    row_num = 1
            counter = 0