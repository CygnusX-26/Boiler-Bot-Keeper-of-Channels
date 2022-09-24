import sqlite3

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

db_path2 = 'users.db'
conn2 = sqlite3.connect(db_path2)
c2 = conn2.cursor()


def getChannel(name:str) -> list:
    c.execute(
        f"SELECT * FROM channels WHERE name = ?", (name,))
    return c.fetchone()

def updateChannel(name:str, id:int, inc:int) -> None:
    c.execute(f"SELECT * FROM channels WHERE id = ?", (id,))
    temp = c.fetchone()[2]
    with conn:
        c.execute(f"""UPDATE channels SET usercount = {temp + inc}
                WHERE name = ? AND id = ?
                """, (name, id))

def getUserCount(id:int):
    c.execute(f"SELECT * FROM channels WHERE id = ?", (id,))
    return c.fetchone()[2]

def getOwner(id:int) -> int:
    c.execute(f"SELECT * FROM channels")
    return c.fetchone()[3]

def getAllChannels() -> list:
    c.execute(
        f"SELECT * FROM channels")
    return c.fetchall()

def removeChannel(id:int) -> None:
    with conn:
        c.execute(f"DELETE from channels WHERE id = ?", (id,))
    
def insertChannel(name:str, id:int, current:int, owner:int) -> None:
    with conn:
        c.execute(f"INSERT INTO channels VALUES (?, ?, ?, ?)", (name, id, current, owner))

def insertUser(id:int, name:str) -> None:
    with conn2:
        c2.execute(f"INSERT INTO users VALUES (?, ?, ?)", (id, name, 0))

def getUser(id:int):
    c2.execute(
        f"SELECT * FROM users WHERE id = ?", (id,))
    return c2.fetchone()

def updateUser(id:int, num:int) -> None:
    c2.execute(f"SELECT * FROM users WHERE id = ?", (id,))
    temp = c2.fetchone()[2]
    with conn2:
        c2.execute(f"""UPDATE users SET channel = {temp + num}
                WHERE id = ?
                """, (id,))