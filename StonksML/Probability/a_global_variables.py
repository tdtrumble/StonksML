#-------------INPUTS------------
startdate = '2022-02-21'
enddate = '2022-03-11'
stock_history_lines_expected = 14
dup_row = True #True = duplicate a row in stock histories when weeks are short
row_to_dup = 2 #this is the row to duplicate, use actual file row numbers (so first day will be a 2)
#-------------INPUTS------------













eval_period_range = [.01, .02, .03, .04, .05, .06, .07, .08, .09, .10, .20, .30, .40, .50, .60, .70, .80, 1.00]

#controls for training
output_filename_root = startdate + '_' + enddate + '_'
cycles = 300 #num of epochs to train
cycles_earlystop = 80 #num of cycles to stop if loss is consistent

#controls for final HTML
algorithm_name = 'canary.1w.' + str(cycles) + '.' + str(cycles_earlystop)
prediction_strength_selection_threshold_high = .90
prediction_strength_selection_threshold_low = .001
prediction_average_selection_threshold_high = .35
prediction_average_selection_threshold_low = .001