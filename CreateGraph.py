import sqlite3

import os

from comtypes.safearray import numpy
import time
import readXml

con = sqlite3.connect("firstDb.db")
cur = con.cursor()
path=""
path1=""
searchSet=""

def getSpecifyClassByClient():
    t = time.time()
    cursorClasses = con.execute(
        "SELECT distinct RgdCode,ClassCode81 from " +
        "info_rgd_desc")
    dictClasses = {}
    for a in cursorClasses:
        dictClasses[a[0]] = a[1]
    allTables=readXml.retTables()
    cursor=[]
    for table in allTables:
        print("process of ",table)
        str="SELECT distinct CliCode, RgdCode from "+table
        cursor1 = con.execute(str)
        for i in cursor1:
            cursor.append(i)

    t1 = time.time()
    print("cursor time: ", t1 - t)
    dict = {}
    ind = 0
    ind1 = 0
    for a in cursor:
        try:
            if (True):
                c = int(a[0])
                if (c in dict):
                    dict[int(a[0])].append(dictClasses[a[1]])
                else:
                    dict[int(a[0])] = []
                    dict[int(a[0])].append(dictClasses[a[1]])
            ind1 += 1
        except Exception:
            # print("this key doesn't exist: ",a[1])
            ind += 1
            # traceback.print_exc()
    t2 = time.time()
    print("list time: ", t2 - t1)
    print("Number of errors is: ", ind)
    print("Number of operations is: ", ind1)
    return (dict, dictClasses)


def createDictOfClasses():
    dict = {}
    cursorClasses = con.execute(
        "SELECT distinct ClassCode81 from " +
        "info_class81")
    index = 0
    for a in cursorClasses:
        dict[a[0]] = index
        index += 1
    return dict


def createGraph():
    res = getSpecifyClassByClient()
    dict = res[0]
    dictClasses = res[1]
    dictNodes = createDictOfClasses()
    arr = numpy.zeros((len(dictNodes.keys()), len(dictNodes.keys())), dtype=numpy.float)
    print("//////////////////////////////////////")
    arrKol = numpy.zeros((len(dict.keys()),))
    if (True):
        for i in dict.keys():
            setRep = set()
            for j in range(len(dict[i])):
                arrKol[dictNodes[dict[i][j]]] += 1
                for k in range(j + 1, len(dict[i])):
                    if ((dictNodes[dict[i][k]], dictNodes[dict[i][j]]) in setRep):
                        continue
                    if (not dictNodes[dict[i][j]] == dictNodes[dict[i][k]]):
                        # print(dictNodes[dict[i][j]]," ",dictNodes[dict[i][k]]," ","+1")
                        arr[dictNodes[dict[i][j]]][dictNodes[dict[i][k]]] += 1
                        arr[dictNodes[dict[i][k]]][dictNodes[dict[i][j]]] += 1
                        setRep.add((dictNodes[dict[i][j]], dictNodes[dict[i][k]]))
                        setRep.add((dictNodes[dict[i][k]], dictNodes[dict[i][j]]))
    numpy.save(path, arr)
    numpy.save(path1, arrKol)



if __name__ == "__main__":
    path=os.path.dirname(os.path.abspath(__file__))+"\graph"
    path1=os.path.dirname(os.path.abspath(__file__))+"\kol"
    print("CreateGraph is started!")
    createGraph()
    print("Graph is created!")
    print("You can see two new files, they are very important for future work, don't touch them! ")
    print("kol.npy")
    print("graph.npy")
    print("Else run again!")
