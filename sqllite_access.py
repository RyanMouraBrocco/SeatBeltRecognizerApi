import sqlite3
from sqlite3 import Error
from classes.user import User
from classes.child import Child


def createConnection(dbFile):
    return sqlite3.connect(dbFile)


def createIfNotDatabase():
    return createConnection("data/tccdatabase.db")


def closeConnection(conn):
    conn.close()


def createUserTable(conn):
    createCityTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS User 
    (
        Id integer PRIMARY KEY AUTOINCREMENT, 
        Name text not null, 
        Email text not null, 
        Password text not null, 
        CityId integer not null,
        Key text null
    );
    """)
    conn.commit()


def createCityTable(conn):
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS City 
    (
        Id integer PRIMARY KEY AUTOINCREMENT, 
        Name text not null
    );
    """)
    conn.commit()


def createChildTable(conn):
    createUserTable(conn)
    command = conn.cursor()
    command.execute("""
    CREATE TABLE IF NOT EXISTS Child 
    (
        Id integer PRIMARY KEY AUTOINCREMENT, 
        Name text not null,
        UserId integer not null,
        ImageQuantity int null 
    );
    """)
    conn.commit()


def insertUser(conn, user):
    createUserTable(conn)
    cursor=conn.cursor()
    data = [user.name, user.email, user.password, user.cityId]
    cursor.execute(
        "INSERT INTO User (Name, Email, Password, CityId) VALUES (?, ?, ?, ?);", data)
    user.id = cursor.lastrowid
    conn.commit()
    return user

def getUserById(conn, userId):
    conn.createUserTable(conn)
    cursor = conn.execute(
        "SELECT Id, Name, Email, Password, CityId FROM User WHERE Id = ?", [userId])
    user = None
    for row in cursor:
        user = User(row[0], row[1], row[2], row[3], row[4])

    return user


def getUserByEmail(conn, email):
    createUserTable(conn)
    cursor = conn.execute(
        "SELECT Id, Name, Email, Password, CityId FROM User WHERE Email = ?", [email])
    user = None
    for row in cursor:
        user = User(row[0], row[1], row[2], row[3], row[4])

    return user


def getUserByKey(conn, key):
    createUserTable(conn)
    cursor = conn.execute(
        "SELECT Id, Name, Email, Password, CityId FROM User WHERE Key = ?", [key])
    user = None
    for row in cursor:
        user = User(row[0], row[1], row[2], row[3], row[4])

    return user


def updateUserKey(conn, userId, key):
    createUserTable(conn)
    conn.execute(
        "UPDATE User SET Key = ? WHERE Id = ?", [key, userId])
    conn.commit()


def insertChild(conn, child):
    createChildTable(conn)
    data = [child.name, child.userId, child.imageQuantity]
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Child (Name, UserId, ImageQuantity) VALUES (?, ?, ?);", data)
    child.id = cursor.lastrowid
    conn.commit()
    return child

def getAllChildsByUserId(conn, userId):
    createChildTable(conn)
    childs = []

    cursor = conn.execute(
        "SELECT Id, Name, UserId, ImageQuantity FROM Child WHERE UserId = ?", [userId])
    for row in cursor:
        childs.append(Child(row[0], row[1], row[2], row[3]))

    return childs

def updateChildImageQuantity(conn, childId, imageQuantity):
    createChildTable(conn)
    conn.execute(
        "UPDATE Child SET ImageQuantity = ? WHERE Id = ?", [imageQuantity, childId])
    conn.commit()
