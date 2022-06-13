import shutil
import os

if os.path.exists('stock_histories') == True:
    shutil.rmtree('stock_histories')
if os.path.exists('stock_histories_clean') == True:
    shutil.rmtree('stock_histories_clean')
if os.path.exists('test_data') == True:
    shutil.rmtree('test_data')
if os.path.exists('training_positive') == True:
    shutil.rmtree('training_positive')
if os.path.exists('training_negative') == True:
    shutil.rmtree('training_negative')
if os.path.exists('errors') == True:
    shutil.rmtree('errors')
if os.path.exists('results') == True:
    shutil.rmtree('results')