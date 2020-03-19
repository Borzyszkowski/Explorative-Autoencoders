import os
import pandas as pd

numberWorkingDay = 253



def check(CSVPath, removedCount):
    index = CSVPath[5:-4]
    date = 'date'
    df = pd.read_csv(CSVPath)
    if(len(df)<numberWorkingDay/2):
        os.remove(CSVPath)
        removedCount+=1
        return
    return


path = 'data1/'
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
removedCount=0
for f in files:
    check(f,removedCount)
print(removedCount)