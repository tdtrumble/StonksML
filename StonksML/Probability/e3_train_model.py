from a_global_variables import *
import os
import csv
import numpy as np
from tensorflow.python.ops.gen_batch_ops import batch
from keras.callbacks import EarlyStopping
#suppress messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

for current_train_dir in eval_period_range:
    print('Training for ' + str(current_train_dir))
    train_data_directory = 'training_negative/' + str(current_train_dir) + '/'
    biglist = []
    labels = []
    with os.scandir(train_data_directory) as entries:
        for entry in entries:
            with open(train_data_directory + entry.name, newline='') as csvfile:
                labels.append(0)
                data = list(csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
                biglist.append(data)

    train_data_directory = 'training_positive/' + str(current_train_dir) + '/'
    with os.scandir(train_data_directory) as entries:
        for entry in entries:
            with open(train_data_directory + entry.name, newline='') as csvfile:
                labels.append(1)
                data = list(csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
                biglist.append(data)

    biglabels = np.array(labels)
    bigarray = np.array(biglist)
    bigtensor = tf.constant(bigarray)

    print('biglabels type = ' + format(biglabels.dtype))
    print('bigtensor shape = ' + format(bigtensor.shape))
    print('bigtensor type = ' + format(bigtensor.dtype))

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(10, 7)), #10 days, 7 data points
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(2)
    ])

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    es = EarlyStopping(monitor='loss', mode='min', patience=cycles_earlystop)
    model.fit(bigtensor, biglabels, epochs=cycles, callbacks=[es])

    print('model trained, processing test data...')

    test_data_directory = 'test_data/'
    biglist_test = []
    labels_test = []
    with os.scandir(test_data_directory) as entries:
        for entry in entries:
            try:
                with open(test_data_directory + entry.name, newline='') as csvfile:
                    labels_test.append(entry.name)
                    data = list(csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
                    biglist_test.append(data)
            except:
                print('error: ' + entry.name)

    bigarray_test = np.array(biglist_test)
    bigtensor_test = tf.constant(bigarray_test)

    print('labels_test length = ' + format(len(labels_test)))
    print('bigtensor_test shape = ' + format(bigtensor_test.shape))
    print('bigtensor_test type = ' + format(bigtensor_test.dtype))

    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    predictions = probability_model.predict(bigtensor_test)

    counter = 0
    f = open('results/RESULTS_' + output_filename_root + str(current_train_dir) + '.csv','w+')
    f.write('symbol,band,negative,positive\n')
    while counter <= (len(labels_test) - 1):
        txt1 = str(labels_test[counter])
        txt2 = str(current_train_dir)
        txt3 = str(predictions[counter, 0])
        txt4 = str(predictions[counter, 1])
        row = txt1 + ',' + txt2 + ',' + txt3 + ',' + txt4 + '\n'
        f.write(row)
        counter += 1
    f.close()

