import csv, sqlite3
import os
import readXml

con = sqlite3.connect("firstDb.db")
cur = con.cursor()
PATH_WORD=""

def createcolumns(dr):
    s = "";
    j = len(dr.fieldnames)
    k = 0;
    for i in dr.fieldnames:
        k += 1
        if (k == 1):
            s += "( " + i
        else:
            if (k != j):
                s += " , " + i
            else:
                s += " , " + i + " )"
    return s


def createemptycolumns(dr):
    s = "";
    j = len(dr.fieldnames)
    k = 0;
    for i in dr.fieldnames:
        k += 1
        if (k == 1):
            s += "( " + "?"
        else:
            if (k != j):
                s += " , " + "?"
            else:
                s += " , " + "?" + " )"
    return s


def build_table(path, s):
    with open(path + "\\" + s + ".csv", 'r') as fin:  # `with` statement available in 2.5+
        dr = csv.DictReader(fin, delimiter=';')  # comma is default delimiter
        column = createcolumns(dr)
        cur.execute("CREATE TABLE " + s + " " + column)
        to_db = []
        temp = []
        for i in dr:
            temp = []
            for j in dr.fieldnames:
                temp.append(i[j])
            to_db.append(temp)
        emptyColumn = createemptycolumns(dr)
        cur.executemany("INSERT INTO " + s + " " + column + " VALUES " + emptyColumn + ";", to_db)
        con.commit()


def rambler(path):
    ls = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            ls.append(file)
    return ls


def deleteAll(listoffiles):
    for namefull in listoffiles:
        name, sep, format = namefull.partition('.')
        con.execute("Delete from " + name)
        con.execute("drop table if exists " + name)
        print("delete: "+name)


def buildallbase():
    path = PATH_WORD
    listoffiles = rambler(path)
    try:
        deleteAll(listoffiles)
    except Exception:
        print("delete is completed")
    for namefull in listoffiles:
        name, sep, format = namefull.partition('.')
        build_table(path, name)
    print("base has been built")


if __name__ == "__main__":
    print("Program is started!")
    #"C:\\Users\\Alex\\Desktop\\courseWorkFromCloud\\DataMining"
    PATH_WORD=readXml.retPathOfData()
    #PATH_WORD=sys.argv[1]
    #PATH_WORD=os.path.dirname(os.path.abspath(__file__))
    print("Current path is: ",PATH_WORD)


    print("if you have some troubles with paths, please open this file and describe explicitly path!")
    print("For example, PATH_WORD = C:\\Users\\Alex\\Desktop\\courseWorkFromCloud")
    print("Don't worry, if you have created db, all some columns in not valid, run!")
    print("This script delete all, although you can delete this the routine way!")
    print();print()
    print("Rambler start! Wait for some time!")
    buildallbase()
    print();print()
    print("DATABASE is created!")
    print("You can use others scripts")


