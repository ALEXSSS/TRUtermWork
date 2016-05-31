import xmltodict

def retTables():
    with open('PARAM.xml') as fd:
        doc = xmltodict.parse(fd.read())
    givenTables=doc["PARAM"]["Tables"];
    tables=givenTables.split(",")
    return tables

def retCHRG():
    with open('PARAM.xml') as fd:
        doc = xmltodict.parse(fd.read())
    givenTables=doc["PARAM"]["CHRG"];
    return givenTables

def retIsDirected():
    with open('PARAM.xml') as fd:
        doc = xmltodict.parse(fd.read())
    givenTables=doc["PARAM"]["isDirected"];
    return givenTables

def retPathOfData():
    with open('PARAM.xml') as fd:
        doc = xmltodict.parse(fd.read())
    givenTables=doc["PARAM"]["PathOfData"];
    return givenTables





