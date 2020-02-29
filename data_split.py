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

def normalize(train,test):
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

path = 'data2/'

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
x_train, x_test = normalize(x_train, x_test)
y_train, y_test = normalize(y_train,y_test)



