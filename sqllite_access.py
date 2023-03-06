import sqlite3
from sqlite3 import Error


def createConnection(dbFile):
    return sqlite3.connect(dbFile)

def createIfNotDatabase():
    return createConnection("tccdatabase.db")

def createUserTable(conn):
    createCityTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS User 
    (
        Id int PRIMARY KEY, 
        Name text not null, 
        Email text not null, 
        Password text not null, 
        CityId int not null
    )
    """)

def createCityTable(conn):
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS City 
    (
        Id int PRIMARY KEY, 
        Name text not null
    )
    """)

def createChildTable(conn):
    createUserTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS City 
    (
        Id int PRIMARY KEY, 
        Name text not null,
        UserId int not null
    )
    """)