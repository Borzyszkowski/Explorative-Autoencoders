import pandas as pd
import os
import matplotlib.pyplot as plt

#create plot with given x,y,path to save plot and name of ylabel
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
    #we create plot with 40 days, one day should be predicted
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
progresFile='progres.txt'

with open(progresFile) as t:
    content = t.readlines()
content = [x.strip() for x in content]
#content have list of csv already done
files = []
#files is list of all csv in data folder
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

progres = open(progresFile,"a+")
for f in files:
    if not f in content:
        createPredictionImages(f, 'open')
        createPredictionImages(f, 'close')
        print("wydrukowano obrazki dla " + f)
        progres = open(progresFile, "a+")
        progres.write(f + '\n')
        progres.close()
    else:
        print(f + "juz stworzone")