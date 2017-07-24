import sqlite3
from random import randint
import utils
import bot


def addUser(username):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Points FROM ChattersPoints WHERE Name = :user", {"user": username})
    if cursor.fetchone() is None:
        cursor.execute("insert into ChattersPoints(Name, Points) values (:user, 0)", {"user": username})
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def addPoint(username, points):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Points FROM ChattersPoints WHERE Name = :user", {"user": username})
    a = cursor.fetchone()
    if a == None:
        addUser(username)
        connection.close()
        return False
    else:
        b = a[0] + int(points)
        cursor.execute("UPDATE ChattersPoints SET Points = ? WHERE Name = ?", (b, username))
        connection.commit()
        connection.close()
        return True


def takeawayPoint(username, points):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Points FROM ChattersPoints WHERE Name = :user", {"user": username})
    a = cursor.fetchone()
    if a[0] < int(points):
        connection.close()
        return False
    else:
        b = a[0] - int(points)
        cursor.execute("UPDATE ChattersPoints SET Points = ? WHERE Name = ?", (b, username))
        connection.commit()
        connection.close()
        return True


def countPoint(username):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Points FROM ChattersPoints WHERE Name = :user", {"user": username})
    return cursor.fetchone()


def createMSize(username):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Size FROM MSize WHERE Name = :user", {"user": username})
    size = cursor.fetchone()
    if size is None:
        rand = randint(1, 30)
        cursor.execute("insert into MSize(Name, Size) values (?, ?)", (username, rand))
        connection.commit()
        connection.close()
        return rand
    else:
        connection.close()
        return size[0]


def setMSize(username, count):
    connection = sqlite3.connect('ChattersPoints.db')
    cursor = connection.cursor()

    if int(count) == 0:
        rand = randint(1, 30)
        cursor.execute("UPDATE MSize SET Size = ? WHERE Name = ?", (rand, username))
        connection.commit()
        connection.close()
        return rand
    else:
        cursor.execute("UPDATE MSize SET Size = ? WHERE Name = ?", (int(count), username))
        connection.commit()
        connection.close()
        return int(count)