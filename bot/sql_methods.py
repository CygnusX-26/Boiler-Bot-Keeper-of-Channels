import sqlite3

db_path = 'channels.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()


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

def getAllChannels() -> list:
    c.execute(
        f"SELECT * FROM channels")
    return c.fetchall()

def removeChannel(id:int) -> None:
    with conn:
        c.execute(f"DELETE from channels WHERE id = ?", (id,))
    
def insertChannel(name:str, id:int, current:int) -> None:
    with conn:
        c.execute(f"INSERT INTO channels VALUES (?, ?, ?)", (name, id, current))