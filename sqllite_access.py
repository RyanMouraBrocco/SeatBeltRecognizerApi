import sqlite3
from sqlite3 import Error
from classes.user import User
from classes.child import Child


def createConnection(dbFile):
    return sqlite3.connect(dbFile)


def createIfNotDatabase():
    return createConnection("data/tccdatabase.db")


def createUserTable(conn):
    createCityTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS User 
    (
        Id integer AUTOINCREMENT PRIMARY KEY, 
        Name text not null, 
        Email text not null, 
        Password text not null, 
        CityId integer not null
    );
    """)


def createCityTable(conn):
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS City 
    (
        Id integer AUTOINCREMENT PRIMARY KEY, 
        Name text not null
    );
    """)


def createChildTable(conn):
    createUserTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS Child 
    (
        Id integer AUTOINCREMENT PRIMARY KEY, 
        Name text not null,
        UserId integer not null
    );
    """)


def insertUser(conn, user):
    data = [user.name, user.email, user.password, user.cityId]
    conn.execute(
        "INSERT User (Name, Email, Password, CityId) VALUES (?, ?, ?, ?);", data)


def getUserById(conn, userId):
    cursor = conn.execute(
        "SELECT Id, Name, Email, Password, CityId FROM User WHERE Id = ?", [userId])
    user = None
    for row in cursor:
        user = User(row[0], row[1], row[2], row[3], row[4])

    return user


def insertChild(conn, child):
    data = [child.name, child.userId]
    conn.execute("INSERT Child (Name, UserId) VALUES (?, ?);", data)


def getAllChildsByUserId(conn, userId):
    childs = []

    cursor = conn.execute(
        "SELECT Id, Name, UserId FROM Child WHERE UserId = ?", [userId])
    for row in cursor:
        childs.append(Child(row[0], row[1], row[2]))

    return childs
