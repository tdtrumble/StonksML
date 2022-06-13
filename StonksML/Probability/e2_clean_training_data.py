#takes the cleaned and sorted stock histories and cuts everything but the first X days to use for training on positive/negative

import os
import csv

#opens files, removes header row
counter = 0
for root, dirs, files in os.walk('training_positive/'):
    for name in files:
        with open(root + '/' + name, 'r') as infile, open(root + '/t_' + name, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            for row in csv.DictReader(infile):
                counter += 1
                if counter <= 10:
                    row['Date'] = counter
                    writer.writerow(row)
                else:
                    break
            counter = 0
        os.remove(root + '/' + name)
        os.rename(root + '/t_' + name, root + '/' + name)
        print('.', end='', flush=True)

#opens files, removes header row    
counter = 0
for root, dirs, files in os.walk('training_negative/'):
    for name in files:
        with open(root + '/' + name, 'r') as infile, open(root + '/t_' + name, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            for row in csv.DictReader(infile):
                counter += 1
                if counter <= 10:
                    row['Date'] = counter
                    writer.writerow(row)
                else:
                    break
            counter = 0
        os.remove(root + '/' + name)
        os.rename(root + '/t_' + name, root + '/' + name)
        print('.', end='', flush=True)