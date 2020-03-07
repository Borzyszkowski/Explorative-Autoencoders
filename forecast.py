import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import numpy
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras import backend as K
import random
from pandas import DataFrame

#create plot with given x,y,path to save plot and name of ylabel

# type is 'open' or 'close', finalPath should be company name, it will be added first date and type
def createSplit(CSVPath, type,x_train,x_test,y_train,y_test):
    # size of predicted time
    size = 50
    # current index of
    index = CSVPath[5:-4]
    date = 'date'
    df = pd.read_csv(CSVPath)
    #we create plot with 40 days, one day should be predicted
    for i in range(int(len(df.index) / 50)):
        # first create without predicting value
        tmp = df.iloc[i * 50:int(size * 4 / 5 + i * 50) + 1]
        tmp.reset_index()
        y = tmp[["open" , "close"]][0:-1]
        firstDate = tmp[date][i * 50]
        if firstDate < "2018-01-01":
            x_train.append(y.values.tolist())
        else:
            x_test.append(y.values.tolist())
        y = tmp["open"].iloc[-1]
        if firstDate < "2018-01-01":
            y_train.append(y)
        else:
            y_test.append(y)
    return

def normalise_x(train, test):
    min = numpy.amin(train, axis=1)
    min = numpy.amin(min, axis=0)
    min_open = min[0]
    min_close = min[1]
    min1 = numpy.amin(test, axis=1)
    min1 = numpy.amin(min1, axis=0)
    min1_open = min1[0]
    min1_close = min1[1]
    if min1_open < min_open:
        min_open = min1_open
    if min1_close < min_close:
        min_close = min1_close
    train = train - [min_open, min_close]
    test = test - [min_open, min_close]
    max = numpy.amax(train, axis=1)
    max = numpy.amax(max, axis=0)
    max_open = max[0]
    max_close = max[1]
    max1 = numpy.amax(test, axis=1)
    max1 = numpy.amax(max1, axis=0)
    max1_open = max1[0]
    max1_close = max1[1]
    if max1_open > max_open:
        max_open = max1_open
    if max1_close > max_close:
        max_close = max1_close
    train = train / [max_open, max_close]
    test = test / [max_open, max_close]
    return train, test, min_open, max_open

def normalise_y(train, test):
    min_t = numpy.amin(train)
    min1 = numpy.amin(test)
    if min1<min_t:
        min_t=min1
    train= train-min_t
    test = test-min_t
    max_t = numpy.amax(train)
    max1 = numpy.amax(train)
    if max1>max_t:
        max_t=max1
    train = train/max_t
    test = test/max_t
    return train,test, min_t, max_t


def AutoEncoder(x_train,x_test,y_train,y_test,x_val,y_val):
    tf.random.set_seed(33)
    os.environ['PYTHONHASHSEED'] = str(33)
    numpy.random.seed(33)
    random.seed(33)

    session_conf = tf.compat.v1.ConfigProto(
        intra_op_parallelism_threads=1,
        inter_op_parallelism_threads=1
    )
    sess = tf.compat.v1.Session(
        graph=tf.compat.v1.get_default_graph(),
        config=session_conf
    )
    tf.compat.v1.keras.backend.set_session(sess)

    ### DEFINE FORECASTER ###
    inputs1 = Input(shape=(x_train.shape[1], x_train.shape[2]))
    lstm1 = LSTM(128, return_sequences=True, dropout=0.3)(inputs1, training=True)
    lstm1 = LSTM(32, return_sequences=False, dropout=0.3)(lstm1, training=True)
    dense1 = Dense(50)(lstm1)
    out1 = Dense(1)(dense1)

    model1 = Model(inputs1, out1)
    model1.compile(loss="mape", optimizer='adam', metrics=['mse'])

    ### FIT FORECASTER ###
    history = model1.fit(x_train, y_train, epochs=30, batch_size=128, verbose=2, shuffle=True)
    return model1.predict(x_test)


def metrics(df: DataFrame):
    df['y_pred_diff'] = df.last_day - df.y_pred
    df['y_true_diff'] = df.last_day - df.y_true
    df['sign_pred'] = df.y_pred_diff.apply(numpy.sign)
    df['sign_true'] = df.y_true_diff.apply(numpy.sign)
    df['is_correct'] = 0
    df.loc[df.sign_pred * df.sign_true> 0,'is_correct'] = 1
    df['result'] = df.y_true_diff * df.sign_pred

    return df

def score(df):
    scorecard = pd.Series()
    y_dif = abs(df.y_pred_diff - df.y_true_diff)
    scorecard.loc["accuracy"] = df.is_correct.sum()*100.0 / len(df.index)
    scorecard.loc["edge"] =df.result.mean()
    scorecard.loc["noise"] =numpy.mean(y_dif)
    scorecard.loc['y_true_chg'] = df.y_true.abs().mean()
    scorecard.loc['y_pred_chg'] = df.y_pred.abs().mean()
    scorecard.loc['prediction_calibration'] = scorecard.loc['y_pred_chg'] / scorecard.loc['y_true_chg']
    scorecard.loc["capture_ratio"] = scorecard.loc['edge'] / scorecard.loc['y_true_chg']*100

    return scorecard

path = 'data3/'

# content have list of csv already done
files = []
# files is list of all csv in data folder
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
x_train,x_test,y_train,y_test=[],[],[],[]
for f in files:
    createSplit(f, 'open',x_train,x_test,y_train,y_test)
    print(" dodano " + f)


x_train = numpy.array(x_train)
x_test = numpy.array(x_test)
y_train = numpy.array(y_train)
y_test = numpy.array(y_test)

x_train, x_test, min_t, max_t = normalise_x(x_train, x_test)
y_train, y_test, min_y, max_y = normalise_y(y_train,y_test)

x_val, y_val = x_train[1200:], y_train[1200:]
x_train, y_train = x_train[:1200], y_train[:1200]
y_pred = AutoEncoder(x_train,x_test,y_train,y_test, x_val, y_val)

x_test *= max_t
x_test += min_t
y_test *= max_y
y_test += min_y
y_true = y_test
y_pred *= max_y
y_pred += min_y
y_pred = y_pred.reshape((y_pred.shape[0]))

last_day = []
for i in range(x_test.shape[0]):
    last_day.append(x_test[i][x_test.shape[1]-1][0])




df = pd.DataFrame()
df['y_pred'] = y_pred
df['y_true'] = y_true
df['last_day'] = last_day

metrics(df)
print(score(df))