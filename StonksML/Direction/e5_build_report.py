from lib2to3.pgen2.token import NEWLINE
import shutil
import sys
from time import sleep
from turtle import color

from numpy import average
from a_global_variables import *
from msilib.schema import Directory
import plotly.express as px
import csv
import uuid
import os
import datetime
import pandas
from pandas import DateOffset

#need to use kaleido 0.1.0post1 if current version doesnt work for writing image files

if os.path.exists('html_out/img') == False:
    os.mkdir('html_out/img')

pred_week_start = (datetime.datetime.strptime(enddate, '%Y-%m-%d') + DateOffset(3)).__format__('%Y%m%d') # enddate of learning time + 3 days

#format output filename, uses randomely generated UUID
filename = pred_week_start
filename = filename + '_'
filename = filename + uuid.uuid4().hex
filename = filename + '.html'

#make sure there is only one final CSV file, then store filename
counter = 1
with os.scandir('results/') as entries:
    for entry in entries:
        if entry.is_file():
            if counter > 1:
                sys.exit('ERROR: more than one final CSV file found')
            csv_filename = entry.name
            counter += 1

#format HTML for output file
html_top_1 = '<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link href="stylesheet.css" rel="stylesheet"><script src="sortsearch.js"></script>'
html_top_2 = '<title>' + datetime.datetime.strptime(pred_week_start, '%Y%m%d').__format__('%m%d%Y') + '</title></head>'
html_top_3 = '<body onload="sort(0, 0)"><div class="content"><div class="container"><div>'
html_top_4 = '<h2><b>' + 'Short Term Gain' + '</b></h2>'
html_top_5 = '<h2>' + datetime.datetime.strptime(pred_week_start, '%Y%m%d').__format__('%B %d, %Y') + '</h2>'
html_top_6 = '<h6>algorithm: ' + algorithm_name + '</h6></div>'
html_top_7 = '<div style="margin-top:20px"><h5></div><div style="margin-top:20px"><h5> <a href="'
html_top_8 = 'csv/' + csv_filename
html_top_9 = '"><b>here</b></a>.</div>'
html_top_10 = '<div style="margin-top:20px"><h5></h5></div>'
html_top_11 = '<div style="margin-top:60px; margin-bottom:-20px"><input type="text" id="searchbox" onkeyup="search()" placeholder="Search.."></div><div><table id="table" class="table symbol-table"><thead><tr><th onclick="sort(0, 0)" class="sortable">Symbol</th><th>Security Name</th><th onclick="sort(2, 1)" class="sortable">Max Gain Probability</th><th onclick="sort(3, 1)" class="sortable">Average Gain Probability</th><th>Predication Plot</th></tr></thead><tbody>'
#table rows will be added by loop here
html_bottom = '</tbody></table></div></div></div></body></html>'

with open('html_out/' + filename, 'a') as f:
    f.write(html_top_1)
    f.write(html_top_2)
    f.write(html_top_3)
    f.write(html_top_4)
    f.write(html_top_5)
    f.write(html_top_6)
    f.write(html_top_7)
    f.write(html_top_8)
    f.write(html_top_9)
    f.write(html_top_10)
    f.write(html_top_11)

color_list = px.colors.sequential.Plasma #colors to use for plotly
color_list.reverse()


counter = 1
dataset = list(csv.DictReader(open('results/' + csv_filename, 'r')))
total_rows = len(dataset)
for row in dataset:
    stocksymbol = row['symbol']
    stockname = row['name']
    x_arr = []
    y_arr = []
    for band in eval_period_range:
        x_arr.append(str(band))
        y_arr.append(float(row[str(band)]))

    # #for troubleshooting, speeds up run
    # if round(counter / total_rows, 5) > .03: 
    #     continue

    os.system('cls')
    print(str(round(counter / total_rows, 5)*100) + '%' + ' complete', flush=True)
    counter += 1

    #skip those that don't meet prediction_strength_selection_threshold
    if prediction_strength_selection_threshold_low < max(y_arr) < prediction_strength_selection_threshold_high:
        #dont skip those with a low/high average gain
        if prediction_average_selection_threshold_low < average(y_arr) < prediction_average_selection_threshold_high:
            continue
    
    #used for display text above bars
    y_arr_formatted = []
    for num in y_arr:
        if round(num, 3) == 1:
            temp_string = '1.0'
        elif num < .01 :
            temp_string = '.00'
        else:
            temp_string = str(round(num, 3))
            temp_string = temp_string[1 : 4 : ]
        y_arr_formatted.append(temp_string)

    data = {"Probability": y_arr, "ProabilityDisplayFormat": y_arr_formatted}
    dataframe = pandas.DataFrame(data, index=x_arr)

    fig = px.bar(   
        dataframe, 
        x=dataframe.index, 
        y="Probability", 
        labels={"index":"Percent Increase", "Probability":"Probability"}, 
        range_y=[0,1.2], 
        color="Probability",
        color_continuous_scale=color_list,
        text="ProabilityDisplayFormat",
    )   
    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    fig.update_xaxes(showgrid=True, gridcolor='#e3e3e3', showline=True, linewidth=1, linecolor='#e3e3e3')
    fig.update_yaxes(showgrid=True, gridcolor='#e3e3e3', showline=True, linewidth=1, linecolor='#e3e3e3')                
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width=500,
        height=160,
        font=dict(family="Roboto, sans-serif, verdana, arial, Open Sans", color="#848484"),
        coloraxis=dict(showscale=False),
        plot_bgcolor='rgba(0,0,0,0)',
        uniformtext_minsize=8, 
        uniformtext_mode='show'
    )
    
    #format output filename, uses randomely generated UUID
    img_filename = stocksymbol
    img_filename = img_filename + (datetime.datetime.strptime(enddate, '%Y-%m-%d') + DateOffset(3)).__format__('%Y%m%d') # enddate of learning time + 3 days
    img_filename = img_filename + '_'
    img_filename = img_filename + uuid.uuid4().hex
    img_filename = img_filename + '.jpg'

    fig.write_image('html_out/img/' + img_filename)

    highest_gain_prob = round(max(y_arr), 3)
    average_gain_prob = round(average(y_arr), 3)
    #format table row in HTML
    table_row = '<tr><td>'
    table_row = table_row + stocksymbol
    table_row = table_row + '</td><td>'
    table_row = table_row + stockname
    table_row = table_row + '</td><td>'
    table_row = table_row + str(highest_gain_prob)
    table_row = table_row + '</td><td>'
    table_row = table_row + str(average_gain_prob)
    table_row = table_row + '</td><td>'
    table_row = table_row + '<img src="img/' + img_filename + '">'
    table_row = table_row + '</td></tr>'

    with open('html_out/' + filename, 'a') as f:
        f.write(table_row)

with open('html_out/' + filename, 'a') as f:
   f.write(html_bottom)

shutil.move('results/' + csv_filename, 'html_out/csv/' + csv_filename)

os.startfile('html_out\\' + filename, 'open')