import pandas as pd
import plotly.graph_objects as go
import os
import plotly.io as pio
import matplotlib.pyplot as plt


def plotCreate(x, y, finalPath, type):
    date = 'date'
    plt.clf()
    plt.plot(x, y)
    plt.ylabel(type)
    plt.xlabel(date)
    plt.savefig(finalPath)


# type is 'open' or 'close', finalPath should be company name, it will be added first date and type
def createPredictionImages(CSVPath, type):
    if not os.path.exists("images"):
        os.mkdir("images")
    # size of predicted time
    size = 50
    # current index of
    index = CSVPath[5:-4]
    date = 'date'
    df = pd.read_csv(CSVPath)
    for i in range(int(len(df.index) / 50)):
        # first create without predicting value
        tmp = df.iloc[i * 50:int(size * 4 / 5 + i * 50) + 1]
        minValue = tmp[type][0:-1].min()
        y = tmp[type][0:-1] - minValue
        x = list(range(int(size * 4 / 5)))
        firstDate = tmp[date][i * 50]
        finalPath = 'images/' + type + index + firstDate + '.png'
        plotCreate(x, y, finalPath, type)
        # now we create plot with one more day
        y = tmp[type] - minValue
        x.append(int(size * 4 / 5))
        finalPath = 'images/' + type + index + firstDate + 'result.png'
        plotCreate(x, y, finalPath, type)


# createPredictionImages('data/PIH.csv', 'close')
path = 'data/'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

for f in files:
    createPredictionImages(f, 'open')
    createPredictionImages(f, 'close')
    print("wydrukowano obrazki dla " + f)
