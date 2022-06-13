from audioop import avg
import datetime
import shutil
from symtable import Symbol
import uuid
from numpy import average, dtype
from pandas import DateOffset
from a_global_variables import *
import os
import csv

bigarray = [] #array to fill up with ALL the data from RESULT files
newarray = [] #array to fill up with data organized for final file
array_for_stocks = []

#load all data from RESULT files
with os.scandir('results/') as entries:
    for entry in entries:
        if entry.is_file():
            for row in csv.DictReader(open('results/' + entry.name, 'r')):
                bigarray.append(row)

with os.scandir('results/') as entries:
    for entry in entries:
        if entry.is_file():
            shutil.move('results/' + entry.name, 'results/used_delete/' + entry.name)

#populate newarray with dicts that have stock symbol and positive values from all bands from RESULT files
#rows look like this:
#{'symbol': 'ZYME', 'name': 'Zymeworks Inc. Common Shares', '0.01': '0.7808861', '0.02': '0.6352802', '0.03': '0.452474', '0.04': '0.30970192', '0.05': '0.205866', '0.06': '0.17191681', '0.07': '0.11847946', '0.08': '0.094536744', '0.09': '0.06133415', '0.1': '0.05369161', '0.2': '0.0060439776', '0.3': '0.0023302333', '0.4': '0.00077969814', '0.5': '3.201953e-08', '0.6': '9.7798356e-08', '0.7': '1.1625671e-06', '0.8': '7.8561825e-06', '1.0': '2.6723985e-05', 'maxgain': 0.7808861, 'avggain': 0.16074204308847145}
csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
with open('MASTER_SYMBOL_LIST_GOODONLY', 'r') as infile:
    for row_master in csv.DictReader(infile, dialect='piper'):
        temp_dict = {}
        temp_vals = []
        temp_dict['symbol'] = row_master['Symbol']
        temp_dict['name'] = row_master['Security Name']
        for row_results in bigarray:
            if row_results['symbol'] == temp_dict['symbol']:
                temp_dict[row_results['band']] = row_results['positive']
                temp_vals.append(float(row_results['positive']))
        if not temp_vals:
            continue
        temp_dict['maxgain'] = max(temp_vals)
        temp_dict['avggain'] = average(temp_vals)
        newarray.append(temp_dict)

#build CSV header
header_row = ['symbol', 'name', 'maxgain', 'avggain']
for item in eval_period_range:
    header_row.append(str(item))

pred_week_start = (datetime.datetime.strptime(enddate, '%Y-%m-%d') + DateOffset(3)).__format__('%Y%m%d') # enddate of learning time + 3 days

with open('results/' + pred_week_start + '_' + str(uuid.uuid4().hex) + '.csv', 'a', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=header_row)
    writer.writeheader()
    for row in newarray:
        writer.writerow(row)