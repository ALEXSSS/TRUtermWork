import sqlite3
import networkx
import readXml
from comtypes.safearray import numpy
import time
import traceback
import matplotlib.pyplot as plt

con = sqlite3.connect("firstDb.db")
cur = con.cursor()


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


if __name__ == "__main__":
    CHRG = float(readXml.retCHRG())
    isDirected = int(readXml.retIsDirected())
    print("CHRG: ",CHRG)
    if(isDirected>0):
        print("isDirected: ",True)
    else:
        print("isDirected: ",False)
    d = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\graph.npy")
    dkol = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\kol.npy")

    for i in range(len(d)):
        for j in range(len(d)):
            if (not dkol[i] == 0):
                d[i][j] = d[i][j] / (dkol[i])
                if (d[i][j] > 1):
                    print("! ", d[i][j], " ", dkol[i], dkol[j])

    for i in range(len(d)):
        for j in range(len(d)):
            if (d[i][j] < CHRG): d[i][j] = 0
    # numpy.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\newgr", d)
    #
    # d = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\newgr.npy")
    if (isDirected > 0):
        G = networkx.DiGraph()
    else:
        G = networkx.Graph()
    for i in range(len(d)):
        for j in range(len(d)):
            if (d[i][j] > 0):
                G.add_edge(i, j)

    print("Run!")
    print("Rules: ")
    cursorNames = con.execute(
        "SELECT distinct ClassCode81,ClassName81 from " +
        "info_class81")
    dictNames = {}
    dictRevClasses = {}
    for a in cursorNames:
        dictNames[a[0]] = [a[1]]
    dc = createDictOfClasses()
    for a in dc:
        dictRevClasses[dc[a]] = dictNames[a]

    A = networkx.simple_cycles(G)
    f = open('rules.txt', 'w')
    als = list(A)
    for ls in als:
        print("[", end="")
        f.write("[")
        for node in ls:
            print(dictRevClasses[node], end=" ")
            f.write(str(dictRevClasses[node]))
        print("]")
        f.write("]")
        f.write("\n")


