import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import numpy
import matplotlib.pyplot as plt

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
    max1_open = max[0]
    max1_close = max[1]
    if max1_open > max_open:
        max_open = max1_open
    if max1_close > max_close:
        max_close = max1_close
    train = train / [max_open, max_close]
    test = test / [max_open, max_close]
    return train, test

def normalise_y(train, test):
    min = numpy.amin(train)
    min1 = numpy.amin(test)
    if min1<min:
        min=min1
    train= train-min
    test = test-min
    max = numpy.amax(train)
    max1 = numpy.amax(train)
    if max1>max:
        max=max1
    train = train/max
    test = test/max
    return train,test


path = 'data/'

#content have list of csv already done
files = []
#files is list of all csv in data folder
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

x_train, x_test = normalise_x(x_train, x_test)
y_train, y_test = normalise_y(y_train,y_test)