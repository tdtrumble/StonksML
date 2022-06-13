from a_global_variables import startdate, enddate
import urllib.request
from datetime import datetime, timedelta
import calendar
import csv
import time
import os
import socket

enddate_inc = 1 #have to increment end date for yahoo to recognize for some reason, # of days seems to change? yahoo sucks
seconds_to_sleep = 1 #any lower than 1 second seems to cause 401 errors (auth errors because im hitting it so frequently)
connection_timeout = 20
clean_files = True
socket.setdefaulttimeout(connection_timeout)

startdate_url = str(calendar.timegm(datetime.fromisoformat(startdate).utctimetuple()))
enddate_url = str(calendar.timegm((datetime.fromisoformat(enddate) + timedelta(days=enddate_inc)).utctimetuple())) 

with open('MASTER_SYMBOL_LIST_GOODONLY', 'r') as infile:
    total_rows = len(list(infile))

badcounter = 0
time_counter = 0
with open('MASTER_SYMBOL_LIST_GOODONLY', 'r') as infile, open('MASTER_SYMBOL_LIST_GOODONLY_NEW', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['Symbol', 'Security Name'], delimiter='|')
    writer.writeheader()
    for row in csv.DictReader(infile, delimiter='|'):
        symbol = row['Symbol']
        try:
            urllib.request.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + symbol + '?period1=' + startdate_url + '&period2=' + enddate_url + '&interval=1d&events=history&includeAdjustedClose=true', filename='stock_histories/' + symbol)
            # write good lines into clean file for next run
            writer.writerow(row)
        except Exception as e:
            badcounter = badcounter + 1
            print(symbol + ': ' + format(e))
            continue
        print(str(((total_rows - time_counter)/60)) + ' minutes remaining', flush=True)
        time_counter += 1
        time.sleep(seconds_to_sleep)

# clean master files based on error count
if badcounter > 0:
    if clean_files == True:
        print('badcounter > 0, cleaning files, swapping in new clean file')
        os.remove('MASTER_SYMBOL_LIST_GOODONLY')
        os.rename('MASTER_SYMBOL_LIST_GOODONLY_NEW', 'MASTER_SYMBOL_LIST_GOODONLY')
    else:
        print('badcounter > 0, no cleaning, check master lists')   
else:
    os.remove('MASTER_SYMBOL_LIST_GOODONLY_NEW')



   

    