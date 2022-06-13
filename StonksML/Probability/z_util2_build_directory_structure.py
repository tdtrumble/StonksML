import os

if os.path.exists('stock_histories') == False:
    os.mkdir('stock_histories')
if os.path.exists('stock_histories_clean') == False:
    os.mkdir('stock_histories_clean')
if os.path.exists('test_data') == False:
    os.mkdir('test_data')
if os.path.exists('training_positive') == False:
    os.mkdir('training_positive')
if os.path.exists('training_negative') == False:
    os.mkdir('training_negative')
if os.path.exists('errors') == False:
    os.mkdir('errors')
if os.path.exists('results') == False:
    os.mkdir('results')
if os.path.exists('results/used_delete') == False:
    os.mkdir('results/used_delete')
if os.path.exists('html_out') == False:
    os.mkdir('html_out')
if os.path.exists('html_out/img') == False:
    os.mkdir('html_out/img')
if os.path.exists('html_out/csv') == False:
    os.mkdir('html_out/csv')