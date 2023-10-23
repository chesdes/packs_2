import sqlite3 as sq
import json

class DB:
    def __init__(self):
        self.conn = sq.connect(r"app\db\main.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        auth INTEGER,
                        balance INT DEFAULT 100000,
                        packs_open INT DEFAULT 0,
                        inventory TEXT DEFAULT '[]',
                        packs TEXT DEFAULT '[]',
                        gifts TEXT DEFAULT '[]',
                        packs_max INT DEFAULT 25,
                        players_max INT DEFAULT 200,
                        rang INT DEFAULT 0
                        )""")
        self.conn.commit()
    
    async def getUsersAuthsList(self):
        return self.cur.execute("SELECT auth FROM users").fetchall()[0]
    
    async def getUser(self, auth:int):
        user = self.cur.execute(f"SELECT * FROM users WHERE auth={auth}").fetchone()
        if user != None:
            user = list(user)
            user[6] = json.loads(user[6])
            user[5] = json.loads(user[5])
            user[4] = json.loads(user[4])
        return user
    
    async def addUser(self, auth: int):
        self.cur.execute(f"INSERT INTO users(auth) VALUES ({auth})")
        self.conn.commit()
    
    async def setPacks(self, auth: int, packs):
        packs_str = json.dumps(packs)
        self.cur.execute(f"UPDATE users SET packs='{packs_str}' WHERE auth={auth}")
        self.conn.commit()
        
    async def setGifts(self, auth: int, gifts):
        gifts_str = json.dumps(gifts)
        self.cur.execute(f"UPDATE users SET gifts='{gifts_str}' WHERE auth={auth}")
        self.conn.commit()
        
    async def setInventory(self, auth: int, inventory):
        inventory_str = json.dumps(inventory)
        self.cur.execute(f"UPDATE users SET inventory='{inventory_str}' WHERE auth={auth}")
        self.conn.commit()
    
    async def setBalance(self, auth: int, balance):
        self.cur.execute(f"UPDATE users SET balance={balance} WHERE auth={auth}")
        self.conn.commit()
        
    async def openPack(self, auth: int):
        self.cur.execute(f"UPDATE users SET packs_open=packs_open+1 WHERE auth={auth}")
        self.conn.commit()

main_db = DB()