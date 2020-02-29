import pandas as pd
import os
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
        minValue = tmp[type][0:-1].min()
        y = tmp[type][0:-1] - minValue
        firstDate = tmp[date][i * 50]
        z=y.tolist()
        if firstDate < "2018-01-01":
            x_train.append(y.tolist())
        else:
            x_test.append(y.tolist())
        y = tmp[type].iloc[-1] - minValue
        if firstDate < "2018-01-01":
            y_train.append(y)
        else:
            y_test.append(y)
    return




# createPredictionImages('data/PIH.csv', 'close')

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
    createSplit(f, 'close',x_train,x_test,y_train,y_test)
    print(" dodano " + f)
