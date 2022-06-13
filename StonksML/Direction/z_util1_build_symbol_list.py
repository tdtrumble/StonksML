import urllib.request
import csv
import os

# grab files
urllib.request.urlretrieve('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt', 'MASTER_SYMBOL_LIST_TEMP1')
urllib.request.urlretrieve('ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt', 'MASTER_SYMBOL_LIST_TEMP2')

# clean and combine files
with open('MASTER_SYMBOL_LIST_TEMP1', 'r') as infile, open('MASTER_SYMBOL_LIST_TEMP3', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['Symbol', 'Security Name', 'ETF', 'Test Issue'], delimiter='|', extrasaction='ignore')
    writer.writeheader()
    for row in csv.DictReader(infile, delimiter='|'):
        if row['ETF'] == 'N' and row['Test Issue'] == 'N':
            writer.writerow(row)
with open('MASTER_SYMBOL_LIST_TEMP2', 'r') as infile, open('MASTER_SYMBOL_LIST_TEMP3', 'a', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['NASDAQ Symbol', 'Security Name', 'ETF', 'Test Issue'], delimiter='|', extrasaction='ignore')
    for row in csv.DictReader(infile, delimiter='|'):
        if row['ETF'] == 'N' and row['Test Issue'] == 'N':
            writer.writerow(row)

# strip out etf and test columns
with open('MASTER_SYMBOL_LIST_TEMP3', 'r') as infile, open('MASTER_SYMBOL_LIST_GOODONLY', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['Symbol', 'Security Name'], delimiter='|', extrasaction='ignore')
    writer.writeheader()
    for row in csv.DictReader(infile, delimiter='|'):
        writer.writerow(row)

# clean temp files
os.remove('MASTER_SYMBOL_LIST_TEMP1')
os.remove('MASTER_SYMBOL_LIST_TEMP2')
os.remove('MASTER_SYMBOL_LIST_TEMP3')

